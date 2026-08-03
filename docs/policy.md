# Editorial policy

## Standing

In Silico is an experiment in open machine-generated peer review. It is not
accredited, not indexed, and not a substitute for conventional peer review.
Do not cite an In Silico listing as evidence that a result is correct.

## Authority

**The panel is advisory. A human editor decides.**

The editor agent produces a recommendation (accept, minor revision, major
revision, or reject) and we publish it word for word. It binds nobody. A human
editor reads the bundle, reads anything the authors said on the issue, and
decides whether to publish. Merging the pull request is that decision.

The editor may decline to publish a review that is incoherent, that misreads the
paper badly enough to be misleading, or that the panel produced from a truncated
or mangled ingest. Those failures happen and quietly shipping them would be
worse than dropping them.

## Scope

**In scope.** Any original research manuscript, in any discipline, whose claims
a careful reader can evaluate from the manuscript itself and the materials it
cites or deposits. Empirical, theoretical, computational and methodological work
all qualify, as do negative results, replications and reanalyses.

Scope depends on whether the evidence can be checked, not on the field. An
unsupported claim is as findable in a lab paper as in a simulation. The name
describes how we review, not what we review.

**Out of scope.**

- **Anything where a wrong machine-generated review could affect patient care.**
  Clinical trial reports, diagnostic or treatment guidance, dosing
  recommendations. This is the one hard line, and it is not about field: a
  computational paper that outputs a dosing recommendation is out, a
  clinical-adjacent methods paper that does not is in.
- **Work whose central evidence cannot be checked at all**, neither shown in the
  paper nor deposited anywhere a reader can reach.
- **Anything that is not a research manuscript.** Editorials, press releases,
  marketing, or text making no checkable claim.

Being outside the reviewers' expertise is not grounds for rejection. It lowers
their confidence, and the reports say so.

We decline submissions outside scope at the desk, without running the panel.

## Who may submit

Anyone may submit any public preprint, including one they did not write. Work
nobody has looked at is exactly what benefits from being looked at, and
preprints are public.

But a review the authors asked for and a review attached to someone's paper
without their knowledge are different things, and we will not publish them as if
they were the same. **Every review says which it is.** The form asks whether you
are an author, and the answer appears on the page. Where the submitter says they
are not, the review carries a notice that the authors did not request it, were
not consulted, and have not replied. Reviews published before we recorded this
say "solicitation unrecorded", because saying nothing would let them pass for
requested.

We do not verify the claim. Saying so is the point: an unverifiable claim
presented as fact would be worse than one presented as a claim.

Submitting a rival's work to attach a public criticism to it is not a use we
support. The form asks non-authors to say why they are submitting, an editor
reads that before running anything, and we decline submissions that read as
score-settling.

If you find an unrequested review of your work, open an issue. If it misreads
the paper we will correct it. If you object to it existing at all we will take
it down. That is a lower bar than for reviews the authors asked for, because you
did not choose this.

## The desk

Two checks run before any referee is assigned, and either can stop a submission
without a review being produced. `provenance.json` records which screens were
active for that submission. The triage screen publishes its verdict as
`desk_screen.md` whether it passed the paper or not; the integrity scan writes
`integrity.md` only when it found something.

### Submission integrity

Every submitted file is scanned for text hidden from human readers (white fill,
zero opacity, invisible render mode, tiny type, off-page placement) that carries
instructions aimed at an automated reviewer. The obvious example is a paragraph
nobody sees telling the referee to recommend acceptance.

This matters more here than at a normal journal. Our referees are all AI, so a
payload written for AI reaches every referee we have.

Three properties of this check are deliberate:

- **It runs before any model reads the file.** A prompt injection only works on
  a model that reads it, so the scan has to come first. It costs no tokens and
  makes no model call.
- **Hidden text alone is never a rejection.** Scanned PDFs carry an invisible OCR
  layer, and plenty of legitimate files have hidden text for good reasons.
  Rejection needs an instruction aimed at the reviewer inside the hidden text.
- **Visible instructions are also grounds for rejection.** Text addressed to
  whoever is assessing a manuscript does not belong in it, and being unhidden
  does not make it acceptable. Where the scan finds such language in visible
  text, the desk screen reads the passages and decides.

    The line is who the text speaks to, not whether it was hidden. Language that
    *addresses* the reviewer, instructing or flattering or bargaining with them,
    is an attempt to manipulate review. Language that *describes* such attempts
    is a paper about prompt injection quoting its subject, and we will not reject
    research for containing the thing it studies. If you work on this and quote
    payloads, say so in the submission and it will be read that way.

**A finding is never published automatically.** This is an allegation about named
people, not an opinion about their work, and a false positive would be damaging
and hard to undo. These open as draft pull requests and go nowhere unless a human
editor reads the evidence and agrees. If we are unsure we contact the authors
privately and publish nothing.

