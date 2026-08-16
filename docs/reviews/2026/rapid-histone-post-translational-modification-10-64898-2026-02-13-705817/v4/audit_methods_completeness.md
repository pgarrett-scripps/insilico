# Methods Completeness & Reagent Traceability Audit

**Manuscript:** "Using Alternative Proteases and Tandem Mass Tags" (RIPUP workflow)

**Auditor role:** Methods Completeness & Reagent Traceability Auditor

**Date of audit:** Based on manuscript version provided

---

## Categories Triggered and Checked

The following checklist categories are triggered by the manuscript content:

1. **Cross-cutting items** (applies to all manuscripts)
2. **Cell lines** (HEK293T used)
3. **Model organisms / in vivo** (rats used)
4. **Chemicals/drugs/dosing** (NAM treatment, propionic anhydride, TMT labels, urea, TCEP)
5. **Mass spectrometry (proteomics)** (central to the paper)
6. **Computational/ML/modeling** (HiP-Frag, FragPipe, custom R scripts, limma, kNN imputation)
7. **Protocol-provenance rule** (several methods delegated by reference)

Categories **not** triggered (no evidence in manuscript): Antibodies/immunodetection, Human subjects/clinical, Oligos/plasmids/constructs, Genomics/sequencing (beyond MS), Microscopy/imaging/flow.

---

## 1. Cross-Cutting Items

### 1.1 Sample size (n) with what n represents

| Item | Status | Finding |
|---|---|---|
| n stated for HEK293T experiments | **Present** | "n = 4 digestion replicates/condition" (Methods, MS sample preparation); "n = 3 digestion replicates/condition" for NAM experiment |
| n stated for rat hippocampal experiments | **Present** | "n = 5" (Methods, rat tissue section); "detected in ≥2 biological replicates" (Data analysis) |
| Biological vs technical replicate distinction | **Present** | Digestion replicates are technical replicates of the same histone extraction; rat n = 5 are biological replicates (individual animals) |

**Assessment:** Adequate. The distinction between biological and technical replicates is explicit.

---

### 1.2 Named statistical test and error bar definition

| Item | Status | Finding |
|---|---|---|
| Statistical test named | **Present** | "limma package with empirical Bayes moderated t-statistics"; "Benjamini–Hochberg procedure" (Data analysis) |
| Error bars defined | **Missing** | No figure legend states what error bars represent (SD/SEM/CI). Figure 2A shows CV distributions but no error bar definition is given. Figure 4A states "Error bars represent standard deviation across n = 4 digestion replicates" — this is present for Figure 4 only. Other figures (e.g., Figure 2C, 5A–D) show bar plots without error bars or dispersion metrics. |
| Severity | **SOFT** | The statistical test is named; error bar definition is partially present (Figure 4) but not consistently across all figures. |

**Assessment:** The limma/BH procedure is named. Error bar definitions are inconsistent across figures.

---

### 1.3 Software, tool, and instrument versions

| Item | Status | Finding |
|---|---|---|
| FragPipe version | **Present** | "FragPipe (v24.0)" (Data analysis) |
| RStudio version | **Present** | "RStudio 2025.09.2+, Build 418" (Data analysis) |
| Skyline version | **Present** | "Skyline (v 26.1.0.057 (c07debd50))" (Data analysis) |
| Mass spectrometer | **Present** | "Thermofisher Scientific Fusion Lumos Tribrid Mass Spectrometer" (LC-MS/MS section) |
| NanoLC system | **Present** | "Evosep One nanoLC system (Evosep)" (LC-MS/MS section) |
| Column | **Present** | "custom-packed analytical capillary column (25 cm length, 150 nm internal diameter) containing Waters BEH C18 resin (1.7 µm particle size)" |
| HCD collision energy (non-TMT) | **Present** | "fixed collision energy of 30%" |
| HCD collision energy (TMT) | **Present** | "stepped normalized collision energy (NCE) of 30%, 40%, and 50%" |
| HiP-Frag version | **Missing** | Referenced as "HiP-Frag workflow" (Vai et al. 2025) but no version number is given. The workflow is described as "following the recommended guidelines for the HiP-Frag workflow, with some modifications" — the specific version of HiP-Frag is not stated. |
| Bioconductor 'impute' package version | **Missing** | "k-nearest neighbors (kNN, k = 10; Bioconductor 'impute' package)" — no version given. |
| R version | **Missing** | RStudio version given but not the underlying R version. |
| Evosep gradient method | **Present** | "15 spd LC gradient (88 minutes) at 220 nL/min" |
| Severity for HiP-Frag version | **SOFT** | The workflow is described and the underlying search engine (FragPipe v24.0) is versioned; HiP-Frag is a workflow within FragPipe. |

