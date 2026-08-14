# Methods Completeness & Reagent Traceability Auditor

## Summary
This manuscript is a proximity-labeling (TurboID) proteomics study of Smoothened signaling, with follow-up cell biology in NIH3T3 cells and primary cerebellar granule neuron precursors (GNPs). Detected checklist categories: Antibodies/immunodetection, Cell lines/primary cells, Model organisms (mice used to harvest GNPs), Chemicals/drugs/dosing, Oligos/plasmids/constructs (CRISPR, shRNA, cloning), Mass spectrometry, Microscopy/imaging, Computational/ML (R-based proteomics analysis), plus cross-cutting items (sample size, statistics, software versions, data/code availability) and protocol provenance. The strongest gaps are: no mass-spec repository accession and no named MS instrument model; no gRNA or shRNA target sequences; no RRID/clone/application-dilution/host-clonality for most antibodies; no STR authentication or mycoplasma testing for cell lines; no IACUC protocol number for the mouse-derived GNPs; and no data-availability or code-availability statement. Sample sizes, statistical tests, and error-bar definitions are generally well reported. Several methods are delegated to citations that are resolvable but whose contents cannot be verified from the manuscript alone.

## Categories checked
- Antibodies/immunodetection
- Cell lines/primary cells
- Model organisms
- Chemicals/drugs/dosing
- Oligos/plasmids/constructs
- Mass spectrometry
- Microscopy/imaging
- Computational/ML
- Cross-cutting (sample size, statistics, software versions, data/code availability)
- Protocol provenance

**HARD gaps (blocking): 15** · SOFT gaps: 3 · unverifiable: 1

## HARD gaps — reproduction blockers
- **[Cross-cutting] Software, tool, and instrument versions** — Some versions given (GraphPad Prism 8, ShinyGO 0.81), but R version, FIJI/ImageJ version, ProLuCID/DTASelect2/Census2/RawConverter versions, and mass-spec instrument model are not stated. The MS section describes 'nano-LC on a RP 18 column' without naming the mass spectrometer.
- **[Antibodies/immunodetection] Antibody RRID and clone** — No RRIDs are provided for any antibody, and clone identifiers are not given (e.g. 'Mouse anti-PKACa (BD Biosciences, 610980)' has no clone; the pSmo antibody is listed only as '7TM0239A-IC').
- **[Antibodies/immunodetection] Antibody application + dilution** — Dilutions are given only in the GNP protocol (pSMO 1:1000, ARL13B 1:500); the Antibodies list and the fibroblast IF/WB methods do not state application (WB vs IF vs IP) or dilution for the listed antibodies.
- **[Antibodies/immunodetection] Antibody host species / clonality** — The Antibodies list gives species in some names (e.g. 'Rabbit anti-pSmo', 'Mouse anti-V5') but clonality (monoclonal vs polyclonal) is not stated for most entries.
- **[Cell lines/primary cells] Cell line RRID/CVCL** — No RRIDs or CVCL identifiers are provided for NIH3T3, Flp-In 3T3, 293T, or MEF lines.
- **[Cell lines/primary cells] Authentication (STR) and mycoplasma testing** — No STR authentication or mycoplasma-testing statement is provided for any cell line.
- **[Model organisms] IACUC/animal protocol number** — No IACUC/animal-welfare protocol number is stated for the use of P7 mice to harvest GNPs.
- **[Model organisms] Sex, age, n per group, randomization/blinding** — Age (P7) is given, but sex of animals, number of animals per condition, and any randomization/blinding statement are not reported.
- **[Chemicals/drugs/dosing] Identity traceable to vendor/catalog or CAS** — Cyclopamine is traceable (Selleckchem, S1146), but SAG (100 nM), recombinant ShhN (1 µg/ml), and biotin (500 µM) are used without vendor/catalog numbers or CAS identifiers.
- **[Oligos/plasmids/constructs] gRNA target sequence and Cas variant/delivery/edit validation** — Git1 knockout uses 'CRISPR/Cas9-mediated genome editing targeting exon 2' with Sanger-sequencing validation (Fig S4A-B), but the gRNA target sequence is not provided; Cas variant and delivery method are not stated.
- **[Oligos/plasmids/constructs] shRNA target sequences** — Git1 shRNA #1/#2 and 'scrambled shRNA' are used (Figs 4H, 7A) but the target sequences are not provided.
- **[Mass spectrometry] Instrument + acquisition mode** — The MS section describes nano-LC on an RP18 column and MS1/MS2 fragmentation with TMT reporter ions, but the mass spectrometer model and acquisition mode (e.g. Orbitrap, DDA) are not named.
- **[Mass spectrometry] Repository accession (PRIDE/MassIVE)** — No PRIDE, MassIVE, or other repository accession is provided for the raw mass-spec data or the processed TMT dataset, despite the paper describing the dataset as a resource.
- **[Computational/ML] Analysis tool versions (R, packages) and code availability** — R analysis with eBayes/TMM normalization is described, but R version and package versions are not stated; no code repository is provided (code availability is SOFT).
- **[Protocol provenance] Load-bearing claim not outsourced to citation / 'data not shown'** — The Smo-Git1 interaction is stated as 'challenging to detect via co-immunoprecipitation (data not shown)' — a load-bearing interaction claim supported only by 'data not shown' rather than presented evidence or a resolvable citation.

