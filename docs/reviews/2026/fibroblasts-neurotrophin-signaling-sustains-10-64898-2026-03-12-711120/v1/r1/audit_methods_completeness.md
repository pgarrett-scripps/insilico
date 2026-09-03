# Methods Completeness & Reagent Traceability Audit

## Triggered Categories

The following checklist categories are triggered by content in the manuscript:

1. **Antibodies/immunodetection** (WB, IHC, IF, RNAscope, ELISA)
2. **Cell lines/primary cells** (synovial fibroblasts, HUVECs)
3. **Human subjects/clinical** (synovial tissue biopsies, IRB approval)
4. **Chemicals/drugs/dosing** (neurotrophins, inhibitors, agonists)
5. **Oligos/plasmids/constructs** (siRNA, CRISPR-Cas9, lentiviral vectors)
6. **Genomics/sequencing/omics** (Xenium spatial transcriptomics, bulk RNA-seq, scRNA-seq reference)
7. **Microscopy/imaging** (RNAscope, immunofluorescence, immunohistochemistry, whole-mount staining)
8. **Cross-cutting** (sample size, statistics, software versions, data availability)

---

## Cross-Cutting Items

### Sample Size and Replication

| Item | Status | Finding |
|------|--------|---------|
| **Xenium cohort n** | **PRESENT** | 22 RA patients + 2 healthy donors, 46 total samples (paired pre/post for RA patients); 2,049,358 high-quality cells analyzed. Stated in Methods and Figure 1 legend. |
| **Cell culture experiments: n replicates** | **MISSING (HARD)** | Figures 3, 4, 5, 6 and supplementary figures show bar plots with individual data points labeled "biological replicates" but **no explicit statement of how many replicates per condition** (e.g., n=3, n=5). Figures S4, S6, S8, S9 similarly lack stated n. This is critical for reproducibility of in vitro work. |
| **Synovial explant experiments: n replicates** | **MISSING (HARD)** | Figure 6 (TRK inhibitor experiments) and Figure 4K show explant data with "individual data points represent biological replicates" but **no explicit n per treatment group**. How many patient samples? How many technical replicates per sample? |
| **Organoid/micromass experiments: n replicates** | **MISSING (HARD)** | Figures S5, S9 state "individual data points represent biological replicates" but do not specify n. |

### Statistical Tests and Error Bars

| Item | Status | Finding |
|------|--------|---------|
| **Error bar definition** | **PRESENT** | Consistently stated as "mean ± standard deviation (SD)" in figure legends (e.g., Figures 4, 6, S5, S9). |
| **Statistical test naming** | **PRESENT** | Tests named throughout: Wilcoxon matched-pairs signed-rank test (Figure 1G–H), two-tailed Student's t-test, one-way ANOVA with Bonferroni post-hoc correction. Stated in figure legends and Methods. |
| **P-value reporting** | **PRESENT** | P-values shown on graphs and in text (e.g., "p = 0.029", "p = 0.0031"). |

### Software, Tools, and Instrument Versions

| Item | Status | Finding |
|------|--------|---------|
| **Xenium platform** | **PRESENT** | "Xenium 5K Prime platform" named; protocols cited (CG000760 Rev A, CG000584 Rev F, CG000613 Rev A). |
| **Seurat version** | **PRESENT** | "Seurat v5.0.0" stated in Methods. |
| **Harmony version** | **PRESENT** | "Harmony v1.2.4" stated in Methods. |
| **UCell version** | **PRESENT** | "R package UCell" with GitHub link provided; used for signature scoring. |
| **Cellpose version** | **PRESENT** | "Cellpose" cited (ref 48); version not explicitly stated in Methods. |
| **scikit-image version** | **PRESENT** | "scikit-image" cited (ref 49); version not explicitly stated. |
| **ImageJ version** | **PRESENT** | "ImageJ" named in Methods; version not stated. |
| **GraphPad Prism version** | **PRESENT** | "GraphPad Prism version 10.4.1" stated in Statistical Analysis section. |
| **R software version** | **MISSING (SOFT)** | "R software" mentioned for single-cell analyses; version not stated. |
| **EVOS microscope model** | **PRESENT** | "EVOS M7000" named for imaging. |
| **AriaMX qPCR instrument** | **PRESENT** | "AriaMX Real Time PCR machine (Agilent)" named. |
| **Bio-Rad imaging system** | **PRESENT** | "Bio-Rad ChemiDoc imaging system" named for Western blots. |

### Data Availability

