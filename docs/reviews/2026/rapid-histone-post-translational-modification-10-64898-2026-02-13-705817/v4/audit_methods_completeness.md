# Methods Completeness & Reagent Traceability Audit
## Manuscript: "Rapid Histone Post-Translational Modification Analysis Using Alternative Proteases and Tandem Mass Tags"

---

## CROSS-CUTTING ITEMS

### Sample Size & Replication

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **HEK293T experiments: n stated with replication type** | Present | "n = 3 digestion replicates/condition" (MS sample prep); "n = 4/condition" (Figure 2 caption) for comparative analysis | HARD |
| **Rat hippocampal experiments: n stated** | Present | "n = 5" animals; "n = 5 for rat hippocampal samples" (CV assessment); "data represent combined analysis from male rat hippocampi (n = 5)" (Figure 8) | HARD |
| **Distinction: biological vs. technical replicates** | Present | Clearly separated: 3 biological dose groups (0, 3, 10 mM NAM) × 3 technical replicates each for HEK293T; 5 biological animals for hippocampus | HARD |

### Statistical Tests & Error Representation

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Named statistical test for quantitative analysis** | Present | "limma package with empirical Bayes moderated t-statistics"; "cell-means model"; "contrasts tested for 3 mM vs 0 mM and 10 mM vs. 0 mM"; "Benjamini–Hochberg procedure" for multiple testing correction | HARD |
| **Error bars / uncertainty representation** | Present | "Error bars represent standard deviation across n = 4 digestion replicates" (Figure 4A); "Data are presented as means ± standard deviation or medians where appropriate" | HARD |
| **Significance threshold** | Present | "adjusted p < 0.05" (Benjamini–Hochberg corrected) stated throughout quantitative results | HARD |
| **Dose-response correlation metric** | Present | Pearson r reported: "r = 0.803" (Arg-C Ultra, Figure 7B); "r = 0.791" (r-Chymotrypsin, Figure 7D) | HARD |

### Software, Tool & Instrument Versions

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Mass spectrometer model & mode** | Present | "Thermofisher Scientific Fusion Lumos Tribrid Mass Spectrometer"; "electrospray ionization (ESI)"; "positive ion mode"; "High-Energy Collisional Dissociation (HCD)" | HARD |
| **LC system** | Present | "Evosep One nanoLC system"; "custom-packed analytical capillary column (25 cm length, 150 nm ID, Waters BEH C18, 1.7 µm)" | HARD |
| **FragPipe version** | Present | "FragPipe (v24.0)" | HARD |
| **RStudio version** | Present | "RStudio 2025.09.2+, Build 418" | HARD |
| **Skyline version** | Present | "Skyline (v 26.1.0.057 (c07debd50))" | HARD |
| **R package versions** | Partial | "Bioconductor 'impute' package" named; "limma package" named; specific versions NOT stated for limma or impute | SOFT |
| **Thermal cycler model** | Present | "Biorad, MJ Mini" | HARD |
| **Vibrotome model** | Present | "Vibrotome VS1000 (Leica Microsystems)" | HARD |

### Data Availability Statement

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **MS raw data repository** | Present | "MS raw files...deposited to the ProteomeXchange Consortium...via the PRIDE partner repository with the dataset identifier PXD073683" | HARD |
| **Accession number provided** | Present | "PXD073683" | HARD |
| **Supplementary data tables** | Present | "Table S1, S2, S3, S4, S5" referenced; "Sample and Data Relationship Format (SDRF-Proteomics)" and "FragPipe search results" stated as deposited | HARD |

### Code Availability

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Custom R scripts availability** | Present | "The custom R scripts used for data analysis are available at: https://github.com/NataliePTurner/Histone-RIPUP" | HARD |
| **Script scope** | Present | Scripts described as used for "data processing and statistical methods" (RStudio analysis) | HARD |

---

## CONDITIONAL CATEGORIES

### Cell Lines / Primary Cells

**Trigger:** HEK293T cells used in comparative protease experiments and NAM treatment study.

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Cell line source** | Present | "HEK293T cells" named; standard cell line, widely available | HARD |
| **RRID / CVCL identifier** | Missing | No RRID or CVCL number provided | HARD |
| **Authentication (STR)** | Missing | No STR profiling or authentication statement | HARD |
| **Mycoplasma testing** | Missing | No mycoplasma testing mentioned | HARD |
| **Culture media & supplements** | Present | "Dulbecco's Modified Eagle Medium + GlutaMAX™ (DMEM; catalog number 10566016, Gibco™, Thermo Fisher Scientific) supplemented with 1% Penicillin-streptomycin (10,000 IU/mL, catalog number 15140122, Thermo Fisher Scientific) and 10% fetal bovine serum" | SOFT |
| **Culture conditions** | Present | "37 °C and 5% CO₂"; "media changed every 2-3 days"; "80-90% confluency" before splitting | SOFT |

