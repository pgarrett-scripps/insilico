# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

**Overall assessment from a statistics & data-analysis perspective**

The manuscript presents a compelling biological story supported by a rich proteomic dataset and a series of follow-up experiments. However, the quantitative evidence for the central claims—that Git1 regulates Grk2 translocation and Smo phosphorylation—is weakened by several statistical reporting gaps. The most critical issues are the lack of clear definitions for the independent unit of replication in key microscopy quantifications, the absence of multiple comparison corrections in the proteomic analysis, and the use of SEM in bar plots where SD would be more appropriate. These issues are fixable but require explicit reporting and, in some cases, re-analysis. The proteomic data processing is well-described, but the downstream statistical testing on the TMT data is underpowered for the number of comparisons made.

**Strengths**

1. The time-resolved TurboID proteomic design is well-conceived and provides a valuable resource for the field.
2. The authors clearly describe the normalization and scaling procedures for the TMT data, which is a strength for reproducibility.
3. The use of multiple Git1 knockout clones and shRNA constructs strengthens the genetic evidence for the phenotype.

**Weaknesses**

**Load-bearing claims**

1. **The claim that Git1 knockout reduces Grk2 translocation to the cilium (Fig. 5E) rests on a comparison of ciliary Grk2 intensity between WT and Git1-null cells.** The text states that "no detectable Grk2 was observed in the cilium of Git1-null cells at any time point," but the quantification in Fig. 5E shows a flat line near zero. The critical question is whether this is a true biological absence or a detection limit issue. The authors report n=90 cells/condition from three biological replicates. What is the independent unit of replication here? If these 90 cells come from three independent experiments, the effective n is 3, not 90. The two-way ANOVA used would be invalid if cells are treated as independent replicates. The authors must report the mean per biological replicate and test on those, or use a mixed-effects model that accounts for clustering. Without this, the p-values and the claim of "no detectable Grk2" are uninterpretable.

2. **The claim that Git1 knockout reduces Smo phosphorylation (Fig. 4E) and PKA-C recruitment (Fig. 4I) suffers from the same pseudo-replication issue.** The quantification of ciliary pSmo and PKA-C intensity is reported as n=100-150 cells/condition from three biological replicates. The two-way ANOVA is applied to these cell-level data. This is a classic pseudo-replication problem: cells within a culture dish are not independent. The authors should report the mean per biological replicate and perform the test on those three values per condition. The current analysis inflates the apparent sample size and likely produces artificially low p-values. The same issue applies to Fig. 3B, 3D, 5D, 5E, and 6F.

3. **The proteomic discovery (Fig. 2) lacks any correction for multiple hypothesis testing.** The volcano plots use a p-value threshold of 0.05 without any adjustment for the ~1070 proteins tested. At this threshold, one would expect ~50 false positives by chance alone. The authors should report the number of hits that survive a Benjamini-Hochberg correction (FDR < 0.05 or 0.01) or a Bonferroni correction. The current list of "top candidates" is not statistically defensible. The heatmap and box plots in Fig. 2D-E are descriptive but do not constitute evidence for enrichment without a corrected threshold.

**Sweep items**

- **Error bars in bar plots (e.g., Fig. 4E, 4G, 5D, 5E, 6F) are reported as SD but appear to be SEM in some panels (e.g., Fig. 5D, where the error bars are very small relative to the mean).** The figure legends state "mean ± SD," but the authors should verify this is consistent across all panels. If SEM was used, it should be replaced with SD or the raw data points should be shown.
- **The qPCR data in Fig. 6A and 7C show fold-change values without error bars on the control group (which is set to 1).** The control group has variance, and this should be shown, or the analysis should be done on the raw ΔCt values.
- **The Western blot quantifications in Fig. 6C-D report n=4 independent experiments, but the statistical test used is not stated in the figure legend.** The text says "two-way ANOVA followed by Tukey’s multiple comparison test," but this is a one-way design (WT vs Git1-null, with and without Shh). The test should be specified for each panel.
- **The EdU incorporation assay in Fig. 7E reports n=10 fields per condition.** Are these fields from the same coverslip or from independent experiments? If from the same coverslip, they are not independent. The unit of replication should be the biological replicate (e.g., independent GNP cultures), not the field.
- **The correlation plot in Fig. S2A shows high reproducibility across replicates, but the axes are labeled "Replicate 1" vs "Replicate 2" without specifying which channel.** This is a minor clarity issue.
- **The proteomic data processing uses TMM normalization, which is appropriate for RNA-seq but less standard for TMT proteomics.** The authors should justify this choice or cite precedent for its use in TMT data.

**Questions**

1. For the ciliary intensity quantifications (Figs. 4E, 4G, 5D, 5E, 6F), please report the mean and SD per biological replicate (n=3) and perform the statistical test on those three values. Alternatively, specify the mixed-effects model used and confirm that the reported n is the number of independent experiments, not cells.
2. For the proteomic data (Fig. 2), how many proteins survive a Benjamini-Hochberg correction at FDR < 0.05? Please provide a supplementary table with the adjusted p-values.
3. For the EdU assay (Fig. 7E), what is the independent unit of replication? If it is the field, please re-analyze using the mean per biological replicate.