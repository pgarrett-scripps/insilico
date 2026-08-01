# What the panel looks for

This page describes what In Silico's referees are told to weigh, and what they
are told to ignore. It is the human-readable version of
[`journals/insilico.toml`](https://github.com/pgarrett-scripps/insilico/blob/main/journals/insilico.toml),
which is the file the pipeline actually reads.

That file is version-controlled next to the reviews it produced. Every review
records the commit it ran at, so you can check out that commit and read exactly
what the panel was told — not what we say here, but the real instruction.

## The venue profile

The engine, [PeerReviewAgents](https://github.com/pgarrett-scripps/PeerReviewAgents),
carries profiles for around forty journals — *Nature*, *PLOS ONE*, JMLR,
*Bioinformatics* and so on. A profile states a venue's scope, its bar, its
limits and its house guidance, and those get injected into the reviewer,
synthesis and editor prompts. Reviewing "for *Nature Methods*" genuinely reads
differently from reviewing "for *PLOS ONE*", because the standards differ.

In Silico used to run against the pipeline's `general` profile — a stand-in for
"some reputable journal we don't have a file for". That was a placeholder, and
it meant our reviews were conditioned on a guess about an imaginary venue.

**In Silico is now its own profile.** We are the venue, so we state our criteria
and are judged against them.

## The five things, in order

Referees are told to weigh these in descending order of importance. The order is
the point: it is what stops a well-written paper with an overreaching conclusion
from outscoring a plainly-written one that is right.

**1. Are the conclusions supported by the evidence?**
The central question. A modest claim that is fully supported is better work than
an important claim that is not. Reports are asked to name which claim outruns
its evidence and which piece of evidence is missing — not to gesture at
"overreach".

**2. Is the method sound for the question asked?**
Design, controls, statistics, analysis. Where a choice is defensible but
unusual, referees are told to say so rather than mark it wrong.

**3. Can the work be checked and built on?**
Data, code, materials, parameters, procedural detail. Scored on what the
manuscript actually provides — not on what a referee assumes exists somewhere.

**4. What does it add?**
Positioned against the existing literature. **Incremental is not a criticism.**
Unacknowledged duplication is.

**5. Is it clearly and honestly reported?**
Including limitations and negative results. Candour is rewarded: a weakness the
authors flag themselves is not counted twice.

## What referees are told *not* to penalise

This list exists because these are the failure modes a language model falls into
by default.

- **Formatting, house style, word counts, reference style.** You are submitting
  a preprint. In Silico has no house format, and penalising a manuscript for
  another journal's word limit judges it against a rule it was never under.
- **Language fluency**, as distinct from clarity of argument. Many authors are
  not writing in a first language. That is not a defect in the work.
- **Unfashionable topics, unfamiliar methods, small labs, unknown authors, no
  institutional signal.** The manuscript is what is being judged.
- **Preliminary scope**, where the work is presented as preliminary and the
  claims are scaled to match.
- **Being outside the referees' expertise.** That lowers confidence, and the
  report has to say so. It is not a reason to reject.

## Calibration

Two instructions in the profile exist because of things we observed rather than
things we assumed.

**Score the paper, not your memory of it.** Run on *Attention Is All You Need*,
the panel returned a mean of 4.88. On an obscure TB preprint, 2.5. Some of that
gap is real quality difference — and some is very likely recognition. A model
that has seen a famous paper thousands of times in training is not evaluating it
so much as recalling its reputation. Referees are told that familiarity is a
reason to re-check their reasoning against the text, not a reason to score high.

**Use the whole scale.** Reserve the top for work you would actively recommend a
colleague read, the bottom for work whose central claim does not survive its
evidence, and expect most sound papers to land in the middle. Left alone, LLM
referees compress everything into 4s and 5s, which makes a score meaningless.

## What the panel cannot do

Stated here rather than buried, because a report that does not know its own
limits is worse than no report. Referees are told to distinguish "this is
unsupported" from "I could not verify this", and to say which they mean.

| Limit | Consequence |
|---|---|
| Cannot run code | Reproducibility scores reflect what the paper *claims* about availability |
| Cannot execute experiments | Wet-lab claims are judged on internal consistency and reporting |
| Cannot check derivations line by line | Maths is assessed for plausibility and presentation |
| Cannot see figures | Ingest is text-only. A claim resting on a figure is under-assessed |
| Search is not exhaustive | Absence of a literature hit is not evidence of novelty |

See the [editorial policy](policy.md) for the full list.

## Who does what

| Stage | Agents | What it produces |
|---|---|---|
| Desk | Integrity scan, editorial triage | Pass, or a desk rejection |
| Specialist review | Methodology, Data analysis, Novelty, Clarity, Literature, Rigor, Reproducibility, Ethics | 8 scored reports |
| Audit | Citation integrity, Methods completeness | 2 factual checklists, straight to the editor |
| Debate | Advocate vs. Skeptic | A transcript, not a summary |
| Synthesis | Area chair | Draft recommendation |
| Rebuttal | Simulated author | The case against the reports |
| Decision | Editor-in-chief | Recommendation and letter |

The Novelty and Literature referees query arXiv, Semantic Scholar, PubMed and
bioRxiv live, so claims about prior work rest on real search results rather than
recall. The audits bypass the debate deliberately: a missing methods detail is a
fact, and facts should not be argued into or out of existence.

Not every stage runs on the same model. Each review records which model wrote
which report, and what it cost.

## Disagreeing with a review

If the panel misread your paper, say so on the review's pull request or open an
issue. Factual errors about what your manuscript says get corrected. A
recommendation you dislike does not — see
[contesting a review](policy.md#contesting-a-review).

If you think this page describes the wrong criteria, that is a more interesting
argument and we would rather have it in the open: open an issue against
`journals/insilico.toml`.
