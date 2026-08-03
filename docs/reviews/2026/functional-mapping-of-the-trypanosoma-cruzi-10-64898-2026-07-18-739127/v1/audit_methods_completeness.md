# Methods Completeness & Reagent Traceability Auditor

## Summary
The manuscript describes an activity-based chemoproteomic profiling of Trypanosoma cruzi serine hydrolases using fluorophosphonate probes and mass spectrometry, supported by in silico genome analysis. Major reproducibility gaps include: (1) incomplete reporting of mass spectrometry parameters (instrument, acquisition mode, search engine, FDR, database version); (2) missing cell line authentication, source, and mycoplasma testing; (3) unspecified probe concentrations, vehicles, and incubation schedules; (4) absent software versions for key tools (limma, AlphaFold, R); (5) no description of error bars in figures; (6) insufficient detail on sample preparation for proteomics (lysis, click chemistry, enrichment, digestion). Code and raw data are deposited (Zenodo, PRIDE), which is a strength.

## Categories checked
- Cross-cutting
- Cell lines/primary cells
- Chemicals/drugs/dosing
- Mass spec (proteomics/metabolomics)
- Computational/ML/modeling

**HARD gaps (blocking): 16** · SOFT gaps: 3 · unverifiable: 0

## HARD gaps — reproduction blockers
- **[Cross-cutting] Named statistical test and what error bars represent (SD/SEM/CI)** — Statistical test: "empirical Bayes moderated t-tests implemented in the limma package" is stated. However, no figure legends or methods text describe what error bars represent (SD, SEM, CI) — figures 3 and 5 show no error bars or their meaning is not defined.
- **[Cross-cutting] Software, tool, and instrument versions** — Versions not provided for: limma package, AlphaFold Protein Structure Database, Pfam/InterPro/CDD/Panther/MEROPS, R, LC-MS/MS instrument. Only STRING database versions (v12.0, v11.5) are given.
- **[Cell lines/primary cells] Source** — Manuscript refers to "T. cruzi cultures" and "live parasites" but does not state the source (e.g., repository, lab stock, passage history).
- **[Cell lines/primary cells] RRID/CVCL** — No RRID or CVCL identifier provided for the Dm28c strain.
- **[Cell lines/primary cells] Authentication (STR)** — No mention of STR profiling or other authentication.
- **[Cell lines/primary cells] Mycoplasma testing** — No mention of mycoplasma testing.
- **[Chemicals/drugs/dosing] Dose/concentration per experiment** — No concentration of FP-alkyne probes used for whole-cell labelling is reported.
- **[Chemicals/drugs/dosing] Vehicle+final concentration** — Vehicle (likely DMSO) and final probe concentration not stated.
- **[Chemicals/drugs/dosing] Schedule** — Incubation time and temperature not reported.
- **[Mass spec (proteomics/metabolomics)] Instrument + acquisition mode** — Only "MS analysis" by a facility is mentioned; no instrument model, acquisition mode (DDA/DIA), or LC-MS parameters.
- **[Mass spec (proteomics/metabolomics)] Sample prep/digestion/enrichment** — Briefly described as "cell lysis, click chemistry with biotin-N3, streptavidin enrichment, reduction, alkylation, digestion, and LC-MS/MS analysis" but critical details (lysis buffer, click chemistry conditions, enrichment protocol, digestion enzyme, LC gradient) are absent.
- **[Mass spec (proteomics/metabolomics)] Search engine + version** — Not specified (e.g., MaxQuant, Proteome Discoverer, Mascot).
- **[Mass spec (proteomics/metabolomics)] Database + version** — Genome assemblies (Dm28c 2018, 2014, 2017) are cited for annotation, but the protein sequence database used for MS/MS searching is not explicitly defined or versioned.
- **[Mass spec (proteomics/metabolomics)] FDR + modifications + tolerances** — No FDR threshold, fixed/variable modifications, or mass tolerances reported.
- **[Computational/ML/modeling] Library versions + hardware** — No versions for R, limma, AlphaFold, or other packages; no hardware specification.
- **[Computational/ML/modeling] Random seeds** — No random seed reported for any stochastic step.

## SOFT gaps — recommended
- **[Cell lines/primary cells] Media/supplements** — Culture medium composition not described.
- **[Computational/ML/modeling] Compute budget** — Not reported.
- **[Computational/ML/modeling] Environment file** — No conda/requirements.txt or Dockerfile provided.

## Documented (for the record)
- **[Cross-cutting] Sample size n stated with what n represents (biological vs technical replicates)** — "Three biological replicates were analysed per condition." (Methods, under Figure 2 description area).
- **[Cross-cutting] Data-availability statement** — "The data that support the findings of this study are available in the supplementary material of this article. The mass spectrometry proteomics data have been deposited to the ProteomeXchange Consortium via the PRIDE partner repository with the dataset identifier PXD080813." (Data Availability Statement).
- **[Cross-cutting] Code availability when custom analysis was done** — "The R scripts used in this study are available without restrictions via Zenodo: https://doi.org/10.5281/zenodo.20626073" (Code Availability Statement).
- **[Chemicals/drugs/dosing] Identity traceable to vendor+catalog # or CAS/structure** — FP-alkyne probe structures shown in Figure 2; probes are synthesized in-house and referenced to prior publications (refs 17, 29).
- **[Chemicals/drugs/dosing] Route/mode** — "live parasites were incubated with FP-alkyne probes" — whole-cell incubation.
- **[Mass spec (proteomics/metabolomics)] Repository accession** — PRIDE accession PXD080813 provided.
- **[Mass spec (proteomics/metabolomics)] Quant method** — "label-free quantitative proteomics (LFQ-MS)" stated.
- **[Mass spec (proteomics/metabolomics)] Replicates** — "Three biological replicates were analysed per condition.".
- **[Computational/ML/modeling] Dataset(s) with version + exact train/val/test split** — Genome assemblies used: Dm28c 2018 (Berná et al. 2018), 2014 (Grisard et al. 2014), 2017 (implied). Train/val/test split not applicable (no ML training).
- **[Computational/ML/modeling] Architecture/algorithm** — In silico workflow described: clustering, catalytic triad assessment via AlphaFold, differential abundance via limma, GO/PPI via STRING.
- **[Computational/ML/modeling] Hyperparameters** — Catalytic geometry thresholds: Ser–His distance ≤5 Å, His–Asp/Glu ≤5 Å, average pLDDT ≥80 (borderline 60–79). Differential abundance: log2FC >1, p<0.05. GO: Fisher’s exact test, BH-FDR.
- **[Computational/ML/modeling] Training procedure** — Not applicable (no model training).
- **[Computational/ML/modeling] Code availability** — R scripts deposited at Zenodo (doi:10.5281/zenodo.20626073).
- **[Computational/ML/modeling] Ablations** — Not applicable (no ablation study).
- **[Computational/ML/modeling] Metric definitions** — GO enrichment: one-sided Fisher’s exact test, BH-FDR. PPI: PPI enrichment p-value <1e-16.