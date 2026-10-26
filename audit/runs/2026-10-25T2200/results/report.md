# Kaspa mining distribution audit: 2026-10-25T22:00:00.000Z – 2026-10-25T23:00:00.000Z

## Verdict

- HumPool + F2Pool produced **19731 of 35737 confirmed BLUE blocks = 55.21%** (Wilson 95% CI 54.70%–55.73%; minute-cluster bootstrap 95% CI 54.50%–55.86%).
- The claimed 53.9% is **outside** the 95% interval; difference +1.31 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 55.21% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11237 | 42 | 0 | 31.44% | 30.96%–31.93% | 23,286.65 | 31.42% |
| F2Pool | 8494 | 132 | 0 | 23.77% | 23.33%–24.21% | 17,560.58 | 23.69% |
| ViaBTC | 4268 | 14 | 0 | 11.94% | 11.61%–12.28% | 8,900.88 | 12.01% |
| K1Pool | 2649 | 20 | 0 | 7.41% | 7.15%–7.69% | 5,475.15 | 7.39% |
| WhalePool | 1239 | 4 | 0 | 3.47% | 3.28%–3.66% | 2,563.90 | 3.46% |
| SOLO | 1441 | 2 | 0 | 4.03% | 3.83%–4.24% | 2,973.89 | 4.01% |
| UNKNOWN | 2919 | 4 | 0 | 8.17% | 7.89%–8.46% | 6,056.57 | 8.17% |
| HumPool+F2Pool | 19731 | 174 | 0 | 55.21% | 54.70%–55.73% | 40,847.23 | 55.11% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 1527 blocks, e.g. minerInfo `2.0.1/ZKM193d20a42b4788386e37b3bb3966d9fa2c54f2a08d43029fa2d57ef292539d7b2`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 541 blocks, e.g. minerInfo `2.1.0/ZKM10d11ab555b2cad38dd7b727eb30c18f0e5e783004efbc8f161f01a6f1e79732f`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 477 blocks, e.g. minerInfo `2.1.0/ZKM1bc4a3710dad72f0d4e4be9f78df12cabfccbf0a55af7a51853b6907c27ad9b7d`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 378 blocks, e.g. minerInfo `2.0.1/ZKM1dc3d844d72ebb170512811623e9f199ef804f8924fb78ec8f748343926b72650`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11279** window blocks (11237 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5674; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5604; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11279
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8626
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11259 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://dina.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `3d7b9b2ebac0e98c70215a98af0cf0f0e032e49746e1b440d8ed36806056bad0`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 195 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35737}.
- Independent enumeration on second node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json`: 47912 vs 47912 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35958 (9.988 blocks/s), first 2026-10-25T22:00:00.169Z, last 2026-10-25T22:59:59.940Z; per-minute min/max [501, 661]; 60 minutes with blocks; largest timestamp gap 1311 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 3, '[end-1s,end)': 9, '[end,end+1s)': 6}. Blocks outside the window by timestamp but inside its DAA-score range: 2.
- Colors: BLUE 35737, RED 221, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 194 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
