# Kaspa mining distribution audit: 2026-10-26T01:00:00.000Z – 2026-10-26T02:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20269 of 35390 confirmed BLUE blocks = 57.27%** (Wilson 95% CI 56.76%–57.79%; minute-cluster bootstrap 95% CI 56.60%–57.92%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.37 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.27% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11600 | 70 | 0 | 32.78% | 32.29%–33.27% | 23,999.72 | 32.64% |
| F2Pool | 8669 | 147 | 0 | 24.50% | 24.05%–24.95% | 17,932.32 | 24.39% |
| ViaBTC | 2887 | 8 | 0 | 8.16% | 7.88%–8.45% | 6,092.60 | 8.29% |
| K1Pool | 2761 | 18 | 0 | 7.80% | 7.53%–8.09% | 5,720.08 | 7.78% |
| WhalePool | 1305 | 5 | 0 | 3.69% | 3.50%–3.89% | 2,697.40 | 3.67% |
| SOLO | 1325 | 9 | 0 | 3.74% | 3.55%–3.95% | 2,806.56 | 3.82% |
| UNKNOWN | 3418 | 9 | 0 | 9.66% | 9.35%–9.97% | 7,062.62 | 9.61% |
| HumPool+F2Pool | 20269 | 217 | 0 | 57.27% | 56.76%–57.79% | 41,932.04 | 57.03% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 1473 blocks, e.g. minerInfo `2.0.1/ZKM17d16bce80f2fb736c49565a857389c428b40323a1a5c09a36244a17e4bcf3256`
- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 557 blocks, e.g. minerInfo `2.0.1/ZKM13c3eee95847c4c2aae74de4f15bbeb53c4380b2c400b6c9e0668b45375ac7301`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 512 blocks, e.g. minerInfo `2.1.0/ZKM1c9aafccea2f3d731878e49930cf237a682028a28a0c129314c5c51a88997731e`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 486 blocks, e.g. minerInfo `2.1.0/ZKM13de43f090f075def96828fab0cdab7ae8a5135da21dd9d63ff8f881fc83943eb`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 399 blocks, e.g. minerInfo `2.0.1/ZKM1709e19e1048b37a1a56f62c2d002ab665fcfa576e6d166f9395915721e1716ce`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11670** window blocks (11600 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5916; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5751; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×3
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11670
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8816
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11622 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `682d656d0b2ea52cfa8565bb9bce2c44153577496691a60b20cb1083ae395980`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 195 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35390}.
- Independent enumeration on second node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json`: 47905 vs 47905 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 125, 'merging_chain_hash_recomputed_ok=True': 125, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35659 (9.905 blocks/s), first 2026-10-26T01:00:00.086Z, last 2026-10-26T01:59:59.965Z; per-minute min/max [511, 665]; 60 minutes with blocks; largest timestamp gap 1405 ms.
- Boundary counts: {'[start-1s,start)': 16, '[start,start+1s)': 11, '[end-1s,end)': 6, '[end,end+1s)': 11}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 35390, RED 269, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 194 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
