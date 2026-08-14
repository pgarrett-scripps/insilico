# Methods Completeness & Reagent Traceability Auditor

## Summary
This is a molecular-neuroscience manuscript (TDP-43 acetylation and nuclear import) using iPSC-derived human neurons, human cell lines, mice, human postmortem tissue, quantitative and PTM mass spectrometry, immunodetection (WB/IF/IP/ELISA), lentiviral constructs/CRISPR editing, and confocal/live-cell imaging. Cross-cutting items are partially met: the statistical-test and error-bar conventions are stated, and n is defined as biological replicates, but specific n per experiment is frequently absent and several analysis tools lack versions; there is no data-availability or code-availability statement. The largest reproducibility gaps are that nearly all reagent identifiers (antibodies, plasmids, primers, human-case demographics) are delegated to Supplementary Tables S1–S5 that are not included in the manuscript, the CRISPR knock-in editing is not described (no gRNA/Cas/edit validation), mass-spec repository accessions and database versions are absent, and the mouse experiments lack strain/source, sex, n-per-group, IACUC, and randomization details. Human IRB/consent and chemical dosing are well documented. No score is assigned.

## Categories checked
- Antibodies/immunodetection
- Cell lines/primary cells
- Model organisms/in vivo
- Human subjects/clinical
- Chemicals/drugs/dosing
- Oligos/plasmids/constructs
- Mass spec
- Microscopy/imaging
- Computational/ML
- Protocol provenance

**HARD gaps (blocking): 17** · SOFT gaps: 3 · unverifiable: 1

## HARD gaps — reproduction blockers
- **[Cross-cutting] Software/tool/instrument versions** — Some versions given (Prism 8, CQ1 software v.1.05.01.02, Rawconverter, DTASelect2, Census2), but image-analysis/quantification software is unnamed and unversioned, and PTM MS search is 'MaxQuant or Proteome Discoverer' with no version.
- **[Antibodies/immunodetection] Antibody vendor, catalog #, clone, RRID, application+dilution, host/clonality** — All antibody identifiers are delegated to 'Supplementary Table S3' (IF), 'Supplementary Table S4' (WB), and 'Supplementary Table S5' (magnetic beads), none of which are included in the manuscript. No vendor/catalog/clone/RRID/dilution is given in the text.
- **[Cell lines/primary cells] Authentication (STR) and mycoplasma testing** — No STR authentication or mycoplasma-testing statement for HEK293T, SH-SY5Y, or iPSC lines.
- **[Model organisms/in vivo] Species, strain, source/RRID** — Mouse cortex used for proteasome-activity aging curve (Fig S1A) but no strain, source, or RRID is stated.
- **[Model organisms/in vivo] Sex and age** — Age given (3, 6, 12, 18, 24 months) but sex is not stated.
- **[Model organisms/in vivo] n per group** — No n per age group stated for the mouse proteasome-activity data.
- **[Model organisms/in vivo] IACUC protocol number** — No IACUC/animal-welfare approval number is stated for mouse work.
- **[Model organisms/in vivo] Randomization/blinding statement** — No randomization or blinding statement for animal experiments.
- **[Human subjects/clinical] Inclusion/exclusion criteria** — No inclusion/exclusion criteria for the 4 control and 6 sALS cases are stated.
- **[Human subjects/clinical] Participant demographics** — Demographics (age, sex, disease duration, etc.) are delegated to 'Supplementary Table S2', not included in the manuscript.
- **[Oligos/plasmids/constructs] Plasmid source/description** — All plasmids are delegated to 'Supplementary Table S1' (not included); Addgene deposit is only 'at the time of publication', so no accession is currently available.
- **[Oligos/plasmids/constructs] Primer/oligo and siRNA sequences** — qRT-PCR primers/probes delegated to 'Supplementary Table S5' (not included); human TDP-43 siRNA target sequences are not given.
- **[Oligos/plasmids/constructs] CRISPR editing: Cas variant, delivery, gRNA, edit validation** — TDP-43-Clover homozygous knock-in at both endogenous alleles is stated ('Following editing of both endogenous alleles') but no gRNA sequence, Cas variant, delivery method, or edit-validation data are provided.
- **[Mass spec] Database version and repository accession (nuclear proteome)** — Search database is 'a complete human protein database downloaded from UniProt' with no version/date; no PRIDE/MassIVE accession is provided.
- **[Mass spec] PTM MS: instrument, acquisition mode, search engine+version, repository** — PTM detection described only as 'analyzed by LC-MS/MS, using either data-dependent or data-independent acquisition' with 'MaxQuant or Proteome Discoverer' (no version); no instrument, database version, FDR, or repository accession given.
- **[Microscopy/imaging] Image-analysis software and version** — Quantification of nucleocytoplasmic ratios and fluorescence intensities is described but the analysis software and version are not named.
- **[Protocol provenance] Load-bearing method outsourced to citation** — The TDP-43-Clover endogenous knock-in (central to PTM identification) is not described in full and is not delegated to a resolvable protocol; no gRNA/Cas/edit-validation detail is given anywhere.

