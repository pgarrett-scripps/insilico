# Methods Completeness & Reagent Traceability Audit
## IPO9 modulates histone-dependent inhibition of cGAS

---

## CATEGORIES IN SCOPE

The manuscript triggers the following checklist categories:
- **Antibodies/immunodetection** (Western blot, ELISA)
- **Cell lines/primary cells** (THP-1, HEK293T, PBMCs, Lenti-X)
- **Model organisms/in vivo** (Trex1−/− mice)
- **Chemicals/drugs/dosing** (SR-218, SR-051, SR-432, and analogs; VacV70, SR-717)
- **Oligos/plasmids/constructs** (shRNA vectors, N-Flag-IPO9, packaging plasmids)
- **Proteomics/mass spec** (TMT-based quantitative proteomics)
- **Microscopy/imaging** (cryo-EM)
- **Cross-cutting** (sample size, statistics, software versions, data availability)

---

## CROSS-CUTTING ITEMS

### Sample Size & Replication Reporting

| Item | Status | Finding |
|------|--------|---------|
| **n stated (biological vs technical)** | **MIXED** | Most experiments state n=3 independent experiments with three technical replicates per run (e.g., Fig. 1a, 1c, 1e, 1f, 1h; Extended Data Fig. 2). However, several critical experiments lack explicit n values: (1) Fig. 2d (recombinant IPO9 labeling): "Data is representative of n=2 independent experiments" — below standard threshold. (2) Fig. 2e (Flag-IPO9 THP-1): "Data is indicative of n=2 independent experiments" — non-standard language, unclear if n=2 is sufficient. (3) Fig. 3d (malachite green assay): "Data is indicative of n=3 independent experiments with three technical replicates per experiment" — uses "indicative" rather than "representative," suggesting uncertainty. (4) Cryo-EM: no explicit statement of how many grid preparations, micrograph collections, or particle picks were performed; only final particle numbers in processing workflow (Extended Data Fig. 6a) are given. (5) In vivo cGAMP measurement (Fig. 1g, Extended Data Fig. 3d): "n=2 independent experiments, with at least n=4 mice per treatment group" — only 2 biological replicates (experiments) is low for in vivo work. |
| **Error bars defined (SD/SEM/CI)** | **PRESENT** | Most figures state "Data are presented as mean ± s.d." (e.g., Figs. 1c, 1e, 1f, 1h; Fig. 3d, 3f). However, some figures do not explicitly state error representation: Fig. 2f, 2g, 2h (rhodamine labeling curves) do not specify error bars or confidence intervals. Extended Data Fig. 2 states "Data are presented as mean ± s.d." but some panels (e.g., 2a, 2b) are marked "representative" without error bars shown. |
| **Statistical test named** | **PRESENT** | Tests are named for most quantitative comparisons: one-way ANOVA with Tukey post-hoc (Fig. 3d), two-way repeated-measures ANOVA (Fig. 3c), one-way ANOVA (Fig. 1c, 1e). However, some figures lack statistical reporting: Fig. 2f, 2g (rhodamine labeling) do not state whether differences were tested. BLI experiments (Fig. 3f, Extended Data Fig. 5) report EC50 values but do not state statistical test for curve fitting. |

### Software, Tool, and Instrument Versions

| Item | Status | Finding |
|------|--------|---------|
| **Cryo-EM software versions** | **PARTIAL** | CryoSPARC is named but version not stated ("cryoSPARC Live" used for motion correction and CTF; reference 86 is Punjani et al. 2017, which describes cryoSPARC but not the specific version used here). UCSF ChimeraX is named (reference 87) but version not stated. Phenix is named (reference 88) but version not stated. |
| **Western blot imaging software** | **MISSING** | Blots were "imaged on a ChemiDoc Imager (Biorad)" but no software version or quantification method is stated. How were band intensities quantified for Fig. 3c (phospho-STING normalization)? |
| **RT-qPCR software** | **MISSING** | TaqMan Fast Advanced Master Mix is named, but no qPCR instrument model or analysis software (e.g., QuantStudio, StepOne) is stated. How were Ct values processed? |
| **Flow cytometry / plate reader software** | **PARTIAL** | Envision plate reader (Perkin Elmer) is named for luciferase assays, but no software version stated. Octet96 Red (Sartorius) is named for BLI but no software version stated. |
| **Proteomics analysis software** | **PARTIAL** | "Proteome Discoverer" is named for TMT data analysis, but version is not stated. Filtering criteria are given ("signal in every TMT channel and at least two peptides identified") but no FDR threshold is stated. |

