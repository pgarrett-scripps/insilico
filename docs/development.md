# Development

Everything needed to run the site or the review pipeline yourself. Authors do not
need any of this; see [`submit.md`](submit.md) instead.

## How the repo fits together

One idea explains the layout: **Python writes the record, Astro renders it.** The
pipeline writes documents and one JSON file per review. The site reads
`docs/reviews/` in place and builds every page from it, so changing how a review
looks never means touching the program that produces one.

```
docs/                     # the record, written by the pipeline
├── policy.md  criteria.md  submit.md  development.md
└── reviews/<year>/<slug>/v<N>/     # our review of the authors' Nth draft
    ├── provenance.json   # verdict, scores, models, cost, PDF fingerprint
    ├── round.json        # machine-readable record a later round rules on
    ├── summary.md  decision_letter.md  desk_screen.md
    ├── debate_transcript.md  journal_recommendations.md
    ├── manuscript_stats.md   # deterministic counts over the text the panel read
    ├── review_*.md       # 5 specialist reports
    └── audit_*.md        # 2 audits, 3 in a revision round

src/                      # the site
├── lib/corpus.js         # walks docs/reviews/ into what pages render
├── layouts/Base.astro    # shell, theme toggle, header, footer
├── components/           # PanelReadout, Notices, Provenance, Citation
├── pages/                # home, the review list, every review page
└── styles/global.css     # the visual system, as tokens

scripts/
├── fetch_preprint.py     # URL to PDF and metadata
├── preview_submission.py # issue metadata and editor command preview
├── run_review.py         # fetch, review, write the bundle
├── check_updates.py      # find reviews whose preprint has changed since
├── smoke_test.py         # the pipeline/site data contract, offline
└── _pinned_review.py     # test helper: review a named version, not the latest

.github/workflows/
├── submission-preview.yml # metadata preview on new or edited submissions
├── review.yml            # /review, opens a review PR
├── ci.yml                # checks the data contract and that the site builds
├── publish.yml           # builds and deploys on merge
└── check-updates.yml     # monthly sweep for stale reviews
```

Pages are generated from `provenance.json`, so a review bundle is the only source
of truth and there is no index to keep in step.

## Submission previews

Opening or editing an issue with the `submission` label runs
`submission-preview.yml`. The workflow resolves public archive metadata without
downloading the PDF or calling a model. It then creates or updates one bot
comment. The comment reports the title, authors, posting date, current draft,
and any published In Silico drafts. It also recommends `/review`, `/review
replace`, or a revision round based on the archive version and the bundles
already in `docs/reviews/`.

The comment carries a hidden marker, so an edit refreshes the existing comment
instead of adding another. The issue body is untrusted input. It reaches Python
through an environment variable, and the existing preprint resolver accepts
only arXiv, bioRxiv, and medRxiv identifiers.

## Working on the site

```bash
npm install
npm run dev      # http://localhost:4321/insilico/
```

The dev server reads `docs/reviews/` directly, so the whole published corpus is
there to design against — no fixtures, no seeding. `npm run build` writes to
`dist/`.

Everything visual is a token in `src/styles/global.css`, redefined for light and
dark. Change a token and it moves everywhere it is used.

## Editor commands

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

## Running a review locally

`requirements.txt` deliberately does not pin the referee panel; the workflow pins
it per run to an exact commit, so every review records the code that produced it.
Install it separately:

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install "peerreviewagents[research] @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

`v<N>` is the draft the archive served, not a count of our runs — `v3` is our
review of the authors' third draft. `resolve()` always reports the current
draft and refuses to go backwards, so the number only ever increases and folder
order can never disagree with the order the drafts were written in.

- `--dry-run` resolves the URL and downloads the PDF without calling a model. It
  does not check the PDF has extractable text, so a scanned paper passes this and
  fails later.
- **Local runs do not publish.** The bundle lands in `runs/` (git-ignored) and
  the comparison is printed. Pass `--publish` to write into `docs/reviews/`,
  which is what the workflow does. A run made to see what a prompt change did
  is a question about the pipeline, and answering it should not add a review to
  someone's paper.
- `--replace` re-reviews a draft that already has a review, overwriting it. It
  can only ever hit a review of the *same* draft: if the authors have posted a
  new version since, the draft number differs and you get a new round instead.
- `--provider openrouter --model <cheap-model>` routes a run through a cheap
  model on a personal key. Use this for prompt work rather than editing
  `peerreview.toml`.

