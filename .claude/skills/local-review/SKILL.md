---
name: local-review
description: Generate an In Silico peer review locally on a Claude Code subscription and open a branch ready for a pull request. Use when asked to review, referee or run the panel on a preprint given as an arXiv id, a bioRxiv or medRxiv DOI, an archive URL, or a local PDF.
---

# Generate a review locally

Produce one review of one preprint with the PeerReviewAgents engine, on this
machine, on the Claude Code subscription, and leave it on a branch for the
editor to open as a pull request. Merging that pull request is what publishes
the review. Nothing here publishes anything.

No paid API key is involved at any point. Engine 0.9 is a Claude Code plugin:
the review runs as a headless Claude Code session on the signed-in
subscription, and the starter clears `ANTHROPIC_API_KEY` and
`ANTHROPIC_AUTH_TOKEN` from the environment it launches before it starts, so a
key that happens to be exported cannot pay for a review. Claude Code is the
only transport, there is no Codex path, and publish refuses a run whose
`protocol.json` names anything else.

## What the engine actually runs

One review is several agents in one session, each pinned to a model by its own
agent file in the plugin:

- N core reviewers, three by default, reading the whole manuscript
  independently and writing up their findings separately
- six specialist readers, one dimension each: `stats`, `figures-tables`,
  `methods-reporting`, `citations`, `consistency`, `field`
- one editor agent, which pools every finding, rules on the ones a reviewer
  escalated, and chooses which belong in the body of the letter

There is no desk screen and no debate stage. Agents that share a model are not
independent corroboration of one another, and the published summary says so.

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

Use whichever interpreter has `peerreviewagents` 0.9.0 or newer importable. It
is often a virtual environment outside this checkout rather than the `.venv`
here, and the `peerreview` command used in step 3 is the console script beside
it. Ask the operator which interpreter that is rather than guessing.

Read the output. It prints the engine version, the fingerprint of the installed
engine, the fingerprint of the plugin and the hash of its review workflow, and
the transport record. Stop and report if it errors.

## Step 2. Prepare the paper

```bash
.venv/bin/python scripts/local_review.py prepare \
  --paper <id-or-doi-or-url> \
  --out runs/prepared-<short-slug> \
  --arm full-two-track \
  --reviewers 3
```

Add `--pdf <path>` when the user supplied the bytes. Add `--replace` only when
the user explicitly asks for a second review of a draft this repository has
already reviewed: without it, an already reviewed draft is refused, which is
the correct default.

This resolves the paper, downloads the exact PDF for that revision, hashes it,
and decides where a review of it belongs. It calls no model. The arm and the
reviewer count are recorded here so the plan and the run can be compared, and
the published record takes both from the run rather than from this plan. Read
the printed plan back to the user: the destination path, the draft number, the
attempt number, and whether this is a first look, a revision round or a
re-review.

## Step 3. Review

One command. It imports the manuscript and runs the whole panel.

```bash
peerreview review \
  runs/prepared-<slug>/<fetched>.pdf \
  runs/<work> \
  --arm full-two-track \
  --reviewers 3 \
  --literature-cutoff <today, YYYY-MM-DD>
```

Use the `peerreview` console script from the environment in step 1. Calling it
by its full path, `<that environment>/bin/peerreview`, is the same command.

Both positionals are required and in this order: the manuscript PDF, then the
run folder to write. Every option belongs after `review`, because `peerreview`
itself carries no options and each command parses its own. The engine writes
two folders under the one you name: `<out>/manuscript`, the imported
manuscript, and `<out>/review`, the run. Add `--plugin-dir <path>` only when
the plugin is not where the installed engine expects it.

`scripts/check_skill_commands.py` parses every `peerreview` command on this
page against the engine's own parser, without executing any of them.

This is the only command that spends anything. Tell the user it is starting and
roughly how long it will take. Do not run it twice on the same output folder:
the engine refuses an existing run folder on purpose, so a retry needs a new
one.

There is no `--provider`, no `--model` and no policy flag. Each agent's model is
pinned by its agent file in the plugin, the run records what every agent
actually ran on in `runtime.json`, and the published record names them from
there.

Then write the readable reports, which costs nothing:

```bash
peerreview report runs/<work>/review
```

## Step 4. Read the review, then ask for the decision

