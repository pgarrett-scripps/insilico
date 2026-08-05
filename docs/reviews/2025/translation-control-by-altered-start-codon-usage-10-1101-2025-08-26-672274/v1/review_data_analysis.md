# Statistics & Data-Analysis Reviewer

## Summary
This is a well-executed experimental study with sound quantitative methods overall. The core claims about start codon usage and SigB regulation are supported by appropriate experiments and statistical tests. Minor issues with multiple-comparison correction and some undefined error bars prevent a higher score, but the work is solid and the conclusions are justified by the evidence presented.

## Strengths
- Acid survival experiments use proper replication (three independent experiments with technical duplicates) and report survival percentages with clear methodology, allowing verification of the rapid emergence of acid resistance.
- Translational reporter assays (Figures 4B–C) employ appropriate quantification with both fluorescence and Western blot confirmation, showing consistent dose-response patterns across three independent experiments.
- Genome-wide start codon analysis of 60,690 sequences is systematic and well-documented, with clear definitions of conserved genes (>95% presence) and flexible usage (>5% variation), providing a solid foundation for the population-level claims.

## Weaknesses
- The qPCR gene expression comparisons (Figure 2C–G) report fold-changes relative to MQ140025 with statistical significance markers but do not state the test used (paired t-test is mentioned only in the figure legend), do not report exact p-values, and do not apply multiple-comparison correction despite testing six genes across six strains—this is a HARD issue because the family size and correction method are not disclosed, making it impossible to verify whether the reported significances survive correction.
- The phylogenetic analysis of ST1 strains (Figure S1, lines 487–494) uses Parsnp2 to infer SNPs associated with branching points but does not report confidence intervals, bootstrap support, or sensitivity to alignment parameters, leaving the evolutionary trajectory claims (lines 354–363) resting on unvalidated tree topology.
- Motility assay (Figure 2B) categorizes strains as low, intermediate, or high motility but does not quantify the measurement (halo diameter, time to spread, or other metric) or report n for replicates, making the phenotypic grouping non-reproducible.
- The start codon usage analysis (Figure 5, Table S1) identifies 39 genes with flexible usage but does not report confidence intervals or statistical tests for the claim that these genes are enriched in virulence/stress pathways (13 of 39 = 33%) versus the genome background.
- Western blot quantification (Figure 4C) shows band intensities but does not state whether densitometry was used, how many replicates were quantified, or whether loading controls were normalized; the figure legend says 'protein samples were collected from three independent experiments' but does not clarify whether all three were quantified.
- Acid survival data (Figures 1C–G) plot percentage survival but do not define the error bars (SEM, SD, or CI) or state whether the three independent experiments were averaged before plotting or plotted separately.
- The reporter strain fluorescence assay (Figure 4B, 5C) normalizes to OD but does not report the absolute fluorescence values, making it impossible to assess whether the signal-to-noise ratio supports the claimed differences, especially for the ATT construct where 'no detectable signal' is claimed (line 244) without a threshold definition.

## Questions
- What multiple-comparison correction, if any, was applied to the six qPCR gene expression tests in Figure 2, and what are the exact p-values for each comparison?
- How were motility phenotypes quantified in Figure 2B, and how many independent replicates were assayed per strain?
- Were all three independent Western blot experiments (Figure 4C) quantified by densitometry, and if so, what was the inter-replicate variability?
- What defines 'no detectable signal' for the ATT construct in Figure 4B—a fluorescence threshold, a signal-to-noise ratio, or visual inspection of the Western blot?