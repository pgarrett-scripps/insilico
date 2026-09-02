# Contribution & Prior-Work Reviewer

The search tools are not returning the full biomedical literature. Let me work from what I can verify in the manuscript itself and the references it cites. I'll examine the core claims and the prior work cited.

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript extends activity-based protein profiling (ABPP) from immortalized cell lines and primary immune cells to intact primary brain cells ("brainocytes"), identifies covalent ligands for CNS-enriched proteins using stereochemically defined electrophilic probes, and demonstrates functional modulation of HCN channels by allosteric covalent ligands targeting the cyclic nucleotide-binding domain. The work is technically sound, well-executed, and makes a genuine contribution to the chemical proteomics toolkit. The three main claims—that brainocytes are amenable to ABPP, that this reveals CNS-specific ligandability not seen in cell lines, and that stereoprobes can selectively block cAMP-dependent HCN gating—are all supported by the evidence presented. The contribution is real but incremental: ABPP itself is established methodology (Simon & Cravatt 2010, Liu et al. 1999, Leung et al. 2003), stereoprobes are the authors' own prior work (Njomen et al. 2024, Hayward et al. 2025, Tao et al. 2022), and the functional HCN work, while novel, is a straightforward application of known electrophysiology to a new ligand class. The work is well-situated within the literature and makes no false novelty claims, but it is primarily a methodological extension and proof-of-concept rather than a transformative discovery.

## Strengths

1. The brainocyte preparation is a practical and scalable advance over previous ABPP studies of brain lysates, with clear evidence (Figure 1C–F, S1D) that intact cell context reveals protein interactions absent in vitro, validated in acute brain slices.

2. The HCN channel work is thorough and well-controlled, with complementary approaches (gel-ABPP, cysteine-directed ABPP, patch clamp in heterologous systems, inside-out patches, and ex vivo hippocampal slices) that consistently demonstrate selective blockade of cAMP-dependent gating while preserving basal activity.

3. The DPYSL2 complexoform-restricted liganding discovery is a genuine mechanistic insight—the finding that stereoprobes engage C504 only in the DPYSL2:DPYSL5 hetero-oligomer, not in DPYSL2 alone, is well-supported by the co-expression experiments (Figure 4D–J) and provides a model for how cell context shapes small-molecule–protein interactions.

## Weaknesses: Load-Bearing Claims

**Claim 1: Brainocytes reveal protein interactions absent in brain lysates and cell lines, providing access to CNS-enriched proteins.**

The evidence for this is the comparison in Figure 1D (35 proteins shared between lysates and brainocytes, 19 unique to lysates, 28 unique to brainocytes) and the observation that ~25% of liganded proteins are CNS-enriched (Figure 2E). However, the manuscript does not establish that the brainocyte-unique interactions are *functionally relevant* or that they represent authentic cellular states rather than artifacts of the dissociation procedure. The authors note that brainocyte-restricted interactions are "generally recapitulated in acute brain slices" (Figure S1D), which is reassuring, but only a subset of proteins is shown (7 examples). Critically, the manuscript does not compare brainocytes to other primary CNS cell types (e.g., purified neurons, astrocytes, oligodendrocytes) that would be needed to determine which cell type(s) contribute each liganded protein. The claim that brainocytes provide "improved access to proteins with restricted expression in the nervous system" (Results, second paragraph) is supported by the absence of most CNS-enriched liganded proteins from prior ABPP studies of Ramos B cells and cancer lines (Table 1), but this is a negative result—it does not prove the proteins are ligandable *only* in brain, only that they were not detected before. The alternative explanation is that these proteins require specific co-factors or post-translational modifications present in brain but absent from the cell types previously studied, which is plausible but not distinguished from true tissue-restricted ligandability.

**Claim 2: Stereoprobes block cAMP-induced modulation of HCN channels while sparing basal activity, offering a differentiated pharmacological tool.**

The patch clamp data (Figure 6B–D) clearly show that WX-02-679 pre-treatment prevents the rightward shift in V₁/₂ induced by cAMP, and the inside-out patch (Figure 6H) confirms the effect is direct. The hippocampal slice data (Figure 6J–K) show stereoselective reduction in voltage sag and rebound depolarization. However, the manuscript does not directly measure basal HCN channel activity in the presence of WX-02-679 without cAMP to confirm that basal gating is truly "spared." Figure 6B shows that WX-02-679 alone (without cAMP) yields a V₁/₂ of −95.0 ± 1.8 mV, which is not significantly different from control (−92.1 ± 2.0 mV), suggesting basal activity is preserved; however, this is inferred from the voltage-clamp protocol rather than directly measured as a conductance or current amplitude at a fixed voltage. The claim that WX-02-679 "specifically disrupts the cAMP-modulated, but not basal function" (Results, HCN section) is supported by the data but would be stronger with explicit quantification of basal current amplitude (e.g., at −70 mV) before and after WX-02-679 in the absence of cAMP. The cysteine mutant HCN channels (C542A) show "poor or cAMP-independent channel conductance" (Results, HCN section), which prevents direct validation that C542 is the functional target; the authors acknowledge this but do not explain the mechanism. This is a limitation but not a fatal flaw, since the site-specific engagement is confirmed by gel-ABPP and the functional effect is clearly on-target by all other measures.

