# Decision Letter

VERDICT: major

## Summary of Evaluation

This manuscript presents a systematic evaluation of alternative proteases (Arg-C Ultra, r-Chymotrypsin) and labeling strategies (propionylation, TMT) for histone PTM analysis by mass spectrometry, and proposes RIPUP, a rapid dual-protease workflow. The core contributions are: (1) a rigorous 10-condition benchmarking matrix with n=4 replicates; (2) a mechanistically plausible claim that TMT's tertiary amine rescues ionization of negatively charged acylations (succinylation, glutarylation); and (3) a practical workflow demonstrated on rat hippocampal tissue within a 3-hour preparation window.

The panel's numerical signal (3.26/5, with 7 of 8 reviewers recommending major revision) reflects a genuine consensus: this is useful, well-designed work whose headline claims modestly outrun the evidence as presented. The workflow itself is sound and the complementary-coverage argument for the dual-protease design is well-supported. However, two central claims — the TMT "dark epigenome" finding and the quantitative NAM experiment — rest on comparisons that are confounded or incompletely specified. These are fixable with targeted additions and reanalyses, but they are not merely presentational gaps.

I am departing slightly from the raw average toward "major" rather than "minor" because the required fixes include at least one new control experiment (the matched-label comparison) and a reanalysis whose outcome could change a conclusion (the NAM replicate structure). These are substantive, not cosmetic.

---

## Required Revisions

1. **Provide a matched-label comparison to isolate the TMT effect from the protease effect.** The central claim that TMT "rescues" ionization of succinylated/glutarylated peptides is confounded: the manuscript compares TMT-labeled Arg-C Ultra against *Trypsin* + Prop, differing in two variables. Report succinylation and glutarylation site counts for Arg-C Ultra + Prop and Trypsin + Prop under identical search parameters, alongside the TMT numbers. If the propionylated Arg-C Ultra condition also detects these sites, the charge-compensation mechanism is not supported and the "dark epigenome" framing must be requalified accordingly.

2. **Clarify the replicate structure of the NAM experiment.** The Methods state cells were "divided into 3 x 5 mL aliquots" — this reads as technical replicates from a single split culture. State explicitly whether the three NAM-treated dishes were derived from three independent cultures (biological replicates) or one split culture. If the latter, the effective n for the limma analysis is 1 and the inference collapses; the quantitative claims must be reanalyzed accordingly.

3. **Address the fragmentation-energy confound.** TMT-labeled samples were fragmented with stepped NCE (30/40/50) while unlabeled samples used fixed 30%. Run the same TMT-labeled samples with fixed 30% NCE and report whether succinylation/glutarylation identifications persist. If they do not, the effect may be a fragmentation artifact rather than charge compensation, and the mechanistic claim must be revised.

4. **Report the propionylated-condition succinylation/glutarylation counts.** The claim that these sites are "largely undetected by propionylation-based methods" requires the corresponding counts for the propionylated conditions (Arg-C Ultra + Prop, Trypsin + Prop) under identical search settings. Without this denominator, the reader cannot distinguish a TMT-specific effect from a general sensitivity difference.

5. **Provide the complete quantitative pipeline specification.** Include: the exact limma model (design matrix, contrasts, eBayes settings), the number of peptidoforms excluded from testing due to missing data in any dose group, the number significant at 3 mM only / 10 mM only / both, and a versioned commit hash for the GitHub repository with a table mapping each figure to its generating script.

6. **Report effect sizes for the key NAM findings.** The text reports significance (adj p < 0.001) but not magnitude or direction for the representative sirtuin-target changes (H3K9ac, H4K16ac). Report log2 fold-changes with confidence intervals for these peptidoforms at both doses.

7. **Requalify the abstract's "quantitative accuracy" claim.** No validation experiment (spike-in, known-ratio, or orthogonal method comparison) supports the term "quantitative accuracy." Replace with "quantitative capacity" or add the missing validation.

8. **Add the HARD traceability items from the compliance audit:** (a) HEK293T cell line source and RRID/CVCL identifier; (b) randomization/blinding statement for the rat experiments (or explicit statement that none was used).

---

## Minor Suggestions

1. **Consolidate duplicate references.** Refs 1 and 7 are the same Sidoli et al. 2016 paper; refs 30 and 68 are the same Maile et al. 2015 paper; refs 41 and 44 are the same Bao et al. 2019 paper.

2. **Verify specific citation claims:** (a) confirm Ryzhaya et al. (ref 10) used trimethylacetic anhydride (TMA) specifically; (b) confirm the "60 core / 13 linker" figures attributed to Vai et al. (ref 20); (c) confirm refs 42 (Stransky et al., Aging Cell 2026) and 48 (Li et al., Cell Discov. 2023) exist and support the stated longevity and HDAC-desuccinylation claims respectively.

3. **Define error bars consistently across all figures.** Only Figure 4A states what error bars represent; Figures 2A, 2C, 4B, and 5A–D need definitions.

4. **State the TMT labeling ratio as molar or mass.** The Methods say "peptide:TMT ratio 1:8" without specifying which.

5. **Define "dark epigenome" at first use** in the abstract or introduction.

6. **Add figure panel definitions for Figure 5C and 5D** in the caption, and repeat the IHP definition in the Figure 4B caption.

7. **Report the per-replicate peptide counts with median and IQR** for the digestion-efficiency comparisons (Figure 2C), and state whether the Arg-C Ultra vs. Trypsin difference survives a paired test across the four replicates.

8. **Report the proportion of succinylated/glutarylated peptides relative to total identified peptides** per condition, restricted to peptides of comparable length and charge state, to distinguish a charge-compensation effect from a general sensitivity effect.

9. **State the missed-cleavage motif enrichment background model and test** for SI Figures S6–S7.

10. **Clarify the rat hippocampal replicate structure:** state whether the five animals were processed in a single batch and whether the reported CVs are within-animal or between-animal.

11. **Pin the database release version** (UniProt release or download date) used for the histone sequence database.

12. **State the R version and package versions** for limma and the Bioconductor 'impute' package.

13. **Soften the mechanistic claim about b-ion enhancement** (Figure 3C) unless a direct b-ion/y-ion coverage comparison for the same peptide with and without TMT is added.

14. **Clarify the positioning against Ryzhaya et al. 2025** — state explicitly what RIPUP adds beyond that workflow (omission of derivatization, addition of r-Chymotrypsin) as a head-to-head rather than as separate workflow descriptions.

---

The panel's concerns are substantive but addressable. The workflow is a genuine contribution, and the TMT charge-compensation hypothesis is worth testing properly. With the matched-label comparison, the replicate-structure clarification, and the fragmentation-energy control, the manuscript's claims will be commensurate with its evidence.