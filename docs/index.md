---
hide:
  - navigation
  - toc
---

<div class="ins-masthead" markdown="1">

<h1 class="ins-masthead__title">In Silico</h1>

<hr class="ins-masthead__rule">

<p class="ins-masthead__tagline">
An open, AI-refereed overlay journal for computational preprints.
</p>

<div class="ins-masthead__actions" markdown="1">
[Browse reviews](reviews/index.md){ .md-button .md-button--primary }
[Submit a preprint](submit.md){ .md-button }
</div>

</div>

<p class="ins-standfirst">
We don't host papers. Point us at a preprint that already exists and we run it
past a multi-agent referee panel, then publish the entire review next to a link
to your work.
</p>

## Why

Peer review is slow, invisible, and mostly discarded. Referee reports are
written once, read by three people, and thrown away.

In Silico inverts that. **The review is the published artifact.** Every
submission gets eight specialist reports, a recorded advocate/skeptic debate, an
area-chair synthesis, a simulated author rebuttal, and an editor's verdict — and
all of it is public, versioned, and reproducible down to the model id.

## What the panel does

| Stage | Who | Output |
|---|---|---|
| Desk | Integrity scan · editorial triage | Pass, or a desk rejection |
| Specialist review | Methodology · Data analysis · Novelty · Clarity · Literature · Rigor · Reproducibility · Ethics | 8 scored reports |
| Audit | Citation integrity · Methods completeness | 2 factual checklists |
| Debate | Advocate vs. Skeptic | Full transcript |
| Synthesis | Area chair | Draft recommendation |
| Rebuttal | Simulated author | Concessions and disagreements |
| Decision | Editor-in-chief | Recommendation + letter |

The Novelty and Literature reviewers query arXiv, Semantic Scholar, PubMed, and
bioRxiv live, so their claims about prior work are grounded in real search
results rather than recall.

Not every stage runs on the same model, and each review records which model
wrote which report. Engine:
[PeerReviewAgents](https://github.com/pgarrett-scripps/PeerReviewAgents).

## Reviews name a revision, not a paper

Authors replace preprints in place, so a review can quietly end up sitting next
to a manuscript it never read. Every review records the version and a SHA-256 of
the exact PDF the panel was given, and we re-check the corpus monthly.

When a revised preprint is re-reviewed, the new review is published **beside**
the old one, not on top of it. Each paper has a page listing every review it has
received; earlier reviews are never edited or removed, because they are the
record of what the panel said about that revision.

This is also why submissions have to come from arXiv, bioRxiv or medRxiv: those
give a DOI and a version number to anchor a review to. A loose PDF link names no
particular revision and can go dead.

## What this is not

!!! warning "Advisory, not authoritative"
    Every recommendation on this site was produced by a language model. It is
    **advisory**. A human editor makes each accept/decline call, and no LLM
    verdict is ever final.

    An In Silico listing is not certification, not a substitute for
    conventional peer review, and not evidence that a result is correct. It is a
    machine-generated second opinion, published openly so you can judge the
    reasoning for yourself.

We publish the panel's mistakes along with its insights. That's the experiment.

See the [editorial policy](policy.md) for scope, limitations, and how to contest
a review.
