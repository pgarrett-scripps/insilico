# Methods Completeness & Reagent Traceability Audit
## Manuscript: N332-GT5 HIV Vaccine Candidate cGMP Manufacturing

---

## CROSS-CUTTING ITEMS

### Sample Size (n) and Replication

| Item | Status | Finding |
|------|--------|---------|
| Biological vs. technical replicates stated | **HARD: MISSING** | Ambr®250 optimization (Section 3.2.2): 12 bioreactors tested, but no explicit statement of whether these are independent biological replicates or technical replicates. Clone ranking (Section 3.1.2–3.1.3): 213 clones screened, then 24 selected, then top clone C235 chosen — no statement of independent replication of the ranking process itself. Pilot-scale runs (Section 3.2.3): two 50-L runs (RCB and MCB) described, but not framed as replicates with n=2; unclear if these are independent biological replicates or sequential demonstrations. |
| Statistical test named | **HARD: MISSING** | No formal statistical tests reported. Comparisons between conditions (e.g., Ambr®250 variants, pilot vs. GMP runs) are descriptive only. No p-values, confidence intervals, or significance statements. Table 6 and Figure 13 present means and ranges but no test of difference. |
| Error bars / uncertainty representation | **SOFT: PARTIAL** | Some figures show ±SD or ±SEM (e.g., Figure 17 DeGlyPHER data: "mean of abundance measurement... with the standard error of mean"). Table 9 shows ranges (e.g., "15521±578 ppm"). However, many results lack error representation entirely (e.g., Figure 14 cell culture data, individual clone titers in Figure 10). Inconsistent reporting across figures. |

### Software, Tool, and Instrument Versions

| Item | Status | Finding |
|------|--------|---------|
| Analytical instruments: model and version | **HARD: PARTIAL** | Instruments named but versions often missing: ForteBio Octet RED384 (no version); Bio-Rad CFX384 Real-Time PCR (no version); SoloVPE spectrophotometer (no version); Sartorius Octet system (no version). UPLC Acquity (no version). FEI Tecnai Spirit TEM (no version). Thermo Orbitrap Eclipse (no version). Thermo Q Exactive HF-X (no version). |
| Bioreactor control software | **HARD: MISSING** | Ambr®250, XDR-50, XDR-200 bioreactors used but no mention of control/monitoring software version or data-logging system. |
| Mass spectrometry analysis software | **HARD: PARTIAL** | DeGlyPHER method (Section 2.7.1): "Integrated Proteomics Pipeline (IP2, Bruker)" named; ProLuCID, DTASelect2, Census2, GlycoMSQuant cited with references (Peng et al. 2003, Tabb et al. 2002, Park et al. 2008, Baboo et al. 2021) but no versions stated in the manuscript. LC-MS glycoproteomics: "Byos (Protein Metrics)" named but no version. |
| Microscopy/EM analysis software | **HARD: PARTIAL** | Negative-stain EM (Section 2.7.2): CryoSPARC named (Pujani et al. 2017) but no version. Leginon (Suloway et al. 2005) named but no version. |
| HPLC/chromatography software | **HARD: MISSING** | SE-HPLC, RP-HPLC, and other chromatography methods described but no data-acquisition or analysis software named or versioned. |

### Data Availability Statement

| Item | Status | Finding |
|------|--------|---------|
| Data availability statement | **HARD: MISSING** | No statement regarding where raw data (bioreactor logs, chromatography traces, mass spec raw files, microscopy images, qPCR Ct values, etc.) are deposited or will be made available. No mention of supplementary data, repositories (e.g., Zenodo, OSF, institutional repository), or conditions for access. |

### Code Availability

| Item | Status | Finding |
|------|--------|---------|
| Custom analysis code | **SOFT: N/A** | No custom code development reported. Analysis relies on commercial software (Byos, IP2, CFX Manager, etc.) and published tools. However, any custom scripts for data processing, figure generation, or statistical analysis are not mentioned. |

---

