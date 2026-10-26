# Kaspa mining distribution audit: 2026-10-25T19:00:00.000Z – 2026-10-25T20:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20165 of 35886 confirmed BLUE blocks = 56.19%** (Wilson 95% CI 55.68%–56.70%; minute-cluster bootstrap 95% CI 55.55%–56.81%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.29 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.19% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11310 | 25 | 0 | 31.52% | 31.04%–32.00% | 23,331.36 | 31.44% |
| F2Pool | 8855 | 62 | 0 | 24.68% | 24.23%–25.12% | 18,282.63 | 24.64% |
| ViaBTC | 4242 | 6 | 0 | 11.82% | 11.49%–12.16% | 8,809.42 | 11.87% |
| K1Pool | 2566 | 8 | 0 | 7.15% | 6.89%–7.42% | 5,328.22 | 7.18% |
| WhalePool | 1220 | 4 | 0 | 3.40% | 3.22%–3.59% | 2,528.54 | 3.41% |
| SOLO | 1037 | 4 | 0 | 2.89% | 2.72%–3.07% | 2,139.46 | 2.88% |
| UNKNOWN | 3405 | 8 | 0 | 9.49% | 9.19%–9.80% | 7,019.94 | 9.46% |
| HumPool+F2Pool | 20165 | 87 | 0 | 56.19% | 55.68%–56.70% | 41,614.00 | 56.08% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3021 blocks, e.g. minerInfo `2.0.1/ZKM166cf7ddfa8e61ff4cb001fe2f76f9abeaa387e06233089d51108f81551bd7540`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 392 blocks, e.g. minerInfo `2.0.1/ZKM1932c8a717988e6e321e6ac28d24c2cd99afdebd5ba60686fb6675260747d186d`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11335** window blocks (11310 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5709; `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5625; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11335
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8917
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11313 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `3567dac41dce0b8f238e7b3970394f6a3cce1af3837101b39058218c1b4103bd`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35886}.
- Independent enumeration on second node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json`: 48180 vs 48180 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36005 (10.001 blocks/s), first 2026-10-25T19:00:00.077Z, last 2026-10-25T19:59:59.636Z; per-minute min/max [490, 667]; 60 minutes with blocks; largest timestamp gap 1242 ms.
- Boundary counts: {'[start-1s,start)': 4, '[start,start+1s)': 15, '[end-1s,end)': 9, '[end,end+1s)': 8}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35886, RED 119, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
