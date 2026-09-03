# Methods Completeness & Reagent Traceability Audit

**Manuscript:** "A Pilot Evaluation of Open-Weight Large Language Models for Screening RNA-seq Metadata in Public Databases"

---

## Triggered Categories & Findings

### 1. **Computational/ML/Modeling** ← PRIMARY TRIGGER
The manuscript centers on LLM-based classification tasks, model benchmarking, and inference reproducibility.

#### Dataset(s) with version + exact train/val/test split
- **Status: MISSING (HARD)**
- The benchmark dataset comprises 150 RNA-seq projects (63 positive, 87 negative labels).
- **Present:** Project count, label distribution, retrieval method (keyword search on GEO/BioProject, executed 7 Dec 2025).
- **Missing:** No explicit train/validation/test split is stated. All 150 projects appear to be used as a single evaluation set against which all models are scored. No cross-validation, hold-out test set, or temporal split is described. For reproducibility, the exact composition of the 150-project benchmark must be fixed and reproducible.
- **Mitigation:** Supplementary Table 8 lists the 150 projects by accession; this allows external verification of the dataset itself, but the *split strategy* remains undocumented.

#### Architecture/algorithm
- **Status: PRESENT (HARD)**
- Models are named and sourced (Table 4, Supplementary File 6). Model cards and technical reports are cited (refs 17–18 for gpt-oss and Qwen3).
- No custom architecture is introduced; the work benchmarks existing LLMs.

#### Hyperparameters
- **Status: PRESENT (HARD)**
- Temperature = 0, max_tokens = 60,000 stated (line 746).
- For open-weight models: reasoning effort (High/Low) for gpt-oss variants is specified (Table 4, line 746).
- For closed models (API): no inference-time hyperparameters are disclosed (expected, as they are provider-managed).

#### Training procedure (optimizer/schedule/early-stopping)
- **Status: NOT APPLICABLE**
- No model training is performed. The work evaluates pre-trained, fixed models. This is correctly implicit in the design.

#### Library versions + hardware
- **Status: PRESENT (HARD)**
- **Hardware:** Mac Studio (2025) with Apple M4 Max, 16-core CPU, 40-core GPU, 128 GB RAM, 2 TB SSD (line 769).
- **Software versions:**
  - LM Studio v0.3.33 (line 767).
  - Internal tools: Metal llama.cpp v1.61.0, LM Studio MLX v0.34.0, Harmony (Mac) v0.3.5 (lines 768–769).
  - Model versions: all models are named with release dates (Table 4, e.g., "gpt-oss-120b" released 2025-08-05).
- **Closed models:** accessed via OpenAI and Google APIs (dates: 14–15 Dec 2025, line 745).

#### Random seeds (or seed-averaging statement)
- **Status: PARTIALLY PRESENT (HARD)**
- **Main benchmark (Table 1):** No random seed is stated. Temperature = 0 should suppress sampling randomness, but inference-time non-determinism is acknowledged (lines 495–497, 601–603).
- **Reproducibility subset (n=50):** Fixed sampling seed = 42 for project selection (line 754). Five independent repeated runs performed on the same 50 projects (lines 751–763). Results show binary labels and probabilities were identical across runs for qwen3-next-80b-a3b-thinking; openai/gpt-oss-120b_low showed minor cross-session drift in self-reported probabilities (5 of 50 projects, within high-confidence range, Supplementary Table 4, lines 333–340).
- **Assessment:** The reproducibility experiment is well-designed and honestly reported. However, the main 150-project benchmark lacks an explicit statement of whether outputs were deterministic or whether a single run was performed. The authors acknowledge that "outputs may be affected by inference-time randomness, software implementation, inference backend, hardware-dependent numerical differences, and session-specific execution conditions" (lines 495–497), which is candid but leaves the main results' reproducibility status ambiguous.

#### Code availability
- **Status: PRESENT (HARD)**
- GitHub repository provided: https://github.com/mshintani22/open-weight-llm-metadata-curation-workflow (lines 681, 869).
- MIT license stated (line 870).
- Supplementary Files 1, 3, 5, 6 contain scripts and outputs (lines 849–868).