## CONDITIONAL CATEGORIES

### Antibodies / Immunodetection

**Trigger:** Yes — multiple antibodies used in BLI assays, ELISA, and as detection reagents.

| Item | Status | Finding |
|------|--------|---------|
| **PGT145 antibody** | **HARD: PARTIAL** | Used in BLI assays (Sections 2.1.2, 2.2.5, 3.1.2, 3.1.3). Described as "directed against a quaternary structure located at the trimer apex" (Section 2.1.2). No vendor, catalog #, clone designation, RRID, or host species stated. Source: Steichen et al. 2019 (reference 24) — unverifiable from manuscript alone whether that paper provides full traceability. |
| **BG18_GL0 antibody** | **HARD: PARTIAL** | Used in BLI assays (Sections 2.1.2, 2.2.5, 3.1.2, 3.1.3). Described as "directed against the glycan-V3 portion of Env" (Section 2.1.2). No vendor, catalog #, clone, RRID, or host species stated. Source: Steichen et al. 2019 (reference 24) — unverifiable. |
| **DEN3 antibody** | **HARD: PARTIAL** | Used as negative control in BLI (Section 2.1.2). No vendor, catalog #, clone, RRID, or host species stated. Source: Steichen et al. 2019 (reference 24) — unverifiable. |
| **2G12 antibody** | **HARD: PARTIAL** | Used for affinity chromatography capture (Sections 2.5.4.1, 3.3.1). Vendor stated as "Polymun Scientific, Austria" (Section 2.5) but no catalog #, clone, RRID, or host species. Residual 2G12 quantified by ELISA (Section 2.2.7) but no details on the detection antibody or assay kit. |
| **Anti-Human Fc Capture (AHC) biosensor tips** | **HARD: PARTIAL** | Used in BLI (Section 2.1.2). Vendor and catalog # provided: "ForteBio Cat. 18-5060" but no further characterization. |
| **Anti-Protein A antibodies (ELISA)** | **HARD: PARTIAL** | Used in residual Protein A quantification (Section 2.2.9). Kit named: "Mix-N-Go Protein A ELISA Kit with Amsphere™ A3 (JSR Life Sciences, CA, USA)" and reference standard "F610, Cygnus Technologies" — vendor and catalog # present but no clone, RRID, or host species for the capture/detection antibodies themselves. |
| **Anti-CHO polyclonal antibodies (HCP ELISA)** | **HARD: PARTIAL** | Used in Section 2.2.4. Kit: "third-generation CHO HCP ELISA kit (Cygnus Technologies, Southport, NC)" — vendor named but no catalog #. Described as "affinity-purified anti-CHO polyclonal antibodies" but no host species, RRID, or further detail. |
| **Alkaline phosphatase–conjugated secondary (2G12 ELISA)** | **HARD: MISSING** | Section 2.2.7 mentions "alkaline phosphatase–conjugated secondary antibody" for 2G12 quantification but provides no vendor, catalog #, host species, or RRID. |
| **Horseradish peroxidase–conjugated secondary (HCP ELISA)** | **HARD: MISSING** | Section 2.2.4 mentions "horseradish peroxidase (HRP)" conjugate but no vendor, catalog #, host species, or RRID. |
| **Dilution/application for all antibodies** | **HARD: PARTIAL** | BLI assays: PGT145 and BG18_GL0 "diluted to 10 µg/mL" (Section 2.1.2). ELISA assays: no dilutions stated for primary or secondary antibodies. |

### Cell Lines / Primary Cells

**Trigger:** Yes — CHO cell line is central to the work.

