# Kaspa mining distribution audit: 2026-10-25T10:00:00.000Z – 2026-10-25T11:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20056 of 35913 confirmed BLUE blocks = 55.85%** (Wilson 95% CI 55.33%–56.36%; minute-cluster bootstrap 95% CI 55.37%–56.31%).
- The claimed 53.9% is **outside** the 95% interval; difference +1.95 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 55.85% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11037 | 0 | 0 | 30.73% | 30.26%–31.21% | 22,742.37 | 30.72% |
| F2Pool | 9019 | 1 | 0 | 25.11% | 24.67%–25.56% | 18,591.64 | 25.11% |
| ViaBTC | 4254 | 0 | 0 | 11.85% | 11.52%–12.18% | 8,771.34 | 11.85% |
| K1Pool | 2595 | 0 | 0 | 7.23% | 6.96%–7.50% | 5,347.47 | 7.22% |
| WhalePool | 1256 | 0 | 0 | 3.50% | 3.31%–3.69% | 2,588.85 | 3.50% |
| SOLO | 1029 | 0 | 0 | 2.87% | 2.70%–3.04% | 2,121.98 | 2.87% |
| UNKNOWN | 3358 | 0 | 0 | 9.35% | 9.05%–9.66% | 6,919.49 | 9.35% |
| HumPool+F2Pool | 20056 | 1 | 0 | 55.85% | 55.33%–56.36% | 41,334.01 | 55.83% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 2983 blocks, e.g. minerInfo `2.0.1/ZKM1a5bb959d6f29dbad990f232082810540af699b6461b2f20236db3d5f24f56eb8`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 375 blocks, e.g. minerInfo `2.0.1/ZKM1ae207c390f9428346327904e9dae2a9f7f59e8e390b1bcda0c1fb99bcb61b30d`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11037** window blocks (11037 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5517; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5516; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×4
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11037
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9020
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11037 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://lena.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `d4b77f68b9a339e7c3fb8a5be071d25762bd3fc602d943ff095caf9d833d05ba`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35913}.
- Independent enumeration on second node `wss://sara.kaspa.red/kaspa/mainnet/wrpc/json`: 48218 vs 48218 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35914 (9.976 blocks/s), first 2026-10-25T10:00:00.077Z, last 2026-10-25T10:59:59.963Z; per-minute min/max [542, 649]; 60 minutes with blocks; largest timestamp gap 1335 ms.
- Boundary counts: {'[start-1s,start)': 14, '[start,start+1s)': 4, '[end-1s,end)': 10, '[end,end+1s)': 6}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35913, RED 1, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
