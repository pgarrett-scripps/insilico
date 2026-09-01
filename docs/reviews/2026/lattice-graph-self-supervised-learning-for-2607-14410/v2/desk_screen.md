# Desk Screen Report: LATTICE

## Summary

This manuscript presents LATTICE, a graph-based self-supervised learning framework for integrating multimodal spatial omics data (combining transcriptomic and epigenomic measurements at Visium spot resolution). The work is technically sound, clearly motivated, and addresses a genuine gap in multimodal spatial analysis. The evaluation is conducted on a private 11-sample melanoma cohort with appropriate metrics and ablations.

## Scope Assessment

**In Scope for In Silico:** Yes. This is original computational/methodological research with checkable claims, presented as preliminary work on a private dataset. The authors are transparent about data availability constraints and provide implementation details, hyperparameters, and reproducibility artifacts (Appendices G–H). The work does not make clinical claims requiring patient safety review.

## Threshold Issues

### 1. Data Availability and Reproducibility
**Potential concern:** The core evaluation uses a private, non-public cohort that cannot be released due to institutional data-use agreements. This is a legitimate constraint for clinical biospecimen data, and the authors acknowledge it clearly (Appendix G.3).

**Assessment:** This does NOT warrant desk rejection. The authors:
- Provide anonymized code, Slurm scripts, dependency manifests, and run snapshots
- Document preprocessing, harmonization, and training procedures in detail (Appendices F, H)
- Report metrics across 11 samples with multiple random seeds
- Acknowledge the limitation explicitly and call for "broader external benchmarking"

The work is reproducible *in principle* by anyone with access to similar multimodal spatial data. For In Silico's scope ("whose claims a careful reader can evaluate from the manuscript itself and its cited or deposited materials"), this meets the bar: the claims are modest and the evidence is transparent.

### 2. Methodological Soundness
**Assessment:** The method is sound. The three-component objective (masked reconstruction, cross-modal alignment, spatial regularization) is well-motivated and standard in self-supervised learning. The graph construction is straightforward (spatial kNN). The ablation study (Table 3) isolates the contribution of each component. Theoretical analysis (Appendix I) provides intuition, though it is informal and does not add much beyond the standard literature.

### 3. Evidence–Claim Alignment
**Key finding:** Adding projected scMultiome RNA (M1→M2) substantially improves ARI, NMI, spatial contiguity, and MUS. Adding in situ chromatin (M4–M5) increases spatial contiguity and MUS but *decreases* ARI and NMI relative to M2.

**Interpretation:** The authors interpret this as the embeddings capturing "chromatin and regulatory structure beyond transcriptomic similarity alone," rather than as a failure. This is a defensible interpretation, but it is also the interpretation that makes the result look good. The authors do acknowledge this trade-off and introduce MUS to address it, which is honest. However, the claim that "full multimodal inputs improve spatial coherence and multimodal neighborhood structure" is supported only if one accepts that MUS is a better metric than RNA-reference agreement—a choice that is reasonable but not inevitable.

**Assessment:** The evidence supports the claims as stated, but the claims are somewhat modest and the interpretation of mixed results is author-favorable. This is not a flaw; it is appropriate candor about a preliminary result. Not grounds for rejection.

### 4. Comparison to Baselines
**Assessment:** Table 2 compares LATTICE against GraphST, STAGATE, SpaGCN, SIMO, and MaxFuse on M1 (Visium RNA only). LATTICE M1 underperforms these baselines, which the authors correctly attribute to the architecture being designed for multimodal inputs rather than RNA-only optimization. For M2–M5, no direct baseline comparisons are provided because existing methods do not handle the full multimodal tensor. This is a limitation but not a fatal one: the modality-ladder analysis (M1→M5) serves as an internal control, and the authors acknowledge the need for external benchmarking.

### 5. Clarity and Completeness
**Assessment:** The manuscript is well-written and well-organized. Methods are clearly described. Hyperparameters are fully specified (Appendix H). Limitations are acknowledged (need for external validation, patient-specific treatment effects, no consistent cross-patient signature). The theoretical analysis in Appendix I is informal but does not mislead.

## Minor Issues (Not Grounds for Rejection)

1. **MUS definition (Eq. 11):** The metric is reasonable but somewhat ad hoc. It averages four normalized quantities, each of which could be weighted differently. The authors do not justify the equal weighting. This is a defensible choice but could be made more explicit.

2. **Paired pre/post analysis (Section 4.3):** The authors find no consistent cross-patient treatment signature and conclude that shifts are "patient-specific." This is honest but limits the clinical utility of the work. Not a flaw, but a genuine limitation.

3. **Upstream pipelines (SARSIM, ReCAST):** LATTICE depends on these pipelines for feature construction. The authors position LATTICE as "modular" and "compatible with alternatives," but the evaluation only uses one configuration. This is fine for a first paper, but external validation with different upstream choices would strengthen the work.

4. **Theoretical analysis (Appendix I):** The lemmas are informal and largely restate standard results from graph neural networks and contrastive learning. They do not provide new theoretical insight. However, they do not detract from the work either.

## Verdict

This manuscript presents a competent, honest, and well-executed study of multimodal spatial omics integration. The method is sound, the evaluation is transparent, and the limitations are acknowledged. The claims are modest and supported by the evidence. The work is preliminary (private cohort, no external validation, patient-specific effects) but is presented as such.

The main weakness—reliance on a private dataset—is not a reason to desk-reject. It is a reason for reviewers to assess whether the transparency and reproducibility artifacts compensate for the lack of public data. That is a judgment for the full panel, not a threshold issue for desk screening.

**DESK DECISION: proceed**

The manuscript should be sent for full review. Reviewers should assess:
1. Whether the MUS metric and modality-ladder interpretation are convincing
2. Whether the lack of external benchmarking is acceptable for a preliminary study
3. Whether the theoretical analysis adds value or is redundant
4. Whether the work's contribution to the field justifies publication despite its limitations