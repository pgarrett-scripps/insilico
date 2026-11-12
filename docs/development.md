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
    ├── review_*.md       # one per core reviewer
    ├── audit_*.md        # one per specialist track
    └── (retired panel)   desk_screen.md  debate_transcript.md
        debate_synthesis.md  journal_recommendations.md

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
├── review_plan.py        # where a review of a given draft belongs
├── review_bundle.py      # writes a bundle the site can render
├── check_updates.py      # find reviews whose preprint has changed since
└── smoke_test.py         # the pipeline/site data contract, offline

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

Every agent in the run reads the same manuscript through the same transport, and
the only thing that distinguishes one reader from another is the prompt it was
given. Three core reviewers in isolation and six specialist tracks are six
questions asked once each, not an independent replication of the review, so a
local review is published as an experiment by default: public, citable, and
unable to set the paper's editorial status or become the baseline for the next
draft. `--baseline-eligible` opts one in, and that is a decision taken per
review.

The decision is a person's. The engine grades findings by severity and
deliberately recommends no verdict, so `--decision` is an operator input that the
record attributes to a human editor. There is no code path that lets the engine
name its own decision, and `provenance.generator.decision_source` is pinned to
`human_editor` by the schema.

### The retired hosted panel

Reviews published before this route ran on a GitHub runner against a paid API
key, as a desk screen, a five-reviewer panel, two audits and a debate. That path
is retired. `.github/workflows/review.yml` is now a manual-only stub that fails
with a pointer here, and the `ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY`
repository secrets are no longer read by anything. `.env.example` is gone with
them. It told a contributor to paste an Anthropic key into `.env`, which no
code here reads any more and which the local route forbids outright.

Its driver is gone too. `scripts/run_review.py`, `scripts/_pinned_review.py`,
`scripts/review_telemetry.py` and `peerreview.toml` were kept so those runs
stayed re-runnable, and every one of them imported a module that
peerreviewagents 0.8.0 deletes: the LangGraph panel, its default config, its
ingest loader, its report writers and its observability hooks. A driver that
cannot import anything is not reproducibility, so the four files were removed
rather than carried as a shim. The fourteen bundles those runs wrote are
untouched, and their pages still render from what is in them.

The sections below marked *retired* describe that path, because fourteen
published reviews came out of it and their records cannot be read without it.
They are history now rather than instructions: nothing in this repository can
run that path any more.

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
# Any interpreter with peerreviewagents 0.9.0 or newer importable. The
# `peerreview` console script used below is the one beside it.
PY=/path/to/.venv/bin/python

$PY scripts/local_review.py fingerprint
$PY scripts/local_review.py prepare --paper 10.1101/2026.03.12.711120 \
    --out runs/prepared-example --arm full-two-track --reviewers 3
```

`fingerprint` is the preflight. It prints the engine version, a SHA-256 over the
engine's own source tree, the same over the plugin that does the reviewing, the
hash of the review workflow, and the transport record. It calls no model. It
reports no authentication status, because the engine exposes none: what keeps
this path free is the plugin starter, which removes `ANTHROPIC_API_KEY` and
`ANTHROPIC_AUTH_TOKEN` from the environment it hands the session, so no key in
the operator's shell can pay for a review. If the `claude` CLI does not report
a version it says so, because a review needs it on PATH and signed in.

`prepare` resolves the identifier, downloads the exact PDF for that revision,
hashes it, and writes `prepared.json` with the destination, the draft number and
the attempt number. It calls no model either.

`--paper` takes an arXiv id, a bioRxiv or medRxiv DOI, or an archive URL for
either. `--pdf` supplies exact bytes for that identity. A `--pdf` with no
`--paper` can still be reviewed, but the run is marked unpublishable and lands in
`runs/`, because a review has to name the revision it judged and a loose PDF
does not.

Then the engine itself, which is the only part that spends anything, and which
the skill walks through. One command imports the manuscript and runs the whole
panel, and a second writes the readable reports:

```bash
peerreview review runs/prepared-example/<fetched>.pdf runs/example \
    --arm full-two-track --reviewers 3 --literature-cutoff 2026-11-12
peerreview report runs/example/review
```

Both positionals are required and in that order: the manuscript PDF, then the
folder to write. The engine writes `runs/example/manuscript`, the imported
paper, and `runs/example/review`, the run. There is no provider flag, no model
flag and no policy flag. Claude Code is the only transport, each agent's model
is pinned by its own agent file in the plugin, and `runtime.json` records what
every agent actually ran on. Read `REVIEW.md` from the run, decide, and write
the bundle:

```bash
$PY scripts/local_review.py publish \
    --prepared runs/prepared-example \
    --run runs/example \
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

The imported manuscript is what ties the steps together. `prepare` hashes the
PDF it fetched, the engine's importer hashes the bytes it was handed into
`paper.json`, and the run records the paper it reviewed. `publish` reads that
`paper.json` from the manuscript folder beside the run, compares all three, and
refuses when they disagree, so a run of one paper cannot be published as a
review of another. `--workspace` points at that folder when it is somewhere
else.