| Item | Status | Finding |
|------|--------|---------|
| **Parental cell line source** | **HARD: PRESENT** | "HD BIOP3 is a GS-null cell line derived from ECACC CHOK1 established by Horizon Discovery" (Section 2.3.1). ECACC is a recognized repository; Horizon Discovery is named. However, no RRID provided for HD BIOP3 or CHOK1. |
| **RRID for cell line** | **HARD: MISSING** | No RRID (Research Resource Identifier) provided for HD BIOP3 or the derived C235 clone. |
| **STR authentication** | **HARD: MISSING** | No statement that the cell line was authenticated by STR profiling. |
| **Mycoplasma testing** | **HARD: MISSING** | No statement of mycoplasma testing at any passage (RCB, MCB, or during culture). |
| **Culture media and supplements** | **SOFT: PRESENT** | EX-CELL Advanced CHO Fed-batch (AFB) media (SAFC, St. Louis, MO) — vendor and supplier named. Dynamis medium (Thermofisher Scientific, Waltham, MA) — vendor and supplier named. Cell Boost 7a, 7b, Cellboost 7, Cellvento 4 feeds (Cytiva, Marlborough, MA) — vendor named. However, no catalog #s for most media components. Antifoam (10% ADCF, Thermofisher Scientific) — vendor and concentration stated but no catalog #. |
| **Passage number tracking** | **SOFT: PRESENT** | Passage numbers tracked during medium adaptation (Passage 1–5, Section 2.4.1) and genetic stability studies (PD0, PD60, Section 2.3.8). However, no statement of maximum passage number used for manufacturing or whether passage number limits were enforced. |

### Chemicals / Drugs / Dosing

**Trigger:** Yes — many reagents and buffers used; viral inactivation with Triton X-100; feeds and supplements.

| Item | Status | Finding |
|------|--------|---------|
| **Triton X-100 (detergent inactivation)** | **HARD: PRESENT** | Vendor: SAFC, St. Louis, MO (Section 2.5.4.3). Concentration: 0.5% (v/v) from 10% stock. Hold time: 60–90 min at 20 ± 5 °C. However, no catalog # or CAS # provided. |
| **Amberlite XAD-2 resin** | **HARD: PARTIAL** | Vendor: MilliporeSigma, MA, USA (Section 2.5.4.4). No catalog # provided. |
| **Sodium hydroxide (NaOH)** | **HARD: PARTIAL** | Concentrations stated (0.5 M, 0.1 M) but no vendor or catalog #. |
| **Magnesium chloride (MgCl₂)** | **HARD: PARTIAL** | Concentration stated (3 M) but no vendor or catalog #. |
| **Phosphate-buffered saline (PBS)** | **HARD: PARTIAL** | pH 7.4 stated but no vendor, catalog #, or composition details. |
| **Tris buffer** | **HARD: PARTIAL** | Concentrations and pH stated (e.g., 20 mM Tris, 75 mM NaCl, pH 8.0) but no vendor or catalog #. |
| **N-Ethylmaleimide (NEM)** | **HARD: PARTIAL** | Concentration: 10 mM (Section 2.1.1). Vendor: Catalog #E3876-5G (Sigma, implied) but vendor name not explicitly stated. |
| **Acetone, acetonitrile, TFA (HPLC solvents)** | **HARD: MISSING** | Used in RP-HPLC (Section 2.2.6) and Triton X-100 quantification (Section 2.2.8) but no vendor, grade, or catalog # stated. |
| **Uranyl formate (EM stain)** | **HARD: PARTIAL** | Concentration: 2% (w/v) (Section 2.7.2). Vendor not stated. |
| **Glow-discharge carbon-coated copper grids** | **HARD: PARTIAL** | Vendor: Electron Microscopy Sciences (Section 2.7.2). No catalog # provided. |
| **Whatman #1 filter paper** | **HARD: PARTIAL** | Named (Section 2.7.2) but no vendor or catalog #. |

### Oligos / Plasmids / Constructs

**Trigger:** Yes — plasmid constructs for N332-GT5 and furin, transposon system, PCR primers for transcript analysis.

