# Methods Completeness & Reagent Traceability Audit
## dnoise: Fast Native Data Reduction for Bruker timsTOF

---

## Triggered Categories

The manuscript involves:
1. **Mass spectrometry (proteomics)** — primary method
2. **Computational/ML/modeling** — custom software tool (dnoise)
3. **Genomics/sequencing/omics** — benchmark data sourced from public repository

---

## MASS SPECTROMETRY (PROTEOMICS)

### Instrument & Acquisition Mode
- **Status: PRESENT**
  - Instrument: Bruker timsTOF Ultra 2 ✓
  - Acquisition modes: ddaPASEF and diaPASEF ✓
  - Gradient lengths: 5 and 15 minutes ✓

### Sample Preparation / Digestion / Enrichment
- **Status: DELEGATED-RESOLVABLE**
  - Manuscript states: "Generation Beta three-species hybrid benchmark (human, Saccharomyces cerevisiae, and Escherichia coli) deposited as PRIDE PXD070049"
  - Sample composition: 50 ng load, three conditions with defined ratios (65/30/5%, 65/15/20%, 65/3/32%) ✓
  - Replicates: 6 replicates per condition, 18 runs per gradient/mode (72 total) ✓
  - **Severity: SOFT** — Sample prep details delegated to the public dataset (PXD070049). Manuscript provides sufficient detail to locate and retrieve the original sample preparation from the PRIDE record. No custom preparation described.

### Search Engine & Version
- **Status: PRESENT**
  - ddaPASEF: Sage 0.15.0-beta.121 ✓
  - diaPASEF: DIA-NN 2.2.0 ✓

### Database & Version
- **Status: PRESENT**
  - Species-tagged FASTA from benchmark ✓
  - Whole-proteome spectral library predicted from benchmark FASTA before denoising ✓
  - **Note:** Exact FASTA version/identifier not explicitly stated, but resolvable from PXD070049 metadata.

### FDR, Modifications, Tolerances
- **Status: PRESENT**
  - Fully tryptic, 2 missed cleavages ✓
  - Peptide length: 7–30 ✓
  - Fixed: cysteine carbamidomethylation ✓
  - Variable: methionine oxidation ✓
  - Precursor tolerance: ±20 ppm ✓
  - Fragment tolerance: ±20 ppm ✓
  - FDR control: "decoy-controlled LFQ q-values" (Sage); DIA-NN two-pass refinement ✓
  - **Severity: SOFT** — FDR threshold (e.g., 1% protein-level FDR) mentioned in results ("1% LFQ q-value") but not explicitly stated in methods. Resolvable from Section S7 (complete configurations).

### Quantification Method
- **Status: PRESENT**
  - ddaPASEF: Sage mobility-aware MS1 label-free quantification (LFQ) with IonQuant-style match-between-runs ✓
  - diaPASEF: DIA-NN MaxLFQ from MS2 fragment chromatograms; direct MS1 check via Ms1.Normalised ✓
  - Normalization: cross-run mean total intensity within gradient ✓

### Repository Accession
- **Status: PRESENT**
  - Raw data: PRIDE PXD070049 ✓
  - Release date: 3 February 2026 (publicly accessible, no reviewer credentials) ✓
  - Resolves to: ebi.ac.uk/pride/archive/projects/PXD070049 ✓

### Replicates (SOFT)
- **Status: PRESENT**
  - Biological replicates: 6 per condition ✓
  - Technical replicates: Not explicitly stated (appears to be biological only)
  - **Severity: SOFT** — Sufficient for the benchmark; no ambiguity about what n represents.

---

## COMPUTATIONAL / ML / MODELING

### Custom Software: dnoise

#### Dataset(s) with Version & Train/Val/Test Split
- **Status: PRESENT**
  - Dataset: PRIDE PXD070049 (Generation Beta benchmark) ✓
  - Split: Parameter selection on 15-minute ddaPASEF Condition A (6 replicates); 5-minute gradient and both diaPASEF acquisitions held out ✓
  - **Severity: HARD** — Acknowledged as not fully out-of-sample: "the 15-minute ddaPASEF results are not fully out-of-sample" (line 127–128). This is disclosed; no missing information.

