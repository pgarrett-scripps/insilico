---
name: local-review
description: Generate an In Silico peer review locally on a Claude Code subscription and open a branch ready for a pull request. Use when asked to review, referee or run the panel on a preprint given as an arXiv id, a bioRxiv or medRxiv DOI, an archive URL, or a local PDF.
---

# Generate a review locally

Produce one review of one preprint with the PeerReviewAgents engine, on this
machine, on the Claude Code subscription, and leave it on a branch for the
editor to open as a pull request. Merging that pull request is what publishes
the review. Nothing here publishes anything.

No paid API key is involved at any point. The engine runs through its
`claude-code` transport, which shells out to the `claude` CLI on the signed-in
subscription. That is the engine's default provider and the only one this
repository uses. The engine also has a `codex` transport, reachable only by
passing `--provider codex`: never pass it, and never run a review on it.
If the CLI turns out to be authenticated against a paid API provider, step 1
stops and says so.

## What you need from the user

One paper, in any of these forms:

- an arXiv id, such as `2501.01234`
- a bioRxiv or medRxiv DOI, such as `10.1101/2026.03.12.711120`
- an archive URL for either
- a local PDF path

An arXiv id, a DOI or an archive URL is a permanent identity, and only those can
be published. A bare PDF names no revision, so a review of one lands in `runs/`
and is marked unpublishable. If the user has a PDF *and* an identifier, pass
both: the identifier is the identity and the PDF supplies the exact bytes.

Ask for the decision later, never now. You cannot choose it, and neither can the
engine.

## Step 1. Preflight

Run from the repository root:

```bash
.venv/bin/python scripts/local_review.py fingerprint
```

Use whichever interpreter has `peerreviewagents` 0.8.0 or newer importable. On
this machine that is normally `/home/ty/Repos/paper-workbench/.venv/bin/python`.

Read the output. It prints the engine version, the engine source fingerprint,
and the transport record including the authentication method and subscription
type. Stop and report if it errors. Do not continue on a paid API provider.

## Step 2. Prepare the paper

```bash
.venv/bin/python scripts/local_review.py prepare \
  --paper <id-or-doi-or-url> \
  --out runs/prepared-<short-slug>
```

Add `--pdf <path>` when the user supplied the bytes. Add `--replace` only when
the user explicitly asks for a second review of a draft this repository has
already reviewed: without it, an already reviewed draft is refused, which is
the correct default.

This resolves the paper, downloads the exact PDF for that revision, hashes it,
and decides where a review of it belongs. It calls no model. Read the printed
plan back to the user: the destination path, the draft number, the attempt
number, and whether this is a first look, a revision round or a re-review.

## Step 3. Import, then review

Two engine commands, in order. Set `PY` to the interpreter from step 1 and
`WORK` to a fresh working folder under `runs/`.

```bash
$PY -m peerreviewagents.engine import \
  runs/prepared-<slug>/<fetched>.pdf runs/<work>/workspace \
  --source-url <the archive URL>

$PY -m peerreviewagents.engine review \
  runs/<work>/workspace runs/<work>/run \
  --provider claude-code --model claude-sonnet-5-5 \
  --policy agentic-v1 \
  --literature-cutoff <today, YYYY-MM-DD> \
  --mode ensemble --reviewers 2
```

There is no billing step. The engine asked for a confirmation file before it
would start a subscription run, and 0.8.0 removes that file, the flag that
named it and every usage gate around it.

`--provider`, `--model` and `--policy` belong after `review`, not before it.
The engine defines them on each subcommand's parser rather than at the top
level, so a command that puts them first is rejected before anything runs.
`scripts/check_skill_commands.py` parses every engine command on this page
against the engine's real parser, without executing any of them.

Pass `--policy agentic-v1` by name even though it is the engine's default:
high effort, thirty tool calls per reviewer and no cap on findings. Naming it
puts the allowance a published review ran under in the command, where it can
be read back. The alternative is `standard-v1`, the bounded study budget of at
most five findings in about 900 words at medium effort, which is not what a
review published here should run under.

The second command is the only one that spends anything. Tell the user it is
starting and roughly how long it will take. Do not run it twice on the same
output folder: the engine refuses an existing run directory on purpose, so a
retry needs a new one.

`--model` accepts `claude-sonnet-5-5` or `claude-opus-5-5`. Default to
`claude-sonnet-5-5` unless the user asks otherwise. Whichever you pass, one
model writes the entire review, and the published page says so.

Then write the readable reports, which costs nothing:

```bash
$PY -m peerreviewagents.engine report runs/<work>/run
```

## Step 4. Read the review, then ask for the decision