**Assessment:** Most instrument and software versions are present. HiP-Frag version and R version are minor gaps.

---

### 1.4 Data-availability statement

| Item | Status | Finding |
|---|---|---|
| Data availability statement | **Present** | "The MS raw data files, annotations, Sample and Data Relationship Format (SDRF-Proteomics), and FragPipe search results have been deposited to the ProteomeXchange Consortium... with the dataset identifier PXD073683" (Data availability) |
| PRIDE partner repository named | **Present** | "via the PRIDE partner repository" |
| Severity | **SOFT** (availability statements are SOFT per instructions) | Present and specific. |

---

### 1.5 Code availability (custom analysis)

| Item | Status | Finding |
|---|---|---|
| Custom R scripts availability | **Present** | "The custom R scripts used for data analysis are available at: https://github.com/NataliePTurner/Histone-RIPUP" (Data availability) |
| Severity | **SOFT** | Present. |

---

## 2. Cell Lines (HEK293T)

| Item | Status | Finding |
|---|---|---|
| Source | **Missing** | "HEK293T cells were cultured..." — no vendor or source institution is stated. |
| RRID/CVCL | **Missing** | No RRID or CVCL identifier given. |
| Authentication (STR) | **Missing** | No statement of STR authentication. |
| Mycoplasma testing | **Missing** | No statement of mycoplasma testing. |
| Media/supplements | **Present** | "Dulbecco's Modified Eagle Medium + GlutaMAX™ (DMEM; catalog number 10566016, Gibco™, Thermo Fisher Scientific) supplemented with 1% Penicillin-streptomycin (10,000 IU/mL, catalog number 15140122, Thermo Fisher Scientific) and 10% fetal bovine serum" |
| Culture conditions | **Present** | "humidified incubator at 37 °C and 5% CO2" |
| Severity | **HARD** for source/RRID; **SOFT** for authentication/mycoplasma | Source and RRID are required for traceability. Authentication and mycoplasma status are recommended but not strictly required for reproducibility of the protocol itself. |

**Assessment:** The cell line source is not stated, which is a HARD gap for traceability. Authentication and mycoplasma testing are not mentioned.

---

## 3. Model Organisms / In Vivo (Rats)

| Item | Status | Finding |
|---|---|---|
| Species + strain | **Present** | "Adult male Sprague-Dawley rats" (Methods) |
| Source | **Present** | "Charles River Laboratories, Raleigh, NC" |
| Sex | **Present** | "male" |
| Age | **Present** | "446 ± 17.8 g" (weight given; age not explicitly stated but weight is a standard proxy) |
| n per group | **Present** | "n = 5" |
| IACUC protocol # | **Present** | "approved by the Scripps Research Institute (TSRI) Animal Care and Use Committee (IACUC #09-0006)" |
| Genotype/background | **Present** | "Sprague-Dawley" (outbred, wild-type implied) |
| Randomization/blinding statement | **Missing** | No statement of randomization or blinding for the rat experiments. |
| Housing | **Missing** | "temperature- and humidity-controlled room (12 h reverse light cycle)" — housing conditions partially described but cage type, group size per cage, and enrichment are not stated. |
| Power justification | **Missing** | No power calculation or justification for n = 5. |
| Severity | **HARD** for randomization/blinding; **SOFT** for housing and power | Randomization/blinding is a HARD item per the checklist. Housing details and power justification are SOFT. |

