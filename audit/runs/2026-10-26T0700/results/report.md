# Kaspa mining distribution audit: 2026-10-26T07:00:00.000Z – 2026-10-26T08:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20508 of 35623 confirmed BLUE blocks = 57.57%** (Wilson 95% CI 57.06%–58.08%; minute-cluster bootstrap 95% CI 57.01%–58.11%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.67 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.57% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11273 | 0 | 0 | 31.65% | 31.16%–32.13% | 23,233.57 | 31.62% |
| F2Pool | 9235 | 0 | 0 | 25.92% | 25.47%–26.38% | 19,045.58 | 25.92% |
| ViaBTC | 3480 | 0 | 0 | 9.77% | 9.46%–10.08% | 7,186.98 | 9.78% |
| K1Pool | 2702 | 0 | 0 | 7.58% | 7.31%–7.86% | 5,569.63 | 7.58% |
| WhalePool | 1285 | 0 | 0 | 3.61% | 3.42%–3.81% | 2,647.70 | 3.60% |
| SOLO | 760 | 0 | 0 | 2.13% | 1.99%–2.29% | 1,566.87 | 2.13% |
| UNKNOWN | 3584 | 1 | 0 | 10.06% | 9.75%–10.38% | 7,386.33 | 10.05% |
| HumPool+F2Pool | 20508 | 0 | 0 | 57.57% | 57.06%–58.08% | 42,279.15 | 57.55% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 3173 blocks, e.g. minerInfo `2.0.1/ZKM1218f50cf9a1afe6c3a51a6caf4badd4eb84535457afefbec1cb12a999f2b95ad`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 412 blocks, e.g. minerInfo `2.0.1/ZKM1a36ae0b322e9cdee61ca9500abfee05517f00365a3aeae1166d03504b6b7bd26`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11273** window blocks (11273 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5688; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5583; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×2
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11273
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9235
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11272 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `ef59b3f0dc01a4e2badb070ef4aa7b4b02126765b46e6ad48c6f51fa777d9f1f`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 194 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35623}.
- Independent enumeration on second node `wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json`: 47726 vs 47726 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35624 (9.896 blocks/s), first 2026-10-26T07:00:00.135Z, last 2026-10-26T07:59:59.902Z; per-minute min/max [551, 671]; 60 minutes with blocks; largest timestamp gap 1413 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 12, '[end-1s,end)': 5, '[end,end+1s)': 10}. Blocks outside the window by timestamp but inside its DAA-score range: 1.
- Colors: BLUE 35623, RED 1, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 193 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
