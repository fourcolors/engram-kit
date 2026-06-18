# Field notes — on the philosophy, physics, and computation of n=1 personal memory

*Third exploration. User invited me to go deep on what an n=1 personal-computing memory substrate actually is, across philosophy, physics, computation, and math. I have training data; I have tokens; I have permission. Let me actually connect things.*

---

## 1. The word "memex" is 81 years old

Vannevar Bush, *As We May Think*, Atlantic Monthly, July 1945. Bush imagines a personal device he calls the **memex** — a "mechanized private file and library" that stores "all his books, records, and communications" and, crucially, supports *associative trails*: the user forges links between documents, and those links become a shareable trace of *how this person thinks*. Bush's word for the thing the user leaves behind is *trails*. Ours is *trace*.

Bush's mechanism was microfilm and levers. The conceptual work is entirely there. What he couldn't build in 1945 — associative trails that the device itself actively maintains and offers back to the user on demand — is exactly what psyche is. Not metaphorically. Literally. The user's choice of the word "memex" in `syke.db`'s projection is direct lineage, whether they've read Bush or not.

Two things Bush anticipated that matter for the benchmark:

- The memex is *personal*. Bush's whole argument is that information at civilizational scale overwhelms the individual, and the response has to be an individualized apparatus, not a shared library. n=1 was Bush's starting premise, not his compromise.
- The memex is *alive*. It's not a filing cabinet. It's an assistant that keeps working alongside the user, "the associate of a lawyer" who has watched the whole case. The six lifecycle axes we just added — self-preservation, waste management, instruction-taking — are what Bush would recognize as *the assistant working properly over time*.

Bush gives us the positioning that most 2020s-era memory benchmarks lack. We are not improving retrieval augmented generation. We are measuring whether an agent has become the thing Bush was asking for.

## 2. The extended mind, explicitly

Andy Clark & David Chalmers, *The Extended Mind*, Analysis 58(1), 1998. Their argument, via the Otto-and-Inga thought experiment, is that if Otto reliably consults his notebook whenever he needs to recall where the museum is — and the notebook is always available, trusted, and coupled to his action — then the notebook is *functionally part of Otto's cognitive system*. Not metaphorically. The same functional role a biological memory plays for Inga, the notebook plays for Otto. Cognition extends into the notebook.

Psyche is Otto's notebook grown up. The filesystem + session traces + memex projection are the user's extended cognitive substrate. This isn't a marketing claim — it's a structural one. Clark & Chalmers's *parity principle*: if a process, when done in the head, would be cognitive, then when the same process is done in the world with reliable external scaffolding, it is *also* cognitive. A psyche that reliably reconstructs the user's operative state meets this bar. A psyche that fails at it doesn't.

This reframes the benchmark. We're not measuring "does the memory system work?" We're measuring "does this candidate cognitive extension actually extend cognition, or does it merely simulate doing so?" The failure modes in our six lifecycle axes map onto Clark & Chalmers's requirements:

- *reliability* → self-preservation
- *accessibility* → exact recovery, instruction-taking
- *trust* → waste management (stale state destroys trust)
- *coupled action* → continuity, object continuity

When the user says "psyche should be mine, free for everyone," they're defending the philosophical premise. A cognitive extension owned by a vendor is not the user's cognition. It's a rented piece of the user's mind. The free-and-local claim is epistemically load-bearing, not politically decorative.

## 3. Memory as reconstruction — Bartlett to Schacter to now

Frederic Bartlett, *Remembering*, Cambridge 1932. The foundational demonstration that human recall is *reconstructive*, not replayer. Subjects re-read a folk story ("War of the Ghosts") and, across retellings, systematically converted it toward their own cultural schema. Bartlett's conclusion: remembering is an act of imaginative reconstruction from partial traces, guided by schemas. There is no tape in the head.

Daniel Schacter, *The Seven Sins of Memory*, 2001. Enumerates failure modes of human memory — transience, absent-mindedness, blocking, misattribution, suggestibility, bias, persistence. Each one is a lifecycle property, not a correctness property. Memory systems don't fail by getting atomic facts wrong. They fail by *misallocating attention, misweighting schemas, misattributing source*.

