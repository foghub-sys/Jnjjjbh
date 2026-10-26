// Enumerates every block of the Kaspa BlockDAG whose header timestamp falls in [start, end)
// via getBlocks paging from a public rusty-kaspa node (wRPC JSON), then queries
// getBlockRewardInfo for each in-window block.
//
// usage: node collect.js --start 2026-10-26T12:00:00Z --end 2026-10-26T13:00:00Z --out DIR --node wss://...
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const { Rpc } = require('./rpc');

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => {
  if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1]]);
  return acc;
}, []));
const START = Date.parse(args.start);
const END = Date.parse(args.end);
const MARGIN = Number(args.margin || 600) * 1000;
const OUT = args.out;
const NODE = args.node;
const REST = args.rest || 'https://api.kaspa.org';
const CONCURRENCY = Number(args.concurrency || 16);
fs.mkdirSync(OUT, { recursive: true });

const sha256 = (s) => crypto.createHash('sha256').update(s).digest('hex');
const log = (...a) => console.log(new Date().toISOString(), ...a);
const gz = (name) => { const z = zlib.createGzip(); z.pipe(fs.createWriteStream(path.join(OUT, name))); return z; };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function retry(fn, label, errors, tries = 4) {
  for (let i = 1; ; i++) {
    try { return await fn(); } catch (e) {
      errors.push({ label, attempt: i, error: e.message, at: new Date().toISOString() });
      if (i >= tries) throw e;
      await sleep(1000 * 2 ** i);
    }
  }
}

