# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Overall Assessment

LATTICE presents a graph-based self-supervised learning framework for multimodal spatial omics integration with a reasonable methodological foundation, but the statistical evaluation contains several critical gaps that prevent the claims from being fully supported. The core contribution—combining masked reconstruction, cross-modal alignment, and spatial regularization—is sound in principle, but the empirical validation relies on metrics that are either inadequately defined, computed against a biased reference, or reported without proper uncertainty quantification. The modality-ladder results (M1–M5) are the paper's main evidence, yet the statistical properties of these comparisons are not established. The work would benefit from major revision addressing the statistical rigor of the evaluation before acceptance.

## Strengths

1. The authors transparently acknowledge that adding chromatin modalities reduces agreement with RNA-only reference labels (ARI/NMI decrease from M2 to M5) and propose MUS as an alternative metric, rather than hiding this trade-off.

2. Reproducibility artifacts are well-documented: pinned dependencies, Slurm logs, hyperparameters, and random seeds are provided in appendices, enabling readers to assess computational claims.

3. The modular design allows LATTICE to accept multimodal inputs from different upstream pipelines (SARSIM, ReCAST, or alternatives), increasing practical extensibility.

## Major Weaknesses: Load-Bearing Claims

### 1. The modality-ladder comparison (M1–M5) lacks statistical testing and proper uncertainty quantification.

The central claim is that "adding scMultiome RNA to Visium RNA alone substantially improved concordance with Space Ranger clusters across 11 runs (ARI +0.157, NMI +0.143, spatial contiguity +0.174)." Table 2 reports means and standard deviations (e.g., M1: 0.269 ± 0.067, M2: 0.426 ± 0.075 for ARI), but no statistical test is performed to establish whether the M1→M2 difference is significant. The manuscript states "across 11 runs" but does not clarify whether these are 11 independent samples (the cohort size) or 11 random seeds applied to the same data. If the latter, the standard deviations reflect optimization variance, not sampling variance, and cannot support a claim about the effect of adding a modality. The reported ±values appear to be standard deviations across the 11 samples (Appendix A.1 mentions "11 successful cohort runs"), making n=11 the independent unit. A paired t-test or non-parametric alternative (Wilcoxon signed-rank) should be applied to each M-level transition to test whether the difference is significant. Without this, the claim that M2 "substantially improved" M1 is unsupported—the difference could reflect sampling noise or the particular composition of the 11-sample cohort. The same applies to all other M-level transitions and comparisons with baselines in Table 2.

**What would resolve this:** Report paired statistical tests (with p-values and effect sizes) for each M-level transition and each baseline comparison, with n=11 samples as the unit of replication. State the test used (e.g., paired t-test with Bonferroni correction for multiple comparisons across M1–M5) and whether assumptions (normality, equal variance) were checked or a non-parametric test was used instead.

### 2. The multimodal utility score (MUS) is defined but not validated as a meaningful metric.

Equation 11 defines MUS as the unweighted average of four normalized quantities: spatial contiguity, silhouette, same-cluster spatial-neighbor fraction, and embedding k-NN overlap with spatial k-NN. The normalization procedure is deferred to "Appendix A.2" but the appendix only states "min–max normalized across all methods and LATTICE modality-ladder rows in the cohort evaluation pool before averaging." This is circular: the normalization depends on the set of methods being compared, so MUS values are not comparable across different benchmark sets or external studies. More critically, there is no justification for why these four quantities should be equally weighted, why they measure "multimodal utility," or whether they are independent (if they are correlated, averaging them double-counts shared variance). The claim that "LATTICE M5 has the highest MUS" (Section 4.2) rests on this unvalidated metric. If MUS is meant to capture aspects of embedding quality that ARI/NMI miss (because they reward RNA-only agreement), then MUS should be validated against held-out biological ground truth or external multimodal benchmarks—neither of which is provided.

**What would resolve this:** Either validate MUS against an independent multimodal benchmark (e.g., a public dataset with known regulatory domains), or report the four component metrics separately and let readers judge their relative importance. If equal weighting is arbitrary, justify it or perform a sensitivity analysis showing that conclusions hold under alternative weightings.

### 3. The claim that chromatin modalities capture "regulatory and chromatin structure beyond transcriptomic similarity" is inferred from metric changes, not demonstrated.

