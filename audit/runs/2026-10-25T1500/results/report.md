# Kaspa mining distribution audit: 2026-10-25T15:00:00.000Z – 2026-10-25T16:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20431 of 36002 confirmed BLUE blocks = 56.75%** (Wilson 95% CI 56.24%–57.26%; minute-cluster bootstrap 95% CI 56.29%–57.20%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.85 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.75% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11275 | 0 | 0 | 31.32% | 30.84%–31.80% | 23,238.38 | 31.11% |
| F2Pool | 9156 | 2 | 0 | 25.43% | 24.98%–25.88% | 18,882.47 | 25.28% |
| ViaBTC | 4064 | 2 | 0 | 11.29% | 10.97%–11.62% | 8,393.97 | 11.24% |
| K1Pool | 2603 | 0 | 0 | 7.23% | 6.97%–7.50% | 5,366.36 | 7.18% |
| WhalePool | 1151 | 0 | 0 | 3.20% | 3.02%–3.38% | 2,371.60 | 3.18% |
| SOLO | 1499 | 4 | 0 | 4.16% | 3.96%–4.37% | 3,091.96 | 4.14% |
| UNKNOWN | 2973 | 0 | 0 | 8.26% | 7.98%–8.55% | 6,134.30 | 8.21% |
| HumPool+F2Pool | 20431 | 2 | 0 | 56.75% | 56.24%–57.26% | 42,120.85 | 56.39% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 1036 blocks, e.g. minerInfo `2.1.0/ZKM17c57179f1aa38458103db4e3cf452cba5b289069acd997b2fc3df5284fa0f5fe`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 957 blocks, e.g. minerInfo `2.1.0/ZKM1d304a9ef4b138d19786f94560fffab03b691f1ea39596a2039a2748f9f5348a7`
- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 497 blocks, e.g. minerInfo `2.0.1/ZKM17d503de32fcb6fba0e2b93d4323ce796fa949f9c113308c95208a3bd42288e5d`
- kaspa:qqzffjn32q670kat0huq5j0pcvk95r8j0am62c8fyzd6yr24tefaq758ug3tw: 483 blocks, e.g. minerInfo `2.1.0/ZKM168df5810b7a036dd5a48e007af9c7bb96b3933eb74e2628c33eb2c98cf90e6fe`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11275** window blocks (11275 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5776; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5497; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×2
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11275
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9158
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11281 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `d52c0259bcf4a4fc03f9f60f5c5d8607c8eddaaf3c531b9cd74d5ef8c309055d`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36002}.
- Independent enumeration on second node `wss://luna.kaspa.blue/kaspa/mainnet/wrpc/json`: 48477 vs 48477 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36010 (10.003 blocks/s), first 2026-10-25T15:00:00.018Z, last 2026-10-25T15:59:59.874Z; per-minute min/max [542, 651]; 60 minutes with blocks; largest timestamp gap 1486 ms.
- Boundary counts: {'[start-1s,start)': 15, '[start,start+1s)': 8, '[end-1s,end)': 8, '[end,end+1s)': 12}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 36002, RED 8, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
