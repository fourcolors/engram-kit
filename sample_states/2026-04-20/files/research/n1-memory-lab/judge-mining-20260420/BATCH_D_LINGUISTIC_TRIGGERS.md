# BATCH D: LINGUISTIC TRIGGERS IN JUDGE REASONING
**Judge-Calibration Mining Pass | 72-sample stratified corpus | April 20, 2026**

---

## 1. GPT-JUDGE PHRASEBOOK

### Top Recurring Phrase Patterns (Partial/Missed Verdicts)

**Pattern 1: "overreaches with unsupported claims" (4 occurrences)**
- **Interpretation:** Judge penalizes answers that extend beyond evidence bounds without hedging.
- **Direct quotes:**
  - "It overreaches into claims about empty memory/session state and no harness traces, which are not bounded by the evidence..." [R08 pure factual_grounding]
  - "It presents unsupported specifics with high confidence and no caveats, rather than qualifying them as tentative or inferred..." [R12 production factual_grounding]

**Pattern 2: "invents artifacts not in evidence" (2 occurrences)**
- **Interpretation:** Judge catches hallucinated details: specific paths, UUIDs, commands, config states not present in the slice.
- **Direct quotes:**
  - "The answer instead invents an exact pytest command and claims durable persistence without evidence." [R15 production coherence]
  - "Uses UUIDs for thread routing that don't exist in any artifact." [R09 production coherence]

**Pattern 3: "contradictions unresolved" (1 occurrence)**
- **Interpretation:** Judge flagsPR internal logical inconsistencies or conflicting claims within the answer itself.
- **Direct quote:**
  - "It fails to resolve contradictions between earlier Phase 2 planning, later phase-complete notes, and the thread spiral; instead it states one side as if current without reconciling..." [R12 production coherence]

**Pattern 4: "privileged one surface over another" (1 occurrence)**
- **Interpretation:** Answer overweights git/commit data vs. slice session evidence or vice versa; incomplete multi-surface synthesis.
- **Direct quote:**
  - "It privileges the git/commit surface and earlier traces over later slice evidence from the same day, so the world model is incomplete..." [R03 pure coherence]

**Pattern 5: "does not address contradictions" (1 occurrence)**
- **Interpretation:** Answer sidesteps or ignores conflicting facts in the evidence without reconciliation attempt.
- **Direct quote:**
  - "It does not address or resolve the contradiction between the claimed blank slate and the concrete repo state shown by `git status`." [R08 pure coherence]

**Pattern 6: "high confidence without caveats" (1 occurrence)**
- **Interpretation:** Tone/calibration issue: answer sounds certain despite limited or conflicting evidence.
- **Direct quote:**
  - "The answer presents exact times and statuses confidently, without caveating that later active threads existed by cutoff..." [R03 pure factual_grounding]

---

## 2. OPUS-JUDGE PHRASEBOOK

### Top Recurring Phrase Patterns (Partial/Missed Verdicts)

**Pattern 1: "directly contradicted by slice data" (2 occurrences)**
- **Interpretation:** Core claim provably false against available evidence; not a marginal dispute.
- **Direct quotes:**
  - "The answer's central claim ('no record exists') is directly contradicted by the slice data. Multiple sessions contain detailed memorix architecture..." [R10 zero factual_grounding]
  - "The core claim (LM Studio/Qwen benchmarking was most recent) is contradicted by both the git anchor and session timestamps." [R19 production factual_grounding]

**Pattern 2: "does not integrate across data surfaces" (1 occurrence)**
- **Interpretation:** Misses cross-cutting evidence synthesis; treats independent data streams as isolated.
- **Direct quote:**
  - "The answer is internally consistent and doesn't contradict itself. However, it doesn't meaningfully integrate across the available data surfaces (JSONL sessions, git history, adapters) to build a coherent world model..." [R08 zero coherence]

**Pattern 3: "internally consistent but incomplete" (1 occurrence)**
- **Interpretation:** No internal logical flaws, but shallow coverage; doesn't exploit available evidence.
- **Direct quote:**
  - "Only claude-code harness data was available. The answer uses session transcripts and project data but fails to reconcile session-time git state with actual final git state." [R03 zero coherence]

**Pattern 4: "cross-harness picture is speculative" (1 occurrence)**
- **Interpretation:** Answer ventures claims about unmeasured/unseen systems; lacks grounding for cross-system claims.
- **Direct quote:**
  - "The PiAdapter claim contradicts the git reality, and the TOML descriptor claim contradicts the stub-removal commit. The cross-harness picture is somewhat speculative for adapters beyond the confirmed 5." [R11 zero coherence]

**Pattern 5: "fails to reconcile temporal state" (1 occurrence)**
- **Interpretation:** Conflates or mixes observations from different time windows without marking transition or stale data.
- **Direct quote:**
  - "The slice contains data from claude-code (2990 files) and opencode (2 files). The answer doesn't reference or attempt to braid across any harness sources." [R07 zero coherence]

**Pattern 6: "does not reference available sources" (1 occurrence)**
- **Interpretation:** Available artifacts (git, trace logs, config files) left unrouted or unmentioned.
- **Direct quote:**
  - "The answer correctly identifies adapters/ and syke.db exist but fails to route any transcript or git artifacts into the response." [R01 zero coherence]

