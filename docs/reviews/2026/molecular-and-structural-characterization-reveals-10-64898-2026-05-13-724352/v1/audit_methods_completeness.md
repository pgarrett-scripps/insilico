# Methods Completeness & Reagent Traceability Auditor

## Summary
The manuscript is a wet-lab molecular/structural characterization study (EV isolation, WB, IP/ELISA, vesicle flow cytometry, TEM/cryo-EM, proteomics, STED, organoid co-culture). Detected checklist categories: cross-cutting reporting, antibodies/immunodetection, cell lines (hiPSC), chemicals/drugs, mass spectrometry, microscopy/imaging/flow, computational/ML (Cellpose image segmentation), and protocol provenance. Overall the methods are unusually detailed and most reagent identifiers, instrument versions, and repository accessions are present. The main gaps are: (1) IHC antibodies (AT8, MAP2, Abeta XP in section 2.16) lack vendor/catalog/clone/RRID entirely; (2) RRIDs are absent for nearly all antibodies and the hiPSC lines; (3) several load-bearing methods are delegated to citations (Labra et al. 2026 for organoid differentiation and WB; Turner/Wiśniewski for FASP; Sandau/Tekkatte for vFC) whose contents cannot be verified from the manuscript alone and are therefore flagged unverifiable; (4) the Cellpose segmentation step lacks version/seed/model details. No delegated-dead references were found; all citations are full and plausibly resolvable. No score or accept/reject judgment is rendered.

## Categories checked
- Cross-cutting (n, statistics, software, availability)
- Antibodies / immunodetection
- Cell lines / primary cells
- Chemicals / drugs / dosing
- Mass spectrometry (proteomics)
- Microscopy / imaging / flow
- Computational / ML (image segmentation)
- Protocol provenance

**HARD gaps (blocking): 1** · SOFT gaps: 3 · unverifiable: 4

## HARD gaps — reproduction blockers
- **[Antibodies / immunodetection] IHC primary antibody vendor/catalog/clone/RRID** — Methods 2.16 lists Abeta XP (1:500, Rb), AT8 (1:500, Mu), MAP2 (1:1000, Ch) with dilutions and host but NO vendor, catalog number, clone, or RRID for any of the three IHC antibodies. A lab cannot obtain the same reagents.

## Unverifiable (raise as questions)
- **[Protocol provenance] Organoid differentiation protocol delegation** — Methods 2.1: 'performed in accordance with a previously established protocol (Labra et al. 2026)'. The reference is a full citation (Advanced Science e14783) and plausibly contains the protocol, but its contents cannot be confirmed from the manuscript alone. The method is largely self-contained in 2.1, so this is not blocking.
- **[Protocol provenance] Western blot protocol delegation** — Methods 2.3: 'SDS-PAGE and western blot analysis was performed according to previously established protocols (Labra et al. 2026)'. Resolvable full citation; contents not verifiable from manuscript alone.
- **[Protocol provenance] FASP proteomics protocol delegation** — Methods 2.10: 'as previously described (Turner et al. 2022; Wiśniewski et al. 2009)' — both are full, resolvable citations; the method is also described in detail in 2.10, so largely self-contained.
- **[Protocol provenance] vFC protocol delegation** — Methods 2.5: 'single vesicle flow cytometry (Sandau et al. 2020; Tekkatte et al. 2023)' — resolvable citations; method also described in 2.5 with kit identifiers.

## SOFT gaps — recommended
- **[Antibodies / immunodetection] Antibody RRID / clone** — No RRIDs are given for any antibody; clone is only implied for FLOT1 (JB19-45) and AT8 (named clone, no catalog). Catalogs are present, so traceability exists, but RRIDs are absent.
- **[Cell lines / primary cells] Cell line RRID/CVCL** — No RRID/CVCL identifier is given for the hiPSC lines; source and originating publication are provided, so the lines are traceable, but the identifier is absent.
- **[Computational / ML (image segmentation)] Cellpose model version, hyperparameters, seed** — Methods 2.17: 'Nuclei were segmented using the Cellpose Segmenter with the nucleus model' — no Cellpose version, model weights, or random seed given. This is a minor image-analysis step, not a load-bearing claim.

