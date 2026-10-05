# Submission — verified live scope

Contribution type: Builder → Intelligent Contracts

Title: DurationQuantileTape — Evidence-Derived Rolling Interval Statistics

Description:

DurationQuantileTape is a reusable rolling-statistics primitive, not a graph proposal or certificate variant. The contract fetches complete RFC Editor documents and verifies SHA-256 commitments. Leader and validators independently interpret duration quantities, units, defaults and qualifications; exact equality of the evidence-bearing report is required. Accepted intervals populate a bounded circular window, evicting its oldest sample. UNKNOWN or mismatched evidence is retained as HELD without changing the distribution. Quantile queries return conservative nearest-rank interval bounds and fail closed on stale observations. Immutable reports, feed-bound identities and permanent sample/source replay guards constrain mutation. StudioNet deployment, feed creation and RFC 6298 extraction finalized successfully; readback confirms an exact 1000 ms historical default. Fourteen local tests pass. Further lifecycle proofs remain pending; historical document values are not measured performance.

Evidence:

- https://github.com/mahdiaqal/duration-quantile-tape
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/contracts/DurationQuantileTape.py
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/README.md
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/tests/test_tape.py
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/LIVE_PROOFS.md
- https://explorer-studio.genlayer.com/address/0x938f450450004d413255cC94CD36B41CdF823913
- https://explorer-studio.genlayer.com/tx/0x8b489a083de41a61d0948758c3e4d0709536b2a7d46973207e879744aa8a54f9
- https://explorer-studio.genlayer.com/tx/0x2b6e67cc3b2b652eb895bee9c84f5a9b93ab38697cadaff4f4181f25dfbc55ac
- https://explorer-studio.genlayer.com/tx/0x53cd1112e24e02c9a06eb9e1315dab8a53163da08976fb2a66e76dd25ea73f9a

Claim only the finalized live scope above. The second observation is pending; eviction and adversarial paths are not yet live-proven. Historical RFC values are not current protocol advice. Local tests use mocked evidence and cannot prove distributed validator agreement.
