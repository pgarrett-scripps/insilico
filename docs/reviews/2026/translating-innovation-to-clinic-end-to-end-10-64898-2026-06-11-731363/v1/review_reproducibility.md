# Reproducibility Reviewer

SCORE: 3  
CONFIDENCE: 4  

## Summary

This manuscript reports the end-to-end development and cGMP manufacturing of the N332-GT5 gp140 HIV vaccine candidate, covering cell line development, upstream process scale-up, downstream purification, viral clearance, and product characterization. The work is significant and the overall narrative is coherent, but from a reproducibility standpoint the manuscript has several gaps that would prevent an independent group from rerunning the process without contacting the authors. The most load-bearing claims — the consistency of product quality across scales, the removal of the preparative SEC step, and the viral clearance results — are each supported by data that is either incompletely specified or not fully traceable to the described procedures.

## Strengths

1. The manuscript provides a clear, step-by-step description of the upstream and downstream process, including specific operating parameters (temperatures, pH setpoints, feed schedules, membrane types, column resins).
2. The viral clearance study is well-designed with two model viruses and multiple orthogonal unit operations, and the results are reported with log reduction values and standard deviations.
3. The product characterization is thorough, using two complementary mass spectrometry methods for glycan analysis and negative-stain EM for structural confirmation.

## Weaknesses

### Load-bearing

**1. The claim that the preparative SEC step could be removed without impacting product quality is not supported by the data presented.** The manuscript states (Section 3.3.2) that the final UF/DF step "was able to remove impurities from the product pool to an acceptable level and the overall results were comparable to the control execution with preparative SEC." However, Table 10 shows that the control (with SEC) achieved 0.8% LMW and 0.5% pre-Main in the flowthrough, while the SEC-removal run achieved 1.0% LMW and 0.8% pre-Main in the final retentate. These are not identical, and the manuscript does not state what threshold was used to define "comparable." More importantly, the study appears to have been performed once (n=1) with no replicate runs, and the load material for both arms is described only as "Demonstration Run preparative SEC load material" — it is unclear whether both arms used the same load pool or different pools. The decision to remove a unit operation from a cGMP process based on a single non-replicated comparison, with no statistical analysis, is a reproducibility gap: an independent group could not determine whether the observed differences are within normal process variability. The authors should report the number of replicates, the acceptance criteria used for "comparable," and ideally provide the raw SE-HPLC and RP-HPLC chromatograms or at least the full data table for both arms.

**2. The viral clearance claim (≥18.14 log reduction for XMuLV) rests on a summation of individual step clearances that may not be additive, and the manuscript does not provide the raw data needed to verify the calculation.** Table 12 reports individual LRV values for four steps, but the manuscript does not state whether these were measured in a single study or pooled across multiple studies, whether the same virus stock was used for all steps, or whether the scale-down model was qualified against the manufacturing scale (e.g., by comparing step yields and product quality between scale-down and full-scale runs). The footnote to Table 12 says the study used "material from the cGMP run," but the scale-down model description (Section 2.6) is one sentence: "A scale-down model of the purification process was developed to ensure comparability with the manufacturing-scale process." No data are shown demonstrating this comparability. For a claim that is central to the regulatory acceptability of the process, the authors should provide the scale-down qualification data (yields, product quality, and impurity profiles at both scales) and state whether the LRV values are from a single study or combined from multiple studies.

**3. The claim that the process "scaled efficiently from Ambr® 250 miniature bioreactors to 200-L single-use systems, delivering consistent product quality across multiple cGMP batches" is not fully supported because the titer comparison across scales uses different reference standards.** Section 3.2.3 states that the 50L Supply run titer (562 mg/L) was measured against IAVI/Scripps reference material, while the 50L Demonstration run (355 mg/L) and the GMP run (390 mg/L) were measured against two different KBI reference lots. The manuscript acknowledges this ("mainly due to different reference standards") but does not provide any cross-calibration data between the reference standards. An independent group could not determine whether the observed titer differences reflect process variability or reference standard differences. The authors should report the relative potency of each reference standard against a common anchor (e.g., the IAVI/Scripps standard) or provide the raw BLI response data normalized to a single standard.

### Sweep

- The manuscript does not state the software versions for any of the analytical instruments (e.g., Octet data analysis software, CFX Manager version, Byos version, IP2 version), which is a HARD flag for the glycan analysis and BLI results.
- The DeGlyPHER and LC-MS glycoproteomics methods are described with references, but the manuscript does not state which specific parameters were used (e.g., protease-to-protein ratios, digestion times, LC gradients, MS resolution settings) — "performed as previously described" resolves to the cited papers, which is acceptable, but the authors should confirm the cited papers contain the full protocol.
- The negative-stain EM analysis (Section 3.6.2) reports 6,086 particles analyzed but does not state the number of micrographs used for 2D classification or the resolution of the class averages; this is a SOFT issue since the conclusion (native-like trimers) is visually supported.
- The intermediate hold-time stability study (Section 3.3.3) reports a "3-4% increase in HMW" for the UF/DF1 retentate but does not state the actual Day 0 and Day 1 values, making it impossible to verify the ≤1-day hold time recommendation.
- The manuscript states that "the 50L Demonstration (C235 MCB) BLI titer was determined using KBI Reference Material lot # S-20210314-0001-SD2-E-M" but does not describe how this reference material was produced or characterized, which is a HARD gap for the titer comparison across runs.
- The downstream process flow chart (Figure 4) is described in text but the figure itself is not shown in the manuscript text I received; I could not verify that the figure matches the described unit operations.
- The manuscript does not state whether the cGMP batch was produced under a specific regulatory framework (e.g., ICH Q7, 21 CFR 210/211) or whether any deviations occurred during manufacturing; this is relevant for assessing whether the process is reproducible under GMP conditions.
- The viral clearance study does not report the virus titers used for spiking or the cytotoxicity of the load material on the indicator cells, which are standard parameters needed to assess the validity of the LRV calculations.

## Questions

1. For the preparative SEC removal study (Table 10): how many replicate runs were performed for each arm, and what were the pre-defined acceptance criteria for "comparable" product quality?
2. For the viral clearance study: was the scale-down model qualified against the manufacturing scale (e.g., by comparing step yields and product quality), and if so, where are those data?
3. Can the authors provide the cross-calibration data between the three reference standards used for BLI titer measurements (IAVI/Scripps 19Apr0088, KBI S-20210314-0001-SD2-E-M, and KBI P65)?
4. What were the actual Day 0 and Day 1 %HMW values for the UF/DF1 retentate in the hold-time stability study that led to the ≤1-day recommendation?