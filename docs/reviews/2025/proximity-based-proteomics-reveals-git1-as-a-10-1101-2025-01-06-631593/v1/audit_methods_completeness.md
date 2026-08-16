# Methods Completeness & Reagent Traceability Audit

**Manuscript:** "Proximity based proteomics reveals Git1 as a regulator of Smoothened signaling"

**Auditor role:** Methods Completeness & Reagent Traceability Auditor

**Date of audit:** Based on manuscript as provided

---

## Categories in play (trigger detected)

The following checklist categories are triggered by the manuscript content:

| Category | Trigger |
|---|---|
| Antibodies/immunodetection | WB, IF, IP all used extensively |
| Cell lines/primary cells | NIH3T3, Flp-In 3T3, 293T, MEFs, primary GNPs |
| Chemicals/drugs/dosing | SAG, cyclopamine, ShhN, biotin, EdU |
| Oligos/plasmids/constructs | CRISPR, shRNA, lentiviral constructs, TurboID fusions |
| Mass spec (proteomics) | TMT-labeled quantitative proteomics |
| Microscopy/imaging | Confocal microscopy, immunofluorescence quantification |
| Computational/ML/modeling | Custom R-based normalization and differential expression analysis |
| Model organisms / in vivo | Primary GNP culture from P7 mice (ex vivo, borderline — treated as cell/primary cell category) |

**Not triggered:** Human subjects/clinical, genomics/sequencing (no sequencing data reported beyond Sanger validation of CRISPR edits, which is covered under oligos/constructs).

---

## Cross-cutting items

### Sample size (n) with what n represents

| Item | Status | Finding |
|---|---|---|
| n stated for each quantification | **present** | n values given in most figure legends (e.g., "n = 150 cells/condition", "n = 90 cells/condition", "n = 15 fields per condition"). |
| Biological vs technical replicates distinguished | **present** | "n = 3 biological replicates" or "n = 3 independent experiments" stated in most legends. |
| n stated for mass spec | **present** | "Three biological replicates were prepared and processed in parallel." |
| n stated for Western blot quantifications | **present** | "n = 4 independent experiments" (Fig. 6C-D). |
| n stated for GNP experiments | **present** | "n = 10 fields for each condition" (Fig. 7E). |

**Assessment:** Adequate. n values and replicate types are stated for the major quantifications.

---

### Statistical tests and error bars

| Item | Status | Finding |
|---|---|---|
| Named statistical test | **present** | Student t-test, two-way ANOVA followed by Tukey's multiple comparison test, one-way ANOVA followed by Sidak's multiple comparison test all named in figure legends. |
| Error bars defined (SD/SEM/CI) | **present** | "Data is shown as mean ± SD" stated in multiple legends (Figs. 3D, 5D-E, 7). Some legends omit explicit error-bar definition (e.g., Fig. 4E, 4G, 6F) — the text states "Data are shown as mean ± SD" in some but not all. |
| p-value thresholds stated | **present** | "*p < 0.01, ***p < 0.001, ****p < 0.0001, ns, not significant" stated in legends. |

**Assessment:** Adequate, though error-bar definition is inconsistent across legends — some state "mean ± SD" explicitly, others do not. This is a minor SOFT issue.

---

### Software, tools, instrument versions

| Item | Status | Finding |
|---|---|---|
| Microscopy instruments | **partially present** | "Zeiss LSM 880 confocal Laser Scanning Microscope with 100x oil immersion lens or a LEICA DMi8 system with ×63 oil-immersion lens or Leica Mica" — models named, but no software version for acquisition (e.g., ZEN version). |
| Image analysis software | **present** | "FIJI" named; version not stated (SOFT). |
| Mass spec search software | **present** | "Integrated Proteomics Pipeline (IP2, Bruker Scientific LLC)", "ProLuCID", "DTASelect2", "Census2" — named but no version numbers (SOFT). |
| Statistical software | **present** | "GraphPad Prism 8" named. |
| R packages | **partially present** | "eBayes package in R studio" named; no R version or package version stated (SOFT). |
| CRISPR design tools | **missing** | No tool named for gRNA design (e.g., Benchling, CRISPRscan). |
| Lentivirus concentration | **present** | "4 x lentivirus concentrator (40% W/V PEG-8000, 1.2 M NaCl, PBS, pH 7.2)" — described in full. |

