# Security

Experimental StudioNet code, unaudited. Do not connect assets or production decisions. Report vulnerabilities privately to the repository owner before public disclosure.

Main risks: owner-controlled sample selection; single RFC hosting authority; incorrect but unanimous semantic extraction; prompt injection; unavailable or changed source; strict equivalence liveness failures; growing immutable history despite bounded active windows. Exact agreement verifies report consistency, not universal truth. Historical documents and acquisition freshness are not evidence of current practice.

No delegated writes, upgrades, funds, transfers or cross-contract calls. Freshness-bounded readers must check state BOUNDED and bind the returned window root. Spent sources include HELD attempts. One-day duration limit and 90,000-byte document limit are deliberate.
