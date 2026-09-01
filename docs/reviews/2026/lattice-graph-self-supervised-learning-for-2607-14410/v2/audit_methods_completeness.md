# Methods Completeness & Reagent Traceability Audit
## LATTICE: Graph Self-Supervised Learning for Multimodal Spatial Omics Integration

---

## CROSS-CUTTING ITEMS

### Sample Size and Replication

**Status: PRESENT (with caveats)**

- **n stated**: 11 samples retained after QC (from 14 source samples); 54,912 total Visium spots; 4,992 spots per sample. Three patients with paired pre/post-treatment samples.
- **What n represents**: Biological replicates (tissue samples from different patients/timepoints). No technical replicates explicitly stated.
- **Severity**: HARD
- **Finding**: Sample size is stated clearly. However, the manuscript does not explicitly state whether any technical replicates (e.g., repeated LATTICE runs on the same sample with different random seeds) were performed during primary analysis. Section 4.3 mentions "11 analysis seeds {7, 11, 19, 23, 29, 31, 37, 41, 43, 47, 53}" for joint multisample analysis, but it is unclear whether these represent independent training runs on the same data or post-hoc seed variations for stability assessment. The ablation study (Table 3) reports standard deviations across runs, suggesting multiple runs occurred, but the primary modality-ladder results (Table 2) report means ± SD without explicitly stating how many independent runs were averaged.

**Question for authors**: Were the Table 2 results (ARI, NMI, etc.) computed as means over multiple independent LATTICE training runs per sample, or single runs? If multiple, how many?

---

### Statistical Tests and Error Representation

**Status: PRESENT (with limitations)**

- **Error bars**: Tables 2 and 3 report ± SD (standard deviation).
- **Named statistical tests**: None explicitly named. No hypothesis tests (t-tests, ANOVA, etc.) are reported. Comparisons are descriptive (e.g., "ARI increased from M1 to M2").
- **Severity**: SOFT
- **Finding**: Error bars are defined as SD, which is appropriate for reporting variability. However, no formal statistical significance testing is performed between modality levels or methods. For a methods paper with a private cohort, this is acceptable if framed as exploratory, but the manuscript does not explicitly state whether differences (e.g., M1 vs M2 in Table 2) are statistically significant or merely descriptive.

---

### Software, Tool, and Instrument Versions

**Status: PARTIALLY PRESENT**

| Component | Version | Status |
|-----------|---------|--------|
| PyTorch | Not specified | **MISSING** |
| PyTorch Geometric | Not specified | **MISSING** |
| Scanpy | "Scanpy-style tooling" (vague) | **MISSING** |
| Space Ranger | Not specified | **MISSING** |
| Leiden clustering | Cited [19] | **PRESENT (by reference)** |
| UMAP | Cited [20] | **PRESENT (by reference)** |
| Python | Not specified | **MISSING** |
| AdamW optimizer | Cited [13] | **PRESENT (by reference)** |

**Severity**: HARD

**Finding**: Appendix H states "We additionally rely on Scanpy-style tooling" and "PyTorch [[10](#ref-10)] and PyTorch Geometric [[11](#ref-11)]" but provides no version numbers. The supplementary materials are mentioned to include "pinned dependency files (environment.yml and/or requirements.txt)" but these files are not visible in the manuscript itself. For reproducibility, exact versions of PyTorch, PyTorch Geometric, and Scanpy are essential.

**Question for authors**: Are the environment.yml and requirements.txt files included in the supplementary materials? If so, please confirm they are present. If not, they must be provided.

---

### Data Availability Statement

**Status: PRESENT (with restrictions)**

**Severity**: HARD

**Finding**: Section G.1 explicitly states:
> "The cohort tensors are de-identified clinical biospecimen-derived profiles under a collaborator institution's proprietary agreement, cannot be redistributed publicly, and have no public five-modality substitute at this lattice resolution."

This is a clear, honest statement of unavailability due to privacy/proprietary constraints. The manuscript also notes that "anonymized code, Slurm driver scripts, pinned dependency manifests, and run snapshots" are included as supplementary material. This is appropriate for a clinical dataset under data-use agreements.

**Status of availability statement**: PRESENT and justified.

---

### Code Availability

**Status: PRESENT (with caveats)**

**Severity**: HARD

