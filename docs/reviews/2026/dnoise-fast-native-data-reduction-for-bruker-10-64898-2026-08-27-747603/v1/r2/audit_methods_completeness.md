# Methods Completeness & Reagent Traceability Audit
## dnoise: Fast Native Data Reduction for Bruker timsTOF

---

## Triggered Categories

The manuscript involves:
1. **Mass spectrometry (proteomics)** — primary method
2. **Computational/ML/modeling** — dnoise tool development and benchmarking
3. **Genomics/sequencing/omics** — benchmark data from public repository

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
  - **Unverifiable detail**: Full digestion protocol (enzyme, buffer, time, temperature) not stated in manuscript. Delegated to PXD070049 PRIDE entry. Manuscript does not explicitly state whether this is a commercial standard or custom preparation. Citation is resolvable (PRIDE accession given), but contents unverified from manuscript alone.

### Search Engine & Version
- **Status: PRESENT**
  - ddaPASEF: Sage 0.15.0-beta.121 ✓
  - diaPASEF: DIA-NN 2.2.0 ✓

### Database & Version
- **Status: PRESENT**
  - Species-tagged FASTA from benchmark ✓
  - One whole-proteome spectral library predicted from benchmark FASTA before denoising ✓
  - **Unverifiable detail**: Exact FASTA file version/date not stated. Delegated to PXD070049. Resolvable via PRIDE but not verified in manuscript.

### FDR, Modifications, Tolerances
- **Status: PRESENT**
  - Precursor tolerance: ±20 ppm ✓
  - Fragment tolerance: ±20 ppm ✓
  - Fixed modification: cysteine carbamidomethylation ✓
  - Variable modification: methionine oxidation ✓
  - Peptide length: 7–30 amino acids ✓
  - Missed cleavages: 2 ✓
  - Tryptic specificity: fully tryptic ✓
  - **Missing (HARD)**: FDR threshold not explicitly stated for Sage searches. Manuscript mentions "decoy-controlled LFQ q-values" and "1% LFQ q-value" (line 244) but does not state the PSM-level or peptide-level FDR cutoff applied during initial search. For DIA-NN, no FDR threshold is stated.

### Quantification Method
- **Status: PRESENT**
  - ddaPASEF: Sage mobility-aware MS1 label-free quantification (LFQ) with IonQuant-style precursor integration and match-between-runs ✓
  - diaPASEF: DIA-NN MaxLFQ from MS2 fragment chromatograms ✓
  - Normalization: cross-run mean total intensity within gradient ✓
  - Protein reporting rule: ≥2 distinct quantified peptides, ≥2 replicates per compared condition ✓

### Repository Accession
- **Status: PRESENT**
  - Raw data: PRIDE PXD070049 ✓
  - Deposition date: 3 February 2026 (stated as released and publicly accessible) ✓
  - URL: ebi.ac.uk/pride/archive/projects/PXD070049 ✓

### Replicates (SOFT)
- **Status: PRESENT**
  - Biological replicates: 6 per condition ✓
  - Technical replicates: not explicitly stated whether the 6 replicates are independent LC-MS runs or technical replicates of the same sample. Implied to be independent runs (standard for benchmark design) but not stated.

---

## COMPUTATIONAL / ML / MODELING

### Dataset(s) with Version & Train/Val/Test Split
- **Status: PRESENT (with caveat)**
  - Dataset: Generation Beta three-species benchmark (PXD070049) ✓
  - Composition: human/yeast/E. coli at three defined ratios ✓
  - **Unverifiable detail**: Dataset version/release date not stated in manuscript. PRIDE accession resolves to the data, but version control is delegated to PRIDE.
  - **Train/val/test split**: Not applicable — this is a benchmarking study, not a machine-learning model. Parameter selection used "one homogeneous sample, the six replicates of Condition A of the 15-minute ddaPASEF gradient" (line 93). The remaining three conditions and both diaPASEF acquisitions are out-of-sample. The 5-minute gradient and diaPASEF are explicitly stated as not used in parameter selection (line 109). ✓

### Architecture / Algorithm
- **Status: PRESENT**
  - Three-stage filtering pipeline described:
    1. Acquisition-aware geometric gates (precursor-selection polygon for ddaPASEF, isolation windows for diaPASEF) ✓
    2. Ion-mobility streak filter (per-TOF-column mobility profile, run grouping, length/gap thresholds) ✓
    3. Halo filter (off-column peak-fraction threshold) ✓
  - Optional stages: MS/MS filtering, MS1 centroiding (watershed and box) ✓