| Item | Status | Finding |
|------|--------|---------|
| **N332-GT5 gp140 expression construct** | **HARD: PARTIAL** | Described as "Leap In1 transposon-based backbone" with "codon-optimized coding sequence" (Section 2.3.3). Codons optimized using "ATUM's proprietary algorithm." Sequences "chemically synthesized from phosphoramidites, cloned into intermediate vectors, and transformed into E. coli" (Section 2.3.3). No plasmid sequence deposited (GenBank, Addgene, or other). No full construct map or sequence provided in manuscript or supplement. Source: ATUM Bio (Section 2.3.3). |
| **Furin expression construct** | **HARD: PARTIAL** | Described as "Leap In1 transposon-based backbone" with "codon-optimized human furin ORF" (Section 2.3.3). Same limitations as N332-GT5 construct — no sequence, no deposit. |
| **Leap-In transposon system** | **HARD: PARTIAL** | Described as "five different transposons and their corresponding cognate transposases" (Section 2.3.2). Developed by ATUM. No sequences, no catalog #s, no deposit location. Mechanism described ("cut-and-paste," "DD[D/E] integrase family") but no specific transposon names or transposase variants identified. |
| **PCR primers (transcript analysis)** | **HARD: MISSING** | Section 2.1.3 states "gene-specific primers" were used for RT-PCR of N332-GT5 and furin but no primer sequences provided. OneStep RT-PCR Amplification Kit (Qiagen Cat. 210212) named but no primer details. |
| **Glutamine synthetase (GS) selection cassette** | **HARD: PARTIAL** | Mentioned as present in both constructs (Section 2.3.3) but no sequence, no details on selection mechanism or concentration of selection agent (L-glutamine withdrawal) used. |

### Genomics / Sequencing / Omics

**Trigger:** Yes — transcript sequence analysis (RT-PCR + Sanger sequencing), qPCR for residual CHO DNA, mass spectrometry for glycosylation and proteomics.

#### Transcript Sequencing (Section 2.1.3)

| Item | Status | Finding |
|------|--------|---------|
| **Sequencing platform** | **HARD: PARTIAL** | "Sanger chemistry with 100% double-stranded coverage" stated (Section 2.1.3). No sequencing vendor or instrument named. |
| **Reference sequence** | **HARD: MISSING** | No reference sequence provided for N332-GT5 or human furin. No GenBank accession or supplementary sequence file. |
| **Alignment/analysis tool** | **HARD: MISSING** | No tool named for sequence assembly or comparison. Statement: "The presence and the perfect match to the expected sequences have been confirmed" (Section 2.1.3) but no method or software version. |
| **Deposit location** | **HARD: MISSING** | No mention of sequence deposition (GenBank, ENA, DDBJ). |

#### qPCR for Residual CHO DNA (Section 2.2.3)

| Item | Status | Finding |
|------|--------|---------|
| **qPCR platform and mode** | **HARD: PRESENT** | "Bio-Rad CFX384 Real-Time PCR Detection System (Bio-Rad Laboratories)" (Section 2.2.3). No instrument version. |
| **Primer/probe sequences** | **HARD: MISSING** | "CHO-specific primers and a TaqMan® probe targeting a conserved genomic sequence" (Section 2.2.3) but no sequences provided. |
| **Reference genome** | **HARD: MISSING** | No CHO genome version or accession stated. |
| **Analysis software** | **HARD: PARTIAL** | "CFX Manager software" named (Section 2.2.3) but no version. |
| **Standard curve details** | **HARD: PARTIAL** | "Standard curve generated from known concentrations of CHO DNA" (Section 2.2.3) but no details on standard source, range, or number of points. |

#### Mass Spectrometry (Sections 2.7.1, 3.6.1)

**DeGlyPHER method:**

