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
    ├── provenance.json   # decision, models, code and configuration fingerprints
    ├── manifest.json     # SHA-256 for every published artifact
    ├── round.json        # machine-readable record a later round rules on
    ├── summary.md  decision_letter.md  manuscript_stats.md
    └── (hosted panel only) desk_screen.md  debate_transcript.md
        journal_recommendations.md  review_*.md  audit_*.md

src/                      # the site
├── lib/corpus.js         # walks docs/reviews/ into what pages render
├── layouts/Base.astro    # shell, theme toggle, header, footer
├── components/           # PanelReadout, Notices, Provenance, Citation
├── pages/                # home, the review list, every review page
└── styles/global.css     # the visual system, as tokens

scripts/
├── fetch_preprint.py     # URL to PDF and metadata
├── preview_submission.py # issue metadata and editor command preview
├── local_review.py       # the current route: prepare, then publish a local run
├── run_review.py         # the retired hosted panel, kept so old runs stay readable
├── check_updates.py      # find reviews whose preprint has changed since
├── smoke_test.py         # the pipeline/site data contract, offline
└── _pinned_review.py     # test helper: review a named version, not the latest

.claude/skills/
└── local-review/SKILL.md # how a review is generated, start to finish

.github/workflows/
├── submission-preview.yml # metadata preview on new or edited submissions
├── review.yml            # retired stub, points at the local-review skill
├── ci.yml                # checks the data contract and that the site builds
├── publish.yml           # builds and deploys on merge
└── check-updates.yml     # monthly sweep for stale reviews
```

Pages are generated from `provenance.json`, so a review bundle is the only source
of truth and there is no index to keep in step.

## How a review is made

A review is generated on an editor's own machine and uploaded as a pull request.
Merging that pull request is what publishes it. Nothing publishes a review on its
own, and no paid API key is involved at any point.

The route is the `local-review` project skill, run inside Claude Code from a
checkout of this repository. It drives the PeerReviewAgents engine over the
`claude-code` transport, which shells out to the signed-in `claude` CLI, so the
run is billed to a subscription rather than metered per token. Reaching the
engine is the skill's job. `scripts/local_review.py` does the two parts either
side of it: `prepare` resolves the paper and decides where a review of it
belongs, and `publish` turns a finished run into a bundle the site can render.

Two things about this route are deliberate and show up on every page it
produces.

One model writes the whole review. There is no desk screen, no five-reviewer
panel and no debate round, so nothing checks the reviewer that is any better
than the reviewer. A local review is therefore published as an experiment by
default: public, citable, and unable to set the paper's editorial status or
become the baseline for the next draft. `--baseline-eligible` opts one in, and
that is a decision taken per review.

The decision is a person's. The engine grades findings by severity and
deliberately recommends no verdict, so `--decision` is an operator input that the
record attributes to a human editor. There is no code path that lets the engine
name its own decision, and `provenance.generator.decision_source` is pinned to
`human_editor` by the schema.

### The retired hosted panel

Reviews published before this route ran on a GitHub runner against a paid API
key, as a desk screen, a five-reviewer panel, two audits and a debate. That path
is retired. `.github/workflows/review.yml` is now a manual-only stub that fails
with a pointer here, `scripts/run_review.py` and `peerreview.toml` remain only
so those runs stay reproducible and their pages keep rendering, and the
`ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY` repository secrets are no longer
read by anything.

The sections below marked *retired* describe that path, because fourteen
published reviews came out of it and their records cannot be read without it.

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

An editor no longer triggers a review from the submission issue. The command
preview still appears on new submissions, because it records which draft is
current and whether this repository has reviewed it, but acting on it means
running the `local-review` skill in a checkout.

Whether a run is a first look or a revision round is still not something an
editor declares. The archive version selects `v<N>`. A same-draft re-review
requires `--replace` and creates the next `r<M>`. No published attempt is ever
replaced or edited.

## Running a review

```bash
# Any interpreter with peerreviewagents 0.7 or newer importable.
PY=/path/to/.venv/bin/python

$PY scripts/local_review.py fingerprint
$PY scripts/local_review.py prepare --paper 10.1101/2026.03.12.711120 \
    --out runs/prepared-example
