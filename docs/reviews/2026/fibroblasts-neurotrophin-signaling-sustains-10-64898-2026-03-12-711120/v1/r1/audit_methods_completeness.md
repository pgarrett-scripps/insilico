# Methods Completeness & Reagent Traceability Audit

## Triggered Categories

The manuscript contains work in the following areas:
- **Antibodies/immunodetection** (WB, IHC, IF, RNAscope, ELISA)
- **Cell lines/primary cells** (synovial fibroblasts, HUVECs)
- **Human subjects/clinical** (synovial tissue biopsies, patient cohort)
- **Chemicals/drugs/dosing** (neurotrophins, inhibitors, agonists)
- **Oligos/plasmids/constructs** (siRNA, CRISPR-Cas9, lentiviral vectors)
- **Genomics/sequencing/omics** (Xenium spatial transcriptomics, bulk RNA-seq, scRNA-seq reference)
- **Microscopy/imaging/flow** (RNAscope, immunofluorescence, immunohistochemistry, whole-mount imaging)
- **Computational/ML/modeling** (Xenium data analysis, cell typing, signature scoring)

---

## Cross-Cutting Items

### Sample Size (n) Reporting

**Status: PARTIALLY PRESENT, INCONSISTENT**

- **Xenium cohort**: "22 RA patients and 2 healthy donors, including 22 RA patients with paired pre- and post-treatment biopsies" — n is stated; total cells analyzed (2,049,358 high-quality cells, 368,217 vascular cells) reported. ✓
- **Cell culture experiments**: Most figures show "Individual data points represent biological replicates" but **n per group is rarely stated numerically in figure legends or methods**. Example: Fig. 4D–F (collagen gel contraction) — no explicit n given; Fig. 3D–E (siRNA knockdown) — no n stated. **HARD missing for reproducibility.**
- **Synovial explant studies**: Fig. 6C–G states "Individual data points represent biological replicates" but does not specify how many replicates per condition. **HARD missing.**
- **Organoid/micromass studies**: Fig. S5C and S9 similarly lack explicit n values. **HARD missing.**

### Statistical Tests & Error Bars

**Status: PRESENT BUT INCOMPLETE**

- **Named tests**: Wilcoxon matched-pairs signed-rank test (Fig. 1G–H), two-tailed Student's t-test, one-way ANOVA with Bonferroni correction stated repeatedly. ✓
- **Error bar definition**: Most figures state "mean ± standard deviation (SD)" or "mean ± SEM" — present. ✓
- **Missing**: No statement of whether error bars represent SD, SEM, or 95% CI in several figures (e.g., Fig. 4D–F caption says "mean ± SD" but some panels lack explicit statement). Minor inconsistency. **SOFT.**

### Software, Tool, and Instrument Versions

**Status: PARTIALLY PRESENT**

**Present:**
- Seurat v5.0.0 ✓
- Harmony v1.2.4 ✓
- Louvain algorithm (no version) — **unverifiable which implementation**
- presto package ✓
- UCell (R package, GitHub link provided) ✓
- Cellpose (cited, no version stated) — **SOFT missing**
- scikit-image (cited, no version stated) — **SOFT missing**
- RANN (R package, no version) ✓
- ImageJ (no version) — **SOFT missing**
- GraphPad Prism v10.4.1 ✓
- R software (no version) ✓
- Adobe software (no version) ✓
- BioRender (no version) ✓

**Missing:**
- Xenium instrument software version — **SOFT missing** (CG000584 Rev F cited but instrument control software version not stated)
- Python version for UCell/pyUCell — **SOFT missing**
- Microscope software (EVOS M7000) — **SOFT missing**

### Data Availability Statement

**Status: MISSING**

No explicit data-availability statement is provided in the manuscript. The authors state "Synovial tissue collected after patients undergoing arthroplasty or synovectomy procedures" and reference IRB protocols, but do not declare whether raw Xenium data, bulk RNA-seq, or scRNA-seq reference data will be deposited in a public repository (GEO, SRA, Zenium, etc.). **HARD missing.**

### Code Availability

**Status: MISSING**

No statement regarding availability of custom analysis code (Seurat pipeline, signature scoring, spatial analysis scripts). The manuscript references published packages (Seurat, Harmony, UCell) but does not state whether the authors' analysis pipeline will be shared (GitHub, Zenium, supplementary materials). **HARD missing.**

---

## Antibodies/Immunodetection

### Immunohistochemistry (IHC) & Immunofluorescence (IF)