**Assessment:** Most animal details are present. Randomization/blinding is missing.

---

## 4. Chemicals / Drugs / Dosing

### 4.1 Nicotinamide (NAM)

| Item | Status | Finding |
|---|---|---|
| Identity traceable | **Present** | "Millipore Sigma, catalog number N0636" |
| Dose/concentration | **Present** | "3 mM or 10 mM NAM" |
| Route/mode | **Present** | "complete media supplemented with 3 mM or 10 mM NAM" (in culture media) |
| Vehicle + final concentration | **Present** | "complete media" (DMEM + 10% FBS + 1% Pen-Strep); final concentration stated as 3 mM or 10 mM |
| Schedule | **Present** | "Cells were cultured for a further 18 h" |

**Assessment:** Complete.

---

### 4.2 Propionic anhydride (derivatization)

| Item | Status | Finding |
|---|---|---|
| Identity traceable | **Missing** | "The propionylation reagent was prepared as previously described" — no vendor, catalog number, or CAS number for propionic anhydride is given. |
| Protocol provenance | **Unverifiable** | "as previously described" resolves to reference [1] (Sidoli et al. 2016) and [2] (Garcia et al. 2007). Both are published protocols that plausibly contain the preparation method. However, the manuscript does not state the vendor or catalog number for propionic anhydride itself. |
| Severity | **SOFT** | The protocol is delegated to a resolvable reference; the reagent identity is implied by the protocol name. However, a vendor/catalog number would improve traceability. |

---

### 4.3 TMT labels

| Item | Status | Finding |
|---|---|---|
| Identity traceable | **Present** | "TMT10-126" and "TMT10-131 (cat no 90309, Thermo Scientific)" |
| Monoisotopic mass | **Present** | "229.162932 Da" |
| Labeling ratio | **Present** | "peptide:TMT ratio 1:8" |
| Solvent conditions | **Present** | "final concentration of anhydrous acetonitrile = 44%" |
| Quenching | **Present** | "1 µL of 5% hydroxylamine... 15 min at RT" |

**Assessment:** Complete.

---

### 4.4 Other reagents

| Item | Status | Finding |
|---|---|---|
| Arg-C Ultra | **Present** | "MS grade, Cat number: VA1831, Promega™" |
| r-Chymotrypsin | **Present** | "rChymoselect, MS grade, Cat Number: CS3332042, Promega™" |
| Trypsin | **Present** | "Trypsin Gold, MS Grade, Promega, V5280" |
| Urea | **Present** | "2 M Urea" (concentration given; vendor not stated — minor) |
| TCEP | **Present** | "5 mM TCEP" (concentration given; vendor not stated — minor) |
| AMBIC | **Present** | "100 mM ammonium bicarbonate (AMBIC)" (concentration given; vendor not stated — minor) |
| TEAB | **Present** | "100 mM TEAB pH 8.5" (concentration given; vendor not stated — minor) |

**Assessment:** Enzymes are fully traceable. Buffers are identified by name and concentration but vendors are not stated — this is acceptable for common reagents.

---

## 5. Mass Spectrometry (Proteomics)

