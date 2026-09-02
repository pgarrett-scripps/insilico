# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript describes an activity-based protein profiling (ABPP) platform adapted for intact primary brain cells and applies it to identify covalent ligands for CNS-enriched proteins, with particular focus on HCN channels. The work is methodologically sound and the central results are well-supported by the evidence presented. Reproducibility is strong overall: protocols are detailed, data are deposited, and key materials are available. One significant gap concerns the proteomic data processing pipeline; otherwise, the reporting is transparent about limitations and the authors have made genuine efforts to enable replication.

## Strengths

1. The authors provide detailed step-by-step protocols for brain cell dissociation, ABPP workflows (both gel and MS-based), and electrophysiology, with sufficient parameter specification to enable independent replication.

2. Mass spectrometry proteomics data are deposited in ProteomeXchange (PXD082934) with raw files available; processed data are in Supporting Dataset S2; and chemical probes are available from the lead contact with a materials transfer agreement.

3. The functional validation of HCN channel ligands is comprehensive, spanning recombinant systems, inside-out patches, and native hippocampal neurons, with consistent results across three HCN isoforms and two species.

## Weaknesses: Load-bearing claims

**Claim 1: Brainocytes preserve protein-ligand interactions that are lost or altered in brain lysates, and thus represent a superior substrate for mapping CNS-enriched protein ligandability.**

The evidence is Figure 1D–F and Dataset S2, which show that 28 proteins were stereoselectively enriched only in brainocytes, not in brain lysates, while 19 were unique to lysates. The authors argue this reflects authentic cell-context-dependent interactions. However, the alternative explanation — that brainocytes simply have lower overall stereoprobe uptake (acknowledged in Figure S2A) — is not fully excluded. Lower uptake could shift the detection threshold, causing some weak interactions to fall below the noise floor in lysates while remaining detectable in cells, without implying those interactions are functionally relevant *in vivo*. The pilot acute brain slice data (Figure S1D) partially address this by showing brainocyte-restricted interactions are recapitulated in slices, but only for a small subset of proteins (7 examples named). To establish that brainocyte-restricted events represent genuine cell-state-dependent ligandability rather than a detection artifact, the authors would need to show either: (i) that the brainocyte-unique proteins are expressed at similar or higher levels in brainocytes than lysates (Coomassie staining in Figure 1C is a crude proxy), or (ii) that a larger, unbiased sample of brainocyte-restricted interactions replicates in acute slices. The current evidence is suggestive but not definitive.

**Claim 2: WX-02-679 selectively blocks cAMP-modulated gating of HCN channels while sparing basal activity.**

The evidence is Figures 6B–D and S6A–B, showing that WX-02-679 pre-treatment prevents the rightward shift in V₁/₂ induced by cAMP in whole-cell recordings, while basal V₁/₂ (without cAMP) is unaffected. This is strong evidence for the claim as stated. However, the mechanism — whether WX-02-679 acts by blocking cAMP binding, preventing conformational coupling, or some other allosteric effect — is not directly demonstrated. The authors show cAMP competitively blocks WX-02-679 binding (Figure 5E), but do not show the reverse: whether WX-02-679 blocks cAMP binding to the CNBD. An orthogonal binding assay (e.g., fluorescence polarization or surface plasmon resonance with purified CNBD) would clarify whether the ligand acts as a competitive antagonist of cAMP or as an allosteric inhibitor of the cAMP-induced conformational change. The functional result is clear, but the molecular mechanism remains inferred rather than proven.

**Claim 3: DPYSL2 is liganded by WX-01-06/WX-02-26 only when complexed with DPYSL5, and this represents a complexoform-restricted interaction.**