### Model Organisms / In Vivo

**Trigger:** Rat hippocampal tissue used in proof-of-concept RIPUP experiment.

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Species, strain, source** | Present | "Adult male Sprague-Dawley rats"; "Charles River Laboratories, Raleigh, NC" | HARD |
| **Sex & age** | Present | "male"; "446 ± 17.8 g" (weight proxy for age) | HARD |
| **n per group** | Present | "n = 5" animals | HARD |
| **IACUC protocol #** | Present | "IACUC #09-0006" | HARD |
| **Randomization / blinding statement** | Missing | No statement on randomization or blinding in tissue collection or analysis | HARD |
| **Housing conditions** | Present | "temperature- and humidity-controlled room (12 h reverse light cycle)"; "food and water ad libitum" | SOFT |
| **Anesthesia & euthanasia** | Present | "isoflurane (3%)"; "decapitated" | HARD |

---

### Chemicals / Drugs / Dosing

**Trigger:** Nicotinamide (NAM) used as pan-sirtuin inhibitor; multiple proteases and chemical reagents used.

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Nicotinamide (NAM)** | | | |
| — Vendor & catalog # | Present | "Millipore Sigma, catalog number N0636" | HARD |
| — Doses tested | Present | "0 mM NAM", "3 mM", "10 mM" | HARD |
| — Vehicle & final concentration | Present | "complete media supplemented with...NAM"; final concentrations stated (3, 10 mM) | HARD |
| — Treatment schedule | Present | "18 h" incubation after media replacement | HARD |
| **Arg-C Ultra protease** | | | |
| — Vendor & catalog # | Present | "Promega™, Cat number: VA1831" | HARD |
| — Grade | Present | "MS grade" | HARD |
| — Enzyme-to-substrate ratio** | Present | Multiple ratios tested: 1:100, 1:50, 1:10 (stated per experiment in Methods & Table S2) | HARD |
| **r-Chymotrypsin (rChymoselect)** | | | |
| — Vendor & catalog # | Present | "Promega™, Cat Number: CS3332042" | HARD |
| — Grade | Present | "MS grade" | HARD |
| — Enzyme-to-substrate ratio | Present | "1:40 or 1:10" (stated in Methods); Table S2 specifies per condition | HARD |
| **Trypsin Gold** | | | |
| — Vendor & catalog # | Present | "Promega, V5280" | HARD |
| — Enzyme-to-substrate ratio | Present | "1:10" (stated in Methods) | HARD |
| **TMT labeling reagent** | | | |
| — Vendor & catalog # | Present | "Thermo Scientific; cat no 90309" | HARD |
| — Monoisotopic mass | Present | "229.162932 Da" | HARD |
| — Labeling ratio (peptide:TMT) | Present | "1:8" | HARD |
| — Incubation conditions | Present | "1 h at RT"; "final concentration of anhydrous acetonitrile = 44%" | HARD |
| **Propionic anhydride** | | | |
| — Preparation method | Present | "prepared as previously described" with reference to Garcia et al. 2007 (ref 2) | Delegated-resolvable |
| — Concentration / volume | Partial | "50 mM AMBIC pH 8.0" buffer stated; anhydride volume not explicitly stated, but "two rounds" and "three rounds" mentioned | SOFT |
| **Hydroxylamine (quench)** | | | |
| — Concentration | Present | "5% hydroxylamine"; "15 min at RT" | HARD |
| **TCEP** | | | |
| — Concentration | Present | "5 mM TCEP" (in Trypsin + Urea condition) | HARD |
| **Urea** | | | |
| — Concentration | Present | "2 M Urea" or "6 M Urea" (stated per condition in Methods & Table S2) | HARD |

---

### Mass Spectrometry (Proteomics)

