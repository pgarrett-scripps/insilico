# Post-Debate Synthesis for the Editor

## Issue 1: Statistical support for the "broadly similar skill" / "viable alternative" claim

**Manuscript evidence:** Figure 2 (CRPS, energy score, graph energy score experiments over 84 initialization dates), text describing results as "broadly similar" with "small differences" in the extratropics and visible separation in the tropics (graph energy best, global energy degraded).

This concern was raised independently, in near-identical form, by all four scored reviewers (contribution, data_analysis, reporting_reproducibility, scientific_validity) — this is substantive duplication rather than four independent corroborations, since the underlying observation (no CIs, no significance test, single run, 84 dates) is the same fact cited each time.

**Advocate's case:** The abstract's actual wording ("suggest," "viable alternative," "broadly similar") is hedged and descriptive, not a formal equivalence claim; the manuscript openly reports the one place the pattern is not uniform (tropical asymmetry) rather than suppressing it. Honest disclosure of a directional exception is evidence against overclaiming, not for it.

**Skeptic's case:** The abstract's headline claim is functionally a claim of rough equivalence between training objectives, and every quantitative comparison supporting it rests on a single unreplicated run with zero error bars, seeds, or significance tests, despite 84 initialization dates being available for a bootstrap CI at no additional compute cost. Hedge words ("somewhat," "broadly") do not substitute for uncertainty quantification when the claim being hedged is itself the paper's central finding.

**Conceded:** The advocate conceded no CIs or seed-replication are reported and that this is a real gap; the advocate maintained this is fixable via analysis of existing runs (bootstrap CIs), not new experiments. The skeptic conceded the manuscript's reporting is honest about the directional tropical exception and does not conceal the composite objective.

**Status:** Unresolved on severity, but both sides agree it is **fixable without new experiments** — bootstrap confidence intervals over the 84 existing initialization dates and/or a stated equivalence margin would materially strengthen or narrow the claim. Not resolved as to whether the claim as currently worded is adequately supported in the meantime.

## Issue 2: Graph energy score's tropical advantage confounded with its global fES anchor

**Manuscript evidence:** The graph energy score experiment uses a composite objective (documented in Table 1) combining localized graph energy score with a 0.1×fES global anchor, added because the graph score "may fail to be strictly proper." No experiment tests the graph component alone.

Raised independently by contribution, scientific_validity, and reporting_reproducibility reviewers using substantially the same reasoning — again, one underlying observation restated three times rather than three independent lines of evidence.

**Advocate's case:** This is a legitimate limitation on the *mechanistic* interpretation (why the graph score wins in the tropics) but does not undermine the *skill-comparison* finding, since the composite objective is transparently reported and run exactly as specified — the paper never claims the graph mechanism alone is responsible.

**Skeptic's case:** This is not a data-analysis fix but a missing experiment (a new training run isolating fGES_graph without the anchor), and it specifically undercuts the one favorable result the paper leans on to argue multivariate objectives are "viable" rather than merely non-catastrophic. The causal story behind the paper's strongest positive finding is untested.

**Conceded:** The advocate conceded this in round 1 and maintained the concession throughout — it is a real limitation on mechanistic interpretation. The skeptic conceded the comparison as specified (composite objective vs. CRPS) is fair and the design is not unsound.

**Status:** **Unresolved, and agreed by both sides to require new training runs to fix** (not analysis of existing data). Both sides agree this does not invalidate the skill-comparison as run, but does prevent attributing the tropical advantage to the graph localization mechanism the paper is nominally validating.

## Issue 3: Scale-aware losses "substantially improve" spectral realism

**Manuscript evidence:** Figures 3–14 (accumulated tendency spectra across 12 configurations), with the manuscript's own hedges: "differences between scale-aware loss objectives are comparatively small," some experiments show "overcompensation," and the authors attribute observed differences partly to "different effective weights per scale" rather than to the scoring mechanism itself.

This claim was raised by all four scored reviewers in substantially overlapping terms (no quantitative summary metric, no error bars, ad hoc/untuned weighting confounds mechanism vs. weight-magnitude effects) — again one underlying observation, not independent corroboration.

**Status:** **Not engaged in the debate transcript.** Neither advocate nor skeptic addressed this issue directly in the exchanges provided; the debate concentrated on Issue 1 and Issue 2. This should not be read as resolved — it stands as a reviewer-identified gap (lack of quantitative spectral summary statistic, no separation of weighting-choice effects from scale-awareness-mechanism effects) that the editor should weigh on the reports' merits.

## Additional concerns raised but not engaged in debate

- **Compute-parity confound** (raised by skeptic r1 in passing, not picked up by advocate or skeptic r2 substantively): whether graph/edge-based losses' extra neighbourhood computation per step alters effective training under a nominally identical schedule. Advocate r2 called this "speculative" but this exchange did not develop into a resolved position either way — it remains an open question flagged by only one voice.
- **Reproducibility/code availability** (no repository, version, or commit hash for the Anemoi implementation) — raised by reporting_reproducibility, not discussed in debate at all.
- **Missing baseline comparison** (no climatology/persistence baseline; CRPS values not reported numerically) — raised by data_analysis, not discussed in debate.
- **Hyperparameter justification** (k=16 neighbourhood, kernel widths, α=0.95 for almost-fair CRPS, 0.1 anchor weight) — raised across multiple reports as an unablated sweep item, not discussed in debate.
- **Missing comparison to Pacchiardi et al.'s patched energy score**, cited by the manuscript as motivating context but never benchmarked against — raised by contribution and scientific_validity reviewers, not discussed in debate.
- **Ethics reviewer** found no applicable concerns; not contested.