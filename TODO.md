# TODO

Working notes. Not published — `docs/*.md` becomes a site page, this does not.

## Prompt hygiene: who owns which instruction

`journals/insilico.toml` carries a 525-word `guidelines` block. It renders into
`journal_block`, which PRA folds into the shared cached prefix read by the
reviewers, the area chair, the editor and the venue scout. Three kinds of
content are mixed in there and only one of them belongs to In Silico.

### 1. Move the pipeline-limits warning into PRA

`insilico.toml` tells reviewers:

> You cannot run code, execute experiments, check derivations line by line, or
> read figures.

That is a fact about the tool, not about this venue, and PRA's reviewer prompts
never say it — grepped `agents/reviewers/` and `agents/utils/`, no match. So the
only place a PRA reviewer learns about its own blindness is In Silico's venue
file. Anyone running PRA against a different profile gets referees that assess
figures they never saw.

It also goes stale silently: if PRA gains figure reading, this file starts
lying to its own panel.

**Do:** move it into the shared reviewer prompt in PRA, delete it here.

### 2. Cut the report-craft duplication from `insilico.toml`

"Be specific", "no praise-padding", separate what is wrong from what you would
have done differently — PRA's `agents/reviewers/base.py` already covers all of
this, at length, in its Length and Invention sections. We are re-teaching the
reviewer something it was already told, in different words, and paying for the
tokens on all eight reviewers plus the synthesis agents.

**Do:** delete the duplicated craft advice and let PRA's base prompt own it.
Keep anything that genuinely differs from PRA's default rather than restating
it.

### 3. Keep the venue-specific content where it is

Not a change — the conclusion of the audit, recorded so it is not relitigated.
These belong to In Silico and should stay in `insilico.toml`:

- "Reviews are published in full alongside the preprint, write accordingly"
- The five criteria, in priority order
- What not to penalise (house format, fluency, unfashionable topics)
- Scope, including the patient-care line
- Calibration (use the whole scale; recognition is not evaluation)

The accept/reject bar is this category too. It is In Silico's call what its own
bar is, so it goes in this file rather than into PRA.

`docs/criteria.md` is the human-readable version of this file and the two must
be kept in step. Any edit here needs the matching edit there.
