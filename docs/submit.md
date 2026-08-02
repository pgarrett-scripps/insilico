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

`--dry-run` on the runner script checks all of this without spending tokens, and
the editor will run it before triggering a review.

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

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

Nothing is submitted or published by running it locally.
