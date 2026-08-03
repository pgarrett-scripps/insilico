# In Silico

**An open, AI-refereed overlay journal. Any field, and the whole review is published.**

In Silico does not host papers. You send us a link to a preprint that already
exists on arXiv, bioRxiv or medRxiv. We run it through a panel of AI referees and
publish the entire review next to a pointer to your paper.

The review is the point. Eight specialist reviewers, two audits, a debate, an
area chair and an editor, all published in full.

> **This is an experiment.** The AI panel only advises. A human editor makes
> every decision, and no automated verdict is final. Read these reviews as a
> machine-generated second opinion, not as a stamp of approval.

**[Read the reviews →](https://pgarrett-scripps.github.io/insilico/reviews/)**

## Submitting a paper

You do not need to know how to code. You do need a free GitHub account.

1. [Open a submission issue](../../issues/new?template=submit.yml) and paste your
   preprint link.
2. An editor starts the panel. This usually takes under an hour once started.
3. The review appears as a pull request. Read it, and reply in the thread if you
   disagree. A human editor reads your reply. No AI does.

Anyone can submit any public preprint, including one they did not write. The form
asks whether you are an author, and every review says which it was, so a review
nobody asked for cannot be mistaken for one the authors requested.

Full details for authors: [`docs/submit.md`](docs/submit.md).

## What we review

Original research in any field. What matters is whether the evidence can be
checked, not what the paper is about. An unsupported claim in a lab paper is as
findable as one in a simulation. The name describes how we review, not what we
review.

We do not review work where a wrong machine-generated review could affect
patient care. See [`docs/policy.md`](docs/policy.md#scope).

Links must be to arXiv, bioRxiv or medRxiv. Those give us a DOI and a version
number, so a review names an exact draft. A bare PDF link can change or go dead,
so we reject those.

## How a review happens

```
  anyone opens a submission issue
             ↓
  an editor comments  /review
             ↓
  a GitHub Action fetches the preprint and runs the panel
             ↓
  a bot opens a pull request with the full review
             ↓
  editor merges  → published
  editor closes  → declined, nothing published
```

Merging is what publishes a review. It means the review is now public, not that
anyone endorses what the panel recommended.

Editors have two commands, both written as a comment on the submission issue:

| Command | Use it when | What happens |
|---|---|---|
| `/review` | first look at a preprint | a fresh round 1 |
| `/revise` | the authors changed the paper | referees rule on what changed |

Only owners, members and collaborators can trigger either.

## What authors cannot do

Nothing an author writes reaches the panel. There is no appeal command and no
response letter. A review that authors can talk their way out of is one they can
change without changing the paper, and we watched that happen when we tried it.

If you think a review is wrong, you can get a published right of reply, ask an
editor to withdraw it, or ask for a fresh review of a new draft.
See [`docs/policy.md`](docs/policy.md#contesting-a-review).

## Reading a review

Every review is one folder per version of a paper, published under
`docs/reviews/`. A later review sits **beside** the one before it rather than
replacing it, so `v1` stays exactly as it was and the paper's page lists both.

Each folder holds the editor's decision letter, the eight specialist reports,
the audits, the debate, and a `provenance.json` recording the verdict, the panel
scores, which models ran, and what it cost. Anyone can check out the commit a
review names and see exactly what the panel was told to do.

There is also a `manuscript_stats.md` with no opinion in it at all: counts over
the text the panel read, so a reader holding the PDF can check the panel read
the same document.

## Documentation

| | |
|---|---|
| [`docs/submit.md`](docs/submit.md) | how to submit, and what to expect |
| [`docs/criteria.md`](docs/criteria.md) | what the panel looks for |
| [`docs/policy.md`](docs/policy.md) | editorial policy, limitations, how to contest a review |
| [`docs/development.md`](docs/development.md) | running the site or the pipeline yourself |

## License

Reviews and site content are CC BY 4.0. Scripts and workflows are MIT. See
[`LICENSE`](LICENSE). Preprints stay under whatever license their authors chose,
since we host none of them.

The referee panel is [PeerReviewAgents][pra].

[pra]: https://github.com/pgarrett-scripps/PeerReviewAgents