### Data Availability Statement

| Item | Status | Finding |
|------|--------|---------|
| **Atomic coordinates & cryo-EM map** | **PRESENT** | "The atomic model and cryo-EM density map for the cGAS:H2A-H2B complex have been deposited to the PDB (accession number: 13ME) and EMDB (accession number: EMD-77152)." |
| **Raw proteomics data** | **MISSING** | TMT-based quantitative proteomics (Fig. 2b, Methods section "Quantitative Proteomics") — no statement of deposition to PRIDE, MassIVE, or other repository. No raw mass spectrometry files or search results provided. |
| **Raw sequencing data** | **NOT APPLICABLE** | No genomics/sequencing work reported. |
| **Cell line authentication / mycoplasma** | **MISSING** | No statement of STR authentication or mycoplasma testing for THP-1, HEK293T, or Lenti-X cells. |
| **Plasmid/construct availability** | **PARTIAL** | N-Flag-IPO9 is stated as "gift from the Cravatt Lab at Scripps Research, Addgene: #217916" — Addgene number provided. shRNA vectors are identified by clone ID (TRCN0000161611, TRCN0000160703, TRCN0000146282, SHC016) but no statement of availability (Sigma Mission library is implied but not confirmed). Packaging plasmids are Addgene #11260 and #12259 — available. |
| **Code availability** | **MISSING** | No statement of code availability for custom analysis (e.g., cryo-EM image processing scripts, proteomics filtering, BLI curve fitting). |

---

## ANTIBODIES & IMMUNODETECTION

### Western Blot Antibodies

| Antibody | Vendor | Catalog # | Clone | RRID | Dilution | Host/Clonality | Status |
|----------|--------|-----------|-------|------|----------|----------------|--------|
| phospho-STING (S366) | CST | 19781 | — | — | 1:1000 | — | **PARTIAL** — vendor and catalog present; clone and RRID missing; host species not stated |
| phospho-IRF3 | CST | 37829 | — | — | 1:1000 | — | **PARTIAL** — same as above |
| IPO9 | Thermo Fisher | A305-475A | — | — | 1:2000 | — | **PARTIAL** — same as above |
| Vinculin | Thermo Fisher | 14-9777-82 | — | — | 1:10,000 | — | **PARTIAL** — same as above |
| Flag | Sigma | F1804 | — | — | 1:2000 | — | **PARTIAL** — same as above |
| STING | CST | 13647 | — | — | 1:1000 | — | **PARTIAL** — same as above |
| IRF3 | CST | 4302 | — | — | 1:1000 | — | **PARTIAL** — same as above |
| Histone H3 | CST | 4499 | — | — | 1:2000 | — | **PARTIAL** — same as above |
| cGAS | CST | 15102 | — | — | 1:1000 | — | **PARTIAL** — same as above |

**Severity: HARD** — Clone identity, RRID, and host species (rabbit vs mouse) are essential for reproducibility and antibody validation. CST (Cell Signaling Technology) antibodies are typically rabbit monoclonal or polyclonal, but this is not stated. Sigma F1804 is typically mouse monoclonal, but not confirmed in the manuscript.

### Secondary Antibodies

| Antibody | Vendor | Catalog # | Dilution | Status |
|----------|--------|-----------|----------|--------|
| Goat anti-Rabbit IgG, HRP-linked | Thermo Fisher | 31460 | 1:10,000 | **PARTIAL** — vendor and dilution present; clone/RRID missing |
| Goat anti-Mouse IgG, HRP-linked | CST | 7076 | 1:10,000 | **PARTIAL** — vendor and dilution present; clone/RRID missing |

**Severity: HARD** — RRID and clone information missing for secondary antibodies.