**Status: INCOMPLETE**

**Present:**
- Primary antibodies listed in Methods (e.g., "NGFR, NTRK1, NTRK2, NTRK3 (Cell Signaling Technology, #4638)") — vendor and catalog # provided. ✓
- Secondary antibodies with catalog #s (e.g., "AF555 anti-rabbit, #A-21424") — vendor and catalog # present. ✓
- Application stated (IHC, IF, whole-mount) ✓

**Missing:**
- **Clone information**: For most antibodies, clone (monoclonal vs polyclonal) not stated. Example: "NGFR, NTRK1, NTRK2, NTRK3 (Cell Signaling Technology, #4638)" — single catalog # for four targets suggests a kit, but clone/specificity not detailed. **HARD missing.**
- **Dilutions**: Methods state "Primary antibodies against smooth muscle actin (SMA), PECAM, NGFR, TRKA, TRKB, and TRKC... were used according to standard protocols at Brigham and Women's Hospital Pathology Core" — **no dilutions given**. **HARD missing.**
- **Host species**: Not stated for most antibodies. **HARD missing.**
- **RRID**: No RRIDs provided for any antibody. **HARD missing.**

### Western Blot

**Status: INCOMPLETE**

**Present:**
- Antibodies listed: "TrkA and TrkB antibody sampler kit against TrkA, TrkB, p-TrkA/TrkB (Cell Signaling Technology, #4638, 1:500)" — vendor, catalog #, and dilution (1:500) provided. ✓
- Secondary antibodies with dilutions and catalog #s. ✓
- Loading control (GAPDH, β-actin) stated. ✓

**Missing:**
- **Clone/host**: Not stated for primary antibodies. **HARD missing.**
- **RRID**: None provided. **HARD missing.**
- **Membrane blocking reagent**: "Everyblot blocking buffer" — product name given but not concentration/incubation time. **SOFT.**
- **Antibody incubation conditions**: "overnight at 4°C" stated for primary; secondary "1 hour at room temperature" stated. ✓

### RNAscope (In Situ Hybridization)

**Status: INCOMPLETE**

**Present:**
- Assay kit: "RNAScope multiplex fluorescent V2 assay (ACD Bio, SOP 45-009A)" — vendor and protocol reference provided. ✓
- Probes listed in Table 2 (referenced but table not fully visible in manuscript text). Probe identities should be verifiable from ACD Bio catalog.
- Imaging: "EVOS M7000" — instrument stated. ✓

**Missing:**
- **Probe catalog #s**: Table 2 is referenced but not fully reproduced in the provided text. **Status unverifiable** — cannot confirm probe identities without seeing the table.
- **Probe sequences**: Not provided. **SOFT missing** (standard commercial probes, but sequences not stated).
- **Hybridization temperature/time**: Not stated. **SOFT missing.**
- **Quantification method**: "Cellpose" for nuclear segmentation, "scikit-image" for expansion — tools named but parameters not stated. **SOFT missing.**

### ELISA

**Status: INCOMPLETE**

**Present:**
- Assay: "ELISA quantification of NGF secretion levels (pg/ml)" — analyte and units stated. ✓
- Figure S3B and S8A show ELISA data.

**Missing:**
- **Kit vendor/catalog #**: Not stated. **HARD missing.**
- **Plate type/coating**: Not stated. **HARD missing.**
- **Detection antibody**: Not stated. **HARD missing.**
- **Standard curve**: Not described. **HARD missing.**

---

## Cell Lines & Primary Cells

### Synovial Fibroblasts (Primary)

**Status: INCOMPLETE**

**Present:**
- Source: "Synovial tissue samples were obtained from Brigham and Women's Hospital (MGB IRB no. 2019P002924) and Flinders Medical Center (Protocol#396.10)" — IRB approval stated. ✓
- Derivation method: "Synovial fibroblast cell lines were generated from the synovial tissue mentioned above using an established protocol" with reference to prior work. ✓
- Culture medium: "complete FLS media (DMEM supplemented with 10% fetal bovine serum, HEPES, MEM amino acids, L-glutamine, penicillin-streptomycin, nonessential MEM amino acids, 2-mercaptoethanol, and gentamicin)" — detailed. ✓
- Passage number: "3 to 6 passages for experiments" — stated. ✓

**Missing:**
- **Authentication (STR profiling)**: Not stated. **HARD missing.**
- **Mycoplasma testing**: Not stated. **HARD missing.**
- **RRID/CVCL**: Not provided. **HARD missing.**
- **FBS source/lot**: Not specified. **SOFT missing.**

