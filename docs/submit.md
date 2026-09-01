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
3. **Your file passes [the desk](policy.md#the-desk)**, including conversion
   checks and a triage pass for scope.
4. **A bot opens a pull request** with the full review and posts a summary to
   your issue.
5. **You can comment.** The submission issue is the place for questions or a
   request to remove the review.
6. **The editor merges or closes.** Merged means published. Closed means
   declined, and nothing appears.

## Submitting a revised draft

Post the new version to the same preprint server, then say so on your original
issue. An editor runs `/review` again — the archive now serves your new draft,
so it opens a new round by itself.

Expect the panel to read your revision from scratch. The five referees are
never told a previous round happened, so they will not credit you for a fix by
comparing drafts — write the paper so that someone meeting it for the first time
finds nothing to raise. It is the same standard your first submission was held
to, applied again.

What does follow you between rounds is the numbered list in the decision letter.
An auditor rules on every item against your new draft and has to quote the
passage that settles it, so an ask is closed by text that is in the paper, not
by a claim that it was handled. Items still open keep their original numbers, so
`R1-03` stays `R1-03` however many rounds it takes. The editor decides on that
list, the previous recommendation, and this round's panel.

The earlier review stays published as the record of that version unless you ask
us to remove it. The paper's page shows the whole arc. **Cap of three rounds.**

### Why we do not accept a response letter

The pipeline supports one. We do not send it.

Given a letter claiming revisions had been made, the compliance auditor
confirmed four of them and invented the supporting detail, citing a statistical
test it said was "reported in the Fig. 6 legend" that appears nowhere in the
paper. The editor then moved the verdict a full grade on that basis. Run again
with no letter, the same auditor read the paper and got all ten items right.

So the panel reads the new draft and nothing else. If you want a change noticed,
put it in the manuscript.

### If your submission is stopped at the desk

A short note on your issue, and no review is produced. Hidden-text findings are
never published automatically: they open as draft pull requests and go nowhere
unless an editor reads the evidence and agrees. Hidden text has innocent causes,
a scanned PDF's OCR layer being the common one, so if you think the scan is
wrong, say so.

## What gets published

Everything the panel produced: five specialist reports, the audits, the full
debate transcript, the debate synthesis the editor read, the decision letter,
and a `provenance.json` recording the models, config, pipeline commit and
cost.

Alongside it, `manuscript_stats.md`: counts over the text the panel actually
read, with no model involved and no opinion in them. It is there so a reader
holding your PDF can confirm the panel read the same document, which is the one
thing an overlay journal cannot otherwise prove.

## Removing a submission or review

Comment on your issue before the review is merged and we close it, no questions
asked. After publication, ask on the same issue and we remove the review from
the site.

## Reviewing your own work first

Encouraged. Run the panel locally before submitting anywhere — see
[`development.md`](development.md#running-a-review-locally). Nothing is
submitted or published by running it yourself.