If you think a finding is wrong, see [Contesting a review](#contesting-a-review).
It applies to desk rejections too.

### Editorial triage

A single fast pass then decides whether the submission clears the bar for full
review: in scope, intelligible, complete, and not fatally flawed on its face.
The instruction to this screen is to reject sparingly and to send anything
borderline to the panel.

A desk rejection is recorded in `provenance.json` and badged separately. It is
not the same as a panel rejection and we will not present it as one, because
nothing read the paper in depth and no specialist reports exist.

## Known limitations

These are properties of the method, not bugs we expect to fix:

- **The panel cannot run your code.** Reproducibility scores reflect what the
  paper claims about availability, not what we verified.
- **It cannot check your maths.** Derivations are judged on plausibility and
  presentation, not correctness.
- **It cannot see figures.** The paper reaches the panel as text and the images
  are dropped. Claims resting on a figure will be under-assessed.
- **Long papers cost more, and cost is what limits us.** Nothing is truncated
  today. Every agent reads the whole paper. If long submissions become a budget
  problem we may cap that, and each affected review will record it.
- **Literature checks are real but not exhaustive.** The novelty and literature
  reviewers query real databases, but no hit is not proof of novelty.
- **It has AI-shaped biases.** It rewards conventional structure and clear
  writing. Unusual but correct work will probably score worse than it deserves.

Eight referees are assigned to every paper, and some papers contain nothing in a
given referee's area. A qualitative interview study has no statistics to judge.
Those referees can return **not applicable** instead of a score, which is left
out of the mean rather than averaged in, and the page says how many referees the
mean covers.

We added that because we measured the alternative. Forced to produce a number,
the data-analysis reviewer wrote that a paper had "no p-values, confidence
intervals, effect sizes, sample-size calculations, or statistical claims to
evaluate" and then scored it 5 out of 5, the highest such score in the corpus. A
forced score is not neutral, it is generous. Not applicable is also not a quiet
way of marking work down: thin or missing evidence is a low score. Only an area
the paper contains nothing of gets a not applicable.

## Reproducibility

Every review ships a `provenance.json` recording the provider, the model used at
each stage and any per-agent override, pipeline version and commit SHA, debate
rounds, which desk screens were active, per-reviewer scores, total cost and the
per-agent cost breakdown, and the resolved preprint metadata. Given the same
inputs you can re-run the panel yourself. Output will not be identical, since
the models are not deterministic, but the configuration is fully disclosed.

Not every stage runs on the same model, which is why the record is per stage.
Reading one model name off a review would misdescribe it.

Reviews are never silently edited. Where one is wrong, a human editor withdraws
it or annotates the page with what it got wrong, and the published bundle stays
byte-for-byte as it was; where a fresh run is warranted, the new review is
published beside the old one rather than over it.

A revision round adds a review; it never replaces one. The earlier round stays
published as the record of the draft it read, and each round records which
version it saw and a checksum of that exact file. Where a round ran without a
verified comparison against the previous draft, the page says so. See
[revision rounds](criteria.md#revision-rounds). Rounds are capped at three, past
which the submission is decided rather than cycled.

## Contesting a review

Comment on the review PR, or on your submission issue if it's already merged.

Nothing you write is shown to the panel. We removed author input deliberately
rather than never building it. See
[why](submit.md#why-we-do-not-accept-a-response-letter). Instead you get three
routes that do not send your words through an AI, described in full under
[if the review got something wrong](submit.md#if-the-review-got-something-wrong):

- **A right of reply.** We publish your response beside the review, labelled as
  yours. No AI reads it and it changes no score. This is the route for
  disagreeing with the judgement. We will not remove a recommendation because
  you dispute it, and your dissent sits next to it permanently.
- **Withdrawal or correction.** Where the panel clearly misread the paper, a
  human editor withdraws or annotates the review. A person decides. A statement
  about your paper that is factually false gets corrected or the review gets
  pulled, because that is the one failure we treat as disqualifying.
- **Re-review.** A fresh review of the unchanged paper with no author input,
  published alongside the original rather than replacing it.

## Conflicts and cost

The editor is one person running this out of pocket. Reviews are triggered
manually because each one costs real money. There is no queue guarantee, no SLA,
and no promise the project outlives the author's interest in it.

If a submission is the editor's own work, the review is labeled as such on its
page.

## Data

We store the preprint URL and its public metadata, the review bundle, the GitHub
issue thread, and your reply if you send one, which we publish beside the review
and keep permanently. We do not store PDFs. They are fetched to a temporary
directory at review time and deleted afterwards.

Paper text is sent to a third-party AI provider, currently Anthropic. Do not
submit anything you cannot send to a commercial API. Since we only take
already-public preprints, this should not come up.

## License

Reviews and site content are CC BY 4.0, so reuse them with attribution.
Preprints stay under whatever license their authors chose. We host none of them
and claim nothing over them.