`python scripts/smoke_test.py` checks the contract between the pipeline and the
site. No network, no API key. CI runs it alongside a build that fails if a
published bundle goes unrendered.

## Configuration

Model selection lives in [`peerreview.toml`](../peerreview.toml), not in the
workflow, which passes no model flags on purpose — anything on the command line
would override that file and collapse every stage onto one model.

Read the comments in that file first. Its layout matters: a top-level key written
below a `[table]` header silently becomes part of that table.

The panel is held to In Silico's own profile in
[`journals/insilico.toml`](../journals/insilico.toml). Each review records the
exact pipeline commit in `provenance.json`, so the
[DOI](https://doi.org/10.5281/zenodo.21781895) identifies the software and the
sha identifies the run.

### Running on one model instead of the split

`/review openrouter vendor/model` on the issue, or `--provider openrouter
--model vendor/model` locally, runs every agent on that one model. Needs
`OPENROUTER_API_KEY` in repository secrets.

Naming a model **clears the `[models]` and `[agent_models]` tables**. Those
tables beat `reasoning_model`, so leaving them in place would send every agent to
OpenRouter asking for `claude-haiku-4-5`: the model you named would review
nothing, and the run would either fail strangely or bill someone for Claude.

The model name is required and always will be — OpenRouter's free tier is a
rotating set of specific models, not a stable alias.

`parse_command` in `run_review.py` does the parsing, never the workflow. An issue
comment is untrusted text, and the parser accepts only known provider names and
model slugs matching a strict pattern.

## The PDF converter

`run_review.py` hands the pipeline the PDF itself, never a conversion of it.
Every run records which converter read the manuscript, and a conversion done
here would be recorded as though the pipeline's own converter produced it.

Behind the loader the PDF becomes markdown, and that is what the referees read.
The converter is [rustypaper](https://github.com/pgarrett-scripps/rustypaper), a
per-platform wheel with no Rust toolchain to install. It is required and has no
fallback: one that will not install stops the run rather than quietly degrading
it. The workflow pins an exact version, and the pin is what `replace` rests on:
a rerun proves it is reading the same draft by comparing the converted text
against the previous run's, so a converter that changed how it reads a
two-column page would refuse the correct draft. It is also what makes
`manuscript_stats.md` comparable between two reviews of one paper.

```bash
uv pip install rustypaper
```

Every conversion is measured, deterministically and with no model:

| verdict | what happens |
|---|---|
| clean | nothing. No warning appears anywhere. |
| degraded | the run proceeds, the panel is told what the converter mangled, and the review page carries a note |
| broken | the run stops at the desk before a referee is paid, and nothing is published |

A stop raises `ManuscriptUnreadable` rather than desk-rejecting. A desk rejection
is a verdict on a manuscript and gets a published bundle; this is a fact about a
file and gets none. The workflow exits 3, posts a note on the issue, and opens no
pull request. `conversion_gate = "off"` in `peerreview.toml` reviews the file
anyway.

The measurements go to `manuscript_stats.md` and into `provenance.json` under
`ingest.prose`. They reach no prompt: an agent handed "8.4 boosters per 1000
words" writes a finding about it.

`PEERREVIEW_CAVEMAN` controls telegraphic compression and defaults to `off`. It
saves under a cent a review and it is not free. Under `light`, the old
eight-role panel's clarity reviewer reported grammatical errors three times on
a paper where the uncompressed run reported none, having read the compressor's
work as the authors' writing.

## Cost

A full round is 15 model calls when venue suggestions are enabled. The main
lever is the per-tag model split in `peerreview.toml`: the widest fan-out on the
cheapest tier, the debate in the middle, and only the agent that decides the
verdict on the most expensive one.

`debate_rounds` is 2, and the advocate and skeptic argue in parallel within
each round: two blind opening cases in round 1, two rebuttals in round 2 after
each side reads the other. Because the rounds are parallel, two rounds cost
two serial steps — the same wall-clock depth the old sequential single round
had — and a synthesizer then condenses the exchange into the record the
editor reads in place of the raw transcript.

Every review records its own per-agent spend in `provenance.json`. A desk
rejection ends the run before the other 14.

## First-time setup

- [ ] Add `ANTHROPIC_API_KEY` to repository secrets
- [ ] Settings, Pages, Source: **GitHub Actions**
- [ ] Settings, Actions, Workflow permissions: **Read and write**, and allow PR
      creation
- [ ] Set `site` and `base` in [`astro.config.mjs`](../astro.config.mjs) to match
      where the site is served from
- [ ] Check the model split in [`peerreview.toml`](../peerreview.toml)
