# Reproducibility Reviewer

SCORE: 3  
CONFIDENCE: 4

## Summary

This manuscript presents a systematic comparison of alternative proteases (Arg-C Ultra, r-Chymotrypsin) and labeling strategies (propionylation, TMT) for histone PTM analysis, and proposes a rapid dual-protease workflow (RIPUP). The central claims are: (1) Arg-C Ultra outperforms Trypsin in digestion efficiency and peptide yield; (2) TMT labeling uniquely enables detection of negatively charged acylations (succinylation, glutarylation) via charge compensation; (3) the combined workflow detects a broad PTM landscape in rat hippocampus within 3 hours. The work is largely reproducible in principle, but several load-bearing artifacts are not fully traceable from the deposited materials, and some quantitative claims rest on analyses whose exact parameters are not recoverable from the manuscript alone.

## Strengths

1. The systematic comparison across 10 conditions with n=4 replicates is a solid experimental design, and the CV reporting is commendable.
2. The mechanistic explanation for TMT's advantage in detecting acidic acylations (tertiary amine charge compensation) is plausible and well-articulated.
3. The authors deposit raw data to ProteomeXchange and provide custom R scripts on GitHub — a genuine effort toward reproducibility.

## Weaknesses

### Load-bearing

**1. The quantitative analysis pipeline is not fully specified end-to-end.** The manuscript states that "quantitation was performed directly on individual peptidoform intensities with histone-level loading correction," but the exact normalization formula, the imputation parameters beyond "k = 10," and the limma model specification (contrasts, design matrix) are not given in the text or methods. The GitHub link is provided, but the manuscript does not state which script corresponds to which figure, nor does it provide a versioned commit or tag. An independent group could not reproduce the 112 significant peptidoforms from the described procedure alone. **What would settle it:** a versioned repository commit hash, a table mapping each figure to its generating script, and the exact limma call (design formula, contrasts, eBayes settings) in the methods or a supplementary file.

**2. The claim that TMT "rescues" ionization of succinylated/glutarylated peptides is supported by detection counts, but the alternative explanation — that TMT simply improves overall peptide identification sensitivity — is not excluded.** The manuscript reports 58 succinylation and 31 glutarylation sites with TMT versus near-zero with propionylation, but does not report the total peptide identification rates per condition as a denominator. If TMT simply identifies more peptides overall (which Figure 2C suggests: 416 vs 179 fully cleaved peptides), then the enrichment of acidic acylations could be a sensitivity effect rather than a charge-compensation effect specific to negatively charged modifications. **What would settle it:** report the proportion of succinylated/glutarylated peptides relative to total identified peptides per condition, and ideally show that the effect persists when matching for peptide length and charge state.

**3. The rat hippocampal "proof-of-concept" results are presented without the quantitative traceability required to verify them.** The manuscript reports 231 unique PTM sites and lists specific modifications (e.g., H2A K118/K119 ubiquitination, H3 K27/K36/K37 methylation), but the supplementary peptide lists (Table S4) are referenced without a description of how they were filtered (the text says "detected in ≥2 replicates" but does not specify whether this is at PSM or peptide level, nor the FDR applied at each step). The FragPipe search parameters are in Table S1, but the exact mass offset list and variable modification declarations are not fully enumerated in the manuscript text. **What would settle it:** a supplementary table with columns for each PTM site, the peptide evidence, the number of replicates detecting it, and the search parameters used, cross-referenced to the deposited raw files.

### Sweep

- The manuscript states "data were searched against a restricted database containing extracted human or rat histone sequences" — the exact FASTA file and how "extracted" sequences were curated is not specified; a versioned FASTA or the exact UniProt accessions would be needed.
- The "informative histone peptides" (IHP) definition is clear, but the threshold "identified in 3 out of 4 replicates" is not stated as a filtering step in the FragPipe workflow — was this applied post-hoc in R? The order of operations (FragPipe output → R filtering → statistics) is not documented as a single pipeline.
- The TMT labeling efficiency calculation ("~92% by site count") does not state how biologically modified lysines were excluded from the denominator; the manuscript says they were "excluded from calculations" but not how they were identified (by mass offset? by known PTM lists?).
- The NAM dose-response analysis uses kNN imputation restricted to groups with ≥2/3 replicates, but the manuscript does not state the random seed or whether imputation was performed per-histone or globally; this affects reproducibility of the imputed values.
- The GitHub repository link is provided but without a commit hash or release tag; the manuscript states "custom R scripts" but does not list the R package versions (e.g., limma version, impute version) used.
- The "missed cleavage motif analysis" (SI Figures S6–S7) is described in one sentence without the statistical test used to call residues "enriched"; the enrichment calculation is not specified.
- The claim that "TMT's tertiary amine sequesters a mobile proton" is presented as established fact but is not experimentally demonstrated (e.g., via ion mobility or hydrogen/deuterium exchange); this is a mechanistic hypothesis that would benefit from a direct test.

## Questions

1. Can you provide the exact limma model specification (design matrix, contrasts, eBayes settings) and the R script version (commit hash) used to generate Figure 7?
2. What is the proportion of succinylated/glutarylated peptides relative to total identified peptides in TMT-labeled versus propionylated conditions, restricted to peptides of comparable length and charge state?
3. For the rat hippocampal data, what is the exact filtering pipeline from FragPipe output to the 231 PTM sites reported — specifically, the FDR thresholds at PSM and peptide level, and the replicate-detection rule applied?