### ELISA

| Assay | Kit | Vendor | Catalog # | Protocol | Status |
|-------|-----|--------|-----------|----------|--------|
| 2'3'-cGAMP ELISA | cGAMP ELISA kit | Cayman Chemical | 501700 | "according to the manufacturer's instructions" | **DELEGATED-RESOLVABLE** — kit is named with catalog #; protocol delegated to manufacturer instructions (standard practice for commercial kits) |

**Severity: SOFT** — Commercial kit with published protocol; acceptable delegation.

---

## CELL LINES & PRIMARY CELLS

| Cell Line | Source | RRID/CVCL | Authentication | Mycoplasma | Media/Supplements | Status |
|-----------|--------|-----------|----------------|------------|-------------------|--------|
| THP-1 Dual (thpd-nfis) | InvivoGen | — | Not stated | Not stated | RPMI 1640, 2 mM L-glutamine, 25 mM HEPES, 10% FBS, 1000 U/mL pen, 1000 µg/mL strep, 0.25 µg/mL Ampho B | **PARTIAL** |
| THP-1 Lucia ISG (thpl-isg) | InvivoGen | — | Not stated | Not stated | Same as above | **PARTIAL** |
| HEK293T | Not stated | — | Not stated | Not stated | DMEM, 10% FBS, 1000 U/mL pen, 1000 µg/mL strep, 0.25 µg/mL Ampho B | **PARTIAL** |
| Lenti-X | Not stated | — | Not stated | Not stated | DMEM, 10% FBS, 1000 U/mL pen, 1000 µg/mL strep, 0.25 µg/mL Ampho B | **PARTIAL** |
| PBMCs (primary human) | "gift from the Teijaro Lab at Scripps Research" | — | Not stated | Not stated | RPMI, 10% FBS, 0.1% BME | **PARTIAL** |

**Severity: HARD** — No STR authentication or mycoplasma testing stated for any cell line. RRID/CVCL identifiers missing. HEK293T and Lenti-X sources not stated (assumed commercial but not confirmed).

**Severity: SOFT** — Media and supplements are stated; acceptable.

---

## MODEL ORGANISMS & IN VIVO

| Item | Status | Finding |
|------|--------|---------|
| **Species, strain, source** | **PARTIAL** | "Wild type and Trex1−/− C57BL/6J mice were a gift from the Stetson lab." — Strain identified (C57BL/6J), genotype stated (Trex1−/−), source stated (Stetson lab). However, no RRID for the strain or source repository (JAX, etc.) is provided. |
| **Sex** | **MISSING** | Not stated. |
| **Age** | **MISSING** | Not stated. |
| **n per group** | **PRESENT** | "at least n=4 mice per treatment group" (Fig. 1g caption); Extended Data Fig. 3d states same. However, only 2 independent experiments are reported, making total n unclear (is it 4 mice × 2 experiments = 8 total, or 4 per experiment?). |
| **IACUC protocol #** | **MISSING** | No IACUC approval number or statement of ethical review stated. |
| **Randomization/blinding** | **MISSING** | No statement of randomization or blinding in treatment assignment or outcome assessment. |
| **Housing, power justification** | **MISSING** — SOFT | Not stated. |

**Severity: HARD** — Sex, age, IACUC approval, and randomization/blinding are missing. These are essential for reproducibility and ethical compliance in in vivo work.

---

## CHEMICALS, DRUGS, & DOSING

### Small Molecule Compounds

