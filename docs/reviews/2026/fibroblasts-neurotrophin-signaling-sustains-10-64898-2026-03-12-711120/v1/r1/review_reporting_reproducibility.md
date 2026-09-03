# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling, regulated by NOTCH3, drives pathological vascular maturation in RA synovial tissue and persists despite immunosuppressive therapy. The core finding—that TRK inhibitors reverse this maturation in explants—is potentially valuable, but critical load-bearing claims rest on evidence that cannot be fully reconstructed from the methods provided, and key mechanistic steps lack sufficient procedural specificity to verify independently.

## Strengths

1. The spatial transcriptomic dataset is large (2M+ cells across 46 samples with paired pre/post-treatment biopsies) and the cell-type annotation pipeline is described with reference to published integration methods.

2. The authors validate neurotrophin receptor expression across multiple orthogonal modalities (spatial transcriptomics, RNAscope, immunohistochemistry, Western blot) and test pharmacological effects with both selective and pan-inhibitors.

3. The explant system preserves tissue architecture and endogenous cell-cell interactions, making the functional readout (aSMA staining, vascular density) more physiologically relevant than isolated cell culture alone.

## Weaknesses: Load-Bearing Claims

**Claim 1: Neurotrophin signaling is necessary and sufficient to induce fibroblast-to-mural-cell differentiation.**

The evidence rests on three types of experiment: (i) fibroblasts stimulated with recombinant NGF/BDNF/NT3 upregulate mural cell markers; (ii) siRNA knockdown of neurotrophin receptors blocks this response; (iii) explants treated with neurotrophins show increased aSMA. However, the manuscript does not establish that the fibroblasts actually *differentiate* into functional mural cells—only that they express mural cell markers. The collagen gel contraction assay (Fig. 4D–F) tests contractility, but contractility is not unique to VSMCs and does not prove lineage conversion. Critically, the authors do not show that fibroblasts expressing mural markers physically integrate into vascular structures, adopt the spatial organization of native mural cells, or acquire the full transcriptomic signature of pericytes or VSMCs. The RNAscope images (Fig. 3A, 4K) show marker expression but do not quantify the proportion of fibroblasts that convert or demonstrate that converted cells remain stable. An alternative explanation is that neurotrophins induce a partial, reversible transcriptional program in fibroblasts that mimics mural cell identity without true lineage commitment. To resolve this: report the proportion of fibroblasts expressing both fibroblast and mural markers simultaneously before and after neurotrophin treatment, quantify stability of marker expression over time in culture, and perform single-cell RNA-seq on treated fibroblasts to compare their transcriptome to primary pericytes and VSMCs.

**Claim 2: NOTCH3 initiates neurotrophin signaling by inducing NGF expression, and NGFR potentiates TRKA signaling to sensitize fibroblasts to low-dose NGF.**

The evidence for NOTCH3 → NGF induction is solid (DLL4 stimulation, DAPT inhibition, NOTCH3 knockout all reduce NGF; Fig. 5C–E). However, the mechanism by which NGFR potentiates TRKA signaling is inferred from phosphorylation data in overexpression cells, not demonstrated mechanistically. Figure 5G–H shows that NGFR-overexpressing fibroblasts exhibit higher pY-TRKA at baseline and with 1 ng/ml NGF, but the authors do not show direct binding, complex formation, or kinetic parameters. The claim that NGFR acts as a "co-receptor" relies on a citation (ref. 33) to prior work in neurons; whether this mechanism operates identically in fibroblasts is not tested. Moreover, the baseline phosphorylation increase in NGFR-overexpressing cells (Fig. 5H) raises the question of whether NGFR is simply increasing TRKA expression or stability rather than enhancing ligand binding. To resolve this: perform co-immunoprecipitation of NGFR and TRKA in fibroblasts, measure TRKA protein levels in NGFR-overexpressing cells, and test whether NGFR overexpression enhances NGF binding affinity using surface plasmon resonance or similar biophysical assay.

**Claim 3: FDA-approved TRK inhibitors larotrectinib and entrectinib reverse pathological vascular maturation in RA synovial explants.**