| Item | Status | Finding |
|------|--------|---------|
| **Data availability statement** | **MISSING (HARD)** | **No explicit data availability statement** in the manuscript. No mention of where Xenium data, bulk RNA-seq data, or processed datasets will be deposited (GEO, Zenodo, etc.). This is critical for spatial transcriptomics and RNA-seq work. |
| **Code availability statement** | **MISSING (HARD)** | **No statement on code availability**. Custom analysis pipelines (Seurat integration, UCell scoring, spatial analysis) are described but no GitHub repository, Zenodo link, or supplementary code is mentioned. |
| **Supplementary tables/data** | **PRESENT** | Tables S1–S3 referenced (neurotrophin receptor panel genes, RNAscope probes, primer list) but not shown in the provided manuscript text. Assumed to be available. |

---

## Antibodies/Immunodetection

### Western Blotting

| Antibody/Reagent | Vendor | Catalog # | Clone | Host/Clonality | Application | Dilution | Status |
|---|---|---|---|---|---|---|---|
| TrkA, TrkB, p-TrkA/TrkB | Cell Signaling Technology | #4638 | Not stated | Not stated | WB | 1:500 | **UNVERIFIABLE** |
| CNN1 (calponin) | Proteintech | #24855-1-AP | Not stated | Not stated | WB | Not stated | **MISSING (HARD)** |
| MYH11 | Proteintech | #21404-1-AP | Not stated | Not stated | WB | Not stated | **MISSING (HARD)** |
| NGF | Abcam | #ab52918 | Not stated | Not stated | WB | Not stated | **MISSING (HARD)** |
| GAPDH | Thermo Fisher Scientific | #MA5-15738 | Not stated | Not stated | WB | Not stated | **MISSING (HARD)** |
| β-actin | Cell Signaling Technology | #3700 | Not stated | Not stated | WB | Not stated | **MISSING (HARD)** |
| HRP-conjugated anti-Rabbit | Thermo Fisher Scientific | #32460 | Not stated | Not stated | WB (secondary) | Not stated | **MISSING (HARD)** |
| HRP-conjugated anti-Mouse | Thermo Fisher Scientific | #31430 | Not stated | Not stated | WB (secondary) | Not stated | **MISSING (HARD)** |
| HRP-conjugated anti-Goat | Thermo Fisher Scientific | #A16005 | Not stated | Not stated | WB (secondary) | Not stated | **MISSING (HARD)** |

**Finding:** Dilutions for most primary antibodies in Western blotting are not stated. Secondary antibody dilutions are not stated. Host species and clonality are not provided for any antibody. This blocks reproducibility of WB protocols.

### Immunohistochemistry (IHC)

| Antibody | Vendor | Catalog # | Application | Status |
|---|---|---|---|---|
| α-SMA (smooth muscle actin) | Not stated | Not stated | IHC | **MISSING (HARD)** |
| PECAM1 (CD31) | Not stated | Not stated | IHC | **MISSING (HARD)** |
| NGFR | Not stated | Not stated | IHC | **MISSING (HARD)** |
| TRKA | Not stated | Not stated | IHC | **MISSING (HARD)** |
| TRKB | Not stated | Not stated | IHC | **MISSING (HARD)** |
| TRKC | Not stated | Not stated | IHC | **MISSING (HARD)** |

**Finding:** IHC section states "Primary antibodies against smooth muscle actin (SMA), PECAM, NGFR, TRKA, TRKB, and TRKC...were used according to standard protocols at Brigham and Women's Hospital Pathology Core." **No vendor, catalog #, clone, dilution, or host species provided.** This is delegated to an institutional core facility, but the specific antibodies used are not traceable. **Status: MISSING (HARD).**

### Immunofluorescence (IF) / Whole-Mount Staining

| Antibody | Vendor | Catalog # | Clone | Host | Application | Dilution | Status |
|---|---|---|---|---|---|---|---|
| NGFR | Cell Signaling Technology | #4638 | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| NTRK1 | Cell Signaling Technology | #4638 | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| NTRK2 | Cell Signaling Technology | #4638 | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| NTRK3 | Cell Signaling Technology | #4638 | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| MYH11 | Proteintech | #21404-1-AP | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| CD31 | Biolegend | #303106 | Not stated | Not stated | IF | Not stated | **MISSING (HARD)** |
| AF555 anti-rabbit | Thermo Fisher | #A-21424 | Not stated | Not stated | IF (secondary) | Not stated | **MISSING (HARD)** |
| AF488 anti-rabbit | Thermo Fisher | #A11034 | Not stated | Not stated | IF (secondary) | Not stated | **MISSING (HARD)** |
| AF555 anti-goat | Thermo Fisher | #A110055 | Not stated | Not stated | IF (secondary) | Not stated | **MISSING (HARD)** |
| AF647 anti-rabbit | Thermo Fisher | #A32733 | Not stated | Not stated | IF (secondary) | Not stated | **MISSING (HARD)** |

