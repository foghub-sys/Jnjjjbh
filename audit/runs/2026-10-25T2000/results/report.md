# Kaspa mining distribution audit: 2026-10-25T20:00:00.000Z – 2026-10-25T21:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20155 of 36124 confirmed BLUE blocks = 55.79%** (Wilson 95% CI 55.28%–56.31%; minute-cluster bootstrap 95% CI 55.13%–56.48%).
- The claimed 53.9% is **outside** the 95% interval; difference +1.89 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 55.79% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 10991 | 7 | 0 | 30.43% | 29.95%–30.90% | 22,650.05 | 30.40% |
| F2Pool | 9164 | 5 | 0 | 25.37% | 24.92%–25.82% | 18,893.12 | 25.36% |
| ViaBTC | 4260 | 2 | 0 | 11.79% | 11.46%–12.13% | 8,808.50 | 11.82% |
| K1Pool | 2569 | 1 | 0 | 7.11% | 6.85%–7.38% | 5,293.57 | 7.11% |
| WhalePool | 1261 | 0 | 0 | 3.49% | 3.31%–3.69% | 2,599.89 | 3.49% |
| SOLO | 1051 | 2 | 0 | 2.91% | 2.74%–3.09% | 2,166.36 | 2.91% |
| UNKNOWN | 3524 | 0 | 0 | 9.76% | 9.45%–10.07% | 7,261.50 | 9.75% |
| HumPool+F2Pool | 20155 | 12 | 0 | 55.79% | 55.28%–56.31% | 41,543.16 | 55.76% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3109 blocks, e.g. minerInfo `2.0.1/ZKM1778c703ed02e81dc345534717f922eb50732aaf2c7654a168b16960182fb60f5`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 415 blocks, e.g. minerInfo `2.0.1/ZKM19a9dcb0a929917e0011cecab27eaeb3b8dbbde2c163c145579aa3e64e5fcfb72`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **10998** window blocks (10991 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5580; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5413; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×10998
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9169
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 10995 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://kate.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `eb8c471580446f8bc8d0967f664603469e6ac633bc332f4125a8b57f54025669`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36124}.
- Independent enumeration on second node `wss://emma.kaspa.stream/kaspa/mainnet/wrpc/json`: 48461 vs 48461 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36142 (10.039 blocks/s), first 2026-10-25T20:00:00.022Z, last 2026-10-25T20:59:59.972Z; per-minute min/max [551, 659]; 60 minutes with blocks; largest timestamp gap 1522 ms.
- Boundary counts: {'[start-1s,start)': 9, '[start,start+1s)': 8, '[end-1s,end)': 13, '[end,end+1s)': 9}. Blocks outside the window by timestamp but inside its DAA-score range: 2.
- Colors: BLUE 36124, RED 18, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
