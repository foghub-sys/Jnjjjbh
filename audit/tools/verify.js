// Independent cross-checks against a second node:
//  1. --enum: re-enumerate the DAG hash set (getBlocks, hashes only) from the same lowHash
//     until the same final page boundary, to compare against the primary collection.
//  2. --sample: for each sampled hash, save the verbatim raw responses of getBlock,
//     getBlockRewardInfo (and getBlock of its merging chain block) from every node, plus the REST indexer record.
//
// usage: node verify.js --out DIR --nodes wss://a,wss://b [--enum LOW:UNTIL] [--sample hashes.txt]
const fs = require('fs');
const path = require('path');
const { Rpc } = require('./rpc');

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => {
  if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1]]);
  return acc;
}, []));
const OUT = args.out;
const NODES = args.nodes.split(',');
const REST = args.rest || 'https://api.kaspa.org';
fs.mkdirSync(OUT, { recursive: true });
const log = (...a) => console.log(new Date().toISOString(), ...a);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function retry(fn, tries = 4) {
  for (let i = 1; ; i++) {
    try { return await fn(); } catch (e) { if (i >= tries) throw e; await sleep(1000 * 2 ** i); }
  }
}

async function enumerate(url, low, until) {
  const rpc = new Rpc(url); await rpc.connect();
  const info = (await rpc.call('getServerInfo')).result;
  const seen = new Set();
  let pages = 0;
  for (;;) {
    const { result } = await retry(() => rpc.call('getBlocks', { lowHash: low, includeBlocks: false, includeTransactions: false }, 120000));
    pages++;
    for (const h of result.blockHashes) seen.add(h);
    const high = result.blockHashes[result.blockHashes.length - 1];
    if (seen.has(until) || high === low) break;
    low = high;
  }
  rpc.close();
  return { node: url, serverInfo: info, pages, reachedUntil: seen.has(until), hashes: [...seen] };
}

async function sample(hashes) {
  const conns = [];
  for (const url of NODES) { const r = new Rpc(url); await r.connect(); conns.push(r); }
  const dir = path.join(OUT, 'raw_samples');
  fs.mkdirSync(dir, { recursive: true });
  const failures = [];
  for (const [i, h] of hashes.entries()) {
    const rec = { hash: h, fetchedAt: new Date().toISOString(), responses: [] };
    for (const [k, rpc] of conns.entries()) {
      for (const [method, params] of [['getBlock', { hash: h, includeTransactions: true }], ['getBlockRewardInfo', { hash: h }]]) {
        try {
          const { raw } = await retry(() => rpc.call(method, params));
          rec.responses.push({ node: NODES[k], method, params, raw });
          if (method === 'getBlockRewardInfo' && k === 0) {
            const m = JSON.parse(raw).params.mergingChainBlockHash;
            if (m) {
              const mb = await retry(() => rpc.call('getBlock', { hash: m, includeTransactions: true }));
              rec.responses.push({ node: NODES[k], method: 'getBlock', params: { hash: m, includeTransactions: true }, role: 'mergingChainBlock', raw: mb.raw });
            }
          }
        } catch (e) {
          failures.push({ hash: h, node: NODES[k], method, error: e.message });
        }
      }
    }
    try {
      const r = await retry(async () => {
        const res = await fetch(`${REST}/blocks/${h}?includeColor=true&includeTransactions=true`);
        if (!res.ok) throw new Error(`REST ${res.status}`);
        return res.text();
      });
      rec.responses.push({ node: REST, method: 'GET /blocks/{hash}?includeColor=true&includeTransactions=true', raw: r });
    } catch (e) {
      failures.push({ hash: h, node: REST, error: e.message });
    }
    fs.writeFileSync(path.join(dir, `${h}.json`), JSON.stringify(rec, null, 1));
    if ((i + 1) % 25 === 0) log('sampled', i + 1, '/', hashes.length);
  }
  conns.forEach((c) => c.close());
  return failures;
}

(async () => {
  const report = { nodes: NODES, startedAt: new Date().toISOString() };
  if (args.enum) {
    const [low, until] = args.enum.split(':');
    const res = await enumerate(NODES[NODES.length - 1], low, until);
    fs.writeFileSync(path.join(OUT, 'enum_secondary.json'), JSON.stringify(res));
    report.enum = { node: res.node, serverInfo: res.serverInfo, pages: res.pages, reachedUntil: res.reachedUntil, count: res.hashes.length };
    log('secondary enumeration', JSON.stringify(report.enum));
  }
  if (args.sample) {
    const hashes = fs.readFileSync(args.sample, 'utf8').split('\n').filter(Boolean);
    report.sampleFailures = await sample(hashes);
    report.sampleCount = hashes.length;
    log('sample done, failures', report.sampleFailures.length);
  }
  report.finishedAt = new Date().toISOString();
  fs.writeFileSync(path.join(OUT, `verify_report_${Date.now()}.json`), JSON.stringify(report, null, 2));
})().catch((e) => { console.error('FATAL', e); process.exit(1); });
