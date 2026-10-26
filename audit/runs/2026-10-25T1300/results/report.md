# Kaspa mining distribution audit: 2026-10-25T13:00:00.000Z – 2026-10-25T14:00:00.000Z

## Verdict

- HumPool + F2Pool produced **20191 of 35989 confirmed BLUE blocks = 56.10%** (Wilson 95% CI 55.59%–56.62%; minute-cluster bootstrap 95% CI 55.64%–56.54%).
- The claimed 53.9% is **outside** the 95% interval; difference +2.20 percentage points.
- That the two pools' blocks exceed 50% in this window is **supported (whole CI above 50%)**.

## Three claims, kept apart

1. **Two addresses produce more than 50% of blocks.** Checked directly on-chain. The two largest miner addresses (kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j [HumPool], kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp [F2Pool]) produced 56.10% of BLUE blocks in this window.
2. **Two operators control more than 50% of block production.** Not provable from chain data. A pool address and tag show where rewards go and what the block template says; they do not prove who owns the hashrate. A pool's share is the sum of many independent miners who can switch pools. Proving operator control needs off-chain evidence about infrastructure and who controls the hashrate.
3. **Two operators could coordinate active censorship.** Does not follow from (1) or (2). Censorship in GHOSTDAG would require sustained majority control of the selected chain and coordination. This audit measures neither intent nor coordination.

## Shares (denominator: all confirmed BLUE blocks in the window)

| pool | BLUE | RED | UNKNOWN color | share of BLUE | Wilson 95% CI | confirmed reward (KAS) | share of reward |
|---|---|---|---|---|---|---|---|
| HumPool | 11096 | 18 | 0 | 30.83% | 30.36%–31.31% | 22,903.17 | 30.81% |
| F2Pool | 9095 | 22 | 0 | 25.27% | 24.83%–25.72% | 18,776.68 | 25.26% |
| ViaBTC | 4223 | 4 | 0 | 11.73% | 11.41%–12.07% | 8,743.04 | 11.76% |
| K1Pool | 2667 | 7 | 0 | 7.41% | 7.14%–7.69% | 5,498.87 | 7.40% |
| WhalePool | 1159 | 6 | 0 | 3.22% | 3.04%–3.41% | 2,388.35 | 3.21% |
| SOLO | 1720 | 9 | 0 | 4.78% | 4.56%–5.00% | 3,549.56 | 4.78% |
| UNKNOWN | 2667 | 3 | 0 | 7.41% | 7.14%–7.69% | 5,498.13 | 7.40% |
| HumPool+F2Pool | 20191 | 40 | 0 | 56.10% | 55.59%–56.62% | 41,679.85 | 56.07% |

All other pools found are in `pool_shares.csv`. SOLO means untagged, unlabelled addresses with <1% of window blocks each (heuristic). UNKNOWN (pool) means untagged, unlabelled addresses with ≥1% of blocks, whose operator cannot be identified:

- kaspa:qqrprr45fsgj8zrypu6fnz7fku4ct45tzy38m50nka53pdmxl0dds4vtf39f2: 1593 blocks, e.g. minerInfo `2.0.1/ZKM127df2a4a2d3f114b1b35056ca63475d72554447c1b3052a0eda1a92af02dee09`
- kaspa:qqje6ps46n6pvjstupfxgrg6v3pegd22q84jachnfrnz2vh5vznqw8redgln6: 627 blocks, e.g. minerInfo `2.1.0/ZKM16c93d81ae95753da8b712025a7b61c185b5055abdf9f501f620c7ced162817dc`
- kaspa:qzv6lyy49ztas78037umkc9acmrertejgesqsnmjxjrd30fem6em5we3gujgy: 450 blocks, e.g. minerInfo `2.1.0/ZKM1e967dd865e5a83eb9d05bee1800eb6ec5e6d21d4ecafbfd2d98565c51c1204a4`

## HumPool address check

