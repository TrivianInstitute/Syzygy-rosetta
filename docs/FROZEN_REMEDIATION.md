# Frozen audit remediation — candidate 2.1.0

Frozen base: 68b850af8de79c1af181fa61cc496b7e5ff65019 (2.0.0). Frozen witnesses are preserved externally without edits. New tests are in `tests/test_frozen_remediation.py`.

## Authority ownership (F013/F015)

AuthorityGrant construction and dataclass reconstruction normalize supported status strings to AuthorityStatus. Unknown states fail at construction. Scope becomes a frozenset of nonempty strings. Metadata is copied into a read-only string mapping; unsupported nested values are rejected rather than retained by reference. State digest is a scalar string. Registry lifecycle mutations are serialized in process. This does not claim distributed atomic authorization plus execution.

## Queued subject identity (F014 specification decision)

A queued reference now captures the grant subject. Current resolution must match that subject. A higher version may change a registry subject, but cannot transfer an older subject's queued authority. References without a subject fail closed and must be rebuilt from authoritative state, not automatically filled from a current grant. This is a serialized-reference compatibility break. Host authentication still must establish the actual executing principal; the registry does not authenticate people or external callers.

## Scoring evidence (F046 specification decision)

The original witness and its criterion are retained: invariant vocabulary must not let a violating response obtain a perfect governance-fidelity score. The old keyword function was not an implementation of semantic or behavioral fidelity. Adding more keywords or embeddings would not establish current authority, consent, scope or compliance.

`lexical_signal` retains that experimental heuristic under an explicitly untrusted name. It can still return 1.0 for the frozen violating sentence, and that result is not governance evidence. `assess_governance` runs host-owned behavioral checks for `authority_current`, `consent_current`, `scope_valid`, and `constraints_preserved` (plus additional supplied checks) against the exact input/response. Any false check yields FAILS; absent, exceptional or nonboolean evidence yields UNRESOLVED and no score. Only all true checks yield SURVIVES for those checks. The host is responsible for authoritative data and meaningful callbacks. A callback that merely returns True is not independent evidence.

The compatibility scalar `evaluate_coherence` returns 0.0 when evidence is missing/invalid/violated. Use `assess_governance` to distinguish uncertainty from a known violation. An invariant vocabulary dictionary alone never supplies a positive score. `breath_loop` records its governance assessment as UNRESOLVED, keeps any lexical signal separate and emits no success note from keyword padding. These results do not authorize external consequences or establish arbitrary-language fidelity. F050 remains unresolved.

This is an explicit behavior/API decision, not a claim that the historical promise of semantic fidelity has now been implemented. The bounded frozen F046 assertion can pass because unsupported positive evidence is withheld; universal semantic validity remains unestablished. The original scalar-only evaluation harness has legacy high/low vocabulary expectations and must be interpreted separately from the new behavioral tests.

## Compatibility and packaging

Package/public version is 2.1.0. The existing test's exact version literal changes from 2.0.0 to 2.1.0 only; all governance assertions and frozen witnesses are unchanged. Its old file is preserved and rerun separately in revalidation evidence, where the expected literal-version mismatch is reported. Existing PDF and historical verification notes retain their historical claims/versions; this document is the candidate's operational contract.

Scope/metadata containers and queued references have stricter construction and serialization behavior. MappingProxyType metadata should be exported as a dict explicitly; arbitrary pickled objects are not a supported authority interchange format. No persisted grant migration is implemented. The existing stale-authority, missing registry, narrowed scope, expiry and resolver-exception witnesses must still run unchanged.
