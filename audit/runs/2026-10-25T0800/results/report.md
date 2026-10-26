# Kaspa mining distribution audit: 2026-10-25T08:00:00.000Z – 2026-10-25T09:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20100 of 35883 confirmed BLUE blocks = 56.02%** (Wilson 95% CI 55.50%–56.53%; minute-cluster bootstrap 95% CI 55.52%–56.52%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.12 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.02% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 10948 | 0 | 0 | 30.51% | 30.04%–30.99% | 22,560.12 | 30.49% |
| F2Pool | 9152 | 0 | 0 | 25.51% | 25.06%–25.96% | 18,872.05 | 25.50% |
| ViaBTC | 4145 | 0 | 0 | 11.55% | 11.22%–11.89% | 8,555.80 | 11.56% |
| K1Pool | 2569 | 1 | 0 | 7.16% | 6.90%–7.43% | 5,293.66 | 7.15% |
| WhalePool | 1251 | 0 | 0 | 3.49% | 3.30%–3.68% | 2,578.36 | 3.48% |
| SOLO | 1505 | 0 | 0 | 4.19% | 3.99%–4.41% | 3,102.36 | 4.19% |
| UNKNOWN | 2848 | 1 | 0 | 7.94% | 7.66%–8.22% | 5,876.57 | 7.94% |
| HumPool+F2Pool | 20100 | 0 | 0 | 56.02% | 55.50%–56.53% | 41,432.17 | 55.99% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 953 blocks, e.g. minerInfo `2.0.1/ZKM1bec2ff3a4063dc85ba80cc081b9a8362a102e247ad29a639ab1e08e99118b9b1`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 745 blocks, e.g. minerInfo `2.1.0/ZKM1c762e7928372c2dec0b4eca268a01142dc44f12f1a3d905f90fe68421e833392`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 710 blocks, e.g. minerInfo `2.1.0/ZKM1388affd1dbf439a0b4faa16bd0d08106197098a143d70f16a582b2155012ea5f`
- kaspa:qqzffjn32q670kat0huq5j0pcvk95r8j0am62c8fyzd6yr24tefaq758ug3tw: 441 blocks, e.g. minerInfo `2.1.0/ZKM1c762e7928372c2dec0b4eca268a01142dc44f12f1a3d905f90fe68421e833392`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **10948** window blocks (10948 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5475; `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5469; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×4
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×10948
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9152
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 10949 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://luna.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `271e4b140d2fda91caeb1bf9fd7a2a3bf076a8a6df56d8ea96fd250a83c9da76`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35883}.
- Independent enumeration on second node `wss://isla.kaspa.red/kaspa/mainnet/wrpc/json`: 48227 vs 48227 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35886 (9.968 blocks/s), first 2026-10-25T08:00:00.005Z, last 2026-10-25T08:59:59.973Z; per-minute min/max [544, 650]; 60 minutes with blocks; largest timestamp gap 1265 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 15, '[end-1s,end)': 9, '[end,end+1s)': 9}. Blocks outside the window by timestamp but inside its DAA-score range: 2.
- Colors: BLUE 35883, RED 3, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