| Item | Status | Finding |
|------|--------|---------|
| **Instrument** | **HARD: PRESENT** | "Q Exactive HF-X mass spectrometer (Thermo)" (Section 2.7.1). No version or firmware stated. |
| **Acquisition mode** | **HARD: PRESENT** | "Data-dependent mode with HCD fragmentation" (Section 2.7.1). No MS1 resolution, AGC target, max IT, or MS2 settings stated. |
| **Sample prep / digestion** | **HARD: PRESENT** | "Disulfide bonds reduced and alkylated before digestion with Proteinase K, followed by sequential deglycosylation with Endo H and then PNGase F in the presence of H₂¹⁸O" (Section 2.7.1). No enzyme vendor, catalog #, or incubation conditions (time, temperature, pH, buffer). |
| **Separation** | **HARD: PARTIAL** | "Peptides separated on C18 resin using an EASY-nLC 1200 UHPLC (Thermo)" (Section 2.7.1). No gradient, flow rate, or column dimensions. |
| **Search engine** | **HARD: PRESENT** | "ProLuCID (Xu et al., 2015)" (Section 2.7.1). Reference provided (ref. 30). No version stated in manuscript. |
| **Database** | **HARD: PRESENT** | "Known protein sequence of N332-GT5 within a CHO (Chinese Hamster Ovary) cell proteome background" (Section 2.7.1). No database version or source (e.g., UniProt, NCBI). |
| **FDR and modifications** | **HARD: PRESENT** | "Up to 1% FDR (Peng et al., 2003) using DTASelect2 (Tabb et al., 2002)" (Section 2.7.1). Static modification: C+57.02146 Da. Variable modifications: N+2.988261 Da (complex glycans), N+203.079373 Da (high-mannose/hybrid), M+15.994915 Da, N-terminal Q–17.026549 Da. No mass tolerances (precursor or fragment) stated. |
| **Quantification** | **HARD: PARTIAL** | "Census2 (Park et al., 2008) label-free analysis, applying 'match between runs'" (Section 2.7.1). No details on normalization, missing-value handling, or statistical test. |
| **Post-processing** | **HARD: PARTIAL** | "GlycoMSQuant (Baboo et al., 2021) used to compile final results, aligning PNGS to Env of the HXB2 HIV-1 variant" (Section 2.7.1). No version stated. |
| **Repository accession** | **HARD: MISSING** | No mention of deposition in PRIDE, MassIVE, or other proteomics repository. |

**LC-MS glycoproteomics method:**

| Item | Status | Finding |
|------|--------|---------|
| **Instrument** | **HARD: PRESENT** | "Thermo Orbitrap Eclipse" (Section 2.7.1). No version or firmware. |
| **Acquisition mode** | **HARD: MISSING** | No MS1 resolution, AGC, max IT, or MS2 settings stated. |
| **Sample prep / digestion** | **HARD: PRESENT** | "Three proteases – trypsin, chymotrypsin, and alpha-lytic protease (Watanabe et al., 2020)" (Section 2.7.1). No enzyme vendor, catalog #, incubation conditions, or rationale for three proteases. |
| **Separation** | **HARD: MISSING** | No LC method, column, gradient, or flow rate stated. |
| **Search engine / analysis** | **HARD: PRESENT** | "Byos (Protein Metrics)" (Section 2.7.1). No version stated. |
| **Database / glycoform library** | **HARD: PARTIAL** | "Glycoform library of candidate oligomannose- and complex-type glycans" (Section 2.7.1) but no source, size, or composition. |
| **Repository accession** | **HARD: MISSING** | No deposition mentioned. |

### Microscopy / Imaging / Flow Cytometry

**Trigger:** Yes — negative-stain electron microscopy (Section 2.7.2, 3.6.2).

