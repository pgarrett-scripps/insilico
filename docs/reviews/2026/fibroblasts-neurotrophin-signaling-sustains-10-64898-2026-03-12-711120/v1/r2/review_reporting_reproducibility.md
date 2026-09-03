# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling sustains pathological vascular maturation in RA synovia despite immunosuppressive therapy, and demonstrates that FDA-approved TRK inhibitors can reverse this maturation ex vivo. The core findings are supported by coherent spatial transcriptomics data and mechanistic experiments, but critical procedural details are missing or scattered, making independent reproduction difficult. Data availability is incomplete, and several load-bearing claims rest on results that cannot be fully verified from the text alone.

## Strengths

1. Comprehensive spatial transcriptomic profiling across 46 samples (22 RA patients with paired pre/post-treatment biopsies plus healthy controls) with clear cell-type annotation against a published reference dataset provides a solid foundation for the vascular maturation claim.

2. The mechanistic pathway is traced through multiple complementary approaches: spatial transcriptomics, RNAscope, immunohistochemistry, cell culture, co-culture, organoid explants, and pharmacologic perturbations, creating internal consistency across methods.

3. The authors transparently report that vascular maturation persists despite clinical improvement in some patients, and acknowledge the 6-month treatment window as a limitation rather than claiming definitive evidence of permanent resistance.

## Weaknesses: Load-bearing claims

**Claim 1: Neurotrophin receptors are expressed on synovial mural cells in RA and their expression persists despite treatment.**

The spatial transcriptomics data (Fig. 1, Fig. 2A) show NGFR and NTRK2 expression in mural cells at baseline and post-treatment. However, the quantitative evidence for *persistence* is not clearly separated from baseline expression. Figure 1H reports absolute cell proportions of VSMCs and pericytes increasing post-treatment, but does not report receptor expression levels (transcript count per cell) before and after treatment. The RNAscope validation (Fig. 2B) and immunohistochemistry (Fig. 2C) are shown as representative images without quantification of expression intensity or frequency across samples. The claim that expression "persists despite 6-months of immunosuppressive therapy" requires paired quantification of receptor expression in pre- and post-treatment samples from the same patients; the manuscript shows presence at both timepoints but not whether expression level changed. This distinction matters because upregulation post-treatment would strengthen the claim of active pathway engagement, while stable expression could reflect a baseline feature unrelated to treatment resistance.

**Claim 2: Neurotrophin stimulation induces fibroblasts to differentiate into mural cells, and this is the mechanism by which endothelial cells drive pathological vascular maturation in RA.**

Figure 4 demonstrates that NGF, BDNF, and NT3 induce mural cell markers (ACTA2, RGS5, MYH11, CNN1) in cultured fibroblasts and increase aSMA in synovial explants. However, the causal link between *fibroblast* differentiation and the *expansion of mural cells* observed in vivo (Fig. 1H) is not established. The spatial transcriptomics shows increased pericyte and VSMC density post-treatment, but does not demonstrate that these cells originated from fibroblasts rather than from recruitment, proliferation of existing mural cells, or endothelial-to-mesenchymal transition. The explant experiments (Fig. 4K) show increased aSMA staining with neurotrophin treatment, but aSMA is expressed by both VSMCs and activated fibroblasts; without lineage tracing or cell-type-specific markers distinguishing newly differentiated mural cells from pre-existing ones, the interpretation that fibroblasts are the source of the expanded mural compartment remains inferential. The co-culture experiments (Fig. 3) show fibroblasts adjacent to endothelial cells express neurotrophin receptors and mural markers, but do not prove these fibroblasts become functional mural cells or that they account for the mural cell expansion in vivo.

**Claim 3: TRK inhibitors reverse pathological vascular maturation in RA synovial explants.**

