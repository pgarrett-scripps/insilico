# Development

Everything needed to run the site or the review pipeline yourself. Authors do not
need any of this. See [`submit.md`](submit.md) instead.

## How the repo fits together

One idea explains the layout: **Python writes the record, Astro renders it.** The
pipeline writes documents and one JSON file per review. The site reads
`docs/reviews/` in place and builds every page from it, so changing how a review
looks never means touching the program that produces one.

```
docs/                     # the record, written by the pipeline
├── policy.md  criteria.md  submit.md  development.md
└── reviews/<year>/<slug>/v<N>/r<M>/ # manuscript draft, then review attempt
    ├── provenance.json   # verdict, models, code and configuration fingerprints
    ├── manifest.json     # SHA-256 for every published artifact
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
there to design against. No fixtures or seeding are needed. `npm run build` writes to
`dist/`.

Everything visual is a token in `src/styles/global.css`, redefined for light and
dark. Change a token and it moves everywhere it is used.

## Editor commands

Editors have one command, written as a comment on the submission issue. Only
owners, members and collaborators can trigger it.

| Command | What happens |
|---|---|
| `/review` | reviews whatever draft the archive serves now |
| `/review replace` | adds an independent review attempt for the same draft |
| `/review openrouter vendor/model` | every agent uses that one named model against the paid budget |

Whether a run is a first look or a revision round is not something an editor
declares. The archive version selects `v<N>`. A same-draft re-review requires
`replace` and creates the next `r<M>`. The command name is retained for
compatibility, but no published attempt is replaced.

A review run on a single model says so on its page: one model wrote all of it,
and nothing checked the referees that was any better than the referees.

## Running a review locally

`requirements.txt` deliberately does not pin the referee panel. The workflow pins
it per run to an exact commit, so every review records the code that produced it.
Install it separately:

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install "peerreviewagents[research] @ git+https://github.com/pgarrett-scripps/PeerReviewAgents.git"

export ANTHROPIC_API_KEY=...
python scripts/run_review.py --url https://arxiv.org/abs/2401.12345
```

`v<N>` is the draft the archive served, not a count of our runs. `v3` is the
authors' third draft. `r<M>` is our attempt number for that exact draft. A
second independent read of draft 3 is `v3/r2`, while the first review of draft
4 is `v4/r1`.

The newest eligible editorial attempt on the newest earlier draft is the
baseline for a revision. A single-model experiment stays public but cannot set
the paper's status or become the baseline for the next draft. The revision
pipeline receives that selected bundle through its existing `revision_of`
input, which activates the built-in compliance comparison.

- `--dry-run` resolves the URL and downloads the PDF without calling a model. It
  does not check the PDF has extractable text, so a scanned paper passes this and
  fails later.
- **Local runs do not publish.** The bundle lands in `runs/` (git-ignored) and
  the comparison is printed. Pass `--publish` to write into `docs/reviews/`,
  which is what the workflow does. A run made to see what a prompt change did
  is a question about the pipeline, and answering it should not add a review to
  someone's paper.
- `--replace` re-reviews a draft that already has a review. It creates the next
  immutable attempt and keeps every earlier attempt. If the authors have posted
  a new version, the draft number differs and the run becomes a revision round.
- `--provider openrouter --model <cheap-model>` routes a run through a cheap
  model on a personal key. Use this for prompt work rather than editing
  `peerreview.toml`.

`python scripts/smoke_test.py` checks the contract between the pipeline and the
site. No network, no API key. CI runs it alongside a build that fails if a
published bundle goes unrendered.

## Configuration

Model selection lives in [`peerreview.toml`](../peerreview.toml), not in the
workflow, which passes no model flags on purpose. Anything on the command line
would override that file and collapse every stage onto one model.

Read the comments in that file first. Its layout matters: a top-level key written
below a `[table]` header silently becomes part of that table.

The panel is held to In Silico's own profile in
[`journals/insilico.toml`](../journals/insilico.toml). Each review records the
exact PeerReviewAgents commit, the In Silico commit, a hash of the journal
profile, and the resolved semantic configuration with its hash. The
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

The model name is required and always will be. OpenRouter's free tier is a
rotating set of specific models, not a stable alias.

`parse_command` in `run_review.py` does the parsing, never the workflow. An issue
comment is untrusted text, and the parser accepts only known provider names and
model slugs matching a strict pattern.

## Manuscript text hierarchy

`run_review.py` prefers the archive's official full text. The order is JATS XML,
archive HTML, validated PDF conversion, then OCR. Every candidate must contain
the archive title and abstract and clear minimum length checks before a model
sees it. The selected source and validation result are recorded in provenance.

JATS and HTML headings are source structure. PDF and OCR section guesses do not
control prompt assembly. Every reviewer receives the complete selected text.

The PDF converter is
[rustypaper](https://github.com/pgarrett-scripps/rustypaper), a per-platform
wheel with no Rust toolchain to install. The workflow pins its exact version.
OCR uses Poppler and Tesseract and runs only when the PDF conversion fails
validation.

```bash
uv pip install rustypaper
```

Every representation is measured deterministically and with no model:

| verdict | what happens |
|---|---|
| clean | nothing. No warning appears anywhere. |
| degraded | the run proceeds, the panel is told what the converter mangled, and the review page carries a note |
| broken | the runner tries the next source, then stops before review if none pass |

A final stop is a technical failure, never a desk rejection. The workflow exits
3, posts a note on the issue, and opens no pull request.

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
two serial steps, the same wall-clock depth the old sequential single round
had. A synthesizer then condenses the exchange into the record the editor reads
in place of the raw transcript.

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
