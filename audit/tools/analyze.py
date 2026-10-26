"""Builds blocks.csv, pool_shares.csv and audit.json from the raw collection.

usage: python3 -I analyze.py --collect DIR --verify DIR --names address_names.json --out DIR
       --start 2026-10-26T12:00:00Z --end 2026-10-26T13:00:00Z
"""
import argparse
import collections
import csv
import datetime as dt
import glob
import gzip
import hashlib
import json
import math
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kaspa import header_hash, parse_coinbase_payload  # noqa: E402

CLAIM_ADDRESS = "kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j"
CLAIM_SHARE = 0.539
SAMPLE_SEED = "kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z"
SAMPLE_SIZE = 128
# An untagged, unlabelled address producing at least this share of window blocks is not presumed solo.
SOLO_MAX_ADDRESS_SHARE = 0.01
REPORTED_POOLS = ["HumPool", "F2Pool", "ViaBTC", "K1Pool", "WhalePool", "SOLO", "UNKNOWN"]

# Pool tags searched for in the block's own coinbase payload extra data (minerInfo), case-insensitive.
POOL_TAGS = [
    ("HumPool", r"humpool"),
    ("F2Pool", r"f2pool"),
    ("ViaBTC", r"viabtc"),
    ("K1Pool", r"k1pool"),
    ("WhalePool", r"whalepool|(^|/)wpool"),
    ("Kaspa-pool", r"kaspa-pool\.org"),
    ("EMCD", r"emcd"),
    ("2Miners", r"2miners"),
    ("AntPool", r"antpool"),
    ("HeroMiners", r"herominers"),
    ("Kryptex", r"kryptex"),
    ("Binance Pool", r"(^|/)bpool"),
    ("WoolyPooly", r"woolypooly"),
    ("CyberPool", r"cyberpool"),
    ("RabidPool", r"rabidpool"),
    ("BaikalMine", r"baikalmine"),
    ("NiceHash", r"nicehash"),
    ("Kat Pool", r"katpool"),
    ("SoloPool.org", r"solopool"),
    ("Zergpool", r"zergpool"),
    ("DxPool", r"dxpool"),
    ("GoGPool", r"gogpool"),
]
# Explorer labels (kaspa-rest-server /addresses/names) are mapped to the same canonical names.
LABEL_ALIASES = {"Whalepool": "WhalePool", "Kaspa-pool": "Kaspa-pool", "ANTPOOL": "AntPool"}


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def tag_pool(miner_info):
    for name, rx in POOL_TAGS:
        if re.search(rx, miner_info, re.I):
            return name
    return None


def load_jsonl_gz(path):
    with gzip.open(path, "rt") as f:
        return [json.loads(line) for line in f]