### Hyperparameters
- **Status: PRESENT**
  - Default parameters: Table S1 (referenced, not fully reproduced in main text) ✓
  - Streak filter: min_feature_length=5, max_internal_gap=2 ✓
  - Halo filter: halo_peak_fraction=0.15 ✓
  - Padding for edge protection: stated as configurable but specific values for benchmark not given in main text (delegated to Table S1).
  - **Unverifiable detail**: Table S1 is in Supporting Information, not provided in the manuscript text. Stated to be "listed in Table S1" but full parameter set not reproduced in main body. This is acceptable for supplementary material, but the specific padding values used in the benchmark are not stated in the main text.

### Training Procedure (Optimizer/Schedule/Early-Stopping)
- **Status: NOT APPLICABLE**
  - dnoise is a rule-based filtering tool, not a trained model. No optimization, learning schedule, or early-stopping applies.

### Library Versions & Hardware
- **Status: PRESENT**
  - Language: Rust ✓
  - Key library: timsrust 0.4.215 ✓
  - Parallelization: rayon ✓
  - Encoding: custom Bruker type-2 analysis.tdf_bin encoder ✓
  - Hardware (benchmark): Intel Core i7-12700H, 20 threads ✓
  - Operating system: implied Linux/Unix (memory-mapped I/O, RSS reporting) but not explicitly stated.

### Random Seeds
- **Status: NOT APPLICABLE**
  - Deterministic filtering algorithm; no randomness or stochastic elements.

### Code Availability (HARD)
- **Status: PRESENT**
  - Repository: github.com/pgarrett-scripps/dnoise ✓
  - License: MIT ✓
  - Package registry: crates.io ✓
  - Exact release: dnoise v0.1.0 ✓
  - Archival: Zenodo doi.org/10.5281/zenodo.21959649 ✓

### Compute Budget (SOFT)
- **Status: PRESENT**
  - Runtime: 7.4–39.0 seconds (MS1-only), 10.2–68.7 seconds (MS1+MS/MS) on benchmark workstation ✓
  - Memory: peak working set 2.4–4.56 GB, RSS up to 8.8 GB ✓
  - Table S16 provides per-file timing and memory ✓

### Ablations (SOFT)
- **Status: PRESENT**
  - Per-stage ablation: Table S4 separates acquisition gate, streak filter, and halo filter contributions ✓
  - Matched intensity-threshold control: Section S5 and Figure S5 compare streak filter vs. per-point intensity cutoff ✓
  - Optional MS/MS filtering: Section S4 and Table S6 characterize identification/reduction tradeoff ✓
  - Optional centroiding: Section S6, Figure S7, Table S15 ✓

### Metric Definitions (SOFT)
- **Status: PRESENT**
  - Data reduction: frame-binary size (bytes) and point count ✓
  - Identification retention: PSM, peptide, protein-group counts ✓
  - LFQ accuracy: species-specific median log₂ ratio vs. known mixture ratio ✓
  - Precision: median pooled protein CV within conditions ✓
  - Feature-level agreement: Pearson r and median absolute Δlog₂ (Figure 5) ✓

### Environment File (SOFT)
- **Status: MISSING**
  - No Cargo.toml, requirements.txt, or equivalent dependency manifest provided in manuscript or (as far as stated) in the repository documentation quoted. The manuscript lists key dependencies (timsrust 0.4.215, rayon) but does not provide a complete reproducible environment specification.
  - **Note**: Rust projects typically include Cargo.lock in version control, which would be sufficient. The Zenodo archive likely includes this, but it is not explicitly confirmed in the manuscript.

---

## GENOMICS / SEQUENCING / OMICS

### Platform & Mode
- **Status: PRESENT**
  - Platform: Bruker timsTOF Ultra 2 ✓
  - Mode: trapped ion mobility spectrometry (TIMS) + parallel accumulation–serial fragmentation (PASEF) ✓
  - Variants: ddaPASEF (data-dependent) and diaPASEF (data-independent) ✓

### Library-Prep Kit
- **Status: DELEGATED-RESOLVABLE**
  - Not stated in manuscript. Delegated to PXD070049 PRIDE entry and Generation Beta benchmark documentation (Van Puyvelde et al., refs 18–19).
  - **Unverifiable**: Manuscript does not provide enough detail to confirm library prep from the text alone.