## Unverifiable (raise as questions)
- **[Protocol provenance] Delegated methods resolve to a specific, plausible protocol reference** — Several methods are delegated to citations that are resolvable but whose contents cannot be confirmed from the manuscript alone: GNP culture 'as previously described71' (Peng et al. 2021), CRISPR PRKACA knockout 'as previously described16' (Arveseth et al. 2021), DArl13b 'described previously in Liu et al. 2024' (ref 23), PKA-deficient MEFs 'obtained from Kathryn Anderson's lab55' (Tuson et al. 2011). These appear to resolve to real references but their protocol contents cannot be verified here.

## SOFT gaps — recommended
- **[Cross-cutting] Data-availability statement** — No data-availability section or statement appears anywhere in the manuscript; the proteomics dataset is described as a 'resource' but no repository link is given.
- **[Cross-cutting] Code availability for custom analysis** — Custom R analysis (eBayes moderation, TMM/scaling normalization) is described in Methods and 'Supplementary data 4/5' are referenced, but no code repository, version, or availability statement is provided.
- **[Microscopy/imaging] Analysis software with version** — FIJI/ImageJ is used for quantification but no version is given.

## Documented (for the record)
- **[Cross-cutting] Sample size n with what n represents (biological vs technical replicates)** — n values are stated throughout with replicate identity, e.g. 'n = 150 cells/condition; data are pooled from 3 biological replicates' (Fig 1B), 'n = 90 cells/condition from three biological replicates' (Fig 4I), 'n = 4 independent experiments' (Fig 6C-D), 'n = 10 fields for each condition' (Fig 7E).
- **[Cross-cutting] Named statistical test and error-bar definition (SD/SEM/CI)** — Tests named: two-tailed unpaired t test, one-way ANOVA + Tukey/Sidak, two-way ANOVA + Tukey (Quantification and statistical analysis). Error bars stated as 'mean ± SD' in multiple figure legends (Figs 3D, 5D-E, 7B-C-E).
- **[Antibodies/immunodetection] Antibody vendor + catalog number** — Antibodies listed with vendor and catalog in the Antibodies section, e.g. anti-acetylated tubulin (Sigma, T6793), anti-Arl13b (Proteintech, 17711-1-AP), anti-Git1 (Novus, NBP1-86144), anti-PKACa (BD, 610980), anti-pSmo (7TM, 7TM0239A-IC).
- **[Cell lines/primary cells] Cell line source** — Sources given: NIH3T3 (ATCC, CRL-1658), Flp-In 3T3 (Thermo Fisher, R76107), 293T (ATCC, CRL-3216); PKA-deficient MEFs from Kathryn Anderson's lab; GNPs from P7 C57BL/6J mice.
- **[Cell lines/primary cells] Culture media/supplements** — Media specified: DMEM + 10% FBS (Flp-In 3T3, 293T, MEFs), DMEM + 10% calf serum (NIH3T3), Neurobasal + B-27 + GlutaMAX + Pen/Strep (GNPs); serum starvation to 0.5% for ciliation.
- **[Model organisms] Species/strain/source and genotype/background** — P7 C57BL/6J mice used for GNP culture; genotype/background stated as C57BL/6J.
- **[Chemicals/drugs/dosing] Dose, route/mode, vehicle, schedule** — Doses and schedules given: 100 nM SAG, 5 µM cyclopamine, 1 µg/ml ShhN or 20-30% ShhN-conditioned medium, 500 µM biotin for 15 min; vehicle (DMSO) and treatment durations (15 min-24 h) are specified.
- **[Oligos/plasmids/constructs] Plasmid source / full description** — Plasmid sources given: Smo cloned into pEF5/FRT/V5-DEST (Thermo, V602020); YFP-Git1 (Addgene 15225); FUGW backbone (Addgene 14883); TurboID (gift from A. Ting); Grk2 (gift from B. Myers); DArl13b 'described previously in Liu et al. 2024'.
- **[Mass spectrometry] Search engine + version, database + version, FDR, modifications, tolerances** — ProLuCID search against UniProt Mus musculus UP000000589 (with mSmo-V5-TurboID and streptavidin added); FDR 1% (target-decoy); static modifications carbamidomethylation (+57.02146 C) and TMT (+229.1629 K/N-term); 50 ppm precursor / 500 ppm fragment tolerance; DTASelect2 and Census2 used.
- **[Microscopy/imaging] Instrument model, objective/NA, detector, settings** — Instruments named: Zeiss LSM 880, Leica DMi8, Leica Mica, YOKOGAWA CSU-W1 with PRIME 95B camera; objectives 100x oil and 63x oil are stated.