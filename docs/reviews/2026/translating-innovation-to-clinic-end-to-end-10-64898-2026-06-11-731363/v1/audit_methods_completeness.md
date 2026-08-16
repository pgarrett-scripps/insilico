# Methods Completeness & Reagent Traceability Report

**Manuscript:** Translating Innovation to Clinic: End-to-End Bioprocess Development and cGMP Manufacturing of N332-GT5 HIV Vaccine Candidate for First-in-Human Trials HVTN144

**Auditor role:** Methods Completeness & Reagent Traceability Auditor

**Date of review:** Based on manuscript as provided

---

## Categories Triggered and Checked

The following checklist categories are triggered by content in this manuscript:

| Category | Trigger found in manuscript |
|---|---|
| Cell lines / primary cells | CHO cell line HD BIOP3, clone C235 |
| Antibodies / immunodetection | 2G12, PGT145, BG18_GL0, DEN3 used in BLI/Octet and ELISA |
| Mass spectrometry (proteomics/glycomics) | DeGlyPHER, LC-MS glycoproteomics |
| Microscopy / imaging | Negative-stain electron microscopy |
| Chemicals / drugs / dosing | Buffers, feeds, adjuvants, Triton X-100, MgCl₂, etc. |
| Oligos / plasmids / constructs | Expression constructs, transposon system, codon-optimized sequences |
| Computational / ML / modeling | GlycoMSQuant, Byos, ProLuCID, IP2, CryoSPARC, Leginon |
| Cross-cutting items | Sample size, statistics, software versions, data availability |
| Human subjects / clinical (partial) | Reference to HVTN144 trial (NCT05217641) — checked only for trial registration, not for patient data (none presented) |

Categories **not** triggered and therefore not checked: model organisms/in vivo (no animal data presented in this manuscript), genomics/sequencing (no NGS data presented).

---

## Cross-Cutting Items (apply to all manuscripts)

| Item | Status | Finding |
|---|---|---|
| Sample size n stated, with what n represents | **Missing (HARD)** | Section 3.3.1 reports "1-3", "4", "5" for cycles but does not state whether these are biological or technical replicates. Section 2.7.2 states "6,086 particles analyzed" for nsEM but does not state whether this is from one grid/micrograph set or multiple independent preparations. Section 3.2.2 reports a single Ambr250 run per condition (n=1 per condition) without stating this explicitly. No replicate count is given for the pilot-scale or GMP runs (n=1 each). |
| Named statistical test | **Missing (HARD)** | No statistical test is named anywhere in the manuscript. Section 2.2 describes assays but no statistical methods. Tables 8 and 12 report means ± SD without stating the test used. Section 3.3.3 describes trends without statistical testing. |
| What error bars / ± values represent (SD/SEM/CI) | **Unverifiable** | Tables 7, 8, 9, and 12 report "±" values but the manuscript never states whether these are SD or SEM. Figure 17 states "standard error of mean" in the caption (SEM), and Figure 18 states "average (+/- SEM)". However, Tables 7–9 and 12 do not specify. This is inconsistent reporting. |
| Software/tool/instrument versions | **Partially missing (HARD)** | Several tools are named without versions: Octet RED384 (no model version), CryoSPARC (no version), Leginon (no version), Byos (no version), ProLuCID (no version), Census2 (no version), DTASelect2 (no version), GlycoMSQuant (no version), IP2 (no version), CFX Manager (no version), SoloVPE (no version). Instruments with model numbers but no software versions: Q Exactive HF-X, Orbitrap Eclipse, FEI Tecnai Spirit, FEI Eagle 4K CCD. |
| Data-availability statement | **Missing (SOFT)** | No data-availability statement appears anywhere in the manuscript. |
| Code availability (custom analysis) | **Missing (SOFT)** | Custom analysis tools are named (DeGlyPHER, GlycoMSQuant) but no code repository or availability statement is given. |

---

## Cell Lines / Primary Cells