## Documented (for the record)
- **[Cross-cutting] Sample size n with what n represents (biological vs technical)** — Methods 2.18 states 'data shown is the average of n number of technical replicates (as noted in figure legend)'; Figure 7D gives n=27 (WT+AD) and n=49 (WT+WT) images; cryo-TEM reports 24 WT and 65 AD EVs; proteomics run in technical triplicate. Note: explicit n is not stated for the vFC and ThT experiments.
- **[Cross-cutting] Named statistical test and error-bar meaning (SD/SEM/CI)** — Methods 2.18: two-way ANOVA with default parameters, significance thresholds; Figure 7 legend uses student's t test; error bars described as standard error of the mean.
- **[Cross-cutting] Software/tool/instrument versions** — Versions given throughout: cryoSPARC v4.7, EPU v3.9, DIA-NN v2.2.0, MSstats v4.16.1, MSstatsConvert v1.19.3, mixOmics v6.32.0, VennDiagram v1.7.3, diann v1.0.1, EnrichR, Fiji v154p, Arivis Pro v4.20, ZEN Blue v3.13, ImageStudio v5.2, GraphPad Prism v10.
- **[Cross-cutting] Data-availability statement** — Data Availability section: MS proteomics deposited to ProteomeXchange/PRIDE (PXD076102); other data available upon reasonable request.
- **[Cross-cutting] Code availability for custom analysis** — Data Availability: analysis code at https://github.com/NataliePTurner/Cerebrocortical-EV-analysis---WT-vs-AD (proteomics pipeline). Note: the custom python violin-plot scripts (Methods 2.9) are not deposited.
- **[Antibodies / immunodetection] WB primary antibody vendor + catalog + host + dilution** — Methods 2.3: Calnexin (Rb, 1:1000, ab133615); FLOT1 (Rb, 1:1000, JB19-45); CD9 (Rb, 1:500, ab263019); Abeta XP (Rb, 1:1000, 8243S); secondaries IRDye 680LT (926-68021) and 800CW (926-32210) with dilutions.
- **[Antibodies / immunodetection] IP capture antibody catalog numbers** — Methods 2.4: CD63 (ab134045), CD81 (ab79559), CD9 (ab263019), 5 µg each, immobilized on Protein G Dynabeads (10004D).
- **[Antibodies / immunodetection] ELISA kit identifiers** — Methods 2.4: Invitrogen Human Total Tau ELISA (KHB0041) and Human Amyloid beta 42 ELISA (KHB3441).
- **[Antibodies / immunodetection] Flow cytometry antibody panel (vFC)** — Methods 2.5: vFC Assay kit CBS-4, vFRed membrane stain, vTag TS-APC mix (CBS-5) targeting CD9/CD63/CD81; calibrated with Lipo100 (CBS-1) and nanoCal (CBS-7).
- **[Cell lines / primary cells] hiPSC source** — Methods 2.1: isogenic WT and PSEN1 M146V/WT lines from a male donor, obtained from the Tessier-Lavigne laboratory and New York Stem Cell Foundation (Paquet et al. 2016).
- **[Cell lines / primary cells] Authentication (STR) and mycoplasma testing** — Methods 2.1: 'Pluripotency and euploidy were confirmed by immunolabeling and G-banding'; cultures 'regularly karyotyped and tested for mycoplasma'. Note: authentication is by immunolabeling + G-banding, not STR.
- **[Cell lines / primary cells] Media/supplements** — Methods 2.1: mTeSR Plus + CEPT, Essential 6/hESC, Neural Media (Neurobasal-A, B-27 minus vitamin A, 1% GlutaMAX), EGF2/FGF2, BDNF/NT-3, Accutase, Aggrewell plates.
- **[Chemicals / drugs / dosing] Amyloid dyes identity + concentration** — Methods 2.13: ThT (EW-88226-62) at 10 µM; Methods 2.14: AmyTracker 680 (A680-A-100) at 10 µg/mL; Methods 2.15: Aco-650 (Acoerela) at 2 µM; Hoechst 1:4000 (62249); CellTracker Green (C2925) 1 µM.
- **[Mass spectrometry (proteomics)] Instrument + acquisition mode** — Methods 2.11: timsTOF Pro2 (Bruker) with Evosep nano-LC, DIA-PASEF mode, 15 spd (~88 min), 220 nL/min, 500 ng peptides, technical triplicate.
- **[Mass spectrometry (proteomics)] Search engine + version, database + version, FDR + modifications** — Methods 2.12: DIA-NN v2.2.0 against Homo sapiens library of 20,405 reviewed sequences (Uniprot, 22 Oct 2024), 1% FDR, trypsin, carbamidomethylation on C, up to 3 variable mods, 1 missed cleavage; MSstats v4.16.1 settings listed.
- **[Mass spectrometry (proteomics)] Repository accession (PRIDE/MassIVE)** — Data Availability: PXD076102 deposited to ProteomeXchange via PRIDE.
- **[Microscopy / imaging / flow] Instrument models + objective/NA/detector/settings** — Methods 2.6-2.8, 2.14-2.16: Talos L120C TEM (120 kV, CETA 16M), Talos Arctica cryo-EM (200 keV, Falcon 4i, 1.2 Å/px, 50 e-/Å2, defocus -1 to -3 µm), Abberior STED (Olympus 60x NA 1.42, 561 nm excitation, 775 nm depletion), Zeiss Celldiscoverer 7 (20x/0.7 NA), Cytek Aurora flow cytometer.
- **[Microscopy / imaging / flow] Analysis/gating software + version + gating strategy** — Methods 2.5: vFC gating of membrane-positive events, size and ABC estimation in FCS Express, with dilution series and positive/negative controls per MISEV/MIFlowCyt-EV (Supplementary Figure 3). Analysis in Fiji, Arivis Pro v4.20, ZEN Blue v3.13.