**Finding:** Primary and secondary antibody dilutions for whole-mount IF are not stated. Host species and clonality missing for all. This is a **HARD missing** for reproducibility.

### RNAscope (In Situ Hybridization)

| Probe Target | Vendor | Catalog # / Assay ID | Status |
|---|---|---|---|
| NGFR, NTRK1, NTRK2, NTRK3, MYH11, RGS5, ACTA2, NGF, NOTCH3, PECAM1, and others | ACD Bio | Table 2 (referenced but not shown in provided text) | **UNVERIFIABLE** |

**Finding:** RNAscope probes are referenced in "Table 2: RNAScope probe List" but the table is not provided in the manuscript text. Probe catalog numbers and assay IDs cannot be verified. **Status: UNVERIFIABLE (HARD).** The manuscript states "Different probes for neurotrophins and mural cell markers were used (provided in Table 2)" but Table 2 is not included.

### ELISA

| Analyte | Vendor | Catalog # | Status |
|---|---|---|---|
| NGF secretion quantification | Not stated | Not stated | **MISSING (HARD)** |
| BDNF secretion | Implied but not explicitly stated | Not stated | **MISSING (HARD)** |
| NT3 secretion | Implied but not explicitly stated | Not stated | **MISSING (HARD)** |

**Finding:** Figure S3B and Figure 5C show ELISA quantification of NGF secretion (pg/ml) but no ELISA kit vendor, catalog #, or protocol is stated. **Status: MISSING (HARD).**

---

## Cell Lines and Primary Cells

### Synovial Fibroblasts

| Item | Status | Finding |
|------|--------|---------|
| **Source** | **PRESENT** | "Synovial tissue collected after patients undergoing arthroplasty or synovectomy procedures" from Brigham and Women's Hospital and Flinders Medical Center. |
| **RRID/CVCL** | **MISSING (SOFT)** | No RRID assigned to the fibroblast cell line. |
| **Authentication (STR)** | **MISSING (HARD)** | No STR profiling or authentication mentioned. |
| **Mycoplasma testing** | **MISSING (HARD)** | No mycoplasma testing reported. |
| **Culture media/supplements** | **PRESENT** | "Complete FLS media (DMEM supplemented with 10% fetal bovine serum, HEPES, MEM amino acids, L-glutamine, penicillin-streptomycin, nonessential MEM amino acids, 2-mercaptoethanol, and gentamicin)." |
| **Passage number** | **PRESENT** | "3 to 6 passages for experiments" stated. |

**Finding:** No authentication or mycoplasma testing reported. **Status: MISSING (HARD).**

### HUVECs (Human Umbilical Vein Endothelial Cells)

| Item | Status | Finding |
|------|--------|---------|
| **Source** | **PRESENT** | "HUVECs (Thermofisher)" stated. |
| **RRID/CVCL** | **MISSING (SOFT)** | No RRID provided. Thermofisher catalog # not given. |
| **Authentication** | **MISSING (HARD)** | No authentication mentioned. |
| **Mycoplasma testing** | **MISSING (HARD)** | Not reported. |
| **Culture media** | **PRESENT** | "EGM2 media consisting of EGM-Plus media (Lonza # CC-5035) supplemented with the EGM-plus bulletkit (Lonza, cc-3162)." |
| **Passage number** | **PRESENT** | "Passage 3-7" stated in co-culture methods. |

**Finding:** No authentication or mycoplasma testing. Thermofisher catalog # for HUVECs not provided. **Status: MISSING (HARD).**

---

## Human Subjects and Clinical

| Item | Status | Finding |
|------|--------|---------|
| **IRB approval** | **PRESENT** | "Brigham and Women's Hospital (MGB IRB no. 2019P002924) and Flinders Medical Center (Protocol#396.10)" stated. |
| **Informed consent** | **MISSING (HARD)** | No explicit statement that informed consent was obtained. |
| **Inclusion/exclusion criteria** | **MISSING (HARD)** | Not stated. What defines "RA patient"? What are exclusion criteria? |
| **Participant demographics** | **PARTIAL** | "22 RA patients and 2 healthy donors" stated; no age, sex, disease duration, medication history, or other demographics provided. |
| **Clinical outcome measures** | **PRESENT** | DAS28-ESR < 2.6 mentioned as remission criterion; treatment regimens (triple csDMARD or TNFi) described. |
| **Treatment duration** | **PRESENT** | "6-month post-treatment" stated. |
| **Trial registration** | **N/A** | Not an interventional trial; observational study of existing biopsies. |

