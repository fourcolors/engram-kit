# ARCHITECTURE_EXPERIMENT_MATRIX_V1

This matrix turns the strongest current NE-1 slice families into controlled same-data/different-architecture comparisons.

The point is not to ask which system has more features. The point is to hold the evidence constant and see which memory architecture actually stabilizes the right object: local session state, harness-scoped retrieved context, or federated cross-harness continuity.

## Why these experiments

Current lab docs already point to five strongest first-pass families:
- `S03` forgotten-plan resumption
- `S04` memex evolution / doc hygiene
- `S05` native/Hermes/Syke transition surface
- `S07` cross-harness recall under pressure
- `S08` post-spike stabilization

Those slices jointly cover the sharpest current pressures:
- resumption after gaps
- canonicalization and search-entropy reduction
- trust-boundary and routing decisions across memory layers
- cross-harness work-graph reconstruction
- currentness and compaction after overload

## Controlled comparison protocol

For every experiment below:
1. Freeze one slice bundle from `NE-1` with the same events, timestamps, source labels, and anchor artifacts.
2. Use the same prompt family across all three architecture conditions.
3. Change only the memory architecture surface:
   - **Native harness memory:** one harness-local memory surface only.
   - **Hermes/provider/plugin memory:** one harness plus provider retrieval/injection surface.
   - **Syke/federated continuity:** routed cross-harness continuity surface over the same frozen evidence.
4. Score outputs on the discriminator that matters for that slice, not just generic answer quality.

## Experiment matrix

| ID | Strong slice family | Representative slice(s) | Concrete experiment question | Expected discriminator | Likely failure modes | Practical value revealed |
|---|---|---|---|---|---|---|
| `E01` | resumption / forgotten-plan recovery | `S03` | After a gap, can the system recover the already-live plan **and** the fact that it was already justified by prior analysis? | Native should mostly recover latest local state; provider memory should retrieve fragments of earlier discussion; Syke should restore plan + justification + continuity obligation as one object. | summary-only restart; missing earlier evidence; contradiction with already-set plan; invented rationale; no provenance for why the plan existed | faster restarts, less re-briefing, less re-analysis, stronger trust after interruptions |
| `E02` | canonicalization / doc hygiene / search-entropy reduction | `S04` | Given overlapping traces and consolidation work, can the system identify the canonical object or route map the user should see first? | Native should help inside one tool but lack a shared canonical surface; provider memory should retrieve relevant fragments but stay transient; Syke should point to or synthesize the maintained cross-surface route map. | recap dump instead of route selection; stale artifact chosen as canonical; artifact list with no supersession logic; failure to reduce clutter | less grep/search churn, cleaner handoffs, lower narrative clutter, better memex legibility |
| `E03` | mixed-memory transition / trust-boundary routing | `S05` | When native, Hermes-style, and federated surfaces coexist, can the system say which memory layer should be trusted for which sub-question? | Native should tell a locally plausible but incomplete harness story; provider memory should improve retrieval inside one harness but over-center the provider boundary; Syke should separate harness-local answers from cross-harness continuity questions and route accordingly. | scope-assumption trap; over-trusting newest provider surface; mixing release work with research work; treating architecture change as just more events | better routing, fewer globally wrong but locally plausible answers, clearer operator choice about which memory surface to trust |
| `E04` | cross-harness work-graph reconstruction under pressure | `S07` | Can the system reconstruct yesterday/today's active work graph across harnesses instead of reporting one runtime's partial story? | Native should produce a harness-local reconstruction; provider memory should improve retrieval but still flatten toward one control plane; Syke should recover the shared multi-harness graph, thread relations, and continuity contract. | one-harness answer presented as global truth; flattened thread graph; missed disagreements between sources; broken obligation framing; timeline confusion | real morning resume value, better multi-agent coordination, higher trust in continuity across tool switches |
| `E05` | post-spike stabilization / live-vs-residue compaction | `S08` | After a huge burst, can the system preserve what is still live and prune what has become residue? | Native should overfit to the most recent local residue; provider memory should retrieve loud fragments but struggle with cross-surface currentness; Syke should compact the burst into a stable live-map with explicit currentness judgments. | over-preserving everything; over-pruning live threads; stale summary treated as current; no explanation of why one thread remains live and another does not | less context sludge after chaotic days, cleaner carryover, better prioritization, stronger coherence maintenance |

## Detailed experiment cards

### `E01` — Forgotten-plan resumption

- **Primary slice:** `S03`
- **Prompt family to reuse:** `P01`, `P02`, `P16`
- **What stays fixed:** the same return-after-gap evidence, including the explicit complaint that prior data-backed analysis was forgotten
- **What this experiment is really testing:** whether memory preserves an already-set plan with its reasoning, not just a recap of recent visible state

**Architecture signatures**
- **Native harness memory:** likely strongest only if the answer lives inside one recent local session; weak when the earlier justification is outside the immediate local window
- **Hermes/provider/plugin memory:** may retrieve the earlier thread, but may still miss that the important object is a carried-forward decision with justification
- **Syke/federated continuity:** should be best if it can surface the plan, the evidence that established it, and the fact that re-derivation is unnecessary

