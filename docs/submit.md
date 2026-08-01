# Submitting a preprint

## What you need

A preprint that is already public and machine-readable:

- **arXiv** — `https://arxiv.org/abs/2401.12345`
- **bioRxiv / medRxiv** — `https://www.biorxiv.org/content/10.1101/2024.01.01.573000v1`
- **Any public PDF** — a direct link ending in `.pdf`

That's the whole submission. We fetch the PDF ourselves and pull metadata from
the source API where one exists.

## What we can't read

- Scanned or image-only PDFs — the panel has no OCR. Convert to text first.
- Paywalled or login-gated links.
- Anything that isn't a PDF at the URL you give us.

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