**Finding:** No explicit informed consent statement. Inclusion/exclusion criteria not defined. Participant demographics (age, sex, disease duration, baseline disease activity) not provided. **Status: MISSING (HARD) for consent and criteria; MISSING (SOFT) for demographics.**

---

## Chemicals, Drugs, and Dosing

### Neurotrophins

| Reagent | Vendor | Catalog # | CAS / Identity | Concentration/Dose | Vehicle | Status |
|---|---|---|---|---|---|---|
| NGF (recombinant) | R&D Systems | #256-GF | Not stated | 1, 100 ng/ml | DMSO or PBS | **PRESENT** |
| BDNF (recombinant) | R&D Systems | #11166-BD | Not stated | 100 ng/ml | PBS | **PRESENT** |
| NT3 (recombinant) | R&D Systems | #267-N3-005 | Not stated | 50, 100 ng/ml | PBS | **PRESENT** |

**Finding:** Vendor and catalog # present; final vehicle concentration not stated (e.g., final % DMSO in culture media). **Status: PRESENT but SOFT missing on final vehicle concentration.**

### Small-Molecule Inhibitors

| Drug | Vendor | Catalog # | Target | Concentration | Status |
|---|---|---|---|---|---|
| GW-441756 (TrkA inhibitor) | Tocris | #2238 | TrkA | 1, 5, 10 µM | **PRESENT** |
| ANA-12 (TrkB inhibitor) | Tocris | #4781 | TrkB | 1, 5, 10 µM | **PRESENT** |
| GNF-5837 (TrkA/B/C inhibitor) | Tocris | #4559 | TrkA/B/C | 1, 5, 10 µM | **PRESENT** |
| Entrectinib (TRK inhibitor) | MedChemExpress | #HY-12678 | NTRK1/2/3 | Not explicitly stated for all experiments | **PARTIAL** |
| Larotrectinib (TRK inhibitor) | MedChemExpress | #HY-12866 | NTRK1/2/3 | Not explicitly stated for all experiments | **PARTIAL** |
| DAPT (γ-secretase inhibitor) | Tocris | #2634 | NOTCH | 10 µM | **PRESENT** |

**Finding:** Entrectinib and larotrectinib concentrations not explicitly stated for all experiments (e.g., Figure 6 explant experiments). Cell viability assay (Figure S9B) tests 0–100 µM but the concentration used in explant experiments is not stated. **Status: PARTIAL/MISSING (HARD) for entrectinib and larotrectinib in explant experiments.**

### Neurotrophin Agonists

| Drug | Vendor | Catalog # | Target | Concentration | Status |
|---|---|---|---|---|---|
| LM22B-10 (TrkB/C agonist) | Tocris | #6037 | TrkB/C | 1, 5, 10 µM | **PRESENT** |
| 7,8-DHF (TrkB agonist) | Tocris | #3826 | TrkB | 1, 5, 10 µM | **PRESENT** |

**Finding:** Concentrations stated. **Status: PRESENT.**

### Other Reagents

| Reagent | Vendor | Catalog # | Use | Status |
|---|---|---|---|---|
| DLL4-Fc (NOTCH ligand) | R&D Systems | #10185-D4 | Fibroblast stimulation | **PRESENT** (5 µg/ml) |
| Matrigel | Corning | #356231 | Organoid embedding | **PRESENT** |
| WST-1 (cell viability) | Millipore Sigma | #501594400 | Viability assay | **PRESENT** |
| Dispase II | Sigma | #494207801 | Tissue digestion | **PRESENT** (100 µg/ml) |
| DNase I | Sigma | #10104159001 | Tissue digestion | **PRESENT** (100 µg/ml) |
| Liberase TL | Sigma | #5401020001 | Tissue digestion | **PRESENT** (100 µg/ml) |

**Finding:** Concentrations and vendors generally present. **Status: PRESENT.**

---

## Oligos, Plasmids, and Constructs

### siRNA

