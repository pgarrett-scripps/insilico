# What the panel looks for

This page describes what In Silico's referees are told to weigh, and what they
are told to ignore. It is the human-readable version of
[`journals/insilico.toml`](https://github.com/pgarrett-scripps/insilico/blob/main/journals/insilico.toml),
which is the file the pipeline actually reads.

That file is version-controlled next to the reviews it produced. Every review
records the commit it ran at, so you can check out that commit and read exactly
what the panel was told. Not what we say here, but the real instruction.

## The venue profile

The engine, [PeerReviewAgents](https://github.com/pgarrett-scripps/PeerReviewAgents),
carries profiles for around forty journals: *Nature*, *PLOS ONE*, JMLR,
*Bioinformatics* and so on. A profile states a venue's scope, its bar, its
limits and its house guidance, and those get injected into the reviewer,
synthesis and editor prompts. Reviewing "for *Nature Methods*" genuinely reads
differently from reviewing "for *PLOS ONE*", because the standards differ.

In Silico has its own profile. We are the venue, so we state our own criteria
and the panel is held to them, rather than to a generic stand-in for whatever
journal a paper might otherwise have gone to.

## The five things, in order

Referees are told to weigh these in descending order of importance. The order is
the point: it is what stops a well-written paper with an overreaching conclusion
from outscoring a plainly-written one that is right.

**1. Are the conclusions supported by the evidence?**
The central question. A modest claim that is fully supported is better work than
an important claim that is not. Reports are asked to name which claim outruns
its evidence and which piece of evidence is missing, rather than gesturing at
"overreach".

**2. Is the method sound for the question asked?**
Design, controls, statistics, analysis. Where a choice is defensible but
unusual, referees are told to say so rather than mark it wrong.

**3. Can the work be checked and built on?**
Data, code, materials, parameters, procedural detail. Scored on what the
manuscript actually provides, not on what a referee assumes exists somewhere.

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
gap is real quality difference, and some is very likely recognition. A model
that has seen a famous paper thousands of times in training is not evaluating it
so much as recalling its reputation. Referees are told that familiarity is a
reason to re-check their reasoning against the text, not a reason to score high.

**Use the whole scale.** Reserve the top for work you would actively recommend a
colleague read, the bottom for work whose central claim does not survive its
evidence, and expect most sound papers to land in the middle. Left alone, LLM
referees compress everything into 4s and 5s, which makes a score meaningless.

## When a dimension doesn't apply

A referee may return **not applicable** rather than a score. Every manuscript
gets all eight, and some manuscripts contain nothing in a given referee's
dimension. A qualitative interview study has no statistical analysis to judge.

An n/a is excluded from the panel mean entirely, rather than counted as a good
score, and the review page says how many referees the mean is over ("mean over
7 of 8"). That matters because the forced number was reliably a generous one:
told to score a qualitative study anyway, the data-analysis reviewer wrote that
it had no statistical claims to evaluate and gave it 5 out of 5, the highest
data-analysis score in the corpus.

n/a is not for work judged harshly. Thin, unclear or missing evidence is a low
score, since the referee had something to weigh and found it wanting. n/a is only for
a dimension the manuscript contains nothing of.

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

## Revision rounds

When authors revise and resubmit, the panel does not re-read the paper cold.
Round 2 evaluates the *delta*:

- **Each referee gets its own prior report back**, with every weakness it raised
  addressable by a stable id, and rules on each one. Referees never see each
  other's reports, so the panel's independence is not quietly abandoned in later
  rounds.
- **A compliance auditor** takes the previous decision letter's numbered
  required revisions and checks each against the new draft.
- **The editor decides on what changed**, and is told which round this is and
  how many remain.

Rounds are capped at three; past that the submission is decided rather than
cycled.

Two things make this checkable rather than asserted.

**The round record.** Every round writes `round.json` next to its markdown,
required revisions with stable ids (`R1-03` names the third ask of round 1 for
the life of the manuscript), per-referee weaknesses, scores. Round 2 reports
against those ids rather than string-matching prose, and the record is published
in the bundle so you can verify what was carried forward. The record is also
what makes a later round possible at all: a revision round reports against the
previous round's `round.json`, so a review published before round records
existed cannot be revised and need a fresh review instead.

**The draft comparison.** A revision round diffs the old and new manuscripts.
Because the reviewed PDF is fingerprinted, that baseline is rebuilt by
re-fetching the exact version reviewed and confirming it still hashes to what
the panel saw. If it does not, or if it cannot be fetched, **the round says so
on its own page and in the paper's history**, because a round that ruled without
a verified comparison is weaker evidence than one that did, and the two would
otherwise look identical.

### No author input

What a round reads is the manuscript. The engine can take an author response
letter and In Silico never sends one, because we tried it and watched what
happened: given a letter asserting that revisions had been made, the compliance
auditor confirmed four of them and manufactured the supporting detail, citing a
permutation test as "reported in the Fig. 6 legend" that appears nowhere in the
paper. The editor moved the verdict a full grade on that. Re-run identically
with no letter, the same auditor read the manuscript and got all ten items
right. An interested party's prose is not evidence, and the panel could not be
made to treat it as anything else.

Authors are not left without recourse; the recourse is human rather than
agentic. See [contesting a review](policy.md#contesting-a-review).

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
recommendation you dislike does not. See
[contesting a review](policy.md#contesting-a-review).

If you think this page describes the wrong criteria, that is a more interesting
argument and we would rather have it in the open: open an issue against
`journals/insilico.toml`.
