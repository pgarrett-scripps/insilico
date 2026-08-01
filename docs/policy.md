# Editorial policy

## Standing

In Silico is an experiment in open machine-generated peer review. It is not
accredited, not indexed, and not a substitute for conventional peer review.
Do not cite an In Silico listing as evidence that a result is correct.

## Authority

**The panel is advisory. A human editor decides.**

The editor-in-chief agent produces a recommendation — accept, minor revision,
major revision, or reject — and that recommendation is published verbatim. It
does not bind anyone. A human editor reads the bundle, reads any author
response, and decides whether to publish it. Merging the review pull request is
that decision; there is no other step.

The editor may decline to publish a review that is incoherent, that misreads the
paper badly enough to be misleading, or that the panel produced from a truncated
or mangled ingest. Those failures happen and quietly shipping them would be
worse than dropping them.

## Scope

**In scope.** Computational and *in silico* work where the claims can be checked
by reading the paper and its code: simulation, modeling, method papers,
benchmarks, reanalyses, scientific software, and computational biology,
chemistry, and physics.

**Out of scope.** Clinical trials. Work whose central evidence is data no
referee can inspect. Anything where a wrong machine-generated review could
plausibly affect patient care — the panel has no business near that, and neither
do we.

We will decline submissions outside scope without running the panel.

## Known limitations

These are properties of the method, not bugs we expect to fix:

- **The panel cannot run your code.** Reproducibility scores reflect what the
  paper *claims* about availability, not verification.
- **It cannot check your math.** Derivations are assessed for plausibility and
  presentation, not correctness.
- **It cannot see figures.** Ingest is text-only via `pypdf`. Claims resting on
  a figure will be under-assessed.
- **Long papers are truncated.** There's a per-agent character budget;
  section-aware truncation keeps abstract/methods/results/discussion and drops
  appendices first.
- **Literature claims are search-grounded but not exhaustive.** The Novelty and
  Literature reviewers query real APIs, but absence of a hit is not evidence of
  novelty.
- **It has model-shaped biases.** It rewards conventional structure and clear
  writing. Unusual-but-correct work will likely score worse than it deserves.

## Reproducibility

Every review ships a `provenance.json` recording the provider, model id,
pipeline version and commit SHA, debate rounds, per-reviewer scores, total cost,
and the resolved preprint metadata. Given the same inputs you can re-run the
panel yourself. Outputs won't be byte-identical — the models aren't
deterministic — but the configuration is fully disclosed.

Reviews are never silently edited. Corrections are appended with a dated note.

## Contesting a review

Comment on the review PR, or on your submission issue if it's already merged.

- **The panel misread the paper** — say what it got wrong and where. A
  substantive correction can trigger a re-review; a re-review is published
  alongside the original, not in place of it.
- **You disagree with the judgment** — post your rebuttal. It gets linked from
  the review page. We won't remove a recommendation because you disagree with
  it.
- **A statement about your paper is factually false** — that gets corrected or
  the review gets pulled. Being wrong about what a paper says is the one failure
  mode we treat as disqualifying.

## Conflicts and cost

The editor is one person running this out of pocket. Reviews are triggered
manually because each one costs real money. There is no queue guarantee, no SLA,
and no promise the project outlives the author's interest in it.

If a submission is the editor's own work, the review is labeled as such on its
page.

## Data

We store: the preprint URL and its public metadata, the review bundle, and the
GitHub issue thread. We do not store manuscript PDFs — they're fetched into a
temporary directory at review time and deleted after.

Manuscript text is sent to a third-party model provider (currently Anthropic).
Don't submit anything you can't send to a commercial API. Since we only accept
already-public preprints, this shouldn't come up.

## License

Reviews and site content are CC BY 4.0 — reuse them with attribution.
Preprints remain under whatever license their authors chose; we host none of
them and claim nothing over them.