| Item | Status | Finding |
|------|--------|---------|
| **Instrument model** | **HARD: PRESENT** | "FEI Tecnai Spirit TEM equipped with an FEI Eagle 4K CCD (120 kEV, 2.06 Å pixel size, 52,000 nominal magnification)" (Section 2.7.2). No microscope version or firmware. |
| **Objective / NA / detector** | **HARD: PRESENT** | Pixel size and magnification stated; 120 kEV acceleration voltage stated. No objective NA or detector gain/offset. |
| **Sample preparation** | **HARD: PRESENT** | "Diluted in Tris-buffered saline (50 mM Tris pH 7.4, 150 mM NaCl) to 0.02 mg/mL, adsorbed onto glow-discharged, carbon-coated copper grids" (Section 2.7.2). Stain: "2% (w/v) uranyl formate for 45 s" (Section 2.7.2). |
| **Data collection** | **HARD: PARTIAL** | "82 micrographs collected" (Section 2.7.2). "Data collection automated using Leginon (Suloway et al., 2005)" (Section 2.7.2). No exposure time, defocus range, or dose stated. |
| **Image processing software** | **HARD: PARTIAL** | "CryoSPARC (Pujani et al., 2017)" (Section 2.7.2). No version stated. "Blob Picker (minimum circular diameter 180 Å)" — no software name or version. |
| **Particle extraction and classification** | **HARD: PARTIAL** | "Particles extracted at 160 pixel box size. Particle stack subjected to two rounds of 2D classification, with a total of 6,086 particles analyzed" (Section 2.7.2). No 2D classification parameters (number of classes, convergence criteria, mask). |
| **Comparison / validation** | **HARD: PARTIAL** | "Comparison to previously published HIV Env SOSIP production runs (Dey et al., 2018; Bale et al., 2025)" (Section 2.7.2). No quantitative metrics (e.g., FSC, resolution, RMSD) or gating strategy for "native-like trimers." |

---

## PROTOCOL PROVENANCE & DELEGATION

### Methods Delegated to References

| Method | Reference | Status | Finding |
|--------|-----------|--------|---------|
| **SDS-PAGE staining (InstantBlue™)** | Vendor protocol (Invitrogen) | **DELEGATED-RESOLVABLE** | Vendor protocol is standard and resolvable. Catalog #s provided (NP0008, NP0009, NP0329BOX, ISB1L-1L). |
| **Octet BLI assay** | Vendor protocol (ForteBio) implied | **DELEGATED-RESOLVABLE** | Assay buffer and biosensor tips cited with catalog #s (18-1105, 18-5060). Vendor protocols are standard. |
| **RNeasy Mini Kit (RNA extraction)** | Qiagen vendor protocol | **DELEGATED-RESOLVABLE** | Standard kit; vendor protocol is resolvable. |
| **OneStep RT-PCR Amplification Kit** | Qiagen Cat. 210212 | **DELEGATED-RESOLVABLE** | Standard kit; vendor protocol is resolvable. However, gene-specific primer sequences are NOT provided (see Oligos section above). |
| **Ambr®250 process optimization** | Rameez et al., 2014 (ref. 17) | **DELEGATED-RESOLVABLE** | Reference provided. Rameez et al. 2014 is a published paper on Ambr®250 scalability. However, the specific study parameters (Table 1) are novel to this work and fully described in the manuscript. |
| **BG505 SOSIP.664 downstream process** | Dey et al., 2018 (ref. 7) | **DELEGATED-RESOLVABLE** | Reference provided (DOI: 10.1002/bit.26498). Manuscript states "process developed based on the process established for BG505 SOSIP.664" (Section 2.5) and notes deviations ("modified to be operated using a 20 cm bed height," Section 2.5.1). Dey et al. 2018 is a published cGMP manufacturing paper and plausibly contains the original process. However, the manuscript does not state which specific steps were adopted vs. modified, making full traceability difficult without consulting Dey et al. |
| **Leginon (EM data collection)** | Suloway et al., 2005 (ref. 25) | **DELEGATED-RESOLVABLE** | Reference provided. Suloway et al. 2005 is a published paper on Leginon. |
| **CryoSPARC (EM image processing)** | Pujani et al., 2017 (ref. 18) | **DELEGATED-RESOLVABLE** | Reference provided. Pujani et al. 2017 is a published paper on CryoSPARC. However, no version of CryoSPARC is stated. |
| **DeGlyPHER (glycan analysis)** | Baboo et al., 2023 (ref. 2) and Baboo et al., 2021 (ref. 1) | **DELEGATED-RESOLVABLE** | References provided. Baboo et al. 2023 is a Methods in Enzymology chapter and Baboo et al. 2021 is a published paper. Both are resolvable. However, the manuscript does not state whether the protocol was followed exactly or modified. |
| **LC-MS glycoproteomics (multiple proteases)** | Watanabe et al., 2020 (ref. 28) | **DELEGATED-RESOLVABLE** | Reference provided. Watanabe et al. 2020 is a published paper. However, the manuscript does not detail whether the protocol was followed exactly or adapted. |
| **ProLuCID search engine** | Xu et al., 2015 (ref. 30) | **DELEGATED-RESOLVABLE** | Reference provided. Xu et al. 2015 is a published paper. No version of ProLuCID stated in the manuscript. |
| **DTASelect2 (FDR filtering)** | Tabb et al., 2002 (ref. 26) | **DELEGATED-RESOLVABLE** | Reference provided. Tabb et al. 2002 is a published paper. No version stated. |
| **Census2 (quantification)** | Park et al., 2008 (ref. 14) | **DELEGATED-RESOLVABLE** | Reference provided. Park et al. 2008 is a published paper. No version stated. |
| **GlycoMSQuant (post-processing)** | Baboo et al., 2021 (ref. 1) | **DELEGATED-RESOLVABLE** | Reference provided. Baboo et al. 2021 is a published paper. No version stated. |
| **Byos (LC-MS analysis)** | Protein Metrics (vendor) | **DELEGATED-RESOLVABLE** | Vendor software; no version stated. |
| **CFX Manager (qPCR analysis)** | Bio-Rad (vendor) | **DELEGATED-RESOLVABLE** | Vendor software; no version stated. |

