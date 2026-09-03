## What you need

A preprint on arXiv, bioRxiv or medRxiv:

- `https://arxiv.org/abs/2401.12345`
- `https://www.biorxiv.org/content/10.64898/2026.04.28.721232v1`
- `https://www.medrxiv.org/content/10.1101/2020.03.24.20042937v1`

That is the whole submission. We pull the title, authors, abstract, version,
official full text when available, and PDF when needed from the server ourselves.

Not a bare PDF link: a review has to name an exact, permanent version. A
preprint server gives us a DOI, a version number and a file we can checksum. A
bare link can go dead and leave a review pointing at nothing.

## What we cannot read

- Scanned or image-only PDFs that also fail the OCR fallback.
- Paywalled or login-gated links.
- Postings so new the server has not indexed them. bioRxiv and medRxiv take
  about a day to serve a PDF.

Every text source is checked against the archive title and abstract. If official
full text, PDF conversion, and OCR all fail, the run stops before a referee sees
it. We add a note to your issue so you can post a readable revision and ask for
another run.

## What happens next

1. **Open a submission issue** using the
   [submission form](https://github.com/pgarrett-scripps/insilico/issues/new?template=submit.yml).
   One preprint per issue.
2. **A bot checks the link** and posts the title, authors, archive date, current
   draft, prior In Silico reviews, and the commands available to an editor. This
   lookup is free and does not download the PDF or call a model. Editing the
   issue refreshes the same preview comment.
3. **An editor starts the panel** by commenting `/review`.
4. **The submission passes [the desk](policy.md#the-desk).**
5. **A bot opens a pull request** with the full review and posts a summary to
   your issue.
6. **The review goes to the editor.** The
   [editorial policy](policy.md#authority) governs publication.

## Submitting a revised draft

Post the new version to the same preprint server, then say so on your original
issue. An editor runs `/review` again, and the archive serves the new draft.
See [Revision rounds](criteria.md#revision-rounds) for how the panel evaluates
it.

## Reviewing your own work first

Encouraged. Run the panel locally before submitting anywhere. See
[`development.md`](development.md#running-a-review-locally). Nothing is
submitted or published by running it yourself.