---

### 2. **Genomics/Sequencing/Omics** ← SECONDARY TRIGGER
The manuscript retrieves and analyzes RNA-seq project metadata from public databases.

#### Platform + mode (read length, single/paired)
- **Status: NOT APPLICABLE (SOFT)**
- The work does not perform sequencing itself. It retrieves and classifies *metadata* from existing RNA-seq projects. Read-length and pairing information are part of the retrieved metadata but are not standardized across the 150 projects and are not a focus of the analysis.

#### Library-prep kit
- **Status: NOT APPLICABLE (SOFT)**
- Not performed by the authors.

#### Depth/coverage
- **Status: NOT APPLICABLE (SOFT)**
- Not performed by the authors.

#### Reference genome WITH build
- **Status: NOT APPLICABLE (SOFT)**
- Not performed by the authors. The benchmark task is to classify projects as containing ABA-treated Arabidopsis samples with controls; genome alignment is not part of the workflow.

#### Alignment/analysis tools WITH versions and key params
- **Status: NOT APPLICABLE (SOFT)**
- Not performed by the authors.

#### Repository accession (GEO/SRA/ENA)
- **Status: PRESENT (HARD)**
- The 150 benchmark projects are identified by BioProject accessions (Supplementary Table 8).
- Metadata retrieval used NCBI Entrez E-utilities, European Nucleotide Archive (ENA) read_run API, and TogoID API (lines 711–731).
- Search was executed 7 Dec 2025 on GEO and BioProject (line 729).
- The retrieved metadata are provided in Supplementary File 4 (line 743).

---

### 3. **Cross-Cutting: Sample Size, Statistics, Software Versions, Data Availability, Code Availability**

#### Sample size n stated with what n represents
- **Status: PRESENT (HARD)**
- **Benchmark:** n = 150 projects (63 positive, 87 negative) (lines 729, 816).
- **Reproducibility subset:** n = 50 projects, randomly sampled with seed = 42 (line 754).
- **Repeated runs:** 5 independent runs on the same 50 projects (line 754).
- **What n represents:** Each n is a project (not a biological or technical replicate in the traditional sense; the unit is a metadata record). This is clearly stated.

#### Named statistical test and what error bars represent
- **Status: PRESENT (HARD)**
- **Metrics:** Accuracy, precision, recall, F1 score (lines 161–163, 816–821).
- **Formulas provided:** accuracy = (TP + TN) / (TP + TN + FP + FN); precision = TP / (TP + FP); recall = TP / (TP + FN); F1 = 2 × (precision × recall) / (precision + recall) (lines 820–821).
- **AUPRC:** Precision–recall curves constructed from self-reported positive probabilities; AUPRC computed (lines 299–310, 831–839).
- **Error bars:** No error bars are shown in figures. Confidence intervals are not reported. This is appropriate for a single-run benchmark (though the lack of explicit statement that no replication was performed is a minor gap). The reproducibility subset (n=50, 5 runs) shows that outputs were stable (Supplementary Tables 3–4), but confidence intervals across the full 150-project set are not provided.
- **Assessment:** Statistical methods are standard and clearly defined. No inferential statistics (e.g., hypothesis tests, p-values) are used, which is appropriate for a classification benchmark.

#### Software, tool, and instrument versions
- **Status: PRESENT (HARD)**
- See Computational/ML section above: LM Studio v0.3.33, llama.cpp v1.61.0, MLX v0.34.0, Harmony v0.3.5, all model versions with release dates (Table 4, lines 767–769).
- Closed-model APIs: OpenAI and Google (dates: 14–15 Dec 2025).

#### Data-availability statement
- **Status: PRESENT (HARD)**
- "All supplementary data are available on Figshare (https://doi.org/10.6084/m9.figshare.30265717.v2)" (line 848).
- Supplementary Tables 1–9 and Files 1–6 are enumerated (lines 849–868).
- Metadata inputs (Supplementary File 4) and LLM outputs (Supplementary File 6) are provided.

