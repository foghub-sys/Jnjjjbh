# Is it true that HumPool and F2Pool together produce 53.9% of Kaspa blocks?

**Short answer:** the two pools' combined share is above 50%, but it is not 53.9%. In every audited hour it is higher.

Over 24 consecutive hours (2026-10-25 08:00 → 2026-10-26 08:00 UTC, 863,575 blocks) the two pools produced **56.73%** of all confirmed BLUE blocks:

- 95% CI 56.62–56.83% (Wilson);
- 95% CI 56.34–57.17% from a bootstrap by hour.

Hourly values ranged from 55.21% to 59.70%. The share was above 50% in 24 of 24 hours and never at or below 53.9%. An extra hour earlier on 25 October (00:00–01:00, 56.17%) agrees. The figure of 53.9% cannot be reproduced from chain data for any of these hours.

| pool | share of BLUE blocks (24 h) | 95% CI |
|---|---|---|
| HumPool | 31.49% | 31.39–31.58% |
| F2Pool | 25.24% | 25.15–25.34% |
| **HumPool + F2Pool** | **56.73%** | **56.62–56.83%** |
| ViaBTC | 10.80% | 10.73–10.86% |
| K1Pool | 7.25% | 7.19–7.30% |
| WhalePool | 3.44% | 3.40–3.48% |
| SOLO (heuristic) | 3.43% | 3.39–3.47% |
| UNKNOWN (operator not identifiable) | 9.05% | 8.99–9.11% |

The full table and per-hour breakdown are in [`summary_24h/`](summary_24h/report.md). Per-hour deliverables are in `runs/<hour>/results/`: `blocks.csv`, `pool_shares.csv`, `audit.json` and `report.md`. The first hour audited in full is [`runs/2026-10-26T0700`](runs/2026-10-26T0700/results/report.md).

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks: confirmed on-chain.** `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` (HumPool) and `kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp` (F2Pool) are the miner addresses committed in the blocks' own coinbase payloads. Together they account for 56.73% of BLUE blocks. Each pool tag used exactly one address in every hour.
2. **Two operators control more than 50% of block production: not established.** A pool address shows who builds the templates and receives the reward. It does not show who owns the hashrate. That hashrate comes from many miners who can leave the pool. Proving operator control needs off-chain evidence.
3. **Two operators could coordinate active censorship: does not follow** from (1) or (2). This audit measures neither intent nor coordination.

## HumPool address check

The claimed address `kaspa:qrk9de…t050d57j` **matches**: it is the miner address in the block's own payload of every block tagged `humpool` (e.g. 11,273 of 11,273 in 07:00–08:00 on 26 October). No other address was used with that tag, and no other tag was used with that address. The third-party explorer label agrees (secondary evidence only). The address also appears as a coinbase *payout* recipient, but those outputs pay for earlier merged blocks, so they were not used for attribution.

## Method (summary)

- **Source:** public rusty-kaspa 2.1.0 nodes over wRPC JSON. One primary and one independent secondary node per hour, rotated across 9 nodes.
- **Collection:** every block merged by the selected chain was paged with `getBlocks` (blue and red, not only chain blocks), with a 10-minute margin on each side. The window rule is header timestamp in [start, end).
- **Miner identity:** taken from the block's own coinbase payload (committed script → address; extra data → `minerInfo`). Payout recipients were never used.
- **Colour and reward:** `GetBlockRewardInfo` for every block. RED/BLUE only if the RPC says so; otherwise UNKNOWN. Result: 0 UNKNOWN, 0 failures.
- **Consensus cross-check of every BLUE block:** its merging chain block's coinbase pays the block's payload script, at its index, with the reported reward. 862,316 / 862,316 match.
- **Second-node enumeration:** 0 differences in all 24 hours.
- **Raw responses** for 128 blocks per hour (3,072 in total), chosen reproducibly by `sha256(seed + hash)`. The block hash was recomputed from the header, and both nodes plus the REST indexer agree, with 0 failures. Files are in `runs/<hour>/raw/verify/raw_samples/`.

## Limitations

- Pool names come from miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- UNKNOWN (9%) consists of untagged addresses that change from hour to hour, all with a `ZKM1…` marker. If they belong to one operator, it would be the third-largest producer. The chain alone cannot tell.
- SOLO is a heuristic: untagged, unlabelled addresses with under 1% of the hour's blocks.
- Blocks never merged by the selected chain are not returned by `getBlocks`. Such blocks earn no reward and do not change BLUE shares.
- All nodes are part of one public resolver network. Recomputing the block hash and the consensus payout cross-check reduce, but do not remove, trust in them.
- Public nodes keep about 40 hours of history, so a 7-day analysis needs an archival node or an indexer. Full DAG dumps (`raw/dag_blocks.jsonl.gz`) are committed only for the hours 2026-10-25 00:00, 08:00, 16:00 and 2026-10-26 07:00. The other hours keep the extracted per-block data, every colour/reward response and the raw samples.
- An initial run failed for two hours because the REST indexer returned HTTP 429 while locating the start block. Those hours were re-run successfully; no block data was affected.

Reproduce: `audit/tools/batch.sh 2026-10-25T08:00:00Z 24`, then `python3 -I audit/tools/aggregate.py audit/summary_24h audit/runs/<24 hours>`. This works only while the hours are still within the nodes' pruning window.
