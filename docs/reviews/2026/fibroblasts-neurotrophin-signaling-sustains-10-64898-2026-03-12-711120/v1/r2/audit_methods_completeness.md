# Methods Completeness & Reagent Traceability Audit
**Manuscript:** Fibroblasts neurotrophin signaling sustains pathological vascular maturation in rheumatoid arthritis

---

## Cross-Cutting Items (Apply to All Manuscripts)

### Sample Size & Replication Reporting
**Status: PARTIALLY PRESENT**

- **Spatial transcriptomics cohort (Xenium):** n = 22 RA patients + 2 healthy donors, with paired pre/post-treatment biopsies stated in abstract and Methods. Total cells analyzed (2,049,358) and vascular cells (368,217) reported. ✓
- **Cell culture experiments:** Biological replicates stated in figure legends as "Individual data points represent biological replicates" (e.g., Figs. 3D–E, 4A–C, 5C–E, 6E–G). However, **specific n per condition is not uniformly stated in the main text or Methods**—only visible in figures. For example:
  - Fig. 3D–E (DLL4 + siRNA knockdown): n not stated in Methods or figure legend text
  - Fig. 4A–C (neurotrophin stimulation): n not stated
  - Fig. 5C–E (NOTCH3 KO + DLL4): n not stated
  - **HARD MISSING:** Methods section should state n for each major cell culture experiment (co-culture, siRNA knockdown, NOTCH3 KO, neurotrophin stimulation, TRK inhibitor treatment).

- **Synovial explant/organoid studies:** n stated in some figure legends (e.g., Fig. 6E–G quantifications show individual data points) but **not systematized in Methods**. How many independent tissue donors per condition? How many technical replicates per donor? **HARD MISSING.**

- **Technical vs. biological replicates:** Distinction not clearly stated. Are the "individual data points" in figures biological replicates (independent donors/cultures) or technical replicates (same culture, multiple wells)? **HARD MISSING.**

### Statistical Testing & Error Bars
**Status: PRESENT but INCOMPLETE**

- **Named tests:** Wilcoxon matched-pairs signed-rank test (Fig. 1G–H, paired patient samples), two-tailed Student's t-test, one-way ANOVA with Bonferroni post-hoc correction stated in multiple figure legends. ✓
- **Error bars:** Consistently labeled as "mean ± standard deviation (SD)" in figure legends (e.g., Figs. 4D–F, 5C–E, 6E–G, S5C, S9). ✓
- **P-value reporting:** P values shown on graphs or in legends. ✓
- **Missing:** No statement of significance threshold (α = 0.05 assumed but not stated in Methods). **SOFT MISSING.**

### Software, Tool & Instrument Versions
**Status: PARTIALLY PRESENT**

| Tool/Software | Version | Status |
|---|---|---|
| Seurat | v5.0.0 | ✓ |
| Harmony | v1.2.4 | ✓ |
| Louvain algorithm | not versioned | unverifiable |
| Cellpose | cited (ref 48) | delegated-resolvable |
| scikit-image | cited (ref 49) | delegated-resolvable |
| UCell | GitHub link provided | ✓ |
| ImageJ | mentioned, no version | **SOFT MISSING** |
| Graphpad Prism | v10.4.1 | ✓ |
| R software | no version | **SOFT MISSING** |
| EVOS M7000 imaging system | model stated, no settings | **HARD MISSING** (see Microscopy section) |
| Xenium 5K Prime platform | model stated, no detailed instrument parameters | **HARD MISSING** (see Genomics/Spatial Transcriptomics section) |
| AriaMX Real Time PCR machine | model stated, no cycling parameters | **HARD MISSING** (see qPCR section below) |

### Data Availability Statement
**Status: MISSING**

- **No data-availability statement in the manuscript.** The paper states "Xenium data generation and panel design" in Author Contributions but does not specify whether raw Xenium data, processed count matrices, or single-cell reference data are deposited in a public repository (GEO, ArrayExpress, etc.). **HARD MISSING.**
- **Code availability:** No statement on whether custom analysis scripts (Seurat pipeline, UCell scoring, spatial analysis) are available. GitHub/Zenodo/supplementary materials not mentioned. **HARD MISSING.**

---

## Conditional Categories

### 1. Antibodies & Immunodetection (WB, IHC, IF, ELISA, RNAscope)
**Trigger: PRESENT** (extensive use across WB, IHC, IF, RNAscope, ELISA)

