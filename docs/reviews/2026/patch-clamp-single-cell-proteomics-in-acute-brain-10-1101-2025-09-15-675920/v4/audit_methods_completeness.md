# Methods Completeness & Reagent Traceability Audit
## Patch-Clamp Single-Cell Proteomics in Acute Brain Slices

---

## CROSS-CUTTING ITEMS

### Sample Size & Replication
- **Status: PRESENT (with caveats)**
  - n=12 neurons total explicitly stated in Results ("Comprehensive Neuron Retrieval" section and Figure 5A).
  - n=3 neurons for gigaseal-preservation study (Figure 3D correlation analysis).
  - n=6 neurons for in situ recordings vs. protein identifications analysis (Figure 5C–D).
  - What n represents: individual neurons (biological replicates), not technical replicates.
  - **CAVEAT (SOFT)**: No power calculation or justification for sample size provided. Authors acknowledge "limited sample size" in Limitations section but do not justify why n=12 is adequate for exploratory work or state whether this was predetermined.

### Statistical Tests & Error Representation
- **Status: PRESENT (with gaps)**
  - Gigaseal-preserved correlation (Figure 3D): F-statistic, p-value, adjusted R², regression equation provided. ✓
  - In situ recordings vs. protein IDs (Figure 5C–D): "p > 0.05, n=6" stated; no F or R² given. ✓ (though minimal)
  - SynGO enrichment: Q-value < 0.05 threshold stated; no multiple-testing correction method named explicitly (SOFT).
  - PCA (Figure 6A): method not specified; no variance explained reported (SOFT).
  - **HARD MISSING**: Error bars on figures (Figures 3C ladder plots, 4A action potentials) — no statement of what they represent (SD/SEM/CI) or whether they are present at all.

### Software, Tool & Instrument Versions
- **Status: MOSTLY PRESENT**
  - **Electrophysiology**: Multiclamp 700B amplifier, Digidata 1440A, pClamp10 (version not stated; SOFT). NeuroExpress v19.4.09 ✓
  - **Mass spectrometry**: Orbitrap Astral (instrument model ✓); Vanquish Neo UHPLC (✓); IonOpticks Aurora XS column (✓).
  - **Bioinformatics**:
    - DIA-NN v1.8.1 ✓
    - UniProt Mus musculus reference proteome (download date: 2024; SOFT: no specific build/version number given)
    - R 4.3.1 ✓
    - Packages: ComplexHeatmap, ggplot2, UpSetR (versions NOT stated; SOFT)
    - SynGO (no version stated; SOFT)
  - **HARD MISSING**: pClamp10 version number.
  - **SOFT MISSING**: R package versions; SynGO version/download date; UniProt build identifier.

