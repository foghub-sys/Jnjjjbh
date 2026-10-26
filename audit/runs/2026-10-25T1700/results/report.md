# Kaspa mining distribution audit: 2026-10-25T17:00:00.000Z – 2026-10-25T18:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20397 of 36282 confirmed BLUE blocks = 56.22%** (Wilson 95% CI 55.71%–56.73%; minute-cluster bootstrap 95% CI 55.72%–56.72%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.32 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.22% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11177 | 0 | 0 | 30.81% | 30.33%–31.28% | 23,030.74 | 30.80% |
| F2Pool | 9220 | 0 | 0 | 25.41% | 24.97%–25.86% | 19,004.79 | 25.41% |
| ViaBTC | 4281 | 2 | 0 | 11.80% | 11.47%–12.14% | 8,829.96 | 11.81% |
| K1Pool | 2587 | 1 | 0 | 7.13% | 6.87%–7.40% | 5,330.32 | 7.13% |
| WhalePool | 1195 | 0 | 0 | 3.29% | 3.11%–3.48% | 2,462.67 | 3.29% |
| SOLO | 1081 | 0 | 0 | 2.98% | 2.81%–3.16% | 2,227.47 | 2.98% |
| UNKNOWN | 3486 | 1 | 0 | 9.61% | 9.31%–9.92% | 7,182.60 | 9.60% |
| HumPool+F2Pool | 20397 | 0 | 0 | 56.22% | 55.71%–56.73% | 42,035.52 | 56.21% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3094 blocks, e.g. minerInfo `2.0.1/ZKM1f8b9d4e3b04b79ff3d1f45e08194d4e651e33b435e6408b8725c5ab8d94523aa`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 393 blocks, e.g. minerInfo `2.0.1/ZKM157dc2f747120874b48a82d0800b81e468644c6a0d35c9a57c0531ec063ddb2ce`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11177** window blocks (11177 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5649; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5526; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×2
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11177
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9220
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11177 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `90e80b93964742805a00eef27e3488f317753d7a3fa62cab8a702d5967cef249`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36282}.
- Independent enumeration on second node `wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json`: 48471 vs 48471 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36286 (10.079 blocks/s), first 2026-10-25T17:00:00.077Z, last 2026-10-25T17:59:59.956Z; per-minute min/max [562, 660]; 60 minutes with blocks; largest timestamp gap 1215 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 22, '[end-1s,end)': 13, '[end,end+1s)': 15}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 36282, RED 4, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