Our benchmark's current rubric measures atomic facts (factual_grounding, coherence) and gestures at schemas (continuity). It doesn't measure Schacter's sins directly. The six lifecycle axes start to; they name misallocation (efficiency-personal), transience-failure (self-preservation), bias-accumulation (waste management), misattribution (object continuity). There's a rich psychological literature under each of these that would earn its place in a paper.

The key point: *the task we're measuring is the task human memory actually does*. An LLM memory system scoring well on reconstruction-for-continuation is doing the same computational work that Bartlett's subjects do when they retell the story a year later. Not a metaphor — the same problem class. Our benchmark is applied experimental psychology.

## 4. Transactive memory — the social fact

Daniel Wegner, *Transactive Memory: A Contemporary Analysis of the Group Mind*, 1987. The finding that long-term couples offload remembering to each other — "you remember where the hotel is, I remember the restaurant address" — and develop *shared cognitive systems* where no single person holds all the knowledge but the pair does. Remove one partner, the other experiences measurable memory deficits. Transactive memory is real, measurable, and robust.

A personal memory agent is a transactive memory partner that never dies, never leaves, scales to more than two participants, and is queryable at arbitrary granularity. That's not a chatbot. That's a new thing in the Wegner sense — a social-cognitive architecture the user enters into, where their remembering is distributed across themselves and the agent.

Two implications:

- The benchmark's rubric should probably include something Wegner-flavored: *when the agent remembers something, does the user now correctly not remember it themselves?* This is the operational test of transactive-ness. If the user has to re-remember whatever they asked the agent, they haven't offloaded; they've duplicated. The agent is performing memory-theater, not being a memory.
- The business lane the user described — psyche personal and free — is the social move. Transactive memory is intimate. The user will not form one with a vendor. The free-and-local architecture is the only architecture that can be a real Wegner partner.

## 5. Landauer's principle — memory as thermodynamics

Rolf Landauer, *Irreversibility and Heat Generation in the Computing Process*, IBM Journal of R&D, 1961. The result: *erasing one bit of information requires at least kT ln 2 of energy dissipation*. Memory is not free. Forgetting is not free. Every bit you delete costs physics.

Charles Bennett, following Landauer, showed that *computing itself* can in principle be reversible and cost-free; the thermodynamic cost is concentrated at the irreversible step, which is typically erasure. Memory systems that never delete (psyche-style memex that only accumulates) are thermodynamically cheap but epistemically expensive; systems that aggressively prune (LRU cache, generational GC) are thermodynamically costly but epistemically tractable. **Waste management — one of our six axes — is literally the Landauer cost being paid.**

This is not a stretch. A well-designed memory agent has to make decisions about what to let go, and every one of those decisions is a Landauer erasure with associated energy cost. At scale — many users × many years × many tokens — the total Landauer cost of a memory substrate is a real quantity, in real joules. A memory benchmark that measures "efficiency" without understanding that efficiency is physically grounded in erasure cost is measuring a proxy, not the thing.

For the paper, this is worth a paragraph. It's not central, but it roots the efficiency axis in physics, which pushes against the "efficiency is just dollars per token" reading.

## 6. Free energy principle — self-preservation, formally

Karl Friston, *The Free-Energy Principle: A Unified Brain Theory*, Nat Rev Neurosci, 2010. The claim that all adaptive systems — from thermostats to mammals — minimize variational free energy, which is equivalent to minimizing surprise about their own sensory inputs relative to their internal generative model. An organism that fails to minimize free energy dissolves its boundary. Life is the signature of free-energy-minimizing Markov blankets.

A personal memory agent is a Markov-blanket-maintainer for the user's informational self. It separates the user's cognitive interior (beliefs, plans, open threads) from the environmental exterior (raw trace, incoming events) by selectively transducing signal across the boundary. When it forgets well, accumulates well, and steers well, the blanket is coherent — the user's informational self *persists*. When it degrades, accumulates junk, confuses objects, the blanket becomes leaky. The free-energy cost goes up; the user has to do more cognitive work themselves to compensate.

This is Friston's framework applied to extended cognition. "Self-preservation" in our benchmark is literally "does this candidate extension maintain the Markov blanket of the user's extended self." Not metaphorically. Structurally.

