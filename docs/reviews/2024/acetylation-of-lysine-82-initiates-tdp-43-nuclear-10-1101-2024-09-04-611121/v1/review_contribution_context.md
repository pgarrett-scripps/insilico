# Contribution & Prior-Work Reviewer

Based on my comprehensive search of the literature, I can now write the review. Let me compile my findings.

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a mechanistic study linking age-related proteasome decline to TDP-43 nuclear loss of function through lysine 82 acetylation within the classical NLS. The work is technically sound and makes a concrete contribution by identifying K82 acetylation as a specific, sufficient trigger for disrupting importin-α1 binding and nuclear import. The finding of K82 acetylation in all six sporadic ALS motor cortex samples tested provides disease-relevant evidence. However, the core concept that acetylation disrupts TDP-43 nuclear import is not entirely novel: Cohen et al. (2015, ref. 9) already demonstrated that acetylation controls TDP-43 function and aggregation, and Garcia Morato et al. (2022, ref. 35) showed that K136 acetylation drives phase separation and aggregation. The manuscript's specific contribution is narrower than its framing suggests—it identifies K82 as the critical NLS residue and acetylation there as the initiating event, but does not establish acetylation as the primary driver of proteinopathy initiation in vivo, only as one plausible pathway.

## Strengths

1. **Rigorous identification of K82 as a gatekeeper residue**: The systematic mutagenesis (K-to-R variants, single and multi-lysine combinations) elegantly demonstrates that K82 is necessary for importin-α1 binding and that K82 plus either K95 or K97 are sufficient, a level of mechanistic detail not previously reported for TDP-43.

2. **Direct biochemical validation of acetylation effect**: The peptide-binding assay (Fig. 3F) showing that K82 acetylation alone abolishes importin-α1 binding while K79 and K84 acetylation only reduce it provides direct evidence that the acetylation-mimicking K82Q mutation reflects a real post-translational modification consequence.

3. **Comprehensive proteomics and functional readout**: The TMT mass spectrometry showing TDP-43 is the most sensitive protein to proteasome inhibition (>4-fold nuclear depletion), combined with the stathmin-2 splicing assay as a functional readout of TDP-43 loss of function, strengthens the claim that the observed mislocalization has biological consequence.

## Weaknesses: Load-bearing claims

**Claim 1: Acetylation at K82 is sufficient to initiate TDP-43 nuclear loss of function and is the primary mechanism linking proteasome decline to TDP-43 mislocalization.**

The evidence for sufficiency is strong: K82Q acetylation-mimicking mutation blocks nuclear import in cultured neurons (Fig. 3C–E) and K82 acetylation is detected in all six sALS samples (Fig. 5B). However, the claim that this is the *primary* mechanism is not fully established. The manuscript shows that proteasome inhibition induces acetylation at K79, K82, and K84, as well as ubiquitination at these same sites and phosphorylation at S91/S92 (Fig. 3B). While K82 acetylation is the most potent in blocking import, the manuscript does not demonstrate that ubiquitination at K82 or K79/K84 acetylation do not also contribute significantly to mislocalization in vivo. The Discussion acknowledges that "acetylation at lysine 82 (and K79 and 84 to lesser extents)" can initiate mislocalization, but the abstract and main text emphasize K82 as the driver. The relative contribution of these modifications under physiological proteasome decline remains unclear. Additionally, the manuscript does not address whether the acetyltransferases and deacetylases responsible for K82 acetylation are themselves regulated by proteasome activity or whether K82 acetylation is a direct consequence of reduced proteasome activity or an indirect effect.

**Claim 2: K82 acetylation is an early, initiating event in TDP-43 proteinopathy, preceding phosphorylation.**

The evidence is suggestive but not definitive. Figure 5C shows that ac-TDP-43(K82) is detected in both soluble and insoluble fractions of sALS cortex, while phosphorylated TDP-43 is only in the insoluble fraction, leading the authors to propose acetylation is earlier. However, this comparison conflates two different things: (1) the temporal sequence of modifications during disease progression, and (2) the subcellular compartmentalization of modified forms. The presence of ac-K82 in soluble fractions could reflect either earlier acetylation or continuous acetylation of soluble TDP-43 pools, not necessarily temporal precedence. The manuscript provides no direct evidence (e.g., from longitudinal studies, transgenic models, or temporal kinetics in neurons) that acetylation precedes phosphorylation in the disease cascade. The claim that acetylation "initiates" proteinopathy is therefore based on the logic that nuclear loss of function is necessary for aggregation, not on direct evidence of temporal order.

## Weaknesses: Sweep

1. **Ko et al. (2024, ref. 30)** is cited as showing that "single acetylation-mimetic mutation in TDP-43 NLS disrupts importin alpha1/beta signaling," yet this appears to be concurrent or very recent work (J Mol Biol, in press at time of manuscript submission) that makes an overlapping claim; the manuscript does not clearly delineate what is novel here versus what Ko et al. already reported.

2. The manuscript claims TDP-43 is "the protein whose nuclear localization is most sensitive to reduced proteasome activity" (Fig. 1E–F), but this is based on a single TMT experiment in one cell type (iPSC-derived cortical neurons); generalizability to other neuronal types or tissues is not established.

3. The acetylation-specific antibodies (Fig. 5A) were generated by the authors and validated only by ELISA against synthetic peptides; orthogonal validation (e.g., mass spectrometry of endogenous ac-K82-TDP-43 from patient samples) would strengthen the claim that the signal in patient tissue is genuine.

4. The manuscript does not address whether reduced proteasome activity directly acetylates K82 or whether it indirectly increases acetylation by reducing turnover of acetyltransferases or deacetylases; the mechanism linking proteasome decline to K82 acetylation is assumed, not demonstrated.

5. The PY-NLS rescue experiment (Fig. 2E–I) shows that importin-β2-mediated import is resistant to proteasome inhibition, but does not test whether the PY-NLS variant rescues TDP-43 function in vivo or prevents aggregation in a disease model.

6. The variability in K82 acetylation levels across sALS samples (Fig. 5B) is noted but not explained; the manuscript does not correlate acetylation level with disease duration, severity, or other clinical parameters.

7. The manuscript does not discuss why K82 acetylation would be sufficient to block nuclear import while K79 and K84 acetylation are not, given that all three lysines are within the bipartite NLS; the structural basis for K82 specificity is not explored.

8. The claim that acetylation is "plausible" as an initiator of proteinopathy (abstract) is weaker than the evidence supports, but the framing in the main text and figures suggests a more definitive causal role than the data establish.

## Questions

1. **Figure 3B and Methods**: What is the stoichiometry of acetylation, ubiquitination, and phosphorylation at K79, K82, K84, S91, and S92 in the mass spectrometry data? Are these modifications mutually exclusive or do they occur on the same TDP-43 molecules?

2. **Figure 5B**: Can you provide the clinical metadata (disease duration, age at onset, disease progression rate, site of onset) for the six sALS samples and four controls, and correlate K82 acetylation levels with these parameters?

3. **Figure 5C**: Can you quantify the ratio of ac-K82-TDP-43 in soluble versus insoluble fractions for both sALS and control samples, and compare this to the ratio for phosphorylated TDP-43, to support the claim that acetylation precedes phosphorylation?

4. **Methods and Figure 3**: What acetyltransferases and deacetylases are expressed in iPSC-derived cortical neurons, and are their levels or activities altered by proteasome inhibition?

---