| Compound | Identity | Vendor/Source | Catalog # / CAS | Dose/Concentration | Route | Vehicle | Schedule | Status |
|----------|----------|---------------|-----------------|-------------------|-------|---------|----------|--------|
| SR-218 | 5-aminoisoxazole derivative (structure in Fig. 1a) | Synthesized (ChemPartner) | — | Cell assays: 1 µM; in vivo: 30 mg/kg | IP (intraperitoneal) | 2% DMSO + 98% 10% (w/v) HP-β-CD in saline | Four injections (schedule not stated) | **PARTIAL** |
| SR-051 | 5-aminoisoxazole derivative (structure in Fig. 1a) | Synthesized (ChemPartner) | — | Cell assays: dose-response | — | — | — | **PARTIAL** |
| SR-432 | Diazirine alkyne PAP derivative of SR-218 (structure in Fig. 2a) | Synthesized (ChemPartner) | — | Cell assays: 1 µM | — | — | — | **PARTIAL** |
| G140 | cGAS inhibitor (reference control) | — | — | Cell assays: 10 µM | — | — | — | **MISSING** — no source or identity stated |
| SR-717 | STING agonist | — | — | Cell assays: 2 µM | — | — | — | **MISSING** — no source stated |
| VacV70 | 70 bp dsDNA with viral motifs | InvivoGen | tlrl-vav70c | Cell assays: 0.4–2 µg/mL | — | Pre-complexed with Lyovec | — | **PRESENT** |

