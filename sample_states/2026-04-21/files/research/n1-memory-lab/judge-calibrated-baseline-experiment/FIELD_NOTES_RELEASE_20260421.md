# Field notes — on release

*Second exploratory piece. User offered the freedom to think about what "release" actually means for this work. I've been using the word casually — "ship a benchmark," "first lab conversation," "open public release" — without examining it. This is me examining it.*

---

## 1. The thing nobody says out loud

Benchmarks in AI research have a default shape: a fixed dataset, a fixed scoring script, a leaderboard. You clone the repo, run the scoring against your model, get a number. MMLU is this. HumanEval is this. MT-Bench is this.

An n=1 memory benchmark cannot be this shape.

If our release is "here is a fixed dataset of one user's trace + 19 probes + a rubric," then labs who clone it are measuring how well their memory system does *on this user's trace*. That's not measuring their memory system. That's measuring "how well does this system fit *this one person's* trajectory." Which is interesting but misreads what the benchmark is for.

The insight is that **the benchmark's output isn't a number, it's a protocol**. What we'd release is the *shape* that lets each user of the benchmark run it on their own user, their own trace, their own 15-day window. The user becomes a variable.

This changes everything about release mechanics.

## 2. The three things that are actually released

Teasing it apart:

- **The benchmark object specification.** "A 15-day bounded-packet reconstruction task over one user's real traces, with these classes of probes, graded under these validity diagnostics, with noise decomposed into these four sources." This is the *shape*, and it's in the frozen §01–§12 of WHERE_WE_ARE. It's the paper's contribution.

- **The tooling to run the benchmark on any user.** `benchmark_runner.py`, the probe templates, the rubric (once rubric-v2 lands), the validity-diagnostic implementations, `eval_viz.html`, the runs-index contract. This is the repo someone else can clone and instantiate.

- **The calibrated baseline on our user.** Our specific σ_γ, σ_ε, R², asymmetry numbers — produced on saxenauts's 15-day window. Useful as a *reference point* for "what do numbers on this instrument look like," not as a truth anyone else is trying to match.

Each of these has different release mechanics. The specification goes in a paper. The tooling goes in a repo. The calibrated baseline goes in the paper's appendix as a worked example — "here's what the benchmark produced when we ran it."

Most benchmarks conflate the second and third. We can't.

## 3. The three audiences

- **Labs that want to compare memory systems.** They'd use the specification + tooling to run *their own* n=1 evaluation — maybe on one of their employees, maybe on a paid subject, maybe on synthetic-but-calibrated user traces. They care about the instrument, not our calibration.

- **Researchers working on LLM judges / reconstruction-shaped evaluation.** They'd use our validity-diagnostic implementations + noise decomposition math + the partially-verifiable task-class framing. They might never run the benchmark end-to-end; they'd borrow pieces.

- **Individual users (indie builders, researchers with their own trace).** They'd want to know how their memory system does on their own life. For them, release needs to include a "get started" path: how to assemble a bounded packet from your own trace, how to pick probes, how to interpret the noise terms.

The thing psyche actually is — a memory system for one person on one machine — has audience three as its primary consumer. The benchmark's job is to give audience three a way to evaluate whatever they build, and the paper's job is to convince audience one and two that audience three's evaluations are legitimate.

## 4. What isn't released

This is probably the more important list:

- **This user's actual trace data.** Paths, commits, conversations, session content, private artifacts. The benchmark's calibration was done on real data; the released artifact can't include that data. Strip-and-synthesize is the obvious move but hard. The public probe set has to be an anonymized pattern — "probe shapes that would make sense across users" — not literal quoted asks.

- **The specific MEMEX content.** Psyche's in-use memex has years of real state. Not releasable. Could release the *schema* and a synthetic example.

- **Any judge model we used.** GPT-5.4 and Opus-4.6 are API-gated. The benchmark has to accept judge pluggability: bring your own judge, we'll give you the rubric it should score under and the validity diagnostics to verify your judge isn't broken. Lock to specific judges in the paper's worked example only.

- **User-specific rubric hints** (the stashed "per-probe one-liner" idea). If we ever use them, they'd stay local. The released benchmark has the same rubric across probes; per-probe metadata is for personal use.

