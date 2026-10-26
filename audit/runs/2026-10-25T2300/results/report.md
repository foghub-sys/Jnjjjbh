# Kaspa mining distribution audit: 2026-10-25T23:00:00.000Z – 2026-10-26T00:00:00.000Z

## Verdict

- HumPool + F2Pool produced **19978 of 35586 confirmed BLUE blocks = 56.14%** (Wilson 95% CI 55.62%–56.65%; minute-cluster bootstrap 95% CI 55.48%–56.78%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.24 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.14% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11339 | 9 | 0 | 31.86% | 31.38%–32.35% | 23,401.76 | 31.82% |
| F2Pool | 8639 | 53 | 0 | 24.28% | 23.83%–24.72% | 17,832.82 | 24.25% |
| ViaBTC | 4181 | 2 | 0 | 11.75% | 11.42%–12.09% | 8,667.65 | 11.78% |
| K1Pool | 2525 | 4 | 0 | 7.10% | 6.83%–7.37% | 5,208.78 | 7.08% |
| WhalePool | 1240 | 0 | 0 | 3.48% | 3.30%–3.68% | 2,565.61 | 3.49% |
| SOLO | 1231 | 1 | 0 | 3.46% | 3.27%–3.65% | 2,542.33 | 3.46% |
| UNKNOWN | 2848 | 4 | 0 | 8.00% | 7.73%–8.29% | 5,890.80 | 8.01% |
| HumPool+F2Pool | 19978 | 62 | 0 | 56.14% | 55.62%–56.65% | 41,234.59 | 56.06% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 1018 blocks, e.g. minerInfo `2.1.0/ZKM16960801db59da639d570638d2188c77c834c0a61c5f60c1da6bb153af67389bd`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 933 blocks, e.g. minerInfo `2.1.0/ZKM1d325aace475f5cabbf1a8e7c77df9256a797e399b37800e0be2243e0657004ef`
- kaspa:qqzffjn32q670kat0huq5j0pcvk95r8j0am62c8fyzd6yr24tefaq758ug3tw: 493 blocks, e.g. minerInfo `2.1.0/ZKM1caba09cacdd80984c0e182912cf7d614418f2c6d638054f77537a7a122a52349`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 408 blocks, e.g. minerInfo `2.0.1/ZKM12c2298e025a41dff2208e145366094d88ac35084bf3543de9a8c2d587f1e49de`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11348** window blocks (11339 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5745; `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5600; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×3
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11348
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8692
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11347 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `fcf5b9634ce176f03d1c093404b05250e23aa9823efb154bf32dd2257328c7b6`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35586}.
- Independent enumeration on second node `wss://luna.kaspa.blue/kaspa/mainnet/wrpc/json`: 48276 vs 48276 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35661 (9.906 blocks/s), first 2026-10-25T23:00:00.186Z, last 2026-10-25T23:59:59.713Z; per-minute min/max [517, 646]; 60 minutes with blocks; largest timestamp gap 1452 ms.
- Boundary counts: {'[start-1s,start)': 9, '[start,start+1s)': 6, '[end-1s,end)': 11, '[end,end+1s)': 7}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 35586, RED 75, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
