# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This manuscript presents a well-executed discovery of IPO9 as a regulator of cGAS-STING signaling, supported by integrated cell-based screening, chemical proteomics, biochemical assays, and structural biology. The statistical reporting is generally sound and appropriate to the methods employed. The main quantitative claims are supported by adequate replication and proper statistical tests. However, several analyses lack complete transparency in their statistical specification, and a few key comparisons rest on small sample sizes or single experiments that limit confidence in their generalizability.

## Strengths

1. Appropriate use of multiple independent replicates (n=3 standard) across cell-based assays, with clear specification of technical replicates and independent experimental runs.

2. Correct application of one-way and two-way ANOVA with post-hoc tests (Tukey's) where multiple comparisons are made, with exact p-values reported in figure legends.

3. Biochemical and biophysical experiments (BLI, malachite green assay) conducted in triplicate with explicit n values and error bars defined as mean ± s.d., enabling assessment of effect magnitude.

## Major Weaknesses

**1. In vivo pharmacodynamic claim rests on n=2 independent experiments with n≥4 mice per group (Fig. 1g, Extended Data Fig. 3d).**

The central claim that SR-218 reduces 2'3'-cGAMP levels in Trex1−/− cardiac tissue is stated as "representative of n=2 independent experiments." This is the only in vivo evidence for efficacy. Two independent experimental runs is the minimum threshold for reproducibility; the manuscript does not report whether both replicates showed the same direction of effect, whether effect sizes were consistent, or whether the combined data were analyzed. The figure legend states "at least n=4 mice per treatment group" but does not specify whether this is 4 or more, and whether mice were randomized or stratified. No power analysis is provided for the sample size chosen. The claim would be substantially stronger if both replicates were shown separately or if a combined analysis across both experiments were reported with the per-experiment breakdown disclosed.

**2. IPO9 knockdown phenotype (Fig. 3b–c) shows statistical significance but effect sizes are modest and one condition (IPO9 sh2 + SR-717) approaches non-significance.**

Figure 3c reports phospho-STING quantification following IPO9 shRNA knockdown under two stimulation conditions. For dsDNA (VacV70), IPO9 sh2 achieves p=0.0092 but the figure does not show the raw data or effect size (fold-change relative to WT). For SR-717 stimulation, both knockdown lines show p>0.05 (sh1 p=0.0951, sh2 p=0.0741), yet the text states "loss of IPO9 in THP-1 cells was found to phenocopy the ability of SR-218 to impair STING activation." This overstates the evidence: the SR-717 condition does not reach significance, and without raw data or confidence intervals, it is unclear whether the effect is biologically meaningful or driven by measurement noise. The manuscript should report fold-changes with 95% CIs and disclose whether the knockdown efficiency was verified and consistent between sh1 and sh2 lines.

**3. Cryo-EM structure resolution (4.3 Å) limits mechanistic claims about sidechain interactions.**

The manuscript states: "The resolution of the final map precluded high confidence modeling of sidechains, however, clearly resolved secondary structure enabled unambiguous observation of a cGAS dimer bound to histones." Yet Fig. 4c inset and the text claim that "acidic patch residues on H2A (E61, E64, D90, E92) are situated to interact with basic residues R236 and R255 on cGAS." At 4.3 Å resolution, sidechain positions are not directly observable; these assignments rely on superposition with higher-resolution structures. The manuscript does not state which reference structure was used for sidechain assignment, whether the superposition was validated by independent methods (e.g., cross-linking mass spectrometry), or whether alternative rotamers or conformations are consistent with the map. The claim that "IPO9 could directly induce dissociation of H2A-H2B from cGAS...by binding the exposed histone core...and displacing cGAS interactions with the histone acidic patch with its H18-19 loop" is speculative given the resolution limit and should be framed as a structural hypothesis rather than a mechanistic conclusion.

## Minor Weaknesses

1. **Multiple comparisons in luciferase screen (Fig. 1a, Extended Data Fig. 2a–k):** The manuscript does not state whether a multiple-testing correction was applied during primary hit selection or SAR analysis; if ~80,000 compounds were screened, the false discovery rate threshold should be disclosed.

2. **Rhodamine labeling experiments (Fig. 2c–h, Extended Data Fig. 4a–g) lack quantification:** Blots are shown but no densitometry, band intensity ratios, or statistical comparison between conditions is reported; these appear to be qualitative demonstrations rather than quantitative dose–response curves.

3. **BLI EC₅₀ for IPO9-mediated H2A-H2B disruption (Fig. 3f, 110 nM) is reported without a 95% confidence interval or goodness-of-fit statistic,** making it unclear whether the curve is well-resolved or whether alternative models fit equally well.

4. **Malachite green assay (Fig. 3d, Extended Data Fig. 5b–c) uses "concentrations corresponding to the approximate Km values of substrates"** but does not state the actual concentrations used, the Km values themselves, or whether substrate saturation was verified; this undermines reproducibility.

5. **cGAMP ELISA normalization (Fig. 1c) to "pg/mg of lysate"** introduces a denominator (total protein) that could be affected by cell lysis efficiency or protein precipitation; no validation that this normalization does not confound the effect is provided.

6. **RT-qPCR (Fig. 1e–f) uses delta-delta Ct method but does not report Ct values, primer efficiency, or whether technical replicates were averaged before statistical testing,** risking pseudo-replication.

7. **Cryo-EM 3D classification (Extended Data Fig. 6a) identified a 2:1 cGAS:H2A-H2B population but the functional relevance is not discussed;** the final model uses the 2:2 stoichiometry without justifying why the 2:1 species is not the biologically relevant form.

8. **Compound SR-218 metabolic stability (Extended Data Fig. 3a) is stated as a limitation but no half-life or clearance rate is given,** only a qualitative statement that "metabolic stability...was found to preclude identification of an analog that would enable steady-state drug levels."

## Questions

1. **Figure 3c:** Please report fold-changes with 95% confidence intervals for all conditions in Fig. 3b–c, and disclose the IPO9 knockdown efficiency (% reduction in IPO9 protein) for both sh1 and sh2 lines.

2. **Figure 4c inset:** Which reference structure (PDB ID) was used to assign sidechain positions for the acidic patch residues, and was the superposition validated by an orthogonal method such as cross-linking mass spectrometry or mutagenesis?

3. **Extended Data Fig. 3a:** What is the half-life and intrinsic clearance of SR-218 in mouse liver microsomes, and does this explain why steady-state dosing was not achieved in the Trex1−/− experiment?

4. **Figure 2b:** What was the family-wise error rate or false discovery rate threshold applied during hit prioritization in the TMT proteomics screen, and how many candidate proteins met the filtering criteria before IPO9 was selected?

---

## Technical Notes for Other Reviewers

- **Structural biology reviewer:** The cryo-EM map quality and model building should be independently assessed; I could not verify the FSC curve or angular distribution (Extended Data Fig. 6b) from the text alone.
- **Cell biology reviewer:** The shRNA knockdown efficiency and off-target effects should be validated; the manuscript does not report whether both sh1 and sh2 lines showed equivalent IPO9 reduction.
- **Biochemistry reviewer:** The malachite green assay conditions (substrate concentrations, reaction kinetics, background subtraction) should be detailed sufficiently for independent replication.