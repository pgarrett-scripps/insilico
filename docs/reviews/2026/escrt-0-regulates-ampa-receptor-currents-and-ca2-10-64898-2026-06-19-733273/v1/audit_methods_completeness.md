# Methods Completeness & Reagent Traceability Auditor

## Summary
The manuscript is generally well-documented with strong reporting of sample sizes, statistical tests, error bars, software versions, and reagent catalogs. Key HARD gaps: (1) IACUC protocol number is missing, (2) no randomization/blinding statement for in vivo experiments, (3) RRIDs are absent for all antibodies, (4) shRNA target sequences for Hrs knockdown are not provided. SOFT gaps: custom R analysis code is not deposited in a repository, and antibody host species/clonality is partially reported. All cited 'as previously described' methods resolve to published, DOId references. Overall, the missing items are addressable and would enable full reproducibility.

## Categories checked
- Model organisms / in vivo
- Antibodies/immunodetection
- Mass spec (proteomics/metabolomics)
- Computational/ML/modeling
- Protocol provenance

**HARD gaps (blocking): 5** · SOFT gaps: 2 · unverifiable: 0

## HARD gaps — reproduction blockers
- **[Model organisms / in vivo] IACUC protocol number** — 'All animal experiments were conducted in strict accordance with protocols designed to minimize animal suffering and were approved by the Institutional Animal Care and Use Committee (IACUC) at the University of California, San Diego (UCSD).'
- **[Model organisms / in vivo] Randomization/blinding statement** — No explicit randomization or blinding statement for in vivo experiments (e.g., allocation to AAV groups, Cre vs control).
- **[Antibodies/immunodetection] RRID for each antibody** — Extensive list of antibodies in Immunoblot analysis and Immunostaining sections. Each antibody is listed with vendor and catalog number (e.g., 'anti-Hrs (CST, 15087)', 'anti-PSD95 (CST, 3450)', 'anti-Bassoon (1:1000, Synaptic Systems 141119)'). Clonality/host species not always stated (e.g., 'mouse anti-GFP (1:1000, Santa Cruz Biotechnology, sc-9996)', 'anti-Hrs (Mouse, SantaCruz sc-271455, 1:500)').
- **[Oligos/plasmids/constructs] shRNA target sequence(s)** — 'AAV to mediate depletion of Hrs via shRNA' — 'VectorBuilder, Chicago, IL' mentioned. 'scrambled control shRNA AAV or an Hrs-targeting shRNA AAV' — no shRNA target sequences provided.
- **[Model organisms / in vivo] Randomization/blinding statement** — No statement about randomization or blinding for the in vivo experiments (Cre+/Cre- comparisons, AAV injections).

## SOFT gaps — recommended
- **[Computational/ML/modeling] Code availability for custom analysis** — Custom analysis was done in R (version 4.4.2, then 4.5.2) with packages pheatmap, clusterProfiler, ggplot2, etc. Exact code/repository not deposited. The statement: 'Mass spectrometry data was visualized in R...' but no link to a code repository.
- **[Cross-cutting] Code availability when custom analysis was done** — Custom analysis scripts in R described but no repository URL or DOI provided.