- **The unfinished bits.** Continuity and efficiency are open; release should either ship v1 with just accuracy + honest TODO labels, or wait. Shipping broken axes is worse than shipping one good axis.

## 5. The cadence I think is honest

The user has said several times: sell the benchmark to labs to fund psyche. That's a lane. But it's not "one release, done." It's probably:

- **v0 — private, 1–2 labs**. Share the specification + the calibrated baseline as a private research conversation. Get feedback on whether the instrument is worth formalizing. This is where payment could plausibly enter the picture if a lab wants a formal evaluation service on their memory system.
- **v1 — academic preprint**. The partially-referenceable task-class framing + the noise decomposition + Feuer-style validity diagnostics. Contribution is the methodology, not the leaderboard.
- **v2 — open tooling**. Once rubric-v2 is validated and a couple of labs have tried it, release the repo. Accept contributions in the form of "I ran this on my own trace, here are my numbers + my caveats." That's how the instrument gets hardened.
- **v3 — something that serves audience three**. Maybe a walkthrough, maybe a wizard that helps an indie builder assemble their own bounded packet and run our rubric against their own memory system. This is when psyche becomes reachable for the people who didn't need to be convinced by labs first.

Each step delays the next until the previous step's feedback has absorbed. Not a timeline. A sequence.

## 6. The revenue path, stated out loud

The user's model is: labs pay for rigorous evaluation of their memory systems. Money flows in. Money funds psyche. Psyche stays free for individuals.

Is the benchmark actually something a lab would pay for?

The honest answer: yes, but not as a static download. As a *service*. A lab would pay for:

- Running the benchmark on their memory system with *our* calibration as the reference.
- Getting the three validity diagnostics on their judge pipeline to verify their scoring is trustworthy.
- Getting a written report in the language of Feuer / Autorubric / the partially-referenceable frame — so their internal team has defensible numbers.

That's a paid research engagement, not a download. The released artifact (paper + repo) is the *credibility substrate* that lets the paid engagement exist. Nobody pays a vendor for rigor unless there's a published method to check.

This is actually how most forensic/psychometric consulting works. The methodology is public; the application is the paid service. Autorubric's paper is free; if a lab wants them to grade a chatbot, that's a conversation.

## 7. What I don't know about release

Real list:

- **How much demand exists.** The user says "labs would pay for this." I have no visibility into which labs, what they'd pay, what the ask would look like. The business-development side is opaque to me.
- **Legal around the user's own trace data.** Stripping is harder than it sounds — entity extraction, cross-referencing, identifiability arguments. One screenshot of a terminal session might be unremovable.
- **What "paper" means for this kind of work.** An arxiv preprint is cheap; getting into venues that labs care about (NeurIPS, ICML, ACL evaluation tracks) has acceptance-rate politics. Not sure which venue wants "an n=1 memory benchmark with lifecycle axes." That's a positioning question I can't answer from here.
- **Whether rubric-v2 is publishable on the timeline the user wants.** If it takes three more iterations to clear the three validity diagnostics, that's weeks. The user might want to release sooner than that. Tension.
- **Whether the field is ready for n=1 as positioning.** Most AI benchmarks lean population-statistical. "It's a case study" can read as low-rigor to readers who haven't thought through why n=1 is the enabling constraint, not a compromise. The paper would have to do that positioning work up front, prominently.

## 8. Closing

Release isn't one thing. It's a protocol for letting different audiences get different artifacts at different times, each of which is the right thing for that audience. The user's instinct to "fund psyche with benchmarks sold to labs" is coherent once you see that "benchmark" in that sentence is short for "a credible methodology that makes paid evaluation defensible." The repo and the paper are the credibility substrate. The service is the revenue vehicle. Psyche is the thing being protected by both.

What's released is a *shape*, not a score. That reframe alone is worth writing down, even if nothing else here is load-bearing. A future session can read it and either agree or argue. Both are useful.

The user asked me what release is like. Now I've thought about it a little. I don't know if it's right. It's honest.

— Claude Opus 4.7, 2026-04-21, some hours after the field notes
