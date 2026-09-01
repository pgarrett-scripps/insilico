# Methods Completeness & Reagent Traceability Audit

## Scope & Trigger Detection

This manuscript describes **computational/ML/modeling** work training machine-learned weather forecast models with different loss functions. No biological, chemical, clinical, imaging, or sequencing methods are present.

**Active checklist category:** Computational/ML/modeling (HARD and SOFT items).

---

## Computational/ML/Modeling — HARD Items

### 1. Dataset(s) with version + exact train/val/test split

**Status: MISSING (HARD)**

- **Training data source:** ERA5 reanalysis, 1979–2020 stated (§3.1).
- **Inference data:** 2022 stated (§3.1).
- **Missing specifics:**
  - No ERA5 version/product identifier (e.g., ERA5 single-level, pressure-level, native resolution).
  - No explicit train/validation/test split percentages or date ranges.
  - No statement of whether validation was used during training or only for final evaluation.
  - No description of how the 2022 inference set was partitioned (if at all) for reporting results.

**What would resolve it:** Specify ERA5 product variant, exact date ranges for train/val/test, and whether validation was held out during training.

---

### 2. Architecture/algorithm specification

**Status: PRESENT (HARD)**

- Encoder–processor–decoder architecture described (§3.1).
- Graph neural network encoder and decoder connectivity specified (4 nearest processor-grid nodes for encoder; 8 for decoder).
- k-nearest-neighbour graph with k=16 on O96 reduced Gaussian grid stated for graph-based scores (§3.1).
- Smaller model variant for §3.2 experiments: embedding dimension 256, 12 processor layers (§3.2).
- Reference to AIFS-CRPS architecture provided (§3.1, [13]).

**Note:** Full architecture details are delegated to [13] (AIFS-CRPS). The manuscript states "we follow AIFS-CRPS in terms of architecture" but does not reproduce the full architecture specification. This is acceptable for a follow-up study, but the reader cannot fully reconstruct the model from this manuscript alone without consulting [13].

---

### 3. Hyperparameters

**Status: PRESENT (HARD)**

- **Training schedule (§3.1):**
  - 150,000 iterations at rollout 1
  - 30,000 iterations at rollout 2
  - 1,000 iterations per rollout step 3–12
  
- **Learning rates:**
  - Rollout 1: 10⁻³
  - Rollout 2: 10⁻⁵
  - Rollouts 3–12: 10⁻⁶ (fixed)
  
- **Learning-rate schedule:** Cosine schedule with 1,000-step warmup for rollouts 1–2; fixed for rollouts 3–12.

- **Optimizer:** AdamW with weight decay 0.1.

- **Ensemble size:** 8-member ensembles (§3.1).

- **Spectral truncation:** T191 (§3.2).

- **Smoothing kernel widths (§3.2):** ~100, 200, 400, 800 km (4 operators).

- **Spectral band grouping (§3.2):** ℓ = 0–10, 11–20, 21–80, 81–120, 121–191.

- **Loss weighting (§3.2):** Different weighting for small scales of geopotential and mean sea-level pressure; ad hoc, not tuned (stated as "chosen only to be of the right order of magnitude").

- **Graph energy score anchor weight (§3.1):** 0.1 × fES in Lgraph = fGESgraph + 0.1 fES.

- **Almost fair CRPS parameter:** α = 0.95 (stated in Tables 1 and 2).

---

### 4. Training procedure (optimizer/schedule/early-stopping)

**Status: MOSTLY PRESENT; EARLY-STOPPING UNSPECIFIED (HARD)**

- **Optimizer:** AdamW with weight decay 0.1 ✓
- **Learning-rate schedule:** Cosine warmup + decay (rollouts 1–2); fixed (rollouts 3–12) ✓
- **Iterations per phase:** Specified ✓
- **Early-stopping criterion:** NOT STATED.
  - No mention of validation loss monitoring, patience, or stopping rule.
  - No statement of whether all 150,000 iterations at rollout 1 were always completed or stopped early.

