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

## Acceptance: In Silico accepts at minor revision or better

**Decided.** The panel keeps emitting the four standard verdicts. In Silico
applies its own rule on top: a paper the editor returns at **accept or minor
revision is accepted**; **major revision or reject is declined**.

### Why this rather than the alternatives

The problem was that 24 bundles produced 18 major and 6 minor and nothing else,
so the site could not say how many papers it had accepted. Three fixes were on
the table: teach the editor to use all four verdicts, make its verdict binary,
or split the verdict into a disposition plus a revision burden. This is the
fourth, and it wins on every axis we care about.

**It needs no change to PeerReviewAgents.** PRA keeps the four-verdict
vocabulary that every other venue and user expects. The policy about what a
verdict *means to this journal* lives in this journal. That is the same
separation of concerns as the prompt-ownership audit above.

**It is drawn on the verdict, not the score** — but the two barely differ, and
an earlier version of this note overstated the gap. Corrected: across the 20
graded bundles, everything at or below 3.75 is major and everything at or above
4.00 is minor. The only interleaving is at 3.88, where one paper went each way
on different runs. A threshold at 3.9 reproduces the editor 19 times in 20.

The claim that "three majors sit at or above the lowest minor" came from
counting single-model bundles, which we now exclude from deciding a paper's
status; one of those three was the free Nemotron run. Among graded reviews it
is one paper, not three.

We still use the verdict rather than the mean, because it is a judgement about
the manuscript rather than an average that happens to track it. But the current
data does not show the editor adding signal the arithmetic lacks, and nothing
should be built on the assumption that it does. This is the strongest argument
for phase 2.

**The rate is credible.** 6 of 24 = 25% acceptance.

### Two rules that come with it

**"Declined", never "Rejected".** The editor declined to accept; it did not
reject. This matters practically: In Silico publishes reviews of papers
submitted by people who are not the authors, and a permanent
machine-generated "rejected" on a stranger's preprint is a materially
different act from "In Silico declined to accept this".

**Do not tell the editor the rule.** It currently returns "minor revision"
without anything hanging on it, which is exactly why the 25% is worth trusting.
Handing it the consequence invites it to soften — a model that knows it is
gatekeeping grants more minors. Define what the verdicts mean if we like, but
never what In Silico does with them afterward.

The cost is that a constructive decision letter sits under a "Declined" label.
That is acceptable. Journals decline papers with constructive letters
constantly, and "Declined" does not contradict "here are six things to fix" the
way "Rejected" would.

### Phase 1 — derive and display — DONE

Shipped. 4 of 19 accepted, 21%. `decision` is untouched everywhere and still
reads exactly as the editor wrote it; the rule lives in `corpus.js` alone.

One thing turned up while implementing it and is worth keeping in mind. Status
comes from the most recent **graded** review, not simply the newest.
`intrafilament` has three round-1 bundles — graded major, graded minor, then a
free single-model rerun returning major — and taking the newest would have let
a run the site itself warns about decide the paper. Where every review of a
paper is single-model, the newest stands.

### Phase 2 — sharpen the boundary — NOT DOING, deliberately

Nothing defines what separates minor from major: not `insilico.toml`, not the
editor prompt, not the area chair, and strictness sits at level 3, which
injects no directive by design. The boundary is whatever the model's prior
thinks "minor revision" means, and that unwritten standard is the publication
line.

Decided against acting on it. Phase 1 works: 21% acceptance, a sensible spread,
constructive letters. Writing the definition would change editor behaviour,
move the rate by an unknown amount, and split the corpus into a pre- and
post-definition era — real costs, against a problem that is currently
theoretical.

What would change the decision:

- Someone asks what In Silico's acceptance standard *is* and "whatever the
  editor thinks minor revision means" is not an answer we want to give.
- The rate drifts. If acceptance climbs well above 21% or collapses toward
  zero as papers accumulate, the boundary is moving and needs pinning down.
- A verdict lands that plainly contradicts its own letter, which is the
  signal that the implicit standard has broken rather than merely being
  unwritten.

If it is picked up, the first step is free and decides whether the rest is
worth it: read the decision letters in the 3.75-4.12 band — `optimal-stimulation`
(3.88 major), `intrafilament` v2 (3.88 minor), and the three 4.12 minors. If
the editor is drawing a discernible line, the definition can be written to
describe what it already does and there is no two-era problem. If it is not,
the boundary is noise and defining it is worth the disruption.

Only then re-run, and re-run the overlap band rather than the extremes: 2.50
and 4.12 are unambiguous and would move under any definition worth writing.

## Record what the research tools actually did

The site claims, on the home page and in `criteria.md` and `README.md`:

> Novelty and Literature query arXiv, Semantic Scholar, PubMed and bioRxiv
> live, so claims about prior work rest on search results rather than recall.

Nothing published can confirm that. `run_agent` emits no event when it executes
a tool call, and `observability.py` has no notion of one, so no bundle records
whether a search fired, what was queried, or what came back.

Everything around it checks out. `research_enabled` defaults true with no
override in `peerreview.toml`; three agents declare tools (`literature`,
`novelty`, `citation_integrity`); the prompts tell them plainly to search
("use them", "run a verification search"); all three tools return live results
when called directly. And the two tool-using reviewers cost 3-8x more per run
than any other reviewer on the same model, across 19 runs.

But the cost gap is not proof. Tool-using agents take a two-call path
(`invoke_structured_after_tools`) that doubles cost even when zero tools are
called. And the one literature report read closely cites nothing that did not
come from the manuscript's own reference list.

So the claim is probably true and definitely unverifiable, which for a journal
whose pitch is publishing the complete referee record is the wrong side of the
line to be on.

**Do (PRA, ~1 hour):**

- [ ] Emit an `AgentEvent` per tool call in `run_agent` — tool name, query,
      result count. The loop already has all three in hand.
- [ ] Aggregate per node into `provenance.json`, next to `cost_by_node`.
- [ ] Surface it on the review page: "literature reviewer ran 3 searches, 11
      results". Absent on older bundles, like every other field added late.

This also catches the silent-degradation case. When the tool loop fails,
`structured.py` falls back to a tools-free pass and logs "reviewing without
research tools" — a review that lost its grounding currently looks identical
to one that had it.