`--editor` and `--human-reviewed` have no defaults. The published record carries
an attestation that a named person read the run before it was merged, and that
claim is the operator's to make rather than the script's. Answering
`--human-reviewed no` writes a rehearsal that records the absence instead, and
refuses `--publish`.

Everything in the record about the run itself comes from what the run wrote, and
it is read back through the engine's own `read_run` rather than parsed out of the
files by hand: the arm and the workflow the run was asked for, the paper id and
the hash of each plugin and workflow file taken when the call started, the
reviewer count, one row per agent with the model the transport actually served
it, which stages reported and which were retried, the guards' verdict and how
many findings they held back, and the status the run ended in. One field is read
out of the run folder by hand, because the reading does not carry it: the moment
the starter wrote `startup.json`, which the record publishes as when the
transport evidence was gathered. A value the run did not record is left out of
the record rather than filled in from a flag.

Whether a run can be published is the engine's answer too. `read_run` sets a
`publishable` flag and lists its reasons beside it, and publish gates on the
flag and prints those reasons. No status word is special-cased, which is what
lets a review that raised nothing publish while a review the guards emptied of
every finding does not, although the engine finishes both as
`complete-without-findings`.

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
The model ids are not a flag. `publish` reads them from the JSON the run wrote,
which is the only record of what actually answered.

### Checks

```bash
python scripts/smoke_test.py          # pipeline and site data contract
python scripts/check_review_manifests.py
npm run check:schema                  # published provenance against the schema
npm run check:local                   # the local record validates, a paid one does not
npm run check:markdown
npm run check:attempts
npm run build
npm run check:punctuation             # after a build, over dist/
```

None of these touch the network or call a model. `check:local` is the one that
holds this route honest: it asserts that a record admitting a paid API key, or
naming anything but a human as the source of the decision, fails validation, and
that records from the retired panel still pass unchanged. CI runs the lot,
alongside a build that fails if a published bundle goes unrendered.

## Configuration

A local run has very little to configure, which is the point. The transport is
`claude-code`, the arm names which readers run, and `--reviewers` says how many
core reviewers to send in. There is no model setting: the plugin pins a model per
agent file, and the record reports the model each agent actually ran on.
Everything else that used to be a setting is now a property of the engine
release, and the release is identified in the record rather than described.

Each review records the engine package name and version, the hash of every
plugin and workflow file that did the work, the In Silico commit, the transport
and its authentication method, one row per agent with its model, and a hash of
the exact PDF bytes reviewed. The
[DOI](https://doi.org/10.5281/zenodo.21781895) identifies the software and the
hashes identify the run.

`schemas/review-provenance.schema.json` is the contract. A record from a plugin
run is `schema_version: 4` and carries a `generator` block. The retired panel's
records are `schema_version: 2`, and records written before versioning existed
are read as they are. All of them keep rendering, which is why no published
bundle had to be rewritten for any of this.

### Retired: configuration of the hosted panel

Model selection for the panel lived in `peerreview.toml`, and the panel was
held to In Silico's own profile in
[`journals/insilico.toml`](../journals/insilico.toml). `peerreview.toml` is gone
with the driver that read it, since the engine release that read its `[models]`
and `[agent_models]` tables no longer exists. The journal profile remains and
nothing on the current path reads it.

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

The prompt compression the hosted panel could switch on is gone from the engine.
It saved under a cent a review and it was not free: with compression on, that
panel's clarity reviewer reported grammatical errors three times on a paper
where the uncompressed run reported none, having read the compressor's work as
the authors' writing.

## Cost

A review costs nothing per run. It is generated on a Claude Code subscription
the editor already pays for, so the price of a review is subscription capacity
and the editor's own time rather than a dollar figure. A local record therefore
reports no cost at all. `total_cost_usd` is `null`, and the schema requires it to
be `null` rather than zero, because a zero would read as a measured free run.

The real limit is the subscription's rate and usage limits. Three core reviewers
is the default for that reason, and `--reviewers` is the knob that costs
capacity. The engine refuses an existing run directory, so a retry needs a new
folder and never silently doubles a run.

Reviews published on the retired hosted path do carry a per-agent dollar
breakdown in their `provenance.json`, measured at the time. A full round there
was 15 model calls, and a desk rejection ended the run before the other 14.

## First-time setup

- [ ] Sign in to the `claude` CLI on a subscription, then run
      `python scripts/local_review.py fingerprint` and check it reports a
      subscription login and no paid API key. A Claude subscription reports its
      API provider as `firstParty`, which is the subscription route and not a
      paid key
- [ ] Install an interpreter with `peerreviewagents` 0.9.0 importable
- [ ] Settings, Pages, Source: **GitHub Actions**
- [ ] Settings, Actions, Workflow permissions: **Read and write**, and allow PR
      creation
- [ ] Set `site` and `base` in [`astro.config.mjs`](../astro.config.mjs) to match
      where the site is served from

No repository secret is needed to review a paper any more. `ANTHROPIC_API_KEY`
and `OPENROUTER_API_KEY` are read by nothing in this repository and can be
removed from the repository secrets whenever you want to.
