# In Silico

**An open, AI-refereed overlay journal. Any field; the whole review published.**

In Silico does not host manuscripts. You submit a link to a preprint that already
exists — arXiv, bioRxiv, medRxiv, or any public PDF — and we run it through a
multi-agent referee panel ([PeerReviewAgents][pra]) and publish the **full
review** alongside a pointer to your paper.

The review is the artifact. Eight specialist reviewers, an advocate/skeptic
debate, an area chair, a simulated author rebuttal, and an editor-in-chief
verdict — all of it published, all of it reproducible.

> **This is an experiment.** The referee panel is advisory. A human editor makes
> every accept/decline call, and no automated verdict is ever final. Treat these
> reviews as a machine-generated second opinion, not as certification.

## How it works

```
  author opens a submission issue
             │
             ▼
  editor comments  /review
             │
             ▼
  GitHub Action: fetch preprint → run the 14-agent panel
             │
             ▼
  bot opens a PR containing the full review bundle
             │
             ├── editor merges  → listed in the journal
             └── editor closes  → declined, review not published
```

Merging the review PR *is* the acceptance. There is no other ceremony.

## Submitting

1. Open a [submission issue](../../issues/new?template=submit.yml) with your
   preprint URL.
2. Wait for an editor to trigger the panel.
3. Read the review on the PR. Respond in the thread if you disagree — the editor
   reads rebuttals before deciding.

Full policy: [`docs/policy.md`](docs/policy.md).

## What we consider

Computational and *in silico* work, broadly: simulation, modeling, method
papers, benchmarks, reanalyses, and scientific software. Anything where the
claims can be checked by reading the paper and the code.

We do **not** consider clinical trials, wet-lab-only work, or anything where the
central evidence is data a referee cannot inspect.

## Repository layout

```
docs/
├── index.md              # journal front page
├── policy.md             # editorial policy + limitations
├── submit.md             # author guide
└── reviews/
    ├── index.md          # generated index of published reviews
    └── <year>/<slug>/
        ├── index.md      # verdict + metadata + links (YAML frontmatter)
        ├── provenance.json   # model, config, pipeline SHA, cost
        ├── summary.md
        ├── decision_letter.md
        ├── meta_review.md
        ├── author_rebuttal.md
        ├── debate_transcript.md
        ├── journal_recommendations.md
        └── review_*.md   # 8 specialist reports

scripts/
├── fetch_preprint.py     # URL → PDF + metadata (arXiv / bioRxiv / medRxiv / raw)
├── run_review.py         # fetch → review → publish bundle
├── build_index.py        # regenerate docs/reviews/index.md
└── smoke_test.py         # render fixtures, no API key needed

.github/workflows/
├── review.yml            # /review slash command → opens a review PR
├── ci.yml                # PR check: fixtures render, index fresh, site builds
└── publish.yml           # build + deploy the site on merge
```

## Running a review locally

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
python scripts/build_index.py
```

Add `--dry-run` to fetch and resolve metadata without spending any tokens.

## Setup checklist

Before the first real submission:

- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Settings → Pages → Source: **GitHub Actions**
- [ ] Settings → Actions → Workflow permissions: **Read and write** + allow PR creation
- [ ] Edit `mkdocs.yml` `site_url` / `repo_url` to point at the real repo
- [ ] Decide the model in `.github/workflows/review.yml` (cost note below)

## Cost

A full panel is 14 agents plus a debate loop — roughly 20+ model calls over the
manuscript text. On a frontier model that is dollars, not cents, per paper.
`REVIEW_MODEL` in the workflow is the knob; drop `--debate-rounds` to 1 to cut
the largest variable chunk.

## License

Reviews and site content are CC BY 4.0; scripts and workflows are MIT. See
[`LICENSE`](LICENSE). Submitted preprints remain under whatever license their
authors chose — we host none of them.

[pra]: https://github.com/pgarrett-scripps/PeerReviewAgents