#### Code availability
- **Status: PRESENT (HARD)**
- GitHub repository: https://github.com/mshintani22/open-weight-llm-metadata-curation-workflow (line 869).
- MIT license (line 870).
- Supplementary Files 1, 3, 5, 6 contain analysis scripts (lines 849–868).

---

### 4. **Protocol Provenance: Delegated Methods**

The manuscript delegates several methods to cited references. Checking each:

#### Metadata retrieval via NCBI E-utilities and ENA API
- **Status: DELEGATED-RESOLVABLE (HARD)**
- **Cited:** NCBI Entrez Programming Utilities (E-utilities) and European Nucleotide Archive read_run API (lines 711–731).
- **Assessment:** E-utilities and ENA APIs are well-documented public services with stable, resolvable documentation. The specific queries are provided in the text (lines 720–728), making the method reproducible. Status: **RESOLVABLE**.

#### TogoID API for ID mapping
- **Status: DELEGATED-RESOLVABLE (HARD)**
- **Cited:** Ref 19 (Ikeda et al., Bioinformatics 2022, 38:4194–4199).
- **Assessment:** TogoID is a published, publicly available tool. The citation is resolvable (DOI-based). Status: **RESOLVABLE**.

#### GEO MINiML XML parsing
- **Status: DELEGATED-RESOLVABLE (HARD)**
- **Cited:** GEO MINiML format (line 719).
- **Assessment:** GEO MINiML is a standard, documented format. No custom parsing is described; standard XML parsing is implied. Status: **RESOLVABLE**.

#### LLM inference via LM Studio
- **Status: DELEGATED-RESOLVABLE (HARD)**
- **Cited:** LM Studio v0.3.33 (line 767).
- **Assessment:** LM Studio is a publicly available, documented application. The version is specified. Status: **RESOLVABLE**.

#### Prompts for classification
- **Status: DELEGATED-RESOLVABLE (HARD)**
- **Cited:** "The prompts used in this study are available in the Supplementary File 5" (line 787).
- **Assessment:** Full prompts are provided in supplementary materials. Status: **RESOLVABLE**.

#### Ground-truth labeling criteria
- **Status: SELF-CONTAINED (HARD)**
- **Provided:** Explicit criteria for positive/negative labels (lines 800–813).
- **Assessment:** Criteria are fully stated in the manuscript. Status: **PRESENT**.

---

### 5. **Cross-Cutting: Limitations & Caveats**

The manuscript explicitly acknowledges several limitations (lines 599–670):

1. **Binary classification only; complex structured outputs not evaluated** (lines 599–610).
2. **LLM decisions constrained by input metadata; incomplete/ambiguous metadata may yield incorrect decisions** (lines 611–635).
3. **Dataset derived from specific organism/treatment/data type (Arabidopsis/ABA/bulk RNA-seq); n=150 limited; generalization to other organisms/treatments/databases requires validation** (lines 636–660).
4. **Single-curator annotation; no inter-annotator agreement** (lines 661–662).
5. **Reproducibility caveats:** Outputs may be affected by inference-time randomness, software implementation, hardware differences, and session-specific conditions (lines 495–497, 601–603).

**Assessment:** These limitations are honestly and thoroughly reported. They appropriately scope the claims and are not hidden. This is a strength of the manuscript.

---

## Summary of Findings

