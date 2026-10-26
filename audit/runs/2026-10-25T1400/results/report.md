# Kaspa mining distribution audit: 2026-10-25T14:00:00.000Z – 2026-10-25T15:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20130 of 35893 confirmed BLUE blocks = 56.08%** (Wilson 95% CI 55.57%–56.60%; minute-cluster bootstrap 95% CI 55.53%–56.62%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.18 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.08% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11149 | 5 | 0 | 31.06% | 30.59%–31.54% | 22,979.44 | 31.03% |
| F2Pool | 8981 | 11 | 0 | 25.02% | 24.58%–25.47% | 18,527.43 | 25.02% |
| ViaBTC | 4221 | 2 | 0 | 11.76% | 11.43%–12.10% | 8,709.68 | 11.76% |
| K1Pool | 2583 | 6 | 0 | 7.20% | 6.93%–7.47% | 5,322.85 | 7.19% |
| WhalePool | 1152 | 2 | 0 | 3.21% | 3.03%–3.40% | 2,373.82 | 3.21% |
| SOLO | 1490 | 3 | 0 | 4.15% | 3.95%–4.36% | 3,070.57 | 4.15% |
| UNKNOWN | 3047 | 0 | 0 | 8.49% | 8.21%–8.78% | 6,309.42 | 8.52% |
| HumPool+F2Pool | 20130 | 16 | 0 | 56.08% | 55.57%–56.60% | 41,506.86 | 56.05% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 1301 blocks, e.g. minerInfo `2.1.0/ZKM1e2caf7270a44c0e8463c08c212da935332e734e53c7d6267941a263eab282674`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 1125 blocks, e.g. minerInfo `2.1.0/ZKM1d29878fce2f84a70804e237ce854b6a189dab7c618d78d471875041cfd283120`
- kaspa:qqzffjn32q670kat0huq5j0pcvk95r8j0am62c8fyzd6yr24tefaq758ug3tw: 621 blocks, e.g. minerInfo `2.1.0/ZKM10c816883d7710223630cede697349c04ddeeab42dee227ebbbd8e483a0755170`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11154** window blocks (11149 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5620; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5533; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11154
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×8992
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11151 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://dina.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `597d37daf7f51cd2ca14315ce494ca892079dd85c48125801426608435221f26`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35893}.
- Independent enumeration on second node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json`: 48250 vs 48250 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 127, 'merging_chain_hash_recomputed_ok=True': 127, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35923 (9.979 blocks/s), first 2026-10-25T14:00:00.040Z, last 2026-10-25T14:59:59.974Z; per-minute min/max [543, 660]; 60 minutes with blocks; largest timestamp gap 1500 ms.
- Boundary counts: {'[start-1s,start)': 22, '[start,start+1s)': 2, '[end-1s,end)': 15, '[end,end+1s)': 8}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35893, RED 30, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