The evidence is aSMA staining intensity and PECAM1+ vascular density in explants treated with these drugs (Fig. 6C–G). The reduction in aSMA (36–40%) and vascular density (50–54%) is quantified, but the manuscript does not report whether these changes are accompanied by loss of endothelial cell viability, apoptosis, or non-specific tissue damage. TRK inhibitors are broad kinase inhibitors; off-target effects on other receptor tyrosine kinases (FGFR, VEGFR, etc.) expressed in synovial tissue are not ruled out. The explant culture duration is 3 days; whether the effect persists longer, whether mural cells re-accumulate after drug withdrawal, and whether the vascular structures that remain are functionally immature are not tested. The authors show that DAPT (NOTCH inhibitor) also reduces aSMA (Fig. 6A), but do not compare the magnitude or kinetics of the two approaches, making it unclear whether TRK inhibition is more selective or effective than NOTCH inhibition. To resolve this: perform apoptosis assays (TUNEL, caspase staining) and measure endothelial cell markers (CD31, VE-cadherin) alongside aSMA in drug-treated explants; test off-target kinase inhibition using selective inhibitors for FGFR and VEGFR; extend culture to 7–14 days and assess reversibility after drug washout; and directly compare aSMA reduction with DAPT versus TRK inhibitors in the same explant cohort.

## Weaknesses: Sweep

1. **Xenium data processing and integration:** The authors state they "robustly typed lineages and fine vascular cell states" using Harmony integration and Louvain clustering at resolution 0.3, but do not justify this resolution choice, report silhouette scores, or show sensitivity analysis; reproducibility requires these details and the code/parameters used.

2. **Cell segmentation validation:** Xenium cell segmentation is performed by the instrument software (Cellpose-based), but the authors do not report segmentation accuracy, false-positive/negative rates, or manual validation on a subset of images, which is critical for spatial analysis claims.

3. **Statistical testing and multiple comparisons:** Many figures report p-values from Wilcoxon or t-tests without stating whether multiple-comparison correction was applied across all tests in a figure or experiment; Methods state Bonferroni correction "to control for multiple comparisons" but do not specify which tests were corrected.

4. **Fibroblast source and passage number:** The authors state fibroblasts were cultured "3 to 6 passages for experiments" but do not report whether passage number was randomized across conditions or whether results differ by passage, which affects reproducibility and generalizability.

5. **Neurotrophin ligand concentrations:** NGF, BDNF, and NT3 are tested at different concentrations (NGF 1–100 ng/ml, BDNF 100 ng/ml, NT3 50–100 ng/ml); the rationale for these choices and whether dose-response curves were generated are not stated.

6. **RNAscope quantification:** The authors describe using Cellpose for nuclear segmentation and "nuclear expansion to approximate cell boundaries," but do not report the expansion radius, validation of this approximation against manual segmentation, or inter-rater reliability.

7. **Bulk RNA-seq for NGFR signature:** The authors generated an NGF/NGFR gene signature from bulk RNA-seq of organoids treated with/without drug (Methods, "Single cell signature scoring"), but do not deposit the RNA-seq data, report sequencing depth, or provide the list of 461 upregulated genes, preventing independent validation of the UCell scoring.

8. **Lentiviral transduction efficiency:** NGFR overexpression is achieved via lentiviral transduction, but the authors do not report transduction efficiency, selection method (blasticidin resistance is mentioned but not quantified), or whether all downstream experiments used sorted or selected populations.

## Questions

1. Figure 5J reports bulk RNA-seq of NGFR-overexpressing fibroblasts; where is this RNA-seq data deposited, and what are the exact criteria for calling genes "upregulated" (fold-change threshold, adjusted p-value cutoff)?

2. In the fibroblast-endothelial co-culture (Fig. 3A–B), how were fibroblasts "in the proximal 1–2 cell layers away from the nearest endothelial cells" identified and quantified—was this done computationally from spatial coordinates, and if so, what distance threshold defines "proximal"?

3. Figure 1G reports "statistically significant interval increase" in capillary and arteriolar ECs post-treatment; were these comparisons corrected for multiple testing across all six vascular cell subtypes, and if so, what was the corrected α?