### HUVECs (Human Umbilical Vein Endothelial Cells)

**Status: INCOMPLETE**

**Present:**
- Source: "HUVECs (Thermofisher)" — vendor stated. ✓
- Culture medium: "EGM2 media consisting of EGM-Plus media (Lonza # CC-5035) supplemented with the EGM-plus bulletkit (Lonza, cc-3162)" — detailed. ✓
- Passage: "passage 3-7" — stated. ✓

**Missing:**
- **Catalog #**: Thermofisher HUVEC product not fully identified (multiple HUVEC products exist). **HARD missing.**
- **Authentication**: Not stated. **HARD missing.**
- **Mycoplasma testing**: Not stated. **HARD missing.**
- **RRID**: Not provided. **HARD missing.**

---

## Human Subjects/Clinical

### IRB Approval & Informed Consent

**Status: PRESENT**

- IRB approvals: "Brigham and Women's Hospital (MGB IRB no. 2019P002924) and Flinders Medical Center (Protocol#396.10)" — specific protocol numbers provided. ✓
- Informed consent: Not explicitly stated whether written informed consent was obtained. **SOFT missing** (implied by IRB approval but not stated).

### Inclusion/Exclusion Criteria

**Status: MISSING**

- No inclusion/exclusion criteria stated for RA patient cohort. **HARD missing.**
- No disease activity criteria stated (e.g., DAS28 at baseline). **HARD missing.**
- Only post-hoc statement: "the interval increase in synovial microvascular density occurred in RA patients regardless of whether or not patients reached criteria for clinical remission, as defined by DAS28-ESR < 2.6, at 6 months after treatment" — remission definition given but baseline criteria not.

### Participant Demographics

**Status: INCOMPLETE**

- Age, sex, disease duration, baseline disease activity, medication history: **NOT PROVIDED**. **HARD missing.**
- Only stated: "22 RA patients and 2 healthy donors" — no demographic breakdown.
- Treatment groups: "triple csDMARD therapy (Hydroxychloroquine, methotrexate, and sulfasalazine) or TNFi (adalimumab)" — treatment types stated but not how many patients per group. **HARD missing.**

### Trial Registration

**Status: NOT APPLICABLE** (observational cohort, not an interventional trial).

---

## Chemicals/Drugs/Dosing

### Neurotrophins

**Status: INCOMPLETE**

**Present:**
- NGF: "recombinant NGF (256-GF, R&D Systems)" — vendor and catalog # provided. ✓
- BDNF: "recombinant BDNF (11166-BD, R&D Systems)" — vendor and catalog # provided. ✓
- NT3: "recombinant NT3 (267-N3-005, R&D Systems)" — vendor and catalog # provided. ✓
- Concentrations: "NGF (1, 100 ng/ml), BDNF (100 ng/ml), and NT3 (50, 100 ng/ml)" — stated. ✓
- Vehicle: "reconstituted in DMSO or PBS and diluted in media" — stated. ✓

**Missing:**
- **Final concentration of DMSO/PBS in culture**: Not stated. **SOFT missing.**
- **Incubation time**: "Fibroblasts were treated with NTs" — duration not always stated (e.g., Fig. 4 does not specify treatment duration). **SOFT missing.**

### Small-Molecule Inhibitors

**Status: INCOMPLETE**

**Present:**
- GW-441756 (TrkA inhibitor): "GW-441756 (#2238, Tocris, TrkA inhibitor)" — vendor, catalog #, target stated. ✓
- ANA-12 (TrkB inhibitor): "ANA12 (#4781, Tocris, TrkB inhibitor)" — vendor, catalog #, target stated. ✓
- GNF-5837 (pan-TRK inhibitor): "GNF 5837 (#4559, Tocris TrkA/BC inhibitor)" — vendor, catalog #, target stated. ✓
- Entrectinib: "Entrectinib (Cat. No.: HY-12678, MedChemExpress)" — vendor and catalog # provided. ✓
- Larotrectinib: "Larotrectinib (Cat. No.: HY-12866, MedChemExpress)" — vendor and catalog # provided. ✓
- DAPT (γ-secretase inhibitor): "DAPT (#2634, Tocris, 10 µM)" — vendor, catalog #, and concentration stated. ✓
- Concentrations: "1, 5, and 10 µM respectively" — stated. ✓

