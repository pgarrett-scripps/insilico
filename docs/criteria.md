# What the panel looks for

The pipeline reads
[`journals/insilico.toml`](https://github.com/pgarrett-scripps/insilico/blob/main/journals/insilico.toml).
This page is the readable version; that file is the real instruction, and every
review records the commit it ran at.

## The five things, in order

The order is the point. It stops a well-written paper with an overreaching
conclusion from outscoring a plainly-written one that is right.

1. **Are the conclusions supported by the evidence?** The central question. A
   modest claim fully supported is better work than an important claim that is
   not. Reports must name which claim outruns its evidence.
2. **Is the method sound for the question asked?** Design, controls, statistics.
   A defensible but unusual choice is called unusual, not marked wrong.
3. **Can the work be checked and built on?** Scored on what the manuscript
   provides, not on what a referee assumes exists somewhere.
4. **What does it add?** Incremental is not a criticism. Unacknowledged
   duplication is.
5. **Is it clearly and honestly reported?** A weakness the authors flag
   themselves is not counted twice.

## What referees are told not to penalise

These are the failure modes a language model falls into by default.

- **Formatting, house style, word counts, reference style.** We have no house
  format, and another journal's word limit is a rule your preprint was never
  under.
- **Language fluency**, as distinct from clarity of argument.
- **Unfashionable topics, unfamiliar methods, small labs, unknown authors.**
- **Preliminary scope**, where the claims are scaled to match.
- **Being outside the referees' expertise.** That lowers confidence, and the
  report has to say so. It is not a reason to reject.

## Calibration

**Score the paper, not your memory of it.** On *Attention Is All You Need* the
panel returned a mean of 4.88; on an obscure TB preprint, 2.5. Some of that gap
is real and some is very likely recognition. Familiarity is a reason to re-check
the reasoning against the text, not a reason to score high.

**Use the whole scale.** Left alone, LLM referees compress everything into 4s
and 5s, which makes a score meaningless.

## When a dimension doesn't apply

Every manuscript gets all five referees, and some contain nothing in a given
dimension — a qualitative interview study has no statistics to judge. Those
referees return **not applicable**, which is left out of the mean rather than
counted as a good score, and the page says how many referees the mean covers.

We measured the alternative. Forced to produce a number, the data-analysis
reviewer wrote that a paper had no statistical claims to evaluate and then
scored it 5 out of 5, the highest data-analysis score in the corpus. A forced
score is not neutral, it is generous.

n/a is not a quiet way of marking work down. Thin or missing evidence is a low
score. Only a dimension the paper contains nothing of gets n/a.

## What the panel cannot do

Referees are told to distinguish "this is unsupported" from "I could not verify
this", and to say which they mean.

| Limit | Consequence |
|---|---|
| Cannot run code | Reproducibility reflects what the paper *claims* about availability |
| Cannot execute experiments | Wet-lab claims judged on internal consistency and reporting |
| Cannot check derivations | Maths assessed for plausibility and presentation |
| Cannot see figures | Ingest is text-only; a claim resting on a figure is under-assessed |
| Search is not exhaustive | Absence of a literature hit is not evidence of novelty |

## Who does what

| Stage | Agents | Produces |
|---|---|---|
| Desk | Integrity scan, editorial triage | Pass, or a desk rejection |
| Review | Scientific validity, Quantitative evidence, Contribution and prior work, Reporting and reproducibility, Ethics | 5 scored reports |
| Audit | Citation integrity, Methods completeness | 2 checklists, straight to the editor |
| Debate | Advocate and Skeptic, in parallel rounds | A transcript, published in full |
| Synthesis | Debate synthesizer | The condensed account of the debate the editor reads |
| Decision | Editor-in-chief | Recommendation and letter |

The Contribution and Prior-Work reviewer queries arXiv, Semantic Scholar,
PubMed and bioRxiv live, so claims about prior work rest on search results
rather than recall. The audits bypass the debate deliberately: a missing
methods detail is a fact, and facts
should not be argued into or out of existence.

Not every stage runs on the same model. Each review records which model wrote
which report, and what it cost.

## Revision rounds

**The referees are blind to the round.** Round 3 asks the five specialists
exactly what round 1 asked: read this manuscript. None of them is told that a
previous round exists, sees its own earlier report, or is shown what changed.
They still never see each other's reports either. Rounds are capped at three.

That is a correction, not an economy. Referees used to be handed their prior
critique and asked to rule on a revision, and a panel told it is judging a
revision is a panel given a reason to find progress. On a resubmission that was
byte-identical to the draft before it, one referee raised its score from 3 to 5
"because the revision successfully addresses the concerns", an audit described
an expanded methods section that was not in the paper, and the editor rejected
the manuscript for disregarding a review process nobody had gone through. A
round published before that panel went blind is never edited to match this
page; it carries a notice saying which arrangement produced its reports.

Continuity lives on the editor's numbered required revisions instead, which is
the actual contract with the authors. An item keeps the id it was born with:
`R1-03` is the third ask of round 1 for the life of the manuscript, still called
`R1-03` in round 3. A compliance auditor rules on each one against the new
draft, and to call an item addressed it must quote manuscript text — the quote
is then searched for in the manuscript, and one that is not there is recorded as
unsubstantiated and counts as still open.

Two things follow for a reader. The specialist reports in a later round are an
independent read of the paper as it stands, so a referee restating a concern is
not evidence the authors ignored it, and score movement between rounds includes
the resampling noise of a fresh panel. The account of what happened to the asks
is the compliance audit and the decision letter.

Each round publishes a `round.json` in its bundle, so you can verify what was
carried forward. A review published before round records existed cannot be
revised and needs a fresh review instead.

An unchanged resubmission is caught by comparing the manuscript file's SHA-256
against the one the previous round recorded — no re-reading, no converter that
could disagree with itself. The editor is told plainly that this is a fact about
a file rather than defiance: this pipeline reviews whatever draft an archive
serves it, and the authors have usually never seen the decision letter.

Nothing an author writes reaches the panel
([why](submit.md#why-we-do-not-accept-a-response-letter)). Review removal is
handled by a person under the [editorial policy](policy.md#removing-a-review).

## Removing a review

Anyone who submitted the paper, or an author of the paper, can ask us to remove
the review from the site. No explanation is required.

If you think this page describes the wrong criteria, open an issue against
`journals/insilico.toml`. That is a more interesting argument and we would
rather have it in the open.