The evidence is Figures 4D–J: co-expression of DPYSL2 with DPYSL5 (but not other DPYSL paralogs) restores WX-01-06 reactivity; a C504A mutation abolishes it; DPYSL5 knockout in SH-SY5Y cells eliminates endogenous DPYSL2 liganding; and Neuro2A cells (which express endogenous DPYSL5) show WX-01-06 reactivity while HCT116 cells (which do not) do not. This is a well-controlled demonstration of complex-dependence. However, the claim that this reflects a ligandable pocket at the DPYSL2:DPYSL5 interface (rather than, say, DPYSL5-induced conformational stabilization of a DPYSL2 pocket) is not directly tested. The authors note C504 is at the inter-subunit interface of DPYSL2 homo-tetramers (Figure 4H) and propose it may be similarly positioned in the hetero-complex, but no structural data (crystal structure, cryo-EM, or even cross-linking mass spectrometry) confirm this. The functional dependence on DPYSL5 is proven; the structural basis is plausible but not demonstrated.

## Weaknesses: Sweep

1. **Proteomic data processing pipeline not fully specified:** The manuscript states that ProLuCID was used to search raw files against UniProt databases (Human 2016-07 or Mouse 2017-07), but does not specify the ProLuCID version, the exact parameters (e.g., precursor mass tolerance, fragment ion tolerance, allowed modifications beyond those listed), or the DTASelect filtering thresholds beyond "peptide false-positive rate below 1%." This limits reproducibility of the MS data processing step.

2. **CNS-enrichment classification criteria are post-hoc and somewhat arbitrary:** Proteins with tissue Z-score >4 in ≥2 datasets and max signal >150 (bioGPS) or >10 (GTEx) in brain are classified as CNS-enriched (Figure S2D), but the rationale for these thresholds and the sensitivity of the results to threshold choice are not explored.

3. **Cysteine-directed ABPP filtering criteria are relaxed relative to prior work (33% vs. 50% parent blockade) without empirical justification:** The authors acknowledge this (main text, "Electrophilic stereoprobe ligandability maps" section) but do not validate that the relaxed threshold does not inflate false positives; a comparison of hit reproducibility across the two thresholds would strengthen this choice.

4. **Flow cytometry viability data (Figure S1, "~90%") lack error bars or replication counts:** It is unclear whether this is a single measurement or an average across multiple preps, and whether 90% is the minimum, mean, or range.

5. **HCN cysteine mutants (C542A, C611A, C662A) show poor or cAMP-independent conductance (Figure S6A, C), preventing functional validation that the liganded cysteine is necessary for the observed effect:** The authors acknowledge this but do not explain why the mutation causes dysfunction or whether it reflects a general destabilization of the channel or a specific role of the cysteine in cAMP sensing.

6. **Competitive gel-ABPP IC₅₀ values (Figure 5J–L) are derived from single experiments with n=2–3 replicates; confidence intervals are reported but statistical power is limited.**

7. **The acute brain slice pilot (Figure S1D) is described as "pilot" and includes only 7 protein examples; it is unclear whether these were pre-selected or represent an unbiased sample of brainocyte-restricted hits.**

8. **Inside-out patch clamp experiment (Figure 6G–H) is shown as a single representative trace with no quantification of replicates or variability.**

## Questions

1. For the brainocyte-restricted liganding events (Figure 1D–F), can the authors report the distribution of protein abundance (by quantitative proteomics) for brainocyte-unique vs. lysate-unique hits, to test whether detection differences correlate with expression level?

2. Does WX-02-679 directly compete with cAMP for binding to the isolated CNBD, or does it act allosterically to prevent cAMP-induced conformational change? A direct binding assay would clarify the mechanism.

3. For the DPYSL2:DPYSL5 complex, is there structural or biochemical evidence (cross-linking MS, co-immunoprecipitation under native conditions, or modeling) that C504 is positioned at the hetero-interface?

4. What are the exact ProLuCID search parameters (precursor and fragment mass tolerance, modification list, and DTASelect thresholds) used for the proteomics data processing?

5. Why do HCN cysteine-to-alanine mutations cause loss of channel function, and does this reflect a general destabilization or a specific role of the cysteine in cAMP binding or gating?