- Address `kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j` is the miner address committed in the block's own coinbase payload of **11114** window blocks (11096 BLUE).
- Payload tags seen with it: `2.1.0/humpool/0.12.20/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5654; `2.1.0/humpool/0.12.9/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×5457; `2.1.0/humpool/0.12.32/canxiuminer:61FAba23a639D1028E74BFfe14c483bb80Be9D0E` ×3
- Addresses used by blocks tagged `humpool`: kaspa:qrk9decfnl4rayeegp6gd3tc6605zavclkpud5jp78axat5namppwt050d57j ×11114
- Addresses used by blocks tagged `F2Pool`: kaspa:qpamkvhgh0kzx50gwvvp5xs8ktmqutcy3dfs9dc3w7lm9rq0zs76vf959mmrp ×9117
- Explorer label (third-party, secondary): `HumPool`.
- For comparison only (not used): this address appears in 11097 coinbase outputs of window chain blocks. Those outputs pay for *earlier merged* blocks, so counting recipients assigns rewards to the wrong blocks.

## Method

- Primary source: rusty-kaspa node `wss://eva.kaspa.green/kaspa/mainnet/wrpc/json` (version 2.1.0, synced, wRPC JSON). All blocks were paged with `getBlocks` from `b7798cceb618c6c9ba44d516de160e1bf0fef69783b7b7b60a2f331cd07382cd`, which returns every block merged by the selected chain, blue and red, not only chain blocks. Margin of 600s on each side; 197 pages, contiguous: True.
- Window rule: header timestamp in [start, end). Miner identity comes from the block's own coinbase payload (committed script public key → address, plus extra data → minerInfo). Payout recipients are never used.
- Color and reward come from `GetBlockRewardInfo` for every window block. A block is BLUE/RED only if that RPC says so; otherwise it stays UNKNOWN.
- Consensus cross-check of every BLUE block's miner address: the output at the block's index in its merging chain block's coinbase must pay the payload script with the reported reward. Result: {'match': 35989}.
- Independent enumeration on second node `wss://vivi.kaspa.blue/kaspa/mainnet/wrpc/json`: 48450 vs 48450 hashes; only-in-primary 0, only-in-secondary 0, window blocks missing on secondary 0.
- Reproducible random sample: 128 blocks, `sha256(seed + hash) ascending over all window blocks, first N`, seed `kaspa-audit/2026-10-26T12:00:00Z/2026-10-26T13:00:00Z`. Verbatim raw responses from both nodes and the REST indexer are in `raw/verify/raw_samples/`. Checks: {'header_hash_recomputed_ok=True': 128, 'nodes_agree_block=True': 128, 'nodes_agree_reward_info=True': 128, 'rest_payload_matches=True': 128, 'merging_coinbase_pays_payload_script=True': 128, 'merging_chain_hash_recomputed_ok=True': 128, 'csv_row_matches_raw=True': 128}.
- CI: Wilson score interval treating blocks as Bernoulli draws of the underlying share. A minute-cluster bootstrap (10,000 resamples) allows for clustering in time. The realised count for the window is exact; the intervals describe the underlying hashrate share.

## Completeness and errors

- Window blocks: 36059 (10.016 blocks/s), first 2026-10-25T13:00:00.081Z, last 2026-10-25T13:59:59.915Z; per-minute min/max [556, 648]; 60 minutes with blocks; largest timestamp gap 1192 ms.
- Boundary counts: {'[start-1s,start)': 13, '[start,start+1s)': 4, '[end-1s,end)': 22, '[end,end+1s)': 2}. Blocks outside the window by timestamp but inside its DAA-score range: 0.
- Colors: BLUE 35989, RED 70, UNKNOWN 0. GetBlockRewardInfo failures after retries: 0; transient errors retried: 0.
- Duplicates removed: 196 (getBlocks pages repeat their lowHash), reward-info duplicates 0. Parse/consistency errors: none.

## Limitations

- Blocks never merged by the selected chain are not returned by `getBlocks`. The second-node enumeration covers the same blocks, not orphans; such blocks earn no reward and do not affect BLUE shares.
- Both nodes come from the same public resolver network and may share an operator. The header-hash recomputation and the consensus payout cross-check reduce, but do not remove, reliance on them.
- Pool names rely on miner-supplied payload tags. `wpool` → WhalePool is supported by the third-party explorer label of the same address.
- Public nodes are pruned (about 40 h of history). 24-hour analysis is feasible; 7 days needs an archival node or an indexer.