Figure 6 shows that larotrectinib and entrectinib reduce aSMA expression (36–40% reduction) and vascular density (24–27% reduction in vascular area, 50–54% reduction in PECAM1+ structures) in RA explants. However, the baseline vascular maturity of the explants used is not characterized. The explants are embedded in Matrigel and cultured for 3 days; it is unclear whether they represent the pre-treatment or post-treatment state, whether they were derived from the same patients whose tissue showed persistent maturation (Fig. 1), or whether the 3-day culture window is sufficient to observe meaningful reversal of an established pathological state. The reduction in PECAM1+ structures is substantial (50%), but PECAM1 marks all endothelial cells, not specifically mature ones; a reduction in endothelial density could reflect cell death, dedifferentiation, or loss of tissue viability rather than reversal of maturation. No viability assay or apoptosis marker is reported for the treated explants. The claim that TRK inhibitors "reverse" maturation (implying restoration toward a normal state) is stronger than the data support; the data show reduction in markers associated with maturation, not restoration of a pre-maturation phenotype.

## Weaknesses: Sweep

1. **Data availability:** The manuscript states Xenium data are available but does not provide a repository accession, link, or data availability statement; single-cell RNA-seq reference data from the AMP consortium are cited but the specific dataset version and access path are not given, and bulk RNA-seq from organoid experiments is mentioned but not deposited.

2. **Xenium analysis pipeline:** The cell segmentation, quality control thresholds (transcript and feature counts per cell), and integration procedure using Harmony are described, but the specific Seurat v5.0.0 parameters (resolution for Louvain clustering, distance metric for nearest-neighbor graph, UMAP parameters) are not provided, making the exact cell-type assignments non-reproducible.

3. **Statistical analysis of spatial data:** Figure 1G and 1H report p-values from Wilcoxon matched-pairs signed-rank tests, but the manuscript does not state whether multiple-comparison correction was applied across the six vascular cell types tested, nor does it report effect sizes or confidence intervals alongside p-values.

4. **RNAscope quantification:** The method for quantifying RNAscope signal (Fig. 2B, 3B, 3C) is described in Methods as nuclear segmentation via Cellpose followed by intensity normalization, but the threshold for calling a cell "positive" for a given transcript, the number of fields of view quantified per sample, and the number of samples analyzed are not stated.

5. **Fibroblast source and passage number:** Synovial fibroblasts are generated from tissue digestion and cultured for "3 to 6 passages"; passage number is known to affect fibroblast phenotype and responsiveness to stimuli, but experiments do not report which passage was used for each condition, nor is there a passage-matched control.

6. **DLL4 concentration and kinetics:** Figure 3 and 5 use DLL4 at 5 µg/mL to activate NOTCH signaling, but the dose-response relationship and time-course are not shown; it is unclear whether this concentration is saturating or whether the observed effects are specific to NOTCH3 or reflect off-target effects.

7. **NOTCH3 knockout validation:** CRISPR-Cas9 NOTCH3 KO cells are mentioned (Fig. 5E) but no validation of knockout efficiency (e.g., Western blot, qPCR) is provided in the main text or supplementary figures.

8. **Organoid culture duration and baseline state:** Synovial explants are cultured for 3 days before treatment; the manuscript does not report whether vascular structure, mural cell markers, or neurotrophin receptor expression change during the initial 3-day culture period, which could confound interpretation of drug effects.

## Questions

1. For the persistence claim (Claim 1): Can the authors provide quantification of NGFR, NTRK1, NTRK2, and NTRK3 transcript counts per cell (or fluorescence intensity per cell from RNAscope) in paired pre- and post-treatment samples, stratified by mural cell type?

2. For the fibroblast differentiation claim (Claim 2): Do the spatial transcriptomics data include a fibroblast lineage marker (e.g., THY1, FSP1) that would allow the authors to track whether newly expanded mural cells co-express fibroblast markers, or can lineage tracing be performed on a subset of explants?

3. For the TRK inhibitor claim (Claim 3): What is the viability (e.g., LDH release, caspase activity) of explants treated with larotrectinib and entrectinib at the concentrations used (1–10 µM), and do the explants retain endothelial and fibroblast markers after 3 days of culture and drug treatment?

4. Where are the Xenium raw data and processed count matrices deposited, and what is the accession number or persistent URL?

5. What are the exact Seurat v5.0.0 parameters (Louvain resolution, distance metric, UMAP parameters) used for cell-type annotation, and is the code available in a repository?