# Methods Completeness & Reagent Traceability Report

**Manuscript:** *Patch-Clamp Single-Cell Proteomics in Acute Brain Slices: A Framework for Recording, Retrieval, and Interpretation*

**Auditor role:** Methods Completeness & Reagent Traceability Auditor

---

## Categories Checked

The following checklist categories were triggered by the manuscript content and checked:

1. **Cross-cutting items** (applies to all manuscripts)
2. **Model organisms / in vivo** (rats used)
3. **Mass spec (proteomics)** (central technique)
4. **Chemicals/drugs/dosing** (internal solutions, cutting solutions, aCSF)
5. **Computational/ML/modeling** (PCA, SynGO analysis, custom R scripts)
6. **Protocol-provenance rule** (multiple "as previously described" citations)

Not triggered: Antibodies, cell lines, human subjects, oligos/plasmids, genomics/sequencing, microscopy/imaging/flow.

---

## 1. Cross-Cutting Items

| Item | Status | Finding |
|---|---|---|
| Sample size n stated, with what n represents | **Present** | n = 3 for gigaseal-preserved retrievals (Figure 3C); n = 6 for in situ correlation analysis (Fig 5C–D); n = 12 total neurons. However, the manuscript does not explicitly state whether these are biological or technical replicates. Neurons are individual biological samples, but this is not stated explicitly. **SOFT — clarify.** |
| Named statistical test | **Present** | Linear regression (F-statistic, adjusted R², p-values) reported for correlations in Figures 3D–E and 5C–D. SynGO enrichment uses Q-value < 0.05 threshold. PCA described. No explicit statement of the statistical test used for PCA separation (PCA is descriptive, not inferential — acceptable). |
| Error bars / dispersion measure | **Missing** | No error bars, SD, SEM, or CI are reported anywhere in the manuscript. Figures 3C, 3D, 3E, 4A, 5C, 5D show individual data points without dispersion measures. This may be appropriate for n = 3–7, but the manuscript never states what dispersion measure would apply. **HARD — missing** (relevant data exists; a competent lab cannot assess variability). |
| Software/tool versions | **Partial** | DIA-NN v1.8.1 (stated); NeuroExpress version 19.4.09 (stated); R 4.3.1 (stated); pClamp10 (stated, no minor version); Multiclamp 700B amplifier (stated); Digidata 1440A (stated); Orbitrap Astral (stated, no firmware version); Vanquish Neo UHPLC (stated, no version); FAIMS Pro (stated, no version). **HARD — missing** for pClamp minor version and instrument firmware versions. |
| Data-availability statement | **Present** | MassIVE identifier MSV000099156 and ProteomeXchange identifier PXD068359 stated. Zenodo DOI 10.5281/zenodo.18189812 for videos. |
| Code availability | **Present** | GitHub URL provided: https://github.com/LarryThePharmacologist. However, the manuscript does not state which scripts are in the repo or whether they are versioned. **SOFT** |

---

## 2. Model Organisms / In Vivo

