# In Silico

**An open, AI-refereed overlay journal. Any field; the whole review published.**

In Silico does not host manuscripts. You submit a link to a preprint that already
exists — arXiv, bioRxiv or medRxiv — and we run it through a multi-agent referee
panel ([PeerReviewAgents][pra]) and publish the **full review** alongside a
pointer to your paper.

The review is the artifact. Eight specialist reviewers, two editorial audits, an
advocate/skeptic debate, an area chair, a simulated author rebuttal, and an
editor-in-chief verdict — all of it published, all of it reproducible down to the
model id.

> **This is an experiment.** The referee panel is advisory. A human editor makes
> every accept/decline call, and no automated verdict is ever final. Treat these
> reviews as a machine-generated second opinion, not as certification.

## How it works

```
  anyone opens a submission issue
             │
             ▼
  editor comments  /review
             │
             ▼
  GitHub Action: fetch preprint → run the 17-agent panel
             │
             ▼
  bot opens a PR containing the full review bundle
             │
             ├── editor merges  → published and listed
             └── editor closes  → declined, review not published
```

Merging the review pull request is what publishes it. There is no other step —
and it means the review is public, not that the panel's recommendation has been
endorsed.

Two follow-up commands continue an existing record:

| Command | Means | Effect |
|---|---|---|
| `/review <url>` | review this preprint | a fresh round 1 |
| `/revise [letter-url]` | the **manuscript** changed | next round; referees rule on the delta, an auditor checks the previous letter's required revisions |
| `/appeal <comment-url> [reviewers]` | the **review** is wrong, the manuscript is unchanged | a correction at the same round number; named referees re-run |

Both need the previous round to have left a `round.json` in its bundle, which is
what a later round is pointed at. Reviews published before round records existed
cannot be revised — re-review the current draft as a fresh round instead.

## Submitting

1. Open a [submission issue](../../issues/new?template=submit.yml) with your
   preprint URL.
2. Wait for an editor to trigger the panel.
3. Read the review on the PR. Respond in the thread if you disagree — the editor
   reads rebuttals before deciding.

Anyone may submit any public preprint, including one they did not write. The form
asks whether you are an author and every published review states the answer, so a
review the authors never asked for cannot be mistaken for one they did.

Full policy: [`docs/policy.md`](docs/policy.md).

## What we consider

Any original research manuscript, in any discipline. What decides whether a paper
belongs here is not its field but whether its evidence can be inspected — an
unsupported inference in a wet-lab paper is exactly as findable as one in a
simulation. The name describes how the reviewing is done, not what may be
reviewed.

