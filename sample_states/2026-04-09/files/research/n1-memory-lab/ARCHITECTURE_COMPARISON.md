# ARCHITECTURE_COMPARISON

This lab compares memory systems by the object they stabilize, the scope they assume, and the practical value they unlock on the same evidence.

## Comparison frame

The question is not "which memory system has more features?"

The question is:
- what object does the system believe it is maintaining?
- what boundary does it treat as local vs external?
- what continuity failures still leak through?
- what practical day-to-day value becomes possible?

## Main architecture families

| Family | Primary object | Typical scope | Strengths | Common failure boundary |
|---|---|---|---|---|
| Native harness memory | local session/project/user memo | one harness/runtime | fast local continuity, minimal setup, native UX | cross-tool fragmentation, weak external continuity, poor portability |
| Hermes/provider/plugin memory | provider-defined retrieved state and injected context | one harness with pluggable external provider | standardized integration points, retrieval/profile/graph options, flexible provider layer | still assumes provider-shaped memory objects and harness-local control plane |
| Syke/federated continuity | cross-harness continuity state and routed memory surfaces | many harnesses, sessions, and traces | survives tool switches, supports distribution/routing, treats memory as a continuity substrate | harder systems problem, risk of over-abstraction, requires explicit controller discipline |

## Native harness memory

Native memory is the default baseline because it is what users actually have first.

Typical properties:
- scoped to one runtime or harness
- optimized for quick local carryover
- often file-backed, session-backed, or simple preference-backed
- strong when the task stays inside that harness

What it does well:
- local continuation
- small preference persistence
- low-friction setup
- native UX alignment

Where it breaks for the `n=1` object:
- the user moves across tools, not just sessions
- the same project may be interpreted differently by different harnesses
- contracts, reversals, and latent constraints do not stay aligned across boundaries
- local summaries often become stale because they are not a cross-harness control surface

This is why the useful comparison is not "native memory bad, external memory good."
It is:
- native alone
- native plus a stronger continuity layer

## Hermes / provider / plugin memory

Hermes-style provider memory is the strongest current steelman of a pluggable memory stack.

Typical properties:
- one harness remains the control plane
- external providers standardize retrieval/injection hooks
- providers may optimize for profiles, graphs, retrieval, or summarization
- memory is often injected before/after turns or sessions

What it does well:
- structured provider ecosystem
- better retrieval and profile formation than purely local notes
- explicit extension points
- faster experimentation across memory backends

Where it still falls short for this lab:
- the harness still owns the primary scope boundary
- the memory object is often provider-shaped before it is person-shaped
- cross-tool identity continuity is secondary rather than primary
- the architecture is still largely retrieval/injection centric

This family matters because it is the best current competitor class, not because it is the final answer.

## Syke / federated continuity

This lab should treat Syke not as "one more memory plugin" but as a candidate federated continuity/control plane.

Candidate object:
- the routed continuity state of one changing user across tools, sessions, and agent surfaces

Candidate strengths:
- cross-harness continuity
- routed memex surfaces instead of one local summary
- better support for resumption, dot-connection, and contract preservation
- ability to treat memory as observe + synthesize + distribute rather than only store + retrieve

Candidate risk areas:
- more moving parts
- possible overreach into premature ontology/architecture claims
- controller/runtime complexity
- danger of becoming too abstract without strong slice/probe evidence

## What the lab needs to decide

This comparison is not here to crown a winner immediately.

The lab should use it to answer:
1. which object each architecture actually stabilizes
2. which failures remain unsolved for each family
3. what practical-value surfaces each family unlocks
4. whether "continuity layer" or "control plane" is the right framing for Syke

## Working hypothesis

For now, the best working hypothesis is:
- native harness memory is useful but locally scoped
- Hermes/provider memory broadens retrieval and injection but still centers harness-local control
- Syke is most interesting when treated as a federated continuity/control plane layered on top of native memory, not as a replacement for it

That is still a hypothesis. The lab exists to pressure-test it.