async function restJson(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url} -> ${r.status}`);
  return r.json();
}

// Find a block whose timestamp is before `target` (used only as a starting pointer for getBlocks paging).
async function locateLowHash(rpc, target, errors) {
  const dag = (await rpc.call('getBlockDagInfo')).result;
  const sink = (await rpc.call('getBlock', { hash: dag.sink, includeTransactions: false })).result.block.header;
  let bs = Math.floor(sink.blueScore - ((sink.timestamp - target) / 1000) * 9.9);
  const probes = [];
  for (let round = 0; round < 6; round++) {
    let found = null;
    for (let k = 0; k < 30 && !found; k++) {
      const arr = await retry(() => restJson(`${REST}/blocks-from-bluescore?blueScore=${bs + k}&includeTransactions=false`), 'locate', errors);
      if (arr.length) found = arr[0];
    }
    if (!found) throw new Error('no block found near blue score ' + bs);
    const ts = Number(found.header.timestamp);
    probes.push({ blueScore: Number(found.header.blueScore), hash: found.verboseData.hash, timestamp: ts });
    const diffSec = (ts - target) / 1000;
    if (diffSec <= 0 && diffSec > -120) return { lowHash: found.verboseData.hash, probes };
    bs = Math.floor(Number(found.header.blueScore) - diffSec * 9.9 - 300);
  }
  throw new Error('could not locate low hash');
}

function compactBlock(b) {
  const { parentsByLevel, ...header } = b.header;
  return {
    header: { ...header, parentsLevel0: parentsByLevel[0], parentLevels: parentsByLevel.length },
    verboseData: { ...b.verboseData, childrenHashes: undefined, transactionIds: undefined, txCount: b.verboseData.transactionIds.length },
    coinbase: b.transactions[0],
  };
}

(async () => {
  const errors = [];
  const meta = { node: NODE, rest: REST, start: new Date(START).toISOString(), end: new Date(END).toISOString(), marginSec: MARGIN / 1000, startedAt: new Date().toISOString() };
  const rpc = new Rpc(NODE); await rpc.connect();
  meta.serverInfo = (await rpc.call('getServerInfo')).result;
  const dagInfo = (await rpc.call('getBlockDagInfo')).result;
  meta.blockDagInfoAtStart = dagInfo;
  log('server', JSON.stringify(meta.serverInfo));

  const loc = await locateLowHash(rpc, START - MARGIN, errors);
  meta.locate = loc;
  log('lowHash', loc.lowHash, JSON.stringify(loc.probes));

  // ---- Phase A: enumerate the DAG ----
  const blocksOut = gz('dag_blocks.jsonl.gz');
  const pagesOut = fs.createWriteStream(path.join(OUT, 'pages.jsonl'));
  const seen = new Set();
  const inWindow = [];
  let low = loc.lowHash, page = 0, pastEnd = false;
  let minTs = Infinity, maxTs = -Infinity, dupes = 0;
  while (!pastEnd) {
    const { result, raw } = await retry(() => rpc.call('getBlocks', { lowHash: low, includeBlocks: true, includeTransactions: true }, 120000), `getBlocks ${low}`, errors);
    page++;
    const hashes = result.blockHashes;
    let added = 0;
    for (const b of result.blocks) {
      const h = b.header.hash;
      if (seen.has(h)) { dupes++; continue; }
      seen.add(h); added++;
      const ts = b.header.timestamp;
      minTs = Math.min(minTs, ts); maxTs = Math.max(maxTs, ts);
      const rec = compactBlock(b);
      rec.page = page;
      blocksOut.write(JSON.stringify(rec) + '\n');
      if (ts >= START && ts < END) inWindow.push(h);
    }
    const high = hashes[hashes.length - 1];
    const highBlock = result.blocks[result.blocks.length - 1];
    pagesOut.write(JSON.stringify({ page, lowHash: low, highHash: high, returned: hashes.length, added, bytes: raw.length, sha256: sha256(raw), highTimestamp: highBlock.header.timestamp, highIsChain: highBlock.verboseData.isChainBlock }) + '\n');
    if (page % 10 === 0) log('page', page, 'seen', seen.size, 'inWindow', inWindow.length, 'highTs', new Date(highBlock.header.timestamp).toISOString());
    if (high === low) { errors.push({ label: 'paging', error: 'reached sink before end+margin' }); break; }
    if (highBlock.header.timestamp > END + MARGIN) pastEnd = true;
    low = high;
  }
  await new Promise((r) => blocksOut.end(r));
  pagesOut.end();
  meta.pages = page;
  meta.dagBlocksSeen = seen.size;
  meta.duplicatesSkipped = dupes;
  meta.dagTimestampRange = [new Date(minTs).toISOString(), new Date(maxTs).toISOString()];
  meta.inWindowFromGetBlocks = inWindow.length;
  log('enumeration done', seen.size, 'in window', inWindow.length);

  // ---- Phase B: getBlockRewardInfo for every in-window block ----
  const rewardOut = gz('reward_info.jsonl.gz');
  let idx = 0, done = 0;
  const failed = [];
  async function worker() {
    while (idx < inWindow.length) {
      const h = inWindow[idx++];
      try {
        const { result, raw } = await retry(() => rpc.call('getBlockRewardInfo', { hash: h }, 60000), `rewardInfo ${h}`, errors);
        const { header, ...rest } = result;
        rewardOut.write(JSON.stringify({ hash: h, ...rest, headerHash: header.hash, rawSha256: sha256(raw), fetchedAt: Date.now() }) + '\n');
      } catch (e) {
        failed.push({ hash: h, error: e.message });
      }
      if (++done % 2000 === 0) log('rewardInfo', done, '/', inWindow.length);
    }
  }
  await Promise.all(Array.from({ length: CONCURRENCY }, worker));
  await new Promise((r) => rewardOut.end(r));
  meta.rewardInfoFailed = failed;
  meta.blockDagInfoAtEnd = (await rpc.call('getBlockDagInfo')).result;
  meta.finishedAt = new Date().toISOString();
  meta.errors = errors;
  fs.writeFileSync(path.join(OUT, 'collect_meta.json'), JSON.stringify(meta, null, 2));
  log('done; rewardInfo failures', failed.length, 'transient errors', errors.length);
  rpc.close();
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
