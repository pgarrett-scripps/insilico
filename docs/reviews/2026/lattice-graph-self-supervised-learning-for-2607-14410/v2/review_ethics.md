# Ethics & Compliance Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

LATTICE presents a graph-based self-supervised learning framework for multimodal spatial omics integration. The work is technically sound, addresses a genuine gap in multimodal spatial analysis, and demonstrates stable performance across an 11-sample melanoma cohort. The authors are transparent about data limitations, upstream dependencies, and the trade-offs between RNA-reference agreement and multimodal utility. The main compliance concern is that human biospecimen data governance is stated but incompletely documented for reproducibility purposes.

## Strengths

1. The authors explicitly acknowledge that ARI/NMI improvements plateau or reverse with additional modalities, and they introduce MUS as a complementary metric rather than claiming monotonic gains—this is honest reporting of a genuine tension in multimodal integration.

2. Appendix G provides detailed disclosure of data agreements, IRB governance, compute resources, and reproducibility artifacts (seeds, logs, checkpoints), which is exemplary for a private-data study.

3. The modality ladder (M1–M5) design isolates the contribution of each data source and makes the incremental gains transparent; the ablation study (Table 3) separates training choices from input composition.

## Weaknesses: Load-bearing Claims

**Claim 1: LATTICE learns multimodal representations that improve spatial coherence and multimodal utility.**

The evidence is Table 2, which shows MUS increases from M1 (0.111) to M5 (0.803), and spatial contiguity rises from 0.653 to 0.850. However, this improvement is not uniform across the modality ladder. The largest jump is M1→M2 (+0.622 MUS), driven by adding projected scMultiome RNA. M4 and M5 (the ReCAST-derived chromatin blocks) add only +0.070 MUS over M3, and their inclusion *decreases* ARI and NMI (M3: ARI 0.417, M5: ARI 0.329). The authors interpret this as the embeddings capturing "chromatin and regulatory structure beyond transcriptomic similarity alone" (main text, Section 4.2). This is plausible, but an alternative explanation is that spatial ATAC and CUT&Tag introduce noise or sample-specific artifacts that degrade the learned representation without providing compensating signal. The ablation in Table 3 shows that withholding these modalities at test time does not uniformly improve metrics ("metric changes are not uniformly better"). To distinguish whether M4–M5 genuinely capture complementary biology or introduce confounding signal, the authors would need to show that embeddings trained on M4–M5 alone (without M1–M3) recover known biological structure, or that downstream tasks (e.g., predicting treatment response, identifying cell types) benefit from M4–M5 in a held-out validation set. The current evidence does not exclude the noise hypothesis.

**Claim 2: LATTICE is a practical framework for multimodal spatial omics integration.**

The framework depends on two upstream pipelines: SARSIM (for spatially anchored regulatory projection) and ReCAST (for harmonization and quality control). SARSIM is cited as a preprint (ref. 4, "bioRxiv, 2026"—a future date, likely a placeholder). ReCAST is described as "an internal engineering pipeline" with no public code, no peer review, and no external validation. Section F states that ReCAST "is an internal engineering pipeline and is included here for reproducibility of this submission's data flow" but also that "we do not present ReCAST as a scientific baseline or claim methodological novelty for it here." This creates a reproducibility gap: the five-modality tensors that LATTICE consumes are not independently reproducible without access to ReCAST, and ReCAST's harmonization choices (gene intersection, feature scaling, QC thresholds) are not validated against alternatives. The authors note that "LATTICE is modular with respect to multimodal feature construction" (Section 3.4), but they do not demonstrate this modularity by applying LATTICE to tensors constructed by a different upstream pipeline. Without that, the claim of practical utility rests on a single, non-public, non-validated preprocessing stack. To resolve this, the authors could either (i) release ReCAST code and validation, (ii) apply LATTICE to multimodal tensors from a published alternative (e.g., a different harmonization or projection method), or (iii) scale back the claim to "LATTICE is compatible with multimodal inputs" rather than "LATTICE is a practical framework."

**Claim 3: The modality ladder demonstrates robust gains from multimodal integration.**

Table 2 reports mean and standard deviation across 11 samples for each modality level. However, the per-sample results are not shown, and it is unclear whether the gains are consistent across samples or driven by a few outliers. For instance, Table 1 shows that sample 2-post has only 746 multiome cells and 150 final intersected genes, while sample 4-post has 15,577 cells and 322 genes. If M2–M5 gains are driven by well-resourced samples and absent in sparse samples, the practical utility is limited. The authors report "11 successful cohort runs" after quality control, but do not disclose how many samples were excluded or why, or whether the excluded samples had characteristics (e.g., low multiome depth) that would predict poor LATTICE performance. To address this, the authors should report per-sample ARI, NMI, and MUS for all 11 retained samples, and analyze whether gains correlate with sample-level covariates (multiome cell count, gene intersection size, spatial ATAC signal).

## Weaknesses: Sweep

1. **Data governance incomplete for reproducibility:** Appendix G.3 states that "identifying protocol numbers and committee names are withheld" for double-blind review and "can be restored in the camera-ready version," but the current manuscript does not provide the IRB protocol number, committee name, or institution name, making it impossible for readers to verify compliance or contact the IRB for details.

2. **Baseline comparisons limited to single-modality or weakly multimodal methods:** Table 2 compares LATTICE M1 against GraphST, STAGATE, SpaGCN, SIMO, and MaxFuse, but none of these baselines are designed for the full five-modality input that LATTICE uses; LATTICE M1 underperforms because the architecture is "designed for multimodal representation learning rather than optimization for transcriptomic clustering alone" (main text, Section 4.2), making the M1 comparison unfair and the M2–M5 comparisons against single-modality baselines uninformative about whether LATTICE's gains come from the method or from the additional input data.