## Documented (for the record)
- **[Model organisms / in vivo] Species, strain, source, RRID** — Hrsf/f mice on C57BL/6J background crossed with hSyn1-Cre mice (The Jackson Laboratory). 'All Hrsf/f Cre+ and Cre- littermates were housed...' Age: 'Hrsf/f Syn Cre+ and Cre- mice' used; 'adult male and female C57BL/6J mice (57-73 days old)' for PSD prep; 'male C57BL/6J mice (80-120 days old)' for AAV transduction.
- **[Model organisms / in vivo] Genotype and background** — Hrsf/f mice on a C57BL/6J background (Tamai et al., 2008) crossed with hSyn1-Cre mice (The Jackson Laboratory).
- **[Model organisms / in vivo] Sex** — 'Age-matched littermates female Hrsf/f Cre+ and Cre- mice...' and 'adult male and female C57BL/6J mice (57-73 days old)'. Also 'male C57BL/6J mice (80-120 days old)' for AAV.
- **[Model organisms / in vivo] Age** — See above — ages explicitly given for each experiment.
- **[Model organisms / in vivo] n per group** — Hrsf/fCre+ (n=7) and Cre- (n=7) for biochemical analyses; n=4 Cre+ and n=5 Cre- for phosphoproteomics; n=6 per group for AAV overexpression.
- **[Model organisms / in vivo] Housing conditions and power justification** — 'Age-matched littermates' are mentioned; no specific housing conditions beyond 'specific pathogen-free conditions in a 12-hour light/dark cycle.' No power justification.
- **[Antibodies/immunodetection] Application + dilution for every antibody** — Dilutions given throughout (e.g., '1:1000', '1:500', '1:250').
- **[Antibodies/immunodetection] Host species/clonality for each primary antibody** — Some entries include host species (e.g., 'mouse anti-GFP', 'anti-Hrs (Mouse)') but many do not (e.g., 'anti-PSD95 (CST, 3450)', 'anti-Bassoon (chicken; Synaptic Systems, 141119,1:1000)').
- **[Mass spec (proteomics/metabolomics)] Instrument + acquisition mode** — 'Orbitrap Fusion Lumos Tribrid Mass Spectrometer (Thermo Scientific)', 'EasynLC 1200 system (Thermo Scientific)', full gradient described, MS1 120K resolution, CID in ion trap, MS3 SPS3 60K.
- **[Mass spec (proteomics/metabolomics)] Sample prep/digestion/enrichment** — 'precipitated with methanol and chloroform. The precipitated proteins were digested with trypsin...' 'Phosphorylated peptides were enriched sequentially using ferric nitrilotriacetate (Fe-NTA) Thermo Scientific Phosphorylation Enrichment Kit.'
- **[Mass spec (proteomics/metabolomics)] Search engine + version, database + version, FDR, modifications, tolerances** — 'Proteome Discoverer 2.5', 'Uniprot mouse protein database with isoforms (version 2022-06-14)', '1% FDR', 'phosphorylation (+79.9663 Da) as variable modification on serine, threonine, and tyrosine', 'TMT labeling as static modification on lysine and peptide N-termini (+229.162932 Da) and carbamidomethylation of cysteine (+57.021464 Da)' — search engine version: Proteome Discoverer 2.5, database: Uniprot mouse (2022-06-14), FDR 1%, modifications listed. Precursor and fragment tolerance not explicitly stated.
- **[Mass spec (proteomics/metabolomics)] Repository accession (PRIDE/MassIVE)** — 'Raw mass spectrometry data is publicly available in the ProteomExchange depository (PXD073715).'
- **[Computational/ML/modeling] Software/library versions** — R-package versions listed (e.g., clusterProfiler version 4.12.6, ggplot2 version 4.0.1, pheatmap version 1.0.13).
- **[Protocol provenance] 'performed as previously described' — Keil et al. 2010 resolves** — PSD purification: 'performed with modifications based on a previously described protocol (Keil et al., 2010)' — Keil et al. 2010 is cited (DOI/PMID available in references). The modifications are described in the text.
- **[Protocol provenance] 'using a previously established protocol' — Patrick et al. 2003 resolves** — 'Primary hippocampal or cortical neurons ... using a previously established protocol (Patrick et al., 2003).' Patrick et al. 2003 is in references with DOI.
- **[Protocol provenance] Full method description vs delegated** — 'Surface biotinylation assay' — no citation, described fully.
- **[Protocol provenance] 'as described previously' — Dore et al. 2021 resolves** — 'Organotypic hippocampal slices were prepared ... as described previously (Dore et al., 2021).' Dore et al. 2021 is cited in references with DOI.
- **[Protocol provenance] 'modifications to a previously described protocol' — Thakar et al. 2017 resolves** — 'Post-synaptic membrane (PSM) fractions were prepared with modifications to a previously described protocol (Thakar et al., 2017).' Thakar et al. 2017 is cited in references with DOI. Modifications described.
- **[Protocol provenance] 'according to an established method' — Zecha et al. 2019 resolves** — 'TMT labeling ... according to an established method (Zecha et al., 2019).' Zecha et al. 2019 is cited with DOI.
- **[Protocol provenance] 'following a previously described protocol' — Kawata et al. 2023 resolves** — '...followed by solubilization...' — no citation, described. '...digested with trypsin following a previously described protocol (Kawata et al., 2023).' Kawata et al. 2023 is cited with DOI.
- **[Cross-cutting] Sample size n stated with what n represents (biological vs technical)** — Sample sizes stated per experiment (e.g., n=7, n=6, n=3, n=30 dendrites). Biological vs technical replicates: e.g., 'N = 8 independent experiments', 'n = 30 and 36 dendrites ... from 2 and 3 independent experiments', 'N = 3 independent cultures'.
- **[Cross-cutting] Named statistical test and what error bars represent (SD/SEM/CI)** — Named tests: 'unpaired two-tailed Student's t test', 'Chi-square (Fisher's exact) test', 'one-way ANOVA with Tukey's multiple comparison test'. Error bars: 'mean ± SEM' stated throughout.
- **[Cross-cutting] Software, tool, and instrument versions** — Software versions stated: GraphPad Prism version 10, R version 4.4.2/4.5.2, various R-package versions, Proteome Discoverer 2.5, Huygens Essential, ImageJ/FiJi, Clampex 11, Clampfit 11, MultiClamp 700B, Axon Digidata 1550B. Instrument models: Leica DMI6000 B, Abberior Facility Line microscope, Orbitrap Fusion Lumos, EasynLC 1200.
- **[Cross-cutting] Data-availability statement** — 'All data generated or analyzed during this study are included in the manuscript and supporting files.' Also 'Raw mass spectrometry data is publicly available in the ProteomExchange depository (PXD073715).'
- **[Chemicals/drugs/dosing] Identity traceable to vendor + catalog # or CAS** — Bicuculline (Bic; Tocris, 0130), tetrodotoxin (TTX; Tocris, 1069), AMPA (20 µM), DMSO vehicle. Concentrations: '20 µM bicuculline', '2 µM tetrodotoxin', '72 hours' for chronic treatment, '10 minutes' for AMPA.
- **[Chemicals/drugs/dosing] Dose/concentration per experiment** — See above: concentration stated for each experiment.
- **[Chemicals/drugs/dosing] Vehicle + final concentration** — '2 µL DMSO' as vehicle for chronic activity modulation; final concentration not explicitly stated for bicuculline/TTX in terms of DMSO % but described.
- **[Oligos/plasmids/constructs] Plasmid source (Addgene #) or full description** — 'AAV-Cre [pENN.AAV.hSyn.HI.eGFP-Cre.WPRE.SV40 (AAV PHP.eB), Addgene #105540-PHPeB]', 'AAV-YFP [hSyn1-eYFP (AAV PHP.eB), Addgene #117382-PHPeB]', 'CAP-B10 hSyn-GFP and CAP-B10 hSyn-Hrs' — Addgene numbers provided for some constructs; CAP-B10 constructs not linked to Addgene.