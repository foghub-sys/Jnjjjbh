# Kaspa mining distribution audit: 2026-10-26T04:00:00.000Z – 2026-10-26T05:00:00.000Z

## Verdict

- HumPool + F2Pool produced **21503 of 36016 confirmed BLUE blocks = 59.70%** (Wilson 95% CI 59.20%–60.21%; minute-cluster bootstrap 95% CI 59.22%–60.20%).
- The claimed 53.9% is **outside** the 95% interval; difference +5.80 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 59.70% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11859 | 2 | 0 | 32.93% | 32.44%–33.41% | 24,446.93 | 32.91% |
| F2Pool | 9644 | 2 | 0 | 26.78% | 26.32%–27.24% | 19,888.88 | 26.78% |
| ViaBTC | 2626 | 2 | 0 | 7.29% | 7.03%–7.56% | 5,422.17 | 7.30% |
| K1Pool | 2575 | 2 | 0 | 7.15% | 6.89%–7.42% | 5,306.54 | 7.14% |
| WhalePool | 1332 | 0 | 0 | 3.70% | 3.51%–3.90% | 2,745.21 | 3.70% |
| SOLO | 905 | 2 | 0 | 2.51% | 2.36%–2.68% | 1,865.44 | 2.51% |
| UNKNOWN | 3722 | 0 | 0 | 10.33% | 10.02%–10.65% | 7,670.92 | 10.33% |
| HumPool+F2Pool | 21503 | 4 | 0 | 59.70% | 59.20%–60.21% | 44,335.82 | 59.69% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 3322 blocks, e.g. minerInfo `2.0.1/ZKM16bad40694f8d74ed1359374a43823371a973f3b26f4a8eb3a6e7f998c48eede3`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 400 blocks, e.g. minerInfo `2.0.1/ZKM10f42c3df2ec27e63192ebb79916ab17dab773412e2f4054fa016a19f57902b2a`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11861** window blocks (11859 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5951; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5905; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11861
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9646
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11866 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://eva.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `cfde7b90d7ce709f26d6165977dc59efb31a5b0b41b104d9f15252f294cd3662`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36016}.
- Independent enumeration on second node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json`: 48428 vs 48428 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36027 (10.008 blocks/s), first 2026-10-26T04:00:00.019Z, last 2026-10-26T04:59:59.689Z; per-minute min/max [535, 653]; 60 minutes with blocks; largest timestamp gap 1366 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 15, '[end-1s,end)': 7, '[end,end+1s)': 8}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 36016, RED 11, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 3.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