Read `runs/<work>/review/REVIEW.md` yourself, and the `audit_<track>.md` file
of any specialist whose findings matter to the decision. Summarise for the
user: the editor agent's assessment, how many findings there are at each
severity, which ones a reviewer escalated and how the editor ruled on them, and
anything that looks wrong or unsupported. A review with no findings is a real
outcome, not a failed run. Say so plainly and go on to the decision.

Then ask the user for the decision. It is one of `accept`, `minor`, `major`,
`reject`. You may say which one the findings point toward and why, but the
choice is theirs, and the published record attributes it to a human editor. Do
not pick one on their behalf, and do not proceed without an answer.

The engine's editor agent records a judgement of its own, on significance and
strength of evidence. It is published, labelled as advisory, and it recommends
no decision. It is not an answer to this question.

Ask also whether this review should set the paper's editorial status. The
default is no. Agents wrote all of it, so by default it is published as an
experiment with a public record and no editorial weight, which is what
`baseline_eligible: false` means. Pass `--baseline-eligible` only if the user
says yes.

## Step 5. Write the bundle

```bash
.venv/bin/python scripts/local_review.py publish \
  --prepared runs/prepared-<slug> \
  --run runs/<work> \
  --decision <the user's answer> \
  --editor <the user's name or GitHub login> \
  --human-reviewed yes \
  --publish
```

`--editor` and `--human-reviewed` are required and have no defaults. `--editor`
names whoever read the run, because the attestation on the page is a claim
about a person. Pass `--human-reviewed yes` only after the user has read step
4's review and given a decision. Answering `no` writes a rehearsal bundle under
`runs/rehearsal/` instead, which is also what happens whenever `--publish` is
left off, and that bundle can never be published without a fresh run of this
command.

`--run` takes either the folder you gave the engine or the `review` folder
inside it. The manuscript workspace is found beside the run, and
`--workspace <path>` is only for a workspace that is somewhere else. The
workspace is what ties the run to the paper that was prepared: publish compares
the hash prepare took of the PDF against the hash the importer recorded, and
refuses when they differ.

Publish requires a run that finished, which means `progress.json` says
`status: complete`. A run that stopped part way cannot become a bundle that
looks whole, and a `blocked` run is refused with the cause the run recorded. It
also requires every stage the arm asked for to have reported: a specialist that
never answered is refused by name, because a bundle saying six specialist
readers over such a run describes a reader that did not report.

A review that raised nothing is one of those complete runs. Three reviewers and
six specialists can read a manuscript end to end and find nothing worth
reporting, and the engine records that as `complete` with
`review_guard_status: clean` and no findings. It publishes with an empty
findings list, which is the honest record of what happened. Do not re-run a
review to try for findings.

The engine's other finished state, `complete-without-findings`, is not that.
The engine writes it in exactly one case: every finding the reviewers raised
failed the evidence guards and was quarantined. Publish refuses it, because
such a review endorses none of its own work, which is a different claim from a
manuscript found sound, and the letter would tell the authors the wrong one.
Read the quarantined findings in `editor-package.json` before deciding what to
do next.

Add `--baseline-eligible` if the user said yes in step 4. When a submission
issue named a submitter, add `--submitter <login>` and, if that issue stated
whether they are connected to the paper, `--submitter-is-author yes` or
`--submitter-is-author no`. Leave all three off for a paper the editor picked up
themselves: the page then says nobody solicited the review, which is true.

This writes `summary.md`, `decision_letter.md`, `manuscript_stats.md`, one
`audit_<track>.md` per specialist reader copied out of the run,
`editor-package.json`, `round.json`, `provenance.json` (schema version 4) and
`manifest.json` into the destination from step 2. It refuses to overwrite an
existing bundle, and it prints which specialist readers wrote no report.

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

- Never invent the decision. The engine produces findings, severities and an
  advisory judgement, not a verdict. `provenance.generator.decision_source`
  records `human_editor`, and that has to stay true.
- Never pass a paid API key, and never set `ANTHROPIC_API_KEY` or
  `OPENROUTER_API_KEY`. If the engine asks for credentials, stop and report it.
- Never edit a published bundle under `docs/reviews/`. A re-review is a new
  immutable attempt, which is what `--replace` and the `rN` folders are for.
- Never write or reword the reviewer's text. The documents are rendered from the
  saved engine output. If one reads badly, that is a finding about the engine.
- No em dashes and no semicolons in anything you write into the repository
  outside `docs/reviews/`. Reviewer output is exempt, since it is quoted rather
  than authored.