#### Western Blot
**Status: PARTIALLY PRESENT**

| Antibody | Vendor | Catalog # | Clone | Dilution | Host | Application | Status |
|---|---|---|---|---|---|---|---|
| pY-TRKA | Cell Signaling | #4638 (TrkA/TrkB sampler kit) | not stated | 1:500 | not stated | WB | unverifiable |
| Total TRKA | Cell Signaling | #4638 | not stated | 1:500 | not stated | WB | unverifiable |
| pY-TRKB | Cell Signaling | #4638 | not stated | 1:500 | not stated | WB | unverifiable |
| Total TRKB | Cell Signaling | #4638 | not stated | 1:500 | not stated | WB | unverifiable |
| CNN1 (calponin) | Proteintech | #24855-1-AP | not stated | not stated | not stated | WB | **HARD MISSING** dilution |
| MYH11 | Proteintech | #21404-1-AP | not stated | not stated | not stated | WB | **HARD MISSING** dilution |
| NGF | Abcam | #ab52918 | not stated | not stated | not stated | WB | **HARD MISSING** dilution |
| GAPDH | Thermo Fisher | #MA5-15738 | not stated | not stated | not stated | WB | **HARD MISSING** dilution |
| β-actin | Cell Signaling | #3700 | not stated | not stated | not stated | WB | **HARD MISSING** dilution |
| HRP-conjugated anti-rabbit | Thermo Fisher | #32460 | not stated | 1 hour, RT | not stated | WB secondary | **SOFT MISSING** dilution |
| HRP-conjugated anti-mouse | Thermo Fisher | #31430 | not stated | 1 hour, RT | not stated | WB secondary | **SOFT MISSING** dilution |
| HRP-conjugated anti-goat | Thermo Fisher | #A16005 | not stated | 1 hour, RT | not stated | WB secondary | **SOFT MISSING** dilution |

**Issues:**
- Primary antibody dilutions missing for CNN1, MYH11, NGF, GAPDH, β-actin. **HARD MISSING.**
- Host species not stated for any antibody. **HARD MISSING.**
- Clone information not provided (monoclonal vs. polyclonal). **HARD MISSING.**
- Secondary antibody dilutions not stated. **SOFT MISSING.**

#### Immunohistochemistry (IHC) & Immunofluorescence (IF)
**Status: PARTIALLY PRESENT**

| Antibody | Vendor | Catalog # | Clone | Dilution | Host | Application | Status |
|---|---|---|---|---|---|---|---|
| α-SMA (smooth muscle actin) | not stated | not stated | not stated | not stated | not stated | IHC, IF | **HARD MISSING** all details |
| PECAM1 (CD31) | Biolegend | #303106 | not stated | not stated | not stated | IF | **HARD MISSING** dilution, host |
| NGFR | Cell Signaling | #4638 | not stated | not stated | not stated | IF, IHC | **HARD MISSING** dilution, host |
| NTRK1 (TRKA) | not stated | not stated | not stated | not stated | not stated | IF, IHC | **HARD MISSING** all details |
| NTRK2 (TRKB) | not stated | not stated | not stated | not stated | not stated | IF, IHC | **HARD MISSING** all details |
| NTRK3 (TRKC) | not stated | not stated | not stated | not stated | not stated | IF, IHC | **HARD MISSING** all details |
| MYH11 | Proteintech | #21404-1-AP | not stated | not stated | not stated | IF, IHC | **HARD MISSING** dilution, host |
| RGS5 | not stated | not stated | not stated | not stated | not stated | IF (RNAscope) | delegated to RNAscope probes |
| Alexa Fluor 555 anti-rabbit | Thermo Fisher | #A-21424 | not stated | not stated | not stated | IF secondary | **SOFT MISSING** dilution |
| Alexa Fluor 488 anti-rabbit | Thermo Fisher | #A11034 | not stated | not stated | not stated | IF secondary | **SOFT MISSING** dilution |
| Alexa Fluor 647 anti-rabbit | Thermo Fisher | #A32733 | not stated | not stated | not stated | IF secondary | **SOFT MISSING** dilution |
| Alexa Fluor anti-goat | Thermo Fisher | #A110055 | not stated | not stated | not stated | IF secondary | **SOFT MISSING** dilution |

**Issues:**
- α-SMA source and catalog # not provided. **HARD MISSING.**
- Most primary antibody dilutions missing. **HARD MISSING.**
- Host species not stated. **HARD MISSING.**
- Secondary antibody dilutions not stated. **SOFT MISSING.**