**Missing:**
- **Vehicle for inhibitors**: Not stated (DMSO assumed but not confirmed). **SOFT missing.**
- **Final DMSO concentration in culture**: Not stated. **SOFT missing.**
- **Incubation time**: Not always stated for each inhibitor. **SOFT missing.**

### Neurotrophin Agonists

**Status: INCOMPLETE**

**Present:**
- LM22B-10 (TrkB/C agonist): "LM22B 10 (#6037, Tocris, TrkB/C agonist)" — vendor, catalog #, target stated. ✓
- 7,8-DHF (TrkB agonist): "7-8 DHF (#3826, Tocris, TrkB agonist)" — vendor, catalog #, target stated. ✓
- Concentrations: "1, 5, and 10 µM respectively" — stated. ✓

**Missing:**
- **Vehicle**: Not stated. **SOFT missing.**
- **Incubation time**: Not stated. **SOFT missing.**

### Other Reagents

**Status: INCOMPLETE**

**Present:**
- DLL4-Fc: "recombinant DLL4-Fc (10185-D4, R&D Systems)" — vendor and catalog # provided. ✓
- Concentration: "5 µg/ml" — stated. ✓
- Matrigel: "Matrigel (Corning, Cat. 356231)" — vendor and catalog # provided. ✓

**Missing:**
- **Matrigel batch/lot**: Not stated. **SOFT missing** (can affect reproducibility).
- **FBS source/lot**: Not stated. **SOFT missing.**

---

## Oligos/Plasmids/Constructs

### siRNA

**Status: INCOMPLETE**

**Present:**
- siRNA targets: "siRNAs targeting Notch3 or neurotrophin receptors (NTRK1, NTRK2, NTRK3)" — targets stated. ✓
- Transfection reagent: "RNAiMax reagent (Life Technologies)" — vendor and product stated. ✓
- Incubation: "Cells were transfected for 2 days" — duration stated. ✓
- Specific siRNA IDs: "NGFR assay ID-S194655: NTRK1 assay ID-S534734: NTRK2 assay ID-n321595: NTRK3 assay ID-s9753, NOTCH3-106100" — Silencer Select assay IDs provided. ✓

**Missing:**
- **siRNA sequences**: Not provided (proprietary Silencer Select, but sequences should be obtainable from Thermo Fisher). **SOFT missing** (identifiable by assay ID).
- **Transfection efficiency**: Not stated. **SOFT missing.**
- **Off-target assessment**: Not stated. **SOFT missing.**

### CRISPR-Cas9

**Status: INCOMPLETE**

**Present:**
- Cas variant: "CRISPR-Cas9" — stated. ✓
- Delivery: "P3 primary cell 4D-nucleofector X kit S (#V4XP-3032, Lonza)" — vendor, kit, and catalog # provided. ✓
- gRNA design: "Guide RNAs were designed using Synthego design tool" — tool and reference cited. ✓
- Target: "NOTCH3 KO" — target stated. ✓

**Missing:**
- **gRNA sequence(s)**: Not provided. **HARD missing.**
- **Edit validation**: "NOTCH3 KO cells were generated" — no validation shown (e.g., sequencing, Western blot of NOTCH3 protein). **HARD missing** (claimed in text but not demonstrated).
- **Off-target assessment**: Not stated. **SOFT missing.**

### Lentiviral Vectors

**Status: INCOMPLETE**

**Present:**
- Vector: "pLV-BsdCMV-hNGFR, VectorBuilder, #VB230823-1657hvq" — vendor, plasmid name, and catalog # provided. ✓
- Control: "pLV-Bsd-CMV-EGFP (VectorBuilder, # VB230502-1039MVR)" — vendor and catalog # provided. ✓
- Packaging: "Virapower™ HiPerform™ Lentiviral FastTiter™ Gateway® Expression protocol (Thermo Fisher Scientific, #K534000)" — kit and protocol reference provided. ✓
- Selection: "Blasticidin S" (implied by "Bsd" in plasmid name) — not explicitly stated. **SOFT missing.**

**Missing:**
- **Promoter confirmation**: "CMV-driven" stated but no validation that CMV drives expression. **SOFT missing.**
- **GFP-tag confirmation**: "N-terminal GFP-tag" stated but no validation shown. **SOFT missing.**
- **Transduction efficiency**: Not stated. **SOFT missing.**
- **Titer**: Not stated. **SOFT missing.**

---

## Genomics/Sequencing/Omics

### Xenium Spatial Transcriptomics

**Status: INCOMPLETE**