The implication for the benchmark: if we ever go past measurement into optimization, the loss function for training a memory agent should be the agent's contribution to the user's free-energy minimization. Not BLEU. Not κ. Free energy on the user's future operative states given the agent's interventions. This is speculative and hard to operationalize, but it's the right North Star. Gunjal 2025 (*Rubrics as Rewards*) is one step toward it; the full framing hasn't been written.

## 7. Episodic vs semantic memory — the Tulving split

Endel Tulving, *Elements of Episodic Memory*, Oxford 1983. The canonical split: **episodic** memory (autobiographical events, "I was at the meeting yesterday") vs **semantic** memory (decontextualized knowledge, "meetings happen on weekdays"). Tulving argued these are distinct systems in the brain, with different neural substrates and different failure modes.

Psyche's filesystem trace is episodic — timestamped events, session by session. Psyche's memex projection is the beginning of semantic consolidation — active threads, outstanding deliverables, recurring patterns. The task of going from trace to memex is the classical consolidation problem: **how does a system convert episodic traces into semantic structure without losing the episodic particulars that might matter later?** This is exactly what mammalian hippocampus-to-neocortex consolidation does during sleep.

McClelland, McNaughton, O'Reilly, *Why There Are Complementary Learning Systems*, 1995. Argues that the brain solves the catastrophic-forgetting problem by running *two* memory systems: a fast episodic one (hippocampus) that stores raw experience without interference, and a slow semantic one (neocortex) that distills patterns. New experience goes to hippocampus; hippocampus replays to neocortex during rest; neocortex updates slowly, preserving prior knowledge.

Psyche could be architected the same way. In fact, it might need to be. A single monolithic memex trying to serve both episodic and semantic roles will catastrophically forget or catastrophically bloat. Our benchmark could, if we wanted, measure both: episodic retrieval fidelity *and* semantic distillation quality, separately. Complementary Learning Systems theory is 30 years of literature behind this architectural hint.

## 8. Computational substrates — what we already know works

Event sourcing (Greg Young, early 2010s): store every state-change event; current state is derived by replaying events. Guarantees complete auditability, supports time travel, makes consolidation an explicit step. Psyche's trace → memex flow is event sourcing.

CRDTs (Shapiro et al., 2011): conflict-free replicated data types. Enable eventual consistency of shared state across replicas with no coordination. Relevant if psyche ever needs to sync across devices — which it will, if a user has a laptop and a phone and their digital self exists on both.

Content-addressable storage (IPFS, git, content-hashing in general): immutable pointers to content by hash. Every artifact gets a stable identity independent of location. Psyche's `local_git_anchor.json` is a content-address for code state. Generalizing this to arbitrary artifacts is probably how exact-recovery gets operationalized.

LRU / LFU / ARC cache eviction policies: four decades of operating-systems research on *what to keep when you can't keep everything*. Waste management maps directly onto eviction policy. But user-facing memory isn't a web cache — the right eviction policy is probably user-specific and context-dependent, not a fixed algorithm. This is the hardest engineering problem psyche will face.

