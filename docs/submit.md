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
5. **You get a say.** Comment on the PR if the panel misread something. A human
   editor reads it before deciding, and a substantive objection can trigger a
   re-review. No agent reads it.
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

**No response letter goes to the panel.** The pipeline supports one; In Silico
deliberately doesn't send it, and it is worth saying plainly why. Handed a
letter asserting that revisions had been made, the compliance auditor confirmed
four of them and invented the supporting detail — a permutation test it said was
"reported in the Fig. 6 legend", which appears nowhere in the manuscript — and
the editor moved the verdict a full grade on the strength of that. Re-run
identically with no letter attached, the same auditor read the manuscript and
got all ten items right. An interested party's prose is not evidence, and the
system demonstrably could not treat it as anything else.

So the panel reads the new draft and nothing else. If you want a change noticed,
it has to be in the manuscript.

There is a **cap of three rounds**. An endless revise-and-resubmit loop is a
failure rather than a process, and at that point the submission gets decided.

## If the review got something wrong

That's a different thing from a revision, and it does not go back through the
panel. The manuscript hasn't changed, so there is nothing new for a referee to
read — and for the reason above, nothing you write is shown to one. Say what the
review got wrong on your submission issue. Three routes exist, and none of them
asks a model to weigh your account against the referees'.

**A right of reply.** We publish your response verbatim beside the review,
clearly labelled as yours. It is read by no agent, ever, and it changes no
score. It isn't edited down or summarised, and it doesn't have to be about a
factual error — if you simply think the panel was wrong, say so there. A reader
who reaches the review reaches your answer to it in the same place.

**Editor withdrawal or correction.** Where the panel demonstrably misread the
paper — it said you reported no effect sizes and they are in Table 2 — a human
editor can withdraw the review or annotate it with what it got wrong. A person
reads the manuscript and decides. No agent is involved and nothing is re-scored,
because the failure was a misreading and the fix for a misreading is a correct
reading, not another sample.

**Re-review.** A fresh review of the unchanged manuscript, run with no author
input at all. It can land anywhere, including exactly where the first one did;
there is no thumb on the scale, which is what makes the result worth anything.
The new review is published alongside the original and never replaces it.

Which route fits depends on what went wrong. A factual error about what your
manuscript says gets corrected or withdrawn — that is the one failure mode we
treat as disqualifying. A disagreement about judgment — *"we think this is more
novel than you credited"* — gets a right of reply, and stands publicly next to
the review rather than being argued into it.

The original review is never removed. Whatever follows is published beside it,
and the paper's page shows both.

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
uv pip install "peerreviewagents[research] @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

The second install is the pipeline itself — `requirements.txt` deliberately
leaves it out. Note that the PeerReviewAgents repository is currently private,
so this step may fail for you; until it's opened up, running the panel locally
is limited to people with access.

Nothing is submitted or published by running it locally.
