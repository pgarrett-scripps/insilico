# Methodology Reviewer

SCORE: 3  
CONFIDENCE: 4  

## Summary

This manuscript presents RIPUP, a streamlined histone PTM analysis workflow using Arg-C Ultra and r-Chymotrypsin with or without TMT labeling, benchmarked against the conventional Trypsin + propionylation protocol. The design is a systematic comparison across 10 conditions with 4 replicates each, and the authors claim improved PTM coverage, faster sample preparation, and — most notably — that TMT labeling rescues ionization of negatively charged acylations (succinylation, glutarylation) via charge compensation from the tertiary amine. The quantitative NAM experiment and the rat hippocampal proof-of-concept are secondary but relevant demonstrations.

## Strengths

1. The systematic comparison across 10 conditions with matched replicates is a rigorous benchmarking design that directly addresses the question of which protease/labeling combination performs best.
2. The mechanistic explanation for TMT's advantage (charge compensation via tertiary amine) is a plausible and testable hypothesis that goes beyond mere empirical observation.
3. The inclusion of a real biological sample (rat hippocampus) and a functional perturbation (NAM) demonstrates the workflow's practical applicability beyond cell lines.

## Weaknesses

### Load-bearing

**1. The claim that TMT "rescues" ionization of negatively charged acylations is not directly supported by the data presented.** The authors report 58 succinylation and 31 glutarylation sites detected with TMT labeling, but they do not show that these same sites are *not* detected with propionylation or unlabeled approaches under otherwise identical conditions. The comparison is confounded by the fact that TMT-labeled samples were digested with Arg-C Ultra and r-Chymotrypsin, while the propionylated comparator was Trypsin-digested. Different proteases generate different peptides, so the absence of succinylation in the propionylated condition could be due to sequence coverage differences rather than ionization suppression. To establish the charge-compensation claim, the authors need to compare TMT-labeled vs. propionylated peptides from the *same* protease digest (e.g., Arg-C Ultra with both labels) and show that succinylation sites are specifically lost with propionylation but retained with TMT. Without this matched comparison, the conclusion that TMT "rescues" ionization of acidic acylations is not earned.

**2. The quantitative NAM experiment lacks a critical control: a vehicle-treated sample processed through the same workflow at the same time.** The authors compare 0 mM vs. 3 mM vs. 10 mM NAM, but all samples appear to be processed in parallel. However, the claim that NAM induces "dose-dependent missed cleavage redistribution" (259 peptidoforms detected exclusively in NAM-treated samples) is presented as a finding, not a confound. If NAM treatment changes the modification landscape such that Arg-C Ultra cleavage efficiency changes, then the quantitative comparison of peptidoform intensities across doses is comparing different peptide populations — the denominator shifts. The authors acknowledge this and switch to direct peptidoform intensity comparison, but this does not fully address the issue: if the cleavage efficiency changes with dose, the same peptidoform may be represented by different backbone lengths across doses, and the intensity comparison is not apples-to-apples. A control would be to spike a known amount of a synthetic unmodified histone peptide into each sample before digestion and normalize to that, or to compare only peptidoforms that are detected in all doses with the same backbone.

**3. The claim that TMT's tertiary amine "sequesters a mobile proton" and enhances b-ion series is not directly demonstrated.** The authors show a schematic (Figure 3C) and state that TMT-labeled peptides produce enhanced b-ions, but they do not present a quantitative comparison of b-ion vs. y-ion coverage for the same peptide sequence with and without TMT labeling. The stepped collision energy (30/40/50) is also different from the fixed 30% used for non-TMT peptides, which is a confound in the fragmentation comparison. To support the mechanistic claim, the authors should show, for at least one peptide, the fragment ion coverage with and without TMT at the same collision energy, or at least report the average b-ion coverage across TMT-labeled vs. unlabeled peptides from the same digest.

### Sweep

- The comparison of "Trypsin + Prop" to Arg-C Ultra is confounded by the fact that Trypsin digestion was performed with a 6-hour incubation and propionylation before and after digestion, while Arg-C Ultra was 2 hours with post-digestion labeling only — the time difference is a variable, not a controlled comparison.
- The claim that "TMT labeling efficiency was ~99% by intensity" is based on a calculation that excludes biologically modified lysines, but the authors do not report how many lysines were excluded or whether the calculation was performed on the same peptide set across conditions — this could bias the efficiency comparison.
- The NAM dose-response experiment uses only 3 replicates per dose, which is minimal for the limma-based differential analysis; the authors should report the power or at least the number of peptidoforms that were detected in all 3 replicates per dose before imputation.
- The rat hippocampal experiment is presented as a proof-of-concept, but the authors do not report whether the 5 animals were processed in a single batch or whether batch effects were considered — if processed in separate batches, batch is confounded with animal.
- The claim that "TMT's tertiary amine provides charge compensation" is presented as a general mechanism, but the authors do not test this with a control label that lacks the tertiary amine (e.g., a TMT variant without the amine) — this would be a direct test of the mechanism.

## Questions

1. For the succinylation/glutarylation comparison, can you provide the same analysis (PTM site counts) for Arg-C Ultra digested peptides with and without TMT labeling, and with propionylation, to isolate the effect of the label from the protease?
2. In the NAM experiment, did you verify that the same peptidoform (same backbone, same modifications) is detected across all doses, or did you restrict the quantitative analysis to only those peptidoforms with identical backbone lengths across doses?
3. For the fragment ion comparison, can you report the b-ion and y-ion coverage for a specific peptide (e.g., H3 9-17) with and without TMT at the same collision energy?

## Overall

The design is a solid benchmarking effort with a clear question, but the central mechanistic claim (TMT rescues acidic acylations) is not isolated from the protease confound, and the quantitative NAM experiment has a cleavage-efficiency confound that is acknowledged but not controlled. The workflow is useful and the data are likely reproducible, but the conclusions outrun the evidence in the two key places. With matched controls (same protease, different labels) and a direct fragment-ion comparison, the paper would be substantially stronger.