| Item | Status | Finding |
|---|---|---|
| Species + strain + source | **Present** | Wistar rats, Charles River (stated in Methods). |
| RRID | **Missing** | No RRID for the rat strain. **SOFT** (RRID is recommended but not universally required for rats). |
| Genotype and background | **Present** | Wild-type Wistar rats; background implied by strain. |
| Sex | **Present** | Male rats (stated: "Wistar rats (75 days of age, Charles River)" — sex not explicitly stated in the Methods; the phrase "male rats" appears only in the title of a cited reference [27]. **HARD — missing** — sex is a required identifier for animal work and is not stated in the Methods. |
| Age | **Present** | 75 days of age. |
| n per group | **Present** | n = 3 (gigaseal-preserved), n = 7 (in-situ correlation), n = 12 total. |
| IACUC protocol # | **Present** | Protocol no. 09-0006, Scripps Research IACUC. |
| Randomization/blinding statement | **Missing** | No statement about randomization or blinding during electrophysiology or analysis. **SOFT** (not always applicable to exploratory patch-clamp studies, but should be stated). |
| Housing | **Missing** | No housing conditions (cage type, light/dark cycle, temperature, humidity) stated. **SOFT** |
| Power justification | **Missing** | No power calculation or justification for n = 12. **SOFT** |

---

## 3. Mass Spectrometry (Proteomics)

| Item | Status | Finding |
|---|---|---|
| Instrument + acquisition mode | **present** | Orbitrap Astral mass spectrometer, DIA mode with FAIMS Pro (CV = −50). |
| Sample prep / digestion | **present** | 0.02% DDM lysis, 7 ng trypsin, 37°C for 2 h, quenched with 0.1% formic acid. |
| Search engine + version | **present** | DIA-NN v1.8.1. |
| Database + version | **present** | UniProt Mus musculus reference proteome (downloaded 2024). Note: the manuscript states "Mus musculus" but the animals are rats (Rattus norvegicus). This is a **discrepancy** — the search database is mouse, not rat. This is a HARD issue for reproducibility: the database must match the species. |
| FDR | **present** | 1% FDR at precursor and protein-group level. |
| Modifications | **present** | Oxidation (variable). |
| Tolerances | **Missing** | Precursor and fragment mass tolerances are not stated. DIA-NN defaults may apply, but they are not specified. **HARD** |
| Repository accession | **present** | MassIVE MSV000099156; ProteomeXchange PXD068359. |
| Quant method | **present** | MaxLFQ (stated). |
| Replicates | **present** | n = 12 neurons (biological replicates); no technical replicates stated. **SOFT** |

**Additional note:** The database species mismatch (mouse vs rat) is a significant reproducibility concern. If the search was run against the mouse proteome, the results may be missing rat-specific isoforms or contain mouse-specific entries. This must be clarified.

---

## 4. Chemicals / Drugs / Dosing

| Item | Status | Finding |
|---|---|---|
| Identity traceable to vendor + catalog # or CAS | **Missing** | All chemicals (sucrose, KCl, CaCl₂, MgCl₂, NaH₂PO₄, NaHCO₃, glucose, HEPES, KGluconate, EGTA, Mg-ATP, Na-GTP, DDM, trypsin, formic acid) are named but **no vendor, catalog number, or CAS number is provided for any of them**. **HARD** |
| Dose/concentration per experiment | **Present** | All concentrations are given in the Methods (e.g., 206 mM sucrose, 145 mM KGluconate, 0.5 mM EGTA, 7 ng trypsin, 0.02% DDM). |
| Route/mode | **Present** | Perfusion (aCSF), internal solution via patch pipette, digestion in well plate. |
| Vehicle + final concentration | **Present** | aCSF and internal solution compositions fully specified. |
| Schedule | **Present** | Incubation times (37°C 30 min, RT 30 min), digestion time (2 h), gradient time (36 min). |

---

## 5. Computational / ML / Modeling

| Item | Status | Finding |
|---|---|---|
| Dataset(s) with version | **present** | MassIVE dataset MSV000099156; DIA-NN output file report.pg_matrix.tsv. |
| Train/val/test split | **N/A** | No ML model training. |
| Architecture/algorithm | **present** | PCA (descriptive), SynGO enrichment, DIA-NN search. |
| Hyperparameters | **present** | DIA-NN parameters stated (FDR 1%, oxidation variable, up to 2 missed cleavages, match-between-runs enabled). |
| Training procedure | **N/A** | No training. |
| Library versions + hardware | **Partial** | R 4.3.1 stated; packages (ComplexHeatmap, ggplot2, UpSetR) named but **no versions** stated. Hardware (Orbitron Astral) stated. **SOFT** |
| Random seeds | **N/A** | No stochastic training. |
| Code availability | **present** | GitHub URL provided. |
| Metric definitions | **present** | FDR, Q-value, adjusted R², p-value. |
| Environment file | **Missing** | No environment file (e.g., conda/renv) for R packages. **SOFT** |

---

## 6. Protocol-Provenance Rule

The manuscript uses "performed as previously described" / "as in [ref]" for several methods. Each must be checked for resolvability.

| Delegated method | Citation | Resolvable? | Classification |
|---|---|---|---|
| Acute brain slice preparation and electrophysiology | "as previously described [10, 26–31]" | Refs 10, 26–31 are full citations with DOIs/PMIDs (e.g., ref 10: Patel et al., 2024, Neurobiol Stress; ref 26: Rodriguez et al., 2022, IJMS). These are published, resolvable papers. | **delegated-resolvable** — but note: the manuscript does not state which specific steps were taken from which reference. The reader must consult 6 different papers to reconstruct the protocol. This is acceptable but should be flagged as a **SOFT** concern for clarity. |
| NeuroExpress analysis | "developed and provided by A. Szücs" | The citation is to a ResearchGate page (ref 15). This is not a peer-reviewed publication and the URL is not given. The reference is "Szücs, A., NeuroExpress program for analyzing patch-clamp data. ResearchGate, 2022." | **delegated-dead** — a ResearchGate page is not a stable, resolvable citation. The manuscript states the version (19.4.09) but the software itself is not formally published. **HARD** — the analysis method is load-bearing (passive membrane properties are central to the capacitance correlation), and the software provenance is not verifiable. |
| SynGO analysis | "SynGO [16]" | Ref 16 is Koopmans et al., Neuron 2019, a published paper with DOI. | **delegated-resolvable** |
| IUPHAR-DB | "IUPHAR-D [17, 18]" | Refs 17–18 are published papers (Br J Pharmacol). | **delegated-resolvable** |
| DIA-NN | "DIA-NN v1.8.1 [33]" | Ref 33 is Demichev et al., Nature Methods 2020. | **delegated-resolvable** |

**Deviations from cited protocols:** The manuscript states "as previously described [10, 26–31]" but does not state any deviations. However, the manuscript adds a novel step — "During withdrawal of the patched neuron, light negative pressure (−50 to −140 mmHg) was applied" — which is not described as a deviation from the cited protocol. This is a **new step** that should be flagged as an addition to the cited protocol. **SOFT** — the step is described in full, so it is reproducible.

---

## Summary of HARD Missing Items

1. **Error bars / dispersion measures** — no SD/SEM/CI reported anywhere.
2. **Sex of animals** — not stated in Methods (only implied by a cited reference title).
3. **Mass tolerance** — not stated for DIA-NN search.
4. **Database species mismatch** — search database is *Mus musculus* but animals are *Rattus norvegicus*.
5. **Chemical vendor/catalog/CAS** — none provided for any reagent.
6. **NeuroExpress software provenance** — cited to a ResearchGate page, not a stable publication.

## Summary of SOFT / Unverifiable Items

- **Unverifiable:** Whether the cited references (10, 26–31) actually contain the full protocol — cannot be confirmed from the manuscript alone.
- **Unverifiable:** Whether the GitHub repository contains the exact scripts used for the figures.
- **SOFT:** No randomization/blinding statement; no housing details; no power justification.
- **SOFT:** R package versions not stated; no environment file.
- **SOFT:** No technical replicates for mass spec.
- **SOFT:** The new negative-pressure step is not flagged as a deviation from cited protocols.

---

## Questions for the Authors

1. **Species discrepancy:** The search database is stated as "UniProt Mus musculus reference proteome" — the animals are rats. Was the search actually run against the mouse proteome, or is this a typo? If mouse, what is the justification?
2. **Sex:** Please confirm the sex of the rats used.
3. **NeuroExpress:** Can you provide a stable DOI or institutional repository link for the software, or confirm the version used?
4. **Mass tolerance:** What precursor and fragment mass tolerances were used in the DIA-NN search?
5. **Reagent vendors:** Can you provide vendor and catalog numbers for the key reagents (e.g., DDM, trypsin, ATP, GTP)?
6. **Error bars:** For the correlations in Figures 3D–E and 5C–D, what dispersion measure would be appropriate, and why is none shown?

---

*This report is factual and enumerative. No score or accept/reject judgment is made.*