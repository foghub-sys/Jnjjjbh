# Kaspa mining distribution audit: 2026-10-26T05:00:00.000Z – 2026-10-26T06:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20977 of 36241 confirmed BLUE blocks = 57.88%** (Wilson 95% CI 57.37%–58.39%; minute-cluster bootstrap 95% CI 57.27%–58.48%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.98 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.88% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11548 | 0 | 0 | 31.86% | 31.39%–32.35% | 23,795.51 | 31.86% |
| F2Pool | 9429 | 0 | 0 | 26.02% | 25.57%–26.47% | 19,433.28 | 26.02% |
| ViaBTC | 3458 | 0 | 0 | 9.54% | 9.24%–9.85% | 7,129.38 | 9.54% |
| K1Pool | 2657 | 2 | 0 | 7.33% | 7.07%–7.60% | 5,476.72 | 7.33% |
| WhalePool | 1321 | 0 | 0 | 3.65% | 3.46%–3.84% | 2,722.08 | 3.64% |
| SOLO | 782 | 0 | 0 | 2.16% | 2.01%–2.31% | 1,612.23 | 2.16% |
| UNKNOWN | 3685 | 0 | 0 | 10.17% | 9.86%–10.48% | 7,594.78 | 10.17% |
| HumPool+F2Pool | 20977 | 0 | 0 | 57.88% | 57.37%–58.39% | 43,228.79 | 57.87% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 3284 blocks, e.g. minerInfo `2.0.1/ZKM1e77423f5949baecea5d8522947314468fbf5ea3175d06ba2876c23bcb6ce6761`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 401 blocks, e.g. minerInfo `2.0.1/ZKM1b3ca8a947da77af338d79a0a82cab3cc71b54235af997e577289922e8b35b787`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11548** window blocks (11548 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5799; `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5745; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×4
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11548
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9429
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11540 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://dina.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `2c8c2c9f7f766e7c0897dc8187353caca6530b872196e1943a9657fe93579f7a`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 198 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36241}.
- Independent enumeration on second node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json`: 48658 vs 48658 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36244 (10.068 blocks/s), first 2026-10-26T05:00:00.365Z, last 2026-10-26T05:59:59.837Z; per-minute min/max [547, 653]; 60 minutes with blocks; largest timestamp gap 1153 ms.
- Boundary counts: {'[start-1s,start)': 7, '[start,start+1s)': 8, '[end-1s,end)': 14, '[end,end+1s)': 8}. Blocks outside the window by timestamp but inside its DAA-score range: 2.
- Colors: BLUE 36241, RED 3, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 197 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
