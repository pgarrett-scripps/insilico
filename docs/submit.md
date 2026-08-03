# Submitting a preprint

## What you need

A preprint on one of three servers:

- **arXiv**: `https://arxiv.org/abs/2401.12345`
- **bioRxiv**: `https://www.biorxiv.org/content/10.64898/2026.04.28.721232v1`
- **medRxiv**: `https://www.medrxiv.org/content/10.1101/2020.03.24.20042937v1`

That is the whole submission. We fetch the PDF and pull the title, authors,
abstract and version from the server ourselves.

### Why not a direct PDF link?

A review has to name an exact, permanent version of a paper. A preprint server
gives us a DOI and a version number, and we record a checksum of the file so a
reader can confirm they have the same one the panel read. A bare PDF link gives
none of that, and can go dead and leave a review pointing at nothing.

If your work is not on a preprint server yet, posting it is free, takes minutes,
and gets you a citable DOI whatever we say about the paper.

## What we cannot read

- Scanned or image-only PDFs. The panel has no OCR.
- Paywalled or login-gated links.
- Postings so new the server has not indexed them. bioRxiv and medRxiv take about
  a day to serve a PDF. Wait and resubmit.

Editors check the middle one before starting a run. A scanned file gets past that
check, and the pipeline catches it: every PDF is measured on conversion, and one
that arrives as run-together letters stops the run before a referee sees it. You
get a note on your issue saying so.

That note is not a rejection and no review is published. It is a statement about
a file, and we keep the two apart on purpose: a verdict attached to work no model
ever read would follow the paper around as though it meant something. Post a
version exported from your writing software rather than scanned, and ask for
another run.

Damage short of that is passed through, and the panel is told about it: reviewers
are shown what the converter mangled so nobody writes you up for spacing you
never wrote. The measurements are published with the review.

## The process

1. **Open a submission issue** using the
   [submission form](https://github.com/pgarrett-scripps/insilico/issues/new?template=submit.yml).
   One preprint per issue.
2. **An editor starts the panel** by commenting `/review`. This is manual, which
   controls cost and keeps out spam, so expect a wait.
3. **Your file passes the desk.** Two quick checks run first: a scan for text
   hidden from human readers, and a triage pass for scope. Most submissions clear
   both without noticing. See [the desk](policy.md#the-desk).
4. **A bot opens a pull request** with the full review and posts a summary to
   your issue.
5. **You get a say.** Comment on the pull request if the panel misread something.
   A human editor reads it, and a serious objection can trigger a re-review. No
   AI reads it.
6. **The editor merges or closes.** Merged means published. Closed means
   declined, and nothing appears.

## Submitting a revised draft

Post the new version to the same preprint server, then say so on your original
issue. An editor runs `/revise` and the panel opens a new round.

A revision round is not a fresh review. Each referee gets back the points it
raised, by number, and has to rule on each one: addressed, partly addressed, or
not. An auditor checks the previous decision letter's required revisions against
the new draft. The editor then decides on what changed rather than reading the
paper cold.

The earlier review is never edited or removed. It stays published as the record
of that version, and the paper's page shows the whole arc.

There is a **cap of three rounds**. Past that the submission gets decided.

### Why we do not accept a response letter

The pipeline supports one. We do not send it, and the reason is worth stating.

Given a letter claiming revisions had been made, the compliance auditor confirmed
four of them and invented the supporting detail, citing a statistical test it
said was "reported in the Fig. 6 legend" that appears nowhere in the paper. The
editor then moved the verdict a full grade on that basis. Run again with no
letter, the same auditor read the paper and got all ten items right.

So the panel reads the new draft and nothing else. If you want a change noticed,
put it in the manuscript.

## If the review got something wrong

This is different from a revision, and it does not go back through the panel. The
paper has not changed, so there is nothing new for a referee to read. Say what
went wrong on your submission issue. Three routes exist, and none of them asks an
AI to weigh your account against the referees'.

**A right of reply.** We publish your response next to the review, labelled as
yours. No AI reads it and it changes no score. It is not edited or summarised,
and it does not have to be about a factual error. If you think the panel was
simply wrong, say so there. Anyone who reads the review reads your answer in the
same place.

**Withdrawal or correction.** Where the panel clearly misread the paper, for
example claiming you reported no effect sizes when they are in Table 2, an editor
can withdraw the review or annotate what it got wrong. A person reads the paper
and decides. Nothing is re-scored, because the fix for a misreading is a correct
reading, not another attempt.

**Re-review.** A fresh review of the unchanged paper with no author input. It can
land anywhere, including exactly where the first one did. There is no thumb on
the scale, which is what makes the result worth anything. It is published beside
the original.

Which route fits depends on what went wrong. A factual error about what your
paper says gets corrected or withdrawn, and that is the one failure we treat as
disqualifying. A disagreement about judgement, such as thinking the work is more
novel than the panel credited, gets a right of reply and stands publicly next to
the review.

### If your submission is stopped at the desk

You get a short note on your issue, and no review is produced. Nothing is
published, and the finding is not final until a human has checked it.

Hidden-text findings are never published automatically. They open as draft pull
requests and go nowhere unless an editor reads the evidence and agrees. If you
think the scan is wrong, say so. Hidden text has innocent causes, a scanned PDF's
OCR layer being the common one, and we would rather hear about a false positive
than sit on it.

## What gets published

Everything the panel produced: all eight specialist reports, the debate, the
synthesis, the rebuttal, the decision letter, and a `provenance.json` recording
the models, config, pipeline commit and cost.

Alongside it, `manuscript_stats.md`: counts over the text the panel actually
read, measured with no model involved. How well your PDF converted, how long the
paper is, how its sentences and citations are distributed. It carries no opinion
and no agent is shown it. It is there so a reader holding your PDF can confirm
the panel read the same document, which is the one thing an overlay journal
cannot otherwise prove.

We publish unflattering reviews too, as long as the paper is in scope and the
review holds together. If you would rather that not happen, do not submit. We
will not take a review down because you dislike the recommendation. We will take
one down if it is factually wrong about what your paper says.

## Withdrawing

Comment on your issue before the review is merged and we close it, no questions
asked. After merging we add a withdrawal notice but keep the record, since the
review was already public and quietly deleting it is worse than annotating it.

## Reviewing your own work first

Encouraged. You can run the panel locally before submitting anywhere. See
[`development.md`](development.md#running-a-review-locally). Nothing is submitted
or published by running it yourself.
