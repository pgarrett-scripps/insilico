# Development

Everything needed to run the site or the review pipeline yourself. Authors do not
need any of this; see [`submit.md`](submit.md) instead.

## How the repo fits together

One idea explains the layout: **Python writes the record, Astro renders it.** The
pipeline writes documents and one JSON file per review. The site reads
`docs/reviews/` in place and builds every page from it. Nothing is copied, so
changing how a review looks never means touching the program that produces one.

```
docs/                     # the record, written by the pipeline
├── policy.md             # editorial policy and limitations
├── criteria.md           # what the panel looks for
├── submit.md             # author guide
├── development.md        # this file
└── reviews/<year>/<slug>/v<N>/     # one review of one version
    ├── provenance.json   # verdict, scores, models, cost, PDF fingerprint
    ├── round.json        # machine-readable record a later round rules on
    ├── summary.md
    ├── decision_letter.md
    ├── desk_screen.md
    ├── integrity.md      # only when the hidden-text scan found something
    ├── meta_review.md
    ├── author_rebuttal.md
    ├── debate_transcript.md
    ├── journal_recommendations.md
    ├── manuscript_stats.md   # deterministic counts over the text the panel read
    ├── review_*.md       # 8 specialist reports
    └── audit_*.md        # 2 audits, 3 in a revision round

src/                      # the site
├── lib/corpus.js         # walks docs/reviews/ into what pages render
├── layouts/Base.astro    # shell, theme toggle, header, footer
├── components/           # PanelReadout, Notices, Provenance, Citation
├── pages/                # home, the review list, every review page
└── styles/global.css     # the visual system, as tokens

scripts/
├── fetch_preprint.py     # URL to PDF and metadata
├── run_review.py         # fetch, review, write the bundle
├── check_updates.py      # find reviews whose preprint has changed since
├── smoke_test.py         # the pipeline/site data contract, offline
└── _pinned_review.py     # test helper: review a named version, not the latest

.github/workflows/
├── review.yml            # /review and /revise, opens a review PR
├── ci.yml                # checks the data contract and that the site builds
├── publish.yml           # builds and deploys on merge
└── check-updates.yml     # monthly sweep for stale reviews
```

Pages are generated from `provenance.json`, so a review bundle is the only source
of truth and there is no index to keep in step.

## Working on the site

```bash
npm install
npm run dev      # http://localhost:4321/insilico/
```

The dev server reads `docs/reviews/` directly, so the whole published corpus is
there to design against. No fixtures, no seeding. `npm run build` writes to
`dist/`.

Everything visual lives in `src/styles/global.css` as tokens, redefined for light
and dark. Change a token and it moves everywhere it is used.

## Running a review locally

`requirements.txt` covers the scripts but deliberately does not pin the referee
panel, because the workflow pins that per run to an exact commit so every review
records the code that produced it. Install it separately:

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install "peerreviewagents[research] @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

PeerReviewAgents is private and not on PyPI, so that second install needs an
account with read access.

The bundle lands under `docs/reviews/<year>/<slug>/v<N>/` and the site picks it up
on the next build.

Useful flags:

- `--dry-run` resolves the URL and downloads the PDF without calling a model, so
  you can check a link works before spending anything. It does not check that the
  PDF has extractable text, so a scanned paper passes this and fails later.
- `--provider openrouter --model <cheap-model>` routes a run through a cheap model
  on a personal key. Use this for prompt work rather than editing
  `peerreview.toml`.

`python scripts/smoke_test.py` checks the contract between the pipeline and the
site. It needs no network and no API key, and CI runs it alongside a build that
fails if a published bundle goes unrendered.

## Configuration

Model selection lives in [`peerreview.toml`](../peerreview.toml), not in the
workflow, which passes no model flags on purpose. Anything on the command line
would override that file and collapse every stage onto one model.

Read the comments in that file before changing it. Its layout matters: a
top-level key written below a `[table]` header silently becomes part of that
table.

The panel is held to In Silico's own profile in
[`journals/insilico.toml`](../journals/insilico.toml), version-controlled next to
the reviews it produced.

## The PDF converter

`run_review.py` hands the pipeline the PDF itself, never a conversion of it. The
integrity screen dispatches on file type, and only its PDF path can find text
hidden inside a content stream. Give it a `.md` and the screen reports as having
run while looking for something it cannot find.

Behind the loader the PDF becomes markdown, and that is what the referees read.
The converter is [rustypaper](https://github.com/pgarrett-scripps/rustypaper). It
is required and has no fallback: one that will not install stops the run rather
than quietly degrading it. It ships as a per-platform wheel, so there is no Rust
toolchain to install.

```bash
uv pip install rustypaper
```

The workflow pins an exact version rather than letting it float, because a
converter that changed how it reads a two-column page between two rounds of the
same paper would look like the authors having rewritten it.

Every conversion is measured, deterministically and with no model, and the
result decides three things:

| verdict | what happens |
|---|---|
| clean | nothing. No warning appears anywhere. |
| degraded | the run proceeds, the panel is told what the converter mangled, and the review page carries a note |
| broken | the run stops at the desk before a referee is paid, and nothing is published |

A stop raises `ManuscriptUnreadable` rather than desk-rejecting, and the
difference matters: a desk rejection is a verdict on a manuscript and gets a
published bundle, while this is a fact about a file and gets none. The workflow
exits 3, posts a note on the issue, and opens no pull request. Set
`conversion_gate = "off"` in `peerreview.toml` to review a file anyway.

The measurements go to `manuscript_stats.md` and into `provenance.json` under
`ingest.prose`. The counts and prose statistics reach no prompt, on purpose:
they measure style, the reviewers already carry more checklist than they can
attend to, and an agent handed "8.4 boosters per 1000 words" writes a finding
about it. They are published for the reader, not fed to the panel.

`PEERREVIEW_CAVEMAN` controls telegraphic compression and defaults to `off`. It
saves under a cent a review, and it is not free: under `light` the clarity
reviewer reported grammatical errors three times on a paper where the
uncompressed run reported none, having read the compressor's work as the authors'
writing.

## Cost

A full round is 19 agents reading the manuscript. On a frontier model that is
dollars per paper, not cents.

The main lever is the per-tag model split in `peerreview.toml`. The widest
fan-out runs on the cheapest tier, the debate on a middle tier, and only the
agent that decides the verdict on the most expensive one.

`debate_rounds` is 2. The second round is the more expensive of the pair, since
it re-sends the whole of the first, and it is kept because one round only gives
the skeptic an unanswered swing. A second lets the advocate answer and the
skeptic judge whether the answer held.

Every review records its own per-agent spend in `provenance.json`, so cost
decisions come from a breakdown rather than a guess. A desk rejection ends the
run before the other 18 calls.

## First-time setup

- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Add `PRA_READ_TOKEN`, a fine-grained token with **Contents: Read** on
      PeerReviewAgents, needed while that repo is private. Without it the workflow
      fails at the pin step, and GitHub reports a missing permission the same way
      it reports a typo.
- [ ] Settings, Pages, Source: **GitHub Actions**
- [ ] Settings, Actions, Workflow permissions: **Read and write**, and allow PR
      creation
- [ ] Set `site` and `base` in [`astro.config.mjs`](../astro.config.mjs) to match
      where the site is served from
- [ ] Check the model split in [`peerreview.toml`](../peerreview.toml)