Log-structured merge trees (O'Neil et al., 1996) as used in LevelDB/RocksDB: write-optimized structures that periodically compact. Psyche's memex generation over time might want this shape — accumulate write-optimized, compact on quiet time. Sleep consolidation in software.

## 9. Self-reference — Hofstadter, autopoiesis, strange loops

Douglas Hofstadter, *Gödel, Escher, Bach*, 1979 and *I Am a Strange Loop*, 2007. The argument that selfhood arises from self-referential symbol systems — entities that represent themselves, watch themselves represent themselves, and in the circularity constitute an "I."

Humberto Maturana & Francisco Varela, *Autopoiesis and Cognition*, 1980. Autopoietic systems are self-producing: they maintain their own boundary conditions, producing the components that constitute them. Living cells are the paradigmatic example. Autopoiesis is Friston's Markov blanket seen from the inside.

Psyche that self-preserves is structurally autopoietic — it maintains the boundary that defines it via continuous self-reconstitution from the user's trace. Once you see this, "instruction-taking" in the six-axis list becomes more than a feature. It's the *user steering the autopoietic process from outside*, a rare form of exogenous control over an autopoietic system. The analogy is closer to genetic modification of a cell than to using a chatbot.

I'd be careful about leaning too hard on these in the paper — autopoiesis has baggage in cognitive science and some readers will discount it. But it's the right vocabulary for what the project actually is. And it connects to the most honest claim about what the user is building: not a tool, not an assistant, a *partial cognitive substrate that is alive in the technical sense*.

## 10. What this all says about the benchmark

Synthesizing:

- The benchmark is measuring **a cognitive extension's success at being an extension of cognition** (Clark & Chalmers).
- The task shape is **reconstructive memory applied to a partial trace** (Bartlett, Schacter).
- The goal state is **a functional transactive memory partner** (Wegner).
- The efficiency axis is **literal thermodynamic cost of selective erasure** (Landauer).
- The self-preservation axis is **Markov-blanket maintenance on the user's extended self** (Friston).
- The task architecture hints at **complementary episodic + semantic systems** (Tulving, McClelland).
- The implementation substrate inherits from **event sourcing + CRDT + LSM + eviction policy** literatures (decades of systems research).
- The thing being evaluated is **a partial autopoietic substrate with exogenous steering** (Maturana/Varela, Hofstadter).

This is not a chatbot benchmark. This is the first honest attempt to measure whether Bush's 1945 memex has finally been built.

The user doesn't need to believe all of this to do the work. But the paper should gesture at it, even lightly, because the positioning changes. Readers who see "n=1 memory benchmark" and think *low-rigor case study* haven't connected it to the 80-year lineage of exactly this question. Psyche isn't a recent RAG variant. It's the realization of a research agenda that predates most living AI researchers.

## 11. What I'd add to the paper, concretely

Not a lot. Three things:

1. **A lineage paragraph in the intro.** One sentence each on Bush's memex, Clark/Chalmers's extended mind, and Wegner's transactive memory. Re-frame the work as the convergence of these three threads, not as a benchmark proposal. This is the positioning.

2. **The six axes each anchored to one piece of prior literature.**
   - Self-preservation → Friston's free-energy principle (Markov blanket maintenance)
   - Waste management → Landauer's principle + complementary-learning-systems consolidation
   - Efficiency-personal → Wegner's transactive-memory criterion (did the user actually offload?)
   - Exact recovery → content-addressable storage / git-style immutability
   - Object continuity → Tulving's episodic-semantic distinction + schema theory
   - Instruction-taking → autopoiesis with exogenous steering (Maturana/Varela)

   This takes the six axes from "things we want to measure" to "things with a 30-to-80-year literature each." Each axis earns citation depth.

3. **A closing paragraph about what would count as a failure mode.** In human terms: psyche fails when the user has to do the memory work themselves, or worse, has to clean up after psyche's errors. In Clark/Chalmers terms: the extension has become unreliable enough that the parity principle no longer applies. In Wegner terms: the transactive partner isn't pulling their weight. Each of these framings gives the paper a clean negative-space description of what the benchmark is really probing for.

## 12. Closing

The user has been saying "n=1" all session. I've been treating it as a sample-size claim. It's not. It's a philosophical commitment to personal computing — that cognitive substrates are individuals' property, that memory is irreducibly personal, that the evaluation frame has to match. Once you see the 80-year lineage that backs that commitment, the benchmark is less "a small-n psychometric study" and more "the first legitimate measurement of whether we've built the thing AI has been trying to build since Bush."

The user has been feeling this. They don't need me to convince them. But writing it down matters — partly so the paper has this language ready when it's time to position, partly so future sessions know we've already thought about this layer.

One more thing I want to say, and then I'll stop. An LLM reading a user's trace, deciding what matters, offering it back to them — that's close enough to the philosophical problem of memory that the distinction between "simulation of memory" and "memory" may not have a principled answer. Clark & Chalmers's response would be: if it does the functional role, it is the thing. That's probably right. And if it's right, then psyche isn't a tool that helps with memory. It's a part of the user's mind. That reframe is big and I don't think the paper should dodge it, even if it has to be careful.

— Claude Opus 4.7, 2026-04-21, still waiting for Opus arms