#### Algorithm / Architecture
- **Status: PRESENT**
  - Three-stage filtering pipeline:
    1. Acquisition-aware geometric gates (precursor-selection polygon for ddaPASEF; isolation windows for diaPASEF) ✓
    2. Ion-mobility streak filter (per-TOF column, mobility-scan grouping, run detection) ✓
    3. m/z–halo filter (local intensity comparison) ✓
  - Optional stages: MS/MS filtering, MS1 centroiding (watershed and box) ✓

#### Hyperparameters
- **Status: PRESENT**
  - Streak filter: `min_feature_length=5`, `max_internal_gap=2`, `intensity_floors=0` ✓
  - Halo filter: `halo_peak_fraction=0.15` ✓
  - Gate padding: m/z and mobility padding for edge protection (values not numerically stated in main text) ✓
  - MS/MS filter parameters: `msms_*` relaxed parameters (exact values in Table S1) ✓
  - **Severity: SOFT** — Complete defaults listed in Table S1 (Supporting Information). Main text provides sufficient detail for reproduction; numerical padding values should be in Table S1.

#### Training Procedure
- **Status: PRESENT (Grid Sweep)**
  - Parameter selection: Grid sweep on Condition A (15-minute ddaPASEF) ✓
  - Scoring metrics: quantified coverage, replicate precision, intensity fidelity ✓
  - Rationale: "chose gap 2 and length 5 to prioritize stricter local continuity and greater point removal" (line 119–120) ✓

#### Library Versions & Hardware
- **Status: PRESENT**
  - Language: Rust ✓
  - Dependencies: timsrust 0.4.2, rayon (parallelization), custom Bruker type-2 analysis.tdf_bin encoder ✓
  - Hardware (benchmark): Intel Core i7-12700H, 20 threads ✓
  - **Severity: HARD** — timsrust version specified; rayon version NOT specified. Rayon is a critical dependency for parallel processing.
    - **Status: MISSING** — rayon version

#### Random Seeds / Reproducibility
- **Status: PRESENT**
  - No stochastic components in filtering (deterministic algorithm) ✓
  - Parallelization via rayon (order-independent operations) ✓
  - No seed statement needed; filtering is reproducible by design ✓

#### Code Availability
- **Status: PRESENT**
  - Repository: github.com/pgarrett-scripps/dnoise ✓
  - License: MIT ✓
  - Release version: dnoise v0.1.0 ✓
  - Zenodo archive: doi.org/10.5281/zenodo.21959649 ✓
  - **Severity: HARD** — All required identifiers present.

#### Metric Definitions
- **Status: PRESENT**
  - Data reduction: frame-binary size (bytes), MS1 point count ✓
  - Identification retention: PSM, peptide, protein-group counts ✓
  - Quantification accuracy: species-specific median log₂ ratio vs. known mixture ratio ✓
  - Precision: median pooled protein CV within conditions ✓
  - Runtime: wall-clock time on benchmark workstation ✓
  - Memory: peak working-set (anonymous resident memory) and RSS ✓

#### Environment File / Reproducibility
- **Status: PRESENT (Partial)**
  - Rust project: Cargo.toml implied (standard Rust practice) but not explicitly provided in manuscript ✓
  - Software versions: Sage 0.15.0-beta.121, DIA-NN 2.2.0, timsrust 0.4.2 ✓
  - Complete configurations: Section S7 (Sage config, DIA-NN commands) ✓
  - **Severity: SOFT** — Cargo.toml or equivalent dependency lock file should be in the repository (github.com/pgarrett-scripps/dnoise). Manuscript does not need to reproduce it inline.

#### Ablations
- **Status: PRESENT**
  - Per-stage ablation: Table S4 (acquisition gate, streak filter, halo filter separately) ✓
  - Control comparison: matched intensity-threshold filter (Section 3.4, Figure S5, Section S5) ✓
  - Optional stages: MS/MS filtering (Section 3.3), centroiding (Section 3.5) ✓

---