**Present:**
- Platform: "Xenium 5K Prime platform" — stated. ✓
- Probe panels: "Xenium Prime 5K Human Pan Tissue & Pathways Panel (PN-1000671, 10X Genomics) and custom add-on panels" — vendor and catalog # provided. ✓
- Custom panels: "Table. S, 1 to 3" referenced but not fully visible in provided text. **Status unverifiable.**
- Sample preparation: "FEPE blocks and processed following the manufacturer's protocol (CG000760 Rev A, 10X Genomics)" — protocol reference provided. ✓
- Cell segmentation: "Cellpose" — tool named. ✓
- Quality control: "Following quality control and cell segmentation" — mentioned but thresholds not stated. **SOFT missing.**
- Total cells: "2,049,358 high-quality cells" — count stated. ✓
- Vascular cells: "368,217 cells" — count stated. ✓

**Missing:**
- **Read length/depth**: Not stated. **HARD missing.**
- **Number of genes profiled**: Not stated (5K panel implies ~5,000 but not confirmed). **SOFT missing.**
- **Sequencing platform/instrument**: Xenium is in-situ but underlying sequencing not detailed. **SOFT missing.**
- **Reference genome**: "single-cell reference dataset generated from the AMP RA/SLE Consortium" — reference cited but genome build not stated. **HARD missing.**
- **Alignment/analysis tool versions**: Seurat v5.0.0 stated, Harmony v1.2.4 stated, but Louvain algorithm implementation not specified. **SOFT missing.**
- **Repository accession**: No GEO, SRA, or Zenium accession provided. **HARD missing.**
- **QC thresholds**: "thresholded the high quality cells based on transcripts and features per cell" — thresholds not stated. **HARD missing.**

### Bulk RNA-Sequencing

**Status: INCOMPLETE**

**Present:**
- Mentioned: "Bulk RNA sequencing analysis of differentially expressed genes in NGFR-overexpressing versus GFP-control fibroblasts treated without NGF (100 ng/ml)" (Fig. 5J). ✓
- Differential expression: "top differentially expressed gene sets" — 461 upregulated genes identified. ✓

**Missing:**
- **Platform/instrument**: Not stated. **HARD missing.**
- **Library prep kit**: Not stated. **HARD missing.**
- **Read length/depth**: Not stated. **HARD missing.**
- **Alignment tool/version**: Not stated. **HARD missing.**
- **Reference genome/build**: Not stated. **HARD missing.**
- **Normalization method**: Not stated. **HARD missing.**
- **Statistical test for DE**: Not stated. **HARD missing.**
- **FDR threshold**: Not stated. **HARD missing.**
- **Repository accession**: Not provided. **HARD missing.**
- **Sample size (n replicates)**: Not stated. **HARD missing.**

### Single-Cell RNA-Seq Reference (AMP RA/SLE Consortium)

**Status: DELEGATED-RESOLVABLE**

- Reference: "single-cell reference dataset generated from the AMP RA/SLE Consortium" — cited as ref. 17 (Zhang et al., Nature 2023). ✓
- The reference is published and resolvable (PMID/DOI available). ✓
- **Note**: The manuscript uses this as a reference for cell-type annotation but does not re-analyze it. Delegated method is resolvable.

---

## Microscopy/Imaging/Flow

### Immunofluorescence Microscopy (Whole-Mount Organoids)

**Status: INCOMPLETE**

**Present:**
- Instrument: "EVOS M7000" — stated. ✓
- Magnification: "1.25x and 4X magnification" — stated. ✓
- Imaging software: "ImageJ software" — tool stated (no version). **SOFT missing.**
- Antibodies: Listed above (see Antibodies section). ✓

**Missing:**
- **Objective NA**: Not stated. **SOFT missing.**
- **Detector type**: Not stated (assumed fluorescence but not confirmed). **SOFT missing.**
- **Laser/illumination settings**: Not stated. **HARD missing.**
- **Exposure time/gain**: Not stated. **HARD missing.**
- **Fluorophore panel**: Antibodies listed but not organized as a formal panel. **SOFT missing.**
- **Image processing**: "Images were acquired... and analyzed using ImageJ software" — no processing steps detailed. **SOFT missing.**

### RNAscope Imaging

**Status: INCOMPLETE**

**Present:**
- Instrument: "EVOS M7000" — stated. ✓
- Magnification: "20x magnification" — stated. ✓
- Probes: Table 2 referenced. **Status unverifiable** (table not fully shown).

