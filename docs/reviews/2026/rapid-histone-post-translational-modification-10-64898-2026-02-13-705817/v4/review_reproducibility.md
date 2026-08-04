# Reproducibility Reviewer

## Summary
This manuscript presents RIPUP, a streamlined multi-protease workflow for histone PTM analysis, with systematic evaluation of alternative proteases and labeling strategies. From a reproducibility standpoint, the work is substantially transparent: raw MS data are deposited in ProteomeXchange (PXD073683), custom R scripts are available on GitHub, and the computational framework (HiP-Frag via FragPipe) is publicly accessible. However, several procedural gaps and ambiguities prevent full end-to-end reproducibility without author contact. Key issues include incomplete specification of FragPipe parameter configurations, missing details on kNN imputation thresholds and missing-data handling logic, and lack of clarity on how artifact-stripping and canonical-mapping decisions were implemented. The hippocampal proof-of-concept lacks sufficient procedural detail to replicate independently. These are fixable but represent SOFT-to-borderline-HARD barriers to replication.

## Strengths
- Raw MS data deposited in ProteomeXchange with accession PXD073683, enabling access to load-bearing empirical datasets.
- Custom R scripts for data analysis publicly available on GitHub (https://github.com/NataliePTurner/Histone-RIPUP), supporting reproducibility of statistical and quantitative analyses.
- Detailed FragPipe search parameters provided in SI Table S1, including mass offsets, variable modifications, and FDR thresholds (1% PSM and peptide level).
- Software versions specified for key tools: FragPipe v24.0, RStudio 2025.09.2+, Skyline v26.1.0.057, and limma package identified for statistical testing.
- Quantitative analysis workflow clearly described with explicit normalization (histone-level scaling to grand mean), log2 transformation, kNN imputation parameters (k=10), and statistical method (limma with Benjamini–Hochberg correction).
- LC-MS/MS instrument configuration and acquisition parameters fully specified (Fusion Lumos, DDA settings, collision energies, resolution, isolation window).
- Protease digestion conditions systematically documented in Tables S1 and S2 with enzyme-to-substrate ratios, incubation times, temperatures, and buffer compositions.
- Biological sample collection and handling procedures detailed with IACUC approval, animal numbers, and tissue preparation protocols.

## Weaknesses
- FragPipe search configuration incompletely specified: while SI Table S1 lists mass offsets, the exact command-line parameters, search engine selection (MSFragger vs. Comet), and database search settings (e.g., precursor mass tolerance, fragment mass tolerance settings beyond the stated 10 ppm and 20 ppm) are not fully documented in the main text or supplementary methods, requiring reference to external FragPipe documentation or author contact.
- kNN imputation logic under-specified: the manuscript states 'restricted to dose groups where at least 2 of 3 replicates had measured values' but does not clarify whether k=10 was applied uniformly across all samples or adjusted per dose group, nor is the rationale for k=10 justified or sensitivity tested.
- Artifact-stripping procedure vaguely described: 'all artifact-bearing forms of each peptidoform (Met oxidation, dehydration) were collapsed to a single biological modification state by stripping artifact masses' — the exact algorithm, order of operations, and handling of ambiguous cases (e.g., a peptide with both Met oxidation and a biological modification) are not specified.
- Canonical mapping for histone variants not procedurally detailed: 'For histone variants producing near-identical peptide sequences at the same protein positions (e.g., H2B type 1-J and H2B type 3-B), intensities were summed after canonical mapping' — the mapping rules, decision tree, and edge cases are not provided, making this step difficult to replicate.
- Hippocampal tissue analysis lacks procedural completeness: the proof-of-concept experiment (Figure 8) uses 'Arg-C Ultra (1:10) and r-Chymotrypsin (1:10) in 20 µL reactions' but does not specify histone input mass, buffer composition, or whether propionylation was applied, creating ambiguity about exact conditions.
- Missing-data imputation scope unclear: the manuscript states groups with '0 or 1 measured replicates were left as missing' but does not specify how many peptidoforms fell into this category or how they were handled in downstream visualization (e.g., Figure 7), potentially affecting reproducibility of quantitative results.
- Dose-response concordance analysis (Figure 7B, 7D) computed as Pearson correlation but the statistical significance, confidence intervals, or sensitivity to outliers are not reported, limiting reproducibility of this key validation step.
- Motif analysis for missed cleavage (SI Figures S6–S7) references enrichment calculations but does not specify the statistical test, background model, or p-value thresholds used to define 'enriched' residues.
- No random seed or seed-averaging statement provided for kNN imputation or any stochastic steps in the analysis pipeline, potentially affecting reproducibility of exact numerical outputs.
- Supplementary methods section (SI) referenced multiple times but not fully reproduced in the main text; histone extraction protocol stated as 'described in SI Methods' without inline summary, requiring readers to consult supplementary material to understand a load-bearing procedure.

## Questions
- Can the authors provide the complete FragPipe command-line invocation or configuration file (e.g., params.txt) used for all searches, including search engine selection, precursor/fragment mass tolerance, and any non-default settings?
- How was the k=10 threshold for kNN imputation chosen? Was sensitivity analysis performed, and how does the choice affect quantitative results (e.g., Figure 7)?
- In the artifact-stripping procedure, if a peptide carries both Met oxidation and a biological modification (e.g., acetylation), what is the order of operations and how are ambiguous cases resolved?
- What are the explicit canonical-mapping rules used to assign histone variant peptides to a single representative sequence? Can a lookup table or decision tree be provided?
- For the hippocampal tissue analysis, what was the histone input mass per digestion reaction, and was propionylation applied? These details are missing from the main text and SI Methods.
- How many peptidoforms were excluded from quantitative analysis due to incomplete data across dose groups (i.e., 0 or 1 replicates), and how were these handled in Figure 7 visualizations?
- For the dose-response concordance correlations (Figure 7B, 7D), what are the 95% confidence intervals, and how sensitive are the reported r values to removal of outliers?
- What statistical test and background model were used for the motif enrichment analysis in SI Figures S6–S7? What p-value threshold defines 'enriched'?
- Can the authors provide a random seed or statement on seed-averaging for the kNN imputation step to ensure reproducibility of exact numerical outputs?
- The histone extraction protocol is referenced as 'described in SI Methods' — can this be summarized inline in the main text or provided as a protocols.io DOI for full procedural transparency?