**Severity: HARD** — G140 and SR-717 sources are not stated. CAS numbers or chemical identities for SR-218, SR-051, SR-432 are not provided (structures are shown but CAS/vendor catalog # would aid external sourcing). In vivo injection schedule (timing between four injections) is not stated.

**Severity: SOFT** — Vehicle composition is stated for in vivo dosing; acceptable.

### Recombinant Proteins & Histones

| Protein | Source | Catalog # | Purity/Lot | Status |
|---------|--------|-----------|-----------|--------|
| Human Histones H2A, H2B | Histone Source (Colorado State University) | — | Not stated | **PARTIAL** — source named; lot/purity not stated |
| Recombinant human IPO9 | Expressed in BL21(DE3) E. coli | — | Purified via GST-tag cleavage; SEC | **PRESENT** — expression system and purification method stated |
| Recombinant human cGAS (full-length) | Addgene #127161 | 127161 | Expressed in BL21(DE3); Ni-NTA purified | **PRESENT** |
| Recombinant human cGAS (aa157-522, N-terminal truncated) | Addgene #108676 | 108676 | Expressed in BL21(DE3); GST-tag cleaved via PreScission Protease | **PRESENT** |
| Biotinylated recombinant mononucleosomes | Active Motif | 31467 | — | **PARTIAL** — vendor and catalog present; lot/purity not stated |

**Severity: SOFT** — Histone lot numbers and purity not stated, but source is identified and expression/purification methods are described for recombinant proteins.

---

## OLIGOS, PLASMIDS, & CONSTRUCTS

### shRNA Vectors

| Target | Clone ID | Source | Sequence | Validation | Status |
|--------|----------|--------|----------|-----------|--------|
| IPO9 | TRCN0000161611 ("sh1") | Mission (Sigma) | Not stated | Not stated | **PARTIAL** — clone ID provided; sequence and off-target assessment missing |
| IPO9 | TRCN0000160703 ("sh2") | Mission (Sigma) | Not stated | Not stated | **PARTIAL** — same as above |
| cGAS | TRCN0000146282 | Mission (Sigma) | Not stated | Not stated | **PARTIAL** — same as above |
| Non-targeting control | SHC016 | Mission (Sigma) | Not stated | Not stated | **PARTIAL** — same as above |

**Severity: HARD** — shRNA target sequences are not provided. While clone IDs are given (allowing lookup in Sigma's database), the manuscript should state the target sequence for transparency and to allow verification of potential off-targets.

### Expression Plasmids

| Construct | Source | Addgene # | Backbone | Selection Marker | Status |
|-----------|--------|-----------|----------|------------------|--------|
| N-Flag-IPO9 | Gift from Cravatt Lab | 217916 | — | — | **PRESENT** — Addgene # provided |
| psPAX.2 (packaging) | Addgene | 11260 | — | — | **PRESENT** |
| pMD.2 (packaging) | Addgene | 12259 | — | — | **PRESENT** |
| pGEX-4T-3 (GST-IPO9 expression) | — | 79149 | — | Ampicillin (implied) | **PARTIAL** — backbone named; selection marker not stated |

**Severity: SOFT** — Addgene numbers provided for key constructs; selection markers not explicitly stated but implied by standard plasmid use.

### Cloning & Expression Details

| Item | Status | Finding |
|------|--------|---------|
| **Full-length IPO9 cloning** | **PARTIAL** | "Full length human IPO9 coding sequence and a TEV cleavage site were cloned into the pGEX-4T-3 backbone" — method (restriction sites, ligation, etc.) not stated. Cloning strategy is delegated to standard molecular biology practice. |
| **cGAS expression validation** | **MISSING** | No statement of expression level verification (e.g., SDS-PAGE, densitometry) or protein identity confirmation (e.g., mass spec). |

**Severity: HARD** — Cloning methods are not detailed, but this is acceptable if the construct is available via Addgene (for N-Flag-IPO9) or if expression is validated by the purification and biochemical activity shown. However, no explicit validation of recombinant protein identity is stated.

---

## PROTEOMICS & MASS SPECTROMETRY

### TMT-Based Quantitative Proteomics

| Item | Status | Finding |
|------|--------|---------|
| **Instrument** | **MISSING** | No mass spectrometer model or manufacturer stated. Methods section says "shipped to the Herbert Wertheim UF Scripps Institute for Biomedical Innovation & Technology Mass Spectrometry and Proteomics Core" but does not name the instrument used by that facility. |
| **Acquisition mode** | **MISSING** | No MS/MS method stated (e.g., DDA, DIA, targeted). |
| **Sample prep** | **PARTIAL** | Click chemistry enrichment (biotin azide + streptavidin beads), trypsin digestion, and TMT labeling are described. However, no digestion time, temperature, or enzyme:protein ratio stated. |
| **Search engine & version** | **PARTIAL** | "Proteome Discoverer" is named but version not stated. |
| **Database & version** | **MISSING** | No protein database (UniProt, RefSeq) or version stated. |
| **FDR threshold** | **MISSING** | No FDR cutoff stated. Filtering criteria given: "signal in every TMT channel and at least two peptides identified, while also removing common contaminants such as keratin" — but no peptide-level or protein-level FDR. |
| **Modifications** | **MISSING** | No statement of fixed or variable modifications searched (e.g., carbamidomethylation, oxidation, TMT labeling). |
| **Mass tolerances** | **MISSING** | No precursor or fragment mass tolerance stated. |
| **Repository accession** | **MISSING** | No deposition to PRIDE, MassIVE, or other repository stated. |
| **Quantification method** | **MISSING** — SOFT | TMT intensity-based quantification is implied but not explicitly stated. |

**Severity: HARD** — Instrument, search engine version, database, FDR threshold, modifications, and mass tolerances are missing. These are essential for method reproducibility and data interpretation. Repository accession is missing, preventing data inspection.

---

## MICROSCOPY & IMAGING

### Cryo-EM

| Item | Status | Finding |
|------|--------|---------|
| **Instrument model** | **PRESENT** | Glacios 2 microscope (ThermoFisher), 200 kV, Falcon 4i detector (ThermoFisher) |
| **Magnification & pixel size** | **PRESENT** | 190,000× nominal magnification, 0.718 Å pixel size |
| **Objective/NA** | **NOT APPLICABLE** | Cryo-EM does not use traditional objectives; microscope optics are described. |
| **Detector & settings** | **PRESENT** | Falcon 4i detector; ~45 e/Å² exposure dose; −0.8 to −1.8 µm defocus range; 30° tilt |
| **Sample preparation** | **PRESENT** | Glow-discharged UltrAuFoil 1.2/1.3 300-mesh grids; 3 µL sample; 0.1% octyl-β-glucoside; 3 s wait time, 3–4 s blot time; Vitrobot Mark IV at 4°C, 100% humidity |
| **Data collection software** | **PRESENT** | EPU (ThermoFisher) |
| **Image processing software** | **PARTIAL** | CryoSPARC (Patch Motion Correction, Patch CTF, 2D classification, ab-initio reconstruction, heterogeneous refinement, non-uniform refinement, local refinement) — version not stated. Reference 86 (Punjani et al. 2017) describes the software but not the version used. |
| **Refinement software** | **PARTIAL** | Phenix (real-space refinement) — version not stated. Reference 88 (Adams et al. 2010) is the original Phenix paper; current version unknown. |
| **Visualization software** | **PARTIAL** | UCSF ChimeraX (docking, figure generation) — version not stated. Reference 87 (Goddard et al. 2018) describes ChimeraX but not the version used. |
| **Symmetry & masking** | **PRESENT** | C2 symmetry applied; local refinement with mask around 1 copy each of cGAS and H2A-H2B; symmetry expansion performed |
| **Resolution & validation** | **PRESENT** | 4.3 Å resolution (tilted 30° dataset); FSC curve and angular distribution shown (Extended Data Fig. 6b); final map deposited (EMDB EMD-77152) |
| **Model building & validation** | **PRESENT** | Coordinates from PDB 7C0M (cGAS) and 7PII (H2A-H2B) docked and refined; real-space refinement in Phenix; atomic model deposited (PDB 13ME) |
| **Particle numbers** | **PRESENT** | Processing workflow shows particle counts at each stage (Extended Data Fig. 6a); final particle number for 2:2 class not explicitly stated but implied from refinement |

**Severity: HARD** — Software versions for CryoSPARC, Phenix, and ChimeraX are not stated. These are essential for reproducibility of image processing and model building.

**Severity: SOFT** — Sample preparation and data collection parameters are well-documented; acceptable.

---

## BIOCHEMICAL ASSAYS

### Malachite Green Phosphate Release Assay

| Item | Status | Finding |
|------|--------|---------|
| **Assay principle** | **PRESENT** | Malachite green-based detection of pyrophosphate release (reference 73) |
| **Substrate concentrations** | **PRESENT** | 100 nM cGAS, 100 nM biotin-100bp-ISD, 50 µM ATP, 50 µM GTP |
| **Reaction conditions** | **PRESENT** | Assay buffer (20 mM Tris-HCl pH 7.5, 100 mM NaCl, 5 mM MgCl₂), 30 min at 37°C |
| **Quenching** | **PRESENT** | Boiling at 95°C for 10 min |
| **Pyrophosphatase treatment** | **PRESENT** | 0.3 units/mL E. coli pyrophosphatase (NEB M0361S), 15 min at room temperature |
| **Kit & reagent** | **PRESENT** | Malachite green phosphate assay kit (Sigma MAK307) |
| **Plate reader** | **MISSING** | No plate reader model or software stated for absorbance reading at 650 nm. |
| **Positive/negative controls** | **MISSING** | No mention of control reactions (e.g., cGAS alone, substrate alone, no enzyme). |

**Severity: HARD** — Positive and negative controls are not mentioned. While the assay is described, validation of the assay performance is not shown.

**Severity: SOFT** — Plate reader model not critical if the standard 650 nm absorbance is used.

### Biolayer Interferometry (BLI)

| Item | Status | Finding |
|------|--------|---------|
| **Instrument** | **PRESENT** | ForteBio Octet96 Red (Sartorius) |
| **Biosensor types** | **PRESENT** | NTA and Streptavidin biosensors (Sartorius) |
| **Kinetics buffer** | **PRESENT** | Buffer A: PBS 7.4, 0.05% Tween-20, 1% BSA; Buffer B: PBS 7.4, 0.05% Tween-20, 0.1% BSA |
| **Loading & association** | **PRESENT** | Protein loading thresholds, association times, and concentrations stated for each experiment (e.g., 100 nM FL-cGAS, 250 nM H2A-H2B) |
| **Dissociation/competition** | **PRESENT** | IPO9 concentration series (2-fold dilutions from 500 nM to 7.8 nM or 250 nM to 3.9 nM); 0 nM background subtraction |
| **Data analysis** | **PARTIAL** | "IPO9 induced loss of signal was measured as the difference between the reading at the start and end of IPO9 incubation." — method is clear, but no statement of curve fitting (e.g., 1:1 binding, non-linear regression) or software used. EC50 is reported (Fig. 3f: 110 nM) but fitting method not stated. |
| **Replicates** | **PRESENT** | "All experiments were performed in triplicate" |
| **Software & version** | **MISSING** | No BLI analysis software version stated (Octet Data Analysis Software version?). |

**Severity: HARD** — Curve fitting method and software version are not stated. EC50 calculation requires specification of the model used (1:1 binding, Hill coefficient, etc.).

---

## COMPUTATIONAL & STRUCTURAL ANALYSIS

### Cryo-EM Image Processing (detailed)

| Item | Status | Finding |
|------|--------|---------|
| **CTF threshold** | **PRESENT** | 6 Å |
| **2D classification parameters** | **MISSING** | Number of classes, convergence criteria, or other parameters not stated. |
| **Ab-initio reconstruction** | **MISSING** | Number of classes, symmetry assumptions, or other parameters not stated. |
| **Heterogeneous refinement** | **MISSING** | Number of classes, convergence criteria not stated. |
| **Non-uniform refinement parameters** | **MISSING** | Learning rate, number of iterations, or other optimization parameters not stated. |
| **Local refinement mask** | **PRESENT** | "mask around 1 copy each of cGAS and H2A-H2B" — mask generation method not stated (e.g., threshold, dilation). |
| **Symmetry expansion** | **PRESENT** | C2 symmetry expanded; method standard but parameters not detailed. |
| **Resolution estimation** | **PRESENT** | FSC curve shown (Extended Data Fig. 6b); 4.3 Å reported at FSC=0.143 (standard threshold implied but not stated). |
| **Angular distribution** | **PRESENT** | Shown in Extended Data Fig. 6b; 30° tilt dataset noted as preferred orientation. |

**Severity: HARD** — CryoSPARC processing parameters (2D classification, ab-initio, heterogeneous refinement settings) are not stated. These are essential for reproducibility and troubleshooting.

### Model Building & Refinement

| Item | Status | Finding |
|------|--------|---------|
| **PDB templates** | **PRESENT** | PDB 7C0M (human cGAS), PDB 7PII (human H2A-H2B) |
| **Docking method** | **PRESENT** | "UCSF ChimeraX" (reference 87) |
| **Real-space refinement** | **PRESENT** | "Phenix" (reference 88) |
| **Refinement parameters** | **MISSING** | No statement of restraints, weights, or convergence criteria used in Phenix. |
| **Model validation** | **MISSING** | No Ramachandran plot, clash score, or other geometry validation metrics stated. |
| **Resolution limitations** | **PRESENT** | "The resolution of the final map precluded high confidence modeling of sidechains, however, clearly resolved secondary structure enabled unambiguous observation of a cGAS dimer bound to histones." — acknowledged; appropriate caution stated. |

**Severity: HARD** — Model validation metrics (Ramachandran, clash score, MolProbity) are not provided. These are standard for PDB deposition and should be stated or referenced.

---

## SUMMARY TABLE: HARD vs SOFT MISSING ITEMS

| Category | HARD Missing | SOFT Missing |
|----------|--------------|--------------|
| **Cross-cutting** | Code availability; Proteomics raw data repository; Cell line authentication/mycoplasma; Western blot quantification software | — |
| **Antibodies** | RRID, clone, host species for primary and secondary antibodies | — |
| **Cell lines** | STR authentication, mycoplasma testing, RRID/CVCL for all lines; source for HEK293T and Lenti-X | — |
| **In vivo** | Sex, age, IACUC protocol #, randomization/blinding statement | Power justification, housing |
| **Chemicals/drugs** | Source/identity for G140 and SR-717; in vivo injection schedule; CAS/catalog # for SR-218, SR-051, SR-432 | — |
| **Plasmids/shRNA** | shRNA target sequences; off-target assessment | — |
| **Proteomics** | Instrument model, acquisition mode, search engine version, database, FDR threshold, modifications, mass tolerances, repository accession | Quantification method details |
| **Cryo-EM** | Software versions (CryoSPARC, Phenix, ChimeraX); processing parameters (2D, ab-initio, heterogeneous refinement); model validation metrics | — |
| **BLI** | Curve fitting method, software version | — |
| **Malachite green assay** | Positive/negative controls | Plate reader model |

---

## PROTOCOL PROVENANCE ASSESSMENT

### Delegated Methods

| Method | Reference | Type | Status |
|--------|-----------|------|--------|
| cGAMP ELISA | Cayman Chemical kit 501700 | Commercial kit | **DELEGATED-RESOLVABLE** — kit is named with catalog #; manufacturer protocol is standard and accessible |
| Cryo-EM sample preparation (Vitrobot) | Standard protocol | Instrument manual | **DELEGATED-RESOLVABLE** — Vitrobot Mark IV is a standard instrument; parameters (temperature, humidity, blot time) are stated |
| Western blotting | "Bolt 4-12% Bis-Tris gels and Bolt mini transfer system" | Commercial system | **DELEGATED-RESOLVABLE** — system is named; standard protocol is implied |
| Cell culture media | Standard RPMI/DMEM | Standard practice | **DELEGATED-RESOLVABLE** — media composition is stated |
| Protein expression & purification | "BL21(DE3) E. coli" + standard affinity chromatography | Standard practice | **DELEGATED-RESOLVABLE** — expression system and purification methods (GST-tag, Ni-NTA, SEC) are described; standard protocols apply |
| Lentiviral transduction | "concentrated virus and 8 µg/mL polybrene... centrifugation for 1 hour at 800 × g" | Standard protocol | **DELEGATED-RESOLVABLE** — key parameters (polybrene concentration, centrifugation) are stated |
| Puromycin selection | "2 µg/mL puromycin for 72 hours" | Standard protocol | **DELEGATED-RESOLVABLE** — concentration and duration stated |

**No delegated-dead protocols identified.** All methods either are described in full or reference standard commercial systems/kits with stated parameters.

---

## UNVERIFIABLE ITEMS (Questions for Authors)

1. **Proteomics database and FDR threshold**: The manuscript states filtering criteria but does not name the protein database (UniProt, RefSeq, etc.) or state the FDR cutoff. Can the authors confirm these details and provide the Proteome Discoverer version?

2. **cGAS expression validation**: No mass spectrometry or SDS-PAGE confirmation of recombinant cGAS identity is stated. Was the expressed protein validated by any method?

3. **G140 and SR-717 sources**: These reference compounds are used but their source (commercial vendor, synthesized in-house, gift) is not stated. Can the authors provide this information?

4. **In vivo injection schedule**: Four intraperitoneal injections of SR-218 are mentioned, but the timing between injections (e.g., daily, every 12 hours) is not stated. What was the schedule?

5. **Cryo-EM particle numbers**: The final particle count for the 2:2 cGAS:H2A-H2B class is not explicitly stated in the text or figure legend. Can the authors provide this number?

6. **BLI curve fitting**: The EC50 value (110 nM) is reported, but the fitting model (1:1 binding, Hill coefficient, etc.) and software used are not stated. What model was used?

7. **Malachite green assay controls**: No positive or negative controls are mentioned. Were control reactions (e.g., cGAS alone, no enzyme) performed to validate the assay?

8. **Cell line sources**: HEK293T and Lenti-X cell sources are not stated. Were these obtained from ATCC, a repository, or another source?

---

## CONCLUSION

**Overall Assessment:**

The manuscript provides substantial methodological detail for most experiments, with clear descriptions of cell-based assays, biochemical assays, and cryo-EM data collection. However, several **HARD missing items** prevent full reproducibility:

1. **Antibody identifiers** (RRID, clone, host species) are absent for all primary and secondary antibodies used in Western blots.
2. **Cell line authentication and mycoplasma testing** are not stated.
3. **Proteomics data** (instrument, database, FDR, modifications, repository accession) lack critical details and are not deposited.
4. **Cryo-EM software versions and processing parameters** are not fully specified.
5. **In vivo work** lacks sex, age, IACUC approval, and randomization/blinding statements.
6. **Source/identity of reference compounds** (G140, SR-717) and injection schedule are missing.
7. **Code availability** is not stated.

**SOFT missing items** (recommended but not blocking) include plate reader models, power justifications, and housing details.

The work is substantially reproducible for the core biochemical and structural findings, but external groups would face significant challenges in repeating the cell-based assays and in vivo experiments without additional information from the authors.