### Depth / Coverage
- **Status: PRESENT**
  - Gradient length: 5 and 15 minutes ✓
  - Sample load: 50 ng ✓
  - Frame count: "thousands of frames" per run; specific frame counts per run not stated.
  - **Unverifiable detail**: Total number of frames per run not given. Implied from "27 minutes of acquisition" and "6.7 GB of frame data" (line 37) but not explicitly counted.

### Reference Genome WITH Build
- **Status: NOT APPLICABLE**
  - Proteomics study; no genomic alignment. Protein sequences from FASTA (species-tagged) used for database search.

### Alignment / Analysis Tools WITH Versions & Key Parameters
- **Status: PRESENT**
  - Sage 0.15.0-beta.121 (ddaPASEF) ✓
  - DIA-NN 2.2.0 (diaPASEF) ✓
  - Key parameters listed above (search section) ✓
  - **Unverifiable detail**: DIA-NN two-pass refinement procedure not fully detailed in manuscript. Delegated to DIA-NN documentation/defaults.

### Repository Accession
- **Status: PRESENT**
  - PRIDE PXD070049 ✓

### QC Thresholds (SOFT)
- **Status: PARTIALLY PRESENT**
  - Protein reporting: ≥2 distinct quantified peptides, ≥2 replicates per condition ✓
  - LFQ q-value: 1% mentioned (line 244) but not stated as the primary FDR threshold for all searches.
  - **Missing (SOFT)**: No explicit statement of PSM-level FDR or peptide-level FDR thresholds for Sage or DIA-NN.

### Batch Handling (SOFT)
- **Status: PRESENT**
  - Normalization: cross-run mean total intensity within gradient ✓
  - Match-between-runs: Sage/IonQuant with decoy-controlled LFQ q-values ✓
  - DIA-NN two-pass refinement (batch-aware) ✓

---

## CROSS-CUTTING ITEMS

### Sample Size n with Definition
- **Status: PRESENT**
  - n = 6 biological replicates per condition ✓
  - n = 3 conditions (A, B, C) ✓
  - n = 2 acquisition modes (ddaPASEF, diaPASEF) ✓
  - n = 2 gradient lengths (5, 15 minutes) ✓
  - Total: 72 raw runs ✓
  - **Clarification needed (SOFT)**: Whether the 6 replicates per condition are independent biological samples or technical replicates of the same sample. Implied to be independent (standard for benchmark) but not explicitly stated.

### Statistical Test & Error Bars
- **Status: PRESENT**
  - Accuracy comparison: percentile-bootstrap 95% confidence intervals (2,000 resamples) on shared contributing proteins ✓
  - Precision: median pooled protein CV ✓
  - Feature-level agreement: Pearson r and median absolute Δlog₂ ✓
  - **Unverifiable detail**: Specific statistical tests for other comparisons (e.g., protein-count changes) not stated. Differences reported as counts or percentages without formal hypothesis tests, which is acceptable for a descriptive benchmark.

### Software, Tool, Instrument Versions
- **Status: PRESENT**
  - Sage 0.15.0-beta.121 ✓
  - DIA-NN 2.2.0 ✓
  - timsrust 0.4.215 ✓
  - dnoise v0.1.0 ✓
  - Bruker timsTOF Ultra 2 (instrument model, no firmware version stated) ✓
  - **Missing (SOFT)**: Bruker instrument firmware version, Bruker timsdata library version (used by DIA-NN), operating system and version for benchmark workstation.

### Data-Availability Statement
- **Status: PRESENT**
  - Raw MS data: PRIDE PXD070049, publicly accessible ✓
  - Code: github.com/pgarrett-scripps/dnoise, MIT licensed, Zenodo archive ✓
  - Configuration: Table S1 (parameters), Section S7 (Sage and DIA-NN configs) ✓
  - Supporting data: Section S2–S6 (ablations, parameter sweeps, controls) ✓

### Code Availability (Custom Analysis)
- **Status: PRESENT**
  - dnoise tool: github.com/pgarrett-scripps/dnoise ✓
  - Analysis scripts: "analysis and figure-generation scripts" mentioned (Acknowledgment, line 395) as used with Claude AI, but repository location not stated.
  - **Missing (HARD)**: Analysis and figure-generation scripts (for reproducing Figures 2–6 and Tables S5–S16) not explicitly deposited or linked. Manuscript states scripts exist but does not provide a repository URL or supplementary code archive.

---

## PROTOCOL-PROVENANCE ASSESSMENT

### Delegated Methods

