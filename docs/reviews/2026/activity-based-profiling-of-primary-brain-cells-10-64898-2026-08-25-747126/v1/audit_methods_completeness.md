# Methods Completeness & Reagent Traceability Audit

## Scope & Triggering Categories

The manuscript describes:
- **Antibodies** (Western blotting, immunoprecipitation)
- **Cell lines** (HEK293T, Neuro2a, SH-SY5Y, HCT116, Ramos)
- **Primary cells** (mouse brain dissociations)
- **Model organisms** (C57BL/6 mice, in vivo electrophysiology)
- **Chemicals/drugs** (stereoprobes, cAMP, inhibitors)
- **Oligos/plasmids/constructs** (Gateway cloning, CRISPR/Cas9, lentiviral vectors, site-directed mutagenesis)
- **Mass spectrometry** (TMT proteomics, LC-MS/MS)
- **Flow cytometry**
- **Electrophysiology** (patch clamp, whole-cell, inside-out, acute slices)

All eight conditional categories are triggered.

---

## ANTIBODIES / IMMUNODETECTION

**Status: HARD — PRESENT with minor gaps**

### Present:
- **Vendor, catalog #, host species, clonality provided for all primary antibodies:**
  - Mouse anti-FLAG M2 (Sigma #F3165, 1:1000)
  - Rabbit anti-GAPDH (CST #2118, 1:1000)
  - Rabbit anti-FLAG (CST #14793, 1:1000)
  - Rabbit anti-Myc (CST #71D10, 1:1000)
  - Rabbit anti-CRMP-2/DPYSL2 (CST #9393, 1:1000)
  - Rat anti-CRMP-5/DPYSL5 (Thermo Fisher #MA3-700, 1:1000)

- **Secondary antibodies** (Li-Cor IRDye, catalog #s, host/target species provided)

- **Application context** (Western blotting, IP) stated for each

- **Dilutions** provided for all antibodies

### Missing:
- **RRID identifiers** for any antibody (none provided; these are increasingly expected for reproducibility)
- **Clone information** for monoclonal antibodies (e.g., anti-FLAG M2 is a clone, but not explicitly labeled as such in the report; CST catalog numbers imply clonality but are not stated)

### Assessment:
Sufficient for reproduction. Vendor + catalog # + dilution is the standard HARD requirement and is met. RRID absence is a SOFT gap (increasingly expected but not yet universal requirement in 2024).

---

## CELL LINES / PRIMARY CELLS

**Status: HARD — PRESENT for lines; PARTIAL for primary cells**

### Cell Lines — Present:
- **Source stated:** ATCC for HEK293T (CRL-3216), Neuro2a (CCL-131), SH-SY5Y (CRL-2266)
- **CVCL identifiers:** Implicit via ATCC catalog numbers (resolvable)
- **Media/supplements:** DMEM + 10% FBS + 2 mM L-glutamine + pen-strep (SOFT, provided)
- **Culture conditions:** 37 °C, 5% CO₂, humidified (SOFT, provided)

### Cell Lines — Missing:
- **STR authentication:** Not stated whether lines were authenticated by STR profiling
- **Mycoplasma testing:** Not stated whether lines were tested for mycoplasma contamination

### Primary Cells (Brainocytes) — Present:
- **Source:** Adult C57BL/6 mice, male, 4–8 weeks old (for Scripps experiments)
- **Dissociation protocol:** Detailed (MACS Octodissociator, enzymatic + mechanical)
- **Viability:** ~90% reported (flow cytometry, Supplementary Dataset S1)
- **Media:** DMEM + pen-strep + glutamine (SOFT, provided)

### Primary Cells — Missing:
- **Mycoplasma testing:** Not stated for primary cell preparations
- **Passage number:** Not stated (relevant for stability across experiments)

### Assessment:
**HARD requirement met for source and basic characterization.** STR and mycoplasma testing are increasingly expected but not universally mandated; their absence is a SOFT gap. Brainocyte viability is well-documented.

---

## MODEL ORGANISMS / IN VIVO

**Status: HARD — MOSTLY PRESENT; SOFT gaps noted**

### Present:
- **Species + strain + source:**
  - C57BL/6 mice (Scripps Research, for proteomics)
  - C57BL/6J mice (Jackson Laboratory, for electrophysiology at Columbia)
  - Age: 4–8 weeks (Scripps); 2–5 months (Columbia)
  - Sex: Male (stated for both)

- **IACUC approval:** Stated for both Scripps and Columbia; protocols approved by respective IACUCs

- **Housing/care:** NIH Guide compliance stated; 12 hr light–dark cycle, ad libitum food/water, pathogen-free conditions (Columbia details provided)

- **Acute brain slice experiments:** 200 µm slices, 6 slices per experiment (n stated)

- **Hippocampal slice electrophysiology:** n per group stated (vehicle: N=8, WX-02-679: N=10, WX-02-678: N=7; Figure 6K)

### Missing:
- **Randomization statement:** Not explicitly stated whether animals were randomly assigned to treatment groups
- **Blinding statement:** Not stated whether experimenters were blinded to treatment during recordings
- **Power justification:** No a priori power calculation provided for electrophysiology experiments
- **Genotype/background:** Assumed WT; not explicitly stated

### Assessment:
**HARD requirements substantially met.** Randomization and blinding are SOFT gaps (increasingly expected for in vivo work but not universally stated in 2024). Sample sizes are provided for key experiments.

---

## CHEMICALS / DRUGS / DOSING

**Status: HARD — PRESENT for stereoprobes; PARTIAL for other compounds**

### Stereoprobes — Present:
- **Identity:** Chemical structures provided (Figure 1B, Figure 5I)
- **Concentrations/doses:** Consistently stated (e.g., 5 µM, 1 h; 20 µM, 2 h)
- **Vehicle:** DMSO (concentration not always stated; see below)
- **Route/mode:** In cellulo (brainocytes), in vitro (lysates), in vivo (brain slices, patch clamp)

### Stereoprobes — Missing:
- **Vendor/catalog # or CAS #:** Stereoprobes (WX-01-06, WX-02-46, WX-03-57, etc.) are proprietary compounds. No CAS numbers or vendor information provided. **Unverifiable** — authors state "All chemical probes and other elaborated electrophilic compounds in this study are available from the Lead Contact with a completed Materials Transfer Agreement" (Resource Availability section). This is acceptable for proprietary compounds but limits immediate reproducibility.
- **Final DMSO concentration:** Often not stated (e.g., "5 µM stereoprobe" but final DMSO % not given)

### Other Compounds — Present:
- **cAMP:** Concentration stated (0.5–100 µM, depending on experiment); source not given but standard reagent
- **Ivabradine, RO-27569:** Concentrations stated; vendor not given (SOFT)
- **BRL-50481, IBMX:** Concentrations stated (200 µM, 100 µM); vendor not given (SOFT)

### Other Compounds — Missing:
- **Vendor/catalog # for cAMP, ivabradine, RO-27569, BRL-50481, IBMX:** Not provided (SOFT gap; these are standard reagents but traceability is incomplete)

### Assessment:
**HARD requirement partially met.** Stereoprobes are proprietary and available via MTA; this is acceptable but limits reproducibility. Standard reagents (cAMP, inhibitors) lack vendor information (SOFT gap).

---

## OLIGOS / PLASMIDS / CONSTRUCTS

**Status: HARD — PRESENT for sequences; PARTIAL for plasmid sources**

### Plasmids — Present:
- **Gateway cloning:** Destination vectors named (pRK5, pLEX307, etc.); Gateway enzymes cited (Thermo Fisher #11791019, #11789013)
- **Lentiviral vectors:** psPAX2, VSV-G envelope vector named; standard reagents
- **CRISPR/Cas9:** LentiCRISPR v2-Blast vector named; sgRNA sequences provided:
  - sgDPYSL5-03: 5′-GACGCTTATGAGAAGTGCCG-3′
  - sgDPYSL5-04: 5′-GCACGCTTGCAAGGACATTG-3′

### Plasmids — Missing:
- **Addgene # or full plasmid description:** pRK5, pLEX307, psPAX2, VSV-G, LentiCRISPR v2-Blast are standard but no Addgene accession numbers provided. **Unverifiable** — these are widely available but not uniquely identified.
- **Plasmid maps or sequences:** Not provided (SOFT; not always required for standard vectors)

### Primers/Oligos — Present:
- **sgRNA sequences** for CRISPR provided (see above)
- **Site-directed mutagenesis:** "Q5 site-directed mutagenesis kit (New England BioLabs #E0554S)" used; primers referenced as "shown below" but **primers are NOT shown in the manuscript** (Methods section states "using the primers shown below" but no primer table appears)

### Primers/Oligos — Missing:
- **Primer sequences for site-directed mutagenesis:** Referenced as "shown below" in Methods but **not provided in the text or supplementary materials** (HARD missing). The manuscript states: "Site-directed mutagenesis was carried out using a Q5 site-directed mutagenesis kit (New England BioLabs #E0554S), using the primers shown below."
- **Cloning primers:** Referenced in 'Cloning and Mutagenesis' section but not provided

### Off-target Assessment:
- **CRISPR off-target analysis:** Not stated (SOFT gap; increasingly expected)

### Assessment:
**HARD gap identified:** Primer sequences for site-directed mutagenesis and cloning are referenced but not provided. This blocks independent reproduction of mutant constructs. Plasmid sources are standard but lack unique identifiers (Addgene #s).

---

## GENOMICS / SEQUENCING / OMICS

**Status: Not triggered** — No genomic sequencing, RNA-seq, or genomic analysis performed by the authors. Brain RNA-seq data are cited from public repositories (BrainRNASeq.org, bioGPS, GTEx) for classification purposes only.

---

## MASS SPECTROMETRY (Proteomics)

**Status: HARD — MOSTLY PRESENT; some parameters unverifiable**

### Instrument & Acquisition — Present:
- **Instrument:** Orbitrap Fusion or Orbitrap Eclipse Tribrid (Thermo Scientific)
- **Ionization:** ESI (implied by standard LC-MS setup)
- **Acquisition mode:** MS3-based TMT method (described in detail)
- **MS1:** Orbitrap analysis, 120,000 resolution, 400–1,700 m/z, AGC 2E5, max injection time 50 ms
- **MS2:** Ion trap, CID, AGC 1.8E4, normalized collision energy 35%, max injection time 120 ms
- **MS3:** Orbitrap, HCD, collision energy 55%, AGC 1.5E5, max injection time 120 ms, resolution 50,000

### Sample Prep — Present:
- **Protein normalization:** 500 µL of 2 mg/mL (1 mg total protein)
- **Click chemistry:** Biotin-PEG4-azide, TBTA, CuSO₄, TCEP (reagents and concentrations provided)
- **Protein precipitation:** Methanol/chloroform/water
- **Digestion:** Trypsin (on-bead overnight, 2 M urea, 1 mM CaCl₂, 10 µg/mL trypsin, 200 mM EPPS pH 8.0)
- **TMT labeling:** TMT10plex or TMT16plex (Thermo Fisher #90406, #A44520)
- **Fractionation:** High-pH reverse-phase (10 fractions for protein-directed; 12 fractions for cysteine-directed)

### Search Engine & Database — Present:
- **Search engine:** ProLuCID (version not stated, but IP2 version 6.0.2 cited)
- **Database:** Human UniProt (release 2016-07) or Mouse UniProt (release 2017-07)
- **Database format:** Reverse concatenated, non-redundant variant
- **Modifications:**
  - Static: Carbamidomethylation (+57.02146 Da on cysteine)
  - Static: TMT tag (+229.1629 Da for 10plex; +304.2071 Da for 16plex) on N-terminus and lysine
  - Dynamic: IA-DTB labeling (+398.25292 Da on cysteine; max 2 per peptide)
- **Peptide criteria:** ≥6 amino acids
- **FDR:** Peptide false-positive rate <1% (via DTASelect 2.0)

### Quantification — Present:
- **Method:** MS3-based reporter ion quantification
- **Reporter ion mass tolerance:** 20 ppm
- **Normalization:** Enrichment ratios calculated as (probe intensity) / (sum of all channel intensities)
- **Protein-level filtering:** Coefficient of variation <0.5, ≥2 distinct peptides, summed intensity >10,000
- **Stereoprobe liganding criteria:** >2.5-fold enantioselective enrichment + >33% competitive blockade (protein-directed); >33% IA-DTB blockade + >2.5-fold vs. enantiomer (cysteine-directed)
- **Replicates:** 4 independent replicates (protein-directed); 6 independent replicates (cysteine-directed)

### Repository & Accession — Present:
- **Repository:** PRIDE (ProteomeXchange Consortium)
- **Accession:** PXD082934 (stated in Data and Code Availability section)
- **Previous dataset:** PXD042541 (referenced for comparison)

### Missing / Unverifiable:
- **ProLuCID version:** Not stated (IP2 version 6.0.2 is stated, but ProLuCID version within IP2 is not specified) — **Unverifiable**
- **RAW Converter version:** Stated as 1.1.0.22 (2004 release) — **Present**
- **DTASelect version:** Stated as 2.0 — **Present**
- **Charge-state dependent isolation windows:** Stated (z=2: 1.2; z=3–6: 0.7) — **Present**
- **Cysteine-directed ABPP filtering criteria:** Variability threshold (20%), IA-DTB blockade (>33.3%), enantioselective ratio (>2.5-fold), replicates (≥4) — **Present**
- **Protein-directed ABPP filtering criteria:** Variability threshold (20%), blockade (>33.3%), enantioselective ratio (>2.5-fold), replicates (≥2) — **Present**

### Assessment:
**HARD requirements substantially met.** Instrument, acquisition parameters, sample prep, search engine, database, modifications, FDR, quantification method, and repository accession are all provided. ProLuCID version within IP2 is unverifiable from the manuscript alone (would require checking IP2 documentation). Replicates and filtering criteria are clearly stated.

---

## FLOW CYTOMETRY

**Status: HARD — PRESENT**

### Present:
- **Instrument:** NovoCyte Quanteon Agilent analyzer
- **Stain:** LIVE/DEAD Fixable Violet Dead Cell Stain Kit (Thermo Fisher #L34964)
- **Staining protocol:** 1 million cells/mL, 30 min at room temperature, protected from light
- **Fixation:** 2% paraformaldehyde in DPBS, 15 min at 4 °C
- **Data acquisition:** Stated (no gating strategy details provided, but viability reported as ~90%)

### Missing:
- **Full gating strategy:** Not provided (HARD gap for reproducibility)
- **Fluorophore/detector assignment:** Not stated (implied violet laser for LIVE/DEAD, but not explicit)
- **Analysis software:** Not named (SOFT gap)

### Assessment:
**HARD gap:** Full gating strategy is not provided. Viability is reported as a summary statistic (~90%) but the gating logic is not described. This limits reproducibility of the cell preparation quality control.

---

## ELECTROPHYSIOLOGY (Patch Clamp)

**Status: HARD — MOSTLY PRESENT; some parameters unverifiable**

### Whole-Cell Patch Clamp (HEK293T) — Present:
- **Amplifier:** ePatch (Elements) or Axopatch 200b (Molecular Devices)
- **Digitizer:** Axon Digidata 1550B (Molecular Devices) where applicable
- **Sampling rate:** 5 kHz
- **Low-pass filter:** 2.5 kHz
- **Pipette resistance:** 3–6 MΩ
- **Holding potential:** -20 mV (1 s)
- **Voltage steps:** -30 to -120 mV (-10 mV increments, 3.5 s); extended to -140 mV for HCN4 (5 s)
- **Tail current recording:** -40 mV (3.5 s)
- **Seal criterion:** ≥1 GΩ
- **Series resistance compensation:** Not applied (stated)
- **Leak correction:** Not applied (stated)
- **Boltzmann fitting:** y = 1/[1+exp((V-V₁/₂)/k)]
- **Data analysis software:** Clampfit 10.7, Origin 2016
- **Statistical test:** Student's t-test (unpaired) or One-way ANOVA with Fisher's test
- **Significance level:** p = 0.05
- **Replicates:** ≥2 independent experiments, ≥4 cells per condition per experiment
- **Data presentation:** Mean ± SEM

### Whole-Cell Patch Clamp (Hippocampal Slices) — Present:
- **Amplifier:** Multiclamp 700B (Molecular Devices)
- **Digitizer:** Digidata 1322A (Molecular Devices)
- **Sampling rate:** 10 or 50 kHz (low-pass filtered at 10 kHz)
- **Pipette resistance:** 4–6 MΩ
- **Holding potential:** -70 mV (bias current injection)
- **Current steps:** 0 to +400 pA (25 pA increments, 1 sec)
- **Hyperpolarizing steps:** Adjusted to reach -105/-110 mV per cell
- **Series resistance criterion:** ≤15 MΩ, change ≤20% during experiment
- **Temperature:** Room temperature (HEK293T); 33–34 °C (slices)
- **Recordings kept:** Only if series resistance ≤15 MΩ and stable
- **Data analysis:** Clampfit, MATLAB, Origin
- **Statistical test:** One-way ANOVA with Fisher's test
- **Significance level:** p = 0.05
- **Replicates:** Vehicle: N=8, WX-02-679: N=10, WX-02-678: N=7 (Figure 6K)

### Inside-Out Patch Clamp (HEK293T, HCN4) — Present:
- **Amplifier:** ePatch (Elements)
- **Acquisition software:** PULSE (E-Zpatch, Elements)
- **Pipette resistance:** ~1 MΩ
- **Holding potential:** -20 mV
- **Voltage steps:** -60 to -175 mV (-15 mV increments, 5 s)
- **Tail current:** -120 mV (1 s)
- **Return to holding:** 6 s at -20 mV
- **cAMP application:** 100 µM in bath solution
- **WX-02-679 application:** 20 µM in bath solution
- **Recording timing:** ~2 min after each application
- **Data analysis:** Clampfit 10.4, Origin 2016

### Missing / Unverifiable:
- **Intracellular solution composition:** Provided for HCN1 (10 mM NaCl, 130 mM KCl, 1 mM EGTA, 0.5 mM MgCl₂, 2 mM ATP, 5 mM HEPES–KOH pH 7.2) and hippocampal slices (125 mM K-gluconate, 10 mM phosphocreatine, 1.5 mM NaCl, 3 mM KCl, 10 mM HEPES, 0.1 mM EGTA, 5 mM ATP, 0.4 mM Na₃-GTP, pH 7.25) — **Present**
- **Extracellular solution composition:** Provided for HCN1 (110 mM NaCl, 30 mM KCl, 1.8 mM CaCl₂, 0.5 mM MgCl₂, 5 mM HEPES–KOH pH 7.4) and hippocampal slices (ACSF: 22.5 mM glucose, 125 mM NaCl, 1 mM MgCl₂, 2 mM CaCl₂, 25 mM NaHCO₃, 2.5 mM KCl, 1.25 mM NaH₂PO₄, 3 mM Na-pyruvate, 1 mM ascorbic acid, pH 7.2) — **Present**
- **Slice incubation conditions:** 33–34 °C, oxygenated ACSF, 5–6 min pre-incubation with compounds — **Present**
- **Blinding during recordings:** Not stated (SOFT gap)
- **Randomization of cell selection:** Not stated (SOFT gap)

### Assessment:
**HARD requirements substantially met.** Detailed protocols for all three patch-clamp configurations (whole-cell HEK293T, whole-cell slices, inside-out) are provided with instrument models, parameters, solutions, and analysis methods. Blinding and randomization are SOFT gaps.

---

## STATISTICAL ANALYSIS & SAMPLE SIZE

**Status: HARD — MOSTLY PRESENT; some gaps**

### Present:
- **Sample sizes (n):**
  - Protein-directed ABPP: 4 independent replicates (2 experiments × 2 replicates each)
  - Cysteine-directed ABPP: 6 independent replicates (3 experiments × 2 replicates each)
  - Gel-ABPP: "representative of at least two independent experiments" (stated for many figures)
  - Hippocampal slice electrophysiology: N=8 (vehicle), N=10 (WX-02-679), N=7 (WX-02-678)
  - HEK293T patch clamp: "≥2 independent experiments, ≥4 cells per condition per experiment"

- **Error bars:** Stated as ± SD (proteomics figures) or ± SEM (electrophysiology figures)

- **Statistical tests:** Student's t-test (unpaired), One-way ANOVA with Fisher's test, paired sample t-tests (IP-MS)

- **Significance level:** p = 0.05

### Missing / Unverifiable:
- **Gel-ABPP replicates:** Many figures state "representative of at least two independent experiments" but do not provide quantification or n for all replicates. **Unverifiable** — unclear whether "representative" means 1 of 2 or averaged across 2+.
- **IP-MS replicates:** "Six independent experiments" stated for Figure 3I but unclear whether this is 6 biological replicates or 6 technical replicates.
- **Proteomics filtering variability:** Stated as "coefficient of variation <0.5" but the basis for this threshold is not justified (SOFT gap).

### Assessment:
**HARD requirements mostly met.** Sample sizes are provided for key experiments. Error bar definitions (SD vs. SEM) are stated. Statistical tests are named. Some gel-ABPP figures lack explicit n values (marked as "representative"), which is a SOFT gap for those specific figures.

---

## DATA & CODE AVAILABILITY

**Status: HARD — PRESENT for data; SOFT for code**

### Data Availability — Present:
- **Mass spectrometry proteomics:** PRIDE repository, accession PXD082934
- **Supplementary datasets:** Dataset S1 (flow cytometry, electrophysiology) and Dataset S2 (proteomics, CNS-enriched proteins) referenced
- **Previous dataset:** PXD042541 (cited for comparison)

### Code Availability — Missing:
- **Custom analysis code:** No statement regarding availability of R scripts, MATLAB scripts, or analysis pipelines (SOFT gap; increasingly expected for computational work)
- **Proteomics analysis:** IP2 pipeline and ProLuCID are cited but custom filtering/analysis code not provided

### Materials Availability — Present:
- **Stereoprobes:** "Available from the Lead Contact with a completed Materials Transfer Agreement"
- **Cell lines:** ATCC sources provided

### Assessment:
**HARD requirement met for data.** SOFT gap for code availability (increasingly expected but not universally mandated).

---

## PROTOCOL PROVENANCE & DELEGATION

**Status: MIXED — Multiple delegated protocols; most resolvable, some unverifiable**

### Delegated Protocols Identified:

1. **Brain dissociation (MACS Octodissociator):**
   - Stated: "using the gentleMACS Octodissociator and Miltenyi Biotec adult brain dissociation kit (Miltenyi #130-107-677)"
   - **Status: Resolvable** — Kit number provided; protocol is vendor-supplied and reproducible.

2. **Protein-directed ABPP:**
   - Stated: "Protein-directed ABPP was carried out as previously reported¹³ with slight modifications."
   - **Reference 13:** Njomen et al. (2024), Nat Chem, DOI 10.1038/s41557-024-01601-1
   - **Status: Resolvable** — Published reference with DOI; modifications are stated ("with slight modifications") and detailed in the manuscript (click chemistry, TMT labeling, fractionation).

3. **Cysteine-directed ABPP:**
   - Stated: "Cysteine-directed ABPP was carried out as previously reported¹³ with slight modifications."
   - **Reference 13:** Same as above
   - **Status: Resolvable** — Published reference; modifications detailed (IA-DTB probe, TMT labeling, fractionation).

4. **Gel-ABPP (click chemistry):**
   - Stated: "Stereoprobe-reactive proteins were visualized by copper-catalyzed azide-alkyne cycloaddition (CuAAC or click¹²³,¹²⁴)"
   - **References 123–124:** Rostovtsev et al. (2002), Angew. Chem. Int. Ed., DOI 10.1002/1521-3773(20020715)41:14<2596::AID-ANIE2596>3.0.CO;2-4; Tornøe et al. (2002), J. Org. Chem., DOI 10.1021/jo011148j
   - **Status: Resolvable** — Foundational click chemistry references; standard protocol.

5. **Whole-cell patch clamp (HEK293T):**
   - Stated: "Whole cell patch clamp experiments were performed as previously described.⁷⁵,⁸⁸,⁹²"
   - **References 75, 88, 92:** Castelli et al. (2026, preprint), Loya-Lopez et al. (in press), Merseburg et al. (2022)
   - **Status: Unverifiable** — Reference 75 is a preprint (bioRxiv); Reference 88 is "in press" (not yet published); Reference 92 is published (Merseburg et al., eLife, DOI 10.7554/eLife.70826). The manuscript provides detailed protocols in the Methods section, so delegation is not load-bearing.

6. **Hippocampal slice electrophysiology:**
   - Stated: "Hippocampal slices were obtained from C57BL/6J mice aged 2-5 months as previously described.⁷⁶"
   - **Reference 76:** Castelli et al. (2026, preprint)
   - **Status: Unverifiable** — Preprint reference; however, detailed protocols are provided in the manuscript (slice preparation, solutions, recording parameters).

7. **Inside-out patch clamp:**
   - Stated: "Whole-cell configuration was first established, after which the pipette was rapidly withdrawn to excise the membrane patch and obtain the inside-out configuration.¹³³"
   - **Reference 133:** Not provided in the reference list (appears to be missing)
   - **Status: Missing reference** — The citation number 133 is not resolved in the reference list. However, the inside-out protocol is standard and briefly described in the manuscript.

8. **CNS-enriched protein classification:**
   - Stated: "Human bioGPS⁴⁰, mouse bioGPS⁴⁰, and GTEx⁴¹ (human RNAseq) data were analyzed and aggregated to classify proteins for tissue-enrichment."
   - **References 40–41:** Wu et al. (2013), Nucleic Acids Res; GTEx Consortium (2013), Nat Genet
   - **Status: Resolvable** — Published references; methodology detailed in Methods.

9. **Brain cell type enrichment (RNA-seq):**
   - Stated: "Brain RNA-Seq data (Mus musculus) from BrainRNASeq.org were analyzed to classify proteins for brain cell type enrichment.¹²⁶"
   - **Reference 126:** Zhang et al. (2014), J. Neurosci., DOI 10.1523/JNEUROSCI.1860-14.2014
   - **Status: Resolvable** — Published reference; data source (BrainRNASeq.org) provided.

10. **Panther Classification System:**
    - Stated: "Panther Classification System (ver. PANTHER 18.0) and KEGG BRITE databases were used to analyze protein functional classes as described previously.¹³,¹²⁹,¹³⁰"
    - **References 13, 129–130:** Njomen et al. (2024); Thomas et al. (2022), Protein Sci; Ashburner et al. (2000), Nat Genet
    - **Status: Resolvable** — Published references; tool version (18.0) provided.

### Assessment:
**Most delegated protocols are resolvable to published references or vendor protocols.** Key load-bearing methods (protein-directed ABPP, cysteine-directed ABPP, gel-ABPP, patch clamp) are either detailed in the manuscript or delegated to published references with DOIs. Two unverifiable issues:
- **Reference 133 (inside-out patch clamp):** Citation number not resolved in reference list (HARD missing).
- **References 75, 88 (patch clamp):** Preprint/in-press status limits verifiability (SOFT gap).

---

## SUMMARY TABLE

| Category | Status | Severity | Key Findings |
|----------|--------|----------|--------------|
| **Antibodies** | Present | SOFT | RRID identifiers missing; otherwise complete (vendor, catalog #, dilution, host/clonality). |
| **Cell Lines** | Present | SOFT | STR authentication and mycoplasma testing not stated. Source and media provided. |
| **Primary Cells** | Present | SOFT | Viability documented (~90%); mycoplasma testing and passage number not stated. |
| **Model Organisms** | Present | SOFT | IACUC approval, age, sex, strain provided. Randomization and blinding not stated. Power justification absent. |
| **Chemicals/Drugs** | Partial | HARD | Stereoprobes proprietary (MTA required); standard reagents lack vendor info. Final DMSO concentrations sometimes missing. |
| **Oligos/Plasmids** | Missing | HARD | **Primer sequences for site-directed mutagenesis referenced but not provided.** Plasmid sources lack Addgene #s. |
| **Mass Spectrometry** | Present | SOFT | Instrument, acquisition, sample prep, search engine, database, modifications, FDR, quantification, repository all provided. ProLuCID version within IP2 unverifiable. |
| **Flow Cytometry** | Partial | HARD | **Full gating strategy not provided.** Viability reported as summary statistic. |
| **Electrophysiology** | Present | SOFT | Detailed protocols for all three configurations (whole-cell HEK293T, whole-cell slices, inside-out). Blinding and randomization not stated. |
| **Statistics** | Present | SOFT | Sample sizes, error bars, tests, significance level provided. Some gel-ABPP figures marked "representative" without explicit n. |
| **Data Availability** | Present | SOFT | PRIDE accession provided. Code availability not stated. |
| **Protocol Provenance** | Mostly Resolvable | SOFT/HARD | Most delegated protocols resolvable to published references. **Reference 133 (inside-out patch clamp) not resolved in reference list.** References 75, 88 are preprint/in-press (unverifiable). |

---

## CRITICAL GAPS (HARD)

1. **Primer sequences for site-directed mutagenesis and cloning:** Referenced as "shown below" but not provided in the manuscript. This blocks independent reproduction of mutant constructs (PLP1_C6A, PLP1_C7A, PDE7B_C136A, DPYSL2_C504A, HCN1_C542A, HCN2_C611A, HCN4_C662A, and others).

2. **Flow cytometry gating strategy:** Full gating logic not provided. Viability is reported as ~90% but the gates used to define live/dead populations are not described.

3. **Reference 133 (inside-out patch clamp):** Citation number appears in text but is not resolved in the reference list.

---

## SOFT GAPS (RECOMMENDED BUT NOT BLOCKING)

- RRID identifiers for antibodies
- STR authentication and mycoplasma testing for cell lines
- Randomization and blinding statements for animal experiments
- Power justification for electrophysiology sample sizes
- Vendor information for standard reagents (cAMP, ivabradine, etc.)
- Addgene accession numbers for plasmids
- ProLuCID version specification
- Code availability statement
- Full gating strategy for flow cytometry (beyond viability reporting)

---

## UNVERIFIABLE ITEMS (REQUIRE AUTHOR CLARIFICATION)

- **ProLuCID version within IP2 6.0.2:** Not explicitly stated; would require checking IP2 documentation or author confirmation.
- **References 75, 88 (patch clamp protocols):** Preprint and in-press status; content not independently verifiable from published sources.
- **Stereoprobe vendor/catalog #:** Proprietary compounds; available via MTA only (acceptable but limits immediate reproducibility).