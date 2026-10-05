# StudioNet proof ledger

Contract: [0x938f450450004d413255cC94CD36B41CdF823913](https://explorer-studio.genlayer.com/address/0x938f450450004d413255cC94CD36B41CdF823913)

Normalized deployed source SHA-256: `03fc731a8c9a71f3165ef71da6b89dde82d23331828d40cc13074fd6a14841a0`.
The deployed source matches contracts/DurationQuantileTape.py (LF normalization and final newline). No contract changes were made after deployment.

## Verified proof matrix

| Scenario | Transaction | Final receipt / observed outcome |
| --- | --- | --- |
| Deployment | [8b489a…a8a54f9](https://explorer-studio.genlayer.com/tx/0x8b489a083de41a61d0948758c3e4d0709536b2a7d46973207e879744aa8a54f9) | FINALIZED, leader SUCCESS, MAJORITY_AGREE |
| Immutable feed creation | [2b6e67…fbc55ac](https://explorer-studio.genlayer.com/tx/0x2b6e67cc3b2b652eb895bee9c84f5a9b93ab38697cadaff4f4181f25dfbc55ac) | FINALIZED, leader SUCCESS, MAJORITY_AGREE; rto capacity 2 |
| Independent RFC 6298 extraction | [53cd11…ea73f9a](https://explorer-studio.genlayer.com/tx/0x53cd1112e24e02c9a06eb9e1315dab8a53163da08976fb2a66e76dd25ea73f9a) | FINALIZED, leader SUCCESS, MAJORITY_AGREE; report APPENDED/EXACT, 1000–1000 ms |

Readback report root: `d5004e3f7afb527edb4d4236e1c6a69d86fdc7bd7804ab47038e3903abef1b54`.
Acquired RFC 6298 full-response hash: `f3a6d937c0a7653bd431fdbbdcd7920f4e9d9cdb6134fa9db7a74b90d215edf6`.
Read-only p50 query returned BOUNDED, count 1, 1000–1000 ms, with window root `a60032571128632270272645c29f7699d695291e6506d0a90fdadb94773a7835`. This query is state readback, not an additional transaction proof.

The quantity is the historical document's recommended default initial TCP retransmission timeout before the first RTT measurement, excluding permitted alternatives and historical comparisons. This is not current configuration advice or observed network performance.

## Pending — not a completed usage proof

[Historical RFC 2988 observation](https://explorer-studio.genlayer.com/tx/0x989ad953e77dbd0611d8f1e39a0a6e4ae7ffac9868019555dc9acf5495064cb9) was broadcast but remains COMMITTING in the latest checked receipt. No applied interval or final agreement is claimed for it. Do not rebroadcast this observation while its outcome is unresolved.

Irrelevant-source, mismatch and replay calls have not been broadcast yet. They must not be listed as live proofs. Ring eviction, freshness, access control and equivalence disagreement currently have local mock/helper coverage only. Fourteen local tests pass; that is not distributed validator proof.

## Verification

Use `node scripts/check.mjs --source ADDRESS` and `node scripts/check.mjs --success TX_HASH`; inspect execution, not just lifecycle status. An optional Windows read-only HTTPS fallback is `node --require ./scripts/windows_read_transport.cjs scripts/check.mjs --success TX_HASH`. It requires PowerShell 7, applies only to public read RPC methods and never retries broadcasts.

CLI receipt polling timed out after successful broadcasts. Raw RPC receipt checks and state readback establish the results above; a CLI timeout alone is neither proof of failure nor permission to rebroadcast. Agreement was majority, not claimed unanimous.
