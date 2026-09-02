# Area Chair Brief for Editor

## Overview
Five reviews (contribution/context, data/analysis, ethics, reporting/reproducibility, scientific validity) converge on a consistent picture: a methodologically rigorous chemical proteomics study extending ABPP to primary brain cells, with a genuinely multi-modal HCN channel finding and a well-controlled DPYSL2 complexoform result. No reviewer identified fabricated or logically unsupported data. All substantive weaknesses are described by reviewers as fixable via rewording, additional quantification of data already collected, or explicit disclosure — not new experiments, with one contested exception (below). The debate (one advocate, one skeptic, two rounds each) tested whether these weaknesses are truly minor or load-bearing enough to undercut headline claims.

## Issue 1: "Spares basal activity" claim vs. hippocampal slice data (central debate issue)

**Manuscript evidence cited:** Heterologous patch-clamp (Fig 6B–D) shows WX-02-679 alone gives HCN2 V₁/₂ = −95.0 ± 1.8 mV vs. DMSO control −92.1 ± 2.0 mV (statistically indistinguishable), while blocking the cAMP-induced shift to −83.5 mV — the load-bearing evidence for "basal activity spared." Separately, hippocampal slice recordings (Fig 6J–K, S6E–F) show WX-02-679 alone (no exogenous cAMP) produces a stereoselective *decrease* in sag ratio, rebound depolarization, and changes to resting membrane potential, input resistance, and firing frequency. The Discussion attributes this to "loss of the tonic depolarizing Ih."

**Strongest case for concern (skeptic, echoed independently by scientific_validity reviewer):** This is not an incidental phrase but a Highlight-level differentiator claim (positioning the compound against pore blockers like ivabradine). The slice data show a measured change in *basal* Ih in native tissue — the only ex vivo readout in the paper — which is in tension with a "basal-sparing" claim stated generally. The Discussion's own explanation ("loss of tonic depolarizing Ih") concedes the point the Highlight denies.

**Strongest case for dismissal/limitation (advocate):** The heterologous data are the direct, controlled test of the basal-sparing claim (compound alone vs. vehicle alone, no cAMP) and hold up cleanly across three isoforms and two species. The slice result addresses a different, harder question — native neurons where a fraction of channels may be tonically cAMP-modulated — and represents a boundary condition rather than a direct contradiction.

**Concessions:** Advocate conceded the Highlight-level wording is broader than what the slice data support and that this is a genuine problem, not something arguable away. Skeptic conceded the HCN mechanistic work and DPYSL2 findings are genuinely multi-modal, not single-assay artifacts.

**Status: Unresolved but classified by both sides as fixable, not fatal.** Both debaters agree on the remedy in principle — either reconcile the discrepancy (e.g., direct voltage-clamp measurement of Ih amplitude without cAMP in slices) or narrow the claim to the heterologous-cell dataset where it is supported — but disagree on whether this can be done by rewording alone (advocate) or requires a clarifying analysis/experiment before publication (skeptic). This directly duplicates a concern raised independently by the scientific_validity report (internal contradiction) and, more narrowly, by data_analysis and reporting_reproducibility reports (effect-size/mechanism questions around the same figures) — these are one underlying issue, not three corroborating ones.

## Issue 2: Possible pseudoreplication in hippocampal slice recordings

**Manuscript evidence cited:** Fig 6J–K reports N=8–10 cells per condition without stated animal count (raised independently by data_analysis reviewer, Q5).

**Debate treatment:** Skeptic raised this as compounding the Issue 1 problem: if this is exactly the experiment meant to test the basal-activity question, and few animals contributed many cells, the statistics underlying that specific claim are undermined. Advocate initially treated all such gaps as answerable by mining existing data; skeptic countered that this specific gap cannot be fixed by reanalysis alone — if pseudoreplication is real, new recordings may be needed.

**Status: Unresolved.** No consensus reached on whether disclosure alone (reporting animal-level n) suffices or whether new data collection is required; this depends on facts not stated in the manuscript.

## Issue 3: Brainocyte-restricted liganding as artifact of dissociation vs. genuine cell-context effect

**Manuscript evidence cited:** Fig 1D (28 brainocyte-unique proteins), Fig S1D ("pilot" acute slice validation of only 7 of 28 candidates, described qualitatively as "generally recapitulated"), Fig S2A (lower overall probe uptake in brainocytes, unquantified).

**Debate treatment:** Skeptic raised this in round one as a third, compounding weakness; this duplicates near-identical concerns independently raised by all five reviewer reports (contribution/context, data_analysis, ethics is silent, reporting_reproducibility, scientific_validity) — this is the most heavily repeated concern across the whole review, but as one substantive issue, not five independent corroborations. Advocate's response folded this into the general "addressable by mining existing data" defense (quantify replication rate from Dataset S2) without specific rebuttal.

**Status: Unresolved, not directly contested.** Both sides treat this as fixable by disclosure/quantification, but the debate did not resolve whether a "pilot" 7/28 validation is sufficient support for the manuscript's claim of "improved access to proteins with restricted expression in the nervous system," or whether the lower-uptake confound (Fig S2A) has been adequately excluded.

## Issue 4: Stereoprobe off-target specificity in slice preparation

Raised by skeptic in closing as a collective blind spot: every reviewer independently flags general stereoprobe specificity/off-target concerns (contribution/context Q4, scientific_validity sweep, reporting_reproducibility), but none confirms an orthogonal check for off-target cysteine engagement specifically in the slice preparation. **Never engaged by the advocate or resolved in debate.**

## Concerns from reports not engaged in debate

- DPYSL2:DPYSL5 complex stoichiometry/abundance not quantified (data_analysis, reporting_reproducibility, contribution/context all raise this independently — same underlying issue).
- No FDR/multiple-comparison correction reported for the 2.5-fold liganding threshold or IP-MS co-enrichment list (data_analysis).
- HCN cysteine mutants (C542A etc.) show poor/cAMP-independent conductance, precluding direct validation that the liganded cysteine is functionally necessary (raised by contribution/context, reporting_reproducibility, scientific_validity — same issue, acknowledged by authors in-text but not resolved).
- Relaxed cysteine-ABPP blockade threshold (33% vs. prior 50%) lacks empirical justification (data_analysis, reporting_reproducibility).
- Proteomic search pipeline parameters incompletely specified, limiting reproducibility (reporting_reproducibility).
- CNS-enrichment classification thresholds are post-hoc without sensitivity analysis (reporting_reproducibility).
- PDE7B enzymatic null result lacks assay sensitivity/positive control (data_analysis).
- Ethics/compliance: no issues raised; uncontested 5/5.