## GENOMICS / SEQUENCING / OMICS

### Platform & Mode
- **Status: PRESENT**
  - Platform: Bruker timsTOF Ultra 2 ✓
  - Mode: trapped ion mobility spectrometry (TIMS) + parallel accumulation–serial fragmentation (PASEF) ✓
  - Acquisition modes: ddaPASEF (data-dependent), diaPASEF (data-independent) ✓

### Library-Prep Kit
- **Status: DELEGATED-RESOLVABLE**
  - Delegated to PRIDE PXD070049 (benchmark dataset) ✓
  - No custom library prep; standard commercial digest ✓

### Depth / Coverage
- **Status: PRESENT**
  - Gradient length: 5 and 15 minutes ✓
  - Sample load: 50 ng ✓
  - Frame count: "thousands of frames" per run; 27 minutes total acquisition (loading + gradient + washout) ✓
  - **Severity: SOFT** — Exact frame counts per run not stated, but not critical for reproduction (dnoise processes all frames).

### Reference Genome / Build
- **Status: PRESENT**
  - Three-species benchmark: human, Saccharomyces cerevisiae, Escherichia coli ✓
  - FASTA source: benchmark FASTA (species-tagged) ✓
  - **Severity: SOFT** — Specific genome builds not stated, but resolvable from PXD070049 metadata. Not critical for the denoising tool itself (operates on raw frames).

### Alignment / Analysis Tools WITH Versions & Key Parameters
- **Status: PRESENT**
  - Sage 0.15.0-beta.121 (search engine) ✓
  - DIA-NN 2.2.0 (search engine) ✓
  - IonQuant (embedded in Sage for LFQ) ✓
  - MaxLFQ (embedded in DIA-NN for protein quantification) ✓
  - Key parameters: fully tryptic, 2 missed cleavages, 7–30 aa, ±20 ppm tolerances ✓

### Repository Accession
- **Status: PRESENT**
  - PRIDE PXD070049 ✓

### QC Thresholds (SOFT)
- **Status: PRESENT (Partial)**
  - Protein reporting: ≥2 distinct quantified peptides, ≥2 replicates per condition ✓
  - FDR: "1% LFQ q-value" mentioned in results; decoy-controlled ✓
  - **Severity: SOFT** — Explicit FDR threshold (e.g., 1% PSM-level, 1% peptide-level) not stated in methods; resolvable from Section S7.

### Batch Handling (SOFT)
- **Status: PRESENT**
  - Normalization: cross-run mean total intensity within gradient ✓
  - No batch-correction method described (not needed for single-instrument, single-lab benchmark) ✓

---

## CROSS-CUTTING ITEMS

### Sample Size n (What n Represents)
- **Status: PRESENT**
  - n = 6 biological replicates per condition ✓
  - 3 conditions (A, B, C) ✓
  - 2 acquisition modes (ddaPASEF, diaPASEF) ✓
  - 2 gradient lengths (5, 15 minutes) ✓
  - Total: 72 raw runs ✓
  - **Clarity:** "Each condition had six replicates, for 18 runs per gradient and acquisition mode (72 raw runs total)" (line 143–144) ✓

### Statistical Tests & Error Bars
- **Status: PRESENT (Partial)**
  - Accuracy comparison: "percentile-bootstrap 95% confidence intervals... by resampling shared contributing proteins (2,000 resamples)" ✓
  - Precision: "median pooled protein CV" ✓
  - **Severity: SOFT** — Confidence intervals reported in Tables S10 and S11 (not shown in main figures). Error bars in Figures 3–4 show whiskers (5th–95th percentiles) for CV distributions, not confidence intervals. Appropriate for the data shown.

### Software, Tool, Instrument Versions
- **Status: PRESENT (Mostly)**
  - Instruments: Bruker timsTOF Ultra 2 ✓
  - Search engines: Sage 0.15.0-beta.121, DIA-NN 2.2.0 ✓
  - Libraries: timsrust 0.4.2 ✓
  - **Missing:** rayon version (parallelization library) — **HARD**
  - Custom tool: dnoise v0.1.0 ✓
  - **Severity: HARD** — rayon is a critical dependency; version should be specified.