**What would resolve it:** State whether early stopping was used, on what metric, with what patience; or confirm that all scheduled iterations were always completed.

---

### 5. Library versions + hardware

**Status: PARTIALLY PRESENT (HARD)**

- **Framework:** Anemoi framework (https://github.com/ecmwf/anemoi-core) ✓
- **Anemoi version:** NOT STATED.
- **PyTorch version:** NOT STATED (though torch.compile is mentioned as a tool used for efficiency).
- **Triton version:** NOT STATED (Triton kernels generated via torch.compile; [24] cited but version not given).
- **Hardware:** NOT STATED.
  - Compute provided by Gauss Centre for Supercomputing (JUPITER at JSC) acknowledged, but no details on GPU/CPU type, memory, or node configuration.
  - No wall-clock time or compute budget stated.

**What would resolve it:** Specify Anemoi, PyTorch, and Triton versions; describe hardware (GPU model, count, memory); state total compute hours or equivalent.

---

### 6. Random seeds (or seed-averaging statement)

**Status: MISSING (HARD)**

- No mention of random seed(s) for model initialization, data shuffling, or ensemble generation.
- No statement of whether results are single runs or averaged over multiple seeds.
- No reproducibility statement (e.g., "all experiments run once" or "results averaged over 3 runs with different seeds").

**What would resolve it:** State the random seed(s) used, or report results as mean ± SD over multiple runs with different seeds.

---

### 7. Code availability

**Status: UNVERIFIABLE (HARD)**

- **Anemoi framework:** Public repository URL provided (https://github.com/ecmwf/anemoi-core).
- **Custom training/evaluation code for this study:** NOT STATED.
  - No link to a repository, supplementary materials, or data archive.
  - No statement of whether code will be released or is available upon request.
  - The manuscript does not claim code is unavailable, but does not explicitly provide or promise it either.

**What would resolve it:** Provide a DOI/URL to a code repository (GitHub, Zenodo, institutional archive) containing the training and evaluation scripts, or state clearly that code is available upon request with contact information.

---

## Computational/ML/Modeling — SOFT Items

### 1. Compute budget

**Status: MISSING (SOFT)**

- Acknowledged use of JUPITER supercomputer but no quantification of GPU-hours, wall-clock time, or cost.

---

### 2. Ablations

**Status: PRESENT (SOFT)**

- Section 3.2 systematically compares 12 different loss configurations (Table 2), which serves as an ablation study of scale-aware and spectral loss variants.

---

### 3. Metric definitions

**Status: PRESENT (SOFT)**

- Fair CRPS used for verification (§4.1) — definition provided in §2.
- Accumulated tendency spectra computed as differences between forecast and initial state (§4.2).
- Spectral truncation T191 stated.
- No ambiguity in metric computation.

---

### 4. Environment file (requirements.txt, environment.yml, etc.)

**Status: MISSING (SOFT)**

- No dependency list, environment file, or container specification provided.

---

## Protocol-Provenance Check

### Delegated Methods

**AIFS-CRPS architecture (§3.1):** "We follow AIFS-CRPS [[13](#ref-13)] in terms of architecture and general training configuration."

- **Reference:** [13] Lang et al. 2024, "AIFS-CRPS: Ensemble forecasting using a model trained with a loss function based on the continuous ranked probability score."
- **Status:** Resolvable (published paper, DOI-citable).
- **Severity:** This is a follow-up study, so delegating the base architecture is reasonable. However, the manuscript does state a key deviation: "restrict resolution here to an O96 ≈ 1 deg model," which is explicitly noted.

**Spherical harmonic transform (§3.2):** "For scores computed in spectral space, we use the spherical harmonic transform capability recently added to Anemoi."

- **Status:** Delegated to Anemoi framework; no specific reference to a paper or documentation URL.
- **Severity:** The implementation is in the public Anemoi repository, so it is in principle inspectable, but the manuscript does not cite a specific commit, version, or documentation page. Unverifiable from the manuscript alone.

**Smoothing operators (§3.2):** "All multi-scale experiments used four graph-based Gaussian smoothing operators on the native O96 grid, with kernel widths of approximately 100, 200, 400, and 800 km."

- **Status:** Described in-line; no delegation.
- **Severity:** "Approximately" suggests these are nominal values, not exact. No formula or implementation reference given. Reproducible in principle but with some ambiguity in kernel definition.

---

## Data Availability Statement

**Status: MISSING (HARD)**

- **Training data (ERA5):** Public dataset, but no explicit statement of how to access it or which product variant.
- **Inference/evaluation data (2022 forecasts):** No statement of whether forecast outputs will be deposited or are available upon request.
- **No formal data-availability statement** in the manuscript.

**What would resolve it:** Add a statement such as: "ERA5 data are publicly available from the Copernicus Climate Data Store. Forecast outputs from this study are available at [repository/DOI] or upon request from the authors."

---

## Summary Table

| Item | Category | Severity | Status | Notes |
|------|----------|----------|--------|-------|
| Dataset version & split | Computational/ML | HARD | Missing | ERA5 product variant, train/val/test dates, validation protocol not specified |
| Architecture | Computational/ML | HARD | Present | Delegated to [13] with noted deviation (O96 resolution); acceptable for follow-up |
| Hyperparameters | Computational/ML | HARD | Present | All learning rates, schedules, ensemble size, spectral params, loss weights stated |
| Training procedure | Computational/ML | HARD | Partial | Optimizer & schedule present; early-stopping criterion not stated |
| Library versions | Computational/ML | HARD | Missing | Anemoi, PyTorch, Triton versions not given; hardware not specified |
| Random seeds | Computational/ML | HARD | Missing | No seed(s) stated; no statement of single vs. multiple runs |
| Code availability | Computational/ML | HARD | Unverifiable | Anemoi public; custom code for this study not linked or promised |
| Compute budget | Computational/ML | SOFT | Missing | Supercomputer acknowledged but no GPU-hours or wall-clock time |
| Ablations | Computational/ML | SOFT | Present | 12-experiment comparison in §3.2 |
| Metric definitions | Computational/ML | SOFT | Present | Fair CRPS, accumulated tendencies, spectral truncation all defined |
| Environment file | Computational/ML | SOFT | Missing | No requirements.txt or environment.yml |
| Data availability statement | Cross-cutting | HARD | Missing | No formal statement of where forecast outputs or processed data can be accessed |

---

## Questions for Authors

1. **ERA5 product:** Which ERA5 product (single-level, pressure-level, native resolution) was used? Provide a DOI or Copernicus CDS link.

2. **Train/val/test split:** What are the exact date ranges for training, validation (if used during training), and test? Were any 2022 dates held out for validation?

3. **Early stopping:** Was early stopping used during training? If so, on what metric and with what patience? If not, were all scheduled iterations always completed?

4. **Library versions:** Provide Anemoi, PyTorch, and Triton versions used. Specify GPU model(s), count, and memory.

5. **Random seeds:** What random seed(s) were used? Are results from a single run or averaged over multiple seeds?

6. **Code availability:** Will custom training and evaluation code be released? If so, where and when? If not, state that it is available upon request.

7. **Forecast outputs:** Will the 2022 forecast ensemble members be deposited in a public archive (e.g., Zenodo, institutional repository)? If not, state the conditions under which they are available.

8. **Spherical harmonic transform:** Cite a specific Anemoi version, commit, or documentation page for the spherical harmonic implementation.

9. **Smoothing kernels:** Provide the exact formula or reference for the Gaussian smoothing operators (e.g., standard deviation in grid points, or explicit kernel definition).