**Assessment:** Instrument models are named; software versions are largely absent. This is a SOFT issue — a competent lab could likely reproduce with the named tools, but exact versions are not traceable.

---

### Data availability statement

| Item | Status | Finding |
|---|---|---|
| Data availability statement | **missing** | No data availability statement is present in the manuscript. The mass spectrometry data is not deposited in PRIDE/MassIVE (see Mass spec section below). This is a HARD missing for the proteomics data specifically (repository accession required), and a general SOFT issue for the manuscript as a whole. |

---

### Code availability

| Item | Status | Finding |
|---|---|---|
| Code availability statement | **missing** | No code availability statement. The custom R-based normalization and differential expression pipeline is described in the Methods ("Subsequent data analysis was done in R studio (Supplementary data 4)... All data processing methods and equations can be found in the Supplementary data 5.") — but the referenced supplementary files are not accessible from the manuscript as provided. The normalization method is described in text (TMM normalization, scaling normalization), which is partially reproducible, but the actual code is not deposited. This is a **HARD missing** for the custom analysis code, and the supplementary data files referenced are **unverifiable** from the manuscript alone. |

---

## Antibodies / immunodetection

**Trigger:** WB, IF, IP all used.

| Antibody | Vendor | Catalog # | Clone | RRID | Application + dilution | Host/clonality | Status |
|---|---|---|---|---|---|---|---|
| Rabbit anti-pSmo | 7TM antibodies | 7TM0239A-IC | — | — | IF (1:1000, stated in GNP methods) | Rabbit (polyclonal implied) | **present** (catalog # given; dilution stated for GNP; dilution for NIH3T3 IF not stated) |
| Rabbit anti-Smo | Gift from M. Scott, Stanford | — | — | — | WB, IF | Rabbit | **missing** (no catalog #, no RRID, no dilution stated) |
| Mouse anti-acetylated tubulin | Sigma | T6793 | — | — | IF | Mouse | **present** (catalog #; dilution not stated) |
| Rabbit anti-Arl13b | Proteintech | 17711-1-AP | — | — | IF | Rabbit | **present** (catalog #; dilution not stated) |
| Rat anti-Arl13b | BiCell Scientific | 90413 | — | — | IF | Rat | **present** (catalog #; dilution not stated) |
| Rabbit anti-IFT88 | Proteintech | 13967-1-AP | — | — | IF | Rabbit | **present** (catalog #; dilution not stated) |
| Goat anti-Gli2 | R&D Systems | AF3635 | — | — | IF | Goat | **present** (catalog #; dilution not stated) |
| Goat anti-Gli1 | R&D Systems | AF3455 | — | — | WB | Goat | **present** (catalog #; dilution not stated) |
| Rabbit anti-Git1 | Novus Biologicals | NBP1-86144 | — | — | WB | Rabbit | **present** (catalog #; dilution not stated) |
| Chicken anti-GFP | Aves labs | GFP-1020 | — | — | IF | Chicken | **present** (catalog #; dilution not stated) |
| Rabbit anti-GFP | Thermo Fisher | A-11122 | — | — | IF/WB | Rabbit | **present** (catalog #; dilution not stated) |
| Mouse anti-Flag | Sigma | F3165 | — | — | WB/IP | Mouse | **present** (catalog #; dilution not stated) |
| Rabbit anti-HA | Cell Signaling | 3724 | — | — | IF/WB | Rabbit | **present** (catalog #; dilution not stated) |
| Mouse anti-GAPDH | Thermo Fisher | MA5-15738 | — | — | WB | Mouse | **present** (catalog #; dilution not stated) |
| Mouse anti-V5 | Thermo Fisher | R960-25 | — | — | IF/WB | Mouse | **present** (catalog #; dilution not stated) |
| Mouse anti-PKACa | BD Biosciences | 610980 | — | — | IF | Mouse | **present** (catalog #; dilution not stated) |
| Rabbit anti-PKACa | Cell Signaling | D38C6 | — | — | IF/WB | Rabbit | **present** (catalog #; dilution not stated) |
| Mouse anti-pericentrin | BD Biosciences | 611814 | — | — | IF | Mouse | **present** (catalog #; dilution not stated) |
| Mouse anti-gamma Tubulin | Proteintech | 66320-1-Ig | — | — | IF | Mouse | **present** (catalog #; dilution not stated) |
| DAPI | Thermo Fisher | D21490 | — | — | IF | — | **present** (catalog #) |
| Secondary antibodies | Jackson ImmunoResearch | various | — | — | IF | Donkey | **present** (catalog #s given for each) |
| Alexa Fluor 647 Streptavidin | Jackson ImmunoResearch | 016-600-084 | — | — | IF | — | **present** (catalog #) |
| HRP-Conjugated Streptavidin | Thermo Fisher | N100 | — | — | WB | — | **present** (catalog #) |

**Overall antibody assessment:**
- **HARD missing:** Rabbit anti-Smo (gift from M. Scott) — no catalog #, no RRID, no dilution. This antibody is used for key experiments (Fig. 4D, 4F). While gifted antibodies are common, the manuscript must provide at least a RRID or a published characterization reference.
- **HARD missing:** Dilutions are not stated for most primary antibodies in the NIH3T3 IF experiments. The Methods state "cells were incubated with primary antibody at 4˚C overnight" but no dilution factors are given for the NIH3T3 experiments. Dilutions are only stated for the GNP experiments ("rabbit anti-pSMO (1:1000), rat anti-ARL13B (1:500)"). This is a systematic gap.
- **SOFT:** No RRIDs provided for any antibody.
- **SOFT:** Clone names not provided for monoclonal antibodies (e.g., mouse anti-acetylated tubulin clone 6-11B-1 is standard but not stated).

---

## Cell lines / primary cells

**Trigger:** NIH3T3, Flp-In 3T3, 293T, MEFs, primary GNPs all used.

| Item | Status | Finding |
|---|---|---|
| NIH3T3 source | **present** | "ATCC, CRL-1658" |
| Flp-In 3T3 source | **present** | "Thermo Fisher Scientific, R76107" |
| 293T source | **present** | "ATCC, CRL-3216" |
| MEF source | **present** | "PKA-Ca knockout MEF cell is a gifted from the Anderson lab at Sloan Kettering Institute" — no RRID/CVCL, no passage number. |
| GNP source | **present** | "cerebella from postnatal day 7 (P7) C57BL/6J mice" — strain and age stated; no sex stated; no IACUC protocol number stated. |
| Authentication (STR) | **missing** | No STR authentication statement for any cell line. |
| Mycoplasma testing | **missing** | No mycoplasma testing statement. |
| Media/supplements | **present** | DMEM with 10% FBS (Flp-In 3T3, 293T, MEFs), DMEM with 10% calf serum (NIH3T3), Neurobasal with B-27, GlutaMAX, Pen Strep (GNPs). |
| Serum starvation for ciliation | **present** | "Ciliation was induced by reducing the growth media to 0.5% serum for 16-24h." |
| PKA-null MEF generation | **present** | Described: "PKA-deficient MEFs were obtained from Kathryn Anderson's lab and determined to be PRKACA+/-; PRKACB-/-... The remaining PRKACA allele was then knocked out using the CRISPR-mediated gene disruption technique (Alt-R system, IDT)". gRNA sequence for PRKACA provided in the text. |

**Assessment:**
- **HARD missing:** No STR authentication statement.
- **HARD missing:** No mycoplasma testing statement.
- **HARD missing:** No IACUC protocol number for the mouse work (GNP isolation from P7 mice). This is technically an animal procedure, even if the cells are cultured ex vivo.
- **HARD missing:** No sex of the P7 mice stated.
- **SOFT:** No RRID/CVCL for any cell line.
- **SOFT:** No passage numbers stated.

---

## Chemicals / drugs / dosing

**Trigger:** SAG, cyclopamine, ShhN, biotin, EdU all used.

| Item | Status | Finding |
|---|---|---|
| SAG | **present** | "100 nM SAG" — concentration stated; no vendor/catalog # stated. |
| Cyclopamine | **present** | "5 µM cyclopamine (Selleckchem, S1146)" — vendor + catalog # + concentration stated. |
| Recombinant ShhN | **present** | "1 µg/ml recombinant ShhN" — concentration stated; no vendor stated. |
| ShhN conditioned medium | **present** | "ShhN condition medium (20%-30% [vol/vol]) depending on batch) produced with 293 ecR-Shh-N cells (gift from R. Rohatgi, Stanford University)" — described. |
| Biotin | **present** | "500 µM biotin" — concentration stated; no vendor/catalog # stated. |
| EdU | **present** | "EdU was incubated with GNPs for 2 h" — no vendor/catalog # stated, no concentration stated. |
| DMSO (vehicle) | **present** | "treated with DMSO or 100 nM SAG" — vehicle named. |
| Papain | **present** | "15U/ml papain solution (Worthington Biochemical Corporation, LS003126)" — vendor + catalog # + concentration. |
| DNase I | **present** | "(Roche, 11284932001)" — vendor + catalog #. |
| Poly-D-Lysine | **present** | "(Sigma, A003E)" — vendor + catalog #. |
| Laminin | **present** | "(Gibco, 23017015)" — vendor + catalog #. |
| PEG-8000 (lentivirus concentrator) | **present** | "40% W/V PEG-8000, 1.2 M NaCl, PBS, pH 7.2" — described in full. |

**Assessment:**
- **HARD missing:** SAG vendor/catalog # not stated.
- **HARD missing:** Recombinant ShhN vendor/catalog # not stated.
- **HARD missing:** Biotin vendor/catalog # not stated.
- **HARD missing:** EdU vendor/catalog # and concentration not stated.
- **SOFT:** Vehicle for SAG (DMSO) is stated in the GNP section but not explicitly for the NIH3T3 experiments.

---

## Oligos / plasmids / constructs

**Trigger:** CRISPR (Git1 KO, PKA KO), shRNA (Git1), lentiviral constructs (YFP-Git1, Grk2-V5, Grk2-V5-DArl13b), TurboID fusions, Smo-HA, Git1-Flag.

| Item | Status | Finding |
|---|---|---|
| Git1 gRNA sequence | **missing** | The Methods state "Git1 gene was disrupted in NIH3T3 cells using CRISPR/Cas9-mediated genome editing targeting exon 2" — but the gRNA sequence is NOT provided. Fig. S4A shows a schematic ("guide RNA was designed to target exon 2 of mouse Git1") but the actual gRNA sequence is not given in the text or figure legend. This is a **HARD missing** — a lab cannot reproduce the Git1 KO without the gRNA sequence. |
| PKA-Ca gRNA sequence | **present** | The Alt-R crRNA sequence is provided in the Methods: "/AltR1/rUrCrU rCrCrC rCrArC rCrUrA rCrGrG rCrGrG rArUrG rUrUrU rUrArG rArGrC rUrArU rGrCrU /AltR2/". |
| Git1 shRNA target sequences | **missing** | The Methods state "cells were infected with lentiviruses expressing shRNA against Git1" — but the shRNA target sequences are NOT provided. Fig. S4F and Fig. 7 reference "Git1 shRNA #1, #2" but the sequences are not given. This is a **HARD missing**. |
| Control/scrambled shRNA sequence | **missing** | Referenced ("scrambled shRNA as control") but sequence not provided. **HARD missing.** |
| Smo-V5-TurboID construct | **partially present** | "full-length mouse Smo was first cloned into pEF5/FRT/V5-DEST backbone... TurboID (gift from A. Ting, Stanford University) was attached to the C terminus of Smo and linked by V5 tag" — described but no Addgene # or full sequence. The TurboID source is acknowledged. |
| YFP-Git1 | **present** | "human Git1 (Addgene, 15225)" — Addgene # given. |
| Grk2-V5 / Grk2-HA | **present** | "bovine Grk2 (gift from B. Myers, University of Utah)" — source named but no Addgene # or sequence. |
| Grk2-V5-DArl13b | **partially present** | "a truncated version of Arl13b (DArl13b) described previously in Liu et al. 2024" — delegated to a reference. The reference is cited (Liu et al. 2024, Nat Commun) and appears resolvable, but the exact DArl13b sequence is not given. |
| Smo-HA | **missing** | Used in Fig. S3A but no source or construction description given. |
| Git1-Flag | **missing** | Used in Fig. 5B but no source or construction description given. |
| FUGW backbone | **present** | "(Addgene, 14883)" — Addgene # given. |
| pEF5/FRT/V5-DEST | **present** | "(Thermo Fisher Scientific, V602020)" — vendor + catalog #. |
| Cas9 delivery | **present** | "CRISPR/Cas9-mediated genome editing" — but delivery method (plasmid, RNP, lentivirus) for Git1 KO not stated. |
| Edit validation | **present** | "Sanger sequencing of the Git1 genome sequence revealed Indel mutations" and Fig. S4B shows sequencing alignment. |
| Selection markers | **missing** | Not stated for any construct. |
| Off-target assessment | **missing** | Not stated. |

**Assessment:**
- **HARD missing:** Git1 gRNA sequence.
- **HARD missing:** Git1 shRNA target sequences (both #1 and #2).
- **HARD missing:** Control shRNA sequence.
- **HARD missing:** Smo-HA and Git1-Flag construct sources.
- **HARD missing:** Cas9 delivery method for Git1 KO (plasmid transfection? RNP? lentivirus?).
- **SOFT:** Selection markers, off-target assessment.

---

## Mass spectrometry (proteomics)

**Trigger:** TMT-labeled quantitative proteomics.

| Item | Status | Finding |
|---|---|---|
| Instrument + acquisition mode | **partially present** | "nano-LC on a RP 18 column using a flow rate of 200nL/min" — but the mass spectrometer model is NOT stated. The Methods describe the general workflow ("Mass spectrometer first measures the mas-to-charge ratio (m/z) of intact peptides...") but do not name the instrument (e.g., Orbitrap Fusion, Q-Exactive, etc.). This is a **HARD missing**. |
| Sample prep/digestion | **present** | "Proteins bound to the magnetic beads were denatured with 8 M urea, reduced with tris (2-carboxyethyl) phosphine (TCEP), alkylated with 2-chloroacetamide, and precipitated with methanol-chloroform. Bead-bound proteins were digested with trypsin and the peptides labeled with TMT 6-plex (Thermo)." |
| TMT labeling | **present** | "TMT 6-plex (Thermo)" — kit named; no catalog #. |
| Fractionation | **present** | "TMT-labeled peptides were pooled and fractionated into 8 fractions at high pH (Pierce, 84868)". |
| Search engine + version | **partially present** | "ProLuCID" named — no version. |
| Database + version | **present** | "UniProt reviewed (Swiss-Prot) proteome for Mus musculus (UP000000589)" — accession given. |
| FDR | **present** | "false discovery rate to 1%, at the spectrum level" |
| Modifications | **present** | "Carbamidomethylation (+57.02146 C) and TMT (+229.1629 K and N-terminus) were considered static modifications." |
| Tolerances | **present** | "50 ppm precursor ion tolerance and 500 ppm fragment ion tolerance" |
| Repository accession | **missing** | No PRIDE/MassIVE accession number provided. This is a **HARD missing** — the raw mass spectrometry data is not deposited in any public repository. |
| Quant method | **present** | "Census2 isobaric-labeling analysis was performed based on the TMT reporter ion intensity" |
| Replicates | **present** | "Three biological replicates were prepared and processed in parallel." |

**Assessment:**
- **HARD missing:** Mass spectrometer model not stated.
- **HARD missing:** No repository accession (PRIDE/MassIVE).
- **SOFT:** No version numbers for ProLuCID, DTASelect2, Census2, IP2.

---

## Microscopy / imaging

**Trigger:** Confocal microscopy, immunofluorescence quantification.

| Item | Status | Finding |
|---|---|---|
| Instrument model | **present** | "Zeiss LSM 880 confocal Laser Scanning Microscope with 100x oil immersion lens or a LEICA DMi8 system with ×63 oil-immersion lens or Leica Mica" — models named. |
| Objective + NA | **partially present** | "100x oil immersion lens" and "×63 oil-immersion lens" — but NA values not stated. |
| Detector + settings | **missing** | No detector type (e.g., GaAsP, PMT), no acquisition settings (e.g., pinhole, gain, scan speed). |
| Fluorophore↔marker panel | **partially present** | Fluorophores are implied by secondary antibody names (e.g., "Donkey anti-rabbit Rhodamine", "Donkey anti-rabbit Alexa 488") but the excitation/emission channels are not explicitly mapped. |
| Analysis software + version | **present** | "FIJI" named; version not stated. |
| Gating strategy (flow) | **not applicable** | No flow cytometry used. |
| GNP imaging system | **present** | "YOKOGAWA CSU-W1 system with PHOTOMETRICS PRIME 95B camera with 100X oil immersion lens" — model named. |

**Assessment:**
- **HARD missing:** Detector type and acquisition settings for confocal imaging.
- **SOFT:** NA values not stated.

---

## Computational / ML / modeling

**Trigger:** Custom R-based normalization and differential expression analysis.

| Item | Status | Finding |
|---|---|---|
| Dataset(s) with version | **partially present** | The proteomics dataset is described (1070 proteins, 6 TMT channels, 3 replicates) but not deposited. |
| Train/val/test split | **not applicable** | No ML model. |
| Architecture/algorithm | **not applicable** | No ML model. |
| Hyperparameters | **not applicable** | No ML model. |
| Training procedure | **not applicable** | No ML model. |
| Library versions + hardware | **missing** | R version, eBayes package version not stated. |
| Random seeds | **not applicable** | No stochastic training. |
| Code availability | **missing** | No code repository. The Methods state "All data processing methods and equations can be found in the Supplementary data 5" — but this supplementary file is not accessible from the manuscript as provided. |
| Normalization method description | **present** | "trimmed mean of M values (TMM) normalization" and "scaling normalization" described in text. |
| Differential expression method | **present** | "Empirical Bayes moderation approach" with "eBayes package in R studio" named. |

**Assessment:**
- **HARD missing:** Code not deposited; supplementary data files referenced but not accessible from the manuscript as provided.
- **SOFT:** R version and package versions not stated.

---

## Protocol-provenance check (delegated methods)

The following methods are delegated to references:

| Delegated method | Reference | Resolvable? | Assessment |
|---|---|---|---|
| DArl13b construct | "described previously in Liu et al. 2024" (Nat Commun 15, 3365) | **unverifiable from manuscript alone** — the citation appears in the reference list as "Liu, X. et al. Numb positively regulates Hedgehog signaling at the ciliary pocket. Nat Commun 15, 3365 (2024). https://doi.org/10.1038/s41467-024-47244-1" — the DOI is present and appears resolvable. | **delegated-resolvable** (assuming the DOI resolves and the paper contains the DArl13b description). |
| GNP culture | "Cerebellar GNPs were cultured as previously described" — reference given: "Peng, H. et al. Myomegalin regulates Hedgehog pathway by controlling PDE4D at the centrosome. Mol Biol Cell 32, 1807-1817 (2021). https://doi.org/10.1091/mbc.E21-02-0064" | **unverifiable from manuscript alone** — DOI present and appears resolvable. | **delegated-resolvable** (assuming the DOI resolves and the paper contains the GNP culture protocol). |
| TurboID | "TurboID (gift from A. Ting, Stanford University)" — no citation given for TurboID itself, though the original TurboID paper (Branon et al. 2018) is in the reference list. | **unverifiable** — the gift is acknowledged but the TurboID sequence/plasmid is not deposited. | **delegated-resolvable** (the Branon et al. reference is in the reference list with DOI: 10.1038/nbt.4201). |
| PKA-null MEF generation | "PKA-deficient MEFs were obtained from Kathryn Anderson's lab" — described in Methods with gRNA sequence. | **self-contained** — the Methods describe the generation process including the gRNA sequence. | **self-contained** |

**Assessment:** All delegated methods resolve to references with DOIs that appear in the reference list. None are circular or dead based on the manuscript alone, though I cannot verify the contents of the cited papers without accessing them. The DArl13b construct is load-bearing (used for the rescue experiment in Fig. 6G-H) and is outsourced to a citation — this is acceptable per the protocol-provenance rule only if the cited paper actually contains the full DArl13b description. This should be verified by the editor.

---

## Summary of HARD missing items

| # | Category | Item |
|---|---|---|
| 1 | Data availability | No data availability statement; mass spec data not deposited in PRIDE/MassIVE |
| 2 | Code availability | No code repository; custom R analysis code not deposited |
| 3 | Antibodies | Rabbit anti-Smo (gift) — no catalog #, RRID, or dilution |
| 4 | Antibodies | Dilutions not stated for most primary antibodies in NIH3T3 IF experiments |
| 5 | Cell lines | No STR authentication statement |
| 6 | Cell lines | No mycoplasma testing statement |
| 7 | Model organisms | No IACUC protocol number for mouse work (GNP isolation) |
| 8 | Model organisms | Sex of P7 mice not stated |
| 9 | Chemicals | SAG vendor/catalog # not stated |
| 10 | Chemicals | Recombinant ShhN vendor/catalog # not stated |
| 11 | Chemicals | Biotin vendor/catalog # not stated |
| 12 | Chemicals | EdU vendor/catalog # and concentration not stated |
| 13 | Oligos/constructs | Git1 gRNA sequence not provided |
| 14 | Oligos/constructs | Git1 shRNA target sequences not provided |
| 15 | Oligos/constructs | Control shRNA sequence not provided |
| 16 | Oligos/constructs | Smo-HA and Git1-Flag construct sources not described |
| 17 | Oligos/constructs | Cas9 delivery method for Git1 KO not stated |
| 18 | Mass spec | Mass spectrometer model not stated |
| 19 | Microscopy | Detector type and acquisition settings not stated |

---

## Summary of SOFT missing items

| # | Category | Item |
|---|---|---|
| 1 | Cross-cutting | Software versions not stated (FIJI, R, ProLuCID, DTASelect2, Census2, IP2, ZEN) |
| 2 | Cross-cutting | Error-bar definition inconsistent across figure legends |
| 3 | Antibodies | No RRIDs for any antibody |
| 4 | Antibodies | Clone names not stated for monoclonals |
| 5 | Cell lines | No RRID/CVCL for cell lines |
| 6 | Cell lines | No passage numbers |
| 7 | Oligos/constructs | Selection markers not stated |
| 8 | Oligos/constructs | Off-target assessment not stated |
| 9 | Microscopy | NA values not stated |
| 10 | Computational | R version and package versions not stated |

---

## Items marked unverifiable (questions for the authors)

1. **Supplementary data files** — The Methods reference "Supplementary data 4" and "Supplementary data 5" for the R analysis code and equations. These are not accessible from the manuscript as provided. Are these deposited anywhere accessible?

2. **DArl13b construct** — The construct is described as "described previously in Liu et al. 2024." Does the cited paper contain the full DArl13b sequence and construction details?

3. **GNP culture protocol** — The protocol is delegated to Peng et al. 2021. Does that paper contain the full protocol?

4. **Gifted antibodies and reagents** — Rabbit anti-Smo (M. Scott lab), TurboID (A. Ting lab), ShhN-producing cells (R. Rohatgi lab), Grk2 (B. Myers lab), PKA-null MEFs (K. Anderson lab) — are these available to other labs upon request, and can the manuscript state this?

---

## Note on the Smo-TurboID cell line screening

The manuscript describes screening "over 50 Smo-TurboID cell colonies" and selecting one that meets four criteria (no ciliary Smo before Shh, no Hh signaling without Shh, expression comparable to endogenous, normal cilium length). This is a commendable and important control. However, the manuscript does not state whether the selected clone was verified for correct integration at the FRT locus (e.g., by PCR or sequencing), nor whether the transgene is single-copy. This is a **SOFT** gap — the functional criteria are described, but the genomic integration is not verified.