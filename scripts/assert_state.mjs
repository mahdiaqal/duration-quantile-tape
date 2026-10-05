import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import dns from 'node:dns';
dns.setDefaultResultOrder('ipv4first');
const [address] = process.argv.slice(2);
if (!/^0x[0-9a-fA-F]{40}$/.test(address ?? '')) throw Error('Address required');
const client = createClient({chain: studionet});
const read = async (functionName, args) => {
  for (let attempt = 0; attempt < 3; attempt++) {
    try { return await client.readContract({address, functionName, args}); }
    catch (error) { if (attempt === 2) throw Error(`Read ${functionName} failed (${error.code ?? 'RPC'})`); }
  }
};
const asNumber = x => Number(x);
const feed = await read('get_feed', ['rto']);
assert.equal(asNumber(feed.accepted), 2);
assert.equal(asNumber(feed.held), 2);
const current = await read('window', ['rto']);
assert.deepEqual(current.map(r => r.spec.sample), ['modern', 'historical']);
for (const [sample, value] of [['modern', 1000], ['historical', 3000]]) {
  const report = await read('get_report', ['rto', sample]);
  assert.equal(report.state, 'APPENDED');
  assert.equal(report.kind, 'EXACT');
  assert.equal(asNumber(report.lower_ms), value);
  assert.equal(asNumber(report.upper_ms), value);
  assert.equal(crypto.createHash('sha256').update(report.text).digest('hex'), report.spec.expected_hash);
}
for (const sample of ['irrelevant', 'mismatch']) {
  const report = await read('get_report', ['rto', sample]);
  assert.equal(report.state, 'HELD');
  assert.equal(report.kind, 'UNKNOWN');
}
const p50 = await read('quantile', ['rto', 50, 604800]);
const p100 = await read('quantile', ['rto', 100, 604800]);
assert.equal(p50.state, 'BOUNDED');
assert.equal(asNumber(p50.lower_ms), 1000);
assert.equal(asNumber(p50.upper_ms), 1000);
assert.equal(asNumber(p100.lower_ms), 3000);
assert.equal(asNumber(p100.upper_ms), 3000);
assert.equal(p50.window_root, feed.window_root);
assert.equal(p100.window_root, feed.window_root);
const events = await read('history', [0, 20]);
assert.equal(events.length, 5);
for (let i = 1; i < events.length; i++) assert.equal(events[i].previous, events[i - 1].root);
assert.equal(events[3].window_root, events[2].window_root);
assert.equal(events[4].window_root, events[2].window_root);
console.log(JSON.stringify({address, assertions: 'PASS', accepted: 2, held: 2,
  window_root: feed.window_root, p50_ms: 1000, p100_ms: 3000,
  qualification: 'Historical RFC defaults; not current protocol advice or measured performance'}));
