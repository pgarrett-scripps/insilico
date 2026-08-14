# Methods Completeness & Reagent Traceability Auditor

## Summary
This manuscript uses iPSC-derived human cortical neurons, SH-SY5Y and HEK293T cell lines, fresh-frozen human motor cortex samples, and mice, with extensive immunodetection (WB/IF/IP/co-IP/ELISA), chemical proteasome-inhibitor dosing, plasmid/siRNA manipulation, TMT quantitative mass spectrometry and PTM mass spectrometry, and confocal/live-cell microscopy. Cross-cutting items (n, replicate definition, statistical tests, error bars) are largely present; software versions, data-availability and code-availability statements are incomplete. The dominant reproducibility gap is that nearly all key resources (antibodies, plasmids, primers, human-sample demographics) are deferred to Supplementary Tables S1-S5 that are not present in the manuscript text, so they are unverifiable from the manuscript alone. Several HARD identifiers (cell-line authentication/mycoplasma, siRNA/gRNA sequences, mass-spec repository accession, mouse strain/IACUC, image-analysis software) are absent. No score or accept/reject judgment is rendered.

## Categories checked
- Antibodies/immunodetection
- Cell lines/primary cells
- Model organisms / in vivo
- Human subjects/clinical
- Chemicals/drugs/dosing
- Oligos/plasmids/constructs
- Mass spec (proteomics/metabolomics)
- Microscopy/imaging/flow
- Computational/ML/modeling
- Protocol provenance

**HARD gaps (blocking): 9** · SOFT gaps: 4 · unverifiable: 6

## HARD gaps — reproduction blockers
- **[Cross-cutting] Software/tool/instrument versions** — Prism 8 (GraphPad) and CQ1 software v.1.05.01.02 are versioned; but versions are absent for RawConverter, DTASelect2, Census2, MaxQuant/Proteome Discoverer, R package for volcano plot, and image-quantification software.
- **[Cell lines/primary cells] Authentication (STR) and mycoplasma testing** — No STR authentication or mycoplasma-testing statement is provided for HEK293T, SH-SY5Y, or iPSC lines.
- **[Model organisms / in vivo] Mouse strain/source/RRID, genotype/background** — Fig. S1A uses mice of 3-24 months for proteasome-activity decline, but no strain, source, or background is stated.
- **[Model organisms / in vivo] Mouse sex, n per group, IACUC protocol #** — No sex, group size, or IACUC/animal-welfare protocol number is stated for the mouse experiments.
- **[Human subjects/clinical] Inclusion/exclusion criteria** — No explicit inclusion/exclusion criteria for control vs sALS cases are stated (only '4 control cases, 6 sALS cases').
- **[Chemicals/drugs/dosing] Vehicle + final concentration** — The vehicle/solvent (e.g., DMSO) and its final concentration for BTZ/MG132/MRZ treatments are not stated.
- **[Oligos/plasmids/constructs] siRNA/shRNA/gRNA target sequences** — Human TDP-43 siRNAs are used (48 hr pre-treatment) but no target sequences are given; the endogenous TDP-43-Clover knock-in editing (both alleles) is described without gRNA sequence, Cas variant, or edit validation details.
- **[Mass spec (proteomics/metabolomics)] Repository accession (PRIDE/MassIVE)** — No mass-spectrometry data repository accession (PRIDE/MassIVE) is provided for either the TMT nuclear-proteome or the PTM datasets.
- **[Microscopy/imaging/flow] Analysis/quantification software + version** — Image quantification (nucleocytoplasmic ratios, nuclear fluorescence intensities in Figs. 1D, 3D, 4E/G, 2G/H) is described but the analysis software and version are not stated.

## Unverifiable (raise as questions)
- **[Antibodies/immunodetection] Antibody vendor/catalog/clone/RRID/application+dilution/host-clonality** — Methods state 'Antibodies and dilutions are provided in Supplementary Table S3' (IF), 'Supplementary Table S4' (WB), and 'Supplementary Table S5' (IP beads); these tables are not present in the manuscript text, so the identifiers cannot be confirmed. Only Anti-6*His-HRP (Proteintech HRP-66005) and Anti-rabbit-HRP (Proteintech SA00001-2) are given inline.
- **[Human subjects/clinical] Participant demographics** — Demographics are deferred to 'Supplementary Table S2', which is not present in the manuscript text.
- **[Oligos/plasmids/constructs] Plasmid source/description** — Methods state 'all plasmids used in this paper is listed in Supplementary Table S1' and 'will be deposited to Addgene at the time of publication'; the table is not present in the manuscript text and deposition is prospective.
- **[Oligos/plasmids/constructs] Primer/probe sequences** — qRT-PCR/RT-PCR primers are deferred to 'Supplementary Table S5', not present in the manuscript text.
- **[Protocol provenance] iPSC NGN2 differentiation 'as previously engineered... WTC11 background37'** — Delegated to ref 37 (Fernandopulle et al., Curr Protoc Cell Biol 79, e51, 2018), a resolvable citation that plausibly contains the protocol; contents cannot be confirmed from the manuscript alone.
- **[Protocol provenance] Claims supported by cited work (refs 30, 33, 34)** — Statements 'consistent with a recent report30', 'challenges an earlier hypothesis33', and 'supported by a mass spectrometry analysis...34' cite references whose contents cannot be verified from the manuscript alone.