**Missing:**
- **Objective NA**: Not stated. **SOFT missing.**
- **Detector**: Not stated. **SOFT missing.**
- **Laser settings**: Not stated. **HARD missing.**
- **Exposure/gain**: Not stated. **HARD missing.**
- **Image processing**: "Images were acquired on an EVOS M7000" — no processing steps stated. **SOFT missing.**
- **Quantification gating strategy**: "Cellpose" and "scikit-image" used but full gating/thresholding strategy not provided. **HARD missing.**

### Immunohistochemistry Imaging

**Status: INCOMPLETE**

**Present:**
- Instrument: "EVOS M7000 imaging system" — stated. ✓
- Magnification: "20x magnification" — stated. ✓

**Missing:**
- **Objective NA**: Not stated. **SOFT missing.**
- **Detector**: Not stated. **SOFT missing.**
- **Laser/illumination**: Not stated. **HARD missing.**
- **Exposure/gain**: Not stated. **HARD missing.**
- **Image analysis**: "Images were analyzed using imageJ software" — no thresholding or quantification method stated. **HARD missing.**

### Flow Cytometry

**Status: NOT USED** (no flow cytometry in manuscript).

---

## Computational/ML/Modeling

### Xenium Data Analysis Pipeline

**Status: INCOMPLETE**

**Present:**
- Datasets: "46 synovial tissue biopsy samples (22 RA patients and 2 healthy donors, including 22 RA patients with paired pre- and post-treatment biopsies)" — sample composition stated. ✓
- Train/val/test split: Not applicable (no train/test split; all samples analyzed). ✓
- Architecture/algorithm: "Seurat v5.0.0 for quality control and data analysis" — tool and version stated. ✓
- Integration: "Harmony v1.2.4" — tool and version stated. ✓
- Clustering: "Louvain algorithm with resolution 0.3" — algorithm and parameter stated, but implementation not specified. **SOFT missing.**
- Hyperparameters: "top 50 PCs" — stated. ✓
- Normalization: "log-transforming the transcript counts for each sample, with the median number of detected transcripts from both Xenium and AMP scRNA-seq reference serving as the scaling factor" — method stated. ✓
- Signature scoring: "UCell rank-based scoring method" — tool and method stated. ✓

**Missing:**
- **Random seed(s)**: Not stated. **HARD missing.**
- **Hardware/compute environment**: Not stated. **SOFT missing.**
- **Library versions**: Seurat v5.0.0, Harmony v1.2.4 stated; R version not stated. **SOFT missing.**
- **Code availability**: No GitHub, supplementary code, or data repository link provided. **HARD missing.**
- **QC thresholds**: "thresholded the high quality cells based on transcripts and features per cell" — specific thresholds not stated. **HARD missing.**
- **Batch handling**: "integrated over sample-specific effects in the PC using Harmony" — method stated but batch variable not explicitly named. **SOFT missing.**

### Cell-Type Annotation

**Status: INCOMPLETE**

**Present:**
- Reference: "AMP RA/SLE Consortium" single-cell reference — cited. ✓
- Method: "Cell type labels were assigned to each cluster based on known function state and lineage markers" — approach stated. ✓
- Marker genes: "Heatmap showing expression of marker genes used to define the identified cell clusters" (Fig. 1B, 1D) — shown visually. ✓

**Missing:**
- **Annotation algorithm**: Not stated (assumed manual gating by marker expression but not confirmed). **SOFT missing.**
- **Confidence/probability scores**: Not provided. **SOFT missing.**
- **Validation**: No independent validation of cell-type assignments stated. **SOFT missing.**

### Differential Expression Analysis

**Status: INCOMPLETE**

**Present:**
- Test: "Wilcoxon rank sum test as implemented in the presto package" — test and tool stated. ✓
- Tool: "presto package" — stated. ✓

**Missing:**
- **FDR correction**: Not stated (assumed but not confirmed). **HARD missing.**
- **Log-fold-change threshold**: Not stated. **SOFT missing.**
- **P-value threshold**: Not stated. **SOFT missing.**

### Signature Scoring (NGF/NGFR Gene Signature)

**Status: INCOMPLETE**

**Present:**
- Method: "UCell rank-based scoring approach" — tool and method stated. ✓
- Gene set: "461 upregulated genes from RNA-sequencing" — size stated. ✓
- Source: "Bulk RNA-seq for the organoid with drug treatment and without drug treatment" — data source stated. ✓

