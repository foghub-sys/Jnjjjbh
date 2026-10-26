# Kaspa mining distribution audit: 2026-10-25T00:00:00.000Z – 2026-10-25T01:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20105 of 35793 confirmed BLUE blocks = 56.17%** (Wilson 95% CI 55.66%–56.68%; minute-cluster bootstrap 95% CI 55.55%–56.79%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.27 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.17% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11091 | 8 | 0 | 30.99% | 30.51%–31.47% | 22,903.27 | 30.91% |
| F2Pool | 9014 | 22 | 0 | 25.18% | 24.74%–25.64% | 18,679.22 | 25.21% |
| ViaBTC | 4168 | 7 | 0 | 11.64% | 11.32%–11.98% | 8,652.91 | 11.68% |
| K1Pool | 2364 | 2 | 0 | 6.60% | 6.35%–6.87% | 4,886.04 | 6.59% |
| WhalePool | 1240 | 2 | 0 | 3.46% | 3.28%–3.66% | 2,560.78 | 3.46% |
| SOLO | 1290 | 12 | 0 | 3.60% | 3.42%–3.80% | 2,668.94 | 3.60% |
| UNKNOWN | 3144 | 3 | 0 | 8.78% | 8.49%–9.08% | 6,512.94 | 8.79% |
| HumPool+F2Pool | 20105 | 30 | 0 | 56.17% | 55.66%–56.68% | 41,582.49 | 56.12% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 1209 blocks, e.g. minerInfo `2.1.0/ZKM13bc30903390f9b5679226da7dc4be14fbdb72e0f8adc9b56b6a3af1ba61d0e14`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 894 blocks, e.g. minerInfo `2.1.0/ZKM1e229c4141300b7f156c676000781449199e4f0ad5a936f691aad46bc21e79da1`
- kaspa:qqzffjn32q670kat0huq5j0pcvk95r8j0am62c8fyzd6yr24tefaq758ug3tw: 658 blocks, e.g. minerInfo `2.1.0/ZKM1e58fa81984832e5d2eebb1d0c51f61aa20b039ca9bdd7cf6aff9ec9bc0826c5d`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 386 blocks, e.g. minerInfo `2.0.1/ZKM1335dfbe47b8710621e866756a54c57363b9219cb13afa9ea0e610b4f3998b616`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11099** window blocks (11091 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5553; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5541; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11099
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9036
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11092 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `8e4e9478a29e48680c7644d30c1423061793882ce15c17103ea9ab91f8e9da07`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35793}.
- Independent enumeration on second node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json`: 48198 vs 48198 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35850 (9.958 blocks/s), first 2026-10-25T00:00:00.317Z, last 2026-10-25T00:59:59.960Z; per-minute min/max [546, 648]; 60 minutes with blocks; largest timestamp gap 1305 ms.
- Boundary counts: {'[start-1s,start)': 5, '[start,start+1s)': 16, '[end-1s,end)': 20, '[end,end+1s)': 15}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 35793, RED 57, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
