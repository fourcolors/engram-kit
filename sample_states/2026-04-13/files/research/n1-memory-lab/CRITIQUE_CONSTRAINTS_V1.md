# CRITIQUE_CONSTRAINTS_V1

This memo defines the minimum benchmark discipline required before any public claim. If these constraints are not satisfied, the result is not a hard benchmark result. It is internal exploration.

## data integrity

- Every scored item must map to a frozen raw-trace window with source identity, time bounds, and coverage recorded.
- No prompt, rubric, or report may rely on evidence not present in the frozen bundle.
- Control, threshold, and Syke-native items must be built from real slices, not hand-authored composites designed to flatter the thesis.
- If an item cannot survive adversarial provenance review, it is out.
- If source coverage is partial, that incompleteness must be declared at item level, not hidden in narrative prose.

## bundle/object integrity

- The raw cross-harness trace is the primary object. Replay bundles, normalized stores, and convenience DBs are derived transport only.
- No benchmark language may quietly substitute the transport layer for the memory object under test.
- Every bundle used for scoring must carry a parity hash, derivation note, and explicit canonical/distractor artifact list.
- Bundle freezing happens before scored runs. Post hoc bundle cleanup is contamination.
- If the bundle cannot support same-data replay across architectures, the architecture claim is inadmissible.

## architecture parity

- Track C comparisons are invalid unless prompt text, bundle, order, budget, retry policy, and rubric are held constant.
- We do not compare a polished Syke path against crippled baselines. Each architecture gets a serious, competent instantiation.
- Native memory, provider/plugin memory, and Syke must be evaluated at the boundary each one actually claims to cover.
- The benchmark must not smuggle Syke's preferred ontology into the task definition, scoring language, or required elements.
- Syke must face its own failure pressure: over-abstraction, stale memex confidence, wrong layer routing, synthesis laundering, controller complexity, and false cross-tool coherence.
- If a result only shows that Syke is better at reading artifacts Syke itself created, that result is worthless.

## operational vs stress distinction

- Every item must declare track, regime, and claim type before scoring.
- Operational items must show user-work reduction, not just elegant reconstruction.
- Stress items must be reported as structural pressure tests, not product proof.
- Hybrid items must satisfy both obligations or be downgraded.
- No report may mix operational wins and stress wins into one undifferentiated success story.
- If the benchmark cannot tell whether an item measures day-to-day value or extreme failure exposure, the item is underspecified and should not ship.

## regime balance

- Public claims require explicit coverage of `R0` local-memory control, `R1` fragmentation threshold, and `R2` multi-harness continuity.
- `R0` is mandatory. If native memory is not allowed to win where it should win, the benchmark is rigged.
- `R1` is mandatory. If the threshold where the object changes is not tested, the central thesis is unearned.
- `R2` is mandatory. If Syke's intended regime is not tested directly, the product claim is ungrounded.
- The benchmark must include both competitor failure modes and Syke failure modes in each regime where they are plausible.
- No public claim from an `R2`-heavy set without showing what happens in `R0` and `R1`.

## scoring discipline

- No single scalar headline. Reports must break out results by track, regime, claim type, slice, hard fails, efficiency, and practical gain.
- Hard fails are binding. Unsupported claims, stale-as-live errors, local-as-global errors, parity breaks, and undeclared extra evidence are not redeemable by nice prose.
- Quality, efficiency, and practical gain stay separate until inspection is complete.
- Pairwise architecture judgment is mandatory for Track C. "Looks better" is not a result.
- Hidden validation is required before any strong public architecture claim.
- If an item rewards benchmark-theater language over correct routing, freshness, and provenance, the rubric is bad and must be fixed before publication.

## anti-overclaim rules

- This benchmark may support bounded claims about this user, these slices, these regimes, and these architecture conditions. Nothing broader is automatic.
- We do not claim universal personal-memory laws from one operator.
- We do not claim final architectural victory from one prompt family, one bundle family, or one replay substrate.
- We do not claim product readiness from stress-only wins.
- We do not claim architecture superiority unless hidden holdouts preserve the same direction under parity.
- We do not claim Syke solves continuity if Syke's own failure gallery is thin, selective, or missing.
- When the evidence only shows "interesting signal," the public claim must say exactly that.

Until these constraints are met, external-facing benchmark language should be limited to: early benchmark design, internal comparison work, and provisional findings.
