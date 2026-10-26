# Kaspa mining distribution audit: 2026-10-25T18:00:00.000Z – 2026-10-25T19:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20039 of 35735 confirmed BLUE blocks = 56.08%** (Wilson 95% CI 55.56%–56.59%; minute-cluster bootstrap 95% CI 55.46%–56.72%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.18 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.08% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11011 | 9 | 0 | 30.81% | 30.34%–31.29% | 22,708.98 | 30.78% |
| F2Pool | 9028 | 32 | 0 | 25.26% | 24.82%–25.72% | 18,621.54 | 25.24% |
| ViaBTC | 4215 | 3 | 0 | 11.80% | 11.46%–12.13% | 8,722.53 | 11.82% |
| K1Pool | 2556 | 5 | 0 | 7.15% | 6.89%–7.42% | 5,270.73 | 7.14% |
| WhalePool | 1137 | 0 | 0 | 3.18% | 3.00%–3.37% | 2,343.43 | 3.18% |
| SOLO | 1150 | 2 | 0 | 3.22% | 3.04%–3.41% | 2,373.11 | 3.22% |
| UNKNOWN | 3398 | 2 | 0 | 9.51% | 9.21%–9.82% | 7,021.85 | 9.52% |
| HumPool+F2Pool | 20039 | 41 | 0 | 56.08% | 55.56%–56.59% | 41,330.52 | 56.02% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 3011 blocks, e.g. minerInfo `2.0.1/ZKM1692e42220b5858234ff0a046d1a7ebabe4dbeaaea302101b251b32c56b8c9430`
- kaspa:qqg7cs2e8vh4k2y9ashwqxvv8z5n7rhx0w3kuu3gcwgmrpmzw8luvuwchhsn4: 389 blocks, e.g. minerInfo `2.0.1/ZKM1c06e7510574f44d4070f4fda846c544119ebabbacbe37a1b8f309b0798652e54`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11020** window blocks (11011 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5540; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5479; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×1
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11020
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9060
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11016 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `6f98396cf0391d74c51c695c9338af24a31b7a0fbf89bd0d4f72117c0350aef1`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 195 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35735}.
- Independent enumeration on second node `wss://ava.kaspa.stream/kaspa/mainnet/wrpc/json`: 48019 vs 48019 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 35790 (9.942 blocks/s), first 2026-10-25T18:00:00.022Z, last 2026-10-25T18:59:59.636Z; per-minute min/max [512, 653]; 60 minutes with blocks; largest timestamp gap 1639 ms.
- Boundary counts: {'[start-1s,start)': 13, '[start,start+1s)': 15, '[end-1s,end)': 4, '[end,end+1s)': 15}. Blocks outside the window by timestamp but inside its DAA-score range: 3.
- Colors: BLUE 35735, RED 55, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 3.
- Duplicates removed: 194 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
