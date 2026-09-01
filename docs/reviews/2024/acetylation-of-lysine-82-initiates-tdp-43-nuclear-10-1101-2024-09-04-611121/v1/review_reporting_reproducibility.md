# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a mechanistic study of TDP-43 nuclear import disruption in the context of age-related proteasome decline and ALS. The core claims are well-supported by multiple complementary methods: quantitative mass spectrometry identifies TDP-43 as the most sensitive protein to proteasome inhibition; biochemical assays establish that K82 acetylation abolishes importin-α1 binding; and acetylation-specific antibodies detect K82 acetylation in sALS motor cortex. The experimental workflow is substantially reproducible from the manuscript, with most critical parameters, reagents, and data sources specified. The work merits publication with minor clarifications on reproducibility friction points that do not undermine the central findings.

## Strengths

1. The quantitative TMT mass spectrometry analysis of the nuclear proteome (Fig. 1E–F) is rigorous, with complete search parameters, false-discovery-rate filtering, and statistical testing reported; the finding that TDP-43 is the most sensitive protein to proteasome inhibition is striking and well-documented.

2. The authors use multiple independent proteasome inhibitors (BTZ, MG132, MRZ) at matched ~50% activity levels, and validate findings across iPSC-derived neurons, SH-SY5Y cells, and postmortem tissue, reducing the risk that results reflect off-target effects or cell-type artifacts.

3. The K82 mutagenesis series (Fig. 4, S4) is systematic and interpretable: single lysine-to-arginine variants pinpoint K82 as critical, and the bipartite NLS requirement (K82 + K95 or K97) is clearly mapped, supporting the specificity of the acetylation effect.

## Weaknesses: Load-bearing claims

**Claim 1: Acetylation at K82 is sufficient to block TDP-43 nuclear import.**

The evidence rests on two experiments: (i) the K82Q acetylation-mimicking substitution eliminates nuclear TDP-43 and importin-α1 binding (Fig. 3C–E), and (ii) synthetic peptides acetylated at K82 do not bind importin-α1 (Fig. 3F). However, K82Q is not a perfect mimic of acetylation—it introduces a polar uncharged residue, whereas acetylation adds a bulky acyl group while retaining partial positive charge. The peptide-binding assay (Fig. 3F) uses only 33 amino acids (aa77–110) in isolation; it does not test whether full-length TDP-43 acetylated at K82 in cells actually fails to import, nor does it exclude the possibility that acetylation at K82 triggers compensatory modifications (e.g., phosphorylation at nearby S91/S92) that are the true import-blocking lesion. The live-cell imaging of K82Q-expressing neurons (Fig. 3C–D) shows cytoplasmic accumulation, but does not directly measure importin-α1 binding in those cells. To strengthen this claim, the authors should report: (i) whether endogenous TDP-43 acetylated at K82 (detected by the ac-K82 antibody in Fig. 5) co-immunoprecipitates less importin-α1 than unacetylated TDP-43 in the same lysate, and (ii) whether K82Q-expressing neurons show reduced stathmin-2 splicing defects compared to wild-type TDP-43 under proteasome inhibition, confirming that the mutation preserves nuclear function.

**Claim 2: K82 acetylation is an early event in TDP-43 proteinopathy, preceding phosphorylation.**

The evidence is that ac-K82 is detected in both soluble and insoluble fractions of sALS motor cortex, whereas phosphorylated TDP-43 is only in the insoluble fraction (Fig. 5C). This is suggestive but does not establish temporal order. Soluble ac-K82 could reflect recent acetylation, or it could reflect a pool that is acetylated but not yet phosphorylated because phosphorylation occurs downstream. The authors do not report: (i) the absolute or relative abundance of ac-K82 versus phospho-TDP-43 in the same samples, (ii) whether ac-K82 and phospho-TDP-43 co-localize in the same protein molecules (by co-IP or mass spec of the same TDP-43 molecules), or (iii) whether ac-K82 precedes phosphorylation in a time-course experiment in cultured neurons. The claim that acetylation "may be an earlier event" is appropriately hedged in the text, but the figure caption (Fig. 5C) states it more strongly ("suggesting that acetylation at lysine 82 may be an earlier event"), and the evidence does not yet support even that softer reading without additional data on stoichiometry and co-modification.

