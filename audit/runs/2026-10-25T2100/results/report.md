# Kaspa mining distribution audit: 2026-10-25T21:00:00.000Z – 2026-10-25T22:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20153 of 36053 confirmed BLUE blocks = 55.90%** (Wilson 95% CI 55.39%–56.41%; minute-cluster bootstrap 95% CI 55.40%–56.38%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.00 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 55.90% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11152 | 0 | 0 | 30.93% | 30.46%–31.41% | 22,979.38 | 30.92% |
| F2Pool | 9001 | 1 | 0 | 24.97% | 24.52%–25.42% | 18,550.64 | 24.96% |
| ViaBTC | 4251 | 1 | 0 | 11.79% | 11.46%–12.13% | 8,769.25 | 11.80% |
| K1Pool | 2599 | 0 | 0 | 7.21% | 6.95%–7.48% | 5,354.71 | 7.21% |
| WhalePool | 1253 | 0 | 0 | 3.48% | 3.29%–3.67% | 2,582.02 | 3.47% |
| SOLO | 1065 | 1 | 0 | 2.95% | 2.78%–3.13% | 2,194.97 | 2.95% |
| UNKNOWN | 3473 | 0 | 0 | 9.63% | 9.33%–9.94% | 7,156.79 | 9.63% |
| HumPool+F2Pool | 20153 | 1 | 0 | 55.90% | 55.39%–56.41% | 41,530.02 | 55.88% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3110 blocks, e.g. minerInfo `2.0.1/ZKM1e1e092aa3299e9887db8d50d98a8e3c15b2708976da866a15f6123a0e304afe0`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 363 blocks, e.g. minerInfo `2.0.1/ZKM1fc2ab840386348558f204a9a2d69002ba90c0d8b6d66dc462363779b63240c53`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11152** window blocks (11152 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5597; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5554; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11152
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9002
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11151 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://eva.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `eda776f90a8431705b9e42fa4f4f855f6b7c20bf47c5375c68411ae64e807a7e`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36053}.
- Independent enumeration on second node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json`: 48540 vs 48540 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36056 (10.016 blocks/s), first 2026-10-25T21:00:00.078Z, last 2026-10-25T21:59:59.968Z; per-minute min/max [543, 669]; 60 minutes with blocks; largest timestamp gap 1264 ms.
- Boundary counts: {'[start-1s,start)': 13, '[start,start+1s)': 9, '[end-1s,end)': 8, '[end,end+1s)': 3}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 36053, RED 3, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