```

`fingerprint` is the preflight. It prints the engine version, a SHA-256 over the
engine's own source tree, and the transport record including the authentication
method and subscription type. It calls no model. If the `claude` CLI turns out
to be authenticated against a paid API provider, it refuses to continue, which
is the check that keeps this path free.

`prepare` resolves the identifier, downloads the exact PDF for that revision,
hashes it, and writes `prepared.json` with the destination, the draft number and
the attempt number. It calls no model either.

`--paper` takes an arXiv id, a bioRxiv or medRxiv DOI, or an archive URL for
either. `--pdf` supplies exact bytes for that identity. A `--pdf` with no
`--paper` can still be reviewed, but the run is marked unpublishable and lands in
`runs/`, because a review has to name the revision it judged and a loose PDF
does not.

Then the engine itself, which is the only part that spends anything, and which
the skill walks through: `confirm-billing`, `import`, `review`, `report`. Read
`REVIEW.md` from the run, decide, and write the bundle:

```bash
$PY scripts/local_review.py publish \
    --prepared runs/prepared-example \
    --run runs/example/run \
    --workspace runs/example/workspace \
    --decision major \
    --editor your-name \
    --human-reviewed yes \
    --publish
```

`publish` writes `summary.md`, `decision_letter.md`, `manuscript_stats.md`,
`editor-package.json`, `round.json`, `provenance.json` and `manifest.json`. It
refuses to overwrite an existing bundle. Without `--publish` the bundle lands
under `runs/rehearsal/`, which is git-ignored: a run made to see what a prompt
change did is a question about the pipeline, and answering it should not add a
review to someone's paper.

`--workspace` is what ties the three steps together. `prepare` hashes the PDF it
fetched, the engine's importer hashes the bytes it was handed, and the run
records the paper id it reviewed. `publish` compares all three and refuses when
they disagree, so a run of one paper cannot be published as a review of another.

`--editor` and `--human-reviewed` have no defaults. The published record carries
an attestation that a named person read the run before it was merged, and that
claim is the operator's to make rather than the script's. Answering
`--human-reviewed no` writes a rehearsal that records the absence instead, and
refuses `--publish`.

Everything in the record about the run itself comes from what the run wrote:
`protocol.json` for the model and the mode, `manifest.json` for the paper id and
the engine's own source fingerprint taken when the call started,
`editor-package.json` for the reviewer count and the synthesis policy,
`progress.json` and the usage receipts for the status and the model ids the
transport actually served. A value the run did not record is left out of the
record rather than filled in from a flag.

Nothing in `publish` writes prose. Every document is rendered from the engine's
saved output, and the reviewer's own words are quoted rather than rewritten.

`requirements.txt` still pins and hashes the production Python environment for
Linux and Python 3.12. Every review records the installed package versions and
lock hash. To update dependencies, edit `requirements.in` and run the compile
command in the header of `requirements.txt`. Review both files together. CI
installs the lock and exercises the runtime without calling a model.

`v<N>` is the draft the archive served, not a count of our runs. `v3` is the
authors' third draft. `r<M>` is our attempt number for that exact draft. A
second independent read of draft 3 is `v3/r2`, while the first review of draft
4 is `v4/r1`.

The newest eligible editorial attempt on the newest earlier draft is the
baseline for a revision. A single-model experiment stays public but cannot set
the paper's status or become the baseline for the next draft, which is why a
local review is experimental unless an editor says otherwise.

- `--replace` on `prepare` allows a new attempt on a draft this repository has
  already reviewed. It creates the next immutable attempt and keeps every
  earlier one. Without it, an already reviewed draft is refused, which is the
  right default. If the authors have posted a new version, the draft number
  differs on its own and no flag is needed.
- `--baseline-eligible` on `publish` lets a local review set the paper's
  editorial status. Off by default.
- `--model` on `publish` records the model id the run requested. `publish` also
  reads the run's own JSON for the model ids actually observed, and the page
  says so if the two disagree.
- `--offline` skips the CLI authentication probe. For tests, not for a real run.

### Checks

```bash
python scripts/smoke_test.py          # pipeline and site data contract
python scripts/check_review_manifests.py
npm run check:schema                  # published provenance against the schema
npm run check:local                   # the local record validates, a paid one does not
npm run check:markdown  npm run check:attempts  npm run build
npm run check:punctuation             # after a build, over dist/
```

None of these touch the network or call a model. `check:local` is the one that
holds this route honest: it asserts that a record admitting a paid API key, or
naming anything but a human as the source of the decision, fails validation, and
that records from the retired panel still pass unchanged. CI runs the lot,
alongside a build that fails if a published bundle goes unrendered.

## Configuration

A local run has very little to configure, which is the point. The transport is
`claude-code`, the model is `claude-sonnet-5-5` or `claude-opus-5-5`, and the
workflow is the engine's own ensemble mode with a reviewer count. Everything
else that used to be a setting is now a property of the engine release, and the
release is identified in the record rather than described.

Each review records the engine package name and version, a SHA-256 over the
engine's source tree, the In Silico commit, the transport and its
authentication method, the model requested, the model ids observed in the run,
and a hash of the exact PDF bytes reviewed. The
[DOI](https://doi.org/10.5281/zenodo.21781895) identifies the software and the
hashes identify the run.

`schemas/review-provenance.schema.json` is the contract. A locally generated
record is `schema_version: 3` and carries a `generator` block. The retired
panel's records are `schema_version: 2`, and records written before versioning
existed are read as they are. All three keep rendering, which is why no
published bundle had to be rewritten for any of this.

### Retired: configuration of the hosted panel

Model selection for the panel lived in [`peerreview.toml`](../peerreview.toml),
and the panel was held to In Silico's own profile in
[`journals/insilico.toml`](../journals/insilico.toml). Both files remain so that
the fourteen reviews published that way stay reproducible. Nothing on the
current path reads either of them.

That path could also route every agent through one named model on OpenRouter.
It needed `OPENROUTER_API_KEY`, which is no longer read. Naming a model cleared
the `[models]` and `[agent_models]` tables, because those tables beat
`reasoning_model` and leaving them in place would have sent every agent to
OpenRouter asking for a Claude alias it does not serve.

## Manuscript text hierarchy

On the current path the engine's own `import` command reads the manuscript. It
takes the PDF `prepare` downloaded and writes a workspace holding the converted
text and the evidence-linked source blocks the reviewer quotes from. Quotations
in a review are validated against those blocks before the run is saved, so a
finding cannot cite a passage the manuscript does not contain.

`publish` measures that workspace with no model and records what the reviewer
was handed: the character count, a hash of the converted text, the block count,
and the importer that produced them. Those numbers go into
`manuscript_stats.md` and into `provenance.json` under `ingest`. They reach no
prompt, because an agent handed "8.4 boosters per 1000 words" writes a finding
about it.

### Retired: the four-source hierarchy

The hosted panel preferred the archive's official full text, in the order JATS
XML, archive HTML, validated PDF conversion, then OCR. Every candidate had to
contain the archive title and abstract and clear minimum length checks before a
model saw it, and the selected source and validation result were recorded in
provenance. JATS and HTML headings were source structure, and PDF or OCR section
guesses did not control prompt assembly.

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

A final stop is a technical failure, never a desk rejection. On the retired
path the workflow exited 3, posted a note on the issue, and opened no pull
request. On the current path the engine command fails, and there is nothing to
hand over.

`PEERREVIEW_CAVEMAN` controls telegraphic compression and defaults to `off`. It
saves under a cent a review and it is not free. Under `light`, the old
eight-role panel's clarity reviewer reported grammatical errors three times on
a paper where the uncompressed run reported none, having read the compressor's
work as the authors' writing.

## Cost

A review costs nothing per run. It is generated on a Claude Code subscription
the editor already pays for, so the price of a review is subscription capacity
and the editor's own time rather than a dollar figure. A local record therefore
reports no cost at all. `total_cost_usd` is `null`, and the schema requires it to
be `null` rather than zero, because a zero would read as a measured free run.

The real limit is the subscription's rate and usage limits. Two reviewers in
ensemble mode is the default for that reason. The engine refuses an existing run
directory, so a retry needs a new folder and never silently doubles a run.

Reviews published on the retired hosted path do carry a per-agent dollar
breakdown in their `provenance.json`, measured at the time. A full round there
was 15 model calls, and a desk rejection ended the run before the other 14.

## First-time setup

- [ ] Sign in to the `claude` CLI on a subscription, then run
      `python scripts/local_review.py fingerprint` and check it reports a
      subscription login and no paid API key. A Claude subscription reports its
      API provider as `firstParty`, which is the subscription route and not a
      paid key
- [ ] Install an interpreter with `peerreviewagents` 0.7 or newer importable
- [ ] Settings, Pages, Source: **GitHub Actions**
- [ ] Settings, Actions, Workflow permissions: **Read and write**, and allow PR
      creation
- [ ] Set `site` and `base` in [`astro.config.mjs`](../astro.config.mjs) to match
      where the site is served from

No repository secret is needed to review a paper any more. `ANTHROPIC_API_KEY`
and `OPENROUTER_API_KEY` are read by nothing in this repository and can be
removed from the repository secrets whenever you want to.
