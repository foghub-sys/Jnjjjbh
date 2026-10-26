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
- Public nodes keep about 40 hours of history, so a 7-day analysis needs an archival node or an indexer. Because these blocks will drop out of the public nodes' history, every hour's raw node data is committed (see Reproduce below).
- An initial run failed for two hours because the REST indexer returned HTTP 429 while locating the start block. Those hours were re-run successfully; no block data was affected.

## Reproduce

The 56.73% is reproducible offline from the committed raw node responses, with no network access:

```
audit/tools/reproduce.sh /tmp/repro      # about 3 minutes; needs python3 only
```

The script re-runs `analyze.py` on every hour's `runs/<hour>/raw/` and then `aggregate.py` on the 24 rebuilt hours. A check run of this script gave byte-identical `blocks.csv` and `pool_shares.csv` for all 24 hours, identical per-hour `audit.json`, and an identical 24-hour `pool_shares.csv` and `hourly.csv`. The summary `audit.json` differs only in the input paths it records.

Raw data per hour, in `runs/<hour>/raw/`:

| file | content |
|---|---|
| `dag_blocks.jsonl.gz` | every block returned by `getBlocks` for the hour ±10 min: header without `parentsByLevel` (level-0 parents kept), verboseData, and the full coinbase transaction |
| `reward_info.jsonl.gz` | `GetBlockRewardInfo` result for every window block, with the sha256 of each verbatim response |
| `pages.jsonl` | every `getBlocks` page: lowHash, highHash, count, and the byte size and sha256 of the verbatim response |
| `collect_meta.json` | node, server version, DAG info at start and end, start-block lookup, retries and failures |
| `verify/enum_secondary.json.gz` | the block-hash set re-enumerated on the second node |
| `verify/raw_samples/*.json.gz` | verbatim `getBlock` and `GetBlockRewardInfo` responses from both nodes, the merging chain block, and the REST indexer record, for 128 sampled blocks |
| `sample_hashes.txt`, `address_names.json` | the reproducible sample and the explorer label list used |

In `dag_blocks.jsonl.gz` the header `nonce` went through JavaScript number parsing and can be imprecise. It is not used by the analysis. Exact headers, including the nonce, are in the verbatim raw samples, where the block hash is recomputed.

To re-collect from the network instead: `audit/tools/batch.sh 2026-10-25T08:00:00Z 24` (needs Node.js and `ws@8.18.0`). This works only while those hours are still within the public nodes' pruning window, about 40 hours.
