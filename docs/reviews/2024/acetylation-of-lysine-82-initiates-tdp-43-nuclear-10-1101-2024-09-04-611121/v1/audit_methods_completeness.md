# Methods Completeness & Reagent Traceability Audit

## Triggered Categories

The following checklist categories are triggered by content in the manuscript:

1. **Antibodies/immunodetection** (WB, IF, IP, ELISA)
2. **Cell lines/primary cells**
3. **Human subjects/clinical** (postmortem tissue)
4. **Chemicals/drugs/dosing**
5. **Oligos/plasmids/constructs**
6. **Mass spectrometry** (proteomics)
7. **Microscopy/imaging**
8. **Cross-cutting items** (sample size, statistics, software, data availability)

---

## Findings by Category

### 1. Antibodies/Immunodetection

**Trigger:** Extensive use of WB, IF, IP, ELISA, and co-IP throughout.

| Antibody/Application | Vendor | Catalog # | Clone | RRID | Dilution | Host/Clonality | Status |
|---|---|---|---|---|---|---|---|
| Primary antibodies (WB, IF, IP) | Supplementary Table S3 referenced | — | — | — | Stated in S3 | — | **Missing** |
| Anti-6×His-HRP | Proteintech | HRP-66005 | — | — | 1:4000 | — | **Present** |
| Anti-rabbit-HRP | Proteintech | SA00001-2 | 1:4000 | — | — | — | **Present** |
| TDP-43 acetylation (K82) antibodies (3 polyclonal) | Sanyou Inc. | — | — | — | Not stated | Rabbit polyclonal | **Missing** |
| Lamin B1 (loading control) | — | — | — | — | — | — | **Unverifiable** |
| GAPDH (loading control) | — | — | — | — | — | — | **Unverifiable** |
| FUS antibody (co-IP) | — | — | — | — | — | — | **Unverifiable** |
| Importin-α1, importin-α5, importin-β2 (co-IP) | — | — | — | — | — | — | **Unverifiable** |

**Issues:**