## Weaknesses: Sweep

1. The manuscript claims that previous ABPP studies of brain lysates identified covalent inhibitors for serine hydrolases (endocannabinoid and lysophospholipid lipases) but does not cite the specific papers; reference 22 is cited for "serine hydrolase" ABPP in brain lysates, but the text does not verify whether those studies actually identified the lipases mentioned or whether they were identified by other methods.

2. The cysteine-directed ABPP data for PDE7B (Figure 3F) show "corrupted enrichment" of the C136-containing peptide in protein-directed ABPP, which the authors interpret as a hallmark of stereoprobe-liganded cysteines, but this interpretation is not validated against a set of known non-liganded cysteines to confirm the specificity of this signature.

3. The functional assay for PDE7B (Figure S3F) shows that WX-03-57 does not inhibit cAMP hydrolysis, supporting the claim that the ligand is allosteric; however, the assay uses lysates or intact cells, and it is not clear whether the stereoprobe concentration (20 µM) is sufficient to achieve full occupancy of C136 in the cellular context.

4. The manuscript does not report whether the stereoprobes show any off-target reactivity with non-cysteine residues (e.g., lysine, serine, histidine) that might confound the interpretation of the ligandability maps; the use of IA-DTB in cysteine-directed ABPP assumes complete blockade of free cysteines, but this is not validated.

5. The claim that DPYSL2:DPYSL5 complexes create a "unique ligandable pocket" (Discussion) is inferred from the location of C504 at the inter-subunit interface (Figure 4H), but the manuscript does not provide structural evidence (e.g., cryo-EM, crystal structure, or molecular dynamics) that the stereoprobe-binding pocket exists or that its geometry is altered in the hetero-oligomer.

6. The HCN1 epilepsy variants (E246K, M153I) are rescued by WX-02-679 (Figure 6E–F, S6D), but the rescue is only partial for M153I and the mechanism is not explored; it is unclear whether the compound restores normal gating kinetics or simply shifts the activation curve, and whether this would translate to therapeutic benefit in vivo.

7. The manuscript does not discuss the potential for off-target effects of WX-02-679 in the hippocampal slice experiments; while the authors show that HCN pore blockers (ivabradine, RO-27569) do not affect stereoprobe binding, they do not show that WX-02-679 does not engage other cysteine-containing proteins in the slice.

8. The CNS-enriched protein list (Table 1, Figure 2E) is based on RNA-seq data (bioGPS, GTEx, BrainRNASeq.org) but does not account for post-translational regulation or cell-type-specific protein abundance; a protein with high mRNA in brain may have low protein abundance if it is rapidly degraded or sequestered.

## Questions

1. Figure 1D reports 82 enantioenriched proteins total (35 shared, 19 lysate-unique, 28 brainocyte-unique); what is the distribution of these proteins across the four stereoisomeric configurations (Figure 2B–D), and do brainocyte-unique proteins show different stereoisomeric preferences than shared proteins?

2. For the brainocyte-unique liganded proteins (28 total), how many are validated by cysteine-directed ABPP, and for those that are not, what is the evidence that the protein-directed enrichment is not a false positive from co-enrichment of a nearby protein?

3. In the PDE7B IP-MS experiment (Figure 3I), the authors report stereoselective enhancement of interactions with PRKAR1A, AKAP8L, and AKAP8; are these interactions specific to the WT-PDE7B:C136A comparison, or do they also occur with the enantiomeric stereoprobe WX-03-59?

4. For the HCN channel experiments, what is the IC₅₀ of WX-02-679 for engagement of off-target cysteine-containing proteins in the brainocyte proteome, and is there evidence that the compound is selective for HCN channels in the cellular context?

---

## Minor Issues

- The manuscript is well-written and the figures are clear, but some panels are dense (e.g., Figure 2B–D); a summary table of liganded proteins by functional class would aid interpretation.
- The Materials and Methods are comprehensive and should support reproducibility, though the exact composition of the MACS Octodissociator enzyme mix is proprietary and may limit replication in other labs.