| Item | Status | Finding |
|---|---|---|
| Instrument + acquisition mode | **Present** | "Thermofisher Scientific Fusion Lumos Tribrid Mass Spectrometer... operated in positive ion mode"; DDA mode described ("Full MS scans... cycle time was 3 s") |
| Sample prep/digestion | **Present** | Detailed digestion conditions in Tables S1 and S2; enzyme-to-substrate ratios stated (Arg-C Ultra 1:100, 1:50, 1:10; r-Chymotrypsin 1:40, 1:10; Trypsin 1:10) |
| Enrichment | **N/A** | No enrichment step used (whole histone extracts) |
| Search engine + version | **Present** | "FragPipe (v24.0)" |
| Database + version | **Present** | "restricted database containing extracted human or rat histone sequences, contaminants and decoys (Homo sapiens: 342 sequences, 171 decoys; Rattus norvegicus: 292 entries, 146 decoys; contaminants lists were derived from and curated by Cambridge Centre for Proteomics (CCP) cRAP)" — database composition described; specific UniProt release/version not stated. |
| FDR | **Present** | "1% FDR at the peptide and PSM level" |
| Modifications | **Present** | "Lists of variable modifications and detailed mass offsets are provided in SI Table S1" |
| Tolerances | **Present** | "precursor mass tolerance was set to 10 ppm"; "fragment mass tolerance was within 20 ppm" (stated in Figure 6 legend) |
| Repository accession | **Present** | "PXD073683" (PRIDE/ProteomeXchange) |
| Quant method | **Present** | "Label-free quantification (LFQ) and match-between-runs (MBR) were enabled"; "Peptidoform-level quantitation was performed in FragPipe by disabling 'MaxLFQ' and 'normalize intensity across runs'" |
| Replicates | **Present** | "n = 4 per condition for HEK293T samples; n = 5 for rat hippocampal samples" |
| Database version (UniProt release) | **Missing** | The database is described by sequence count and source (CCP cRAP) but the specific UniProt release or download date is not stated. |
| Severity for database version | **SOFT** | The database composition is described in sufficient detail that a competent lab could reconstruct it, but the exact release version is not pinned. |

**Assessment:** Mass spectrometry methods are thoroughly described. The only minor gap is the exact database release version.

---

## 6. Computational / ML / Modeling

| Item | Status | Finding |
|---|---|---|
| Dataset(s) with version | **Present** | MS raw files deposited at PXD073683; database described (see above) |
| Train/val/test split | **N/A** | No machine learning model trained; statistical analysis only |
| Architecture/algorithm | **N/A** | No ML model |
| Hyperparameters | **N/A** | No ML model |
| Training procedure | **N/A** | No ML model |
| Library versions | **Partial** | RStudio version given; Bioconductor 'impute' package named but not versioned; limma named but not versioned |
| Hardware | **Missing** | No compute hardware described for data analysis (not critical for statistical analysis but listed as HARD in the checklist) |
| Random seeds | **N/A** | No stochastic ML training; kNN imputation is deterministic given k |
| Code availability | **Present** | GitHub link provided |
| Severity for library versions | **SOFT** | limma and impute are named; versions are not critical for reproducibility of the statistical approach given the methods are standard. |
| Severity for hardware | **SOFT** | Hardware is not relevant for the statistical analysis performed. |

**Assessment:** No ML model is trained; the computational analysis is standard statistical testing. Library versions are partially specified.

---

## 7. Protocol-Provenance Rule

The following methods are delegated by reference:

| Delegated method | Reference | Resolvable? | Classification |
|---|---|---|---|
| Propionylation reagent preparation | "as previously described" → refs [1] (Sidoli et al. 2016, JoVE, doi:10.3791/54112) and [2] (Garcia et al. 2007, Nat. Protoc., doi:10.1038/nprot.2007.106) | Yes — both are published protocols with DOIs | **Delegated-resolvable** |
| Histone extraction | "as described in SI Methods (Histone Extraction)" — supplementary methods referenced | Yes — SI is part of the manuscript | **Self-contained** (SI is included with the manuscript) |
| HiP-Frag workflow | "following the recommended guidelines for the HiP-Frag workflow, with some modifications" → ref [20] (Vai et al. 2025, Mol Cell Proteomics, doi:10.1016/j.mcpro.2025.101080) | Yes — published with DOI | **Delegated-resolvable** |
| Evotips loading | "loaded onto Evotips (Evosep) following the manufacturer's instructions" | Yes — manufacturer's protocol | **Delegated-resolvable** (manufacturer protocol) |
| Protease digestion conditions | "according to the manufacturer's recommendations" (Arg-C Ultra, r-Chymotrypsin) | Yes — manufacturer protocols | **Delegated-resolvable** |

**Assessment:** All delegated protocols resolve to specific, published references or manufacturer instructions. No **delegated-dead** citations found.

