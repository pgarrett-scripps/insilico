# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling sustains pathological vascular maturation in RA synovia despite immunosuppressive therapy, and demonstrates that FDA-approved TRK inhibitors can reverse this maturation ex vivo. The work is substantial and addresses an important clinical problem. However, critical load-bearing results lack sufficient procedural transparency and data accessibility to permit independent verification of the central claims, and key experimental choices that drive the conclusions are either incompletely specified or not justified.

## Strengths

1. The spatial transcriptomic profiling across 46 samples (22 RA patients with paired pre/post-treatment biopsies plus healthy controls) is a rigorous and well-powered approach to characterize synovial microvasculature in a clinically relevant context.

2. The mechanistic pathway from NOTCH3 → NGF induction → NGFR/TRK sensitization is traced through multiple complementary methods (spatial transcriptomics, RNAscope, immunohistochemistry, cell culture, siRNA knockdown, lentiviral overexpression, phosphorylation assays).

3. The functional validation that TRK inhibitors reverse vascular maturation in human RA synovial explants is clinically relevant and provides a potential therapeutic avenue.

## Major Weaknesses: Load-Bearing Claims

**Claim 1: Pathological vascular maturation persists despite immunosuppressive treatment and is independent of clinical remission.**

The evidence is the quantification in Figure 1G–H showing increased density of capillary ECs, arteriolar ECs, pericytes, and VSMCs in post-treatment RA compared to healthy controls. However, the manuscript does not report the critical comparison: pre-treatment vs. post-treatment within the same patients. Figure 1G presents three groups (healthy, pre-RA, post-RA) but the statistical test applied is "Wilcoxon matched-pairs signed-rank test for paired patient samples" — yet the figure legend and results text do not explicitly state which comparisons were tested. The p-values shown (e.g., "p = 0.00036; and p=0.0042 compared to healthy") appear to compare post-treatment to healthy, not pre- to post-treatment. If the authors tested pre vs. post and found no significant change, that would directly support persistence; if they tested post vs. healthy and found an increase, that only shows post-treatment RA differs from healthy, not that treatment failed to reduce it. The statement "interval increase in synovial microvascular density occurred in RA patients regardless of whether or not patients reached criteria for clinical remission" is not supported by a shown analysis stratifying by remission status. Without explicit pre-vs.-post comparisons and remission-stratified subgroup analysis, the claim that maturation *persists despite treatment* is not established — the data show post-treatment RA has more vasculature than healthy, which is weaker.

**Claim 2: Neurotrophin signaling is necessary and sufficient to drive fibroblast-to-mural-cell differentiation and vascular maturation in RA synovia.**

The sufficiency evidence comes from ex vivo synovial explant experiments (Figure 4K, Figure 6) where NGF, BDNF, or NT3 stimulation increases aSMA expression. However, aSMA is a marker of smooth muscle cells and myofibroblasts, not a definitive readout of mural cell identity or functional maturation. The authors show increased aSMA staining but do not report whether the cells expressing aSMA are newly differentiated from fibroblasts or represent activation of existing mural cells. RNAscope in Figure 6D shows reduced RGS5, ACTA2, and MYH11 after TRK inhibition, but the baseline expression of these markers in untreated explants is not quantified, making it unclear whether the inhibitor reduces a robust signal or a weak one. For necessity, the authors show that NOTCH3 knockdown reduces neurotrophin receptor expression (Figure 3C, Figure S7) and that DAPT (NOTCH inhibitor) reduces aSMA in explants (Figure 6A), but they do not directly block neurotrophin signaling in intact RA tissue and measure the consequence — they use selective TRK inhibitors in explants but do not show that blocking TRK signaling alone (without NOTCH inhibition) is sufficient to reverse maturation. The pan-TRK inhibitor GNF5837 does reduce aSMA (Figure S9F), but this is a single-agent experiment without dose-response or time-course, and the effect size (0.65-fold, p=0.04) is modest. The two FDA-approved inhibitors (larotrectinib, entrectinib) show larger effects (27–40% reductions in vascular area and aSMA intensity), but these are still ex vivo results in a 3-day culture system, not in vivo evidence that blocking neurotrophin signaling reverses established RA vascular pathology.

**Claim 3: NOTCH3 initiates neurotrophin signaling by inducing NGF expression and sensitizing TRKA signaling through NGFR transactivation.**

