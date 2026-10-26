# Kaspa mining distribution audit: 2026-10-26T06:00:00.000Z – 2026-10-26T07:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20727 of 36288 confirmed BLUE blocks = 57.12%** (Wilson 95% CI 56.61%–57.63%; minute-cluster bootstrap 95% CI 56.55%–57.70%).
- The claimed 53.9% is **outside** the 95% interval; difference +3.22 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 57.12% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11488 | 3 | 0 | 31.66% | 31.18%–32.14% | 23,674.19 | 31.64% |
| F2Pool | 9239 | 2 | 0 | 25.46% | 25.01%–25.91% | 19,046.18 | 25.46% |
| ViaBTC | 3952 | 0 | 0 | 10.89% | 10.57%–11.22% | 8,161.91 | 10.91% |
| K1Pool | 2663 | 2 | 0 | 7.34% | 7.07%–7.61% | 5,487.51 | 7.33% |
| WhalePool | 1244 | 2 | 0 | 3.43% | 3.25%–3.62% | 2,563.22 | 3.43% |
| SOLO | 1062 | 0 | 0 | 2.93% | 2.76%–3.11% | 2,191.79 | 2.93% |
| UNKNOWN | 3347 | 0 | 0 | 9.22% | 8.93%–9.53% | 6,898.28 | 9.22% |
| HumPool+F2Pool | 20727 | 5 | 0 | 57.12% | 56.61%–57.63% | 42,720.37 | 57.10% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qpwz9sgjzkjnslmy7asm4eadwvtfqtv2ae8yr8xav6vc0he5my4jzvx7hsxnr: 2481 blocks, e.g. minerInfo `2.0.1/ZKM129681ef1d3889dd3b9bf4def32cfe8cdeeab559f9ea3e633dc7c0b97139fbd3f`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 460 blocks, e.g. minerInfo `2.1.0/ZKM195398b8ad2bf368cacf4201e65247f1e1b357d93c6064d80465b8ec1b09b2c80`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 406 blocks, e.g. minerInfo `2.0.1/ZKM1ae4659dfc8e235cfe439056e67d276d944568d073d0434c4cfcdd6e590790fa4`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11491** window blocks (11488 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5775; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5715; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11491
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9241
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11489 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `08fc42921a6d93f08cc17b962f0e89139c3dc0c74523e9344db322522d9e24d6`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 36288}.
- Independent enumeration on second node `wss://luna.kaspa.blue/kaspa/mainnet/wrpc/json`: 48507 vs 48507 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36298 (10.083 blocks/s), first 2026-10-26T06:00:00.022Z, last 2026-10-26T06:59:59.966Z; per-minute min/max [549, 645]; 60 minutes with blocks; largest timestamp gap 1729 ms.
- Boundary counts: {'[start-1s,start)': 14, '[start,start+1s)': 8, '[end-1s,end)': 8, '[end,end+1s)': 12}. Blocks outside the window by timestamp but inside its DAA-score range: 4.
- Colors: BLUE 36288, RED 10, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
