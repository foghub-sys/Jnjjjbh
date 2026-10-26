# Kaspa mining distribution audit: 2026-10-25T12:00:00.000Z – 2026-10-25T13:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20257 of 35884 confirmed BLUE blocks = 56.45%** (Wilson 95% CI 55.94%–56.96%; minute-cluster bootstrap 95% CI 55.92%–56.97%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.55 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.45% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11283 | 4 | 0 | 31.44% | 30.96%–31.93% | 23,257.67 | 31.37% |
| F2Pool | 8974 | 13 | 0 | 25.01% | 24.56%–25.46% | 18,576.12 | 25.06% |
| ViaBTC | 4223 | 7 | 0 | 11.77% | 11.44%–12.11% | 8,737.76 | 11.79% |
| K1Pool | 2517 | 3 | 0 | 7.01% | 6.75%–7.28% | 5,186.98 | 7.00% |
| WhalePool | 1217 | 0 | 0 | 3.39% | 3.21%–3.58% | 2,508.19 | 3.38% |
| SOLO | 1553 | 4 | 0 | 4.33% | 4.12%–4.54% | 3,200.12 | 4.32% |
| UNKNOWN | 2866 | 0 | 0 | 7.99% | 7.71%–8.27% | 5,906.44 | 7.97% |
| HumPool+F2Pool | 20257 | 17 | 0 | 56.45% | 55.94%–56.96% | 41,833.80 | 56.43% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 2866 blocks, e.g. minerInfo `2.0.1/ZKM1bb845eb6eb804ff5ec21349ae19fe4828dad5b7e61a3fc6733c773e572a00cda`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11287** window blocks (11283 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5688; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5596; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×3
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11287
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8987
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11285 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://kate.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `9aa70df61358cdae3db73692256877d2cd2e7870eebfc5b5c0fc65c774069050`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35884}.
- Independent enumeration on second node `wss://emma.kaspa.stream/kaspa/mainnet/wrpc/json`: 48200 vs 48200 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35918 (9.977 blocks/s), first 2026-10-25T12:00:00.367Z, last 2026-10-25T12:59:59.815Z; per-minute min/max [538, 647]; 60 minutes with blocks; largest timestamp gap 1537 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 7, '[end-1s,end)': 13, '[end,end+1s)': 4}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35884, RED 34, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