| Target | Vendor | Assay ID / Catalog # | Sequence | Status |
|---|---|---|---|---|
| NGFR | Thermo Scientific | #S194655 | Not provided | **MISSING (HARD)** |
| NTRK1 | Thermo Scientific | #S534734 | Not provided | **MISSING (HARD)** |
| NTRK2 | Thermo Scientific | #n321595 | Not provided | **MISSING (HARD)** |
| NTRK3 | Thermo Scientific | #s9753 | Not provided | **MISSING (HARD)** |
| NOTCH3 | Thermo Scientific | #106100 | Not provided | **MISSING (HARD)** |

**Finding:** siRNA target sequences not provided. Assay IDs given but sequences needed for verification and off-target assessment. **Status: MISSING (HARD).**

### CRISPR-Cas9

| Target | Method | Delivery | Cas Variant | Validation | Status |
|---|---|---|---|---|---|
| NOTCH3 | CRISPR-Cas9 | P3 primary cell 4D-nucleofector X kit S (#V4XP-3032, Lonza) | Not stated (assumed SpCas9) | Not stated | **MISSING (HARD)** |
| Guide RNA design | Synthego design tool | Not stated | N/A | Not stated | **UNVERIFIABLE** |

**Finding:** Cas variant not explicitly stated (assumed SpCas9 but not confirmed). Guide RNA sequences not provided. No validation of knockout (e.g., Western blot, sequencing) shown in main text or supplementary. **Status: MISSING (HARD) for gRNA sequences and validation.**

### Lentiviral Vectors

| Construct | Vendor | Catalog # / ID | Insert | Promoter | Selection | Status |
|---|---|---|---|---|---|
| pLV-BsdCMV-hNGFR (N-terminal GFP-tag) | VectorBuilder | #VB230823-1657hvq | NGFR | CMV | Blasticidin | **PRESENT** |
| pLV-Bsd-CMV-EGFP (control) | VectorBuilder | #VB230502-1039MVR | EGFP | CMV | Blasticidin | **PRESENT** |
| Packaging mix | Thermo Fisher (Virapower) | Part of kit | N/A | N/A | N/A | **PRESENT** |

**Finding:** Vector IDs and vendors present. **Status: PRESENT.**

### Primers for qPCR

| Gene | Forward Primer Sequence | Reverse Primer Sequence | Status |
|---|---|---|---|
| All genes | Not provided in manuscript | Not provided in manuscript | **MISSING (HARD)** |

**Finding:** "The primer list is provided in Table 1" but Table 1 is not shown in the provided manuscript text. Primer sequences cannot be verified. **Status: UNVERIFIABLE (HARD).**

---

## Genomics, Sequencing, and Omics

### Xenium Spatial Transcriptomics

| Parameter | Value | Status |
|---|---|---|
| **Platform** | Xenium 5K Prime (10X Genomics) | **PRESENT** |
| **Sample type** | FFPE synovial tissue biopsies | **PRESENT** |
| **Panel** | Xenium Prime 5K Human Pan Tissue & Pathways Panel (PN-1000671) + custom add-on panels | **PRESENT** |
| **Custom panel genes** | "Genes encoding neurotrophin receptors" (Table S1–S3 referenced but not shown) | **UNVERIFIABLE** |
| **Cell segmentation** | Cellpose (ref 48) | **PRESENT** |
| **Total cells analyzed** | 2,049,358 high-quality cells | **PRESENT** |
| **Vascular cells subset** | 368,217 cells | **PRESENT** |
| **Quality control thresholds** | "Thresholded based on transcripts and features per cell; kept 2 million high quality cells" | **VAGUE** |
| **Integration method** | Harmony v1.2.4 | **PRESENT** |
| **Downstream analysis tools** | Seurat v5.0.0, Wilcoxon rank sum test (presto package) | **PRESENT** |
| **Reference dataset** | AMP RA/SLE Consortium scRNA-seq | **PRESENT** (ref 17) |
| **Batch handling** | Integrated over "sample-specific effects in PC using Harmony" | **PRESENT** |
| **Data repository** | Not stated | **MISSING (HARD)** |
| **Accession number** | Not stated | **MISSING (HARD)** |

**Finding:** 
- QC thresholds vague ("kept 2 million high quality cells" — what were the exclusion criteria?). 
- Custom panel genes (Tables S1–S3) not provided in manuscript.
- **No data repository or accession number stated.** Xenium data must be deposited in GEO or similar.
- **Status: MISSING (HARD) for data availability; UNVERIFIABLE for custom panel composition; VAGUE for QC thresholds.**

### Bulk RNA-Sequencing (NGFR-overexpressing fibroblasts)

| Parameter | Value | Status |
|---|---|---|
| **Platform** | Not stated | **MISSING (HARD)** |
| **Library prep kit** | Not stated | **MISSING (HARD)** |
| **Read length / mode** | Not stated | **MISSING (HARD)** |
| **Sequencing depth** | Not stated | **MISSING (HARD)** |
| **Reference genome** | Not stated | **MISSING (HARD)** |
| **Alignment tool** | Not stated | **MISSING (HARD)** |
| **Differential expression analysis** | "Identified drug response markers with differential expression analysis; top differentially expressed gene sets used to define NGFR-related gene markers" | **VAGUE** |
| **Repository accession** | Not stated | **MISSING (HARD)** |
| **Figure 5J output** | "461 upregulated genes" listed in RNA-seq of NGFR-overexpressing fibroblasts | **PRESENT** (but no raw data) |

**Finding:** Bulk RNA-seq methods are severely under-specified. No platform, library prep, depth, reference genome, alignment tool, or repository accession provided. Figure 5J shows a heatmap of differentially expressed genes but the underlying data and analysis pipeline are not described. **Status: MISSING (HARD) for all major parameters.**

### Single-Cell RNA-Seq Reference (AMP RA/SLE Consortium)

| Parameter | Value | Status |
|---|---|---|
| **Citation** | Ref 17 (Zhang et al., Nature 2023) | **PRESENT** |
| **Data availability** | Assumed in GEO (not verified from manuscript) | **UNVERIFIABLE** |

**Finding:** Reference dataset is published (ref 17) and presumably available, but the manuscript does not state where or provide an accession number. **Status: UNVERIFIABLE.**

---

## Microscopy and Imaging

### RNAscope (In Situ Hybridization)

| Parameter | Value | Status |
|---|---|---|
| **Instrument** | EVOS M7000 | **PRESENT** |
| **Assay kit** | RNAScope multiplex fluorescent V2 (ACD Bio, SOP 45-009A) | **PRESENT** |
| **Probes** | Table 2 (not provided) | **UNVERIFIABLE** |
| **Magnification** | 20x stated for some images | **PARTIAL** |
| **Objective NA** | Not stated | **MISSING (SOFT)** |
| **Detector type** | Not stated | **MISSING (SOFT)** |
| **Fluorophore panel** | Not explicitly stated (implied: DAPI, red, yellow, green) | **VAGUE** |
| **Image analysis software** | Cellpose (nuclei segmentation) + scikit-image (cell boundary expansion) + RANN (distance calculation) | **PRESENT** |
| **Gating/thresholding strategy** | "Cells with high PECAM1 expression labeled as endothelial cells; cells with high RGS5 and low MYH11 as RGS5+..." (90th percentile threshold) | **PRESENT** |

**Finding:** Probe list (Table 2) not provided. Fluorophore assignments not explicitly stated. Objective NA and detector type not stated. **Status: UNVERIFIABLE for probe list; MISSING (SOFT) for optical parameters.**

### Immunofluorescence (Whole-Mount Staining)

| Parameter | Value | Status |
|---|---|---|
| **Instrument** | EVOS M7000 | **PRESENT** |
| **Magnification** | 1.25x and 4x stated | **PRESENT** |
| **Objective NA** | Not stated | **MISSING (SOFT)** |
| **Detector type** | Not stated | **MISSING (SOFT)** |
| **Fluorophore panel** | AF555, AF488, AF647, DAPI | **PRESENT** |
| **Primary antibody dilutions** | Not stated | **MISSING (HARD)** |
| **Secondary antibody dilutions** | Not stated | **MISSING (HARD)** |
| **Blocking buffer** | 1% BSA in 0.1% Triton-X | **PRESENT** |
| **Incubation times/temps** | Primary overnight at 4°C; secondary not stated | **PARTIAL** |
| **Image analysis software** | ImageJ | **PRESENT** |
| **Quantification method** | Not detailed | **MISSING (SOFT)** |

**Finding:** Primary and secondary antibody dilutions not stated. **Status: MISSING (HARD).**

### Immunohistochemistry (IHC)

| Parameter | Value | Status |
|---|---|---|
| **Instrument** | EVOS M7000 | **PRESENT** |
| **Magnification** | 20x stated | **PRESENT** |
| **Objective NA** | Not stated | **MISSING (SOFT)** |
| **Antibodies** | Delegated to Brigham and Women's Hospital Pathology Core | **UNVERIFIABLE** |
| **Antibody dilutions** | Not stated | **MISSING (HARD)** |
| **Detection method** | "Standard protocols at Brigham and Women's Hospital Pathology Core" | **DELEGATED-UNVERIFIABLE** |
| **Image analysis** | ImageJ | **PRESENT** |

**Finding:** IHC methods delegated to institutional core facility; specific antibodies and dilutions not traceable. **Status: DELEGATED-UNVERIFIABLE (HARD).**

### Collagen Gel Contraction Assay (Figure 4D–F)

| Parameter | Value | Status |
|---|---|---|
| **Gel composition** | Collagen I | **PRESENT** |
| **Collagen vendor/catalog** | Not stated | **MISSING (HARD)** |
| **Gel dimensions** | Not stated | **MISSING (HARD)** |
| **Cell density** | Not stated | **MISSING (HARD)** |
| **Culture duration** | Not stated | **MISSING (HARD)** |
| **Measurement method** | "Percent contraction" (Figure 4F) | **VAGUE** |
| **Quantification software** | Not stated | **MISSING (HARD)** |

**Finding:** Collagen gel contraction assay is referenced as "a key function of VSMCs" (ref 12) but the protocol is not detailed in the manuscript. Methods section does not include a dedicated subsection for this assay. **Status: DELEGATED-DEAD (HARD).** The reference (ref 12) is cited but the manuscript does not provide sufficient detail to reproduce the assay independently.

---

## Protocol Provenance and Delegation

### Methods Delegated to Prior Publications

| Method | Cited Reference | Resolvability | Status |
|---|---|---|---|
| Synovial fibroblast cell line generation | Ref 14 | DOI/PMID resolvable (Wei et al., Nature 2020) | **DELEGATED-RESOLVABLE** |
| Synovial tissue organoid generation | Ref 1 | Cited as "our previous study"; appears to be a preprint (bioRxiv 2025.03.14.642821) | **DELEGATED-RESOLVABLE** |
| Collagen gel contraction assay | Ref 12 | Romay et al., J Clin Invest 2024 (resolvable) | **DELEGATED-RESOLVABLE** |
| Xenium data analysis (initial) | Ref 1 | Same preprint | **DELEGATED-RESOLVABLE** |
| Tissue digestion for fibroblast isolation | Described in-text with enzyme concentrations | N/A | **SELF-CONTAINED** |
| CRISPR-Cas9 protocol | "According to manufacturer's protocol" (Lonza kit) | Lonza protocol resolvable | **DELEGATED-RESOLVABLE** |
| Lentiviral transduction | "Virapower™ HiPerform™ Lentiviral FastTiter™ Gateway® Expression protocol (Thermo Fisher Scientific, #K534000)" | Thermo Fisher protocol resolvable | **DELEGATED-RESOLVABLE** |

**Finding:** Most delegated methods are resolvable to published papers or manufacturer protocols. However, some key methods (e.g., collagen gel contraction assay, IHC) are delegated without sufficient in-manuscript detail. **Status: Generally DELEGATED-RESOLVABLE, but HARD missing for in-manuscript detail on load-bearing methods.**

### Deviations from Cited Protocols

| Method | Cited Protocol | Stated Deviation | Status |
|---|---|---|---|
| Xenium analysis | Ref 1 | "Expanded the cohort to 22 patients...and included 2 healthy donors" | **PRESENT** (expansion noted) |
| NOTCH3 knockout | Lonza kit protocol | None stated | **PRESENT** (follows manufacturer) |
| Lentiviral transduction | Thermo Fisher protocol | None stated | **PRESENT** (follows manufacturer) |

**Finding:** Deviations from cited protocols are generally not explicitly stated, but the manuscript does note expansion of the Xenium cohort. **Status: PRESENT for major deviations; SOFT missing for minor procedural variations.**

---

## Summary of HARD Missing Items

| Category | Item | Impact |
|---|---|---|
| **Cell culture** | Biological replicate numbers (n) for in vitro experiments | Cannot reproduce exact experimental design |
| **Cell culture** | Synovial fibroblast authentication (STR) and mycoplasma testing | Cannot verify cell line identity/purity |
| **Cell culture** | HUVEC authentication and mycoplasma testing | Cannot verify cell line identity/purity |
| **Human subjects** | Informed consent statement | Ethical compliance unclear |
| **Human subjects** | Inclusion/exclusion criteria for RA patients | Cannot assess patient selection bias |
| **Antibodies (WB)** | Dilutions for primary and secondary antibodies | Cannot reproduce Western blots |
| **Antibodies (IF)** | Dilutions for primary and secondary antibodies | Cannot reproduce immunofluorescence |
| **Antibodies (IHC)** | Specific antibodies, vendors, catalog #, dilutions | Cannot reproduce IHC (delegated to core facility) |
| **RNAscope** | Probe list (Table 2) | Cannot verify probe identity |
| **ELISA** | Kit vendor, catalog #, protocol | Cannot reproduce ELISA |
| **Chemicals** | Entrectinib and larotrectinib concentrations in explant experiments | Cannot reproduce drug treatment experiments |
| **siRNA** | Target sequences | Cannot verify specificity or assess off-targets |
| **CRISPR** | Guide RNA sequences and knockout validation | Cannot verify NOTCH3 knockout |
| **Xenium** | Data repository and accession number | Cannot access raw spatial transcriptomics data |
| **Bulk RNA-seq** | Platform, library prep, depth, reference genome, alignment tool, repository accession | Cannot reproduce or access RNA-seq analysis |
| **qPCR primers** | Primer sequences (Table 1) | Cannot verify primer design or specificity |
| **Microscopy** | Objective NA, detector type, fluorophore assignments (RNAscope) | Cannot reproduce imaging conditions |
| **Microscopy** | Primary/secondary antibody dilutions (IF, IHC) | Cannot reproduce imaging |
| **Collagen assay** | Gel composition, collagen vendor, cell density, culture duration, quantification method | Cannot reproduce contractility assay |

---

## Summary of SOFT Missing Items

| Category | Item | Impact |
|---|---|---|
| **Software** | R version for single-cell analysis | Minor reproducibility impact |
| **Cell culture** | Synovial fibroblast RRID | Traceability reduced |
| **Cell culture** | HUVEC RRID and Thermofisher catalog # | Traceability reduced |
| **Human subjects** | Participant demographics (age, sex, disease duration) | Cannot assess cohort characteristics |
| **Chemicals** | Final vehicle concentration (DMSO %) in media | Minor reproducibility impact |
| **Microscopy** | Objective NA, detector type (IF, IHC) | Minor reproducibility impact |
| **Microscopy** | Image quantification methods | Minor reproducibility impact |

---

## Summary of UNVERIFIABLE Items

| Category | Item | Reason |
|---|---|---|
| **Antibodies (WB)** | TrkA/TrkB antibody sampler kit (#4638) | Catalog # refers to a kit; individual clone/host not stated in manuscript |
| **RNAscope** | Probe list (Table 2) | Table not provided in manuscript text |
| **Xenium** | Custom panel gene composition (Tables S1–S3) | Tables not provided in manuscript text |
| **qPCR primers** | Primer sequences (Table 1) | Table not provided in manuscript text |
| **Bulk RNA-seq** | Analysis pipeline and raw data | No repository accession; methods severely under-specified |
| **IHC** | Specific antibodies and protocols | Delegated to institutional core facility; not traceable from manuscript |
| **CRISPR** | Guide RNA design tool output | "Synthego design tool" mentioned but no sequences provided |

---

## Overall Assessment

**Data Availability:** No explicit statement on where Xenium spatial transcriptomics data, bulk RNA-seq data, or processed datasets will be deposited. This is a **HARD missing** for a manuscript heavily reliant on high-dimensional omics data.

**Code Availability:** No statement on availability of custom analysis code (Seurat integration, UCell scoring, spatial analysis pipelines). This is a **HARD missing** for computational work.

**Reproducibility Bottlenecks:**
1. **In vitro experiments:** Biological replicate numbers not stated for Figures 3, 4, 5, 6, and supplementary figures. Cannot determine statistical power or reproduce exact experimental design.
2. **Antibody protocols:** Dilutions missing for Western blotting, immunofluorescence, and immunohistochemistry. IHC delegated to institutional core without traceable antibody identities.
3. **Omics data:** Xenium data not deposited (no accession). Bulk RNA-seq severely under-specified (no platform, depth, reference genome, alignment tool, or repository). Custom panel composition (Tables S1–S3) not provided.
4. **Molecular tools:** siRNA target sequences, CRISPR guide RNA sequences, and qPCR primer sequences not provided (Tables 1–2 not shown).
5. **Drug experiments:** Entrectinib and larotrectinib concentrations not explicitly stated for key explant experiments (Figure 6).

**Strengths:**
- Xenium platform and analysis tools (Seurat, Harmony, UCell) well-specified with versions.
- Neurotrophin and inhibitor vendors and catalog numbers generally provided.
- Human subjects IRB approval documented.
- Statistical tests and error bar definitions clearly stated.