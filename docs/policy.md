# Editorial policy

## Standing

In Silico is an experiment in open machine-generated peer review. It is not
accredited, not indexed, and not a substitute for conventional peer review.
Do not cite an In Silico listing as evidence that a result is correct.

## Authority

**The panel is advisory. A human editor decides.**

The editor-in-chief agent produces a recommendation — accept, minor revision,
major revision, or reject — and that recommendation is published verbatim. It
does not bind anyone. A human editor reads the bundle, reads anything the
authors have said on the issue, and decides whether to publish it. Merging the
review pull request is that decision; there is no other step.

The editor may decline to publish a review that is incoherent, that misreads the
paper badly enough to be misleading, or that the panel produced from a truncated
or mangled ingest. Those failures happen and quietly shipping them would be
worse than dropping them.

## Scope

**In scope.** Any original research manuscript, in any discipline, whose claims
a careful reader can evaluate from the manuscript itself and the materials it
cites or deposits. Empirical, theoretical, computational and methodological work
all qualify, as do negative results, replications and reanalyses.

Scope is set by whether the evidence can be inspected, not by discipline. An
unsupported inference is as findable in a wet-lab paper as in a simulation, and
the panel's limits (below) apply in every field alike.

The name describes how the reviewing is done, not what may be reviewed.

**Out of scope.**

- **Anything where a wrong machine-generated review could affect patient care or
  safety** — clinical trial reports, diagnostic or treatment guidance, dosing
  recommendations. The panel has no business near that and neither do we. This
  is the one hard line and it is not discipline-based: a computational paper
  that outputs a dosing recommendation is out; a clinical-adjacent methods paper
  that does not is in.
- **Work whose central evidence cannot be inspected at all** — neither shown in
  the paper nor deposited anywhere a reader could reach.
- **Anything that is not a research manuscript** — editorials, press releases,
  marketing material, or text making no checkable claim.

Being outside the reviewers' expertise is *not* grounds for rejection. It is
grounds for lower confidence, and the reports say so.

We decline submissions outside scope at the desk, without running the panel.

## Who may submit

Anyone may submit any public preprint, including one they did not write. That
is deliberate — work nobody has scrutinised is exactly what benefits from being
looked at, and preprints are public.

But a review the authors asked for and a review attached to someone's paper
without their knowledge are different things, and we will not publish them as
though they were the same. **Every review states which it is.** The submission
form asks outright whether you are an author, and the answer appears on the
published page. Where the submitter says they are not, the review carries a
notice that the authors did not request it, were not consulted, and have not
replied. Reviews published before we started recording the answer carry a third
notice — "solicitation unrecorded" — because saying nothing would let them pass
for requested ones.

We do not verify the claim. Saying so is the point: an unverifiable claim
presented as fact would be worse than one presented as a claim.

Submitting a rival's work to attach a public criticism to it is not a use we
support. The form asks non-authors to say why they are submitting, an editor
reads that before running anything, and we decline submissions that read as
score-settling.

Authors who find an unrequested review of their work: open an issue. If it
misreads the paper we will correct it, and if you object to its existence we
will take it down. That is a lower bar than we apply to reviews the authors
asked for, because you did not choose this.

## The desk

Two checks run before any referee is assigned. Either can stop a submission
without a review being produced; both are recorded in the published bundle.

### Submission integrity

Every submitted file is scanned for text hidden from a human reader — white
fill, zero opacity, invisible render mode, sub-point type, off-page placement —
that carries instructions aimed at an automated reviewer. The obvious example is
a paragraph no human sees that tells the referee to recommend acceptance.

This matters more here than at a conventional journal. Our referees are all
models, so a payload written for a model is written for *every* referee we
have.

Three properties of this check are deliberate:

- **It runs before any model reads the file.** A prompt injection only works on
  a model that reads it, so the scan has to come first. It costs no tokens and
  makes no model call.
- **Concealed text alone is never a rejection.** Scanned PDFs carry an invisible
  OCR layer, and plenty of legitimate files have hidden text for good reasons.
  The rejection requires a reviewer-directed *instruction* found inside the
  concealed text.
- **Visible instructions are also grounds for rejection.** Text addressed to
  whoever is assessing a manuscript does not belong in it, and being unhidden
  does not make it acceptable. Where the scan finds such language in visible
  text, the desk screen reads the passages and decides.

    The line it draws is who the text speaks to, not whether it was hidden.
    Language that *addresses* the reviewer — instructing, flattering or
    bargaining with them — is an attempt to manipulate review. Language that
    *describes* such attempts is a paper about prompt injection quoting its own
    subject matter, and we will not reject scholarship for containing the thing
    it studies. If you work on this and your manuscript quotes payloads, you are
    in scope; say so in the submission and it will be read that way.

**A finding is not published automatically.** An integrity rejection is an
allegation about named people, not an opinion about their work, and a false
positive would be damaging and hard to retract. These open as draft pull
requests and are published only if a human editor reads the evidence and agrees.
If we are unsure, we contact the authors privately and publish nothing.