**Claim 3: Reduced proteasome activity is the physiological trigger for K82 acetylation.**

The authors show that partial proteasome inhibition (BTZ, MG132, MRZ) induces K82 acetylation in cultured neurons (Fig. S5) and that proteasome activity is reduced in sALS motor cortex (Fig. S1A). However, they do not demonstrate that proteasome inhibition is *sufficient* to induce K82 acetylation in sALS-relevant conditions, nor do they show that blocking the acetyltransferase(s) or activating the deacetylase(s) responsible for K82 acetylation prevents the nuclear export of TDP-43 under proteasome inhibition. The identity of the acetyltransferase and deacetylase are not discussed. The authors state that acetylation is "governed by competing activities of acetyltransferases and deacetylases" but do not name candidates or test whether known HDAC inhibitors (which would increase acetylation) or acetyltransferase inhibitors alter the phenotype. Without this, the causal link between proteasome decline and K82 acetylation remains correlative.

## Weaknesses: Sweep

1. The ac-K82 antibodies (three polyclonal antibodies from Sanyou Inc.) are validated only by ELISA binding to synthetic peptides (Fig. 5A, S5); no orthogonal validation (e.g., mass spec confirmation of ac-K82 in the same sALS samples, or loss of signal after deacetylase treatment) is provided, raising the risk of off-target binding in complex tissue lysates.

2. The sALS cohort is small (n=6) and heterogeneous (Fig. 5B shows variable ac-K82 signal); no clinical metadata (disease duration, age, mutation status, postmortem interval) are reported in the main text or supplementary table, limiting interpretation of whether ac-K82 correlates with disease severity or stage.

3. The stathmin-2 splicing assay (Fig. 1G, S2E) is used as a readout of TDP-43 nuclear function, but the authors do not report whether stathmin-2 protein levels or localization are altered, nor whether the cryptic exon-skipping event is the only TDP-43-dependent splicing change under proteasome inhibition.

4. The live-cell imaging quantification (e.g., Fig. 2E, 4E) reports "nuclear versus whole cell" fluorescence intensity, but does not specify whether background subtraction, photobleaching correction, or normalization to cell volume was applied, and the number of cells analyzed per condition is not stated.

5. The co-IP experiments (Fig. 2A–B, 3E, 4C) use standard RIPA or IP lysis buffer; no information is provided on whether the buffers preserve transient protein–protein interactions or whether the immunoprecipitation efficiency (% of target protein recovered) was measured.

6. The TMT mass spectrometry analysis (Fig. 1E–F) reports a volcano plot and fold-changes but does not provide the full proteome dataset (accession number or supplementary table) or specify how many peptides per protein were quantified, limiting independent verification of the TDP-43 result.

7. The lentiviral transduction efficiency and expression levels of TDP-43 variants (Fig. 3C–E, 4D–E) are not quantified; if expression is heterogeneous, the nuclear/cytoplasmic ratio could be confounded by expression level.

8. The Materials and Methods state that plasmids "will be deposited to Addgene at the time of publication," but no Addgene IDs are provided, and the lentiviral vectors are not yet publicly available, preventing immediate reproduction of the transduction experiments.

## Questions

1. Figure 3F: Does the peptide-binding assay include the full bipartite NLS context (aa77–110), and were the K95 and K97 residues present in the acetylated peptides tested?

2. Figure 5B: What is the postmortem interval for each sALS and control sample, and does ac-K82 signal correlate with tissue quality (e.g., RNA integrity number)?

3. Supplementary Table S2: Can the authors provide the clinical and neuropathological metadata (age, disease duration, site of onset, TDP-43 stage, phospho-TDP-43 burden) for the sALS and control cases?

4. Figure 1E–F: Will the complete TMT proteome dataset be deposited to ProteomeXchange or another public repository, and if so, what is the accession number?