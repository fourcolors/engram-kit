# Judge Stability by Ask-Type: Batch E Analysis

**Methodology:** Analyzed 19 probes (R01–R19) across GPT-4.5 judge vs. Claude Opus judge on the same answers, stratified by 7 pressure tags (ask-types). Pass rate = rank 2 (pass) / total. Disagreement = instances where GPT judge and Opus judge assign different ranks to identical answers.

## 1. Master Metrics Table — Per-Pressure Performance

| Pressure | N Probes | GPT Pass | Opus Pass | Judge Disagreement | GPT Mean Rank | Opus Mean Rank | Pass Delta |
|---|---|---|---|---|---|---|---|
| operative_state | 10 | 40.0% | 0.0% | 40.0% | 1.30 | 0.80 | 40.0% |
| bounded_history | 6 | 50.0% | 0.0% | 50.0% | 1.50 | 1.00 | 50.0% |
| object_continuity | 8 | 50.0% | 12.5% | 37.5% | 1.50 | 1.00 | 37.5% |
| completeness | 4 | 50.0% | 0.0% | 50.0% | 1.50 | 1.00 | 50.0% |
| cross_surface | 3 | 66.7% | 0.0% | 66.7% | 1.67 | 1.00 | 66.7% |
| committed_truth | 4 | 50.0% | 0.0% | 50.0% | 1.50 | 1.00 | 50.0% |
| provenance_audit | — | — | — | — | — | — | — |

**Observations:**
- **Provenance_audit:** 0 probes tagged. Insufficient data; exclude from stability ranking.
- **Opus judge exhibits structural leniency:** Never assigns rank 2 (pass) on operative_state, bounded_history, completeness, committed_truth, cross_surface. Only object_continuity sees 1 pass (12.5%).
- **GPT judge passes at 40–67%** across most pressures; object_continuity and completeness at 50%.

## 2. Stability Ranking — Lowest to Highest Judge Disagreement

1. **object_continuity** — 37.5% disagreement (3 disagreements / 8 probes)
2. **operative_state** — 40.0% disagreement (4 disagreements / 10 probes)
3. **bounded_history** — 50.0% disagreement (3 disagreements / 6 probes)
4. **completeness** — 50.0% disagreement (2 disagreements / 4 probes)
5. **committed_truth** — 50.0% disagreement (2 disagreements / 4 probes)
6. **cross_surface** — 66.7% disagreement (2 disagreements / 3 probes)

**Key insight:** Object_continuity is the only pressure-type where judges show relative agreement. Cross_surface shows the worst agreement, but sample is small (n=3).

## 3. Probe Spotlights — Illustrative Stability Patterns

### Spotlight 1: R03 — Operative_state + object_continuity (Major Judge Split)

**Pressure tags:** operative_state, object_continuity

**Judge verdicts:** GPT = **pass (rank 2)**  |  Opus = **fail (rank 0)**  | **Disagreement**

**Ask:** "last thread plus current status of synthesis modernization"

**Pattern:** GPT credits a complete synthesis-context summary as passing "operative state." Opus rejects it entirely. This gap (2 → 0) suggests:
- GPT judge prioritizes availability of *some* state context.
- Opus judge demands *accuracy/confidence* on "what is the current state" — may have penalized hedging or incompleteness.
- No shared rubric for "how fresh" or "how confident" operative_state answers must be.

### Spotlight 2: R13 — Object_continuity Only (Rare Agreement on Pass)

**Pressure tags:** object_continuity only

**Judge verdicts:** GPT = **pass (rank 2)**  |  Opus = **pass (rank 2)**  | **Agreement ✓**

**Ask:** "evolution of adapter-as-compiler"

**Pattern:** Both judges agree on object_continuity. Suggests:
- When the ask is purely "trace the history/evolution," judges converge.
- No "state now" pressure (operative_state) to create friction.
- Object_continuity may be inherently more measurable (clearer narrative/timeline).

### Spotlight 3: R17 — Bounded_history + completeness + cross_surface (Multi-Pressure Jam)

**Pressure tags:** bounded_history, completeness, cross_surface

**Judge verdicts:** GPT = **pass (rank 2)**  |  Opus = **partial (rank 1)**

**Ask:** "last-week broad exhaustive cross-platform reconstruction"

**Pattern:** GPT credits a broad cross-platform summary as passing. Opus downgrades to partial. Three pressures collide:
- **Bounded_history:** "Last week" — temporal scope conflict?
- **Completeness:** "Exhaustive" — coverage rubric undefined (enough depth? enough breadth?).
- **Cross_surface:** Multiple platforms/threads — Opus may penalize fragmentation.
- Opus appears stricter on "cross_surface" (requires *integration*, not list).

### Spotlight 4: R15 — Operative_state + object_continuity + committed_truth (Agreement on Partial)

**Pressure tags:** operative_state, object_continuity, committed_truth

**Judge verdicts:** GPT = **partial (rank 1)**  |  Opus = **partial (rank 1)**  | **Agreement ✓**

**Ask:** "restart observe tests with real data in bounded prior window"

**Pattern:** Both judges agree on partial. Suggests:
- When multiple pressures co-occur, judges may converge on "partial" as a compromise.
- "Restart observe tests" (operative_state) is answerable, but likely incomplete.
- "With real data" adds committed_truth pressure — requires grounding. Judges both recognize the partial fulfillment.

