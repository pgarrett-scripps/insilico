# Post-Debate Synthesis for Editor

## Issue 1: Whether "persistence despite treatment" is the comparison the data actually show

**Evidence cited:** Fig. 1G p-values for capillary EC, arteriolar EC, pericyte, and VSMC density, reported in-text with paired values (e.g., "pericytes p=1.6e-05, p=0.029 compared to healthy"); Methods state a paired Wilcoxon signed-rank test was used "for paired patient samples."

**Reviewer origin:** Raised independently by data_analysis (multiple-comparison correction) and reporting_reproducibility (ambiguity over which contrast is tested); these are related but distinct concerns and should not be treated as one voice — one is about correction, the other about whether the pre-vs-post contrast is shown at all.

**Advocate's case:** The dual p-values per cell type likely represent (1) the paired pre-vs-post contrast and (2) the unpaired comparison to healthy controls; this is a labeling-clarity problem, not a missing analysis. Several effects (pericytes, VSMCs) would survive Bonferroni correction across ~12 tests even on the conservative reading.

**Skeptic's case:** The manuscript's own text explicitly labels only the second p-value in each pair as "compared to healthy," leaving the first p-value's referent undisambiguated in the quoted text. The clinical hook — "6 months of immunosuppressive treatment... did not reduce the density" — depends specifically on a within-patient pre-vs-post contrast that is never unambiguously identified as such. The advocate's Bonferroni defense addresses the healthy-vs-post comparison, not the persistence claim being sold in the abstract.

**Conceded:** The advocate conceded nothing new here beyond the initial argument; the skeptic conceded that *some* effects would likely survive correction regardless of which contrast is meant.

**Status: Unresolved.** No debater produced a passage where the manuscript explicitly reports a pre-vs-post p-value distinguishable from the healthy comparison. This bears on whether the central motivating claim of the paper (treatment-resistant vascular pathology) is textually supported as stated, independent of whether the underlying effect is likely real. Would be resolved by the authors explicitly labeling each contrast and its correction method in the figure legend/text.

## Issue 2: Whether "reversal" (TRK inhibitor explant data) is the correct characterization

**Evidence cited:** Fig. 6C–G (3-day explant treatment with larotrectinib/entrectinib reducing aSMA and PECAM1 signal); Discussion language ("TRK inhibitors effectively reverses vascular maturation"); Fig. 6 title ("Reversal of pathological vascular maturation"); Fig. S9B (WST-1 viability assay, no cytotoxicity below 100 µM); Fig. S9C–F (bidirectional pharmacology — agonists increase, antagonists decrease aSMA).

**Reviewer origin:** Raised independently by contribution_context, scientific_validity, and reporting_reproducibility — this is a genuine cluster of independent convergence (three separate specialist framings: novelty/durability, causal sufficiency, and quantification precision) all landing on the same underlying gap, though each emphasizes a different facet (durability of effect; RA-specificity; measurement definition).

**Advocate's case:** The manuscript's own viability data (Fig. S9B) and bidirectional pharmacology (agonists vs. antagonists producing opposite effects) make nonspecific toxicity an implausible sole explanation; "reversal" should be softened to "acute suppression" as a revision, but this does not undermine the mechanism itself.

**Skeptic's case:** The viability assay and bidirectional pharmacology address cytotoxicity as a *global* explanation but do not distinguish dedifferentiation from selective loss of newly differentiated mural cells specifically, nor establish RA-specificity (no healthy-donor explant comparator is reported by any reviewer). The manuscript's own language ("reverses," "Reversal of pathological vascular maturation" as a figure title) is unhedged, so this is not merely an advocate-proposed softening but a discrepancy between claim and evidence as currently worded.

**Conceded:** Advocate conceded "reversal" should be softened to "acute suppression" in revision. Skeptic conceded the mechanistic chain up to receptor induction is well-supported and that cytotoxicity is not the most likely explanation, only that it remains formally unexcluded for the specific dedifferentiation-vs-loss question.

**Status: Unresolved but not fatal to the underlying pharmacology** — both sides agree the direction of the drug effect is credible; the dispute is over whether "reversal" (implying restoration toward a normal, non-pathological state) is supported versus a narrower "acute suppression of markers in short-term culture." No debater identified a healthy-donor explant control or lineage-tracing/single-cell data in the manuscript that would adjudicate dedifferentiation vs. selective cell loss. This is a wording/scope-of-claim issue rather than a refutation of the pharmacological finding itself.

## Issue 3: NOTCH3→NGF transactivation mechanism

**Evidence cited:** Fig. 5C–E (DLL4 stimulation, DAPT, NOTCH3 KO effects on NGF expression, 1.2-fold, p=0.01).

**Raised by:** scientific_validity (no direct promoter/enhancer evidence of NOTCH3 transactivation of NGF; indirect effects via fibroblast survival/state not excluded) and data_analysis (no stated sample size, marginal fold-change/p-value, ambiguity whether Fig. 5C/5D are independent replicates).

**Debate treatment:** Advocate cited this pathway as an example of "unusually complete" convergent evidence; skeptic conceded the triangulation is "consistent with NOTCH activation" but did not concede it establishes direct transactivation. This point was raised but not fully argued through in debate — treated as background support for the acceptance case rather than contested on its own terms.

**Status: Unresolved, minor relative to Issues 1–2.** Would be resolved by reporting sample sizes/CIs and, ideally, direct promoter occupancy evidence or single-cell timing data, as requested by scientific_validity.

## Concerns raised in reports but not engaged in debate

These were not discussed by either debater and should not be read as resolved:

- **Novelty framing** (contribution_context): whether the NOTCH3→NGF→mural cell axis is RA-specific or a recapitulation of known developmental neurotrophin-vascular biology; no comparison to normal/developing vasculature is offered.
- **Multiple uncorrected/underspecified statistics throughout** (data_analysis): Fig. 5C–E and Fig. 6E–G lack stated sample sizes, CIs, and precise quantification definitions (e.g., "aSMA intensity" undefined); Fig. 1H's two p-values per comparison are ambiguous.
- **Data/code availability**: no repository accession stated for Xenium data, RNA-seq (461-gene NGFR signature), or analysis code; "available on request" flagged as insufficient (reporting_reproducibility).
- **NGFR/TRKA endogenous protein levels** in RA fibroblasts not reported, leaving the "sensitization" model partly inferential from overexpression data (reporting_reproducibility, scientific_validity).
- **TRK inhibitor isoform selectivity and off-target kinase effects** (larotrectinib/entrectinib affecting TRKA/B/C and potentially other kinases) not addressed (contribution_context, scientific_validity).
- **Single-cohort spatial transcriptomics** with no independent validation cohort (contribution_context).
- **Ethics/compliance**: no issues raised; IRB approval and funding disclosure confirmed adequate, with only a soft note on absent data-sharing statement.