**Missing:**
- **Gene list**: The 461 genes not provided (supplementary table not shown). **HARD missing.**
- **UCell parameters**: No parameters (e.g., window size, rank threshold) stated. **SOFT missing.**
- **Validation**: No independent validation of signature. **SOFT missing.**

---

## Protocol Provenance & Delegation

### Methods Delegated to Prior Publications

**Status: MIXED (RESOLVABLE, UNVERIFIABLE, AND DEAD)**

1. **Synovial fibroblast derivation**: "using an established protocol" → ref. 14 (Wei et al., Nature 2020, PMID 32433574). **Delegated-resolvable** (published, DOI available). ✓

2. **Xenium data analysis**: "as outlined in our earlier published work" → ref. 1 (Bhamidipati et al., bioRxiv 2025). **Delegated-unverifiable** (preprint, not peer-reviewed; contents cannot be confirmed from this manuscript alone). ⚠️

3. **Organoid culture**: "as previously described" → ref. 1 (same bioRxiv preprint). **Delegated-unverifiable**. ⚠️

4. **Collagen gel contraction assay**: "as previously described" → ref. 12 (Romay et al., J Clin Invest 2024, PMID 38552715). **Delegated-resolvable** (published). ✓

5. **Synovial tissue explant system**: "en-bloc synovial tissue explant system as in ref. 1" → ref. 1 (bioRxiv preprint). **Delegated-unverifiable**. ⚠️

6. **CRISPR-Cas9 guide RNA design**: "Guide RNAs were designed using Synthego design tool" → ref. 1 (bioRxiv preprint). **Delegated-unverifiable**. ⚠️

7. **Lentiviral protocol**: "Virapower™ HiPerform™ Lentiviral FastTiter™ Gateway® Expression protocol (Thermo Fisher Scientific, #K534000)" — **Delegated-resolvable** (commercial kit with published protocol). ✓

### Deviations from Cited Protocols

**Status: NONE EXPLICITLY STATED**

No "as described, except..." statements found. Unclear whether methods exactly match cited protocols or have been modified.

---

## Summary of HARD Missing Items

| Category | Item | Severity |
|----------|------|----------|
| **Cross-cutting** | Data availability statement (Xenium, RNA-seq, scRNA-seq) | HARD |
| **Cross-cutting** | Code availability statement | HARD |
| **Cross-cutting** | Sample size (n) for cell culture and explant experiments | HARD |
| **Antibodies** | Clone information (monoclonal/polyclonal) for all antibodies | HARD |
| **Antibodies** | Dilutions for IHC/IF primary antibodies | HARD |
| **Antibodies** | Host species for antibodies | HARD |
| **Antibodies** | RRID for all antibodies | HARD |
| **Antibodies** | ELISA kit vendor, catalog #, detection antibody | HARD |
| **Cell lines** | STR authentication for synovial fibroblasts | HARD |
| **Cell lines** | Mycoplasma testing for synovial fibroblasts | HARD |
| **Cell lines** | RRID/CVCL for synovial fibroblasts | HARD |
| **Cell lines** | HUVEC catalog # (full product ID) | HARD |
| **Cell lines** | HUVEC authentication | HARD |
| **Cell lines** | HUVEC mycoplasma testing | HARD |
| **Cell lines** | HUVEC RRID | HARD |
| **Human subjects** | Inclusion/exclusion criteria for RA cohort | HARD |
| **Human subjects** | Participant demographics (age, sex, disease duration, baseline DAS28) | HARD |
| **Human subjects** | Number of patients per treatment group | HARD |
| **Oligos/constructs** | gRNA sequence(s) for NOTCH3 CRISPR-Cas9 | HARD |
| **Oligos/constructs** | NOTCH3 knockout validation (sequencing or Western blot) | HARD |
| **Genomics** | Read length and sequencing depth for Xenium | HARD |
| **Genomics** | Reference genome build for Xenium analysis | HARD |
| **Genomics** | QC thresholds for Xenium cell filtering | HARD |
| **Genomics** | Repository accession for Xenium data (GEO/SRA/Zenium) | HARD |
| **Genomics** | Bulk RNA-seq platform, library prep, depth, alignment tool, reference genome | HARD |
| **Genomics** | Bulk RNA-seq FDR threshold and statistical test | HARD |
| **Genomics** | Bulk RNA-seq repository accession | HARD |
| **Genomics** | Bulk RNA-seq sample size (n replicates) | HARD |
| **Microscopy** | Laser/illumination settings for IF and RNAscope | HARD |
| **Microscopy** | Exposure time/gain for IF and RNAscope | HARD |
| **Microscopy** | Quantification gating/thresholding strategy for RNAscope | HARD |
| **Microscopy** | Image analysis method for IHC (thresholding, quantification) | HARD |
| **Computational** | Random seed(s) for Seurat/Harmony analysis | HARD |
| **Computational** | Code availability (GitHub or supplementary) | HARD |
| **Computational** | FDR correction method for differential expression | HARD |
| **Computational** | NGF/NGFR gene signature list (461 genes) | HARD |
| **Protocol delegation** | Xenium analysis protocol (ref. 1 is bioRxiv preprint, unverifiable) | HARD |
| **Protocol delegation** | Organoid culture protocol (ref. 1 is bioRxiv preprint, unverifiable) | HARD |
| **Protocol delegation** | Synovial tissue explant protocol (ref. 1 is bioRxiv preprint, unverifiable) | HARD |

