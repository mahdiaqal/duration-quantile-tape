# Submission draft — deployment pending

Contribution type: Builder → Intelligent Contracts

Title: DurationQuantileTape — Evidence-Derived Rolling Interval Statistics

Description:

DurationQuantileTape is a reusable bounded statistical primitive, not a graph proposal or certificate variant. A feed defines a duration quantity; the contract independently fetches complete RFC Editor documents and checks exact SHA-256 commitments. Leader and validators separately interpret normative prose, defaults, alternatives and units to extract integer-millisecond intervals. Exact equality of the full evidence-bearing report is required. Known intervals enter a circular window and evict its oldest sample; UNKNOWN or mismatched evidence is retained as HELD without changing the distribution. Quantile queries return conservative nearest-rank bounds tied to the window root and fail closed on stale observations. Feed-bound identities, permanent sample/source replay guards and immutable history constrain mutation. Fourteen local tests cover extraction, eviction, replay, authorization, hash substitution and freshness. Deployment and distributed execution proofs are pending.

Evidence:

- https://github.com/mahdiaqal/duration-quantile-tape
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/contracts/DurationQuantileTape.py
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/README.md
- https://github.com/mahdiaqal/duration-quantile-tape/blob/main/tests/test_tape.py

Do not represent this draft as a demonstrated onchain lifecycle. No successful deployment receipt exists yet. Historical RFC values are not current protocol advice or measured performance. Local tests use mocked evidence and cannot prove distributed validator agreement.