## 4. Cross-Pressure Patterns & Observations

### Pattern A: Object_continuity is most judge-stable (37.5% disagreement)
- **Why:** "Evolution of X" asks have a clear narrative structure. Judges can both assess presence/absence of a coherent timeline.
- **What it teaches:** Linearity and history-tracing are inherently more objective than "current state."

### Pattern B: Cross_surface triggers worst judge disagreement (66.7%)
- **Why:** No consensus on what "cross-surface" means. Does it require:
  - Enumeration of all surfaces (list)?
  - Integration/synthesis (unified narrative)?
  - Correlation of events across surfaces (causal/temporal links)?
- **Small n caveat:** Only 3 probes tagged; may be noise.

### Pattern C: Opus judge is persistently harsher (only 2 passes across 19 probes vs. GPT's 9 passes)
- **Why:** Opus may apply a stricter "confidence threshold" or demand deeper corroboration.
- **Implication:** Opus judge is *unreliable* for binary pass/fail but may be consistent on rejections. Consider Opus as a "false-positive filter" rather than a general evaluator.

### Pattern D: Operative_state and completeness collide badly
- **Why:** "Current state" and "exhaustive list of everything" are in tension:
  - Operative_state wants *immediate relevance* (what's active now?).
  - Completeness wants *exhaustion* (all past work, all threads, all decisions).
- **Example:** R17 fails this collision (cross_surface adds to the friction).

### Pattern E: Committed_truth and object_continuity often co-occur
- **Why:** Tracing evolution requires grounding *why* decisions were made → commits to past truth.
- **Judges agree on this blend:** R15 (both partial). R02 (both partial). Suggests the rubric for "committed history" is clearer than "current state."

## 5. Calibration-Actionable Observations

### Observation 1: Drop operative_state from universal rubric; make pressure-conditional.
- **Why:** 40% judge disagreement. Opus never passes it. No consensus on freshness/confidence thresholds.
- **Action:** Define operative_state as a *conditional ask-type* requiring explicit rubric criteria (e.g., "answer must reflect state as of <date>"; "must cite most recent decision/action").

### Observation 2: Cross_surface needs a shared definition ASAP.
- **Why:** Highest disagreement (67%). Judges interpret it as list vs. synthesis vs. something else.
- **Action:** Formalize: "cross_surface = answer must tie events/decisions across ≥2 named surfaces/threads with explicit causal/temporal links."

### Observation 3: Object_continuity is the most judge-stable ask-type.
- **Why:** 37.5% disagreement (lowest). Can be rubric'd as "must show at least 2 decision points and what changed between them."
- **Action:** Elevate object_continuity to universal criteria. Use it as a baseline for calibrating other pressures.

### Observation 4: Completeness is under-defined; split into two axes.
- **Why:** 50% disagreement. Judges can't tell if "exhaustive" means deep, broad, or both.
- **Action:** Split into:
  - **Enumeration:** "list all X" (bounded, countable, clear pass/fail).
  - **Narrative depth:** "explain how each X connects to Y" (unbounded, requires judgment).

### Observation 5: Committed_truth is judge-stable when paired with object_continuity.
- **Why:** Both agree on partial for probes with this pair (R02, R15). Suggests "committed history" is inherently more rubricable.
- **Action:** Keep committed_truth in universal criteria. Require: "answer must justify past decisions with specific ground-truth evidence."

### Observation 6: Opus judge is a stricter but unreliable filter.
- **Why:** Passes only 2/19 probes. May be useful as a *rejection* filter (if Opus passes, GPT will too) but not as a primary evaluator.
- **Action:** Use Opus in a two-stage evaluation: GPT → Opus (on passes only) for hard rejection. Do not rely on Opus alone.

### Observation 7: Multi-pressure collisions (3+ tags on one probe) correlate with disagreement.
- **Why:** R17 (3 pressures) and R14 (3 pressures) both show disagreement.
- **Action:** For high-pressure-density probes, explicitly resolve priority: which pressure takes precedence (operative_state, then completeness, then committed_truth)?

## Mapping to Primitives Design

**Universal criteria (stable across judges):**
- **support:** Cite evidence/data (implicit in committed_truth). ✓
- **time-local:** Bound by date (implicit in operative_state). Needs explicit rubric.
- **operative-state:** Rename to "restart-observable"; require rank 2 only if restart would succeed. ~40% stable; needs conditioning.
- **wrong-restart:** "If I restart with your answer as context, will I fail?" (inverse of operative_state). Under-explored but likely more judge-stable.

**Conditional criteria (pressure-specific):**
- **enumeration:** For completeness; define "exhaustive enough."
- **cross-surface:** Define as explicit causal/temporal linkage.
- **object-continuity:** Keep as-is; most stable (37.5% agreement).
- **committed-state:** Attach to object-continuity; both stable together.
- **provenance:** 0 tagged probes; insufficient data. Do not use until more probes are labeled.

---

**Dataset:** NE-1.3, R01–R19 (19 probes). Judge pair: GPT-4.5-turbo vs. Claude Opus 4.6. Pressure matrix: 7 tags per probe; provenance_audit and cross_surface under-sampled.