**Finding**: Appendix G.1 states that "anonymized code, Slurm driver scripts, pinned dependency manifests, and run snapshots" are provided as supplementary material. However:
1. The manuscript does not provide a GitHub URL, Zenodo DOI, or other persistent identifier for the code.
2. It is unclear whether the code is anonymized in a way that preserves reproducibility (e.g., are institution names removed but paths/URLs still functional?).
3. The ReCAST pipeline is described as "an internal engineering pipeline" (Appendix F) and is not stated to be publicly released.

**Question for authors**: 
- Will the LATTICE code be released on GitHub or Zenodo with a DOI? 
- Is ReCAST code included in the supplementary materials, or is it proprietary?
- Are the Slurm scripts and manifests sufficient for a user without access to the same HPC cluster to adapt the pipeline?

---

## CONDITIONAL CATEGORIES

### Human Subjects / Clinical Data

**Trigger**: Yes. The manuscript uses "a private 11-sample melanoma cohort from an anonymized clinical collaborator" and "human biospecimens."

**Checklist Items**:

| Item | Status | Finding |
|------|--------|---------|
| IRB approval | **PRESENT** | Appendix G.3: "Ethics and IRB oversight for human biospecimens are handled by the collaborating clinical institution. A data transfer agreement is in place." |
| Informed consent | **UNVERIFIABLE** | Not explicitly stated in the manuscript. Appendix G.3 says "identifying protocol numbers and committee names are withheld" for double-blind review. |
| Inclusion/exclusion criteria | **MISSING** | No criteria stated for sample selection beyond "melanoma cohort" and QC filters. |
| Participant demographics | **PARTIALLY PRESENT** | Table 1 shows sample IDs (anonymized) and pre/post-treatment status. No age, sex, stage, treatment type, or other clinical metadata provided. |
| Trial registration # | **N/A** | Not an interventional trial. |
| Reporting-guideline adherence | **MISSING** | No mention of STROBE, CONSORT, or other guidelines. |
| Power calculation | **MISSING** | No justification for n=11 samples. |
| COI/funding disclosure | **MISSING** | No funding sources or conflicts of interest stated. |

**Severity**: HARD (for IRB/consent/criteria); SOFT (for demographics/power/COI)

**Findings**:
1. IRB approval is confirmed to exist but details are withheld for anonymity. This is acceptable for double-blind review if restored in camera-ready version.
2. Informed consent is not explicitly mentioned. The manuscript should state whether informed consent was obtained.
3. **Inclusion/exclusion criteria are not stated.** Were all melanoma samples in the cohort eligible, or were there clinical/pathological filters?
4. **Participant demographics are minimal.** No age, sex, stage, treatment regimen, or outcome data are provided. This limits interpretation of whether results generalize.
5. **No power calculation is provided** for the choice of n=11.

**Questions for authors**:
- Was informed consent obtained from all participants?
- What were the inclusion/exclusion criteria for the melanoma cohort?
- Can demographic data (age, sex, stage, treatment type) be provided in a de-identified table?
- Was sample size justified a priori, or is n=11 the result of QC filtering?

---

### Genomics / Sequencing / Omics

**Trigger**: Yes. The manuscript uses five modality blocks: Visium RNA, scMultiome RNA, scMultiome ATAC, spatial ATAC, and spatial CUT&Tag.

**Checklist Items**:

| Item | Modality | Status | Finding |
|------|----------|--------|---------|
| **Platform + mode** | Visium RNA | **PRESENT** | "Visium" (10x Genomics). Read length, single/paired not specified. |
| | scMultiome | **PRESENT** | "scMultiome" (10x Genomics). Details delegated to SARSIM [4]. |
| | Spatial ATAC | **UNVERIFIABLE** | "Spatial ATAC" mentioned but platform not named. Appendix F mentions "CGMC prediction" but CGMC is not defined. |
| | Spatial CUT&Tag | **PRESENT** | "spatial CUT&Tag" [2]. Platform/instrument not specified. |
| **Library-prep kit** | All | **DELEGATED** | Visium and scMultiome are 10x kits (standard). Spatial ATAC and CUT&Tag kits not specified. |
| **Depth/coverage** | All | **MISSING** | No read depth, coverage, or sequencing statistics provided. |
| **Reference genome + build** | All | **MISSING** | No reference genome version stated (e.g., hg38, hg19, mm10). |
| **Alignment/analysis tools + versions** | All | **DELEGATED/MISSING** | Space Ranger mentioned for RNA clustering but version not given. SARSIM [4] used for projection but is a preprint (unverifiable). ReCAST is internal (not published). |
| **Repository accession** | All | **MISSING** | No GEO, SRA, ENA, or other public accession provided (acknowledged: data under proprietary agreement). |
| **QC thresholds** | All | **PARTIALLY PRESENT** | Appendix A.1 mentions "HVG filtering is configured but disabled (apply_hvg_filter=false)" but no other QC thresholds (e.g., min genes/spot, max UMI, mitochondrial %) stated. |
| **Batch handling** | All | **MISSING** | No batch-correction method mentioned. Samples are from different patients; no batch-effect assessment reported. |