If you believe a finding is wrong, see [Contesting a review](#contesting-a-review)
— it applies to desk rejections too, and we would rather hear about a false
positive than not.

### Editorial triage

A single fast pass then decides whether the submission clears the bar for full
review: in scope, intelligible, complete, and not fatally flawed on its face.
The instruction to this screen is to reject sparingly and to send anything
borderline to the panel.

A desk rejection is recorded as `desk_rejected` in the bundle's frontmatter and
`provenance.json`, and is badged separately in the index. It is not the same act
as a panel rejection, and we will not present it as one: nothing read the
manuscript in depth, and no specialist reports exist.

## Known limitations

These are properties of the method, not bugs we expect to fix:

- **The panel cannot run your code.** Reproducibility scores reflect what the
  paper *claims* about availability, not verification.
- **It cannot check your math.** Derivations are assessed for plausibility and
  presentation, not correctness.
- **It cannot see figures.** Ingest is text-only via `pypdf`. Claims resting on
  a figure will be under-assessed.
- **Long papers cost more, and cost is what limits us.** No truncation is
  applied today — every agent reads the whole manuscript. The pipeline supports
  a section-aware per-agent character budget, and we may enable one if long
  submissions become a budget problem; if we do, it will be recorded in each
  affected review's `provenance.json` rather than announced only here.
- **Literature claims are search-grounded but not exhaustive.** The Novelty and
  Literature reviewers query real APIs, but absence of a hit is not evidence of
  novelty.
- **It has model-shaped biases.** It rewards conventional structure and clear
  writing. Unusual-but-correct work will likely score worse than it deserves.

One consequence of a fixed panel is worth stating separately. Eight referees are
assigned to every manuscript, and some manuscripts contain nothing in a given
referee's dimension — a qualitative interview study has no statistical analysis
to judge. Those referees may return **not applicable** instead of a score, and
an n/a is left out of the panel mean rather than averaged into it; the review
page says how many referees the mean is actually over.

That exists because the alternative was measured. Required to produce a number
regardless, the data-analysis reviewer wrote that a paper had "no p-values,
confidence intervals, effect sizes, sample-size calculations, or statistical
claims to evaluate" and then scored it 5 of 5 — the highest data-analysis score
in the corpus. A forced score is not a neutral score; it is a generous one. An
n/a is not a quiet way of marking work down, either: thin, unclear or missing
evidence is a low score. Only a dimension the manuscript contains nothing of
gets an n/a.

## Reproducibility

Every review ships a `provenance.json` recording the provider, the model used at
each stage and any per-agent override, pipeline version and commit SHA, debate
rounds, which desk screens were active, per-reviewer scores, total cost and the
per-agent cost breakdown, and the resolved preprint metadata. Given the same
inputs you can re-run the panel yourself. Outputs won't be byte-identical — the
models aren't deterministic — but the configuration is fully disclosed.

Not every stage runs on the same model, and the record is per-stage for that
reason: reading a single model name off a review would misdescribe it.

Reviews are never silently edited. Where one is wrong, a human editor withdraws
it or annotates the page with what it got wrong, and the published bundle stays
byte-for-byte as it was; where a fresh run is warranted, the new review is
published beside the old one rather than over it.

A revision round adds a review; it never replaces one. The earlier round stays
published as the record of the draft it read, and each round records which
manuscript version it saw and a SHA-256 of that exact file. Where a round ran
without a verified comparison against the previous draft, the page and the
paper's review history both say so — see
[revision rounds](criteria.md#revision-rounds). Rounds are capped at three; past
that the submission is decided rather than cycled.

## Contesting a review

Comment on the review PR, or on your submission issue if it's already merged.

Nothing you write is shown to the panel. Author input into a review is a route
we removed deliberately rather than one we never built — see
[why](submit.md#resubmitting-a-revised-draft). What you get instead is three
routes that don't route your words through a model, described in full under
[if the review got something wrong](submit.md#if-the-review-got-something-wrong):

- **A right of reply** — we publish your response verbatim beside the review,
  labelled as yours. No agent reads it and it changes no score. This is the
  route for disagreeing with the judgment: we won't remove a recommendation
  because you dispute it, and your dissent sits next to it permanently.
- **Editor withdrawal or correction** — where the panel demonstrably misread the
  paper, a human editor withdraws the review or annotates it. A person decides;
  no agent is involved. **A statement about your paper that is factually false**
  gets corrected or the review gets pulled, because being wrong about what a
  paper says is the one failure mode we treat as disqualifying.
- **Re-review** — a fresh review of the unchanged manuscript, with no author
  input, published alongside the original rather than in place of it.

## Conflicts and cost

The editor is one person running this out of pocket. Reviews are triggered
manually because each one costs real money. There is no queue guarantee, no SLA,
and no promise the project outlives the author's interest in it.

If a submission is the editor's own work, the review is labeled as such on its
page.

## Data

We store: the preprint URL and its public metadata, the review bundle, the
GitHub issue thread, and — if you send one — your reply, which we publish
verbatim beside the review and keep there permanently. We do not store
manuscript PDFs — they're fetched into a temporary directory at review time and
deleted after.

Manuscript text is sent to a third-party model provider (currently Anthropic).
Don't submit anything you can't send to a commercial API. Since we only accept
already-public preprints, this shouldn't come up.

## License

Reviews and site content are CC BY 4.0 — reuse them with attribution.
Preprints remain under whatever license their authors chose; we host none of
them and claim nothing over them.
