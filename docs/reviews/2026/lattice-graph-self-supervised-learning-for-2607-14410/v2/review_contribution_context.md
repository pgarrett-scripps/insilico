# Contribution & Prior-Work Reviewer

Based on my searches, I now have sufficient information to write the review. Let me compile my findings on the contribution and prior work.

---

SCORE: 3
CONFIDENCE: 4

## Summary

LATTICE proposes a graph self-supervised learning framework combining masked reconstruction, cross-modal alignment, and spatial regularization for multimodal spatial omics integration. The work is evaluated on an 11-sample private melanoma cohort with five aligned modality blocks. The core contribution is methodologically sound but incremental: it assembles existing self-supervised objectives (masked autoencoders, noise-contrastive estimation, graph Laplacian smoothing) into a unified framework for a specific data type. The main empirical finding—that adding projected scMultiome RNA to Visium RNA improves clustering metrics—is useful but expected. The claim that full multimodal inputs improve spatial coherence while reducing RNA-reference agreement is interesting but underdeveloped: the paper does not establish whether this reflects genuine capture of regulatory structure or simply noise from lower-quality epigenomic signals. Evaluation is limited to a single private cohort with no external benchmarking, and the theoretical contribution (Appendix I) is trivial. The work is technically competent and addresses a real problem, but the evidence for the claimed benefits of multimodal integration remains incomplete.

## Strengths

1. **Honest reporting of trade-offs**: The authors transparently document that ARI/NMI decrease when adding chromatin modalities (M4–M5), and they do not overstate this as an unambiguous improvement, instead proposing the MUS metric to capture complementary aspects of spatial organization.

2. **Reproducible implementation and artifact release**: The paper provides pinned dependencies, Slurm scripts, hyperparameter details, and per-sample training logs sufficient for replication on similar data, and commits to code release in camera-ready form.

3. **Modular design**: LATTICE is explicitly decoupled from upstream projection tools (SARSIM, ReCAST) and downstream tasks, making it compatible with alternative integration strategies and emerging spatial platforms.

## Weaknesses: Load-Bearing Claims

### 1. Multimodal integration improves spatial organization beyond RNA alone (M1→M5 ladder)

The paper's central claim is that adding chromatin and histone modalities to Visium RNA improves spatial structure. The evidence is mixed and does not establish the mechanism. Adding projected scMultiome RNA (M1→M2) yields large gains in ARI (+0.157), NMI (+0.143), spatial contiguity (+0.174), and MUS (+0.622), all of which are expected because scMultiome provides higher-resolution transcriptional signal mapped to the same spots. However, adding spatial ATAC and CUT&Tag (M3→M4→M5) decreases ARI and NMI while increasing spatial contiguity and MUS. The paper interprets this as the embeddings capturing "chromatin and regulatory structure beyond transcriptomic similarity alone" (Abstract, Section 4.2). This interpretation is not established. Three alternative explanations are equally consistent with the data: (i) the chromatin signals are lower quality or noisier than RNA, pulling the embedding away from the true RNA-derived clusters; (ii) the spatial regularization term (Eq. 9) dominates when chromatin features are added, artificially smoothing the embedding regardless of biological signal; or (iii) the cross-modal alignment loss (Eq. 8) creates spurious correlations between modalities that do not share true biological structure. The paper does not distinguish these. To resolve this, the authors would need to show that M4–M5 embeddings recover known regulatory domains (e.g., from independent ChIP-seq or validated TF binding sites), or that they predict treatment response or other clinical outcomes better than M2–M3, neither of which is demonstrated. The ablation (Table 3) shows that removing spatial regularization lowers spatial contiguity but does not show whether the contiguity gain from M3→M5 is driven by biological signal or by the spatial loss overfitting to proximity. Without external validation or a mechanistic explanation, the claim that full multimodal inputs improve biological organization is unsupported.

### 2. LATTICE learns unified spot-level representations from multimodal features (positioning vs. baselines)

The paper claims LATTICE differs from prior work by learning "one embedding space for downstream spatial and regulatory analysis without requiring a separate alignment stage" (Section 2). However, the comparison to baselines is incomplete and potentially misleading. GraphST, STAGATE, and SpaGCN are single-modality spatial clustering methods; comparing LATTICE M1 (Visium RNA only) to them is fair, but LATTICE M1 underperforms (ARI 0.269 vs. GraphST 0.423), which the authors correctly attribute to LATTICE being designed for multimodal input. However, the paper does not compare LATTICE M2–M5 to SIMO or MaxFuse, the multimodal baselines cited in Table 2. SIMO and MaxFuse are described as "match or align dissociated cells to tissue, yielding maps or fused views rather than a unified encoder over spot-aligned multimodal tensors" (Section 2). This characterization may be unfair: SIMO (Yang et al. 2025, Nat. Commun.) and MaxFuse (Zhu & Ma 2024, Nat. Biotech.) both produce integrated embeddings, not just maps. The paper does not explain why these methods cannot be applied to the same M2–M5 input tensors, nor does it report their performance on the same cohort under the same evaluation metrics. Without a direct head-to-head comparison on the same data and modality ladder, the claim that LATTICE uniquely learns unified multimodal representations is not established. The comparison in Table 2 uses different modality inputs for different methods (e.g., SpaGCN uses M1 + histology, MaxFuse uses scRNA + spatial ATAC), which conflates method differences with input differences.

