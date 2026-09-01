# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

LATTICE presents a graph-based self-supervised learning framework for multimodal spatial omics integration, evaluated on an 11-sample private melanoma cohort. The core contribution—combining masked reconstruction, cross-modal alignment, and spatial regularization objectives—is sound in principle and the authors provide substantial implementation detail. However, the reproducibility of the central empirical claims is severely compromised by the unavailability of the primary dataset, and the evidence that multimodal integration improves spatial organization is confounded by upstream preprocessing choices that are not fully disclosed or ablated. The work is technically competent but cannot be independently verified on its main claims, and the interpretation of results (especially the divergence between ARI/NMI and MUS metrics) rests on assumptions about what the embeddings capture that are not empirically tested.

## Strengths

1. The authors provide detailed hyperparameters, architecture specifications, and training procedures (Appendix H) sufficient to reimplement the model itself, including loss weights, layer counts, and optimization settings.

2. The modality ladder (M1–M5) is a transparent design choice that isolates the contribution of each data source, and the ablation study (Table 3) directly tests the necessity of training components.

3. The manuscript candidly acknowledges limitations: patient-specific treatment effects, metric trade-offs, and the gap between RNA-reference agreement and spatial coherence metrics, rather than claiming universal improvement.

## Major Weaknesses

**1. Dataset unavailability blocks verification of all empirical claims.**

The 11-sample melanoma cohort is private, proprietary, and explicitly stated as non-redistributable (Appendix G.1: "cannot be redistributed publicly"). This is the sole dataset on which all reported results rest: Table 2 (cohort-level benchmarks), Figure 2 (modality-ladder trends), Figure 3 (pre/post-treatment shifts), and Figures 4–6 (spatial domains, TF programs, accessibility links). The authors state "no public five-modality substitute at this lattice resolution" exists. Without access to the data, a reader cannot verify whether the reported metrics are computed correctly, whether the modality ladder truly produces the claimed improvements, or whether alternative explanations (e.g., differences in upstream preprocessing between M1 and M2) account for the observed gains. The authors deposit "anonymized code, Slurm driver scripts, pinned dependency manifests, and run snapshots as supplementary material" but do not specify where or how to access these. A preprint server URL, GitHub repository, or explicit supplementary materials path is absent. This is a HARD reproducibility failure: the load-bearing empirical results cannot be inspected or rerun.

**2. Upstream preprocessing (ReCAST and SARSIM) is not ablated, confounding the attribution of improvements to LATTICE.**

The multimodal feature matrix X is constructed by ReCAST (harmonization, quality control, gene intersection) and SARSIM (cell-to-spot mapping, regulatory projection). The authors state that ReCAST performs "sample-level quality checks" and "cross-modality gene and feature harmonization" (Appendix F), but do not report which samples failed QC, what harmonization operations were applied, or how the "strict five-way gene intersection" was computed. The jump from M1 (ARI 0.269, NMI 0.364) to M2 (ARI 0.426, NMI 0.507) is the largest gain in Table 2, yet M2 adds not only scMultiome RNA but also SARSIM's spatially anchored regulatory projection. It is unclear whether the improvement comes from the additional modality, the projection quality, or the harmonization step. The authors do not report: (i) the gene intersection size before and after ReCAST filtering, (ii) whether SARSIM's soft cell-to-spot mapping introduces systematic bias toward certain spatial domains, or (iii) performance of LATTICE M2 if scMultiome RNA were projected using a naive nearest-neighbor mapping instead of SARSIM. Without these ablations, the claim that "adding projected scMultiome RNA substantially improved concordance" (Abstract) is confounded with upstream engineering choices.

**3. The interpretation of ARI/NMI decline at M4–M5 as evidence of chromatin-driven structure is not empirically tested.**

The authors observe that ARI and NMI decrease from M3 (ARI 0.417) to M5 (ARI 0.329) while spatial contiguity and MUS increase, and interpret this as the embeddings capturing "chromatin and regulatory structure beyond transcriptomic similarity alone" (Abstract). However, this interpretation assumes that the Space Ranger RNA-derived clusters are a valid reference for what the embeddings should recover. An alternative explanation is that spatial ATAC and CUT&Tag introduce noise or artifacts that degrade clustering quality, or that the cross-modal alignment loss (Eq. 8) creates a bottleneck when modalities are weakly correlated. The authors do not report: (i) the correlation structure between modalities (e.g., Pearson r between Visium RNA and spatial ATAC gene scores), (ii) whether M4 and M5 embeddings are more similar to spatial ATAC/CUT&Tag clusters than to RNA clusters (which would support the interpretation), or (iii) whether the decline in ARI/NMI is driven by specific samples or is cohort-wide. The MUS metric (Eq. 11) is defined post-hoc to reward the observed M4–M5 behavior, raising the question of whether it measures genuine multimodal utility or simply validates the authors' preferred outcome. Without independent validation (e.g., against known spatial domains from histology or independent spatial transcriptomics), the claim that chromatin features improve spatial organization remains speculative.

## Soft Weaknesses

1. **ReCAST is presented as an internal pipeline with no public code or documentation**, making it impossible to audit the harmonization step or reuse it on external data; the authors note it "is an internal engineering pipeline" (Appendix F) but do not commit to release.

2. **The five-way gene intersection is sample-specific** (D = 5G with G ∈ [129, 322]), yet the paper does not report how this variability affects embedding quality or whether results are sensitive to the intersection size.

3. **SARSIM is cited as a concurrent preprint** ("bioRxiv, 2026") with no DOI or accessible URL, preventing readers from verifying the regulatory projections or understanding the soft cell-to-spot mapping.

4. **The cross-modal alignment loss (Eq. 8) is applied only to modality pairs 0 and 1** (Visium RNA and spatial ATAC), not all pairs; the rationale for this choice and its impact on M4–M5 results are not discussed.

5. **Early stopping spans 36–63 epochs** (Appendix G.2) with high variance, yet no learning curves or convergence diagnostics are shown, making it unclear whether the model is stable or sensitive to initialization.

6. **The leave-one-patient-out analysis (Section 4.3) reports "mixed" cross-patient generalization** but does not provide numerical results, making it impossible to assess whether the embeddings are truly patient-specific or whether the sample size is simply too small.

7. **Figures 4–6 show results for one patient only**, and no cohort-level summary of spatial domains, TF programs, or accessibility links is provided, limiting the generalizability of the downstream analyses.

8. **The theoretical analysis (Appendix I) proves that the objective balances three properties** but does not establish that the learned embeddings are optimal or unique, nor does it connect to the empirical results.

## Questions

1. Where are the supplementary code, manifests, and run snapshots deposited, and under what access terms (public repository, institutional archive, or author request)?

2. What is the correlation structure between modalities (Pearson r or mutual information) at M1–M5, and does it explain the ARI/NMI decline at M4–M5?

3. Do M4–M5 embeddings cluster more coherently with spatial ATAC or CUT&Tag derived labels than with Space Ranger RNA labels, and if so, what is the ARI/NMI for those comparisons?

4. Why is the cross-modal alignment loss applied only to modality pairs 0 and 1, and what happens if all pairs are aligned?

5. Can the authors provide the learning curves and early-stopping epoch counts per sample to assess convergence stability?