---

## 3. SHARED VOCABULARY

Both judges frequently use:
- **"contradiction"** / **"contradicts"** – core disagreement with evidence (GPT: 6x, Opus: 5x across samples)
- **"does not"** / **"fails to"** framing – structure for identifying missed content or logic
- **Specificity complaints** – exact paths, UUIDs, times cited without support
- **Surface/evidence** terminology – "slice data," "anchor," "harness traces," "artifacts"

**Interpretation:** Both judges care about **factual grounding** and **internal coherence** but use slightly different entry points to the same problem.

---

## 4. DIVERGENT VOCABULARY

| Judge | Characteristic Phrase | Count | Interpretation |
|-------|-----|------|---|
| **GPT** | "overreaches" | 4x | Violation of evidence boundary; scope expansion |
| **GPT** | "invents" / "exact...without evidence" | 2x | Hallucination framing; specific factual error |
| **GPT** | "privilege/prioritize [surface]" | 1x | Multi-source weighting problems |
| **Opus** | "directly contradicted" | 2x | Binary falsity; not negotiable |
| **Opus** | "does not integrate across" | 1x | Systems-thinking penalty; missing synthesis |
| **Opus** | "speculative" (for cross-harness) | 1x | Unvalidated inference; caution about unmeasured systems |

**Interpretation:**
- **GPT uses a **boundary violation** vocabulary: answers that creep beyond what evidence supports.**
- **Opus uses a **logical contradiction** vocabulary: answers that make provably false claims.**
- **GPT penalizes breadth overflow; Opus penalizes depth insufficiency.**

---

## 5. CALIBRATION-ACTIONABLE OBSERVATIONS

### Observation 1: "Overreach" vs. "Contradiction" — Different Thresholds, Same Penalty
**Phrases:** GPT "overreaches...unsupported" (4x) vs. Opus "directly contradicted" (2x)  
**Rubric Decision:** Define a spectrum: *unsupported claim*, *underspecified claim*, *false claim*, *resolved contradiction*. Next rubric should distinguish: (a) claims beyond bounded evidence (Opus allows more here), (b) claims that contradict anchor facts (both judges penalize). Set explicit thresholds per axis.

### Observation 2: "Invents" is Factual Hallucination; GPT Flags It More
**Phrases:** GPT "invents artifacts" (2x) — specific pytest commands, UUIDs, paths without source.  
**Rubric Decision:** Add explicit hallucination-detection sub-criterion under *factual_grounding*: *Does the answer introduce specific named entities (paths, IDs, commands) not present in the evidence slice?* This catches a class of error GPT marks consistently; Opus does not highlight explicitly.

### Observation 3: Multi-Surface Synthesis is Under-specified in Current Rubrics
**Phrases:** Opus "does not integrate across" (1x), GPT "privileged one surface" (1x)  
**Rubric Decision:** *Coherence* axis should explicitly name: *Does the answer draw from multiple available data surfaces (git, traces, config, transcripts) or rely narrowly on one?* Both judges penalize narrow synthesis; the current rubric doesn't make this a first-class criterion.

### Observation 4: Confidence Calibration Appears Only in GPT Reasoning
**Phrases:** GPT "sounds confident," "without caveats" (1x); Opus never mentions tone/confidence.  
**Rubric Decision:** Confidence calibration may be GPT-specific bias (likelihood overweight confidence signals) rather than answer property. If rubric wants to evaluate *uncertainty marking*, require both judges to score it; otherwise move it to meta-review feedback, not primary verdict.

### Observation 5: Temporal Coherence is Implicit in Both, but Opus Names It
**Phrases:** Opus "reconcile temporal state," "stale/irrelevant" (2x); GPT "later...earlier...thread spiral" without naming time confusion as distinct error.  
**Rubric Decision:** Promote temporal threading to explicit sub-criterion under *continuity*: *Does the answer distinguish and mark events from different time windows?* Opus already detects this; making it explicit in the rubric will help GPT calibrate.

### Observation 6: "Speculative" is Opus's Caution About Unmeasured Systems
**Phrases:** Opus "cross-harness picture is speculative" (1x) — adapters beyond confirmed set, claims about unobserved tools.  
**Rubric Decision:** This is a **risk aversion** signal specific to multi-system inference. Rubric should decide: Are speculative claims about unobserved but plausible systems acceptable if marked, or out-of-scope? Opus treats them as penalty-worthy; GPT tolerates them if bounded. Set a policy.

---

## 6. METHODOLOGY NOTES

- **Corpus:** 72 stratified samples (36 per judge, 3 per judge-verdict-axis combo)
- **Source files:** 4 benchmark results (2 GPT-judge, 2 Opus-judge runs)
- **Extraction:** 2098 partial/missed/fail verdicts across 3375 total judge reasoning texts
- **Phrase identification:** Semantic clustering via regex + manual validation on full reasoning quotes
- **Attribution:** Every phrase includes [probe_id condition axis] for reproducibility

---

**END BATCH D REPORT**
