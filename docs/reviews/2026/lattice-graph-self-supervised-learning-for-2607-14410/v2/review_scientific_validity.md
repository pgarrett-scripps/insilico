# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Overall assessment

LATTICE presents a reasonable graph-based self-supervised framework for multimodal spatial omics integration, but the core claims about multimodal utility rest on a reference-dependent evaluation that systematically penalizes the method's own stated objective. The work is technically sound and honestly reported, but the evidence does not support the headline claim that full multimodal integration improves spatial organization in a way that matters beyond the specific RNA-reference comparison chosen. The modality ladder shows trade-offs, not gains, and the authors acknowledge this but do not resolve the ambiguity about what the embeddings actually capture.

## Strengths

1. The authors transparently report that adding chromatin and histone modalities decreases ARI/NMI agreement with RNA-derived reference labels while increasing spatial contiguity and MUS, and they do not hide this tension.

2. The multimodal utility score (MUS) is a thoughtful attempt to measure complementary aspects of spatial organization beyond RNA similarity, and its construction is explicit enough to inspect.

3. The ablation study (Table 3) isolates the contribution of spatial regularization and masking, and test-time modality withholding shows the model remains stable when chromatin blocks are omitted.

## Load-bearing claims

**Claim 1: "Full multimodal inputs produced the strongest spatial coherence and MUS performance" (Abstract and Results).**

The evidence is Table 2, which shows M5 (full input) achieves the highest MUS (0.803) and spatial contiguity (0.850). However, MUS is a composite metric defined by the authors to reward spatial contiguity, silhouette, and neighborhood consistency — the very properties the spatial regularization loss directly optimizes for. This is not a confound; it is a design choice. The problem is that MUS does not measure whether the multimodal signal itself improves the embedding beyond what spatial regularization alone would produce. A spatial-only baseline (graph convolution on concatenated features with spatial loss but no reconstruction or alignment objectives) is absent. Without it, we cannot distinguish whether the gains come from the multimodal architecture or from the spatial loss dominating the objective. The authors report that removing spatial regularization (Table 3) drops spatial contiguity from 0.850 to 0.783 — a large effect — but do not show what happens to MUS when spatial regularization is removed. If MUS remains high, the multimodal components are not driving the headline result. If it drops sharply, spatial regularization is the load-bearing term, not multimodal integration. Report MUS with and without spatial regularization to settle this.

**Claim 2: "Adding scMultiome RNA to Visium RNA alone substantially improved concordance with Space Ranger clusters" (Abstract, M1→M2 transition).**

The evidence is Table 2: M1 to M2 shows ARI +0.157, NMI +0.143, spatial contiguity +0.174. This is the largest single step in the ladder and is presented as a success. However, M1 (Visium RNA only) achieves ARI 0.269 ± 0.067, which is substantially lower than GraphST (0.423 ± 0.124) and STAGATE (0.308 ± 0.136) on the same modality. LATTICE M1 underperforms because the architecture is "designed for multimodal representation learning rather than optimization for transcriptomic clustering alone" (Results, Section 4.2). This is honest, but it means the M1→M2 gain is not evidence that scMultiome RNA improves Visium RNA; it is evidence that LATTICE recovers performance when given multimodal input. A fair comparison would be to show that M2 outperforms GraphST or STAGATE on the same M2 input (Visium + scMultiome RNA). Table 2 does not provide this. The M1→M2 improvement is real but does not isolate the value of the second modality from the value of having any multimodal input at all. Compare LATTICE M2 against GraphST and STAGATE trained on the same M2 feature matrix to show that the multimodal architecture adds value beyond the baseline methods.

**Claim 3: "LATTICE is a practical and empirically grounded framework for multimodal spatial omics integration" (Abstract).**

The evidence is one private 11-sample melanoma cohort with no external validation, no public benchmark, and no comparison to other multimodal spatial methods on the same data. MaxFuse and SIMO appear in Table 2 but are trained on M1 (Visium RNA only), not on the full multimodal input. The authors state: "we do not claim a consistent cross-patient treatment signature" (Section 4.3) and "these results show that LATTICE captures stable sample-level structure while preserving patient-specific variation" — a retreat from the paired-sample analysis to per-sample stability. The cohort is small, the modalities are proprietary (spatial ATAC and CUT&Tag from an internal pipeline, ReCAST), and the upstream projection (SARSIM) is also from the authors' group. This is not a flaw in itself — private cohorts are common — but it means the claim of "practical and empirically grounded" rests on a single internal validation with no independent replication. The authors acknowledge this: "broader external benchmarking" is listed as future work. The current evidence supports "LATTICE works on our cohort" but not "LATTICE is a practical framework for the field." Narrow the claim to match the evidence, or deposit the cohort and code with sufficient detail that an external group could reproduce and extend the results.

## Sweep

1. The theoretical analysis in Appendix I (Lemmas I.1–I.4 and Theorem I.4) states standard results from spectral graph theory and contrastive learning without proving that the specific combination of three losses yields the claimed properties; the proof sketch for Theorem I.4 is circular (it asserts that minimizing all three terms yields all three properties, which is true by definition but does not establish that the optimum is unique or that the trade-offs are resolved).

2. The modality ladder is presented as a progression (M1→M2→M3→M4→M5) but the results show M2 and M3 are nearly identical (ARI 0.426 vs 0.417, NMI 0.507 vs 0.493), suggesting scMultiome ATAC gene scores add little; this is not discussed.

3. ReCAST and SARSIM are described as "internal engineering pipeline" and "framework" respectively, but their outputs are treated as ground truth for feature construction and evaluation; the sensitivity of LATTICE results to errors or choices in those upstream steps is not explored.

4. The claim that "chromatin and regulatory structure beyond transcriptomic similarity alone" explains the ARI/NMI drop at M4–M5 is plausible but untested; an orthogonal validation (e.g., differential chromatin accessibility in known regulatory regions, or enrichment of TF motifs in high-activity spots) would strengthen it.

5. Spatial contiguity is measured on the same k-NN graph used to train the model, which may inflate the metric; report contiguity on a held-out spatial graph (e.g., 8-nearest neighbors instead of 6) to check independence.

6. The paper states "LATTICE is modular with respect to multimodal feature construction" but all experiments use the same five-block stack; modularity is claimed but not demonstrated.

7. Early stopping spans 36–63 epochs (mean 45.2) across runs, but no learning curves or convergence diagnostics are shown; it is unclear whether the model is stable or whether early stopping is masking optimization instability.

8. The authors note that "adding scMultiome RNA to Visium RNA alone substantially improved concordance" but do not report whether this improvement is statistically significant or whether the standard deviations (Table 2) overlap; confidence intervals or a significance test would clarify.

## Questions

- Can you report MUS with spatial regularization removed (λ₃=0) to isolate the contribution of multimodal objectives from spatial smoothness?
- How does LATTICE M2 compare to GraphST and STAGATE trained on the same M2 input (Visium + scMultiome RNA)?
- What is the biological interpretation of the spots where M5 embeddings diverge most from M2? Do they correspond to known regulatory or chromatin domains?