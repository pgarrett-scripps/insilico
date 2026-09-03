# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling drives pathological vascular maturation in RA synovia, and that TRK inhibitors can reverse this in tissue explants. The core statistical and data-handling infrastructure is substantially sound, but several load-bearing quantitative claims rest on analyses where the generating process introduces ambiguity that the design does not exclude. Most critically: the persistence of vascular maturation post-treatment is demonstrated on a 6-month window in a small paired cohort where the denominator (total synovial cells) itself changes with treatment, and the effect concentrates in exactly the subset where a normalization artefact would concentrate it. The in vitro work is better controlled but uses small n and lacks pre-registration. The paper would benefit from major revision addressing the denominator issue and providing raw effect sizes with confidence intervals throughout.

## Strengths

1. High-dimensional spatial transcriptomics on a paired pre/post-treatment cohort (n=22 RA patients) with careful cell-type annotation against a reference dataset, providing genuine spatial context absent from dissociated single-cell work.

2. Mechanistic pathway traced from NOTCH3 through NGF induction to NGFR-mediated TRKA sensitization, with multiple orthogonal validations (RNAscope, immunohistochemistry, siRNA knockdown, overexpression, pharmacologic inhibition).

3. FDA-approved drugs (larotrectinib, entrectinib) tested in human RA tissue explants rather than only cell lines, with quantified reductions in vascular density and mural cell markers.

## Weaknesses: Load-bearing claims

**Claim 1: Pathological vascular maturation persists despite immunosuppressive treatment.**

The evidence is quantification of vascular cell density and composition in pre- vs. post-treatment biopsies. The critical issue: density is calculated as "cell number per area" (Methods: "microvascular density is calculated by enumerating proportion of vascular cells as a function of total surface area"). This denominator is the total synovial cell count per biopsy, which itself is likely to change with treatment—immunosuppression depletes infiltrating immune cells (acknowledged in Introduction). If total cellularity drops while vascular cell count stays constant or drops less, the proportion rises automatically, independent of any change in vascular maturation per se. 

The authors report that post-treatment RA shows "statistically significant interval increase in density of capillary ECs (p=0.00036), arteriolar ECs (p=0.0065), pericytes (p=1.6e-05), and VSMCs (p=0.0031)" compared to healthy (Fig. 1G). They then report the same comparison as "absolute cell proportion changes" (Fig. 1H), which should be independent of total cellularity—but the text does not clearly state whether Fig. 1H uses the same denominator or a different one. If both use total synovial cells as denominator, the second analysis does not resolve the first problem. The pattern (increase in vascular cells post-treatment) is exactly what a depletion of immune cells would produce even if vascular maturation itself had regressed. 

To resolve this: report vascular cell counts in absolute numbers (cells per unit area) alongside proportions, and show that absolute vascular cell numbers do not decrease post-treatment. Alternatively, restrict the comparison to vascular cells only (density of pericytes relative to endothelial cells, not relative to all synovial cells), which would be immune to immune-cell depletion.

**Claim 2: Neurotrophins induce fibroblast-to-mural-cell differentiation.**

The in vitro evidence is substantial but relies on small sample sizes without pre-registered hypotheses. For example, NGF stimulation induces RGS5 (pericyte marker) at 1.3-fold (p=0.0006, Fig. 4A); BDNF induces MYH11 (VSMC marker) at 2.9-fold (p=0.0001, Fig. 4C). These p-values are reported without stating n (number of independent biological replicates per condition). The Methods state "Individual data points represent biological replicates" but do not specify how many. Figure 4 bar plots show error bars (stated as "mean ± standard deviation") but no raw points, making it impossible to verify the sample size or detect outliers. 