- **HARD missing:** Supplementary Table S3 is referenced for antibody details but is not provided in the manuscript text. The three custom polyclonal antibodies against ac-TDP-43(K82) lack vendor catalog numbers, RRIDs, and working dilutions for WB/IF applications.
- **HARD missing:** Loading control antibodies (Lamin B1, GAPDH) lack vendor, catalog #, and dilution information.
- **HARD missing:** Antibodies used in co-IP experiments (TDP-43, FUS, importins) lack complete traceability (vendor, catalog #, dilution, host species/clonality).
- **SOFT missing:** No RRID identifiers provided for any antibody.

---

### 2. Cell Lines/Primary Cells

**Trigger:** iPSC-derived cortical neurons, SH-SY5Y cells, HEK293T cells.

| Cell Line/Source | RRID/CVCL | Authentication (STR) | Mycoplasma Testing | Media/Supplements | Status |
|---|---|---|---|---|---|
| iPSC (WTC11, NGN2-inducible) | — | — | — | Specified (E8, N2, i3Neuron) | **Unverifiable** |
| SH-SY5Y | ATCC CRL-2266 | — | — | DMEM/F12 + 10% FBS | **Partial** |
| HEK293T | ATCC CRL-11268 | — | — | DMEM + 10% FBS | **Partial** |

**Issues:**

- **HARD missing:** iPSC source stated as "kind gift of Michael Ward" with no RRID, authentication status, or mycoplasma testing reported.
- **HARD missing:** No STR authentication or mycoplasma testing reported for any cell line.
- **SOFT present:** Media and supplements are specified for iPSC differentiation (detailed protocol provided).
- **SOFT missing:** Passage numbers not stated for any cell line.

---

### 3. Human Subjects/Clinical

**Trigger:** Postmortem motor cortex from sporadic ALS patients and controls.

| Item | Status | Details |
|---|---|---|
| IRB approval | **Present** | IRB# 10058 (Benaroya) and IRB# 120056 (UCSD) stated |
| Informed consent | **Present** | "HIPAA-compliant informed consent" stated |
| Participant demographics | **Partial** | n=6 sALS, n=4 controls; Supplementary Table S2 referenced but not provided in manuscript |
| Inclusion/exclusion criteria | **Missing** | Not stated |
| Postmortem interval | **Present** | "Usually under 6 h" stated |
| Sex, age, disease duration | **Unverifiable** | Supplementary Table S2 referenced; cannot verify from manuscript alone |

**Issues:**

- **HARD missing:** Supplementary Table S2 is referenced for participant demographics but not provided in the manuscript text. Sex, age, disease duration, and ALS phenotype are not stated in the main text.
- **HARD missing:** Inclusion/exclusion criteria for sALS and control groups not specified.
- **SOFT missing:** No power calculation or sample-size justification for n=6 sALS, n=4 controls.
- **SOFT missing:** No statement on whether tissue selection was randomized or blinded.

---

### 4. Chemicals/Drugs/Dosing

**Trigger:** Proteasome inhibitors (BTZ, MG132, MRZ), doxycycline, and other reagents.

| Chemical | Vendor | Catalog # | CAS/Identity | Dose/Concentration | Vehicle | Route/Mode | Status |
|---|---|---|---|---|---|---|---|
| Bortezomib (BTZ) | ApexBio | A2614 | — | 2, 20 nM (varies by assay) | — | Added to culture medium | **Present** |
| MG132 | Selleckchem | S2619 | — | 100 nM | — | Added to culture medium | **Present** |
| Marizomib (MRZ) | Selleckchem | S7504 | — | 10 nM | — | Added to culture medium | **Present** |
| Doxycycline | Sigma-Aldrich | D9891 | — | 2 µg/mL | — | Added to culture medium | **Present** |
| ROCK inhibitor (Y-27632) | Selleckchem | S1049 | — | 10 µM | — | Added to culture medium | **Present** |
| Protamine sulfate | — | — | — | 10–50 µg/mL | — | Added to viral supernatant | **Unverifiable** |

**Issues:**

- **SOFT missing:** Vehicle/solvent not stated for proteasome inhibitors (assumed DMSO or aqueous, but not specified).
- **SOFT missing:** Final concentration of protamine sulfate stated as range (10–50 µg/mL) without justification for variation.
- **SOFT missing:** Duration of drug exposure varies across experiments (12, 24, 48 hr) but is stated per experiment.

---

### 5. Oligos/Plasmids/Constructs

**Trigger:** Lentiviral vectors, siRNA, PCR primers, synthetic peptides.

| Construct/Oligo Type | Sequence | Source/Addgene # | Validation | Status |
|---|---|---|---|---|
| Lentiviral plasmids (pST001 backbone) | — | "Will be deposited to Addgene at publication" | — | **Unverifiable** |
| TDP-43 variants (WT, K82Q, K82R, 6KR, 14KR, PY-NLS, etc.) | — | Supplementary Table S1 referenced | — | **Unverifiable** |
| Human TDP-43 siRNA | — | Not specified | — | **Missing** |
| Packaging plasmids (pMD2.G, psPAX2) | — | Standard 2nd-generation system; no catalog # | — | **Unverifiable** |
| qRT-PCR primers/probes | — | Supplementary Table S5 referenced | — | **Unverifiable** |
| TDP-43 peptides (aa77–110, with/without acetylation) | — | "Synthesised by Sanyou Inc." | — | **Unverifiable** |

**Issues:**

- **HARD missing:** Lentiviral plasmids stated to be "deposited to Addgene at publication" but are not yet available; Supplementary Table S1 referenced but not provided in manuscript.
- **HARD missing:** siRNA target sequence(s) not stated. Only "human TDP-43 siRNAs" mentioned; no sequence, vendor, or catalog # provided.
- **HARD missing:** qRT-PCR primer and probe sequences not provided in manuscript (Supplementary Table S5 referenced but not included).
- **HARD missing:** Synthetic peptide sequences and acetylation sites stated generically (e.g., "TDP-43aa77–110 with acetylation at K79, K82, or K84") but exact sequences and synthesis vendor details not fully specified.
- **SOFT missing:** No off-target assessment for siRNA.
- **SOFT missing:** Packaging plasmid sources (pMD2.G, psPAX2) not cited; assumed standard but unverified.

---

### 6. Mass Spectrometry (Proteomics)

**Trigger:** TMT quantitative proteomics (nuclear proteome), PTM detection (acetylation, ubiquitination, phosphorylation).

#### 6a. Nuclear Proteome (TMT)

| Parameter | Value | Status |
|---|---|---|
| **Instrument** | Orbitrap Eclipse | **Present** |
| **Acquisition mode** | Data-dependent; MS1 (120k res), MS2 (ion trap CID), MS3 (SPS3, 7.5k res) | **Present** |
| **Sample prep** | NE-PER nuclear/cytoplasmic extraction | **Present** |
| **Digestion** | Trypsin + Lys-C (1 hr pre-digest, 14 hr main) | **Present** |
| **Labeling** | TMT six-plex | **Present** |
| **LC system** | nLC 1200, 25 cm × 100 µm BEH C18 (1.7 µm) | **Present** |
| **Gradient** | 0–25% B (75 min), 25–40% B (30 min), 40–100% B (10 min), hold 100% B (5 min) | **Present** |
| **Search engine** | Rawconverter (MS extraction), DTASelect2 (PSM filtering), Census2 (TMT quantification) | **Present** |
| **Database** | UniProt human protein database | **Partial** |
| **FDR threshold** | ≤1% at PSM level | **Present** |
| **Static modifications** | Carbamidomethylation (Cys), TMT on Lys + N-terminus | **Present** |
| **Precursor mass tolerance** | 50 ppm | **Present** |
| **Fragment ion tolerance** | 500 ppm (CID), 20 ppm (HECD) | **Present** |
| **Minimum peptide length** | 6 amino acids | **Present** |
| **Isobaric purity filter** | >0.6 | **Present** |
| **Quantification method** | Weighted normalization, one-sample t-test (3 forward + 3 reverse labeling groups) | **Present** |
| **Repository accession** | — | **Missing** |
| **Replicates (n)** | 3 forward + 3 reverse labeling groups (6 total) | **Present** |
| **Peptide coverage (TDP-43)** | 98.3% | **Present** |

**Issues:**

- **HARD missing:** UniProt database version/release date not stated.
- **HARD missing:** No repository accession (ProteomeXchange/PRIDE) provided for raw MS data or processed results.
- **SOFT missing:** Monoisotopic precursor selection and dynamic exclusion (60 s) mentioned but not fully parameterized (e.g., intensity threshold for selection).

#### 6b. PTM Detection (Acetylation, Ubiquitination, Phosphorylation)

| Parameter | Value | Status |
|---|---|---|
| **Instrument** | Not explicitly stated; presumed LC-MS/MS | **Unverifiable** |
| **Sample prep** | IP with GFP nanobody magnetic beads | **Present** |
| **Digestion** | Trypsin and chymotrypsin independently, combined | **Present** |
| **Enrichment** | Titanium dioxide chromatography | **Present** |
| **Acquisition mode** | Data-dependent or data-independent (DIA) | **Unverifiable** |
| **Search engine** | MaxQuant or Proteome Discoverer | **Unverifiable** |
| **Database** | — | **Missing** |
| **FDR** | — | **Missing** |
| **Modifications searched** | Acetylation (K), ubiquitination (K), phosphorylation (S/T) | **Partial** |
| **Tolerances** | — | **Missing** |
| **Repository accession** | — | **Missing** |

**Issues:**

- **HARD missing:** PTM MS analysis lacks instrument model, acquisition parameters, search engine version, database, FDR threshold, and mass tolerances.
- **HARD missing:** No repository accession for PTM MS data.
- **HARD unverifiable:** "Data analysis conducted with software tools (MaxQuant or Proteome Discoverer)" — both tools mentioned without specifying which was used or versions.
- **SOFT missing:** No statement on number of replicates for PTM analysis.

---

### 7. Microscopy/Imaging

**Trigger:** Confocal microscopy (IF, live-cell imaging), high-content analysis.

| Parameter | Value | Status |
|---|---|---|
| **Instrument (fixed IF)** | Yokogawa X1 confocal scanhead on Nikon Ti2 | **Present** |
| **Objective** | Plan apo lambda 100× oil (NA 1.45) or 60× oil (NA 1.4) | **Present** |
| **Detector** | Spinning disk confocal | **Present** |
| **Live-cell imaging instrument** | Yokogawa CQ1 benchtop spinning-disk confocal | **Present** |
| **Live-cell objective** | ×40 or ×60 dry | **Present** |
| **Fluorophores/markers** | Clover (GFP variant), mRuby, DAPI | **Present** |
| **Imaging settings (temperature, CO₂, humidity)** | 37°C, 5% CO₂, humidified | **Present** |
| **Image acquisition software** | CQ1 software v.1.05.01.02 (live-cell) | **Present** |
| **Analysis software** | — | **Missing** |
| **Gating/segmentation strategy** | — | **Missing** |
| **Quantification method** | Nuclear/cytoplasmic ratio; nuclear vs. whole-cell fluorescence intensity | **Partial** |
| **Number of cells/fields analyzed** | — | **Missing** |

**Issues:**

- **HARD missing:** Analysis software for quantifying nuclear/cytoplasmic localization not specified (e.g., Fiji, CellProfiler, Imaris, custom script).
- **HARD missing:** Gating or segmentation strategy for defining nuclear vs. cytoplasmic regions not described.
- **HARD missing:** Number of cells analyzed per condition not stated (e.g., "n=50 cells per condition").
- **SOFT missing:** Laser wavelengths, detector gain, pinhole size, and pixel dwell time not specified.
- **SOFT missing:** Thresholds for nuclear/cytoplasmic segmentation not stated.

---

### 8. Cross-Cutting Items

#### 8a. Sample Size (n) and Replication

| Experiment | n (biological replicates) | n (technical replicates) | What n represents | Status |
|---|---|---|---|---|
| Proteasome activity assay (Fig. 1A) | — | — | — | **Missing** |
| TDP-43 fractionation (Fig. 1B) | — | — | — | **Missing** |
| Immunofluorescence (Fig. 1C–E) | — | — | — | **Missing** |
| TMT proteomics (Fig. 1E–F) | 6 (3 forward + 3 reverse) | — | Labeling groups | **Present** |
| RT-PCR stathmin-2 (Fig. 1G) | — | 3 | Technical replicates stated | **Partial** |
| Co-IP experiments (Fig. 2A–B) | — | — | — | **Missing** |
| Live-cell imaging (Fig. 2D–I) | — | — | — | **Missing** |
| Peptide-importin-α1 binding assay (Fig. 3F) | — | — | — | **Missing** |
| Cell fractionation (Fig. 3C–E) | — | — | — | **Missing** |
| Lysine-to-arginine mutagenesis (Fig. 4A–H) | — | — | — | **Missing** |
| Postmortem tissue (Fig. 5B–C) | 6 sALS, 4 controls | — | Individual donors | **Present** |
| Proteasome activity (mouse/human, Fig. S1A) | 3 mice (per age); 6 sALS, 4 controls | — | Individual animals/donors | **Partial** |

**Issues:**

- **HARD missing:** Biological replicates (n) not stated for most cell-based experiments (proteasome assay, fractionation, IF, co-IP, live-cell imaging, mutagenesis).
- **HARD missing:** Number of cells/fields analyzed per condition not stated for microscopy experiments.
- **SOFT missing:** Technical replicates stated only for qRT-PCR (n=3); not stated for other assays.

#### 8b. Statistical Tests and Error Bars

| Figure/Test | Statistical Test | Error Bar Representation | Status |
|---|---|---|---|
| Fig. 1A (proteasome activity) | — | — | **Missing** |
| Fig. 1D (nucleocytoplasmic ratio) | — | — | **Missing** |
| Fig. 1E (volcano plot) | One-sample two-sided Student's t-test (unadjusted P) | — | **Present** |
| Fig. 1F (nuclear protein levels) | — | — | **Missing** |
| Fig. 1G (RT-PCR) | — | — | **Missing** |
| Fig. 3F (peptide-importin binding) | — | — | **Missing** |
| Fig. 4E (nuclear TDP-43 quantification) | — | — | **Missing** |
| Fig. 5B (ac-TDP-43 levels) | — | — | **Missing** |
| Methods (general) | "Two-tailed Student's t-tests" for two groups; "one-way ANOVA with Tukey's correction" for ≥3 groups; "Chi-squared tests with Yates' correction" | "Error bars represent SEM unless stated otherwise" | **Present** |

**Issues:**

- **HARD missing:** Specific statistical tests not stated for individual figures (e.g., Fig. 1A, 1D, 1F, 1G, 3F, 4E, 5B).
- **SOFT present:** General statistical approach and error bar representation stated in Methods, but not consistently applied to all figures.

#### 8c. Software, Tools, and Instrument Versions

| Software/Tool | Version | Status |
|---|---|---|
| Rawconverter | — | **Missing** |
| DTASelect2 | — | **Missing** |
| Census2 | — | **Missing** |
| MaxQuant | — | **Unverifiable** |
| Proteome Discoverer | — | **Unverifiable** |
| CQ1 (live-cell imaging) | v.1.05.01.02 | **Present** |
| Prism (statistics) | 8 | **Present** |
| R (volcano plot) | — | **Missing** |
| Fiji/ImageJ (microscopy analysis) | — | **Missing** |
| Custom analysis scripts | — | **Missing** |

**Issues:**

- **HARD missing:** Versions of MS analysis tools (Rawconverter, DTASelect2, Census2) not stated.
- **HARD missing:** Versions of MaxQuant or Proteome Discoverer not specified (only "one or the other" mentioned).
- **HARD missing:** R package version for volcano plot generation not stated.
- **HARD missing:** Microscopy image analysis software and version not specified.
- **SOFT missing:** No custom code or scripts provided or deposited.

#### 8d. Data Availability

| Data Type | Repository | Accession | Status |
|---|---|---|---|
| Raw MS data (TMT proteomics) | ProteomeXchange/PRIDE | — | **Missing** |
| Processed proteomics data | — | — | **Missing** |
| PTM MS data | ProteomeXchange/PRIDE | — | **Missing** |
| Microscopy images | — | — | **Missing** |
| Lentiviral plasmids | Addgene | "To be deposited at publication" | **Unverifiable** |
| Cell lines (iPSC) | — | — | **Missing** |

**Issues:**

- **HARD missing:** No data-availability statement provided. Manuscript does not specify where raw or processed data will be deposited.
- **HARD missing:** MS data (both TMT and PTM) not deposited in ProteomeXchange/PRIDE or equivalent.
- **HARD missing:** Lentiviral plasmids stated as "to be deposited" but not yet available; no interim access mechanism provided.
- **SOFT missing:** Microscopy image datasets not deposited (e.g., OMERO, Zenodo).

#### 8e. Code Availability

| Code/Analysis | Language | Repository | Status |
|---|---|---|---|
| Custom image analysis | — | — | **Missing** |
| Statistical analysis scripts | — | — | **Missing** |
| Data processing pipelines | — | — | **Missing** |

**Issues:**

- **HARD missing:** No code availability statement. Custom analysis (e.g., nuclear/cytoplasmic segmentation, quantification) appears to have been performed but no code or pseudocode provided.

---

## Protocol-Provenance Assessment

| Method | Citation | Resolvability | Status |
|---|---|---|---|
| iPSC differentiation | "as previously described" (ref 37) | Fernandopulle et al. 2018 (PMID resolvable) | **Delegated-resolvable** |
| Nuclear extraction (NE-PER) | Thermo Scientific product manual | Manufacturer protocol | **Delegated-resolvable** |
| Nucleus/cytoplasmic fractionation | Abcam Nuclear Extraction Kit | Manufacturer protocol | **Delegated-resolvable** |
| Lentiviral production | "Detailed guides and protocols posted can be found on the Addgene website" | Addgene protocols (resolvable online) | **Delegated-resolvable** |
| Proteasome activity assay | Promega Proteasome-Glo reagent | Manufacturer protocol | **Delegated-resolvable** |
| Cell viability assay | CellTiter-Glo (Promega) | Manufacturer protocol | **Delegated-resolvable** |
| Confocal microscopy | Standard protocols; instrument manuals | Yokogawa/Nikon manuals | **Delegated-resolvable** |
| Silver staining | ProteoSilver kit (Sigma) | Manufacturer protocol | **Delegated-resolvable** |
| ELISA-based binding assays | Custom protocol described in Methods | Full description provided | **Self-contained** |
| TDP-43 peptide-importin-α1 binding assay | Custom protocol described in Methods | Full description provided | **Self-contained** |
| Generation of ac-TDP-43(K82) antibodies | "Polyclonal antibodies generated by Sanyou Inc." | Vendor-performed service; no external protocol | **Delegated-resolvable** |

**Issues:**

- **SOFT:** Most methods delegated to manufacturer protocols or cited references, which is acceptable for standard techniques.
- **SOFT:** Custom assays (peptide-importin binding, ELISA) are described in sufficient detail to be self-contained.
- **SOFT:** No deviations from cited protocols explicitly stated (e.g., "as described, except..."), though some parameter variations are noted (e.g., proteasome inhibitor doses).

---

## Summary of HARD Missing Items

1. **Antibodies:** Vendor, catalog #, dilution, host species/clonality for primary antibodies (Supplementary Table S3 not provided); ac-TDP-43(K82) antibody dilutions not stated.
2. **Cell lines:** No STR authentication or mycoplasma testing for any line; iPSC source lacks RRID.
3. **Human subjects:** Supplementary Table S2 (participant demographics) not provided; inclusion/exclusion criteria not stated.
4. **Oligos/plasmids:** siRNA target sequence(s) not provided; qRT-PCR primer sequences not provided (Supplementary Table S5 not included); lentiviral plasmids not yet deposited to Addgene.
5. **Mass spectrometry (PTM):** Instrument model, acquisition parameters, search engine version, database, FDR, mass tolerances, and repository accession all missing for PTM analysis.
6. **Microscopy:** Analysis software, segmentation strategy, and number of cells analyzed per condition not specified.
7. **Sample size:** Biological replicates (n) not stated for most cell-based experiments; number of cells/fields analyzed not stated for imaging.
8. **Statistical tests:** Specific tests and error bar representations not stated for individual figures.
9. **Software versions:** Versions missing for Rawconverter, DTASelect2, Census2, MaxQuant/Proteome Discoverer, R, and image analysis software.
10. **Data availability:** No statement provided; MS data not deposited; plasmids not yet available.

---

## Summary of SOFT Missing Items

1. **Cell lines:** Passage numbers not stated.
2. **Human subjects:** No power calculation; no randomization/blinding statement for tissue selection.
3. **Chemicals:** Vehicle/solvent not stated for proteasome inhibitors.
4. **Microscopy:** Laser wavelengths, detector gain, pinhole size, pixel dwell time, and segmentation thresholds not specified.
5. **Mass spectrometry (TMT):** UniProt database version not stated; monoisotopic precursor selection intensity threshold not specified.
6. **Code availability:** No custom code or scripts provided or deposited.

---

## Unverifiable Items (Require Author Clarification)

1. **Supplementary Tables S1, S2, S3, S5:** Referenced but not provided in manuscript; cannot verify contents.
2. **iPSC source:** "Kind gift of Michael Ward" — no RRID or authentication status verifiable.
3. **Loading control antibodies (Lamin B1, GAPDH):** Vendor and catalog # not stated; cannot verify.
4. **Co-IP antibodies (TDP-43, FUS, importins):** Vendor, catalog #, dilution not stated; cannot verify.
5. **PTM MS analysis:** "MaxQuant or Proteome Discoverer" — cannot determine which was used or versions.
6. **Protamine sulfate:** Vendor not stated; concentration range (10–50 µg/mL) not justified.
7. **Lentiviral plasmids:** Stated as "to be deposited at publication" but not currently available; cannot verify sequences or construction details.

---

## Conclusion

This manuscript has **substantial gaps in methods completeness and reagent traceability**, particularly in:

- **Antibody specifications** (primary antibodies, custom ac-TDP-43 antibodies)
- **Supplementary table provision** (S1, S2, S3, S5 referenced but not included)
- **Mass spectrometry parameters** (PTM analysis lacks critical details)
- **Sample size and statistical reporting** (n values and specific tests missing for most figures)
- **Data and code availability** (no repository accessions; plasmids not yet deposited)
- **Microscopy quantification** (analysis software and segmentation strategy not specified)

**An independent group would face significant difficulty reproducing this work without substantial author clarification and provision of missing supplementary materials and data.**