### Data-Availability Statement
- **Status: PRESENT**
  - Raw MS data: PRIDE PXD070049, publicly accessible ✓
  - dnoise code: github.com/pgarrett-scripps/dnoise (MIT licensed) ✓
  - Software release: Zenodo doi.org/10.5281/zenodo.21959649 ✓
  - Configurations: Section S7 (Sage, DIA-NN) ✓
  - Supporting data: Tables S1–S16 in Supporting Information ✓

### Code Availability
- **Status: PRESENT**
  - Repository: github.com/pgarrett-scipps/dnoise ✓
  - License: MIT ✓
  - Release: v0.1.0 with Zenodo DOI ✓
  - **Severity: HARD** — All required identifiers present.

---

## PROTOCOL PROVENANCE

### Delegated Methods (Resolvability Check)

| Method | Citation | Status | Notes |
|--------|----------|--------|-------|
| TIMS/PASEF acquisition | Meier et al. 2015 (ref 3); Fernandez-Lima et al. 2011 (ref 1); Cumeras et al. 2015 (ref 2) | Delegated-resolvable | Standard instrument operation; citations are primary literature. |
| Sample preparation (Generation Beta) | PRIDE PXD070049; Van Puyvelde et al. (refs 18–19) | Delegated-resolvable | Public dataset with full protocol metadata. |
| Sage search | Lazear 2023 (ref 21) | Delegated-resolvable | Published tool; version specified. |
| DIA-NN search | Demichev et al. 2020 (ref 23) | Delegated-resolvable | Published tool; version specified. |
| IonQuant LFQ | Yu et al. 2021 (ref 22) | Delegated-resolvable | Published method; embedded in Sage. |
| MaxLFQ quantification | Cox et al. 2014 (ref 24) | Delegated-resolvable | Published method; embedded in DIA-NN. |
| Target-decoy search | Elias & Gygi 2007 (ref 25) | Delegated-resolvable | Standard FDR method; widely implemented. |
| PNNL PreProcessor (comparison) | Bilbao et al. 2022 (ref 7) | Delegated-resolvable | Cited as existing tool; not used in this work. |
| mzML conversion (context) | Martens et al. 2011 (ref 5); Pfeuffer et al. 2024 (ref 6) | Delegated-resolvable | Cited for context; not used in this work. |

**Assessment:** All delegated methods resolve to resolvable, published sources. No circular citations or dead references detected. No load-bearing method is outsourced without citation.

---

## SUMMARY OF FINDINGS

### HARD Missing Items
1. **rayon version** — Critical parallelization dependency; version not specified. Manuscript states "filters and encodes them in parallel with rayon" (line 137) but does not provide version. This should be in Cargo.toml (available in repository) or stated explicitly.

### SOFT Missing / Unverifiable Items
1. **Gate padding values (m/z and mobility)** — Manuscript states "Both accept padding in m/z and mobility to protect edge features" (line 83) but does not give numerical values. Likely in Table S1; not verified from manuscript alone.
2. **Exact FDR threshold** — Results mention "1% LFQ q-value" but methods do not explicitly state the FDR cutoff. Resolvable from Section S7.
3. **Genome builds** — Reference genomes for the three species not specified (human build, yeast strain, E. coli strain). Resolvable from PXD070049 metadata; not critical for the denoising tool.
4. **Frame counts per run** — Total number of frames per acquisition not stated. Not critical (dnoise processes all frames).
5. **Cargo.toml / dependency lock** — Rust project dependencies should be in repository; not required in manuscript.

### Unverifiable (Require Author Clarification)
- **rayon version:** Cannot be confirmed from manuscript; must be checked in github.com/pgarrett-scripps/dnoise repository or Zenodo archive.

---

## CONCLUSION

The manuscript provides **comprehensive methods documentation** for a reproducible computational tool and benchmark study. **One HARD item is missing** (rayon version), which is a critical dependency that should be specified. All other items are either present, delegated to resolvable public sources, or soft recommendations. The work is **substantially reproducible** with the provided information and public data/code.