### Deviations from Cited Protocols

| Method | Cited Protocol | Stated Deviation | Status |
|--------|---|---|---|
| **Downstream process** | Dey et al., 2018 (BG505 SOSIP.664) | "Modified to be operated using a 20 cm bed height" for MabSelect SuRe and Capto adhere (Section 2.5.1). Preparative SEC removed due to resin supply constraints (Section 3.3.2). | **PARTIAL** — Major deviations (removal of SEC, bed height changes) are noted, but the extent of other modifications is not systematically documented. |

---

## SUMMARY TABLE: HARD vs. SOFT MISSING ITEMS

### HARD Missing (Blocking Reproducibility)

| Category | Item | Impact |
|----------|------|--------|
| **Cross-cutting** | Statistical test and p-values | No formal comparison of conditions (Ambr®250 variants, pilot vs. GMP). Descriptive only. |
| **Cross-cutting** | Data availability statement | No repository, supplementary data, or access conditions stated. |
| **Antibodies** | Vendor/catalog # for PGT145, BG18_GL0, DEN3 | Cannot source exact antibodies; traceability to Steichen et al. 2019 unverifiable from manuscript. |
| **Antibodies** | Vendor/catalog # for 2G12 detection antibody (ELISA) | Cannot source detection reagent. |
| **Antibodies** | Host species, clone, RRID for all antibodies | Standard identifiers missing across all antibody uses. |
| **Cell lines** | RRID for HD BIOP3 and C235 clone | No standard identifier for cell line. |
| **Cell lines** | STR authentication and mycoplasma testing | No authentication or contamination testing documented. |
| **Chemicals** | CAS # or catalog # for Triton X-100, buffers, salts | Cannot verify exact reagent identity. |
| **Oligos/Plasmids** | N332-GT5 and furin construct sequences | No sequence deposit (GenBank, Addgene); cannot verify construct or replicate transfection. |
| **Oligos/Plasmids** | Leap-In transposon sequences and transposase variants | No sequences; cannot replicate cell line development. |
| **Oligos/Plasmids** | PCR primer sequences (RT-PCR, transcript analysis) | Cannot replicate transcript verification. |
| **Genomics** | Sanger sequencing vendor and reference sequence | No reference sequence provided; no deposit location. |
| **Genomics** | qPCR primer/probe sequences and CHO genome version | Cannot replicate qPCR assay. |
| **Mass spec** | MS1/MS2 acquisition parameters (resolution, AGC, max IT) | Cannot replicate MS data acquisition. |
| **Mass spec** | Proteinase K vendor, catalog #, incubation conditions | Cannot replicate digestion. |
| **Mass spec** | Endo H and PNGase F vendor, catalog #, conditions | Cannot replicate deglycosylation. |
| **Mass spec** | Mass tolerances (precursor and fragment) | Cannot replicate search. |
| **Mass spec** | Glycoform library source and composition | Cannot replicate glycan identification. |
| **Mass spec** | Repository accession (PRIDE, MassIVE) | Raw data not deposited. |
| **Microscopy** | Exposure time, defocus range, dose for EM | Cannot replicate data collection. |
| **Microscopy** | 2D classification parameters (# classes, convergence) | Cannot replicate image processing. |
| **Microscopy** | Quantitative metrics for "native-like trimer" validation | No FSC, resolution, or gating criteria stated. |

### SOFT Missing (Recommended but Not Blocking)

| Category | Item | Impact |
|----------|------|--------|
| **Cross-cutting** | Software versions (Octet, CFX384, SoloVPE, UPLC, EM instruments) | Reproducibility reduced; exact conditions difficult to match. |
| **Cross-cutting** | Error bars on all figures | Inconsistent uncertainty reporting. |
| **Cell lines** | Passage number limits for manufacturing | No statement of maximum passage used. |
| **Chemicals** | Catalog #s for media, feeds, antifoam | Procurement slightly more difficult. |
| **Mass spec** | Normalization and missing-value handling for quantification | Reproducibility of quantitative results reduced. |
| **Microscopy** | Detector gain/offset settings | Reproducibility of image contrast reduced. |

---

## NOTES ON UNVERIFIABLE ITEMS

The following delegated methods cannot be verified from the manuscript alone:

1. **Steichen et al., 2019 (ref. 24)** — Cited for PGT145, BG18_GL0, DEN3 antibody sources and for N332-GT series design. The manuscript does not confirm whether that paper provides vendor/catalog #s or full antibody characterization. **Unverifiable without consulting ref. 24.**

2. **Dey et al., 2018 (ref. 7)** — Cited as the source of the BG505 SOSIP.664 downstream process. The manuscript states the N332-GT5 process was "developed based on" this process but does not itemize which steps were adopted vs. modified. **Unverifiable without consulting ref. 7.**

3. **Baboo et al., 2023 and 2021 (refs. 2, 1)** — DeGlyPHER protocol. The manuscript does not state whether the protocol was followed exactly or adapted. **Unverifiable without consulting refs. 1, 2.**

4. **Watanabe et al., 2020 (ref. 28)** — LC-MS glycoproteomics with three proteases. No statement of adherence to or deviation from the published protocol. **Unverifiable without consulting ref. 28.**

---

## CONCLUSION

This manuscript describes a complex, multi-stage bioprocess (cell line development, upstream fermentation, downstream purification, viral clearance, product characterization) but lacks sufficient detail in several critical areas to enable independent reproduction:

- **Antibody sourcing** is incomplete; traceability depends on unverified citations.
- **Cell line authentication** (STR, mycoplasma) is not documented.
- **Plasmid/construct sequences** are not deposited.
- **Mass spectrometry parameters** (MS settings, tolerances, glycoform library) are incomplete.
- **Microscopy image processing** (2D classification, validation metrics) lacks detail.
- **Statistical comparison** of process variants is absent.
- **Data availability** is not addressed.

The work is primarily a **process development and manufacturing report** rather than a research discovery paper, and many methods are delegated to vendor protocols or prior publications. However, the load-bearing methods (cell line development, Ambr®250 optimization, downstream purification robustness, viral clearance, glycosylation analysis) would benefit from more complete specification of parameters, software versions, and raw data deposition to support reproducibility and future process improvements.