**Load-bearing method check:** The propionylation protocol is central to the comparison but is delegated to refs [1] and [2]. Both are well-established, published protocols with DOIs. The manuscript also describes the key parameters (buffer, pH, number of rounds, incubation) in sufficient detail that the delegation is acceptable. The HiP-Frag workflow is central to PTM identification but is delegated to ref [20]; the manuscript states "with some modifications" and provides the modification details (enzyme cleavage parameters, missed cleavages, static/variable modifications) in the Methods and SI Table S1. This is acceptable.

---

## Summary of Findings

### HARD Missing Items

| # | Category | Item | Finding |
|---|---|---|---|
| 1 | Cell lines | Source of HEK293T cells | No vendor or source institution stated |
| 2 | Cell lines | RRID/CVCL identifier | Not provided |
| 3 | Model organisms | Randomization/blinding statement | Not stated for rat experiments |

### SOFT Missing Items

| # | Category | Item | Finding |
|---|---|---|---|
| 1 | Cross-cutting | Error bar definitions | Only defined for Figure 4A; not consistently across all figures |
| 2 | Cross-cutting | HiP-Frag version | Workflow referenced but version not stated |
| 3 | Cross-cutting | R version | RStudio version given; R version not stated |
| 4 | Cell lines | Authentication (STR) | Not stated |
| 5 | Cell lines | Mycoplasma testing | Not stated |
| 6 | Model organisms | Housing details | Partial (temperature, humidity, light cycle) but cage type/group size not stated |
| 7 | Model organisms | Power justification | Not stated |
| 8 | Chemicals | Propionic anhydride vendor/CAS | Not stated (protocol delegated to refs) |
| 9 | MS | Database release version | UniProt release not pinned |
| 10 | Computational | Library versions (limma, impute) | Named but not versioned |
| 11 | Computational | Hardware | Not described (minor for statistical analysis) |

### Unverifiable Items (questions to authors)

| # | Category | Item | Finding |
|---|---|---|---|
| 1 | Protocol provenance | Propionylation reagent preparation | Delegated to refs [1] and [2]; both are published with DOIs and plausibly contain the protocol. The manuscript does not state the vendor/CAS of propionic anhydride. Cannot verify the exact reagent source from the manuscript alone. |
| 2 | Protocol provenance | HiP-Frag "with some modifications" | The modifications are described in the Methods and SI Table S1, but the exact HiP-Frag version/parameters used in ref [20] cannot be verified from this manuscript alone. |

---

## Questions for the Authors

1. **HEK293T source:** What is the source of the HEK293T cells (vendor, catalog number, or institution)? What is the RRID/CVCL identifier? Were cells authenticated (STR) and tested for mycoplasma?

2. **Randomization/blinding:** Was any randomization or blinding used in the rat experiments? If not, please state this explicitly.

3. **Error bars:** What do error bars represent in Figures 2A, 2C, 4B, and 5A–D (SD, SEM, or CI)?

4. **HiP-Frag version:** Which version of the HiP-Frag workflow was used, and what specific parameters were modified from the published protocol in ref [20]?

5. **Propionic anhydride source:** What vendor and catalog number (or CAS number) was used for propionic anhydride?

6. **Database release:** Which UniProt release (or download date) was used to construct the histone sequence database?

7. **R and package versions:** What version of R, limma, and the Bioconductor 'impute' package were used?

---

## Overall Assessment

The manuscript is **largely reproducible** with the information provided. The mass spectrometry methods are described in exceptional detail, including instrument settings, gradient conditions, collision energies, tolerances, and FDR thresholds. The digestion conditions are fully specified with enzyme-to-substrate ratios, buffers, temperatures, and times. The data and code availability statements are complete and specific.

The **HARD gaps** are limited to cell line source/RRID and randomization/blinding for the animal work. The **SOFT gaps** are minor and mostly concern version numbers and error bar definitions.

No **delegated-dead** protocol references were found. All delegated methods resolve to published protocols or manufacturer instructions.

---

*This audit assigns no score and makes no accept/reject judgment. It is provided for the editor's use.*