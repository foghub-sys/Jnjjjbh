# Kaspa mining distribution audit: 2026-10-26T02:00:00.000Z – 2026-10-26T03:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20697 of 35915 confirmed BLUE blocks = 57.63%** (Wilson 95% CI 57.12%–58.14%; minute-cluster bootstrap 95% CI 56.91%–58.31%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.73 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.63% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11787 | 32 | 0 | 32.82% | 32.34%–33.31% | 24,392.10 | 32.79% |
| F2Pool | 8910 | 99 | 0 | 24.81% | 24.36%–25.26% | 18,411.49 | 24.75% |
| ViaBTC | 2873 | 3 | 0 | 8.00% | 7.72%–8.28% | 5,992.00 | 8.06% |
| K1Pool | 2746 | 11 | 0 | 7.65% | 7.38%–7.93% | 5,658.41 | 7.61% |
| WhalePool | 1306 | 5 | 0 | 3.64% | 3.45%–3.84% | 2,697.64 | 3.63% |
| SOLO | 1424 | 7 | 0 | 3.96% | 3.77%–4.17% | 2,946.86 | 3.96% |
| UNKNOWN | 3416 | 11 | 0 | 9.51% | 9.21%–9.82% | 7,045.88 | 9.47% |
| HumPool+F2Pool | 20697 | 131 | 0 | 57.63% | 57.12%–58.14% | 42,803.59 | 57.55% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 1946 blocks, e.g. minerInfo `2.0.1/ZKM1acfc47ee7ae497109fd94e845a517b8c2b02000f13d12a34adfc7de74045a1bd`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 565 blocks, e.g. minerInfo `2.1.0/ZKM10a7f248a08bead69ba84330926a400765c1d5ff96aa4d31e2ac47982637dc0cd`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 481 blocks, e.g. minerInfo `2.1.0/ZKM15b93be161b4db42a10c3e8c0724bb771ae46c200f5250982c4c1ac2024d51576`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 435 blocks, e.g. minerInfo `2.0.1/ZKM1a49b8ff7e71f5f2f8612c2a4cc98a680b1f5bd9507e0c6d7a887f5b12e4ff9b5`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11819** window blocks (11787 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5989; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5827; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×3
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11819
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9009
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11805 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://luna.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `7fbf1d39eb851059dccdc6d1d3cfd8bfc6aacccb7d816f5a01796e06fc033640`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 199 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35915}.
- Independent enumeration on second node `wss://isla.kaspa.red/kaspa/mainnet/wrpc/json`: 48903 vs 48903 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36084 (10.023 blocks/s), first 2026-10-26T02:00:00.006Z, last 2026-10-26T02:59:59.995Z; per-minute min/max [492, 685]; 60 minutes with blocks; largest timestamp gap 1367 ms.
- Boundary counts: {'[start-1s,start)': 6, '[start,start+1s)': 11, '[end-1s,end)': 14, '[end,end+1s)': 14}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 35915, RED 169, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 198 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