The one hard exclusion is work where a wrong machine-generated review could
affect patient care. See [`docs/policy.md`](docs/policy.md#scope).

Submissions must come from arXiv, bioRxiv or medRxiv. Those give a DOI and a
version number to anchor a review to; a loose PDF link names no particular
revision, carries no metadata, and can go dead — so direct PDF URLs are rejected.

## Repository layout

```
docs/
├── index.md              # journal front page
├── policy.md             # editorial policy + limitations
├── criteria.md           # what the panel looks for
├── submit.md             # author guide
└── reviews/
    ├── index.md          # generated index of published reviews
    ├── index.json        # the same corpus, machine-readable
    └── <year>/<slug>/
        ├── index.md      # the paper page: every review it has received
        └── v<N>/         # one immutable review of one revision
            ├── index.md          # verdict + metadata + links (YAML frontmatter)
            ├── provenance.json   # models, config, pipeline SHA, per-agent cost
            ├── round.json        # machine-readable record a later round rules on
            ├── summary.md
            ├── decision_letter.md
            ├── desk_screen.md         # only when the desk found something
            ├── integrity.md           #   ditto — the injection scan
            ├── author_response.md     # revisions/appeals: the letter, verbatim
            ├── meta_review.md
            ├── author_rebuttal.md
            ├── debate_transcript.md
            ├── journal_recommendations.md
            ├── review_*.md   # 8 specialist reports
            └── audit_*.md    # 2 editorial audits

scripts/
├── fetch_preprint.py     # URL → PDF + metadata (arXiv / bioRxiv / medRxiv)
├── run_review.py         # fetch → review → publish bundle
├── build_index.py        # regenerate docs/reviews/index.{md,json}
├── check_updates.py      # find reviews whose preprint has since changed
└── smoke_test.py         # render fixtures; no network, no API key

.github/workflows/
├── review.yml            # /review, /revise, /appeal → opens a review PR
├── ci.yml                # PR check: fixtures render, index fresh, site builds
├── publish.yml           # build + deploy the site on merge
└── check-updates.yml     # monthly staleness sweep → files a tracking issue
```

A re-review is published **beside** the review it supersedes, never on top of it:
`v1` stays exactly as it was, and the paper page lists both. Earlier reviews are
the record of what the panel said about that revision.

## Configuration

Model selection lives in [`peerreview.toml`](peerreview.toml), not in the
workflow. The action deliberately passes no model flags, because anything on the
command line would override that file and collapse every stage back onto a single
model. Read the comments there before changing it — the file's layout is
load-bearing, since a top-level key written below a `[table]` header silently
becomes part of that table.

The panel is held to In Silico's own review profile in
[`journals/insilico.toml`](journals/insilico.toml), version-controlled next to
the reviews it produced, so anyone reading a review can check out the commit it
names and see what the panel was told to weigh.

## Running a review locally

`requirements.txt` covers the site build and the scripts, but deliberately does
**not** pin the referee panel — the workflow pins that per-run to an exact SHA so
each review records which code produced it. Install it separately:

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install "peerreviewagents @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
python scripts/build_index.py
```

`--dry-run` resolves the URL and downloads the PDF without calling a model, so
you can check a link is reviewable before spending anything. It does not check
that the PDF has extractable text; a scanned manuscript passes `--dry-run` and
fails later during ingestion.

For iterating on prompts, override the provider per run rather than editing
`peerreview.toml`, which routes through a cheap model on a personal key:

```bash
python scripts/run_review.py --url ... --provider openrouter --model <cheap-model>
```

`python scripts/smoke_test.py` renders the whole bundle from fixtures. It is
hermetic — no network, no API key — and is what CI runs on every PR.

## Setup checklist

Before the first real submission:

- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Add `PRA_READ_TOKEN` — a fine-grained PAT with **Contents: Read** on
      PeerReviewAgents, needed while that repo is private. Without it the
      workflow fails at the pin step, and GitHub reports a missing permission
      identically to a typo.
- [ ] Settings → Pages → Source: **GitHub Actions**
- [ ] Settings → Actions → Workflow permissions: **Read and write** + allow PR creation
- [ ] Edit `mkdocs.yml` `site_url` / `repo_url` to point at the real repo
- [ ] Review the model split in [`peerreview.toml`](peerreview.toml) (cost note below)

## Cost

A full round is 17 agents — 8 specialist reviewers, 2 auditors, a desk screen, an
advocate/skeptic pair, an area chair, a rebuttal, an editor, and a venue scout —
over the manuscript text. On a frontier model that is dollars, not cents, per
paper.

The main lever is the per-tag model split in `peerreview.toml`: the widest
fan-out and the most checklist-like stages run on Haiku, the debate on Sonnet,
and only the two agents that actually decide the verdict on Opus. `debate_rounds`
is already 1, since a second round re-sends the whole of the first. Every review
records its own per-agent spend in `provenance.json`, so cost decisions can be
made from a breakdown rather than a guess.

A desk rejection short-circuits the run before the other 16 calls.

## License

Reviews and site content are CC BY 4.0; scripts and workflows are MIT. See
[`LICENSE`](LICENSE). Submitted preprints remain under whatever license their
authors chose — we host none of them.

[pra]: https://github.com/pgarrett-scripps/PeerReviewAgents