### 3. The combination of three self-supervised objectives yields stable, reproducible embeddings (training design)

The paper proposes combining masked reconstruction (Eq. 6), cross-modal alignment (Eq. 8), and spatial regularization (Eq. 9) with fixed weights (λ₁=1.0, λ₂=0.5, λ₃=0.1). The ablation (Table 3) shows that removing spatial regularization lowers spatial contiguity and removing masking changes silhouette, supporting the inclusion of each term. However, the ablation does not test the loss weights or their sensitivity. The paper reports "stable optimization behavior" and "reproducible embeddings across analysis seeds" (Abstract) but provides limited evidence. Section 4.3 mentions "11 analysis seeds {7, 11, 19, 23, 29, 31, 37, 41, 43, 47, 53}" and states that embeddings are "reproducible," but no quantitative stability metric (e.g., Procrustes distance, rank correlation of nearest neighbors across seeds) is reported. Figure 3 shows PCA of pre/post-treatment samples for three patients, but does not quantify embedding variance across seeds. The claim of reproducibility is stated but not measured. To support it, the authors should report the mean and variance of key metrics (ARI, NMI, silhouette) across the 11 seeds, and show that embeddings from different seeds recover the same nearest-neighbor structure or cluster assignments.

## Weaknesses: Sweep

1. **Private data with no public substitute**: The cohort is proprietary and cannot be released (Appendix G.1), and the authors acknowledge "no public five-modality substitute at this lattice resolution" exists. This prevents independent verification and limits generalizability assessment; external benchmarking on public datasets (e.g., 10x Visium + scMultiome pairs) would strengthen the contribution.

2. **Theoretical analysis is trivial**: Appendix I proves that minimizing a sum of three losses yields embeddings that satisfy all three objectives (Theorem I.4), which is a tautology and adds no insight into why this particular combination is optimal or how the objectives interact.

3. **Modality ladder is confounded with upstream preprocessing**: M1–M5 differ not only in which modalities are included but also in how they are preprocessed (SARSIM vs. ReCAST) and which genes are retained (sample-specific intersection, G ∈ [129, 322]). Isolating the effect of adding modalities from the effect of preprocessing choices is not possible from the reported results.

4. **MUS metric is ad-hoc and not validated**: The multimodal utility score (Eq. 11) averages four normalized quantities with equal weight, but no justification is given for this choice or for the specific metrics included. The normalization is min–max across methods and rows (Appendix A.2), which makes MUS dependent on the comparison set and not interpretable in absolute terms.

5. **Patient-level analysis does not support treatment signature claims**: Section 4.3 states that "global shift alignment is near zero" and "leave-one-patient-out prediction is mixed," leading to the conclusion that "treatment-associated shifts remain patient specific." This is presented as a finding, but it is a negative result that does not validate the method; it simply shows that the embeddings do not capture a universal treatment effect, which is expected if the cohort is small (n=3 paired patients) and heterogeneous.

6. **Masking ratio and other hyperparameters are not justified**: The masking ratio ρ=0.15 (Appendix H) is standard for masked autoencoders in vision but not validated for spatial omics. No sensitivity analysis is provided, and the paper does not explain why this ratio is appropriate for multimodal features with different sparsity patterns.

7. **Cross-modal alignment loss uses only two modalities**: Equation 8 aligns only modalities a and b, but the paper does not specify which pairs are used or whether all pairs are aligned. If only Visium RNA and spatial ATAC are aligned (as suggested by "modality indices zero and one" in Appendix H), then scMultiome RNA, scMultiome ATAC, and CUT&Tag are not directly aligned to each other, which may limit the integration.

8. **Spatial contiguity metric is not clearly defined**: The paper uses "spatial contiguity" as a key metric but does not define it precisely in the main text. Appendix A.2 refers to "SpotCut_v" and "graph-edge spatial contiguity on the spot kNN graph," but the exact formula is not provided, making it difficult to assess whether improvements are meaningful.

## Questions

1. **For the M3→M5 ARI/NMI decrease**: Can you report the per-sample ARI and NMI for M2, M3, M4, M5 to show whether the decrease is consistent across samples or driven by outliers? And can you validate M4–M5 embeddings against independent chromatin data (e.g., ChIP-seq peaks, validated TF binding sites) to test whether they capture true regulatory structure?

2. **For the baseline comparison**: Why were SIMO and MaxFuse not evaluated on the same M2–M5 input tensors and modality ladder? Can you report their performance alongside LATTICE on the same cohort?

3. **For reproducibility claims**: Can you report the mean and variance of ARI, NMI, and silhouette across the 11 analysis seeds, and quantify embedding stability using Procrustes distance or rank correlation of nearest neighbors?

4. **For the cross-modal alignment loss**: Which modality pairs are aligned in Equation 8? If only two pairs are used, why not align all pairs, and what is the effect of aligning all pairs vs. a subset?

5. **For the spatial contiguity metric**: Can you provide the exact formula for SpotCut_v and show that improvements in spatial contiguity from M3→M5 are not driven solely by the spatial regularization term (Eq. 9) overfitting to proximity?