### Data Availability
- **Status: PRESENT**
  - Raw MS data and search files: ProteomeXchange (PXD068359) and MassIVE (MSV000099156) ✓
  - Supplementary tables (protein-level DIA-NN output, SynGO output): stated as available in Supporting Information ✓
  - Videos of patch-SCP attempts: Zenodo (DOI: 10.5281/zenodo.18189812) ✓
  - Custom analysis scripts: GitHub repository URL provided (https://github.com/LarryThePharmacologist) ✓

### Code Availability
- **Status: PRESENT**
  - Custom scripts for figure generation and SynGO-based analysis: GitHub repository cited ✓
  - **SOFT MISSING**: No statement of license, documentation, or whether repository is currently public/accessible.

---

## CONDITIONAL CATEGORIES

### Model Organisms / In Vivo (TRIGGERED: acute brain slices from rats)

#### HARD Items:
- **Species, strain, source**: Wistar rats, Charles River ✓
- **Age**: 75 days ✓
- **Sex**: NOT STATED ✗ (HARD MISSING)
- **n per group**: n=12 neurons total; no breakdown by sex or other grouping ✓ (stated but not stratified)
- **IACUC protocol #**: Protocol no. 09-0006 ✓
- **Randomization/blinding statement**: NOT STATED ✗ (HARD MISSING — no statement that neuron selection was random or that analysis was blinded)
- **Genotype/background**: Wild-type (implied); not explicitly stated ✗ (SOFT MISSING)

#### SOFT Items:
- **Housing**: NOT STATED (SOFT MISSING)
- **Power justification**: NOT PROVIDED (SOFT MISSING); authors acknowledge "limited sample size" but do not justify it prospectively.

---

### Chemicals / Drugs / Dosing (TRIGGERED: internal solution, cutting solution, aCSF, reagents)

#### HARD Items:

**Cutting solution** (ice-cold high-sucrose):
- Sucrose 206 mM ✓
- KCl 2.5 mM ✓
- CaCl₂ 0.5 mM ✓
- MgCl₂ 7 mM ✓
- NaH₂PO₄ 1.2 mM ✓
- NaHCO₃ 26 mM ✓
- Glucose 5 mM ✓
- HEPES 5 mM ✓
- **Vendor/catalog #**: NOT STATED (SOFT MISSING)

**aCSF** (95% O₂/5% CO₂ equilibrated):
- NaCl 130 mM ✓
- KCl 3.5 mM ✓
- NaH₂PO₄ 1.25 mM ✓
- MgSO₄·7H₂O 1.5 mM ✓
- CaCl₂ 2.0 mM ✓
- NaHCO₃ 24 mM ✓
- Glucose 10 mM ✓
- **Vendor/catalog #**: NOT STATED (SOFT MISSING)

**Internal solution** (patch pipette):
- KGluconate 145 mM ✓
- EGTA 0.5 mM ✓
- MgCl₂ 2 mM ✓
- HEPES 10 mM ✓
- Mg-ATP 2 mM ✓
- Na-GTP 0.2 mM ✓
- **Vendor/catalog #**: NOT STATED (SOFT MISSING)

**Sample processing reagents**:
- n-dodecyl-β-D-maltoside (DDM) 0.02% in UHPLC-grade water ✓ (concentration and vehicle stated)
- **Vendor/catalog #**: NOT STATED (SOFT MISSING)
- Sequencing-grade Trypsin, 7 ng per sample, Promega ✓
- Formic acid 0.1% ✓
- **Vendor/catalog #for formic acid**: NOT STATED (SOFT MISSING)

**Negative pressure during retrieval**: −50 to −140 mmHg (range stated; SOFT: no justification for range or how it was optimized per neuron).

#### SOFT Items:
- Vendor/catalog # for all reagents: MOSTLY MISSING (only Promega trypsin identified)
- Preparation/storage conditions for solutions: NOT STATED

---

### Mass Spectrometry (Proteomics) (TRIGGERED: DIA-MS analysis)

#### HARD Items:

**Instrument & acquisition**:
- Instrument: Orbitrap Astral ✓
- Acquisition mode: DIA (data-independent acquisition) ✓
- FAIMS Pro with single compensation voltage (CV = −50) ✓
- Survey scans: 240,000 resolution at m/z 200, 400–1000 m/z range ✓
- DIA windows: 20 m/z wide with overlapping edges ✓
- MS1 AGC target: 800%, max injection time 50 ms ✓
- Fragmentation: HCD, NCE 25 ✓

**Sample preparation/digestion**:
- Lysis: 0.02% DDM in UHPLC-grade water ✓
- Digestion: 7 ng sequencing-grade Trypsin (Promega), 37°C, 2 hours ✓
- Quenching: 2 µL 0.1% formic acid ✓
- **HARD MISSING**: No statement of protein quantification before digestion (e.g., BCA, Bradford). Cannot verify that 7 ng trypsin was appropriate for unknown protein input.
- **HARD MISSING**: No mention of sample cleanup, desalting, or concentration steps between digestion and LC-MS.

**Chromatography**:
- Column: 25 cm × 75 µm IonOpticks Aurora XS with integrated emitter ✓
- Gradient: 36-minute gradient at 400 nL/min ✓
- **HARD MISSING**: Solvent composition (A/B), gradient profile (% B vs. time), temperature not stated.
- **HARD MISSING**: Column lot/batch number not stated.

**Search engine & database**:
- Search engine: DIA-NN v1.8.1 ✓
- Mode: library-free ✓
- Match-between-runs: enabled ✓
- Database: UniProt Mus musculus reference proteome (downloaded 2024) ✓
- **HARD MISSING**: Specific UniProt release/build number (e.g., 2024-01, 2024-02).

**Search parameters**:
- Variable modification: oxidation ✓
- Missed cleavages: up to 2 ✓
- Decoy generation: reversed-sequence ✓
- **HARD MISSING**: Precursor mass tolerance (ppm or Da).
- **HARD MISSING**: Fragment mass tolerance.
- **HARD MISSING**: Enzyme specificity (assumed trypsin; not explicitly stated in search params).

**FDR & filtering**:
- FDR threshold: 1% at precursor and protein-group level ✓
- Retention: protein groups in DIA-NN's report.pg_matrix.tsv ✓
- **SOFT MISSING**: How many peptides per protein required for identification (minimum peptide count).

**Quantification**:
- Method: MaxLFQ (DIA-NN implementation) ✓
- **SOFT MISSING**: Normalization method (e.g., median, quantile).

**Data repository**:
- ProteomeXchange: PXD068359 ✓
- MassIVE: MSV000099156 ✓

#### SOFT Items:
- Solvent composition and gradient profile: NOT STATED
- Column lot/batch: NOT STATED
- Precursor/fragment mass tolerances: NOT STATED
- Minimum peptide count per protein: NOT STATED
- Quantification normalization: NOT STATED

---

### Genomics / Sequencing / Omics (TRIGGERED: DIA-MS proteomics analysis)

#### HARD Items:
- **Platform & mode**: Orbitrap Astral, DIA ✓
- **Library-prep equivalent**: DIA-NN library-free mode ✓
- **Depth/coverage**: Total protein identifications per neuron reported (range ~1400–2300 proteins; Figure 5A) ✓; no statement of peptide-level depth or coverage uniformity.
- **Reference genome/database**: UniProt Mus musculus (2024 download) ✓; **HARD MISSING**: specific build/release number.
- **Alignment/analysis tools WITH versions**: DIA-NN v1.8.1 ✓; R 4.3.1 ✓; SynGO (version NOT stated); ComplexHeatmap, ggplot2, UpSetR (versions NOT stated).
- **Repository accession**: PXD068359, MSV000099156 ✓

#### SOFT Items:
- QC thresholds: 1% FDR stated; no other QC metrics (e.g., mass accuracy, retention-time prediction accuracy) reported.
- Batch handling: NOT DISCUSSED (SOFT MISSING); no statement of whether neurons were processed in batches or randomized order.

---

### Microscopy / Imaging (TRIGGERED: DIC imaging during patch-clamp and retrieval)

#### HARD Items:
- **Instrument model**: NOT STATED ✗ (HARD MISSING — microscope used for DIC imaging not identified)
- **Objective + NA + detector + settings**: NOT STATED ✗ (HARD MISSING)
- **Fluorophore ↔ marker panel**: Not applicable (DIC only, no fluorescence).
- **Analysis/gating software WITH version**: NOT APPLICABLE (qualitative visual assessment only; no automated image analysis).
- **Full gating strategy**: NOT APPLICABLE.

#### SOFT Items:
- Magnification, working distance: NOT STATED

**Videos (Supporting Information)**:
- Four videos of soma retrieval provided (Zenodo DOI: 10.5281/zenodo.18189812) ✓
- **SOFT MISSING**: Video resolution, frame rate, duration not stated in manuscript.

---

### Computational / ML / Modeling (TRIGGERED: PCA, GO enrichment, correlation analysis)

#### HARD Items:

**PCA (Figure 6A)**:
- **Dataset**: All 12 neurons' proteomes (protein-level DIA-NN output) ✓
- **Algorithm**: PCA (standard; no custom implementation stated) ✓
- **Hyperparameters**: NOT STATED (e.g., scaling method, number of components retained, centering) ✗ (HARD MISSING)
- **Software/version**: R 4.3.1 ✓; specific package (e.g., prcomp, FactoMineR) NOT STATED ✗ (HARD MISSING)
- **Training/validation split**: NOT APPLICABLE (unsupervised exploratory analysis).
- **Code availability**: GitHub repository cited ✓

**Correlation analysis (Figures 3D, 5C–D)**:
- **Dataset**: n=3 (gigaseal-preserved) and n=6 (in situ recordings) neurons ✓
- **Algorithm**: Linear regression (log-transformed capacitance vs. protein IDs; Figure 3D) ✓
- **Hyperparameters**: None (standard linear model).
- **Software**: R (version 4.3.1 stated for general analysis; specific function not named) ✓
- **Code availability**: GitHub repository cited ✓

**Gene Ontology / SynGO enrichment (Figures 4B–C, 6B, S2–S3)**:
- **Dataset**: Per-neuron protein lists (detected/not detected after 1% FDR filtering) ✓
- **Algorithm**: GSEA (Gene Set Enrichment Analysis) ✓
- **Database**: SynGO (manually curated synaptic GO ontology) ✓
- **Hyperparameters**: Q-value < 0.05 threshold ✓; **HARD MISSING**: GSEA algorithm variant (e.g., weighted, unweighted), permutation count, ranking metric.
- **Software/version**: SynGO (version NOT STATED) ✗; R 4.3.1 ✓; packages ComplexHeatmap, ggplot2, UpSetR (versions NOT STATED) ✗
- **Code availability**: GitHub repository cited ✓

#### SOFT Items:
- PCA: variance explained per component NOT REPORTED
- GSEA: permutation count, ranking metric NOT STATED
- Batch effects: NOT DISCUSSED
- Random seeds: NOT STATED (not applicable for deterministic methods, but relevant for any stochastic steps in GSEA or PCA initialization)

---

### Electrophysiology (TRIGGERED: patch-clamp recordings)

#### HARD Items:

**Recording configuration**:
- Whole-cell patch-clamp in acute brain slices ✓
- Current-clamp and voltage-clamp modes ✓
- Amplifier: Multiclamp 700B ✓
- Digitizer: Digidata 1440A ✓
- Software: pClamp10 (version NOT STATED) ✗ (HARD MISSING)

**Electrode preparation**:
- Patch pipettes: 3–6 MΩ resistance ✓
- Internal solution composition: fully specified ✓
- **HARD MISSING**: Pipette pulling parameters (puller model, heat/pull/velocity settings) not stated; cannot reproduce electrode fabrication.

**Stimulation protocol**:
- Current-clamp step protocol: 500 ms hyperpolarizing and depolarizing steps in 5 or 10 pA increments ✓
- Holding potential: −70 mV ✓
- **SOFT MISSING**: Temperature during recording not explicitly stated (implied room temperature for some, 37°C for initial incubation).

**Data analysis**:
- Software: NeuroExpress v19.4.09 ✓
- Passive properties extracted: capacitance (C), membrane resistance (RM), resting membrane potential (VM), membrane time constant (τM) ✓
- **SOFT MISSING**: Specific equations or fitting procedures for extracting these parameters not detailed (delegated to NeuroExpress reference [15]).

**Soma retrieval**:
- Negative pressure: −50 to −140 mmHg ✓
- **SOFT MISSING**: Criteria for adjusting pressure within this range not specified; optimization procedure not described.

#### SOFT Items:
- Pipette pulling parameters: NOT STATED
- Recording temperature: NOT EXPLICITLY STATED (implied room temperature; 37°C for initial incubation)
- Sampling rate/filter frequency: NOT STATED

---

### Protocol Provenance (Delegated Methods)

**Electrophysiology protocol**: "Acute brain slices and electrophysiological recordings were performed as previously described [10, 26–31]."

- **References cited**: [10] Patel et al. 2024 (Neurobiol Stress); [26] Rodriguez et al. 2022 (Int J Mol Sci); [27] Vlkolinsky et al. 2024 (Neurobiol Dis); [28] Varodayan et al. 2023 (Brain Behav Immun); [29] Athanason et al. 2023 (Neurobiol Stress); [30] Anjos-Santos et al. 2025 (in press); [31] Guo et al. 2025 (Nature).
- **Status**: DELEGATED-RESOLVABLE (all references appear to be published or in-press; DOIs/PMIDs resolvable in principle). ✓
- **Caveat**: Manuscript does not state which specific reference contains the full protocol or whether all six references describe identical procedures. Readers would need to consult multiple papers.
- **Deviation statement**: "Briefly, rats were anesthetized with isoflurane before cervical dislocation and surgical brain isolation. Coronal mPFC slices (300 µm) were prepared..." — this provides some detail, reducing reliance on the cited protocol. ✓

**Passive property analysis**: "NeuroExpress software (version 19.4.09.) developed and provided by A. Szücs was used for analysis [15]."

- **Reference [15]**: Szücs, A. NeuroExpress program for analyzing patch-clamp data. ResearchGate, 2022.
- **Status**: DELEGATED-RESOLVABLE but UNVERIFIABLE from manuscript alone (ResearchGate is not a peer-reviewed repository; no DOI or PMID; cannot confirm contents without accessing ResearchGate directly). ⚠️
- **Severity**: SOFT (the software is named and versioned; a competent lab could locate it, but the reference is non-standard).

**SynGO analysis**: "Gene set enrichment analyses were performed on gene lists derived from DIA-NN's protein-level output. For SynGO analysis, proteins were annotated based on gene symbols and GSEA filtering was performed under stringent conditions."

- **Reference [16]**: Koopmans et al. 2019 (Neuron, 103(2): 217–234.e4).
- **Status**: DELEGATED-RESOLVABLE (peer-reviewed publication; DOI resolvable). ✓
- **Caveat**: Manuscript does not specify which GSEA algorithm variant (weighted/unweighted), permutation count, or ranking metric was used. "Stringent conditions" is vague.

**Ion channel/GPCR/transporter annotation**: "Ion channel, GPCR, and transporter annotation lists were generated using curated gene families from SynGO [16] and IUPHAR-DB [17, 18]."

- **References [17, 18]**: Alexander et al. 2019 and 2023 (British Journal of Pharmacology).
- **Status**: DELEGATED-RESOLVABLE (peer-reviewed; DOI resolvable). ✓
- **Caveat**: Manuscript does not state how lists were curated (e.g., which gene families were selected, whether all entries were used or filtered by expression level/tissue specificity).

---

## SUMMARY TABLE

| Category | Item | Status | Severity | Notes |
|----------|------|--------|----------|-------|
| **Cross-cutting** | Sample size n & what it represents | Present | — | n=12 neurons; no power justification (SOFT) |
| | Statistical tests & error representation | Partial | HARD | Error bars on figures not explained; SynGO Q-value method not named |
| | Software/tool versions | Partial | HARD | pClamp10 version missing; R package versions missing; SynGO version missing |
| | Data availability | Present | — | ProteomeXchange, MassIVE, Zenodo, GitHub all cited |
| | Code availability | Present | — | GitHub repository cited |
| **Model organisms** | Species, strain, source, age | Present | — | Wistar rats, Charles River, 75 days ✓ |
| | Sex | Missing | HARD | Not stated ✗ |
| | IACUC protocol # | Present | — | 09-0006 ✓ |
| | Randomization/blinding | Missing | HARD | Not stated ✗ |
| | Genotype/background | Missing | SOFT | Wild-type implied but not explicit |
| | Housing | Missing | SOFT | Not stated |
| | Power justification | Missing | SOFT | Not provided |
| **Chemicals/drugs** | Cutting solution composition | Present | — | All components & concentrations stated ✓ |
| | aCSF composition | Present | — | All components & concentrations stated ✓ |
| | Internal solution composition | Present | — | All components & concentrations stated ✓ |
| | Vendor/catalog # for reagents | Missing | SOFT | Only Promega trypsin identified; others missing |
| | Sample prep reagents (DDM, formic acid) | Partial | SOFT | Concentrations stated; vendors missing |
| **Mass spectrometry** | Instrument & acquisition mode | Present | — | Orbitrap Astral, DIA, all key params stated ✓ |
| | Sample prep/digestion | Partial | HARD | Lysis, digestion, quenching stated; protein quantification method missing; no desalting/cleanup step described |
| | Chromatography | Partial | HARD | Column type & gradient time stated; solvent composition & profile missing; column lot missing |
| | Search engine & database | Partial | HARD | DIA-NN v1.8.1 ✓; UniProt 2024 ✓; specific build number missing |
| | Search parameters | Partial | HARD | Modifications & missed cleavages stated; mass tolerances missing; enzyme specificity not explicit |
| | FDR & filtering | Present | — | 1% FDR at precursor & protein level ✓ |
| | Quantification method | Partial | SOFT | MaxLFQ stated; normalization method missing |
| | Repository accession | Present | — | PXD068359, MSV000099156 ✓ |
| **Genomics/omics** | Platform & mode | Present | — | Orbitrap Astral, DIA ✓ |
| | Reference database | Partial | HARD | UniProt Mus musculus 2024 ✓; specific build missing |
| | Analysis tools & versions | Partial | HARD | DIA-NN v1.8.1 ✓; R 4.3.1 ✓; SynGO version missing; R package versions missing |
| | Repository accession | Present | — | PXD068359, MSV000099156 ✓ |
| | QC thresholds | Partial | SOFT | 1% FDR stated; other QC metrics missing |
| | Batch handling | Missing | SOFT | Not discussed |
| **Microscopy** | Instrument model | Missing | HARD | DIC microscope not identified ✗ |
| | Objective, NA, detector, settings | Missing | HARD | Not stated ✗ |
| | Video metadata | Missing | SOFT | Resolution, frame rate, duration not stated |
| **Computational** | PCA: hyperparameters | Missing | HARD | Scaling, centering, component count not stated ✗ |
| | PCA: software/package | Missing | HARD | R package name not stated ✗ |
| | Correlation analysis: algorithm & software | Present | — | Linear regression, R ✓ |
| | GSEA/SynGO: algorithm variant | Missing | HARD | Weighted/unweighted, permutation count, ranking metric not stated ✗ |
| | GSEA/SynGO: software versions | Missing | HARD | SynGO version missing; R package versions missing ✗ |
| | Code availability | Present | — | GitHub repository cited ✓ |
| **Electrophysiology** | Recording configuration | Present | — | Whole-cell, current/voltage clamp, amplifier, digitizer ✓ |
| | Software version | Missing | HARD | pClamp10 version not stated ✗ |
| | Electrode parameters | Missing | HARD | Pipette pulling parameters not stated ✗ |
| | Stimulation protocol | Present | — | Step protocol, holding potential ✓ |
| | Data analysis software | Present | — | NeuroExpress v19.4.09 ✓ |
| | Recording temperature | Missing | SOFT | Not explicitly stated |
| | Sampling rate/filter | Missing | SOFT | Not stated |
| **Protocol provenance** | Electrophysiology delegation | Delegated-resolvable | — | References [10, 26–31] cited; multiple papers; no single definitive source |
| | NeuroExpress reference | Delegated-resolvable | SOFT | ResearchGate (non-standard); no DOI/PMID |
| | SynGO/GSEA delegation | Delegated-resolvable | — | Peer-reviewed reference [16] ✓; specifics (algorithm variant, permutation count) not stated |
| | Ion channel annotation delegation | Delegated-resolvable | — | Peer-reviewed references [16–18] ✓; curation criteria not stated |

---

## CRITICAL GAPS (HARD MISSING)

1. **Rat sex** — not stated; essential for reproducibility and biological interpretation.
2. **Randomization/blinding statement** — no mention of whether neuron selection or analysis was randomized or blinded.
3. **Microscope instrument model** — DIC imaging used throughout; instrument not identified.
4. **Microscope objective, NA, detector, settings** — cannot reproduce imaging.
5. **Protein quantification method** — no BCA, Bradford, or other assay mentioned before digestion; cannot verify that 7 ng trypsin was appropriate.
6. **Sample cleanup/desalting** — no mention of post-digestion cleanup or concentration steps.
7. **LC-MS solvent composition & gradient profile** — only gradient time (36 min) and flow rate (400 nL/min) stated; A/B solvents and % B vs. time missing.
8. **Precursor & fragment mass tolerances** — not stated in search parameters.
9. **UniProt build/release number** — only "2024" given; specific version (e.g., 2024-01) missing.
10. **pClamp10 version** — software used but version not stated.
11. **Pipette pulling parameters** — puller model, heat/pull/velocity settings not stated; cannot reproduce electrode fabrication.
12. **PCA hyperparameters** — scaling, centering, number of components retained not stated.
13. **PCA software package** — R function/package name not stated (e.g., prcomp, FactoMineR).
14. **GSEA algorithm variant & parameters** — weighted/unweighted, permutation count, ranking metric not stated.
15. **SynGO version** — no version or download date given.
16. **R package versions** — ComplexHeatmap, ggplot2, UpSetR versions not stated.

---

## SOFT MISSING (RECOMMENDED BUT NOT BLOCKING)

- Vendor/catalog # for most reagents (cutting solution, aCSF, internal solution, DDM, formic acid).
- Genotype/background of rats (wild-type implied but not explicit).
- Housing conditions for rats.
- Power justification for sample size (n=12).
- Recording temperature (implied room temperature; not explicit).
- Sampling rate and filter frequency for electrophysiology.
- Pipette pulling parameters (alternative: cite a standard protocol).
- Column lot/batch number.
- Minimum peptide count per protein identification.
- Quantification normalization method (e.g., median, quantile).
- QC metrics beyond 1% FDR (e.g., mass accuracy, retention-time prediction accuracy).
- Batch handling / randomization of sample processing order.
- PCA variance explained per component.
- Video metadata (resolution, frame rate, duration).
- GSEA permutation count and ranking metric.
- Specific GSEA algorithm variant (weighted/unweighted).
- Ion channel/GPCR/transporter curation criteria (which gene families selected, filtering by expression/tissue specificity).

---

## UNVERIFIABLE (QUESTIONS FOR AUTHORS)

1. **NeuroExpress reference [15]** — ResearchGate is not a standard scientific repository. Can authors provide a DOI, PMID, or institutional repository link, or confirm that the software is publicly available with documentation?
2. **Electrophysiology protocol references [10, 26–31]** — which of these six papers contains the definitive protocol for slice preparation and recording? Are all six identical, or are there variations?
3. **UniProt 2024 build** — which specific release (e.g., 2024-01, 2024-02, 2024-03) was used? This affects reproducibility of peptide-to-protein mapping.
4. **GitHub repository** — is the repository currently public and accessible? Is there a specific commit hash or release tag that corresponds to this manuscript's analysis?

---

## OVERALL ASSESSMENT

**Completeness**: ~65–70% for methods required to reproduce the work.

**Blocking issues**: 
- Rat sex not stated (HARD).
- Microscope not identified (HARD).
- Protein quantification method missing (HARD).
- LC-MS solvent/gradient profile missing (HARD).
- Mass tolerances missing (HARD).
- Pipette pulling parameters missing (HARD).
- PCA hyperparameters & software package missing (HARD).
- GSEA algorithm details missing (HARD).
- Multiple software versions missing (pClamp10, SynGO, R packages) (HARD).

**Non-blocking but significant gaps**:
- Randomization/blinding not stated.
- Sample cleanup/desalting not described.
- UniProt build number not specified.
- Recording temperature not explicit.
- Power justification absent.

A competent lab could likely reproduce the mass spectrometry and bioinformatic analysis (data and code are deposited), but **electrophysiology and microscopy details are insufficient for independent replication**. The patch-clamp protocol is delegated to six prior papers without clear indication of which is primary, and critical details (rat sex, electrode fabrication, microscope specs) are missing.