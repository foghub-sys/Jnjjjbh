# Kaspa mining distribution audit: 2026-10-26T03:00:00.000Z – 2026-10-26T04:00:00.000Z

## Verdict

- HumPool + F2Pool produced **21300 of 36109 confirmed BLUE blocks = 58.99%** (Wilson 95% CI 58.48%–59.49%; minute-cluster bootstrap 95% CI 58.42%–59.54%).
- The claimed 53.9% is **outside** the 95% interval; difference +5.09 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 58.99% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11909 | 8 | 0 | 32.98% | 32.50%–33.47% | 24,552.96 | 32.92% |
| F2Pool | 9391 | 24 | 0 | 26.01% | 25.56%–26.46% | 19,385.80 | 25.99% |
| ViaBTC | 2779 | 2 | 0 | 7.70% | 7.43%–7.98% | 5,770.89 | 7.74% |
| K1Pool | 2569 | 5 | 0 | 7.11% | 6.85%–7.38% | 5,313.43 | 7.12% |
| WhalePool | 1285 | 1 | 0 | 3.56% | 3.37%–3.75% | 2,651.52 | 3.56% |
| SOLO | 1145 | 0 | 0 | 3.17% | 3.00%–3.36% | 2,362.66 | 3.17% |
| UNKNOWN | 3609 | 3 | 0 | 9.99% | 9.69%–10.31% | 7,441.68 | 9.98% |
| HumPool+F2Pool | 21300 | 32 | 0 | 58.99% | 58.48%–59.49% | 43,938.76 | 58.92% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 3237 blocks, e.g. minerInfo `2.0.1/ZKM1356ada09347e3173f3fe0771a7b7b65487e62c81713ed99f815448031cde9957`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 375 blocks, e.g. minerInfo `2.0.1/ZKM17ec63e6b36ab56ec7e639a694e2e1bf9b29b83cd738c6021978f2b1bd6200f1f`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11917** window blocks (11909 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×6004; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5911; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×2
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11917
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9415
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11909 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://kate.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `0156eedf7a588d65a0f79c47d0b2dd3f441fda921d2c53b87bfcc87ad9ee9a28`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36109}.
- Independent enumeration on second node `wss://emma.kaspa.stream/kaspa/mainnet/wrpc/json`: 48385 vs 48385 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36153 (10.043 blocks/s), first 2026-10-26T03:00:00.103Z, last 2026-10-26T03:59:59.966Z; per-minute min/max [528, 656]; 60 minutes with blocks; largest timestamp gap 1411 ms.
- Boundary counts: {'[start-1s,start)': 14, '[start,start+1s)': 14, '[end-1s,end)': 8, '[end,end+1s)': 15}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 36109, RED 44, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