The authors observe that ARI and NMI decrease from M2 to M5 while spatial contiguity and MUS increase, and interpret this as evidence that M4–M5 embeddings capture chromatin structure that does not align with RNA-derived clusters. However, this interpretation conflates two possibilities: (i) the embeddings genuinely capture regulatory structure that is orthogonal to transcriptomics, or (ii) the added chromatin noise or artifacts degrade the embedding quality in a way that happens to increase spatial contiguity by chance or by overfitting to spatial proximity. The ablation study (Table 3) shows that removing spatial regularization lowers spatial contiguity, but does not test whether the chromatin modalities themselves are informative. A critical test would be to train M5 on a scrambled or permuted version of the spatial ATAC and CUT&Tag blocks and check whether spatial contiguity still increases; if it does, the gain is not due to the chromatin signal. Alternatively, the authors could show that M4–M5 embeddings recover known chromatin-defined domains (e.g., from independent ChIP-seq or ATAC-seq studies) better than M2–M3, but this is not done.

**What would resolve this:** Either (a) report spatial contiguity and MUS for M5 trained on permuted chromatin blocks, or (b) validate M4–M5 embeddings against independent chromatin-based ground truth (e.g., known regulatory domains from external data). Without one of these, the claim that chromatin modalities improve the embedding is confounded with the possibility that they simply increase spatial smoothness without adding biological signal.

## Sweep: Secondary Issues

1. **Baseline comparisons are not on equal footing:** Table 2 compares LATTICE M1 (Visium RNA only) against GraphST, STAGATE, and SpaGCN on M1, but LATTICE M1 underperforms these baselines (ARI 0.269 vs. 0.423 for GraphST). The authors note this is expected because LATTICE is "designed for multimodal representation learning," but this makes the M1 comparison uninformative—LATTICE is not optimized for single-modality tasks, so poor M1 performance does not validate the method. The meaningful comparison is LATTICE M2+ against baselines, but baselines are not re-run on M2+ inputs, so it is unclear whether LATTICE's gains come from the method or from the additional modality data.

2. **Patient-level analysis (Section 4.3) reports no statistical test for pre/post-treatment separation:** Figure 3 shows PCA plots with apparent separation, but no test (e.g., PERMANOVA, discriminant analysis) is applied to quantify whether pre/post samples are significantly separated or whether the shift is patient-specific as claimed.

3. **Ablation study (Table 3) uses the same 11 samples without cross-validation:** Removing masking or spatial regularization and re-training on the same data risks overfitting to the specific cohort. A leave-one-sample-out or k-fold cross-validation would be more convincing.

4. **Marker gene enrichment score (Appendix A.2) is defined but never reported:** The appendix defines a "marker gene enrichment score" but it does not appear in any results table or figure, so its relevance is unclear.

5. **Hyperparameter selection is not described:** Appendix H lists fixed hyperparameters (λ₁=1.0, λ₂=0.5, λ₃=0.1, k=6, masking ratio=0.15) but does not explain how these were chosen or whether they were tuned on the 11-sample cohort (which would introduce selection bias if the same cohort is used for evaluation).

6. **Cross-modal alignment loss (Eq. 8) is applied only to modality pairs 0 and 1 (Visium RNA and spatial ATAC):** The text states "modality indices zero and one correspond to Visium RNA and spatial ATAC" but does not justify why only these two modalities are aligned, or whether aligning all pairs would improve results.

7. **Early stopping patience is 20 epochs with a mean of 45.2 epochs to convergence:** This suggests early stopping is rarely triggered, raising the question of whether the model is actually converging or simply running to the epoch limit.

8. **The five-way gene intersection reduces feature dimension substantially (D ∈ [129, 322]):** This aggressive filtering is necessary for alignment but is not justified—no analysis shows how results change if a less stringent intersection (e.g., union or modality-specific subsets) is used.

## Questions

- In Table 2, are the ± values standard deviations across the 11 samples or across 11 random seeds on the same data? If the latter, how should these be interpreted as evidence for the effect of adding a modality?
- For the M1→M2 transition, what is the p-value of the paired comparison, and is it significant after correction for multiple comparisons across M1–M5?
- How were the hyperparameters (λ₁, λ₂, λ₃, k, masking ratio) selected, and were they tuned on the 11-sample cohort used for evaluation?