## Unverifiable (raise as questions)
- **[Protocol provenance] iPSC/NGN2 line provenance citation** — iPSC 'previously engineered to express NGN2' cites ref 37 (Fernandopulle et al.); the reference is plausible but its contents cannot be confirmed from the manuscript alone.

## SOFT gaps — recommended
- **[Cross-cutting] Data-availability statement** — No data-availability statement appears anywhere in the manuscript.
- **[Cross-cutting] Code availability (custom analysis)** — Volcano plot 'generated using the R package' with no package name, version, or code deposit; no code-availability statement.
- **[Computational/ML] Analysis code and versions** — Volcano plot uses an unnamed 'R package' with no version or code deposit; not a full ML pipeline.

## Documented (for the record)
- **[Cross-cutting] Sample size n stated with what n represents** — Statistical tests section: 'Each data point represents an independent biological replicate (distinct wells of independently treated cells or individual tissue donors).' Specific n given for human cohorts (n=4 control, n=6 sALS) and mouse ages (3-24 mo). However, specific n is not stated for most figures (e.g., Fig 1E volcano, Fig 3F binding curves, Fig 4 quantifications).
- **[Cross-cutting] Named statistical test and error-bar definition** — Statistical tests section names two-tailed Student's t-test, one-way ANOVA with Tukey, Chi-squared with Yates; 'Error bars represent SEM unless stated otherwise.'
- **[Antibodies/immunodetection] Custom acetylation-specific TDP-43 K82 antibodies** — Generation described in Methods (Sanyou Inc., KLH-conjugated peptide 77-90, rabbit polyclonal, affinity-enriched, validated by ELISA); no clone/RRID assigned.
- **[Cell lines/primary cells] Cell-line source and identifiers** — HEK293T (ATCC CRL-11268) and SH-SY5Y (ATCC CRL-2266) given; iPSC is WTC11 background with NGN2 knock-in, 'gift of Michael Ward' (ref 37). No RRID/CVCL for any line.
- **[Cell lines/primary cells] Media and supplements** — Detailed media formulations with catalog numbers given for iPSC maintenance and i3Neuron differentiation (E8, N2, Neurobasal/B27, BDNF, laminin, doxycycline).
- **[Human subjects/clinical] IRB approval and informed consent** — UCSD ALS tissue repository, HIPAA-compliant informed consent, IRB# 10058 (Benaroya) and IRB# 120056 (UCSD) stated.
- **[Chemicals/drugs/dosing] Identity traceable to vendor/catalog # and dose per experiment** — BTZ (ApexBio A2614), MG132 (Selleckchem S2619), MRZ (Selleckchem S7504), doxycycline, Y-27632, etc., with catalog numbers; doses given (BTZ 2 nM, MG132 100 nM, MRZ 10 nM; higher doses in some figures).
- **[Oligos/plasmids/constructs] Selection markers** — Selection concentrations given (neomycin 400 µg/mL, blasticidin-S 10 µg/mL, puromycin 3 µg/mL).
- **[Mass spec] Nuclear-proteome MS: instrument, mode, digestion, search, FDR, tolerances** — Orbitrap Eclipse, DDA with MS3 SPS, trypsin/lys-C digestion, DTASelect2/Rawconverter/Census2, FDR ≤1%, tolerances 50 ppm precursor / 500 ppm CID / 20 ppm HCD, static carbamidomethylation + TMT.
- **[Microscopy/imaging] Instrument model, objective, NA, detector** — Confocal: Yokogawa X1 on Nikon Ti2, Plan Apo Lambda 100x oil NA 1.45 and 60x oil NA 1.4. Live-cell: CQ1 benchtop spinning-disk (Yokogawa), CQ1 software v.1.05.01.02, 40x/60x dry objectives.
- **[Protocol provenance] Vendor-protocol delegations** — Abcam Nuclear Extraction Kit, ATCC guidelines, TransIT X2 product protocol, and manufacturer instructions are self-contained vendor protocols; no circular or dead citations detected.