def main():
    ap = argparse.ArgumentParser()
    for a in ("collect", "verify", "names", "out", "start", "end"):
        ap.add_argument("--" + a, required=True)
    args = ap.parse_args()
    start = int(dt.datetime.fromisoformat(args.start.replace("Z", "+00:00")).timestamp() * 1000)
    end = int(dt.datetime.fromisoformat(args.end.replace("Z", "+00:00")).timestamp() * 1000)
    os.makedirs(args.out, exist_ok=True)

    meta = json.load(open(os.path.join(args.collect, "collect_meta.json")))
    pages = [json.loads(l) for l in open(os.path.join(args.collect, "pages.jsonl"))]
    dag_raw = load_jsonl_gz(os.path.join(args.collect, "dag_blocks.jsonl.gz"))
    rewards_raw = load_jsonl_gz(os.path.join(args.collect, "reward_info.jsonl.gz"))
    names = json.load(open(args.names))
    label_of = {x["address"]: LABEL_ALIASES.get(x["name"], x["name"]) for x in names}

    # ---- dedupe ----
    dag, dup_dag = {}, 0
    for r in dag_raw:
        h = r["header"]["hash"]
        if h in dag:
            dup_dag += 1
            continue
        dag[h] = r
    rewards, dup_rw = {}, 0
    for r in rewards_raw:
        if r["hash"] in rewards:
            dup_rw += 1
            continue
        rewards[r["hash"]] = r

    # ---- window selection by header timestamp ----
    window = sorted((h for h, r in dag.items() if start <= r["header"]["timestamp"] < end),
                    key=lambda h: (dag[h]["header"]["daaScore"], dag[h]["header"]["timestamp"], h))
    wset = set(window)

    # ---- per-block parsing ----
    errors = collections.Counter()
    rows = []
    for h in window:
        r = dag[h]
        hd, vd, cb = r["header"], r["verboseData"], r["coinbase"]
        row = {
            "hash": h, "timestamp_ms": hd["timestamp"], "timestamp_utc": iso(hd["timestamp"]),
            "daaScore": hd["daaScore"], "blueScore": hd["blueScore"], "difficulty": vd["difficulty"], "bits": hd["bits"],
            "isChainBlock": vd["isChainBlock"],
        }
        try:
            p = parse_coinbase_payload(cb["payload"])
            row["minerAddress"] = p["minerAddress"] or ""
            row["minerScript"] = p["script"].hex()
            row["minerInfo"] = p["minerInfo"]
            row["payloadBlueScoreMatchesHeader"] = p["blueScore"] == hd["blueScore"]
            if not p["minerAddress"]:
                errors["non_standard_miner_script"] += 1
            if p["blueScore"] != hd["blueScore"]:
                errors["payload_blue_score_mismatch"] += 1
        except Exception as e:  # noqa: BLE001
            errors["payload_parse_error"] += 1
            row.update(minerAddress="", minerScript="", minerInfo="", payloadBlueScoreMatchesHeader="", parseError=str(e))
        rw = rewards.get(h)
        if rw is None:
            row.update(blockColor="UNKNOWN", colorSource="missing_rpc_response", rewardAmount="", mergingChainBlockHash="", confirmationCount="")
            errors["reward_info_missing"] += 1
        else:
            color = {"blue": "BLUE", "red": "RED"}.get(rw["blockColor"], "UNKNOWN")
            row.update(blockColor=color, colorSource="GetBlockRewardInfo", rewardAmount=rw.get("rewardAmount") if rw.get("rewardAmount") is not None else "",
                       mergingChainBlockHash=rw.get("mergingChainBlockHash") or "", confirmationCount=rw.get("confirmationCount") if rw.get("confirmationCount") is not None else "")
            if rw["headerHash"] != h:
                errors["reward_info_header_hash_mismatch"] += 1
        rows.append(row)

    # ---- consensus check of the payload miner script ----
    # A blue block's reward is paid by its merging chain block's coinbase, output index == position in mergeSetBluesHashes,
    # to the script the blue block committed to in its own payload. This ties minerAddress to consensus-validated data.
    mcheck = collections.Counter()
    for row in rows:
        if row["blockColor"] != "BLUE":
            continue
        m = dag.get(row["mergingChainBlockHash"])
        if m is None:
            mcheck["merging_chain_block_not_in_dataset"] += 1
            row["payoutCrossCheck"] = "not_checked"
            continue
        blues = m["verboseData"]["mergeSetBluesHashes"]
        if row["hash"] not in blues:
            mcheck["not_in_mergeset_blues"] += 1
            row["payoutCrossCheck"] = "FAIL_not_in_mergeset"
            continue
        out = m["coinbase"]["outputs"][blues.index(row["hash"])]
        ok_script = out["scriptPublicKey"][4:] == row["minerScript"]
        ok_value = out["value"] == row["rewardAmount"]
        key = "match" if ok_script and ok_value else f"mismatch_script={not ok_script}_value={not ok_value}"
        mcheck[key] += 1
        row["payoutCrossCheck"] = "OK" if key == "match" else "FAIL"

    # ---- attribution ----
    addr_tags = collections.defaultdict(collections.Counter)
    for row in rows:
        addr_tags[row["minerAddress"]][tag_pool(row["minerInfo"]) or "-"] += 1
    addr_pool = {}
    for a, c in addr_tags.items():
        tagged = {k: v for k, v in c.items() if k != "-"}
        if tagged:
            top, cnt = max(tagged.items(), key=lambda x: x[1])
            if cnt / sum(c.values()) >= 0.9:
                addr_pool[a] = top
    addr_all = collections.Counter(row["minerAddress"] for row in rows)
    for row in rows:
        t = tag_pool(row["minerInfo"])
        a = row["minerAddress"]
        if not a:
            pool, basis = "UNKNOWN", "no_standard_miner_address"
        elif t:
            pool, basis = t, "payload_tag"
        elif a in addr_pool:
            pool, basis = addr_pool[a], "address_seen_with_pool_tag_in_window"
        elif a in label_of:
            pool, basis = label_of[a], "explorer_address_label"
        elif addr_all[a] / len(rows) >= SOLO_MAX_ADDRESS_SHARE:
            pool, basis = "UNKNOWN", "untagged_unlabelled_address_ge_1pct"
        else:
            pool, basis = "SOLO", "untagged_unlabelled_address_lt_1pct(heuristic)"
        row["pool"], row["attributionBasis"] = pool, basis
        row["explorerLabel"] = label_of.get(a, "")
        if t and a in label_of and label_of[a] != t:
            errors["tag_vs_explorer_label_conflict"] += 1

    # ---- shares ----
    color_counts = collections.Counter(r["blockColor"] for r in rows)
    blue = [r for r in rows if r["blockColor"] == "BLUE"]
    n_blue = len(blue)
    total_blue_reward = sum(r["rewardAmount"] for r in blue)
    per_pool = collections.defaultdict(lambda: collections.Counter())
    reward_pool = collections.Counter()
    for r in rows:
        per_pool[r["pool"]][r["blockColor"]] += 1
        if r["blockColor"] == "BLUE":
            reward_pool[r["pool"]] += r["rewardAmount"]

    # minute-cluster bootstrap for the combined share (accounts for temporal clustering of block discovery)
    minute = lambda r: (r["timestamp_ms"] - start) // 60000  # noqa: E731
    mins = collections.defaultdict(lambda: [0, 0])
    for r in blue:
        mins[minute(r)][1] += 1
        if r["pool"] in ("HumPool", "F2Pool"):
            mins[minute(r)][0] += 1
    keys = sorted(mins)
    rng = random.Random(SAMPLE_SEED)
    boots = []
    for _ in range(10000):
        k = n = 0
        for _ in keys:
            a, b = mins[rng.choice(keys)]
            k += a
            n += b
        boots.append(k / n)
    boots.sort()
    boot_ci = (boots[249], boots[9750])

    pool_rows = []
    all_pools = sorted(per_pool, key=lambda p: -per_pool[p]["BLUE"])
    for p in REPORTED_POOLS:
        if p not in per_pool:
            all_pools.append(p)
    for p in all_pools:
        c = per_pool.get(p, collections.Counter())
        k = c["BLUE"]
        lo, hi = wilson(k, n_blue)
        pool_rows.append({
            "pool": p, "reported_separately": p in REPORTED_POOLS,
            "blocks_all_colors": sum(c.values()), "blue_blocks": k, "red_blocks": c["RED"], "unknown_color_blocks": c["UNKNOWN"],
            "share_of_confirmed_blue": round(k / n_blue, 6) if n_blue else "",
            "wilson95_low": round(lo, 6), "wilson95_high": round(hi, 6),
            "confirmed_reward_sompi": reward_pool[p], "confirmed_reward_KAS": round(reward_pool[p] / 1e8, 8),
            "share_of_confirmed_reward": round(reward_pool[p] / total_blue_reward, 6) if total_blue_reward else "",
        })
    k2 = per_pool["HumPool"]["BLUE"] + per_pool["F2Pool"]["BLUE"]
    lo2, hi2 = wilson(k2, n_blue)
    combined = {
        "pool": "HumPool+F2Pool", "reported_separately": True,
        "blocks_all_colors": sum(per_pool["HumPool"].values()) + sum(per_pool["F2Pool"].values()),
        "blue_blocks": k2, "red_blocks": per_pool["HumPool"]["RED"] + per_pool["F2Pool"]["RED"],
        "unknown_color_blocks": per_pool["HumPool"]["UNKNOWN"] + per_pool["F2Pool"]["UNKNOWN"],
        "share_of_confirmed_blue": round(k2 / n_blue, 6), "wilson95_low": round(lo2, 6), "wilson95_high": round(hi2, 6),
        "confirmed_reward_sompi": reward_pool["HumPool"] + reward_pool["F2Pool"],
        "confirmed_reward_KAS": round((reward_pool["HumPool"] + reward_pool["F2Pool"]) / 1e8, 8),
        "share_of_confirmed_reward": round((reward_pool["HumPool"] + reward_pool["F2Pool"]) / total_blue_reward, 6),
    }
    pool_rows.append(combined)
    pool_rows.append({"pool": "TOTAL", "reported_separately": True, "blocks_all_colors": len(rows), "blue_blocks": n_blue,
                      "red_blocks": color_counts["RED"], "unknown_color_blocks": color_counts["UNKNOWN"], "share_of_confirmed_blue": 1.0,
                      "wilson95_low": "", "wilson95_high": "", "confirmed_reward_sompi": total_blue_reward,
                      "confirmed_reward_KAS": round(total_blue_reward / 1e8, 8), "share_of_confirmed_reward": 1.0})

    # ---- address-level view (claim 1 is about addresses, not operators) ----
    addr_blue = collections.Counter(r["minerAddress"] for r in blue)
    top_addr = addr_blue.most_common(5)
    hum_rows = [r for r in rows if r["minerAddress"] == CLAIM_ADDRESS]
    hum_tags = collections.Counter(r["minerInfo"] for r in hum_rows)
    hum_pool_addrs = collections.Counter(r["minerAddress"] for r in rows if r["pool"] == "HumPool")
    f2_addrs = collections.Counter(r["minerAddress"] for r in rows if r["pool"] == "F2Pool")

    # Illustration only (NOT evidence of authorship): what a coinbase-recipient count would give.
    payout_outputs = collections.Counter()
    for r in rows:
        if r["isChainBlock"]:
            for o in dag[r["hash"]]["coinbase"]["outputs"]:
                payout_outputs[o["verboseData"]["scriptPublicKeyAddress"]] += 1

    # ---- completeness: boundaries, gaps, page continuity, secondary enumeration ----
    ts_sorted = sorted(r["timestamp_ms"] for r in rows)
    gaps = sorted(((b - a, a) for a, b in zip(ts_sorted, ts_sorted[1:])), reverse=True)[:5]
    per_min = collections.Counter((t - start) // 60000 for t in ts_sorted)
    near = lambda lo, hi: sum(1 for r in dag.values() if lo <= r["header"]["timestamp"] < hi)  # noqa: E731
    daa_in = [r["daaScore"] for r in rows]
    daa_lo, daa_hi = min(daa_in), max(daa_in)
    outside_in_daa = sum(1 for h, r in dag.items() if h not in wset and daa_lo <= r["header"]["daaScore"] <= daa_hi)
    page_chain_ok = all(p["lowHash"] == prev["highHash"] for prev, p in zip(pages, pages[1:]))

    sec = {}
    enum_path = os.path.join(args.verify, "enum_secondary.json")
    if os.path.exists(enum_path):
        e = json.load(open(enum_path))
        sec_set = set(e["hashes"])
        prim_set = set(dag)
        sec = {
            "node": e["node"], "serverInfo": e["serverInfo"], "pages": e["pages"], "reachedUntil": e["reachedUntil"],
            "secondary_count": len(sec_set), "primary_count": len(prim_set),
            "in_primary_not_secondary": len(prim_set - sec_set), "in_secondary_not_primary": len(sec_set - prim_set),
            "window_blocks_missing_from_secondary": len(wset - sec_set),
            "examples_secondary_only": sorted(sec_set - prim_set)[:10],
        }

    # ---- sample verification from verbatim raw responses ----
    sample_res = collections.Counter()
    sample_details = []
    for path in sorted(glob.glob(os.path.join(args.verify, "raw_samples", "*.json"))):
        rec = json.load(open(path))
        h = rec["hash"]
        res = {"hash": h}
        blocks = [(x["node"], json.loads(x["raw"])["params"]["block"]) for x in rec["responses"] if x["method"] == "getBlock" and x.get("role") != "mergingChainBlock"]
        infos = [(x["node"], json.loads(x["raw"])["params"]) for x in rec["responses"] if x["method"] == "getBlockRewardInfo"]
        merging = [json.loads(x["raw"])["params"]["block"] for x in rec["responses"] if x.get("role") == "mergingChainBlock"]
        rest = [json.loads(x["raw"]) for x in rec["responses"] if x["node"].startswith("http")]
        res["header_hash_recomputed_ok"] = all(header_hash(b["header"]) == h for _, b in blocks) and bool(blocks)
        res["nodes_agree_block"] = len({json.dumps([b["header"], b["transactions"][0]["payload"]], sort_keys=True) for _, b in blocks}) == 1
        res["nodes_agree_reward_info"] = len({json.dumps([i["blockColor"], i.get("mergingChainBlockHash"), i.get("rewardAmount")]) for _, i in infos}) == 1
        res["nodes_responding"] = len(blocks)
        if rest:
            res["rest_payload_matches"] = rest[0]["transactions"][0]["payload"] == blocks[0][1]["transactions"][0]["payload"]
        if merging and infos and infos[0][1]["blockColor"] == "blue":
            mb = merging[0]
            idx = mb["verboseData"]["mergeSetBluesHashes"].index(h)
            out = mb["transactions"][0]["outputs"][idx]
            pay = parse_coinbase_payload(blocks[0][1]["transactions"][0]["payload"])
            res["merging_coinbase_pays_payload_script"] = out["scriptPublicKey"][4:] == pay["script"].hex() and out["value"] == infos[0][1]["rewardAmount"]
            res["merging_chain_hash_recomputed_ok"] = header_hash(mb["header"]) == mb["header"]["hash"]
        pr = next((r for r in rows if r["hash"] == h), None)
        if pr and blocks:
            pay = parse_coinbase_payload(blocks[0][1]["transactions"][0]["payload"])
            res["csv_row_matches_raw"] = pay["minerAddress"] == pr["minerAddress"] and pay["minerInfo"] == pr["minerInfo"] and infos[0][1]["blockColor"].upper() == pr["blockColor"]
        for k, v in res.items():
            if isinstance(v, bool):
                sample_res[f"{k}={v}"] += 1
        sample_details.append(res)

    # ---- write blocks.csv ----
    cols = ["hash", "timestamp_ms", "timestamp_utc", "daaScore", "blueScore", "difficulty", "bits", "minerAddress", "minerInfo",
            "pool", "attributionBasis", "explorerLabel", "blockColor", "colorSource", "rewardAmount", "mergingChainBlockHash",
            "isChainBlock", "confirmationCount", "payloadBlueScoreMatchesHeader", "payoutCrossCheck"]
    with open(os.path.join(args.out, "blocks.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with open(os.path.join(args.out, "pool_shares.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(pool_rows[0].keys()))
        w.writeheader()
        w.writerows(pool_rows)

    audit = {
        "claim": {"text": "HumPool and F2Pool jointly produce 53.9% of Kaspa blocks", "share": CLAIM_SHARE, "address_checked": CLAIM_ADDRESS},
        "window": {"start": iso(start), "end": iso(end), "rule": "header.timestamp in [start, end) (miner-set timestamp, ms)"},
        "sources": {
            "primary_node": meta["node"], "primary_serverInfo": meta["serverInfo"],
            "rpc_methods": ["getBlocks(lowHash, includeBlocks=true, includeTransactions=true)", "getBlockRewardInfo(hash)", "getBlockDagInfo", "getServerInfo"],
            "rest_indexer": meta["rest"] + " (used only to locate the paging start block, for explorer address labels, and for sample cross-checks)",
            "secondary_node": sec.get("node"), "secondary_serverInfo": sec.get("serverInfo"),
            "explorer_labels": "GET /addresses/names (third-party labels, secondary evidence only)",
            "collection_started": meta["startedAt"], "collection_finished": meta["finishedAt"],
            "blockDagInfoAtStart": {k: v for k, v in meta["blockDagInfoAtStart"].items() if k not in ("tipHashes", "virtualParentHashes")},
            "blockDagInfoAtEnd": {k: v for k, v in meta["blockDagInfoAtEnd"].items() if k not in ("tipHashes", "virtualParentHashes")},
        },
        "enumeration": {
            "paging_start_lowHash": meta["locate"]["lowHash"], "paging_start_probe": meta["locate"]["probes"],
            "margin_seconds": meta["marginSec"], "pages": meta["pages"], "pages_contiguous": page_chain_ok,
            "dag_blocks_enumerated_incl_margin": len(dag), "dag_timestamp_range": meta["dagTimestampRange"],
            "duplicates_removed_dag": dup_dag + meta.get("duplicatesSkipped", 0), "duplicates_removed_reward_info": dup_rw,
            "secondary_enumeration": sec,
        },
        "window_completeness": {
            "blocks_in_window": len(rows), "first_timestamp": iso(ts_sorted[0]), "last_timestamp": iso(ts_sorted[-1]),
            "blocks_per_second": round(len(rows) / ((end - start) / 1000), 3),
            "blocks_per_minute_min_max": [min(per_min.values()), max(per_min.values())], "minutes_with_blocks": len(per_min),
            "largest_timestamp_gaps_ms": [{"gap_ms": g, "after": iso(a)} for g, a in gaps],
            "boundary_counts": {"[start-1s,start)": near(start - 1000, start), "[start,start+1s)": near(start, start + 1000),
                                "[end-1s,end)": near(end - 1000, end), "[end,end+1s)": near(end, end + 1000)},
            "window_daaScore_range": [daa_lo, daa_hi],
            "blocks_outside_window_by_timestamp_but_inside_window_daa_range": outside_in_daa,
            "note": "Blocks never merged by the selected chain (outside the past of the sink at query time) are not returned by getBlocks; the secondary-node enumeration is the cross-check.",
        },
        "colors": {"BLUE": color_counts["BLUE"], "RED": color_counts["RED"], "UNKNOWN": color_counts["UNKNOWN"],
                   "rule": "BLUE/RED only when GetBlockRewardInfo returns it; anything else kept as UNKNOWN"},
        "reward_info": {"requested": meta["inWindowFromGetBlocks"], "failed_after_retries": len(meta["rewardInfoFailed"]),
                        "transient_errors_retried": len(meta["errors"])},
        "errors": dict(errors),
        "payout_cross_check_all_blue_blocks": dict(mcheck),
        "attribution": {
            "rule": "miner = the block's own coinbase payload (script public key + extra data). Pool from payload tag; else address seen "
                    "with a pool tag in >=90% of its window blocks; else explorer label; else SOLO if the untagged, unlabelled "
                    "address produced <1% of window blocks (heuristic); else UNKNOWN (also when no standard miner address can be derived). Coinbase payout recipients are never used.",
            "basis_counts": dict(collections.Counter(r["attributionBasis"] for r in rows)),
            "pool_tag_regexes": dict(POOL_TAGS),
        },
        "results": {
            "blue_blocks": n_blue,
            "HumPool_plus_F2Pool": {"blue": k2, "share": k2 / n_blue, "wilson95": [lo2, hi2], "minute_bootstrap95": list(boot_ci),
                                    "claim_0539_inside_wilson95": lo2 <= CLAIM_SHARE <= hi2,
                                    "difference_pp": round((k2 / n_blue - CLAIM_SHARE) * 100, 3)},
            "top_addresses_by_blue_blocks": [{"address": a, "blue": c, "share": c / n_blue, "label": label_of.get(a, "")} for a, c in top_addr],
            "top2_addresses_share": sum(c for _, c in top_addr[:2]) / n_blue,
            "unknown_addresses": [{"address": a, "blocks": c, "blue": sum(1 for r in blue if r["minerAddress"] == a),
                                   "sample_minerInfo": next(r["minerInfo"] for r in rows if r["minerAddress"] == a)}
                                  for a, c in collections.Counter(r["minerAddress"] for r in rows if r["pool"] == "UNKNOWN").most_common()],
            "solo_addresses": len({r["minerAddress"] for r in rows if r["pool"] == "SOLO"}),
        },
        "humpool_address_check": {
            "address": CLAIM_ADDRESS, "blocks_with_this_miner_address": len(hum_rows),
            "blue_blocks_with_this_miner_address": sum(1 for r in hum_rows if r["blockColor"] == "BLUE"),
            "tags_seen_with_this_address": dict(hum_tags.most_common(10)),
            "addresses_of_blocks_tagged_humpool": dict(hum_pool_addrs),
            "addresses_of_blocks_tagged_f2pool": dict(f2_addrs),
            "explorer_label": label_of.get(CLAIM_ADDRESS, ""),
            "illustration_only_coinbase_outputs_paying_this_address_in_window_chain_blocks": payout_outputs[CLAIM_ADDRESS],
        },
        "sample_verification": {"seed": SAMPLE_SEED, "size_requested": SAMPLE_SIZE, "files": len(sample_details),
                                "selection": "sha256(seed + hash) ascending over all window blocks, first N",
                                "checks": dict(sample_res), "details": sample_details},
    }
    with open(os.path.join(args.out, "audit.json"), "w") as f:
        json.dump(audit, f, indent=2, default=str)
    print(json.dumps({k: audit[k] for k in ("colors", "errors", "payout_cross_check_all_blue_blocks", "results")}, indent=1, default=str))
    print(json.dumps(audit["window_completeness"], indent=1))
    print(json.dumps(audit["sample_verification"]["checks"], indent=1))
    for r in pool_rows[:25]:
        print(r["pool"], r["blue_blocks"], r["share_of_confirmed_blue"])


def pick_sample(collect_dir, start_iso, end_iso, out_path):
    start = int(dt.datetime.fromisoformat(start_iso.replace("Z", "+00:00")).timestamp() * 1000)
    end = int(dt.datetime.fromisoformat(end_iso.replace("Z", "+00:00")).timestamp() * 1000)
    hs = {r["header"]["hash"] for r in load_jsonl_gz(os.path.join(collect_dir, "dag_blocks.jsonl.gz")) if start <= r["header"]["timestamp"] < end}
    chosen = sorted(hs, key=lambda h: hashlib.sha256((SAMPLE_SEED + h).encode()).hexdigest())[:SAMPLE_SIZE]
    open(out_path, "w").write("\n".join(chosen) + "\n")
    print(len(hs), "window blocks;", len(chosen), "sampled ->", out_path)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        pick_sample(*sys.argv[2:6])
    else:
        main()