| Category | Item | Status | Severity | Notes |
|----------|------|--------|----------|-------|
| **Computational/ML** | Dataset version + train/val/test split | MISSING | HARD | 150-project benchmark composition is fixed (Supp. Table 8), but no explicit split strategy is stated. All 150 appear used as single eval set. |
| **Computational/ML** | Architecture/algorithm | PRESENT | HARD | Pre-trained models; no custom architecture. |
| **Computational/ML** | Hyperparameters | PRESENT | HARD | Temperature=0, max_tokens=60k, reasoning effort (High/Low) for gpt-oss. |
| **Computational/ML** | Training procedure | N/A | — | No training performed; models are pre-trained and fixed. |
| **Computational/ML** | Library versions + hardware | PRESENT | HARD | LM Studio v0.3.33, llama.cpp v1.61.0, MLX v0.34.0, Harmony v0.3.5, Mac Studio M4 Max. |
| **Computational/ML** | Random seeds / reproducibility | PARTIALLY PRESENT | HARD | Main benchmark: no seed stated; temperature=0 should suppress sampling. Reproducibility subset (n=50, 5 runs): seed=42 for sampling; outputs stable except minor cross-session drift in probabilities for one model. Honest caveats provided. |
| **Computational/ML** | Code availability | PRESENT | HARD | GitHub repo + MIT license; Supp. Files 1, 3, 5, 6. |
| **Genomics/Omics** | Repository accession (GEO/SRA/ENA) | PRESENT | HARD | 150 projects identified by BioProject accession (Supp. Table 8); metadata in Supp. File 4. |
| **Cross-cutting** | Sample size n + what it represents | PRESENT | HARD | n=150 projects (63 pos, 87 neg); n=50 for reproducibility subset. Unit is project/metadata record. |
| **Cross-cutting** | Statistical test + error bars | PRESENT | HARD | Accuracy, precision, recall, F1, AUPRC. Formulas provided. No error bars (single run); reproducibility subset shows stability. |
| **Cross-cutting** | Software/tool/instrument versions | PRESENT | HARD | All versions specified (see above). |
| **Cross-cutting** | Data availability | PRESENT | HARD | Figshare DOI provided; Supp. Tables 1–9 and Files 1–6 enumerated. |
| **Cross-cutting** | Code availability | PRESENT | HARD | GitHub + MIT license. |
| **Protocol provenance** | E-utilities, ENA API, TogoID, GEO MINiML | DELEGATED-RESOLVABLE | HARD | All are public, documented services/formats. Queries provided in text. |
| **Protocol provenance** | LM Studio inference | DELEGATED-RESOLVABLE | HARD | Version specified; publicly available. |
| **Protocol provenance** | Prompts | DELEGATED-RESOLVABLE | HARD | Full prompts in Supp. File 5. |
| **Protocol provenance** | Ground-truth labeling | SELF-CONTAINED | HARD | Explicit criteria in lines 800–813. |

---

## Key Gaps & Questions for Authors

1. **Train/val/test split:** Were all 150 projects used as a single evaluation set, or was a split employed? If a single set, this should be explicitly stated. If a split was used, provide the exact composition of each partition.

2. **Main benchmark reproducibility:** Was the 150-project benchmark run once or multiple times? If once, state this explicitly. If multiple times, provide the random seed(s) or confirm determinism under temperature=0.

3. **Confidence intervals:** The reproducibility subset (n=50, 5 runs) demonstrates stability, but confidence intervals or uncertainty estimates for the main 150-project results are not provided. Consider whether these would strengthen claims about model ranking.

4. **Inter-annotator agreement:** The ground-truth labels were assigned by a single curator. While the authors acknowledge this limitation (line 661), consider whether a second independent annotation of a subset (e.g., 20–30 projects) would validate the labeling criteria.

---

## Conclusion

The manuscript is **well-documented for reproducibility** in most respects. Code, data, model versions, hardware, and hyperparameters are specified. Prompts and ground-truth criteria are provided. Limitations are honestly reported.

**One HARD gap:** The train/val/test split strategy is not explicitly stated. For a classification benchmark, this is a critical detail. The authors should clarify whether all 150 projects were used as a single evaluation set or whether a split was employed.

**One HARD caveat:** The main 150-project benchmark lacks explicit confirmation of reproducibility (single run vs. multiple runs, random seed, determinism under temperature=0). The reproducibility subset (n=50) is well-designed and shows stability, but the main results' reproducibility status should be stated clearly.

**Strengths:** Supplementary materials are comprehensive; limitations are transparent; the reproducibility experiment is well-executed and honestly reported.