## SOFT gaps — recommended
- **[Cross-cutting] Data-availability statement** — No data-availability statement is present anywhere in the manuscript.
- **[Cross-cutting] Code availability (custom analysis)** — Volcano plot 'was generated using the R package' but no code, package name, or repository is provided.
- **[Human subjects/clinical] COI/funding statement** — No funding or conflict-of-interest statement is present in the manuscript.
- **[Computational/ML/modeling] Analysis tool + version / code availability** — Volcano plot generated with an unnamed 'R package'; no version or code provided. No ML/modeling is performed, so no architecture/hyperparameter items apply.

## Documented (for the record)
- **[Cross-cutting] Sample size n stated with what n represents** — Figure legends state n=4 control and n=6 sALS (Fig. S1A, Fig. 5B); statistics section states 'Each data point represents an independent biological replicate (distinct wells of independently treated cells or individual tissue donors).'
- **[Cross-cutting] Named statistical test** — Statistics section: two-tailed Student's t-tests; one-way ANOVA with Tukey's correction; Chi-squared with Yates' correction; one-sample two-sided t-test for MS volcano plot.
- **[Cross-cutting] Error bars meaning (SD/SEM/CI)** — Statistics section: 'Error bars represent SEM unless stated otherwise.'
- **[Antibodies/immunodetection] Ac-K82 TDP-43 polyclonal antibody generation/validation** — Methods describe generation by Sanyou Inc. against TDP-43 aa77-90 acetylated at K82, KLH conjugation, rabbit immunization, affinity enrichment, and ELISA validation (Fig. 5A).
- **[Cell lines/primary cells] Cell line source + RRID/CVCL** — HEK293T (ATCC CRL-11268) and SH-SY5Y (ATCC CRL-2266) given; iPSCs are a gift of Michael Ward, WTC11 background with NGN2 at AAVS1 (ref 37).
- **[Cell lines/primary cells] Media/supplements** — Detailed media formulations given (E8, N2, i3Neuron/Neurobasal+B27, DMEM/F12) with catalog numbers.
- **[Human subjects/clinical] IRB approval + informed consent** — Methods: HIPAA-compliant informed consent; IRB# 10058 (Benaroya) and IRB# 120056 (UCSD).
- **[Chemicals/drugs/dosing] Identity traceable to vendor+catalog/CAS** — BTZ (ApexBio A2614), MG132 (Selleckchem S2619), MRZ (Selleckchem S7504), doxycycline (Sigma D9891), Y-27632 (Selleckchem S1049), and many media reagents carry catalog numbers.
- **[Chemicals/drugs/dosing] Dose/concentration per experiment** — Doses given: BTZ 2 nM (and 20 nM in some figures), MG132 100 nM, MRZ 10 nM/100 nM; doxycycline 2 ug/ml; ROCK inhibitor 10 uM.
- **[Mass spec (proteomics/metabolomics)] Instrument + acquisition mode** — Orbitrap Eclipse with nLC 1200; data-dependent mode, MS3 SPS multi-notch; MS1 at 120k resolution; 3 s cycle time; 120 min gradient.
- **[Mass spec (proteomics/metabolomics)] Sample prep/digestion/enrichment** — Trypsin/lys-C digestion, TMT six-plex labeling, C18 desalting; PTM MS uses trypsin+chymotrypsin and TiO2 enrichment.
- **[Mass spec (proteomics/metabolomics)] Search engine + version, database + version, FDR, modifications, tolerances** — DTASelect2/Census2 (quant), UniProt human database, FDR <=1%, carbamidomethylation + TMT (+229.162932 Da) static mods, 50 ppm precursor / 500 ppm CID / 20 ppm HCD tolerances. PTM analysis cites 'MaxQuant or Proteome Discoverer' without versions.
- **[Microscopy/imaging/flow] Instrument model, objective+NA+detector+settings** — Yokogawa X1 on Nikon Ti2 with 100x oil NA 1.45 and 60x oil NA 1.4 objectives; CQ1 benchtop spinning-disk with 40x/60x dry objectives; DAPI, ProLong Gold mounting.
- **[Protocol provenance] Kit-based protocols (Abcam Nuclear Extraction, Proteasome-Glo, CellTiter-Glo, TransIT X2, ATCC guidelines)** — These are self-contained commercial kit protocols with catalog numbers and manufacturer instructions, not delegated to external citations.