Read `runs/<work>/run/REVIEW.md` yourself. Summarise for the user: the
reviewer's overall assessment, how many findings there are at each severity,
and anything in it that looks wrong or unsupported. A report with no findings
is a real outcome, not a failed run. Say so plainly and go on to the decision.

Then ask the user for the decision. It is one of `accept`, `minor`, `major`,
`reject`. You may say which one the findings point toward and why, but the
choice is theirs, and the published record attributes it to a human editor. Do
not pick one on their behalf, and do not proceed without an answer.

Ask also whether this review should set the paper's editorial status. The
default is no. One model wrote all of it, so by default it is published as an
experiment with a public record and no editorial weight, which is what
`baseline_eligible: false` means. Pass `--baseline-eligible` only if the user
says yes.

## Step 5. Write the bundle

```bash
.venv/bin/python scripts/local_review.py publish \
  --prepared runs/prepared-<slug> \
  --run runs/<work>/run \
  --workspace runs/<work>/workspace \
  --decision <the user's answer> \
  --editor <the user's name or GitHub login> \
  --human-reviewed yes \
  --publish
```

`--workspace`, `--editor` and `--human-reviewed` are all required and have no
defaults. `--workspace` is what ties the run to the paper that was prepared:
publish compares the hash prepare took of the PDF against the hash the importer
recorded, and refuses when they differ. `--editor` names whoever read the run,
because the attestation on the page is a claim about a person. Pass
`--human-reviewed yes` only after the user has read step 4's review and given a
decision. Answering `no` writes a rehearsal bundle under `runs/rehearsal/`
instead, which is also what happens whenever `--publish` is left off, and that
bundle can never be published without a fresh run of this command.

Do not pass `--model`. The published record names the model the run itself
recorded in `protocol.json`, so an opus run says opus without being told. The
flag exists only as a cross-check: pass it when you want publish to refuse if
the run turns out to have used a model other than the one you expected.

Publish also requires a run that finished. It reads `progress.json` and accepts
only the engine's two finished states, `complete` and
`complete-without-findings`, so a run that stopped part way cannot become a
bundle that looks whole. A `blocked` run is refused and the refusal repeats the
cause the run recorded.

`complete-without-findings` is a review. Two reviewers can read a manuscript
end to end and raise nothing, and that result publishes with an empty findings
list, which is the honest record of what happened. Do not re-run a review to
try for findings. The one case publish still refuses is a run whose findings
were every one of them quarantined by the engine's evidence guards: that is a
review endorsing none of its own work, not a manuscript found sound, and the
refusal says which it is.

Add `--baseline-eligible` if the user said yes in step 4. When a submission
issue named a submitter, add `--submitter <login>` and, if that issue stated
whether they are connected to the paper, `--submitter-is-author yes` or
`--submitter-is-author no`. Leave all three off for a paper the editor picked up
themselves: the page then says nobody solicited the review, which is true.

This writes `summary.md`, `decision_letter.md`, `manuscript_stats.md`,
`editor-package.json`, `round.json`, `provenance.json` (schema version 3) and
`manifest.json` into the destination from step 2. It refuses to overwrite an
existing bundle.

## Step 6. Check it builds

```bash
npm run check:schema && npm run check:markdown && npm run build
```

All three must pass before you hand anything over. `check:schema` validates the
new provenance record. If it fails, read the error, fix the record, and do not
edit the schema to make a bad record pass.

## Step 7. Branch and hand over

```bash
git checkout -b review/<slug>-$(date +%s)
git add docs/reviews/<year>/<slug>
git commit -m "review: <title> (<decision>)"
```

Stage the bundle by explicit path. Never `git add -A`, never `git add .`: this
working tree normally holds the owner's uncommitted work, and nothing of theirs
belongs in a review commit.

Do not push and do not open the pull request. Print the branch name, the bundle
path and the decision, and say that merging the pull request is what publishes
the review.

## Rules

- Never invent the decision. The engine produces findings and severities, not a
  verdict. `provenance.generator.decision_source` records `human_editor`, and
  that has to stay true.
- Never pass a paid API key, and never set `ANTHROPIC_API_KEY` or
  `OPENROUTER_API_KEY`. If the engine asks for credentials, stop and report it.
- Never edit a published bundle under `docs/reviews/`. A re-review is a new
  immutable attempt, which is what `--replace` and the `rN` folders are for.
- Never write or reword the reviewer's text. The documents are rendered from the
  saved engine output. If one reads badly, that is a finding about the engine.
- No em dashes and no semicolons in anything you write into the repository
  outside `docs/reviews/`. Reviewer output is exempt, since it is quoted rather
  than authored.
