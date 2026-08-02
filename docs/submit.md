# Submitting a preprint

## What you need

A preprint on one of three servers:

- **arXiv** — `https://arxiv.org/abs/2401.12345`
- **bioRxiv** — `https://www.biorxiv.org/content/10.64898/2026.04.28.721232v1`
- **medRxiv** — `https://www.medrxiv.org/content/10.1101/2020.03.24.20042937v1`

That's the whole submission. We fetch the PDF ourselves and pull the title,
authors, abstract and version from the server's API.

bioRxiv and medRxiv DOIs carry either the `10.1101` prefix or the newer
`10.64898` one. Both work.

### Why not a direct PDF link?

A review has to name a specific, permanent revision of a manuscript, and a bare
PDF URL doesn't provide one.

A preprint server gives us a DOI *and* a version number, so a review can state
exactly which revision it read — and we record a SHA-256 of the file to prove
it. A loose PDF gives us none of that: no stable identity, no way for a reader
to tell whether the file they download is the one the panel saw, and nothing
stopping the link from going dead and leaving a review pointing at nothing.

If your work isn't on a preprint server yet, posting it is free and takes
minutes, and you get a citable DOI out of it regardless of what we say about
the paper.

## What we can't read

- Scanned or image-only PDFs — the panel has no OCR. Convert to text first.
- Paywalled or login-gated links.
- Postings so new the server hasn't finished indexing them. bioRxiv and medRxiv
  don't serve a PDF for a day or so after a preprint first appears; if you get
  an error saying so, wait and resubmit.

`--dry-run` on the runner script catches the last two without spending tokens —
it resolves the URL and downloads the file, so a gated link or a missing PDF
fails there. It only confirms the response really is a PDF, though: a scanned or
image-only file passes the dry run and fails later at ingestion. The editor runs
it before triggering a review.

## The process

1. **Open a submission issue.** Use the
   [submission form](https://github.com/pgarrett-scripps/insilico/issues/new?template=submit.yml).
   One preprint per issue.
2. **An editor triggers the panel** by commenting `/review`. This is manual —
   it gates cost and stops the queue filling with spam. Expect a wait.
3. **Your file passes the desk.** Two quick checks run first: a scan for text
   hidden from human readers that carries instructions to an automated reviewer,
   and a triage pass for scope and completeness. Most submissions clear both
   without noticing they happened. See [the desk](policy.md#the-desk).
4. **The bot opens a pull request** with the full review bundle and posts the
   summary back on your issue.
5. **You get a say.** Comment on the PR if the panel misread something. The
   editor reads rebuttals before deciding, and a substantive one can trigger a
   re-review.
6. **The editor merges or closes.** Merged means listed here with the review
   attached. Closed means declined, and nothing is published.

## Resubmitting a revised draft

Post the revised version to the same preprint server, then say so on your
original submission issue. An editor runs `/revise` and the panel opens a new
round on the new version.

One caveat: a new round reports against the previous round's machine-readable
record (`round.json` in its bundle). Reviews published before round records
existed cannot be revised — those get a fresh `/review` on the new version
instead.

A revision round is not a fresh review. Each referee gets back the specific
points *it* raised, by id, and has to rule on each one: addressed, partly
addressed, or not. A compliance auditor takes the previous decision letter's
numbered required revisions and checks them against the new draft. The editor
then decides on the delta rather than re-reading the paper cold.

The earlier review is never edited or removed. It stays published as the record
of that revision, and the paper's page shows the whole arc — what each round
required, and how the recommendation moved.

**You can include a response letter.** Give the editor a public URL to it and it
goes to the panel — but not as prose. It is screened for hidden instructions at
the same gate as the manuscript, and then read by a verifier that checks each
claim against the manuscript itself. Only corroborated pointers reach the
referees: *"the authors say X was added at §3.2 — go read §3.2 and judge it."*
A response letter can direct attention. It cannot move a score by asserting
something, and the verification is published so you can see exactly what the
panel was shown.

There is a **cap of three rounds**. An endless revise-and-resubmit loop is a
failure rather than a process, and at that point the submission gets decided.

## If the review got something wrong

That's a different thing from a revision, and it has its own route. Comment on
your submission issue saying what the review got wrong. An editor runs
`/appeal`, which re-reviews **without** touching the round number — the
manuscript hasn't changed, so nothing about it is being re-judged. Like
`/revise`, it needs the earlier round to have left a `round.json` in its
bundle; reviews that predate round records need a fresh `/review` instead.

What happens to your comment:

1. It's fetched verbatim and **published in the bundle**. We snapshot rather
   than link, because comments stay editable and a review that cited a mutable
   comment wouldn't be a record of anything. (The published file itself carries
   no byline; where the comment came from is recorded in provenance.)
2. It's screened for hidden instructions, like any submitted text.
3. A verifier checks each claim against your manuscript.
4. Referees get **corroborated pointers only** — "the authors say effect sizes
   are in Table 2; go read Table 2 and judge it" — never your words as prose.

The editor may narrow the appeal to the referee you're disputing; when that
happens, the rest keep their existing reports, so the panel score still reflects
all eight and the change you get is the change you argued for rather than eight
referees resampling. Left unnarrowed, the whole panel re-runs.

**What this can and can't do.** *"You said we didn't report effect sizes; they're
in Table 2"* is checkable, and if it checks out the score can move. *"We think
this is more novel than you credited"* is a disagreement about judgment — the
panel won't re-run for it, and your comment stands publicly as your dissent
next to the review.

The original review is never removed. A correction is published beside it, and
the paper's page shows both.

### If your submission is stopped at the desk

You'll get a short note on your issue saying it was held, and no review will
have been produced. Nothing is published at that point, and the finding isn't
final until a human has checked it.

Integrity findings in particular are never auto-published — they open as draft
pull requests and go nowhere unless an editor reads the evidence and agrees. If
you think the scan is wrong, say so on your issue. Hidden text has innocent
causes (a scanned PDF's OCR layer is the common one) and we would rather hear
about a false positive than quietly sit on it.

## What gets published

Everything the panel produced: all eight specialist reports, the debate
transcript, the synthesis, the rebuttal, the decision letter, and a
`provenance.json` recording the model, config, pipeline commit, and cost.

We publish reviews with unflattering verdicts too, as long as the paper is in
scope and the review is coherent. If you'd rather that not happen, don't submit —
we won't take a review down because you dislike the recommendation. (We will
absolutely take one down if it's factually wrong about what your paper says; see
the [policy](policy.md).)

## Withdrawing

Comment on your submission issue before the review PR is merged and we'll close
it, no questions. After merging, we'll add a withdrawal notice to the page but
keep the record — the review already existed publicly and quietly deleting it is
worse than annotating it.

## Reviewing your own work

Encouraged. Run the panel locally before you submit anywhere:

```bash
git clone https://github.com/pgarrett-scripps/insilico
cd insilico
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install "peerreviewagents @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

The second install is the pipeline itself — `requirements.txt` deliberately
leaves it out. Note that the PeerReviewAgents repository is currently private,
so this step may fail for you; until it's opened up, running the panel locally
is limited to people with access.

Nothing is submitted or published by running it locally.
