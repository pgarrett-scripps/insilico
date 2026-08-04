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

**Every review says which it was.** Where the submitter says they are not an
author, the review carries a notice that the authors did not request it and have
not replied. Older reviews say "solicitation unrecorded" rather than passing for
requested. We do not verify the claim, and we say we don't.

The form asks non-authors why they are submitting. An editor reads that first,
and declines submissions that read as score-settling.

If you find an unrequested review of your work, open an issue. If it misreads
the paper we correct it. If you object to it existing at all we take it down —
a lower bar than for reviews the authors asked for.

## The desk

Two checks run before any referee is assigned, and either can stop a submission.
`provenance.json` records which were active.

### Submission integrity

Every file is scanned for text hidden from human readers — white fill, zero
opacity, invisible render mode, tiny type, off-page placement — carrying
instructions aimed at an automated reviewer. Our referees are all AI, so a
payload written for AI reaches every referee we have.

- **It runs before any model reads the file.** No tokens, no model call.
- **Hidden text alone is never a rejection.** Scanned PDFs carry an invisible
  OCR layer. Rejection needs an instruction aimed at the reviewer inside it.
- **Visible instructions count too.** The line is who the text speaks to.
  Language *addressing* the reviewer is manipulation; language *describing* such
  attempts is a paper about prompt injection quoting its subject. If you quote
  payloads, say so in the submission.

**A finding is never published automatically.** It is an allegation about named
people. Findings open as draft pull requests and go nowhere unless a human
editor reads the evidence and agrees. If we are unsure we contact the authors
privately and publish nothing.

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

Reviews are never silently edited. Where one is wrong, an editor withdraws it or
annotates the page, and the published bundle stays byte-for-byte as it was. A
fresh run is published beside the old one, never over it, and so is a
[revision round](criteria.md#revision-rounds).

## Contesting a review

Comment on the review PR, or on your submission issue if it is already merged.
Nothing you write is shown to the panel
([why](submit.md#why-we-do-not-accept-a-response-letter)). Three routes exist
instead, described in full under
[if the review got something wrong](submit.md#if-the-review-got-something-wrong):

- **A right of reply** — published beside the review, labelled as yours, read by
  no AI, changing no score. This is the route for disagreeing with the
  judgement, and your dissent sits next to it permanently.
- **Withdrawal or correction** — where the panel clearly misread the paper. A
  factually false statement about your paper is the one failure we treat as
  disqualifying.
- **Re-review** — a fresh review of the unchanged paper, published alongside the
  original.

## Conflicts and cost

The editor is one person running this out of pocket. Reviews are triggered
manually because each one costs real money. No queue guarantee, no SLA, and no
promise the project outlives the author's interest in it. If a submission is the
editor's own work, the review says so on its page.

## Data

We store the preprint URL and its public metadata, the review bundle, the GitHub
issue thread, and your reply if you send one. We do not store PDFs — they are
fetched to a temporary directory at review time and deleted afterwards.

Paper text is sent to a third-party AI provider, currently Anthropic. Since we
only take already-public preprints, this should not come up.

## License

Reviews and site content are CC BY 4.0. Preprints stay under whatever license
their authors chose; we host none of them.
