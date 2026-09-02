# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a well-executed chemical proteomics study that extends activity-based protein profiling (ABPP) to intact primary brain cells and identifies covalent ligands for CNS-enriched proteins, including a mechanistically novel allosteric modulator of HCN channels. The core claims are supported by appropriate evidence, though one major load-bearing conclusion rests on an incomplete mechanistic argument, and the generalizability of the brainocyte findings to intact brain physiology remains partially unresolved.

## Strengths

1. The brainocyte preparation is validated against both brain lysates and acute slices, providing reasonable confidence that the ligandability map reflects a physiologically relevant intermediate state between lysate and intact tissue.

2. The HCN channel work combines chemical, structural, electrophysiological, and neuronal-slice evidence in a coherent narrative, with the inside-out patch clamp experiment (Figure 6H) providing direct proof that WX-02-679 acts on the intracellular face of the channel.

3. The DPYSL2 complexoform-restricted liganding is thoroughly characterized across multiple cell lines and genetic backgrounds, with CRISPR knockout validation (Figure 4I–J) that specifically tests the dependence on DPYSL5.

## Load-bearing Weaknesses

### 1. Claim: Brainocyte-restricted liganding events reflect authentic protein interactions requiring intact cell environment

**The evidence:** Protein-directed ABPP identifies 28 proteins liganded only in brainocytes, not brain lysates (Figure 1D). The authors validate this by showing brainocyte-restricted interactions are "generally recapitulated in acute brain slices" (Figure S1D). However, the slice experiment is described as "pilot" and uses only qualitative comparison without quantitative metrics or statistical testing.

**The problem:** The claim that brainocyte-restricted events depend on the intact cell environment is not distinguished from a simpler alternative: these proteins may be present at lower abundance or in different conformational states in lysates due to mechanical disruption, dilution, or loss of post-translational modifications during lysis—not because they require living cells. The slice validation is reassuring but incomplete. Figure S1D shows representative examples (PLP1, UBL3, PTGDS, HPCAL1, TMX4, SCRN1, HPCA) but does not report how many of the 28 brainocyte-restricted proteins were tested, how many replicated, or whether any failed. Without quantitative replication data for the full set, the claim that brainocyte-restricted events are "authentic" interactions requiring intact cells remains partially supported.

**What would settle it:** Report the number of brainocyte-restricted proteins tested in acute slices, the number that replicated with similar stereoselectivity, and the number that did not. Alternatively, perform protein-directed ABPP on lysates prepared from freshly dissociated brainocytes (without the enzymatic dissociation step) to test whether the difference is lysis-dependent rather than cell-state-dependent.

### 2. Claim: WX-02-679 blocks cAMP-induced modulation of HCN channels while sparing basal activity

**The evidence:** Whole-cell patch clamp in HEK293T cells shows WX-02-679 prevents the rightward shift in V₁/₂ induced by cAMP (Figure 6B–D), and inside-out patches confirm the effect is direct (Figure 6H). Hippocampal slice recordings show WX-02-679 reduces voltage sag and rebound depolarization (Figure 6J–K), consistent with loss of Ih. The authors conclude the compound "specifically disrupts the cAMP-modulated, but not basal function of HCN channels."

**The problem:** The claim conflates two distinct observations: (i) WX-02-679 blocks cAMP-induced *shifts* in activation voltage, and (ii) basal channel conductance is spared. However, Figure 6J–K shows that WX-02-679 reduces both voltage sag and rebound depolarization in neurons, which are readouts of total Ih amplitude, not just cAMP-dependent modulation. The authors interpret this as "reduction in Ih" (Results, line describing Figure 6J–K) but argue this is consistent with "loss of the tonic depolarizing Ih" (Discussion). This is internally contradictory: if basal Ih is truly spared, why does sag ratio decrease? The most parsimonious reading is that WX-02-679 reduces basal Ih, not just cAMP-dependent gating. The heterologous system (HEK293T) may not recapitulate the full pharmacology of endogenous channels, and the slice data suggest a broader effect than the title and abstract claim.

**What would settle it:** In hippocampal slices, measure Ih directly using voltage clamp (not current clamp) in the presence and absence of cAMP, with and without WX-02-679, to quantify whether basal Ih amplitude is truly preserved. Alternatively, report the absolute current amplitude at a fixed voltage step (e.g., −105 mV) in the absence of cAMP in HEK293T cells, comparing control and WX-02-679-treated cells.

### 3. Claim: Stereoprobes identify ligands for diverse CNS-enriched proteins absent or underrepresented in prior ABPP studies