The evidence for NOTCH3 → NGF induction is that DLL4 stimulation upregulates NGF (Figure 5C, 1.2-fold, p=0.01), and DAPT or NOTCH3 knockout abolishes this (Figure 5D–E). This is solid. However, the evidence for NGFR-mediated sensitization of TRKA is indirect. The authors show that NGFR-overexpressing fibroblasts exhibit higher TRKA Y490 phosphorylation at baseline and with 1 ng/ml NGF (Figure 5G–H, 1.25-fold increase, p=0.04), and that these cells show enhanced pericyte marker expression at low NGF doses (Figure S8F–G). But this is an overexpression experiment in cultured fibroblasts, not evidence that endogenous NGFR levels in RA synovial fibroblasts are limiting for TRKA signaling. The authors note that NTRK1 expression is "extremely low" in synovial tissue (Figure 2C) and cultured fibroblasts (Figure 3C), yet they do not quantify NGFR expression or show that it is high enough to substantially enhance TRKA signaling at physiological NGF concentrations. The model proposes that low TRKA + high NGFR = sensitization, but the actual NGFR and TRKA protein levels in RA synovial fibroblasts are not reported. Without those measurements, the claim that NGFR transactivation is the mechanism by which fibroblasts sense NGF in vivo remains speculative — alternative mechanisms (e.g., paracrine TRKA signaling from other cells, or NGFR-independent NGF effects) are not excluded.

## Soft Weaknesses: Reproducibility & Specification

1. **Xenium data processing and cell typing:** The manuscript states that "single-cell analysis was performed using Seurat v5.0.0" and that integration was done with "Harmony v1.2.4," but does not provide the Seurat or Harmony parameters (e.g., resolution for Louvain clustering, number of PCs for Harmony, integration method). The statement "we robustly typed lineages and fine vascular cell states with our integrative annotation procedure" is vague; the procedure is described in text but the code is not cited or deposited. Reproducibility requires either the code or explicit parameter values.

2. **Custom spatial transcriptomic panels:** The manuscript mentions "custom add-on panels" and a "high-sensitivity, custom spatial transcriptomic panel (Table. S, 1 to 3)" but these tables are not provided in the manuscript text; they are referenced as supplementary but not shown, making it impossible to verify which genes were profiled or how probe design might affect results.

3. **Statistical comparisons in Figure 1G:** The figure shows p-values for multiple comparisons (healthy vs. pre-RA, healthy vs. post-RA, and implicitly pre-RA vs. post-RA) but does not state whether multiple-comparison correction was applied or which specific contrasts were tested with the "Wilcoxon matched-pairs signed-rank test."

4. **RNA-seq for NGFR signature:** The authors state they "performed bulk RNA-seq for the organoid with drug treatment and without drug treatment" to define the NGFR-related gene signature (Figure 5J), but do not provide the accession number, sequencing depth, or differential expression thresholds (e.g., how many genes were "top differentially expressed"?). The signature is said to comprise "461 upregulated genes" but the full list is not provided.

5. **Synovial organoid culture conditions:** The explant protocol states organoids were "cultured in EGM2 media" and "treated with various neurotrophins and their modulators" for "3 days," but does not specify the starting cell density, whether media was changed, oxygen tension, or whether organoids were embedded in Matrigel throughout or only initially. These details affect reproducibility.

6. **Fibroblast source and passage:** The manuscript uses "synovial fibroblast cell lines" generated from RA tissue and states they were "cultured and maintained (3 to 6 passages for experiments)," but does not specify which passage was used for each experiment, whether passage number was randomized, or whether results were consistent across passages.

7. **Data and code availability:** The manuscript does not state whether Xenium raw data, processed count matrices, Seurat objects, RNA-seq data, or analysis code will be deposited in a public repository (GEO, ArrayExpress, GitHub, etc.). The statement "available on request" is insufficient for a journal with reproducibility standards.

8. **Lentiviral transduction efficiency:** The NGFR overexpression experiments (Figure 5G–I, Figure S8F–G) use lentiviral transduction but do not report the transduction efficiency or whether sorted/selected populations were used, making it unclear what fraction of cells actually express the transgene.

## Questions

1. Figure 1G: Please report the exact statistical comparisons tested (pre-RA vs. post-RA, post-RA vs. healthy, etc.) and whether multiple-comparison correction was applied; if pre-RA vs. post-RA showed no significant change, that directly supports the persistence claim.

2. Figure 5J and related RNA-seq: What is the GEO or ArrayExpress accession for the bulk RNA-seq data, and what were the differential expression thresholds (FDR, log2 fold-change cutoff) used to define the 461-gene signature?

3. Figure 5G–H and Figure S8F–G: What are the endogenous protein levels of NGFR and TRKA in RA synovial fibroblasts, and how do they compare to the overexpression condition?

4. Will Xenium raw data, processed matrices, and analysis code be deposited in a public repository (GEO, GitHub, etc.), and if so, where and when?

---

**For the statistical reviewer:** The Wilcoxon matched-pairs test is appropriate for paired pre/post samples, but the manuscript does not clearly state which comparisons were tested or whether multiple-comparison correction was applied; this should be clarified in the figure legend and results.

**For the methods reviewer:** The Seurat and Harmony parameters (resolution, n_PCs, integration method) are not provided; either cite the code or specify these values explicitly so the clustering can be reproduced.