---

## Summary of SOFT Missing Items

| Category | Item | Severity |
|----------|------|----------|
| **Cross-cutting** | Software versions (Cellpose, scikit-image, ImageJ, R, Python) | SOFT |
| **Antibodies** | Membrane blocking reagent concentration/incubation time (WB) | SOFT |
| **Cell lines** | FBS source/lot | SOFT |
| **Chemicals** | Final DMSO concentration in culture media | SOFT |
| **Chemicals** | Incubation time for inhibitors/agonists | SOFT |
| **Chemicals** | Matrigel batch/lot | SOFT |
| **Oligos** | siRNA sequences (identifiable by assay ID but not provided) | SOFT |
| **Oligos** | siRNA transfection efficiency | SOFT |
| **Oligos** | Off-target assessment for siRNA/CRISPR | SOFT |
| **Oligos** | Lentiviral titer and transduction efficiency | SOFT |
| **Genomics** | Number of genes profiled (5K panel assumed but not confirmed) | SOFT |
| **Genomics** | Louvain algorithm implementation specification | SOFT |
| **Genomics** | Batch variable naming for Harmony integration | SOFT |
| **Microscopy** | Objective NA for all imaging | SOFT |
| **Microscopy** | Detector type for IF and RNAscope | SOFT |
| **Microscopy** | Fluorophore↔marker panel organization | SOFT |
| **Microscopy** | Image processing steps | SOFT |
| **Computational** | Hardware/compute environment | SOFT |
| **Computational** | Cell-type annotation algorithm details | SOFT |
| **Computational** | Cell-type confidence/probability scores | SOFT |
| **Computational** | Log-fold-change and p-value thresholds for DE | SOFT |
| **Computational** | UCell signature scoring parameters | SOFT |
| **Human subjects** | Informed consent statement (implied but not explicit) | SOFT |

---

## Unverifiable Items (Require Author Clarification)

1. **Table S1–3 (Custom Xenium panels)**: Referenced but not fully shown in provided manuscript text. Cannot verify probe identities, gene counts, or panel composition.
2. **Table 1 (Primer list)**: Referenced but not shown. Cannot verify primer sequences or specificity.
3. **Table 2 (RNAscope probe list)**: Referenced but not shown. Cannot verify probe identities or sequences.
4. **Ref. 1 (Bhamidipati et al., bioRxiv 2025)**: Multiple load-bearing methods delegated to this preprint (Xenium analysis, organoid culture, synovial explant protocol, CRISPR gRNA design). Preprint not yet peer-reviewed; contents cannot be confirmed from this manuscript alone.

---

## Conclusion

This manuscript has **extensive missing details** in reagent traceability, cell-line authentication, human-subject demographics, genomics metadata, and computational reproducibility. The most critical gaps are:

- **No data or code availability statement** (HARD)
- **No sample size (n) for most cell culture and explant experiments** (HARD)
- **Incomplete antibody specifications** (clone, host, dilution, RRID) (HARD)
- **No cell-line authentication or mycoplasma testing** (HARD)
- **No human-subject demographics or inclusion/exclusion criteria** (HARD)
- **Bulk RNA-seq completely unspecified** (platform, depth, alignment, FDR, accession) (HARD)
- **Xenium analysis missing QC thresholds, reference genome build, and repository accession** (HARD)
- **Microscopy imaging settings (laser, exposure, gain) not provided** (HARD)
- **CRISPR-Cas9 gRNA sequences and knockout validation missing** (HARD)
- **Multiple load-bearing methods delegated to unverifiable bioRxiv preprint** (HARD)

An independent group would **not be able to reproduce this work** without substantial author clarification and data deposition.