**Trigger:** Bottom-up LC-MS/MS proteomics is the core method.

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Instrument & acquisition mode** | Present | "Thermofisher Scientific Fusion Lumos Tribrid"; "DDA" (data-dependent acquisition); "HCD in the Orbitrap" | HARD |
| **Sample prep / digestion** | Present | Detailed in Methods: histone extraction, protease digestion (Arg-C Ultra, r-Chymotrypsin, Trypsin), propionylation or TMT labeling | HARD |
| **Digestion conditions** | Present | Temperature, pH, buffer, enzyme:substrate ratio, incubation time all stated per protease in Methods & Table S2 | HARD |
| **LC method** | Present | "15 spd LC gradient (88 minutes) at 220 nL/min"; column specs given | HARD |
| **MS acquisition parameters** | Present | Full MS: "120K resolution"; "375–1500 m/z"; "profile mode"; MS/MS: "7.5K resolution"; "centroided"; "1.6 m/z isolation window"; "dynamic exclusion 5 s"; "charge states +2 to +7" | HARD |
| **Search engine & version** | Present | "FragPipe (v24.0)" following "HiP-Frag workflow" | HARD |
| **Database & version** | Present | "restricted database containing extracted human or rat histone sequences, contaminants and decoys" (Homo sapiens: 342 sequences, 171 decoys; Rattus norvegicus: 292 entries, 146 decoys; "Cambridge Centre for Proteomics (CCP) cRAP") | HARD |
| **FDR threshold** | Present | "1% FDR at the peptide and PSM level" | HARD |
| **Cleavage specificity** | Present | "Arg-C Ultra...cleave after R"; "r-Chymotrypsin...FYLM (not before P)"; "Trypsin...cleave after R only" (for propionylated) or "KR" (for partial propionylation test) | HARD |
| **Missed cleavages allowed** | Present | "Up to 2 missed cleavages...Arg-C Ultra and Trypsin"; "up to 3 missed cleavages...r-Chymotrypsin" | HARD |
| **Variable modifications** | Present | "Lists of variable modifications and detailed mass offsets are provided in SI Table S1" | Delegated-resolvable (Table S1 in supplement) |
| **Static modifications** | Present | "N-terminal propionylation...static modification for all propionylated samples"; "monoisotopic mass of the intact label (+229.162932 Da)...static modification on peptide N-termini" for TMT | HARD |
| **Mass tolerances** | Partial | "precursor mass tolerance...10 ppm" stated for DDA; fragment tolerance NOT explicitly stated in main text (stated in Figure 6 caption as "20 ppm" for XICs, but general search tolerance not given) | SOFT |
| **Quantification method** | Present | "Label-free quantification (LFQ)"; "match-between-runs (MBR) enabled"; "MaxLFQ disabled" for peptidoform-level quantitation; "histone-level normalization" | HARD |
| **Repository accession** | Present | "ProteomeXchange Consortium...PRIDE partner repository"; "dataset identifier PXD073683" | HARD |
| **Replicates (technical/biological)** | Present | "n = 4 per condition for HEK293T samples; n = 5 for rat hippocampal samples" | HARD |

---

### Histone Extraction Protocol

**Trigger:** Histone extraction is a critical upstream step; delegated to "SI Methods (Histone Extraction)".

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Histone extraction method** | Delegated | "Cells were washed twice with DPBS before proceeding to nuclei isolation and histone extraction as described in SI Methods (Histone Extraction)" | Delegated-unverifiable |
| **Verification** | Unverifiable | Supplementary Methods section is referenced but not provided in the manuscript text. Cannot confirm whether a full, self-contained protocol is present or whether it itself delegates to another reference. | HARD |

---

### Computational Analysis (Data Processing & Statistics)

**Trigger:** Custom R scripts for data processing, statistical testing, and visualization.

| Item | Status | Evidence | Severity |
|------|--------|----------|----------|
| **Dataset version / source** | Present | FragPipe output from MS searches; specific input: "Data resulting from HiP-Frag output" | HARD |
| **Train/val/test split** | N/A | Not applicable; this is observational/quantitative analysis, not ML | — |
| **Algorithm / method** | Present | "k-nearest neighbors (kNN, k = 10)" for imputation; "limma package with empirical Bayes moderated t-statistics"; "cell-means model" | HARD |
| **Hyperparameters** | Present | "k = 10" for kNN; "Benjamini–Hochberg procedure" for p-value adjustment | HARD |
| **Library versions** | Partial | "Bioconductor 'impute' package"; "limma package"; R version (RStudio 2025.09.2) stated, but specific versions of limma and impute NOT given | SOFT |
| **Random seed / reproducibility** | Missing | No random seed set or seed-averaging statement for kNN imputation | SOFT |
| **Code availability** | Present | "https://github.com/NataliePTurner/Histone-RIPUP" | HARD |
| **Imputation criteria** | Present | "k = 10; Bioconductor 'impute' package"; "restricted to dose groups where at least 2 of 3 replicates had measured values"; "Groups with 0 or 1 measured replicates were left as missing" | HARD |
| **Missing data handling** | Present | Clearly stated: "missing at random" assumption; kNN applied only to genuine single-replicate gaps | HARD |

---

## PROTOCOL PROVENANCE & DELEGATION

### Histone Extraction

| Reference | Status | Severity |
|-----------|--------|----------|
| "as described in SI Methods (Histone Extraction)" | Unverifiable | HARD |
| **Issue:** The supplementary methods section is not included in the provided manuscript text. The audit cannot confirm whether a full protocol is present in the supplement or whether it itself delegates to another citation. This is a load-bearing method (all downstream work depends on it). | — | — |
| **Resolution needed:** Confirm that SI Methods contains a complete, self-contained histone extraction protocol, or provide the full text. |