Trigger: HD BIOP3 CHO cell line, clone C235.

| Item | Status | Finding |
|---|---|---|
| Source of parental cell line | **Present** | Section 2.3.1: "HD BIOP3 is a GS-null cell line derived from ECACC CHOK1 established by Horizon Discovery." |
| RRID / CVCL identifier | **Missing (HARD)** | No RRID or CVCL identifier is given for HD BIOP3 or for the parental CHOK1. |
| Authentication (STR or other) | **Missing (HARD)** | No authentication statement (STR profiling, isozyme, or other) is provided for the parental line or the derived clone. |
| Mycoplasma testing | **Missing (HARD)** | No mycoplasma testing statement appears anywhere in the manuscript. |
| Media and supplements (SOFT) | **Present** | Section 2.4.1: EX-CELL Advanced CHO Fed-batch (SAFC), Dynamis (ThermoFisher), Cell Boost 7a/7b (Cytiva), Cellvento 4 Feed, L-glutamine. Vendor names are given; catalog numbers are not provided for all (e.g., Cell Boost 7a/7b have no catalog #). |

---

## Antibodies / Immunodetection

Trigger: 2G12, PGT145, BG18_GL0, DEN3 used in BLI and ELISA.

| Item | Status | Finding |
|---|---|---|
| Vendor | **Partial** | 2G12: "Polymun Scientific, Austria" (Section 2.5). PGT145, BG18_GL0, DEN3: no vendor stated. Section 2.1.2 refers to "Steichen et al., 2019" for these antibodies but does not state where they were obtained. |
| Catalog number | **Missing (HARD)** | No catalog numbers for any antibody. |
| Clone / RRID | **Missing (HARD)** | No clone identifiers beyond the antibody names themselves (PGT145, BG18_GL0, DEN3, 2G12). No RRIDs. |
| Application + dilution | **Partially present** | Section 2.1.2 states antibodies diluted to 10 µg/mL for BLI. Section 2.2.7 describes a Protein A ELISA for residual 2G12 but gives no dilution. No other applications/dilutions are specified. |
| Host species / clonality | **Missing (HARD)** | Not stated for any antibody. 2G12 is a human monoclonal (widely known) but the manuscript does not state this. PGT145, BG18_GL0, DEN3 clonality not stated. |

---

## Mass Spectrometry (Proteomics / Glycomics)

Trigger: DeGlyPHER, LC-MS glycoproteomics, Q Exactive HF-X, Orbitrap Eclipse.

| Item | Status | Finding |
|---|---|---|
| Instrument + acquisition mode | **Partially present** | Section 2.7.1: "Q Exactive HF-X mass spectrometer (Thermo)" and "Thermo Orbitrap Eclipse" are named. Acquisition mode: "data-dependent mode with HCD fragmentation" is stated for DeGlyPHER. For the traditional LC-MS method, no acquisition mode is stated. |
| Sample prep / digestion / enrichment | **Present** | Section 2.7.1: reduction/alkylation, Proteinase K digestion, Endo H then PNGase F in H₂¹⁸O for DeGlyPHER; trypsin, chymotrypsin, alpha-lytic protease for LC-MS glycoproteomics. |
| Search engine + version | **Partially present** | ProLuCID is named (no version). Byos (Protein Metrics) is named (no version). |
| Database + version | **Partially present** | DeGlyPHER: "CHO (Chinese Hamster Ovary) cell proteome background" — no database version or download date. Byos: no database specified. |
| FDR + modifications + tolerances | **Partially present** | FDR: "up to 1% FDR" stated for DeGlyPHER. Modifications: C+57.02146 (static), N+2.988261, N+203.079373, M+15.994915, N-term Q−17.026549 (variable) — stated. Precursor/fragment mass tolerances: **not stated**. |
| Repository accession (PRIDE/MassIVE) | **Missing (HARD)** | No repository accession is given for any mass spectrometry data. |
| Quant method | **Present** | Label-free with "match between runs" via Census2 — stated. |
| Replicates | **Unverifiable** | Section 2.7.1 states "For each replicate" for LC-MS glycoproteomics but does not state how many replicates were performed. DeGlyPHER replicate count not stated. |

---

## Microscopy / Imaging

Trigger: Negative-stain electron microscopy (nsEM).

| Item | Status | Finding |
|---|---|---|
| Instrument model | **Present** | FEI Tecnai Spirit TEM with FEI Eagle 4K CCD — Section 2.7.2. |
| Objective / magnification / detector settings | **Partially present** | Magnification (52,000×) and pixel size (2.06 Å) are stated. Detector is named (Eagle 4K CCD) but no camera settings (exposure, binning) are given. |
| Analysis software + version | **Missing (HARD)** | CryoSPARC and Leginon are named without versions. Blob Picker is named without version. |
| Gating strategy | **N/A** | No flow cytometry in this manuscript. |

---

## Chemicals / Drugs / Dosing

Trigger: Numerous buffers, feeds, detergents, salts.

| Item | Status | Finding |
|---|---|---|
| Identity traceable to vendor + catalog # or CAS | **Partially present** | Vendors are named for many reagents (e.g., Cytiva, MilliporeSigma, ThermoFisher, SAFC, Asahi Kasei, Sartorius, JSR Life Sciences, Cygnus Technologies, Polymun Scientific). Catalog numbers are given for some (e.g., TSKgel column Cat#22856, Acquity UPLC column Cat#186004497, ZORBAX Cat#865750-906, RNeasy Mini Kit, OneStep RT-PCR Kit Cat. 210212) but **not for the majority** of reagents. No CAS numbers are given for any chemical. |
| Dose / concentration per experiment | **Present** | Concentrations are given throughout (e.g., 3 M MgCl₂, 0.5% Triton X-100, 20 mM Tris, 75 mM NaCl, 10 µg/mL antibodies, feed percentages). |
| Route / mode | **Present** | Chromatography modes, filtration modes, and bioreactor operations are described. |
| Vehicle + final concentration | **Present** | Buffer compositions are given for each step. |
| Schedule | **Present** | Feed schedules, hold times, and process durations are stated. |

---

## Oligos / Plasmids / Constructs

Trigger: Leap-In transposon system, expression constructs for N332-GT5 gp140 and human furin.

| Item | Status | Finding |
|---|---|---|
| Plasmid source (Addgene #) or full description | **Partially present** | Section 2.3.3 describes the constructs ("Leap In1 transposon-based backbone", "glutamine synthetase cassette", codon-optimized) but gives no full plasmid map, no Addgene number, and no sequence. The codon optimization algorithm is described as "ATUM's proprietary algorithm" — not independently reproducible. |
| Primer / oligo sequences | **Missing (HARD)** | Section 2.1.3 mentions "gene-specific primers" for RT-PCR/Sanger sequencing but no primer sequences are given. |
| gRNA / shRNA / siRNA target sequences | **N/A** | Not used. |
| Cas variant + delivery + edit validation | **N/A** | Transposase (not Cas) is used. Delivery is stated (electroporation with Leap In 1 mRNA). Edit validation is described via sequencing (Section 2.1.3). |
| Selection markers | **Present** | Glutamine synthetase cassette is stated. |
| Off-target assessment | **Missing (SOFT)** | No off-target integration assessment is described for the transposon system. |

---

## Computational / ML / Modeling

Trigger: CryoSPARC (2D classification), ProLuCID (search), GlycoMSQuant (quant), Byos (glycoproteomics), IP2 (pipeline).

| Item | Status | Finding |
|---|---|---|
| Dataset(s) with version + train/val/test split | **N/A** | No ML training is performed; the computational tools are used for analysis, not model training. |
| Architecture / algorithm | **Partially present** | Algorithms are named (Blob Picker, 2D classification) but not described in detail. |
| Hyperparameters | **Missing (HARD)** | For CryoSPARC: no particle box size is stated in Section 2.7.2 (the manuscript says "160 pixel box size" — this is present). No number of 2D classes, no number of iterations, no other parameters. For ProLuCID: no precursor/fragment tolerance, no enzyme specificity, no missed-cleavage settings. |
| Training procedure | **N/A** | No training performed. |
| Library versions + hardware | **Missing (HARD)** | No library versions for any tool. Hardware for mass spec is named (Q Exactive HF-X, Orbitrap Eclipse) but no hardware for CryoSPARC processing is given. |
| Random seeds / seed-averaging | **N/A** | No stochastic training. |
| Code availability | **Missing (SOFT)** | DeGlyPHER and GlycoMSQuant are named as tools but no code repository is given. |
| Compute budget | **Missing (SOFT)** | Not stated. |
| Metric definitions | **Partially present** | FDR (1%) is stated for DeGlyPHER. Other metrics (e.g., how "processivity" is defined) are not defined. |

---

## Human Subjects / Clinical (partial check)

Trigger: HVTN144 trial is named (NCT05217641) but no patient data are presented in this manuscript. The manuscript is a manufacturing/process development paper, not a clinical report.

| Item | Status | Finding |
|---|---|---|
| Trial registration # | **Present** | NCT05217641 is cited in reference [10]. |
| IRB approval + informed consent | **Not applicable to this manuscript** | No patient data are presented. The trial itself is referenced but not reported. |
| Inclusion/exclusion criteria | **Not applicable** | Not reported in this manuscript. |
| Participant demographics | **Not applicable** | Not reported in this manuscript. |
| Reporting-guideline adherence | **Not applicable** | Not a clinical report. |

---

## Protocol-Provenance Check (delegated methods)

The following methods are delegated by citation:

| Delegated method | Citation | Status | Assessment |
|---|---|---|---|
| BG505 SOSIP.664 downstream process basis | Dey et al., 2018 (ref [7]) | **Delegated-resolvable** | Full citation with DOI (10.1002/bit.26498). Plausibly contains the protocol. However, the manuscript states the N332-GT5 process was "developed based on" this process but does not state which specific deviations were made. The deviations are described in the text (e.g., different columns, different conditions) but not explicitly framed as deviations from Dey et al. |
| Antibody generation (PGT145, BG18_GL0, DEN3) | Steichen et al., 2019 (ref [24]) | **Delegated-resolvable** | Full citation with DOI (10.1126/science.aax4380). Plausibly contains antibody descriptions. |
| SMNP adjuvant | Silva et al., 2021 (ref [21]) and Pallerla et al., 2025 (ref [13]) | **Delegated-resolvable** | Full citations with DOI for Pallerla. Silva citation lacks DOI in the reference list as provided. |
| DeGlyPHER method | Baboo et al., 2021 (ref [1]) and Baboo et al., 2023 (ref [2]) | **Delegated-resolvable** | Full citations with DOI. |
| GlycoMSQuant | Baboo et al., 2021 (ref [1]) | **Delegated-resolvable** | Full citation with DOI. |
| Leginon automation | Suloway et al., 2005 (ref [25]) | **Delegated-resolvable** | Full citation with DOI. |
| ProLuCID search | Xu et al., 2015 (ref [30]) | **Delegated-resolvable** | Full citation with DOI. |
| CryoSPARC | Punjani et al., 2017 (cited in text as "Pujani, et al., 2017") | **Delegated-resolvable** | Citation is present but the author name is misspelled ("Pujani" vs "Punjani"). The reference list entry appears incomplete in the provided text (no full citation visible). Marked **unverifiable** — needs confirmation. |
| N332-GT series design | Steichen et al., 2019 (ref [24]) | **Delegated-resolvable** | Full citation with DOI. |
| Leap-In transposase system | ATUM proprietary (Section 2.3.2) | **Delegated-dead** | The transposase system is described as "developed by ATUM" with no citation to a peer-reviewed publication or patent. The mechanism is described in the text but the system itself is proprietary and not independently reproducible without access to ATUM materials. This is a **HARD missing** for the cell-line development method since the transposase is central to the stable pool generation. |
| Codon optimization | "ATUM's proprietary algorithm" (Section 2.3.3) | **Delegated-dead** | The algorithm is proprietary and not described. This is a **HARD missing** for reproducibility of the construct design. |
| CHO HCP ELISA | Cygnus Technologies kit (Section 2.2.4) | **Self-contained** | Kit vendor is named; catalog number not given but the kit is commercially available. |
| Mix-N-Go Protein A ELISA | Cygnus Technologies (Section 2.2.9) | **Self-contained** | Kit vendor is named. |
| 2G12 residual ELISA | Section 2.2.7 | **Self-contained** | Described in text. |

**Circular citation check:** No circular citation chains were detected among the delegated methods.

---

## Summary of HARD Missing Items

The following items are HARD missing and would prevent an independent group from reproducing the work:

1. **No statistical test named** anywhere in the manuscript (cross-cutting).
2. **No replicate counts stated** for the Ambr250 optimization (n=1 per condition appears to be the case but is not stated), pilot-scale runs, or GMP runs.
3. **No RRID/CVCL** for the CHO cell line; **no authentication** (STR) and **no mycoplasma testing** statement.
4. **No vendor/catalog/clone/RRID** for PGT145, BG18_GL0, DEN3 antibodies; no catalog for 2G12.
5. **No mass-spec repository accession** (PRIDE/MassIVE) for glycomics data.
6. **No precursor/fragment mass tolerances** for ProLuCID search.
7. **No primer sequences** for the RT-PCR/Sanger verification of transgene mRNA.
8. **No software versions** for CryoSPARC, Leginon, Byos, ProLuCID, GlycoMSQuant, IP2, Census2, DTASelect2.
9. **No hyperparameters** for CryoSPARC 2D classification (beyond box size) or for ProLuCID search (tolerances, enzyme settings).
10. **Leap-In transposase system and codon-optimization algorithm are proprietary** with no independent description or citation — the cell-line development method is not independently reproducible.
11. **No catalog numbers** for the majority of reagents (media, feeds, resins, filters, columns).

## Summary of SOFT Missing Items

1. No data-availability statement.
2. No code availability for custom tools (DeGlyPHER, GlycoMSQuant).
3. No off-target assessment for transposon integration.
4. No compute budget for CryoSPARC processing.
5. No catalog numbers for several commercial kits (CHO HCP ELISA, Protein A ELISA).
6. No CAS numbers for chemicals.

## Questions for the Authors

1. **Error bars:** Are the "±" values in Tables 7–9 and 12 SD or SEM? The figures state SEM; the tables do not specify.
2. **Replicates:** How many independent bioreactor runs per condition in the Ambr250 study? How many replicate injections for SE-HPLC/RP-HPLC? How many replicate mass-spec analyses?
3. **CryoSPARC citation:** The in-text citation reads "Pujani, et al., 2017" — is this Punjani et al.? The reference list entry appears incomplete.
4. **Antibody sources:** Where were PGT145, BG18_GL0, and DEN3 obtained? Are they available from a public repository (e.g., IAVI, NIH AIDS Reagent Program)?
5. **Mass-spec data deposition:** Will the raw mass-spec data be deposited in a public repository (PRIDE/MassIVE)? If so, what is the accession?
6. **Deviations from Dey et al. 2018:** The manuscript states the process was "based on" the BG505 SOSIP.664 process. Which specific steps deviate from that published process, and are those deviations fully described here?
7. **Leap-In system:** Is there a peer-reviewed publication or patent describing the Leap-In transposase system that could be cited in place of the proprietary description?

---

**Auditor note:** This report identifies completeness and traceability gaps only. It does not assess scientific validity, novelty, or significance. The editor should weigh these findings alongside the scientific review.