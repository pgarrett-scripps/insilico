# Decision Letter

**Decision:** major

## Summary of Evaluation
The manuscript presents LATTICE, a graph self-supervised learning framework for multimodal spatial omics integration. The panel recognized the ambition of integrating five modality blocks and the systematic modality-ladder evaluation design. However, several critical issues prevent acceptance in its current form.

The primary concern is methodological: the central claim that LATTICE successfully integrates all five modalities is not fully supported by the evidence. While adding scMultiome RNA (M2) shows clear gains, the subsequent addition of chromatin/histone features (M4-M5) reduces agreement with RNA reference clusters without positive demonstration that these modalities are meaningfully integrated rather than simply degrading the embedding. The modality-ladder comparison also confounds input data with model suitability—LATTICE is designed for multimodal data, so its poor performance on RNA-only (M1) is expected, making the M1→M2 gains difficult to interpret as evidence of improvement.

Additionally, the presentation suffers from circular definitions that obscure what LATTICE itself does versus what upstream pipelines (ReCAST, SARSIM) provide. The private data and absent code create a reproducibility gap, though the detailed methods appendix is appreciated. Several key references could not be verified.

The framework shows promise, and the introduction of the MUS metric to address RNA-only benchmark limitations is thoughtful. With revisions that directly address these concerns—particularly providing orthogonal validation that M4/M5 embeddings capture meaningful epigenetic signal—the work could meet In Silico's standards for sound, checkable research.

## Required Revisions
1. 1. **Clarify LATTICE's scope and distinguish it from upstream pipelines.** Revise the manuscript to provide a clear, standalone description of what LATTICE does that occurs *after* the five modality blocks have been harmonized and aligned by ReCAST/SARSIM. Specifically, state whether LATTICE performs a new integration or simply concatenates pre-integrated features, and delineate the novel contribution of the graph SSL framework from the upstream data processing.
2. 2. **Address the methodological confound in the modality-ladder comparison.** To support the claim that adding modalities improves performance, provide a controlled experiment comparing LATTICE-M2 against a unimodal variant of LATTICE (e.g., with cross-modal alignment loss removed/adapted) trained on M1. This will isolate the effect of added data from the effect of model suitability.
3. 3. **Provide positive evidence for chromatin/histone integration in M4/M5.** The current evidence (reduced ARI/NMI, increased MUS/spatial contiguity) is insufficient to demonstrate that spatial ATAC and CUT&Tag are meaningfully integrated. Add at least one orthogonal validation showing that M4/M5 embeddings specifically encode epigenetic signal. For example: (a) demonstrate that the M5 embedding can predict held-out epigenetic features significantly better than the M2 embedding, or (b) identify a spatial region where M4/M5 clusters differ from M2 clusters and correlate with a clear, biologically plausible epigenetic signal (e.g., high ATAC in a promoter region).
4. 4. **Ensure all cited references are verifiable.** Provide complete citations with DOIs or PubMed IDs for GraphST, STAGATE, SpaGCN, SIMO, and MaxFuse. If any of these are preprints, state so clearly. Update the reference list accordingly.
5. 5. **Provide executable code and synthetic validation data.** Share the exact code, environment specifications, and driver scripts used to produce the results. Additionally, provide a minimal synthetic dataset that replicates the structure (5 modality blocks, spatial coordinates) of your cohort, along with a script that reproduces one key result (e.g., training on M2 and reporting ARI improvement over M1). This will allow verification of the computational pipeline independently of the private clinical data.

## Minor Suggestions
- Restructure the manuscript to introduce the LATTICE method (Section 3) before the detailed evaluation setup and cohort description (Section 4.1) to improve narrative flow.
- Clarify in the main text where the MUS metric is first presented that its value is normalized relative to the specific cohort and set of compared methods, and therefore its absolute magnitude is cohort-dependent.
- For the ablation study (Table 3), explicitly state that n=11 samples per condition and confirm that train/validation splits were consistent across comparisons.
- If the arXiv entry 2607.14410v2 is the same manuscript, disclose this in the submission statement and explain the relationship to this submission.
- Consider adding a brief discussion of how the variable input dimensionality (D = 5G, G ∈ [129,322]) is handled during training and whether it affects cross-sample comparisons.