**Severity**: HARD (for platform, reference genome, alignment tools, depth); SOFT (for QC thresholds, batch handling)

**Findings**:

1. **Spatial ATAC platform is undefined.** The manuscript refers to "spatial ATAC" and "ReCAST CGMC" but does not name the platform (e.g., Visium ATAC, 10x Genomics Visium for ATAC, or another platform). "CGMC" is not defined in the manuscript.

   **Question for authors**: What is the spatial ATAC platform? What does "CGMC" stand for and what is the method?

2. **Reference genome version is not stated.** For reproducibility of alignment and downstream analysis, the reference genome build (hg38, hg19, etc.) must be specified.

   **Question for authors**: What reference genome and build were used for alignment?

3. **Sequencing depth is not provided.** No information on read counts, coverage, or sequencing statistics per sample or modality.

   **Question for authors**: Can you provide mean read depth or UMI counts per spot for each modality?

4. **Alignment tools and versions are missing or delegated.** Space Ranger is mentioned but not versioned. SARSIM [4] is a preprint (bioRxiv, "2026" — a future date, likely a placeholder). ReCAST is internal and not published.

   **Question for authors**: 
   - What version of Space Ranger was used?
   - Is SARSIM [4] a published paper or a preprint? If preprint, provide the correct bioRxiv date.
   - Can ReCAST be described in sufficient detail in the main text or appendix, or will it be released?

5. **QC thresholds are sparse.** Appendix A.1 mentions HVG filtering is disabled, but no other QC filters (min genes, max UMI, mitochondrial content, etc.) are stated.

   **Question for authors**: What QC filters were applied to each modality? (e.g., min genes/spot, max UMI, mitochondrial % threshold)

6. **Batch handling is not discussed.** The cohort spans 11 samples from different patients and timepoints. No batch-correction method is mentioned.

   **Question for authors**: Were batch effects assessed or corrected? If not, why not?

---

### Computational / ML / Modeling

**Trigger**: Yes. LATTICE is a graph neural network trained with self-supervised objectives.

**Checklist Items**:

| Item | Status | Finding |
|------|--------|---------|
| **Dataset(s) with version + exact train/val/test split** | **PARTIALLY PRESENT** | 11 samples, 54,912 spots total. Train/val split: "validation fraction is set to 0.1, with train/validation masks generated at the node level" (Appendix H). No test set mentioned; evaluation is on the same samples used for training. |
| **Architecture** | **PRESENT** | TransformerConv with 3 layers, 4 attention heads, hidden dim 128, embedding dim 128 (Appendix H). |
| **Hyperparameters** | **PRESENT** | Loss weights (λ₁=1.0, λ₂=0.5, λ₃=0.1), learning rate (1×10⁻³), weight decay (1×10⁻⁴), masking ratio (ρ=0.15), temperature (τ=0.1), k=6 for kNN graph, early stopping patience=20 (Appendix H). |
| **Training procedure** | **PRESENT** | AdamW optimizer, full-graph optimization, up to 100 epochs with early stopping, gradient clipping norm 1.0 (Appendix H). |
| **Library versions + hardware** | **PARTIALLY PRESENT** | PyTorch and PyTorch Geometric cited but not versioned. Hardware: CPU-only (device=cpu), 16 cores, 128 GB RAM per node (Appendix G.2). |
| **Random seeds** | **PRESENT** | Global seed=42 for single-sample runs; 11 analysis seeds {7, 11, 19, 23, 29, 31, 37, 41, 43, 47, 53} for multisample analysis (Appendix H). |
| **Code availability** | **PRESENT (with caveats)** | "Anonymized code, Slurm driver scripts, pinned dependency manifests, and run snapshots" in supplementary materials (Appendix G.1). No GitHub/Zenodo URL provided. |
| **Compute budget** | **PRESENT** | ~8 minutes wall clock per sample, 36–63 epochs (mean 45.2) (Appendix G.2). |
| **Ablations** | **PRESENT** | Table 3 removes spatial regularization, masking, and test-time modality dropout. |
| **Metric definitions** | **PRESENT** | ARI, NMI, spatial contiguity, silhouette, MUS (Eq. 11, Appendix A.2). |
| **Environment file** | **UNVERIFIABLE** | Appendix H states "pinned dependency files (environment.yml and/or requirements.txt)" but these are not shown in the manuscript. |

