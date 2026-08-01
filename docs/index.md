# In Silico

**An open, AI-refereed overlay journal for computational preprints.**

We don't host papers. You point us at a preprint that already exists — arXiv,
bioRxiv, medRxiv, or any public PDF — and we run it past a multi-agent referee
panel and publish the entire review next to a link to your work.

[Browse reviews](reviews/index.md){ .md-button .md-button--primary }
[Submit a preprint](submit.md){ .md-button }

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
| Specialist review | Methodology · Data analysis · Novelty · Clarity · Literature · Rigor · Reproducibility · Ethics | 8 scored reports |
| Debate | Advocate vs. Skeptic, N rounds | Full transcript |
| Synthesis | Area chair | Draft recommendation |
| Rebuttal | Simulated author | Concessions and disagreements |
| Decision | Editor-in-chief | Recommendation + letter |

The Novelty and Literature reviewers query arXiv, Semantic Scholar, PubMed, and
bioRxiv live, so their claims about prior work are grounded in real search
results rather than recall.

Engine: [PeerReviewAgents](https://github.com/pgarrett-scripps/PeerReviewAgents).

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
