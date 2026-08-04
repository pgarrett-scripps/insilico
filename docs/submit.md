# Submitting a preprint

## What you need

A preprint on arXiv, bioRxiv or medRxiv:

- `https://arxiv.org/abs/2401.12345`
- `https://www.biorxiv.org/content/10.64898/2026.04.28.721232v1`
- `https://www.medrxiv.org/content/10.1101/2020.03.24.20042937v1`

That is the whole submission. We fetch the PDF and pull the title, authors,
abstract and version from the server ourselves.

Not a bare PDF link: a review has to name an exact, permanent version. A
preprint server gives us a DOI, a version number and a file we can checksum. A
bare link can go dead and leave a review pointing at nothing.

## What we cannot read

- Scanned or image-only PDFs. The panel has no OCR.
- Paywalled or login-gated links.
- Postings so new the server has not indexed them. bioRxiv and medRxiv take
  about a day to serve a PDF.

Every PDF is measured on conversion, and one that arrives as run-together
letters stops the run before a referee sees it. You get a note on your issue.
That note is not a rejection and nothing is published — a verdict attached to
work no model ever read would follow the paper around as though it meant
something. Export from your writing software rather than scanning, and ask for
another run.

Damage short of that is passed through and the panel is told about it, so nobody
writes you up for spacing you never wrote. The measurements are published with
the review.

## The process

1. **Open a submission issue** using the
   [submission form](https://github.com/pgarrett-scripps/insilico/issues/new?template=submit.yml).
   One preprint per issue.
2. **An editor starts the panel** by commenting `/review`. This is manual, which
   controls cost and keeps out spam, so expect a wait.
3. **Your file passes [the desk](policy.md#the-desk)** — a scan for hidden text
   and a triage pass for scope.
4. **A bot opens a pull request** with the full review and posts a summary to
   your issue.
5. **You get a say.** Comment if the panel misread something. A human editor
   reads it, and a serious objection can trigger a re-review. No AI reads it.
6. **The editor merges or closes.** Merged means published. Closed means
   declined, and nothing appears.

## Submitting a revised draft

Post the new version to the same preprint server, then say so on your original
issue. An editor runs `/revise`.

A revision round is not a fresh review. Each referee gets back the points it
raised, by number, and rules on each: addressed, partly addressed, or not. An
auditor checks the previous decision letter's required revisions against the new
draft. The editor decides on what changed rather than reading the paper cold.

The earlier review is never edited or removed; it stays published as the record
of that version, and the paper's page shows the whole arc. **Cap of three
rounds.**

### Why we do not accept a response letter

The pipeline supports one. We do not send it.

Given a letter claiming revisions had been made, the compliance auditor
confirmed four of them and invented the supporting detail, citing a statistical
test it said was "reported in the Fig. 6 legend" that appears nowhere in the
paper. The editor then moved the verdict a full grade on that basis. Run again
with no letter, the same auditor read the paper and got all ten items right.

So the panel reads the new draft and nothing else. If you want a change noticed,
put it in the manuscript.

## If the review got something wrong

This does not go back through the panel — the paper has not changed, so there is
nothing new for a referee to read. Say what went wrong on your submission issue.
A person reads it. Neither route asks an AI to weigh your account against the
referees'.

**We take it down.** Where the panel clearly misread the paper — say, claiming
you reported no effect sizes when they are in Table 2 — the review is removed
from the site. Nothing is re-scored: the fix for a misreading is a correct
reading, not another attempt.

**We review it again.** A fresh review of the unchanged paper with no author
input. It can land anywhere, including exactly where the first one did. There is
no thumb on the scale, which is what makes the result worth anything. It is
published alongside the original.

A factual error about what your paper says is the one failure we treat as
disqualifying, and it gets the review pulled. A disagreement about judgement
does not: we will not remove a recommendation because you dispute it.

### If your submission is stopped at the desk

A short note on your issue, and no review is produced. Hidden-text findings are
never published automatically: they open as draft pull requests and go nowhere
unless an editor reads the evidence and agrees. Hidden text has innocent causes,
a scanned PDF's OCR layer being the common one, so if you think the scan is
wrong, say so.

## What gets published

Everything the panel produced: eight specialist reports, the debate, the
synthesis, the rebuttal, the decision letter, and a `provenance.json` recording
the models, config, pipeline commit and cost.

Alongside it, `manuscript_stats.md`: counts over the text the panel actually
read, with no model involved and no opinion in them. It is there so a reader
holding your PDF can confirm the panel read the same document, which is the one
thing an overlay journal cannot otherwise prove.

We publish unflattering reviews too, as long as the paper is in scope and the
review holds together. If you would rather that not happen, do not submit. We
will not take a review down because you dislike the recommendation. We will take
one down if it is factually wrong about what your paper says.

## Withdrawing

Comment on your issue before the review is merged and we close it, no questions
asked. After merging, ask and we take it down.

## Reviewing your own work first

Encouraged. Run the panel locally before submitting anywhere — see
[`development.md`](development.md#running-a-review-locally). Nothing is
submitted or published by running it yourself.