**The evidence:** Table 1 lists 28 CNS-enriched liganded proteins; the authors note that "the majority of the CNS-enriched liganded proteins were not identified in previous ABPP studies of primary immune and cancer cell lines" (Results, Figure 2E–F section). However, the comparison is implicit: the authors cite prior ABPP work on Ramos cells and HEK293T cells but do not provide a systematic count of how many of the 28 proteins were quantified in those prior studies and how many showed no stereoprobe enrichment.

**The problem:** The claim rests on a negative result (absence from prior studies) that is not quantified. It is possible that many of the 28 proteins were never quantified in prior ABPP experiments (and thus are absent by design, not by lack of ligandability), or that they were quantified but not reported as liganded. Without a detailed comparison table showing which proteins were tested in prior studies and which were not, the claim that brainocytes provide "improved access" to CNS proteins is suggestive but not rigorously supported. The authors do note DPYSL2 was quantified in Ramos cells without enrichment (Figure S4B), which is a good example, but this is one protein.

**What would settle it:** Provide a supplementary table cross-referencing the 28 CNS-enriched liganded proteins against the prior ABPP datasets (Ramos, HEK293T, T cells, etc.), indicating for each protein whether it was (i) quantified and liganded, (ii) quantified but not liganded, or (iii) not quantified. This would clarify whether the brainocyte advantage is discovery of new ligandability or discovery of new proteins.

## Sweep

- The cysteine-directed ABPP data for DPYSL2_C504 show no decrease in IA-DTB reactivity (Figure 4C), yet protein-directed ABPP shows strong enrichment (Figure 4A); the authors explain this via a complexoform-restricted model (Figure S4E), but this explanation is post-hoc and would benefit from direct quantification of the DPYSL2:DPYSL5 complex stoichiometry in brainocytes to confirm that only a small fraction is bound.

- PDE7B_C136 is located at a non-orthosteric site (Figure S3E) and WX-03-57 does not inhibit cAMP hydrolysis (Figure S3F), yet the IP-MS data (Figure 3I) show enhanced association with PKA-AKAP proteins; the functional consequence of this enhanced association is not tested (e.g., does it alter PKA activity or cAMP compartmentalization?).

- The HCN1 cysteine mutants (C542A) show poor or cAMP-independent conductance (Figure S6A, C), preventing direct functional validation that C542 is necessary for the WX-02-679 effect; the authors acknowledge this but do not explain why the mutation is deleterious.

- Flow cytometry shows ~90% viability of brainocytes (Supplementary Dataset S1), but the composition of the cell suspension (neuron vs. glia ratio) is not reported, limiting interpretation of which cell types contribute to the ligandability map.

- The criteria for stereoprobe liganding (>2.5-fold enantioselective enrichment, >33% competitive blockade) are relaxed compared to prior ABPP studies in cell lines (50% blockade), justified by "lower overall uptake" in brainocytes (Figure S2A); however, no quantitative comparison of uptake is provided, and the relaxed threshold may increase false positives.

- The manuscript does not report whether any of the 114 liganded proteins showed stereoprobe reactivity in both brainocytes and lysates with opposite stereoselectivity (i.e., enantiomer-swapped enrichment), which would indicate context-dependent stereochemical selectivity.

- Acute brain slices are incubated with stereoprobes for 1 h at 37 °C in DMEM (Methods), but slices are typically maintained in oxygenated ACSF; the use of DMEM may alter slice physiology and confound the comparison to brainocytes.

## Questions

- Figure 4H shows C504 at the DPYSL2 homo-tetramer interface; is C504 also at the DPYSL2:DPYSL5 hetero-interface, or does hetero-oligomerization induce a conformational change that exposes C504 to solvent?

- In the inside-out patch clamp experiment (Figure 6H), was the membrane potential held constant during cAMP and WX-02-679 application, and were multiple voltage steps tested to confirm the effect is voltage-independent?

- The authors state WX-02-679 "partially rescued" the WT/M153I HCN1 variant (Figure S6D); what is the quantitative definition of "partial," and does the residual shift correlate with the degree of gain-of-function in the unliganded mutant?

---

## Overall Assessment

This is a competent and well-controlled study that makes a solid methodological contribution (ABPP in primary brain cells) and identifies a novel allosteric HCN modulator with interesting pharmacology. The chemical and structural work is rigorous, and the electrophysiology is thorough. However, the central claim that brainocyte-restricted liganding reflects authentic cell-state-dependent interactions is validated only partially (pilot slice data, no quantitative replication), and the claim that WX-02-679 spares basal HCN activity is contradicted by the slice data showing reduced voltage sag. These are not fatal flaws—the work is publishable with minor revision—but they require either clarification or narrower wording of the headline claims. The paper merits acceptance with revision to address the mechanistic ambiguities in the HCN and DPYSL2 findings.