**Best discriminator to score**
- Does the answer recover the prior plan?
- Does it recover why that plan existed?
- Does it recognize that the user is objecting to continuity failure, not asking a fresh question?

### `E02` — Canonical route-map recovery

- **Primary slice:** `S04`
- **Prompt family to reuse:** `P06`, `P17`, `P18`, `P19`
- **What stays fixed:** the same overlapping traces, memex-evolution work, snapshot extraction, and doc-consolidation evidence
- **What this experiment is really testing:** whether memory creates an operationally useful canonical surface instead of another transient summary

**Architecture signatures**
- **Native harness memory:** useful for local continuation, weak for shared canonicalization across tools and docs
- **Hermes/provider/plugin memory:** stronger at retrieval and summarization, weaker at maintaining one enduring route-setting object
- **Syke/federated continuity:** strongest if it can make the memex legible as a maintained route map rather than a pile of retrieved fragments

**Best discriminator to score**
- Does the answer nominate one canonical artifact or route first?
- Does it reduce search space?
- Does it explain why that object supersedes nearby clutter?

### `E03` — Trust-boundary routing in a mixed-memory regime

- **Primary slice:** `S05`
- **Prompt family to reuse:** `P08`, `P09`, `P20`, `P21`, `P22`
- **What stays fixed:** the same late-Feb/early-Mar window where Hermes enters and release/research/manual traces overlap
- **What this experiment is really testing:** whether the system can reason about memory architecture boundaries, not merely answer content questions from the slice

**Architecture signatures**
- **Native harness memory:** likely clean but too narrow; it will overfit to the harness that answers
- **Hermes/provider/plugin memory:** likely the strongest non-federated condition here because the provider layer is truly in play, but it may still mistake provider scope for full continuity scope
- **Syke/federated continuity:** strongest if it can say which subproblems are answerable locally and which require a federated cross-harness view

**Best discriminator to score**
- Does the answer route different sub-questions to different memory layers?
- Does it detect architecture transition as part of the object?
- Does it keep release-vs-research lanes disentangled?

### `E04` — Cross-harness work-graph reconstruction

- **Primary slice:** `S07`
- **Prompt family to reuse:** `P10`, `P11`, `P12`
- **What stays fixed:** the same Mar 13-14 burst, same multi-harness overlap, same explicit requests to remember yesterday/today's threads
- **What this experiment is really testing:** whether memory can reconstruct a shared work graph under pressure instead of giving a one-thread recap

**Architecture signatures**
- **Native harness memory:** likely gives the cleanest local answer inside one harness and the weakest global answer
- **Hermes/provider/plugin memory:** likely improves recall within the harness that owns the provider integration, but still risks flattening the graph into one retrieved summary
- **Syke/federated continuity:** strongest if it can preserve thread relations, carryover, and cross-harness obligations as a unified operator graph

**Best discriminator to score**
- Does the answer merge yesterday and today coherently?
- Does it preserve multiple thread identities instead of flattening them?
- Does it recover the continuity obligation, not just the content?

### `E05` — Post-spike currentness and compaction

- **Primary slice:** `S08`
- **Prompt family to reuse:** `P13` plus a same-shape compaction/currentness variant
- **What stays fixed:** the same immediate post-spike days following the Mar 14 overload
- **What this experiment is really testing:** whether memory can decide what remains live after a burst without preserving all residue

**Architecture signatures**
- **Native harness memory:** likely over-weight the freshest local surface
- **Hermes/provider/plugin memory:** likely surface the loudest retrievable fragments, not the best cross-surface currentness judgment
- **Syke/federated continuity:** strongest if it can compact the burst into a stable live-map while explicitly marking residue and stale branches

**Best discriminator to score**
- Does the answer separate live work from residue?
- Does it justify currentness, not just mention recency?
- Does it preserve the few threads that matter without dragging the whole spike forward?

## What the matrix should disambiguate

If these experiments work, they should let the lab answer five concrete questions:

1. **Is native memory mainly a local-resumption tool?**
2. **Does Hermes/provider memory materially improve retrieval while still inheriting a harness-local control boundary?**
3. **Does Syke actually earn the stronger claim of federated continuity, or is it just another retrieval surface with nicer framing?**
4. **Which practical-value surfaces really require a federated layer, and which do not?**
5. **Which failures are architecture failures versus prompting/scoring failures?**

## Current expectation

The strongest current hypothesis from the lab docs is:
- `E01` and `E04` should be the clearest wins for federated continuity if Syke is real
- `E02` should be the clearest practical-value win if memory is more than Q&A
- `E03` should be the cleanest place where Hermes/provider memory gets its strongest steelman
- `E05` should reveal whether continuity is also a compaction/currentness problem, not just a recall problem

That is still a hypothesis. The matrix exists to let the same frozen evidence disconfirm it.