**Severity**: HARD (for library versions, environment file); SOFT (for compute budget, ablations)

**Findings**:

1. **Library versions are missing.** PyTorch and PyTorch Geometric are cited [10, 11] but no version numbers are given. This is critical for reproducibility.

   **Question for authors**: What versions of PyTorch and PyTorch Geometric were used? (e.g., torch==2.0.0, torch_geometric==2.3.0)

2. **Environment file is not shown.** Appendix H references "environment.yml and/or requirements.txt" but these files are not included in the manuscript text. They must be provided in supplementary materials or a public repository.

   **Question for authors**: Are environment.yml and requirements.txt included in the supplementary materials? If so, please confirm. If not, they must be added.

3. **Train/val/test split is unclear.** A 0.1 validation fraction is used, but no explicit test set is mentioned. Evaluation metrics (ARI, NMI, etc.) are computed on the same samples used for training, which raises concerns about overfitting assessment.

   **Question for authors**: Were any samples held out as a test set, or is all evaluation on training data? If the latter, how is generalization assessed?

4. **Modality-specific preprocessing is partially specified.** Appendix A.1 states "per-modality log1p_then_zscore before concatenation" but does not specify whether this is applied before or after masking, or whether modality-specific normalization constants are computed per sample or globally.

   **Question for authors**: Are log1p and zscore computed per sample and per modality, or globally across the cohort?

5. **Masked reconstruction details are sparse.** The masking ratio is ρ=0.15, but it is not stated whether masking is applied uniformly across all modalities or whether some modalities are masked more frequently than others.

   **Question for authors**: Is the 15% masking ratio applied uniformly to all modality blocks, or are there modality-specific masking rates?

6. **Cross-modal alignment modality pairs are hardcoded.** Equation 8 and Appendix H state that "modality indices zero and one correspond to Visium RNA and spatial ATAC." This is a specific choice that may not generalize to other modality combinations.

   **Question for authors**: Why were Visium RNA and spatial ATAC chosen for the alignment loss? Were other modality pairs tested?

7. **Decoder architecture is simple.** A single hidden layer (width 2d) is used. No justification is provided for this choice.

   **Question for authors**: Was the decoder architecture tuned, or is this a default choice? How sensitive are results to decoder depth/width?

---

### Upstream Pipelines (SARSIM and ReCAST)

**Trigger**: Yes. LATTICE depends on outputs from SARSIM [4] and ReCAST (internal).

**Checklist Items**:

| Pipeline | Status | Finding |
|----------|--------|---------|
| **SARSIM [4]** | **DELEGATED-UNVERIFIABLE** | Cited as a preprint with date "2026" (likely a placeholder). The manuscript states SARSIM "learns a soft cell-to-spot mapping, and projects accessibility and motif activity into tissue space" but does not provide enough detail to reproduce this step independently. |
| **ReCAST** | **DELEGATED-DEAD** | Described as "an internal engineering pipeline" (Appendix F). No publication, code repository, or sufficient methodological detail provided. The manuscript states ReCAST "performs three functions" (standardization, harmonization, QC) but does not specify algorithms, parameters, or validation. |

**Severity**: HARD (for load-bearing methods)

**Findings**:

1. **SARSIM is a preprint with an invalid date.** Reference [4] is listed as "bioRxiv, 2026" — a future date that suggests a placeholder. The manuscript should provide the correct bioRxiv date or indicate that SARSIM is under review/in preparation.

   **Question for authors**: What is the correct bioRxiv date for SARSIM [4]? Is it published or still in review?

