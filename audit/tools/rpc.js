// Minimal wRPC-JSON client for rusty-kaspa with request pipelining.
const WebSocket = require('ws');

class Rpc {
  constructor(url) { this.url = url; this.id = 1; this.pending = new Map(); }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url, { maxPayload: 1 << 30 });
      this.ws.on('open', resolve);
      this.ws.on('error', reject);
      this.ws.on('close', () => {
        this.closed = true;
        for (const [, p] of this.pending) { clearTimeout(p.timer); p.reject(new Error('socket closed')); }
        this.pending.clear();
      });
      this.ws.on('message', (m) => {
        const raw = m.toString();
        const msg = JSON.parse(raw);
        const p = this.pending.get(msg.id);
        if (!p) return;
        this.pending.delete(msg.id);
        clearTimeout(p.timer);
        if (msg.error) p.reject(Object.assign(new Error(msg.error.message), { raw }));
        else p.resolve({ result: msg.params, raw });
      });
    });
  }

  call(method, params = {}, timeoutMs = 60000) {
    if (this.closed) return Promise.reject(new Error('socket closed'));
    const id = this.id++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => { this.pending.delete(id); reject(new Error(`timeout ${method}`)); }, timeoutMs);
      this.pending.set(id, { resolve, reject, timer });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  close() { this.ws.close(); }
}

module.exports = { Rpc };