3. **Cross-patient generalization not demonstrated:** Section 4.3 reports that "leave-one-patient-out prediction is mixed" and treatment-associated shifts are "patient specific," but does not quantify LOPO performance or show whether embeddings from one patient can be used to predict structure in another; this limits claims about the framework's generalizability.

4. **Theoretical analysis (Appendix I) does not address the multimodal case:** Lemmas I.1–I.3 analyze spatial smoothness, reconstruction, and alignment separately, but Theorem I.4 simply states that the joint objective "balances" all three properties without proving that the balance is stable, unique, or optimal; the proof sketch does not address whether the three losses can conflict (e.g., spatial smoothness vs. cross-modal alignment) or how hyperparameter weights affect the trade-off.

5. **Masking ratio and reconstruction target not justified:** The masked reconstruction uses ρ=0.15 (15% of features masked), but no ablation or justification is provided; standard masked autoencoder work (e.g., MAE) uses 75% masking, and the choice of 15% is not explained.

6. **Spatial graph construction uses k=6 without sensitivity analysis:** The kNN graph uses k=6 neighbors, but no ablation or justification is provided; Visium spots have ~6 neighbors in a hexagonal grid, so k=6 may be redundant with the spatial structure already present in the coordinates.

7. **Leiden clustering resolution not pre-specified:** Section 4.1 states that "target cluster count K imported from SARSIM clustering metadata and achieved via a resolution sweep," but does not disclose the resolution range or how ties are broken; this introduces a degree of freedom that could inflate agreement with Space Ranger clusters if the sweep is data-dependent.

8. **MUS definition mixes spatial and embedding metrics without justification:** Equation 11 averages four normalized quantities (spatial contiguity, silhouette, same-cluster spatial-neighbor fraction, Jaccard overlap), but does not justify equal weighting or explain why these four metrics are the right ones to combine; silhouette and Jaccard overlap are both based on embedding geometry, so they are not independent.

## Questions

1. Can the authors provide per-sample results (Table 2 broken down by sample) to show whether M2–M5 gains are consistent across the cohort or concentrated in well-resourced samples?

2. What is the rationale for masking ratio ρ=0.15, and does performance change if ρ is increased to 0.5 or 0.75 as in standard masked autoencoders?

3. Can the authors apply LATTICE to multimodal tensors constructed by a different upstream pipeline (not ReCAST/SARSIM) to demonstrate modularity, or provide ReCAST code and validation?

4. For the three paired pre/post-treatment samples, what is the LOPO prediction accuracy (can embeddings from patient A predict structure in patient B), and does this improve with additional modalities?

5. What is the range of Leiden resolutions swept in Section 4.1, and how sensitive are the reported metrics to this choice?

---

## Ethics & Compliance Assessment

**Human subjects and data governance:** The manuscript involves human biospecimen-derived profiles from a clinical collaborator under a data transfer agreement. Appendix G.3 states that "ethics and IRB oversight for human biospecimens are handled by the collaborating clinical institution" and that "a data transfer agreement is in place," but does not name the IRB, protocol number, or institution. For a preprint under double-blind review, this is understandable, but the authors state that identifiers "can be restored in the camera-ready version." This is acceptable if the camera-ready version will include them; however, the current submission does not provide enough information for readers to verify compliance independently. **SOFT:** Request that the camera-ready version include the IRB protocol number, committee name, and institution name (or a statement that they are available upon request from the corresponding author).

**Funding and competing interests:** The manuscript does not include a funding statement or competing interests declaration. Appendix G.2 mentions "cluster" resources and "Slurm" scheduling, suggesting institutional compute access, but does not disclose funding sources or whether any authors have financial interests in spatial omics platforms or software. **HARD:** Add a funding statement and competing interests declaration (or explicit statement that no competing interests exist).

**Data availability:** The authors state that "the cohort tensors are de-identified clinical biospecimen-derived profiles under a collaborator institution's proprietary agreement, cannot be redistributed publicly, and have no public five-modality substitute at this lattice resolution" (Appendix G.1). This is a legitimate restriction, but it means the central evidence (the 11-sample cohort) cannot be independently verified. The authors provide "anonymized code, Slurm driver scripts, pinned dependency manifests, and run snapshots as supplementary material," which is commendable, but the inability to release data limits reproducibility. This is not a compliance failure (the restriction is legitimate), but it is a limitation that should be stated clearly in the main text, not buried in the appendix.

**No clinical trial, diagnostic guidance, or patient safety claims.** The work is out of scope for clinical-safety review.

---

## Overall Assessment

LATTICE addresses a real problem—multimodal spatial omics integration—and proposes a reasonable solution with honest reporting of trade-offs. The work is technically sound and the authors are transparent about limitations. However, the central claims rest on three pillars that each have gaps: (1) the evidence that M4–M5 improve representation rather than add noise is indirect; (2) the framework's practical utility depends on non-public, non-validated upstream pipelines; and (3) the gains are reported at cohort level without per-sample breakdown, leaving unclear whether they generalize across sample types. The ethics and compliance posture is strong (detailed disclosure, data governance, reproducibility artifacts) but incomplete (missing IRB identifiers for independent verification, no funding statement). For a venue like In Silico, which emphasizes inspectability and honest reporting, this is a borderline accept: the work is sound and the authors are candid about what they do and do not know, but the evidence for the main claims could be stronger, and the dependence on non-public preprocessing limits reproducibility.