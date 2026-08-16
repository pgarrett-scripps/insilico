# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript reports the development and cGMP manufacturing of the N332-GT5 gp140 HIV vaccine candidate, covering cell line development, upstream and downstream process scale-up, viral clearance, and product characterization. The work is a process-development report rather than a hypothesis-testing study, and the quantitative claims are mostly descriptive (yields, purity, clearance factors) rather than inferential. The central claims — that the process is scalable, reproducible, and yields product meeting quality targets — are supported by the data presented, though several quantitative comparisons lack the statistical framing needed to fully assess their robustness.

## Strengths

1. The manuscript reports step yields, purity, and impurity clearance at multiple scales (bench, pilot, cGMP), enabling direct comparability assessment.
2. The viral clearance study uses appropriate model viruses (XMuLV, MMV) with LRV values and standard deviations reported per unit operation.
3. The authors pre-emptively evaluated process robustness (worst-case conditions) and intermediate hold-time stability, which strengthens confidence in the manufacturing claims.

## Weaknesses

### Load-bearing

**1. Reproducibility across scales is asserted from single runs without variability estimates.** The central claim — that the process scales reproducibly from Ambr®250 to 200-L bioreactors — rests on comparing single runs at each scale (one RCB run, one MCB demonstration run, one GMP run). The reported titer differences (562 vs 355 vs 390 mg/L) are attributed to different reference standards, but no quantitative evidence supports this attribution. The BLI titer assay variability is never reported (no replicate measurements, no assay CV). The claim "comparable cell growth, metabolite behavior and BLI titers" is unsupported as stated: three data points with no error bars cannot establish comparability. What would settle this: report the BLI assay precision (replicate measurements of the same sample), and present the three runs' growth curves with the reference-standard conversion factors explicitly stated so titers can be compared on a common scale.

**2. The ">99% trimeric purity" claim conflates SE-HPLC main peak with trimer content.** The manuscript states ">99% trimeric purity" in the abstract, but the SE-HPLC data show %Main Peak of 98.6–99.4%, which is a measure of monomeric (non-aggregated, non-fragmented) species, not specifically trimer. The nsEM data (6,086 particles, 2D classes showing trimer-like morphology) is the actual trimer-content evidence, but no quantitative trimer percentage is derived from it. The BLI relative potency (116% vs reference) is a functional proxy but not a trimer fraction. What would settle this: state explicitly that SE-HPLC main peak is being used as the trimer proxy, or report a quantitative trimer fraction from nsEM (e.g., % particles classified as trimer-like vs other states).

**3. The preparative SEC removal study (Table 10) compares two conditions without replication.** The decision to remove SEC from the process rests on a single comparison between a control run (with SEC) and a test run (without SEC), each executed once. The resHCP values are reported as "<LOQ" for both, and SE-HPLC/RP-HPLC differences (1.8% vs 1.0% LMW; 1.5% vs 0.8% pre-Main) are small but could be within assay variability — which is never reported for these methods. What would settle this: report the assay variability (repeatability) for SE-HPLC and RP-HPLC at these impurity levels, and state whether the observed differences exceed it.

### Sweep

- **HARD**: The hold-time stability study (Section 3.3.3) uses a threshold of ">0.7% increase in HMW or LMW" to define instability, but no justification or source for this threshold is given; it appears to be an arbitrary cutoff rather than a statistically or clinically derived limit.
- **SOFT**: The viral clearance "overall" LRV values (≥18.14 for XMuLV, ≥11.70 for MMV) are summed across unit operations, but this assumes independence of clearance mechanisms; the manuscript does not discuss whether this assumption is justified.
- **HARD**: The glycan occupancy data (Figure 17) report percentages with standard errors, but the n (number of replicate measurements) is not stated in the text; the figure legend says "mean of abundance measurement of peptides" without specifying how many independent measurements.
- **SOFT**: The claim that "65% of BG18 type I antibodies... could bind to at least one trimer containing all glycans in the N332 epitope" (from the Introduction, citing prior work) is a preclinical result not derived from this manuscript's data; it should be clearly marked as background rather than presented as part of this work's findings.
- **HARD**: The BLI relative potency for the cGMP batch is reported as "116% Compared to Reference" with no confidence interval or replicate information; a single potency measurement cannot establish equivalence.
- **SOFT**: The step yield for 2G12 capture is reported as >100% in the pilot run and attributed to "titer assay variability," but no assay variability data are provided to support this explanation.

## Questions

1. What is the replicate count and assay CV for the BLI titer measurements used to compare the three production runs (RCB, MCB demonstration, GMP)?
2. Can you report the SE-HPLC and RP-HPLC assay repeatability (e.g., %RSD) at the impurity levels observed in the preparative SEC removal study, so the reader can judge whether the observed differences exceed assay noise?
3. What is the n for the DeGlyPHER glycan occupancy measurements in Figure 17, and how many independent LC-MS runs were averaged?