#### RNAscope (In Situ Hybridization)
**Status: PARTIALLY PRESENT**

- **Probes listed in Table 2** with gene targets and probe IDs (ACD Bio catalog numbers). ✓
- **Assay:** RNAScope multiplex fluorescent V2 (ACD Bio, SOP 45-009A). ✓
- **Imaging:** EVOS M7000 (model stated, no settings). See Microscopy section.
- **Quantification method:** Cellpose for nuclear segmentation, scikit-image for nuclear expansion and intensity calculation. ✓
- **Missing:** Specific probe sequences not provided in Table 2 (only gene names and catalog #s). For custom probes, sequences should be stated. **SOFT MISSING** (standard commercial probes, so less critical).

#### ELISA
**Status: PARTIALLY PRESENT**

- **NGF ELISA:** Fig. 3B, Fig. S3B, Fig. S8A report "pg/ml" with n and p-values.
- **Kit/vendor not stated.** Methods say "ELISA quantification of NGF secretion" but do not specify which ELISA kit (commercial or in-house). **HARD MISSING.**
- **Assay parameters:** No mention of detection range, sensitivity, or standard curve. **SOFT MISSING.**

---

### 2. Cell Lines & Primary Cells
**Trigger: PRESENT** (synovial fibroblasts, HUVECs)

#### Synovial Fibroblasts
**Status: PARTIALLY PRESENT**

- **Source:** "Synovial tissue collected after patients undergoing arthroplasty or synovectomy procedures" from Brigham and Women's Hospital and Flinders Medical Center. ✓
- **IRB approval:** MGB IRB no. 2019P002924 and Protocol#396.10 stated. ✓
- **Isolation protocol:** Enzymatic digestion (Dispase II, DNase I, Liberase TL) described in Methods. ✓
- **Passage number:** "3 to 6 passages for experiments" stated. ✓
- **Authentication (STR):** Not mentioned. **HARD MISSING.**
- **Mycoplasma testing:** Not mentioned. **HARD MISSING.**
- **RRID/CVCL:** Not assigned. **SOFT MISSING** (primary cells, not a cell line, so less critical).
- **Media:** "Complete FLS media (DMEM supplemented with 10% fetal bovine serum, HEPES, MEM amino acids, L-glutamine, penicillin-streptomycin, nonessential MEM amino acids, 2-mercaptoethanol, and gentamicin)" stated. ✓

#### HUVECs (Human Umbilical Vein Endothelial Cells)
**Status: PARTIALLY PRESENT**

- **Source:** "Thermofisher" stated. ✓
- **Passage number:** "passage 3-7" stated in co-culture section. ✓
- **RRID/CVCL:** Not provided. **SOFT MISSING.**
- **Authentication (STR):** Not mentioned. **HARD MISSING.**
- **Mycoplasma testing:** Not mentioned. **HARD MISSING.**
- **Media:** "EGM2 media consisting of EGM-Plus media (Lonza # CC-5035) supplemented with the EGM-plus bulletkit (Lonza, cc-3162)" stated. ✓

**Issues:**
- Neither cell type authenticated by STR or tested for mycoplasma. **HARD MISSING** for reproducibility.

---

### 3. Human Subjects & Clinical Data
**Trigger: PRESENT** (RA patient biopsies, clinical metadata)

#### IRB & Informed Consent
**Status: PRESENT**

- **IRB approval:** MGB IRB no. 2019P002924 (Brigham and Women's Hospital) and Protocol#396.10 (Flinders Medical Center) stated. ✓
- **Informed consent:** Not explicitly stated. **HARD MISSING** (should confirm consent was obtained).

#### Participant Demographics & Inclusion/Exclusion
**Status: PARTIALLY PRESENT**

- **Cohort size:** n = 22 RA patients + 2 healthy donors. ✓
- **Disease status:** "treatment-naive patients" and "pre-treatment and 6-month post-treatment" stated. ✓
- **Treatment regimens:** "triple csDMARD therapy (Hydroxychloroquine, methotrexate, and sulfasalazine) or TNFi (adalimumab)" stated. ✓
- **Clinical outcome measure:** "DAS28-ESR < 2.6" (clinical remission) mentioned. ✓
- **Missing demographics:**
  - Age not stated. **HARD MISSING.**
  - Sex distribution not stated. **HARD MISSING.**
  - Disease duration not stated. **HARD MISSING.**
  - Inclusion/exclusion criteria not stated. **HARD MISSING.**
  - Serological status (RF, anti-CCP) not stated. **SOFT MISSING.**

#### Trial Registration
**Status: NOT APPLICABLE** (observational study, not an interventional trial)

---

### 4. Chemicals, Drugs & Dosing
**Trigger: PRESENT** (neurotrophins, TRK inhibitors, NOTCH inhibitors, small-molecule drugs)

#### Neurotrophins
**Status: PARTIALLY PRESENT**

| Drug | Vendor | Catalog # | CAS # | Concentration(s) Tested | Vehicle | Status |
|---|---|---|---|---|---|---|
| NGF (recombinant) | R&D Systems | 256-GF | not stated | 1, 100 ng/ml | DMSO or PBS | ✓ |
| BDNF (recombinant) | R&D Systems | 11166-BD | not stated | 100 ng/ml | DMSO or PBS | ✓ |
| NT3 (recombinant) | R&D Systems | 267-N3-005 | not stated | 50, 100 ng/ml | DMSO or PBS | ✓ |

**Issues:**
- CAS numbers not provided. **SOFT MISSING.**
- Vehicle final concentration not stated (e.g., "diluted in media" but % DMSO not specified). **SOFT MISSING.**

#### TRK Inhibitors & Modulators
**Status: PARTIALLY PRESENT**

| Drug | Vendor | Catalog # | CAS # | Concentration(s) | Vehicle | Status |
|---|---|---|---|---|---|---|
| GW-441756 (TRKA inhibitor) | Tocris | #2238 | not stated | 1, 5, 10 µM | not stated | ✓ conc. |
| ANA-12 (TRKB inhibitor) | Tocris | #4781 | not stated | 1, 5, 10 µM | not stated | ✓ conc. |
| GNF-5837 (pan-TRK inhibitor) | Tocris | #4559 | not stated | 1, 5, 10 µM | not stated | ✓ conc. |
| Entrectinib (FDA-approved TRK inhibitor) | MedChemExpress | HY-12678 | not stated | 1, 5, 10 µM (inferred) | not stated | ✓ conc. |
| Larotrectinib (FDA-approved TRK inhibitor) | MedChemExpress | HY-12866 | not stated | 1, 5, 10 µM (inferred) | not stated | ✓ conc. |
| 7,8-DHF (TRKB agonist) | Tocris | #3826 | not stated | 1, 5, 10 µM | not stated | ✓ conc. |
| LM22B-10 (pan-neurotrophin agonist) | Tocris | #6037 | not stated | 1, 5, 10 µM | not stated | ✓ conc. |

**Issues:**
- Vehicle (DMSO, ethanol, etc.) not stated for any inhibitor. **HARD MISSING.**
- Final vehicle concentration in culture media not stated. **HARD MISSING.**
- CAS numbers not provided. **SOFT MISSING.**

#### NOTCH Pathway Modulators
**Status: PARTIALLY PRESENT**

| Drug | Vendor | Catalog # | Concentration | Vehicle | Status |
|---|---|---|---|---|---|
| DAPT (γ-secretase inhibitor) | Tocris | #2634 | 10 µM | not stated | ✓ conc. |
| DLL4-Fc (NOTCH ligand) | R&D Systems | 10185-D4 | 5 µg/ml coating | not stated | ✓ conc. |

**Issues:**
- Vehicle not stated. **HARD MISSING.**

#### Other Reagents
**Status: PARTIALLY PRESENT**

| Reagent | Vendor | Catalog # | Concentration | Status |
|---|---|---|---|---|
| Matrigel | Corning | #356231 | 1:10 dilution (co-culture), 50 µL/well (organoids) | ✓ |
| Polyethylene glycol (PEG-it) | System Biosciences | #LV-810-A-1 | not stated | **SOFT MISSING** |
| Polybrene | not stated | not stated | 10 µg/ml | **HARD MISSING** vendor |
| WST-1 (cell viability assay) | Millipore Sigma | 501594400 | not stated | **SOFT MISSING** protocol |

---

### 5. Oligos, Plasmids & Constructs (siRNA, CRISPR, Lentiviral)
**Trigger: PRESENT** (siRNA knockdowns, CRISPR-Cas9 NOTCH3 KO, lentiviral NGFR overexpression)

#### siRNA Knockdowns
**Status: PARTIALLY PRESENT**

| Target | Vendor | Assay ID / Catalog # | Sequence | Transfection Reagent | Status |
|---|---|---|---|---|---|
| NGFR | Thermo Scientific Silencer Select | S194655 | not provided | RNAiMax | **HARD MISSING** sequence |
| NTRK1 | Thermo Scientific Silencer Select | S534734 | not provided | RNAiMax | **HARD MISSING** sequence |
| NTRK2 | Thermo Scientific Silencer Select | n321595 | not provided | RNAiMax | **HARD MISSING** sequence |
| NTRK3 | Thermo Scientific Silencer Select | s9753 | not provided | RNAiMax | **HARD MISSING** sequence |
| NOTCH3 | Thermo Scientific Silencer Select | 106100 | not provided | RNAiMax | **HARD MISSING** sequence |

**Issues:**
- siRNA sequences not provided. **HARD MISSING** (needed to verify specificity and check for off-targets).
- Transfection efficiency not stated. **SOFT MISSING.**
- Off-target assessment not mentioned. **SOFT MISSING.**

#### CRISPR-Cas9 NOTCH3 Knockout
**Status: PARTIALLY PRESENT**

- **Cas variant:** Not explicitly stated (assumed SpCas9, standard). **SOFT MISSING.**
- **Guide RNA design:** "Guide RNAs were designed using Synthego design tool" (ref 1, which is the authors' own prior work). **Delegated-resolvable** but should provide gRNA sequences. **HARD MISSING** sequences.
- **Delivery method:** "P3 primary cell 4D-nucleofector X kit S (#V4XP-3032, Lonza)" stated. ✓
- **Edit validation:** Not described. Were clones sequenced to confirm NOTCH3 deletion? **HARD MISSING.**
- **Off-target assessment:** Not mentioned. **SOFT MISSING.**

#### Lentiviral NGFR Overexpression
**Status: PARTIALLY PRESENT**

- **Vector:** "pLV-BsdCMV-hNGFR, VectorBuilder, #VB230823-1657hvq" (NGFR with N-terminal GFP-tag) and control "pLV-Bsd-CMV-EGFP (VectorBuilder, # VB230502-1039MVR)" stated. ✓
- **Packaging system:** "Virapower™ HiPerform™ Lentiviral FastTiter™ Gateway® Expression protocol (Thermo Fisher Scientific, #K534000)" cited. ✓
- **Transduction:** "50 µL of viral particles and 10 µg/ml of polybrene" stated. ✓
- **Selection:** Blasticidin selection implied by "Bsd" in vector name, but not explicitly stated. **SOFT MISSING.**
- **Validation:** "GFP expression in transduced cells was monitored microscopically" stated. ✓
- **Titer determination:** Not stated. **SOFT MISSING.**

---

### 6. Genomics, Sequencing & Spatial Transcriptomics
**Trigger: PRESENT** (Xenium spatial transcriptomics, bulk RNA-seq, qPCR)

#### Xenium Spatial Transcriptomics
**Status: PARTIALLY PRESENT**

- **Platform:** "Xenium 5K Prime platform" stated. ✓
- **Sample preparation:** "FFPE blocks" from synovial tissue, processed per "CG000760 Rev A, 10X Genomics" protocol. ✓
- **Probe panels:**
  - "Xenium Prime 5K Human Pan Tissue & Pathways Panel (PN-1000671, 10X Genomics)" ✓
  - "Custom add-on panels" mentioned but not fully described. **HARD MISSING** panel composition (which genes, how many probes).
  - "High-sensitivity, custom spatial transcriptomic panel (Table. S, 1 to 3)" referenced but **supplementary tables not provided in the manuscript text**. **HARD MISSING** panel details.
- **Cell segmentation:** "Xenium Prime In Situ Gene Expression with optional Cell Segmentation Staining" protocol (CG000760, 10X Genomics). ✓
- **Imaging:** Xenium Analyzer (model stated, no detailed settings). **SOFT MISSING** laser power, exposure, gain, etc.
- **Post-run H&E staining:** "CG000613 Rev A, 10X Genomics" protocol. ✓
- **Quality control:** "Thresholded high quality cells based on transcripts and features per cell, kept 2 million high quality cells" stated. **SOFT MISSING** specific thresholds (min transcripts, min features per cell).
- **Reference dataset:** "AMP RA/SLE Consortium" single-cell reference used for annotation. ✓
- **Data analysis:**
  - Seurat v5.0.0 ✓
  - Harmony v1.2.4 ✓
  - Louvain clustering (resolution 0.3) ✓
  - Wilcoxon rank sum test for marker identification (presto package) ✓
- **Repository accession:** **NOT PROVIDED.** No GEO, ArrayExpress, or 10X Cloud accession stated. **HARD MISSING.**

#### Bulk RNA-Sequencing (NGFR Overexpression Study)
**Status: MISSING DETAILS**

- **Mentioned in Fig. 5J:** "Bulk RNA-seq for the organoid with drug treatment and without drug treatment" and "RNA-sequencing of NGFR-overexpressing fibroblasts."
- **Platform:** Not stated. **HARD MISSING.**
- **Library prep kit:** Not stated. **HARD MISSING.**
- **Read length, paired/single-end:** Not stated. **HARD MISSING.**
- **Sequencing depth:** Not stated. **HARD MISSING.**
- **Reference genome & build:** Not stated. **HARD MISSING.**
- **Alignment/analysis tools & versions:** Not stated. **HARD MISSING.**
- **Differential expression method:** "Differential expression analysis" mentioned but tool not named. **HARD MISSING.**
- **FDR threshold:** Not stated. **HARD MISSING.**
- **Repository accession (GEO/SRA):** **NOT PROVIDED.** **HARD MISSING.**

**Issues:** Bulk RNA-seq is central to the NGF/NGFR gene signature (Fig. 5J–M) but is severely under-documented. This is a **load-bearing method** that should not be delegated without full details.

#### qRT-PCR
**Status: PARTIALLY PRESENT**

- **Instrument:** AriaMX Real Time PCR machine (Agilent). ✓
- **Cycling parameters:** Not stated. **HARD MISSING.**
- **Primer sequences:** "Primer list is provided in Table 1." ✓ (Table 1 lists primers with sequences)
- **cDNA synthesis:** "QuantiTect Reverse Transcription Kit (#205311 Qiagen)" stated. ✓
- **qPCR master mix:** "Brilliant III qRT-PCR Master Mixes (#5994-1166EN, Agilent)" stated. ✓
- **Normalization:** "mRNA levels were normalized to GAPDH and calculated using the 2-ΔΔCT method" stated. ✓
- **Replicates:** Not stated per experiment. **SOFT MISSING.**
- **Primer validation:** Not mentioned (e.g., efficiency, specificity). **SOFT MISSING.**

---

### 7. Microscopy & Imaging
**Trigger: PRESENT** (wide-field fluorescence, confocal, whole-mount imaging)

#### Imaging Instruments & Settings
**Status: PARTIALLY PRESENT**

| Instrument | Model | Objective | NA | Detector | Laser/Illumination | Settings | Status |
|---|---|---|---|---|---|---|---|
| Whole-mount IF, IHC, RNAscope | EVOS M7000 | 20x (stated) | not stated | not stated | not stated | not stated | **HARD MISSING** NA, detector type, laser power, gain, offset |
| Confocal (micromass organoids) | not stated | 20x (stated) | not stated | not stated | not stated | not stated | **HARD MISSING** instrument model, detector, settings |
| Xenium Analyzer | Xenium (10X) | not applicable (in situ) | N/A | not stated | not stated | not stated | **SOFT MISSING** imaging settings |

**Issues:**
- EVOS M7000 is used extensively (Figs. 2B–C, 3A–C, 4K, 5A–B, 6C–D, S2E, S4A, etc.) but no objective NA, detector type, or acquisition settings provided. **HARD MISSING.**
- Confocal microscopy mentioned for "enlarged confocal (20X) images" (Fig. S5A) but instrument not identified. **HARD MISSING.**
- Fluorophore panel not explicitly stated (though inferred from RNAscope probes and antibodies). **SOFT MISSING** formal panel table.

#### Image Analysis & Quantification
**Status: PARTIALLY PRESENT**

- **RNAscope quantification:** Cellpose (ref 48) for nuclear segmentation, scikit-image (ref 49) for nuclear expansion and intensity calculation. ✓
- **Gating/thresholding:** "Cell types were assigned by gating normalized per cell intensity on high (>= 90th percentile) and low (<90th percentile) marker expression" stated. ✓
- **Distance calculations:** RANN package (ref 50) for distance to nearest endothelial cell. ✓
- **ImageJ:** Mentioned for "Image analysis and quantification" but no version or specific plugins stated. **SOFT MISSING.**
- **Spatial transcriptomics analysis:** Seurat, Harmony, Louvain, UCell (versions/links provided). ✓

---

### 8. Computational & Machine Learning (if applicable)
**Trigger: PRESENT** (spatial transcriptomics analysis, gene signature scoring)

#### Spatial Transcriptomics Analysis Pipeline
**Status: PARTIALLY PRESENT**

- **Datasets:** Xenium data from 46 samples (22 RA patients + 2 healthy donors, paired pre/post). ✓
- **Train/validation/test split:** Not applicable (descriptive analysis, not predictive modeling).
- **Cell typing algorithm:** Seurat v5.0.0 with Harmony v1.2.4 integration, Louvain clustering (resolution 0.3). ✓
- **Hyperparameters:** Resolution 0.3 stated; other Seurat/Harmony defaults assumed. **SOFT MISSING** full parameter list.
- **Marker identification:** Wilcoxon rank sum test (presto package). ✓
- **Library versions:** Seurat v5.0.0, Harmony v1.2.4, presto (no version), Cellpose (ref 48), scikit-image (ref 49), RANN (ref 50). ✓
- **Hardware/compute budget:** Not stated. **SOFT MISSING.**
- **Random seeds:** Not stated. **SOFT MISSING.**
- **Code availability:** Not stated. **HARD MISSING.**

#### Gene Signature Scoring (UCell)
**Status: PARTIALLY PRESENT**

- **Gene signature:** "NGF/NGFR gene signature score based on 461 upregulated genes from RNA-sequencing." ✓
- **Scoring method:** "UCell rank-based scoring approach." ✓
- **UCell version/source:** GitHub link provided (https://github.com/carmonalab/UCell). ✓
- **Marker genes:** The 461 genes are not listed in the manuscript. **HARD MISSING** gene list (should be in supplementary table or deposited).
- **Validation:** Applied to Xenium spatial data. ✓

---

### 9. Mass Spectrometry
**Trigger: NOT PRESENT** (no proteomics or metabolomics)

---

## Protocol Provenance & Delegation

### Methods Delegated to Citations

| Method | Citation | Resolvability | Status |
|---|---|---|---|
| Synovial fibroblast isolation | "as previously described (14)" | Ref 14 is Wei et al., Nature 582, 259–264 (2020), DOI 10.1038/s41586-020-2225-7 | **Delegated-resolvable** (published, DOI available) |
| Xenium slide preparation | "CG000760 Rev A, 10X Genomics" | 10X Genomics protocol document (not a peer-reviewed citation) | **Delegated-resolvable** (manufacturer protocol, publicly available) |
| Cell segmentation | "as outlined in our earlier published work (1)" | Ref 1 is Bhamidipati et al., bioRxiv 2025.03.14.642821 (preprint) | **Delegated-unverifiable** (preprint, not yet peer-reviewed; may change) |
| Fibroblast-endothelial co-culture | "as previously described (46)" | Ref 46 is Nguyen et al., Immunity 46, 220–232 (2017), DOI 10.1016/j.immuni.2017.01.007 | **Delegated-resolvable** |
| Synovial organoid generation | "as previously described (1, 14)" | Refs 1 & 14 (see above) | **Delegated-resolvable** |
| Collagen gel contraction assay | "as described earlier (12)" | Ref 12 is Romay et al., J Clin Invest 134 (2024), DOI 10.1172/JCI166134 | **Delegated-resolvable** |
| CRISPR guide RNA design | "Synthego design tool (1)" | Ref 1 (authors' prior work, preprint) | **Delegated-unverifiable** (preprint) |
| Cellpose segmentation | Ref 48 (Stringer et al., Nat Methods 18, 100–106, 2020) | Published, DOI 10.1038/s41592-020-01018-z | **Delegated-resolvable** |
| scikit-image analysis | Ref 49 (van der Walt et al., PeerJ 2, e453, 2014) | Published, DOI 10.7717/peerj.453 | **Delegated-resolvable** |
| RANN distance calculation | Ref 50 (Jones et al., PNAS 108, 15679–15686, 2011) | Published, DOI 10.1073/pnas.1015208108 | **Delegated-resolvable** |
| Lentiviral transduction | "Virapower™ HiPerform™ Lentiviral FastTiter™ Gateway® Expression protocol (Thermo Fisher Scientific, #K534000)" | Manufacturer protocol | **Delegated-resolvable** |

**Key Issue:** Ref 1 (Bhamidipati et al., bioRxiv 2025.03.14.642821) is a preprint that appears to be the authors' own concurrent work. Cell segmentation and CRISPR guide design are delegated to this preprint, which is **not yet peer-reviewed and may change**. This is problematic for reproducibility. **HARD MISSING:** These methods should be fully described in the current manuscript or the preprint should be replaced with a published reference.

---

## Summary Table: HARD vs. SOFT Missing Items

| Category | HARD Missing | SOFT Missing |
|---|---|---|
| **Cross-cutting** | Sample size per condition (cell culture); Data availability statement; Code availability | Significance threshold (α); Software versions (R, ImageJ) |
| **Antibodies** | Primary dilutions (WB, IF, IHC); Host species; Clone info; α-SMA source; ELISA kit identity; Secondary dilutions (IF) | — |
| **Cell lines** | STR authentication (both cell types); Mycoplasma testing (both cell types) | RRID/CVCL for HUVECs |
| **Human subjects** | Informed consent statement; Age, sex, disease duration, inclusion/exclusion criteria | Serological status (RF, anti-CCP) |
| **Chemicals/drugs** | Vehicle identity and final concentration (inhibitors, agonists); Polybrene vendor | CAS numbers; ELISA protocol details |
| **Oligos/plasmids** | siRNA sequences; CRISPR gRNA sequences; NOTCH3 KO validation (sequencing) | Transfection efficiency; Off-target assessment; Lentiviral titer |
| **Genomics** | Bulk RNA-seq platform, library prep, read length, depth, reference genome, alignment tool, FDR threshold, repository accession; Xenium custom panel composition; QC thresholds; Bulk RNA-seq repository accession | qPCR cycling parameters; Primer validation; Xenium imaging settings |
| **Microscopy** | EVOS M7000 objective NA, detector type, laser/illumination settings; Confocal instrument model and settings | Fluorophore panel table |
| **Computational** | Code availability; Gene signature (461 genes) list | Hyperparameter details; Hardware; Random seeds |
| **Protocol delegation** | Full description of cell segmentation and CRISPR guide design (currently delegated to unreviewed preprint Ref 1) | — |

---

## Critical Gaps Affecting Reproducibility

1. **Bulk RNA-seq (load-bearing method):** Platform, library prep, depth, reference genome, alignment tool, FDR, and repository accession all missing. This is central to the NGF/NGFR gene signature (Figs. 5J–M) and must be fully documented.

2. **Data & code availability:** No statement on where Xenium raw data, processed matrices, or custom analysis scripts are deposited. **HARD MISSING.**

3. **Antibody dilutions & specifications:** Extensive use of antibodies (WB, IHC, IF, RNAscope) with missing dilutions, host species, and clone information. **HARD MISSING.**

4. **Cell authentication:** No STR or mycoplasma testing for synovial fibroblasts or HUVECs. **HARD MISSING.**

5. **Xenium custom panels:** Composition of custom add-on panels not specified. **HARD MISSING.**

6. **Delegation to unreviewed preprint:** Cell segmentation and CRISPR guide design delegated to Ref 1 (bioRxiv preprint), which is not yet peer-reviewed. **HARD MISSING** in current manuscript.

7. **Clinical metadata:** Age, sex, disease duration, and inclusion/exclusion criteria not provided for RA cohort. **HARD MISSING.**

8. **Vehicle specifications:** Final concentrations of DMSO, ethanol, or other vehicles in culture media not stated for any small-molecule inhibitor or agonist. **HARD MISSING.**

---

## Recommendations for Authors

- **Provide supplementary tables** with full Xenium panel composition, siRNA/gRNA sequences, gene signature (461 genes), and antibody specifications (dilutions, host, clone, RRID).
- **Deposit data:** Submit Xenium count matrices and bulk RNA-seq to GEO or equivalent; provide GitHub link for custom analysis code.
- **Authenticate cells:** Perform STR profiling and mycoplasma testing on synovial fibroblasts and HUVECs; report results.
- **Expand Methods:** Include full bulk RNA-seq protocol (platform, kit, depth, reference genome, alignment tool, FDR threshold) or cite a published protocol.
- **Clarify delegation:** Either move cell segmentation and CRISPR guide design into the main Methods (with full details) or wait for Ref 1 to be published before submission.
- **Complete clinical metadata:** Report age, sex, disease duration, serological status, and inclusion/exclusion criteria for the RA cohort.
- **Specify vehicles & concentrations:** State the vehicle (DMSO, ethanol, etc.) and final concentration in culture media for all small-molecule drugs.