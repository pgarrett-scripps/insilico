# Editorial policy

## Standing

In Silico is an experiment in open machine-generated peer review. It is not
accredited, not indexed, and not a substitute for conventional peer review.
Do not cite an In Silico listing as evidence that a result is correct.

## Authority

**The panel decides the verdict. A human decides whether to publish it.**

The editor agent recommends accept, minor revision, major revision or reject,
and we publish it word for word. It binds nobody. Merging the pull request is
the decision to publish. An editor may decline to publish a review that is
incoherent, that misreads the paper badly enough to mislead, or that came from a
mangled ingest.

## What acceptance means

**In Silico accepts a paper the panel returns at accept or minor revision, and
declines the rest.**

The editor is never told this rule. It recommends one of the four standard
verdicts with nothing hanging on the answer, and the line is drawn afterwards.
An editor told that "minor revision" means acceptance is an editor being asked
to gatekeep, and it would grant more of them.

The line is drawn on the editor's verdict rather than on the panel's mean
score, but on the evidence so far the two barely differ. Across the 20 reviews
by a graded panel, every paper scoring 3.75 or below was returned at major
revision and every paper scoring 4.00 or above at minor; the only overlap is a
single paper at 3.88 that went each way on different runs. A threshold at 3.9
would reproduce the editor's verdict 19 times out of 20.

We use the verdict anyway, because it is a judgement about the manuscript and
the mean is an average that happens to track it. The published evidence cited
above came from the historical eight-reviewer graded panel. New reviews use the
five-reviewer panel. Nobody should read the current acceptance line as evidence
that the editor is doing something the arithmetic could not.

"Declined" rather than "rejected", because that is what happened: the editor
declined to accept, and most declined papers carry a letter setting out what
would fix them. Anyone can submit a preprint they did not write, so a permanent
machine-generated "rejected" is not a label we will attach to a stranger's work
on this evidence.

Where a paper has been reviewed more than once, its status comes from the most
recent review by the graded panel. A run on a single model is a published
experiment rather than an editorial decision, and does not overturn a panel it
was run to be compared against.

## Scope

**In scope.** Any original research manuscript, in any discipline, whose claims
a careful reader can evaluate from the manuscript and what it cites or deposits.
Empirical, theoretical, computational and methodological work all qualify, as do
negative results, replications and reanalyses. What matters is whether the
evidence can be checked, not the field.

**Out of scope.**

- **Anything where a wrong machine-generated review could affect patient care** —
  clinical trial reports, diagnostic or treatment guidance, dosing
  recommendations. This is the one hard line, and it is not about field: a
  computational paper that outputs a dosing recommendation is out, a
  clinical-adjacent methods paper that does not is in.
- **Work whose central evidence cannot be checked at all.**
- **Anything that is not a research manuscript.** Editorials, press releases,
  marketing, or text making no checkable claim.

Out-of-scope submissions are declined at the desk, without running the panel.

## Who may submit

Anyone may submit any public preprint, including one they did not write.

**Every review says which it was.** The form asks one question: are you an
author of, or affiliated with, this paper? Where the answer is no, the review
carries a notice that the authors did not request it and have not replied.
Older reviews say "solicitation unrecorded" rather than passing for requested.
We do not verify the claim, and we say we don't.

Submitting a rival's work to attach a public criticism to it is not a use we
support. An editor reads every submission before starting a run, and declines
any that reads as score-settling.

If you find an unrequested review of your work, open an issue. If you object to
it existing at all, we take it down.

## The desk

Two checks run before any referee is assigned, and either can stop a submission.
`provenance.json` records which were active.

### We do not screen for prompt injection

Our referees are all AI, so a paragraph hidden in a PDF telling the reviewer to
recommend acceptance would reach every referee we have. You should know that we
do not look for it.

We used to. The scan compared a text run's colour against a threshold without
checking what was drawn behind it, so white labels on a dark figure read as
concealed text — and on a real submission it reported that the authors had
hidden eleven thousand characters, which were the axis labels of a heatmap. The
matching half was a list of phrasings: it caught the payload copied off a blog
and nothing rewritten. A check that reliably accuses honest authors and
unreliably catches dishonest ones is worse than no check, so it was removed
rather than tuned.

Nothing here replaces it. If you submit a manuscript with instructions hidden
in it, our referees will read them as prose. What we can promise is the
opposite of what the scan promised: we will not publish a claim that anyone
concealed anything, because we are no longer in a position to make one.

### Editorial triage

One fast pass decides whether the submission is in scope, intelligible,
complete, and not fatally flawed on its face. It is told to reject sparingly and
send anything borderline to the panel.

A desk rejection is badged separately from a panel rejection. Nothing read the
paper in depth and no specialist reports exist.

## Known limitations

Properties of the method, not bugs we expect to fix. The panel cannot run your
code, check your maths, or see your figures; its literature search is real but
not exhaustive; and it rewards conventional structure and clear writing, so
unusual but correct work will probably score worse than it deserves. Consequences
of each: [what the panel cannot do](criteria.md#what-the-panel-cannot-do).

Nothing is truncated today — every agent reads the whole paper. If long
submissions become a budget problem we may cap that, and each affected review
will record it.

Referees may return **not applicable** rather than a score, which is left out of
the mean rather than averaged in. See
[when a dimension doesn't apply](criteria.md#when-a-dimension-doesnt-apply).

## Reproducibility

Every review ships a `provenance.json`: provider, the model at each stage and
any per-agent override, pipeline version and commit SHA, debate rounds, active
desk screens, per-reviewer scores, total and per-agent cost, and the resolved
preprint metadata. You can re-run the panel yourself. Output will not be
identical — the models are not deterministic — but the configuration is fully
disclosed.

A published bundle is never edited. A fresh run is published separately, and so
is a [revision round](criteria.md#revision-rounds).

## Removing a review

Anyone who submitted the paper, or an author of the paper, can ask us to remove
the review. Comment on the review pull request or submission issue. Before
publication, we close it. After publication, we remove the review from the
site. No explanation is required.

## Conflicts and cost

The editor is one person running this out of pocket. Reviews are triggered
manually because each one costs real money. No queue guarantee, no SLA, and no
promise the project outlives the author's interest in it.

## Data

We store the preprint URL and its public metadata, the review bundle, the GitHub
issue thread, and your reply if you send one. We do not store PDFs — they are
fetched to a temporary directory at review time and deleted afterwards.

Paper text is sent to a third-party AI provider, currently Anthropic. Since we
only take already-public preprints, this should not come up.

## License

Reviews and site content are CC BY 4.0. Preprints stay under whatever license
their authors chose; we host none of them.