The collagen gel contraction assay (Fig. 4D–F) shows NT3 induces 21% contraction (p=0.002) and BDNF 16% (p=0.01), but again n is not stated in the figure legend or Methods section for this specific assay. The effect sizes are modest (16–21% contraction) and the p-values are not accompanied by confidence intervals or effect-size estimates (Cohen's d or similar). Without n and without raw data overlaid, these claims cannot be independently verified.

To resolve this: state n for each condition in every figure legend; overlay raw points on all bar plots; report 95% confidence intervals alongside p-values; pre-register the primary hypotheses and effect sizes before conducting the in vitro experiments.

**Claim 3: TRK inhibitors reverse vascular maturation in RA synovial explants.**

Treatment with larotrectinib or entrectinib reduced aSMA expression by 36% (p=0.044) and 40% (p=0.034), respectively, and reduced vascular density (PECAM1) by 54% (p=0.04) and 50% (p=0.031) (Fig. 6E). These are the headline results for the therapeutic claim. However, the sample size (n) for the explant experiments is not stated in the Methods or figure legends. The text says "Individual data points represent biological replicates" but does not specify how many explants were treated per condition. Without n, the degrees of freedom for the t-tests are unknown, and the p-values cannot be evaluated. Additionally, the comparison is vehicle-treated explants vs. drug-treated explants from the same cohort, but it is not stated whether explants came from the same patient (paired) or different patients (unpaired), which affects the appropriate statistical test.

To resolve this: state n (number of independent explants per condition) in the figure legend; specify whether the design is paired or unpaired; report effect sizes (% reduction with 95% CI) alongside p-values; show raw data points for each explant.

## Weaknesses: Sweep

1. **Multiple comparisons not corrected:** Fig. 1G compares vascular cell densities across 6 cell types and 3 groups (healthy, pre-treatment, post-treatment), yielding ~18 pairwise comparisons; no multiple-comparison correction (Bonferroni, FDR) is stated, yet p-values as low as 0.00036 are reported as if they are unadjusted.

2. **Xenium data analysis:** The integration of Xenium and scRNA-seq reference data uses Harmony for batch correction, but no validation of the correction is shown (e.g., no before/after UMAP, no mixing metric); the choice of resolution=0.3 for Louvain clustering is not justified.

3. **Gene signature scoring (UCell):** The NGF/NGFR gene signature (Fig. 5K–M) is derived from bulk RNA-seq of organoids treated with/without drug, but the manuscript does not state how many replicates were sequenced, whether replicates were pooled, or what the FDR threshold was for selecting the 461 "upregulated genes."

4. **RNAscope quantification:** Nuclei are segmented by Cellpose and expanded to approximate cell boundaries; no validation of segmentation accuracy is provided, and Cellpose parameters (model, diameter) are not stated.

5. **Immunohistochemistry scoring:** aSMA staining is quantified as "integrated aSMA staining density" (Fig. 6F) but the method (e.g., threshold, background subtraction, region of interest selection) is not described.

6. **NOTCH3 knockout:** CRISPR-Cas9 knockout efficiency is not reported; if knockout is incomplete, the claim that NOTCH3 is "required" for NGF induction is weakened.

7. **Fibroblast source:** Synovial fibroblasts are cultured from tissue (3–6 passages); passage number is not controlled across experiments, and passage-dependent drift in neurotrophin receptor expression is not addressed.

8. **Organoid viability:** Synovial explants are cultured for 3 days; no viability assay or histological assessment of cell death is provided, so it is unclear whether drug effects reflect true reversal of maturation or simply toxicity.

## Questions

1. In Fig. 1G–H, what is the denominator for the density calculation in each panel, and does it differ between the two figures?

2. For the in vitro experiments (Figs. 3–4), please provide n (number of biological replicates) for each condition in the figure legends, and overlay raw points on all bar plots.

3. For the explant experiments (Fig. 6), state n per condition, specify paired vs. unpaired design, and report whether explants from the same patient were treated with multiple drugs or only one.

4. What is the FDR threshold and replication number for the bulk RNA-seq used to define the NGF/NGFR gene signature in Fig. 5J?

5. Were the primary hypotheses (effect of NGF on RGS5, effect of BDNF on MYH11, effect of TRK inhibitors on aSMA) pre-registered before the experiments were conducted?