### Propionic Anhydride Preparation

| Reference | Status | Severity |
|-----------|--------|----------|
| "The propionylation reagent was prepared as previously described" → Garcia et al. 2007 (ref 2) | Delegated-resolvable | SOFT |
| **Evidence:** Garcia et al. 2007 is a published Nature Protocols paper (DOI: 10.1038/nprot.2007.106), which is a methods-focused venue and plausibly contains the full protocol. The reference is resolvable and specific. | — | — |

### HiP-Frag Workflow

| Reference | Status | Severity |
|-----------|--------|----------|
| "MS raw files were processed in FragPipe (v24.0) following the recommended guidelines for the HiP-Frag workflow, with some modifications" → Vai et al. 2025 (ref 20) | Delegated-resolvable | SOFT |
| **Evidence:** Vai et al. 2025 is cited as "Breaking Boundaries in Histone Modification MS-Based Detection: A Tailored Search Strategy for Unrestricted Identification of Novel Epigenetic Marks" in Molecular & Cellular Proteomics. This is a methods paper and plausibly contains the workflow. The reference is specific and resolvable. | — | — |
| **Deviation noted:** "with some modifications" — the manuscript does NOT explicitly state what modifications were made. The search parameters are detailed (cleavage specificity, missed cleavages, variable modifications in Table S1), but the specific deviations from Vai et al.'s published workflow are not enumerated. | — | SOFT |

### Rat Tissue Preparation (Vibrotome Slicing)

| Reference | Status | Severity |
|-----------|--------|----------|
| Detailed in-text: "A Vibrotome VS1000 (Leica Microsystems) was used to cut 300 µm coronal slices containing hippocampus (AP: -2.00 to -3.25 from bregma)." | Self-contained | — |
| **Status:** Sufficient detail provided; no delegation. | — | — |

---

## SUMMARY TABLE: HARD MISSING ITEMS

| Category | Item | Status | Impact |
|----------|------|--------|--------|
| Cell Lines | HEK293T RRID / CVCL | Missing | Cannot trace exact cell line identity |
| Cell Lines | HEK293T STR authentication | Missing | Cannot verify cell line authenticity |
| Cell Lines | Mycoplasma testing | Missing | Cannot confirm absence of contamination |
| Model Organisms | Randomization / blinding statement (rat tissue) | Missing | Cannot assess bias in tissue collection/analysis |
| Histone Extraction | Full protocol text (delegated to SI Methods) | Unverifiable | Cannot confirm completeness; load-bearing method |
| Mass Spec | Fragment mass tolerance (general search param) | Soft missing | Stated in one figure caption (20 ppm) but not in main search parameters |

---

## SUMMARY TABLE: SOFT MISSING ITEMS

| Category | Item | Status | Impact |
|----------|------|--------|--------|
| Software | R package versions (limma, impute) | Missing | Reproducibility of statistical analysis slightly reduced |
| Computational | Random seed for kNN imputation | Missing | Imputation results not fully reproducible |
| Chemicals | Propionic anhydride volume per round | Partial | Protocol delegated; volume not stated in main text |
| HiP-Frag | Specific modifications from Vai et al. workflow | Unspecified | "With some modifications" stated but not enumerated |

---

## UNVERIFIABLE ITEMS REQUIRING AUTHOR CLARIFICATION

1. **Histone Extraction Protocol (SI Methods):** The full text of the supplementary methods section is not provided in the manuscript. Confirm that SI Methods contains a complete, self-contained protocol for histone extraction, or provide the text.

2. **HiP-Frag Workflow Modifications:** The manuscript states "with some modifications" to the Vai et al. HiP-Frag workflow but does not enumerate them. Clarify which specific parameters or steps deviate from the published workflow.

3. **Fragment Mass Tolerance (General):** Fragment ion mass tolerance is stated as "20 ppm" in Figure 6 caption (for XIC verification) but is not explicitly stated as a general search parameter in the Methods. Confirm the fragment tolerance used in FragPipe searches.

---

## OVERALL ASSESSMENT

**Completeness Status:** The manuscript provides **strong traceability for most reagents and instruments** (proteases, MS equipment, software versions, cell culture media, dosing). **Critical gaps exist in cell line authentication and model organism blinding**, and **the histone extraction protocol is delegated without verification**. The mass spectrometry methods are well-documented with clear FDR, modification, and quantification parameters. Statistical methods are named and thresholds stated. Data and code are deposited with accessions.

**Reproducibility Risk:** A competent lab could **repeat the MS analysis and statistical testing** given the detailed search parameters and code availability. However, **upstream histone extraction and cell line identity cannot be independently verified** from the manuscript alone, and **rat tissue collection bias cannot be assessed** due to missing randomization/blinding statement.