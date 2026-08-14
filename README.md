# In Silico

**An open, AI-refereed overlay journal. Any field, and the whole review is published.**

In Silico does not host papers. You send us a link to a preprint that already
exists on arXiv, bioRxiv or medRxiv. We run it through a panel of AI referees —
eight specialist reviewers, two audits, a debate and an editor —
and publish the entire review next to a pointer to your paper.

> **This is an experiment.** The verdict on every paper here was produced by a
> language model, not a person. A human decides only whether a review gets
> published, never what it says.

**[Read the reviews →](https://pgarrett-scripps.github.io/insilico/reviews/)**

## Submitting a paper

You do not need to know how to code. You do need a free GitHub account.

1. [Open a submission issue](../../issues/new?template=submit.yml) and paste your
   preprint link.
2. An editor starts the panel.
3. The review appears as a pull request. Reply in the thread if you disagree.
   A human editor reads your reply; no AI does.

Anyone can submit any public preprint, including one they did not write. The form
asks whether you are an author, and every review says which it was.

Nothing an author writes reaches the panel — no appeal command, no response
letter ([why](docs/submit.md#why-we-do-not-accept-a-response-letter)). If a
review misreads your paper, say so on the issue and we take it down. If your
paper has changed, ask for a fresh review of the new draft.

Full details: [`docs/submit.md`](docs/submit.md).

## What we review

Original research in any field. What matters is whether the evidence can be
checked, not what the paper is about — the name describes how we review, not
what we review. We do not review work where a wrong machine-generated review
could affect patient care ([scope](docs/policy.md#scope)).

Links must be to arXiv, bioRxiv or medRxiv, so a review names an exact draft.

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

In Silico **accepts** a paper the panel returns at accept or minor revision, and
**declines** the rest. The editor is not told this rule — it recommends one of
the four standard verdicts, and the line is drawn afterwards
([why](docs/policy.md#what-acceptance-means)).

Editors have one command, written as a comment on the submission issue. Only
owners, members and collaborators can trigger it.

| Command | What happens |
|---|---|
| `/review` | reviews whatever draft the archive serves now |
| `/review replace` | redoes a draft already reviewed, overwriting it |
| `/review openrouter vendor/model` | the paid budget is spent — that one named model, for every agent |

Whether a run is a first look or a new round is not something an editor
declares. A bundle is named after the draft it read, so a draft we have not
reviewed is a new round and one we have needs `replace` said out loud before
anything is overwritten.

A review run on a single model says so on its page: one model wrote all of it,
and nothing checked the referees that was any better than the referees.

## Reading a review

Each review is one folder per draft of a paper under `docs/reviews/`, holding
the editor's decision letter, the eight specialist reports, the audits, the
debate, and a `provenance.json` recording the verdict, panel scores, models and
cost. A later review sits **beside** the one before it rather than replacing it.

There is also a `manuscript_stats.md` with no opinion in it at all: counts over
the text the panel read, so a reader holding the PDF can check the panel read the
same document.

## What a review costs

About **$0.08 a paper** on the current setup (`deepseek/deepseek-v4-flash-0731`
for every agent), including the live literature searches; the graded
multi-model panel in `peerreview.toml` runs ~$3.40. Every review records its
own bill in `provenance.json`, and reviews are judged against In Silico's own
criteria ([`journals/insilico.toml`](journals/insilico.toml)).

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

The referee panel is [PeerReviewAgents][pra], archived at
[10.5281/zenodo.21781895](https://doi.org/10.5281/zenodo.21781895).

[pra]: https://github.com/pgarrett-scripps/PeerReviewAgents