| Method | Citation | Status | Notes |
|--------|----------|--------|-------|
| Sample preparation (digestion, enrichment) | PXD070049 (Van Puyvelde et al., refs 18–19) | Delegated-resolvable | PRIDE accession provided; full protocol in benchmark paper, not in this manuscript. |
| Sage search configuration | Lazear 2023 (ref 21) | Delegated-resolvable | Sage documentation and defaults; specific config in Section S7. |
| DIA-NN search & refinement | Demichev et al. 2020 (ref 23) | Delegated-resolvable | DIA-NN documentation; specific config in Section S7. |
| IonQuant LFQ | Yu et al. 2021 (ref 22) | Delegated-resolvable | Integrated into Sage; methodology in cited paper. |
| MaxLFQ quantification | Cox et al. 2014 (ref 24) | Delegated-resolvable | DIA-NN uses MaxLFQ; methodology in cited paper. |
| timsrust library | Willems & MannLabs (ref 15) | Delegated-resolvable | GitHub repository cited; version 0.4.215 specified. |
| Bruker type-2 analysis.tdf_bin format | Bruker proprietary (not cited) | Delegated-dead | Format specification not cited or referenced. Manuscript states dnoise "writes the Bruker type-2 analysis.tdf_bin encoding with its own encoder" but does not cite the format specification. This is a load-bearing method (native-format compatibility is central to the paper's value). **Unverifiable from manuscript alone.** |

### Deviations from Cited Protocols
- **Sage search**: Manuscript specifies "fully tryptic, allowed two missed cleavages and peptide lengths of 7–30" and "±20 ppm precursor and fragment tolerances." These are stated as applied; no explicit deviation from Sage defaults is noted. ✓
- **DIA-NN**: "two-pass refinement and report" mentioned but not detailed. Delegated to DIA-NN defaults/documentation. ✓
- **Streak filter parameters**: "grid sweep on one homogeneous sample" (Condition A, 15-minute ddaPASEF) to select min_feature_length and max_internal_gap. This is a custom optimization, not a delegated protocol. ✓

---

## SUMMARY OF FINDINGS

### HARD Missing (Blocking Reproducibility)

1. **FDR threshold for Sage searches** — PSM-level or peptide-level FDR cutoff not stated. Manuscript mentions "1% LFQ q-value" but does not clarify whether this is applied at search time or post-hoc.
2. **Bruker type-2 analysis.tdf_bin format specification** — Central to native-format compatibility claim, but no citation or reference provided. Format is proprietary and not publicly documented in the manuscript.
3. **Analysis and figure-generation scripts** — Mentioned as existing but not deposited or linked. Figures 2–6 and Tables S5–S16 cannot be independently regenerated without these scripts.

### SOFT Missing (Recommended but Not Blocking)

1. **Exact FASTA file version/date** — Delegated to PXD070049; resolvable but not verified in manuscript.
2. **Full digestion protocol** — Delegated to PXD070049; resolvable but not verified in manuscript.
3. **Bruker instrument firmware version** — Not stated.
4. **Operating system and version for benchmark workstation** — Not stated.
5. **Specific padding values for edge protection** — Stated as configurable; benchmark values delegated to Table S1 (supplementary).
6. **Whether 6 replicates are biological or technical** — Implied to be biological (standard for benchmark) but not explicitly stated.
7. **Complete Cargo.toml or dependency manifest** — Likely in Zenodo archive but not quoted in manuscript.
8. **DIA-NN two-pass refinement details** — Delegated to DIA-NN documentation.

### Unverifiable (Questions for Authors)

1. **Contents of Table S1** — Referenced but not reproduced in main text. Supplementary tables are acceptable, but the specific parameter values should be confirmed as present in the submitted Supporting Information.
2. **Bruker timsdata library version** — Used by DIA-NN; version not stated.
3. **Frame count per run** — Implied from "thousands of frames" and "27 minutes of acquisition" but not explicitly counted.
4. **Exact PRIDE accession contents** — Manuscript cites PXD070049 as the source of raw data and benchmark definition, but the manuscript does not reproduce the full sample metadata or digestion protocol from that entry.

---

## CONCLUSION

The manuscript provides **strong traceability for most methods** through explicit version numbers, public repositories (PRIDE, GitHub, Zenodo), and detailed parameter tables. However, **three HARD gaps** prevent full independent reproduction:

1. Search FDR thresholds are not explicitly stated.
2. The Bruker native-format specification is not cited or documented.
3. Analysis scripts for figure generation are not deposited.

The **SOFT gaps** are primarily delegations to public repositories (PXD070049, timsrust, DIA-NN) that are resolvable but not verified in the manuscript itself. These are acceptable for a benchmarking study but should be confirmed in revision.