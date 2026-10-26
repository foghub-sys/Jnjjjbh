# Kaspa mining distribution audit: 2026-10-25T16:00:00.000Z – 2026-10-25T17:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20178 of 35764 confirmed BLUE blocks = 56.42%** (Wilson 95% CI 55.91%–56.93%; minute-cluster bootstrap 95% CI 55.82%–57.00%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.52 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.42% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11110 | 7 | 0 | 31.06% | 30.59%–31.55% | 22,896.11 | 31.02% |
| F2Pool | 9068 | 11 | 0 | 25.36% | 24.91%–25.81% | 18,697.39 | 25.33% |
| ViaBTC | 4111 | 4 | 0 | 11.49% | 11.17%–11.83% | 8,507.02 | 11.53% |
| K1Pool | 2570 | 3 | 0 | 7.19% | 6.92%–7.46% | 5,295.69 | 7.18% |
| WhalePool | 1108 | 1 | 0 | 3.10% | 2.92%–3.28% | 2,283.21 | 3.09% |
| SOLO | 1186 | 0 | 0 | 3.32% | 3.14%–3.51% | 2,448.41 | 3.32% |
| UNKNOWN | 3431 | 5 | 0 | 9.59% | 9.29%–9.90% | 7,072.57 | 9.58% |
| HumPool+F2Pool | 20178 | 18 | 0 | 56.42% | 55.91%–56.93% | 41,593.50 | 56.36% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3053 blocks, e.g. minerInfo `2.0.1/ZKM1e07bffe1c1f418e251b9a884c3227871ee91ec6304c1305b41e309e0f34a884c`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 383 blocks, e.g. minerInfo `2.0.1/ZKM19ebc73d54216717696ff854c4def0a2876f6ce3ecce56eaec65743044b5bea32`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11117** window blocks (11110 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5669; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5448
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11117
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9079
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11112 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://kate.kaspa.red/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `3b2fa02c67fbde55c8dd4ee8359515a1ad95617747680ad9ef2765bb88a49aa5`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 196 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35764}.
- Independent enumeration on second node `wss://emma.kaspa.stream/kaspa/mainnet/wrpc/json`: 48214 vs 48214 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35797 (9.944 blocks/s), first 2026-10-25T16:00:00.334Z, last 2026-10-25T16:59:59.969Z; per-minute min/max [550, 645]; 60 minutes with blocks; largest timestamp gap 1362 ms.
- Boundary counts: {'[start-1s,start)': 8, '[start,start+1s)': 12, '[end-1s,end)': 8, '[end,end+1s)': 22}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35764, RED 33, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 195 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
