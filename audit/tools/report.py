"""Renders report.md from audit.json + pool_shares.csv of one or more audited windows.

usage: python3 -I report.py OUT.md RESULTS_DIR [RESULTS_DIR ...]   (first dir = primary window)
"""
import csv
import json
import os
import sys

POOLS = ["HumPool", "F2Pool", "ViaBTC", "K1Pool", "WhalePool", "SOLO", "UNKNOWN", "HumPool+F2Pool"]


def pct(x):
    return f"{100 * float(x):.2f}%"


def load(d):
    a = json.load(open(os.path.join(d, "audit.json")))
    shares = {r["pool"]: r for r in csv.DictReader(open(os.path.join(d, "pool_shares.csv")))}
    return a, shares


def main():
    out, dirs = sys.argv[1], sys.argv[2:]
    runs = [load(d) for d in dirs]
    a, shares = runs[0]
    res = a["results"]["HumPool_plus_F2Pool"]
    comp, enum, colors = a["window_completeness"], a["enumeration"], a["colors"]
    sec = enum.get("secondary_enumeration") or {}
    hum = a["humpool_address_check"]
    sv = a["sample_verification"]
    L = []
    w = L.append

    verdict_inside = res["claim_0539_inside_wilson95"]
    w(f"# Kaspa mining distribution audit: {a['window']['start']} – {a['window']['end']}\n")
    w("## Verdict\n")
    w(f"- HumPool + F2Pool produced **{res['blue']} of {a['results']['blue_blocks']} confirmed BLUE blocks = {pct(res['share'])}** "
      f"(Wilson 95% CI {pct(res['wilson95'][0])}–{pct(res['wilson95'][1])}; minute-cluster bootstrap 95% CI "
      f"{pct(res['minute_bootstrap95'][0])}–{pct(res['minute_bootstrap95'][1])}).")
    w(f"- The claimed 53.9% is **{'inside' if verdict_inside else 'outside'}** the 95% interval; difference "
      f"{res['difference_pp']:+.2f} percentage points.")
    over50 = res["wilson95"][0] > 0.5
    w(f"- That the two pools' blocks exceed 50% in this window is **{'supported (whole CI above 50%)' if over50 else 'not established'}**.")
    if len(runs) > 1:
        w("- Other audited windows (same method):\n")
        w("| window | blocks | BLUE | HumPool | F2Pool | HumPool+F2Pool | 95% CI (Wilson) |")
        w("|---|---|---|---|---|---|---|")
        for ra, rs in runs:
            r2 = ra["results"]["HumPool_plus_F2Pool"]
            w(f"| {ra['window']['start']} – {ra['window']['end']} | {ra['window_completeness']['blocks_in_window']} | {ra['results']['blue_blocks']} | "
              f"{pct(rs['HumPool']['share_of_confirmed_blue'])} | {pct(rs['F2Pool']['share_of_confirmed_blue'])} | **{pct(r2['share'])}** | "
              f"{pct(r2['wilson95'][0])}–{pct(r2['wilson95'][1])} |")
    w("")

    w("## Three claims, kept apart\n")
    top = a["results"]["top_addresses_by_blue_blocks"]
    w(f"1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses "
      f"({top[0]['address']} [{top[0]['label']}], {top[1]['address']} [{top[1]['label']}]) produced "
      f"{pct(a['results']['top2_addresses_share'])} of BLUE blocks in this window.")
    w("2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show "
      "where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is "
      "the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure "
      "and who controls the hashrate.")
    w("3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require "
      "sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.\n")

    w("## Shares (denominator: all confirmed BLUE blocks in the window)\n")
    w("| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |")
    w("|---|---|---|---|---|---|---|---|")
    for p in POOLS:
        r = shares.get(p)
        if not r:
            continue
        ci = f"{pct(r['wilson95_low'])}–{pct(r['wilson95_high'])}" if r["wilson95_low"] else ""
        w(f"| {p} | {r['blue_blocks']} | {r['red_blocks']} | {r['unknown_color_blocks']} | {pct(r['share_of_confirmed_blue'])} | {ci} | "
          f"{float(r['confirmed_reward_KAS']):,.2f} | {pct(r['share_of_confirmed_reward'])} |")
    w("\nAll other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). "
      "UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:\n")
    for u in a["results"]["unknown_addresses"]:
        w(f"- {u['address']}: {u['blocks']} blocks, e.g. minerInfo `{u['sample_minerInfo']}`")
    w("")

    w("## HumPool address check\n")
    w(f"- Address `{hum['address']}` is the miner address committed in the block's own coinbase payload of "
      f"**{hum['blocks_with_this_miner_address']}** window blocks ({hum['blue_blocks_with_this_miner_address']} BLUE).")
    w(f"- Payload tags seen with it: " + "; ".join(f"`{k}` ×{v}" for k, v in hum["tags_seen_with_this_address"].items()))
    w(f"- Addresses used by blocks tagged `humpool`: " + ", ".join(f"{k} ×{v}" for k, v in hum["addresses_of_blocks_tagged_humpool"].items()))
    w(f"- Addresses used by blocks tagged `F2Pool`: " + ", ".join(f"{k} ×{v}" for k, v in hum["addresses_of_blocks_tagged_f2pool"].items()))
    w(f"- Explorer label (third-party, secondary): `{hum['explorer_label']}`.")
    w(f"- For comparison only (not used): this address appears in {hum['illustration_only_coinbase_outputs_paying_this_address_in_window_chain_blocks']} "
      "coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.\n")

    w("## Method\n")
    w(f"- Primary source: rusty-kaspa node `{a['sources']['primary_node']}` (version {a['sources']['primary_serverInfo']['serverVersion']}, synced, wRPC JSON). "
      f"All blocks were paged with `getBlocks` from `{enum['paging_start_lowHash']}`, which returns every block merged by the selected chain, blue and red, not only chain blocks. "
      f"Margin of {enum['margin_seconds']}s on each side; {enum['pages']} pages, contiguous: {enum['pages_contiguous']}.")
    w("- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload "
      "(committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.")
    w("- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.")
    w(f"- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the "
      f"payload script with the reported reward. Result: {a['payout_cross_check_all_blue_blocks']}.")
    w(f"- Independent enumeration on second node `{sec.get('node')}`: {sec.get('secondary_count')} vs {sec.get('primary_count')} hashes; "
      f"only-in-primary {sec.get('in_primary_not_secondary')}, only-in-secondary {sec.get('in_secondary_not_primary')}, "
      f"window blocks missing on secondary {sec.get('window_blocks_missing_from_secondary')}.")
    w(f"- Reproducible random sample: {sv['files']} blocks, `{sv['selection']}`, seed `{sv['seed']}`. Verbatim raw responses from both nodes and the REST indexer "
      f"are in `raw/verify/raw_samples/`. Checks: {sv['checks']}.")
    w("- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. "
      "The realised count for the window is exact; the intervals describe the underlying hashrate share.\n")

    w("## Completeness and errors\n")
    w(f"- Window blocks: {comp['blocks_in_window']} ({comp['blocks_per_second']} blocks/s), first {comp['first_timestamp']}, last {comp['last_timestamp']}; "
      f"per-minute min/max {comp['blocks_per_minute_min_max']}; {comp['minutes_with_blocks']} minutes with blocks; "
      f"largest timestamp gap {comp['largest_timestamp_gaps_ms'][0]['gap_ms']} ms.")
    w(f"- Boundary counts: {comp['boundary_counts']}. Blocks outside the window by timestamp but inside its DAA-score range: "
      f"{comp['blocks_outside_window_by_timestamp_but_inside_window_daa_range']}.")
    w(f"- Colors: BLUE {colors['BLUE']}, RED {colors['RED']}, UNKNOWN {colors['UNKNOWN']}. GetBlockRewardInfo failures after retries: "
      f"{a['reward_info']['failed_after_retries']}; transient errors retried: {a['reward_info']['transient_errors_retried']}.")
    w(f"- Duplicates removed: {enum['duplicates_removed_dag']} (getBlocks pages repeat their lowHash), reward-info duplicates {enum['duplicates_removed_reward_info']}. Parse/consistency errors: {a['errors'] or 'none'}.\n")

    w("## Limitations\n")
    w("- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.")
    w("- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.")
    w("- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.")
    w("- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.")
    open(out, "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
