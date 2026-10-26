"""Aggregates per-hour audit runs into one multi-hour summary.

usage: python3 -I aggregate.py OUT_DIR RUN_DIR [RUN_DIR ...]
writes OUT_DIR/pool_shares.csv, OUT_DIR/hourly.csv, OUT_DIR/audit.json, OUT_DIR/report.md
"""
import collections
import csv
import gzip
import json
import math
import os
import random
import sys

REPORTED = ["HumPool", "F2Pool", "ViaBTC", "K1Pool", "WhalePool", "SOLO", "UNKNOWN"]
CLAIM = 0.539
SEED = "kaspa-audit/aggregate"


def wilson(k, n, z=1.959963984540054):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def pct(x):
    return f"{100 * x:.2f}%"


def read_blocks(run):
    for name in ("blocks.csv", "blocks.csv.gz"):
        p = os.path.join(run, "results", name)
        if os.path.exists(p):
            f = gzip.open(p, "rt") if name.endswith(".gz") else open(p)
            with f:
                yield from csv.DictReader(f)
            return
    raise FileNotFoundError(run)


def main():
    out, runs = sys.argv[1], sorted(sys.argv[2:])
    os.makedirs(out, exist_ok=True)
    seen = set()
    dups = 0
    hourly = []
    blue_by_pool = collections.Counter()
    all_by_pool = collections.defaultdict(collections.Counter)
    reward_by_pool = collections.Counter()
    addr_blue = collections.Counter()
    colors = collections.Counter()
    checks = collections.Counter()
    unknown_addr = collections.Counter()
    for run in runs:
        a = json.load(open(os.path.join(run, "results", "audit.json")))
        hb = collections.Counter()
        n_blue = 0
        for r in read_blocks(run):
            if r["hash"] in seen:
                dups += 1
                continue
            seen.add(r["hash"])
            colors[r["blockColor"]] += 1
            all_by_pool[r["pool"]][r["blockColor"]] += 1
            if r["pool"] == "UNKNOWN":
                unknown_addr[r["minerAddress"]] += 1
            if r["blockColor"] == "BLUE":
                n_blue += 1
                hb[r["pool"]] += 1
                blue_by_pool[r["pool"]] += 1
                reward_by_pool[r["pool"]] += int(r["rewardAmount"])
                addr_blue[r["minerAddress"]] += 1
        sec = a["enumeration"]["secondary_enumeration"]
        sv = a["sample_verification"]["checks"]
        checks["hours"] += 1
        checks["blocks"] += a["window_completeness"]["blocks_in_window"]
        checks["reward_info_failed"] += a["reward_info"]["failed_after_retries"]
        checks["parse_or_consistency_errors"] += sum(a["errors"].values())
        checks["payout_cross_check_match"] += a["payout_cross_check_all_blue_blocks"].get("match", 0)
        checks["payout_cross_check_other"] += sum(v for k, v in a["payout_cross_check_all_blue_blocks"].items() if k != "match")
        checks["secondary_enum_differences"] += sec["in_primary_not_secondary"] + sec["in_secondary_not_primary"]
        checks["sample_files"] += a["sample_verification"]["files"]
        checks["sample_check_failures"] += sum(v for k, v in sv.items() if k.endswith("=False"))
        checks["pages_contiguous_false"] += 0 if a["enumeration"]["pages_contiguous"] else 1
        k2 = hb["HumPool"] + hb["F2Pool"]
        hourly.append({
            "start": a["window"]["start"], "end": a["window"]["end"], "primary_node": a["sources"]["primary_node"],
            "secondary_node": a["sources"]["secondary_node"], "blocks": a["window_completeness"]["blocks_in_window"],
            "blue": n_blue, "red": a["colors"]["RED"], "unknown_color": a["colors"]["UNKNOWN"],
            "HumPool": hb["HumPool"], "F2Pool": hb["F2Pool"], "HumPool+F2Pool": k2, "share_HumPool+F2Pool": round(k2 / n_blue, 6),
            "share_HumPool": round(hb["HumPool"] / n_blue, 6), "share_F2Pool": round(hb["F2Pool"] / n_blue, 6),
            "share_UNKNOWN": round(hb["UNKNOWN"] / n_blue, 6),
        })

    n = colors["BLUE"]
    total_reward = sum(reward_by_pool.values())
    rng = random.Random(SEED)
    boots = []
    for _ in range(10000):
        k = m = 0
        for _ in hourly:
            h = rng.choice(hourly)
            k += h["HumPool+F2Pool"]
            m += h["blue"]
        boots.append(k / m)
    boots.sort()
    k2 = blue_by_pool["HumPool"] + blue_by_pool["F2Pool"]
    shares_h = [h["share_HumPool+F2Pool"] for h in hourly]

    rows = []
    for p in sorted(all_by_pool, key=lambda p: -blue_by_pool[p]) + [p for p in REPORTED if p not in all_by_pool]:
        k = blue_by_pool[p]
        lo, hi = wilson(k, n)
        c = all_by_pool.get(p, collections.Counter())
        rows.append({"pool": p, "reported_separately": p in REPORTED, "blocks_all_colors": sum(c.values()), "blue_blocks": k,
                     "red_blocks": c["RED"], "unknown_color_blocks": c["UNKNOWN"], "share_of_confirmed_blue": round(k / n, 6),
                     "wilson95_low": round(lo, 6), "wilson95_high": round(hi, 6), "confirmed_reward_KAS": round(reward_by_pool[p] / 1e8, 8),
                     "share_of_confirmed_reward": round(reward_by_pool[p] / total_reward, 6)})
    lo2, hi2 = wilson(k2, n)
    rows.append({"pool": "HumPool+F2Pool", "reported_separately": True,
                 "blocks_all_colors": sum(all_by_pool["HumPool"].values()) + sum(all_by_pool["F2Pool"].values()), "blue_blocks": k2,
                 "red_blocks": all_by_pool["HumPool"]["RED"] + all_by_pool["F2Pool"]["RED"],
                 "unknown_color_blocks": all_by_pool["HumPool"]["UNKNOWN"] + all_by_pool["F2Pool"]["UNKNOWN"],
                 "share_of_confirmed_blue": round(k2 / n, 6), "wilson95_low": round(lo2, 6), "wilson95_high": round(hi2, 6),
                 "confirmed_reward_KAS": round((reward_by_pool["HumPool"] + reward_by_pool["F2Pool"]) / 1e8, 8),
                 "share_of_confirmed_reward": round((reward_by_pool["HumPool"] + reward_by_pool["F2Pool"]) / total_reward, 6)})
    rows.append({"pool": "TOTAL", "reported_separately": True, "blocks_all_colors": sum(colors.values()), "blue_blocks": n,
                 "red_blocks": colors["RED"], "unknown_color_blocks": colors["UNKNOWN"], "share_of_confirmed_blue": 1.0,
                 "wilson95_low": "", "wilson95_high": "", "confirmed_reward_KAS": round(total_reward / 1e8, 8), "share_of_confirmed_reward": 1.0})
    with open(os.path.join(out, "pool_shares.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(out, "hourly.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(hourly[0]))
        w.writeheader()
        w.writerows(hourly)

    top = addr_blue.most_common(3)
    summary = {
        "runs": runs, "hours": len(hourly), "first_start": hourly[0]["start"], "last_end": hourly[-1]["end"],
        "contiguous_hours": all(a["end"] == b["start"] for a, b in zip(hourly, hourly[1:])),
        "duplicates_across_runs": dups, "colors": dict(colors), "verification_totals": dict(checks),
        "HumPool_plus_F2Pool": {"blue": k2, "of_blue": n, "share": k2 / n, "wilson95": [lo2, hi2],
                                "hour_cluster_bootstrap95": [boots[249], boots[9750]],
                                "hourly_min": min(shares_h), "hourly_max": max(shares_h),
                                "hours_above_50pct": sum(s > 0.5 for s in shares_h),
                                "hours_with_share_at_or_below_claim": sum(s <= CLAIM for s in shares_h),
                                "claim_0539_inside_wilson95": lo2 <= CLAIM <= hi2},
        "top_addresses": [{"address": a, "blue": c, "share": c / n} for a, c in top],
        "top2_addresses_share": sum(c for _, c in top[:2]) / n,
        "unknown_addresses": [{"address": a, "blocks": c} for a, c in unknown_addr.most_common(15)],
    }
    json.dump(summary, open(os.path.join(out, "audit.json"), "w"), indent=2)

    L = [f"# Kaspa mining distribution: {len(hourly)} audited hours ({hourly[0]['start']} – {hourly[-1]['end']})\n"]
    hp = summary["HumPool_plus_F2Pool"]
    L.append(f"- Contiguous hours: {summary['contiguous_hours']}. Blocks: {sum(colors.values())} (BLUE {colors['BLUE']}, RED {colors['RED']}, UNKNOWN {colors['UNKNOWN']}).")
    L.append(f"- **HumPool + F2Pool: {k2} of {n} BLUE blocks = {pct(hp['share'])}** (Wilson 95% CI {pct(lo2)}–{pct(hi2)}; "
             f"hour-cluster bootstrap 95% CI {pct(boots[249])}–{pct(boots[9750])}).")
    L.append(f"- Hourly range {pct(hp['hourly_min'])}–{pct(hp['hourly_max'])}; above 50% in {hp['hours_above_50pct']}/{len(hourly)} hours; "
             f"at or below the claimed 53.9% in {hp['hours_with_share_at_or_below_claim']}/{len(hourly)} hours.")
    L.append(f"- Two largest miner addresses: {pct(summary['top2_addresses_share'])} of BLUE blocks ({', '.join(a for a, _ in top[:2])}).")
    L.append(f"- Verification totals: {dict(checks)}\n")
    L.append("| pool | BLUE | share of BLUE | Wilson 95% CI | share of reward |")
    L.append("|---|---|---|---|---|")
    for r in rows:
        if r["pool"] in REPORTED + ["HumPool+F2Pool", "TOTAL"]:
            ci = f"{pct(r['wilson95_low'])}–{pct(r['wilson95_high'])}" if r["wilson95_low"] != "" else ""
            L.append(f"| {r['pool']} | {r['blue_blocks']} | {pct(r['share_of_confirmed_blue'])} | {ci} | {pct(r['share_of_confirmed_reward'])} |")
    L.append("\n| hour (UTC) | blocks | BLUE | HumPool | F2Pool | HumPool+F2Pool | UNKNOWN |")
    L.append("|---|---|---|---|---|---|---|")
    for h in hourly:
        L.append(f"| {h['start'][:16]} | {h['blocks']} | {h['blue']} | {pct(h['share_HumPool'])} | {pct(h['share_F2Pool'])} | "
                 f"**{pct(h['share_HumPool+F2Pool'])}** | {pct(h['share_UNKNOWN'])} |")
    open(os.path.join(out, "report.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
