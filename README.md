# DurationQuantileTape

A bounded rolling distribution of duration intervals extracted from independently fetched RFC prose. This is an experimental GenLayer primitive, not an audited production oracle.

## Problem and consequential AI

Protocol documents express defaults, permitted alternatives and finite duration ranges in prose. A conventional chain can rank supplied numbers but cannot acquire and interpret those distinctions itself. Here an AI extraction determines whether a sample enters the window, its integer millisecond bounds and which previous sample is evicted. Validators independently fetch and interpret the complete source; they do not simply rerun deterministic graph edits.

## Architecture

`Immutable quantity/feed → RFC Editor acquisition → hash check → independent semantic interval extraction → exact report agreement → ring insertion/eviction → bounded quantile`

No graph proposals, certificates, token consumption or caller-supplied outcome scores. Storage separates immutable reports, permanently spent source IDs and a bounded circular window. Unknown evidence is retained as HELD without changing the distribution.

## Consensus and state

Each full report binds feed, sample, owner, exact quantity, RFC URL, commitment, parent window root, HTTP status, body/hash and interval. The leader and each validator independently perform web acquisition and AI extraction. Complete exact equality is required; no tolerance or majority shortcut in the contract. A disagreement cannot install a window update; network consensus may reject or retry execution. It does not manufacture a recorded CONFLICTED result.

`EMPTY → APPENDED/window update` or `HELD/unchanged window`. Query states are EMPTY, BOUNDED or STALE. Sample/source IDs remain spent even for HELD results. Source failure can therefore require a new feed; intentional tradeoff against repeated semantic grinding.

## Quantile definition

For n retained samples, nearest rank is max(1, ceil(p*n/100)). Independently sorted lower and upper endpoints give conservative bounds on that rank for any point realization within each interval. p=0 selects the minimum. This is not interpolation: p50 of two exact samples 1000 and 3000 is 1000. Capacity is 2–16. Evicted reports and event roots remain readable permanently.

## Security and limitations

Feed creation is open; only the bound creator can append. Feed definitions never change. Reports, replay markers and event history are immutable; IDs are feed-namespaced. Source URLs are constructed from integer RFC IDs, never arbitrary hosts. Hashes alone cannot approve a sample: full evidence and semantic extraction are required. Observation timestamps are transaction-derived. Maximum age checks acquisition age, not whether an RFC remains current. Owners choose sources and can bias a distribution. The RFC Editor is a single source authority, not independent real-world witnesses. AI agreement can still be wrong or influenced by hostile text. No payments, assets, economic settlement or current-performance claims are made.

## Example: historical defaults, not current advice

Ask for the recommended default initial TCP retransmission timeout before the first RTT, excluding alternatives and historical comparisons. [RFC 6298](https://www.rfc-editor.org/rfc/rfc6298.txt) recommends one second; obsolete [RFC 2988](https://www.rfc-editor.org/rfc/rfc2988.txt) recommended three seconds. [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.txt) has no relevant duration. These documents demonstrate semantic qualification, not a benchmark or current TCP configuration recommendation.

## Test and deploy

Install Python requirements and `npm ci`; run `genvm-lint check contracts/DurationQuantileTape.py` before `pytest tests -q`. Direct tests use synthetic mocks and do not establish distributed validator agreement. Windows tests narrowly defer runner-owned open temporary-file cleanup without suppressing contract errors.

Use an encrypted GenLayer keystore, select StudioNet with `genlayer network`, then `genlayer deploy --contract contracts/DurationQuantileTape.py`. Never export a private key. Call `genlayer write ADDRESS create_feed --args rto 'Recommended default initial TCP RTO before the first RTT, excluding permitted alternatives and historical comparisons' 2`, then `genlayer write ADDRESS append --args rto modern 6298 HASH`. Fetch/hash full RFC bytes locally first; validators independently reacquire them. Inspect execution receipts, not only FINALIZED status. `node scripts/check.mjs --source ADDRESS` verifies matching deployed source; `node scripts/check.mjs --success HASH` checks leader execution. View `quantile` through `node scripts/view.mjs ADDRESS quantile '["rto",50,604800]'`.

Live addresses and proof coverage, if available, are in LIVE_PROOFS.md. Local ring-eviction coverage must not be mistaken for a live eviction proof.