2. **ReCAST is not published or released.** Appendix F describes ReCAST as "an internal engineering pipeline" and states it is "not presented as a scientific baseline or claim methodological novelty for it here." However, ReCAST is responsible for:
   - Harmonizing spatial ATAC and spatial CUT&Tag blocks (M4 and M5 inputs).
   - Applying sample-level quality control that filtered 14 samples down to 11.
   - Defining the "strict five-way gene intersection" used for all downstream analysis.

   These are load-bearing steps. Without ReCAST code or detailed methodology, the work cannot be reproduced.

   **Question for authors**: 
   - Will ReCAST be released as code or a detailed methods paper?
   - Can the harmonization and QC procedures be described in sufficient detail in the main text or appendix?
   - What were the QC criteria that filtered 3 samples out of 14?

3. **SARSIM overlap_genes.txt is referenced but not provided.** Appendix H states "Harmonization uses a strict five-way gene intersection anchored on SARSIM overlap_genes.txt" but this file is not provided or described.

   **Question for authors**: Can the overlap_genes.txt file be provided in supplementary materials, or can the gene intersection procedure be described algorithmically?

---

## SUMMARY TABLE

| Category | Trigger | Items Checked | HARD Missing | SOFT Missing | Unverifiable |
|----------|---------|---------------|--------------|--------------|--------------|
| Cross-cutting | Yes | 4 | 1 (PyTorch/PG versions) | 0 | 1 (environment file location) |
| Human subjects | Yes | 8 | 2 (consent, inclusion/exclusion) | 3 (demographics, power, COI) | 1 (IRB details) |
| Genomics/omics | Yes | 10 | 4 (spatial ATAC platform, ref genome, depth, alignment versions) | 2 (QC thresholds, batch handling) | 1 (SARSIM date) |
| Computational/ML | Yes | 10 | 1 (environment file) | 0 | 0 |
| Upstream pipelines | Yes | 2 | 1 (ReCAST methodology) | 0 | 1 (SARSIM date) |
| **TOTALS** | | **34** | **9** | **5** | **3** |

---

## CRITICAL BLOCKERS FOR REPRODUCIBILITY

1. **PyTorch and PyTorch Geometric versions are not specified.** These are essential dependencies. Provide exact version numbers.

2. **Spatial ATAC platform is not named.** The manuscript refers to "spatial ATAC" and "ReCAST CGMC" without defining the platform or method. This is a core input modality.

3. **Reference genome build is not stated.** Reproducibility of alignment and downstream analysis requires knowing whether hg38, hg19, or another build was used.

4. **ReCAST is not published or released.** This internal pipeline is responsible for harmonizing M4–M5 inputs and filtering samples. Without code or detailed methodology, these steps cannot be reproduced.

5. **SARSIM reference has an invalid date.** Reference [4] lists "2026" as the publication year, which is a placeholder. The correct date must be provided.

6. **Environment file is not shown in the manuscript.** Appendix H references environment.yml and requirements.txt but these are not visible. They must be provided in supplementary materials or a public repository.

7. **Informed consent and inclusion/exclusion criteria are not stated.** For human subjects research, these are required.

---

## QUESTIONS FOR AUTHORS

### Immediate (HARD blockers):

1. What are the exact versions of PyTorch and PyTorch Geometric used?
2. What is the spatial ATAC platform? What does "CGMC" stand for?
3. What reference genome and build were used for alignment?
4. What is the correct bioRxiv date for SARSIM [4]?
5. Will ReCAST be released as code or described in sufficient methodological detail?
6. Are environment.yml and requirements.txt included in supplementary materials?
7. Were informed consent and inclusion/exclusion criteria documented?

### Secondary (SOFT/clarification):

8. Were Table 2 results computed as means over multiple independent LATTICE training runs per sample?
9. What QC filters were applied to each modality (min genes, max UMI, mitochondrial %)?
10. Were batch effects assessed or corrected across the 11 samples?
11. Why were Visium RNA and spatial ATAC chosen for the cross-modal alignment loss?
12. Can demographic data (age, sex, stage, treatment) be provided in a de-identified table?
13. What were the QC criteria that filtered 3 samples out of 14?
14. Is the decoder architecture (single hidden layer, width 2d) a default choice or tuned?

---

**Report prepared by**: Methods Completeness & Reagent Traceability Auditor  
**Date**: [Current date]  
**Verdict**: **9 HARD missing items block independent reproduction. 5 SOFT items recommended for completeness. 3 items unverifiable without author clarification.**