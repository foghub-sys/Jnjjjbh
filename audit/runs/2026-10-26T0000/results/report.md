# Kaspa mining distribution audit: 2026-10-26T00:00:00.000Z – 2026-10-26T01:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20580 of 35647 confirmed BLUE blocks = 57.73%** (Wilson 95% CI 57.22%–58.24%; minute-cluster bootstrap 95% CI 57.16%–58.31%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.83 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.73% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11451 | 3 | 0 | 32.12% | 31.64%–32.61% | 23,664.19 | 32.07% |
| F2Pool | 9129 | 18 | 0 | 25.61% | 25.16%–26.07% | 18,887.44 | 25.59% |
| ViaBTC | 3666 | 13 | 0 | 10.28% | 9.97%–10.60% | 7,626.81 | 10.33% |
| K1Pool | 2539 | 6 | 0 | 7.12% | 6.86%–7.39% | 5,246.78 | 7.11% |
| WhalePool | 1225 | 2 | 0 | 3.44% | 3.25%–3.63% | 2,531.74 | 3.43% |
| SOLO | 1691 | 9 | 0 | 4.74% | 4.53%–4.97% | 3,498.38 | 4.74% |
| UNKNOWN | 2581 | 7 | 0 | 7.24% | 6.98%–7.51% | 5,335.14 | 7.23% |
| HumPool+F2Pool | 20580 | 21 | 0 | 57.73% | 57.22%–58.24% | 42,551.63 | 57.66% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 1616 blocks, e.g. minerInfo `2.0.1/ZKM1e37513c494036c9950094a59b9ef9363ee32dba6d87f38bb366ab8623c5a3bb4`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 550 blocks, e.g. minerInfo `2.1.0/ZKM1918e5c0589b69794004b19bdab921842e8bba46f3268d7e0b294816a7b2da3da`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 422 blocks, e.g. minerInfo `2.1.0/ZKM1a55d938eb67bda0db040beff45a79b1b8fe89c523cb113e6c4586ecd3e9a83d5`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11454** window blocks (11451 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5728; `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5722; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×4
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11454
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9147
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11449 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `14027ad255e5626b9c9d1f35980a8bedb10942a806699b220fcbfbef5ac6b388`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 195 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35647}.
- Independent enumeration on second node `wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json`: 47934 vs 47934 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35706 (9.918 blocks/s), first 2026-10-26T00:00:00.158Z, last 2026-10-26T00:59:59.680Z; per-minute min/max [530, 646]; 60 minutes with blocks; largest timestamp gap 1601 ms.
- Boundary counts: {'[start-1s,start)': 11, '[start,start+1s)': 7, '[end-1s,end)': 16, '[end,end+1s)': 11}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35647, RED 59, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 194 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
