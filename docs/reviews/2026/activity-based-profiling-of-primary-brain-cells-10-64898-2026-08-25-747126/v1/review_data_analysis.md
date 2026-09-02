# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a methodologically sound chemical proteomics study that establishes a scalable ABPP platform for primary brain cells and identifies covalent ligands for CNS-enriched proteins, including allosteric HCN channel modulators. The quantitative claims are generally well-supported by appropriate statistical methods, though several analyses lack the transparency needed for full reproducibility and some effect sizes are modest relative to their biological claims. The work is suitable for publication with minor revisions addressing data handling and statistical reporting.

## Strengths

1. Multiple independent replicates (4–6 biological replicates per condition) and consistent use of parametric tests with stated assumptions (Boltzmann fitting, two-tailed Welch's t-tests) strengthen the electrophysiology findings.

2. The authors pre-specify statistical thresholds for liganding events (2.5-fold enantioselective enrichment, >33% competitive blockade) before analysis and apply them consistently across protein- and cysteine-directed ABPP, reducing post-hoc multiple-comparison risk.

3. Negative controls are well-designed: enantiomeric stereoprobes, cysteine-to-alanine mutants, and orthogonal validation (e.g., inside-out patch clamp, IP-MS co-enrichment) directly test the specificity claims rather than relying on statistical significance alone.

---

## Weaknesses: Load-bearing claims

**1. Brainocyte preparation validity as a proxy for intact brain tissue.**

The claim that brainocytes are "suitable and scalable approximation of intact brain cells" (Results, "An ABPP platform") rests on two comparisons: gel-ABPP profiles differ between brainocytes and lysates (Figure 1C), and protein-directed ABPP identifies 28 proteins unique to brainocytes (Figure 1D, Dataset S2). However, the paper does not establish that brainocyte-restricted liganding reflects *authentic* cellular context rather than artifacts of dissociation. The authors cite pilot acute brain slice data (Figure S1D) showing "brainocyte-restricted tryptoline acrylamide-protein interactions were generally recapitulated," but "generally" is unquantified: how many of the 28 brainocyte-unique proteins were confirmed in slices? A count or percentage would settle whether the brainocyte preparation captures genuine cell-state-dependent liganding or whether dissociation-induced changes (e.g., loss of cell–cell contacts, altered redox state, or cysteine oxidation) are driving the observed differences. Without this, the claim that brainocytes preserve "the integrity of their biological states" (Introduction) is aspirational rather than demonstrated.

**2. HCN channel functional effect size and physiological relevance.**

The patch-clamp data show that WX-02-679 (10 µM, 20 min pre-treatment) blocks cAMP-induced shifts in HCN2 V₁/₂ (control + cAMP: −83.5 ± 0.8 mV → cAMP + WX-02-679: −95.0 ± 1.8 mV; Figure 6C). This is presented as "near-complete blockade," but the effect size is modest: the V₁/₂ shift is ~11.5 mV in control + cAMP vs. ~1 mV in cAMP + WX-02-679 (within error bars). The paper does not report the magnitude of cAMP's normal effect in untreated cells or compare WX-02-679's potency to known HCN modulators (e.g., TRIP8b, which the authors mention). Additionally, the 10 µM concentration used in cells is 2–3-fold higher than the IC₅₀ measured in lysates (4.4 µM for HCN1), raising questions about whether the cellular effect reflects on-target activity or off-target effects at this dose. A dose–response curve in cells and a comparison to TRIP8b potency would clarify whether the compound is a practical tool or a proof-of-concept.

**3. DPYSL2 complexoform-restricted liganding: quantification of the rare complex.**

The authors propose that WX-01-06 engages only DPYSL2 when bound to DPYSL5, and that this fraction is small enough that cysteine-directed ABPP (which measures bulk C504 reactivity) shows no effect, while protein-directed ABPP (which enriches liganded proteins) detects it. This is a plausible model (Figure S4E), but the paper provides no estimate of the DPYSL2:DPYSL5 complex stoichiometry or abundance in brainocytes. If the complex is <1% of total DPYSL2, the claim that tryptoline acrylamides are "tools to study the specific functions of the DPYSL2:DPYSL5 complex" (Results, DPYSL2) is overstated: a compound that labels a rare proteoform is not necessarily a tool for studying its function. Quantitative co-IP or proximity-labeling data (BioID, APEX) in brainocytes would establish whether the complex is abundant enough to be biologically relevant.

---

## Weaknesses: Sweep

1. **Multiple-comparison correction for liganding discovery:** The paper identifies 114 stereoprobe-liganded proteins from >11,000 quantified cysteines and >5,600 proteins (Figure 2A), but does not report a family-wise error rate or false-discovery rate correction; the 2.5-fold threshold is data-driven, not pre-registered, and no permutation test or cross-validation is provided to estimate false-positive rate.

2. **Flow cytometry viability (~90%, Supplementary Dataset S1) is reported without n or replicates:** unclear whether this is a single measurement or an average, and whether 90% is sufficient to exclude systematic bias (e.g., selective loss of fragile cell types).

3. **PDE7B enzymatic assay (Figure S3F) shows no inhibition by WX-03-57, but the paper does not report the assay's sensitivity or positive-control IC₅₀ (e.g., for IBMX or BRL-50481), making it impossible to judge whether null result reflects true lack of activity or assay failure.**

4. **IP-MS volcano plot (Figure 3I) reports p-values from two-tailed Welch's t-test on six replicates, but does not state whether multiple-hypothesis correction was applied to the co-enriched protein list or how many proteins were tested.**

5. **Gel-ABPP IC₅₀ values (Figure 5J–L) are fitted to a single-site binding model without reporting goodness-of-fit, Hill coefficient, or confidence intervals; error bars are SD from 2–3 independent experiments, which may underestimate uncertainty in the fitted parameter.**

6. **Hippocampal slice recordings (Figure 6J–K) report sag ratio and rebound depolarization as mean ± SEM from N=8–10 cells, but do not state how many animals these cells came from; if all cells are from one animal, n is 1, not 8–10.**

7. **Cysteine-directed ABPP filtering (Methods) excludes peptides with "summed reporter ion intensities for the DMSO channels of <0.5" without justification; this threshold could bias detection toward cysteines with high baseline reactivity, potentially missing weakly reactive sites.**

8. **AlphaFold2 model of PDE7B (Figure S3E) is used to infer that C136 is "distal to the active site," but no experimental structure is provided and AlphaFold confidence scores are not reported; the inference is qualitative.**

---

## Questions

1. For the 28 brainocyte-unique liganded proteins (Figure 1D), how many were recapitulated in acute brain slices (Figure S1D), and does the authors' definition of "generally recapitulated" correspond to a quantitative threshold (e.g., >50% of proteins)?

2. In the HCN2 patch-clamp experiments, what is the magnitude of cAMP's V₁/₂ shift in vehicle-treated cells (control vs. control + cAMP), and how does WX-02-679's potency compare to published IC₅₀ or EC₅₀ values for TRIP8b or other HCN modulators?

3. For DPYSL2:DPYSL5 complexes in brainocytes, what is the estimated stoichiometry or molar ratio relative to total DPYSL2, and does this abundance support the claim that tryptoline acrylamides are tools for studying the complex's function?

4. In the IP-MS experiment (Figure 3I), was a multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR) applied to the co-enriched protein list, and if so, what is the corrected significance threshold?

5. For hippocampal slice recordings (Figure 6J–K), how many animals contributed cells to each condition, and were cells from the same animal treated as independent replicates or grouped by animal in the statistical model?