# Methods Completeness & Reagent Traceability Auditor

## Summary
The manuscript is a spatial proteomics study (TMT-LC-MS of fractionated human AD/NA hippocampi plus QUAD degradation in an AD mouse model). Detected categories: cross-cutting (sample size, statistics/error bars, software versions, data availability, code availability), antibodies/immunodetection (WB + ELISA), model organisms (mice), human subjects (post-mortem tissue), chemicals/dosing (AHA diet, click chemistry, TMT), mass spectrometry, computational/bioinformatics, and protocol provenance. Overall the protocol is largely self-contained with strong reagent traceability for antibodies (catalog numbers) and mass-spec parameters, but several HARD items are absent: error-bar definition, antibody dilution and host/clonality/RRID, IACUC protocol number, randomization/blinding, human IRB approval and informed consent, inclusion/exclusion criteria, MS mass tolerances, and a proteomics repository accession. No data-availability or code-availability statement is present (SOFT).

## Categories checked
- Cross-cutting (sample size, statistics, software versions, data/code availability)
- Antibodies / immunodetection
- Model organisms / in vivo
- Human subjects / clinical
- Chemicals / drugs / dosing
- Mass spectrometry
- Computational / bioinformatics
- Protocol provenance

**HARD gaps (blocking): 11** · SOFT gaps: 4 · unverifiable: 6

## HARD gaps — reproduction blockers
- **[Cross-cutting] What error bars represent (SD/SEM/CI)** — Figures show error bars (e.g., Fig 5B, 8E/F, 9B) but the manuscript never states whether they are SD, SEM, or CI. No definition of error bars or dispersion measure is given anywhere in Methods or figure legends.
- **[Antibodies / immunodetection] VPS35 antibody vendor + catalog + clone + host/clonality + dilution** — VPS-35 (SCBT, #sc-374372) — vendor and catalog present, but clone, host species/clonality, RRID, and application dilution are not stated.
- **[Antibodies / immunodetection] TAU-5 antibody vendor + catalog + clone + host/clonality + dilution** — TAU-5 (Life Technologies, #AHB0042) — vendor and catalog present, but clone, host species/clonality, RRID, and dilution are not stated.
- **[Antibodies / immunodetection] Ubiquitin antibody vendor + catalog + host/clonality + dilution** — Ubiquitin (CST, #431224) — vendor and catalog present, but host species/clonality, RRID, and dilution are not stated.
- **[Model organisms / in vivo] IACUC protocol number** — Methods state 'protocols were in accordance with the IACUC' but no IACUC approval/protocol number is given.
- **[Model organisms / in vivo] Randomization / blinding statement** — No statement of randomization of animals to groups or blinding during analysis is provided.
- **[Human subjects / clinical] IRB approval** — Human post-mortem hippocampi obtained from Shiley-Marcos ADRC (UCSD), but no IRB approval statement is provided.
- **[Human subjects / clinical] Informed consent** — No statement of informed consent for the post-mortem human tissue is provided.
- **[Human subjects / clinical] Inclusion/exclusion criteria** — AD vs non-AD classification and AsymAD vs 'normal' subgroups are described, but explicit inclusion/exclusion criteria for case selection are not stated.
- **[Mass spectrometry] Precursor/fragment mass tolerances** — No precursor or fragment mass tolerance is stated for the database search.
- **[Mass spectrometry] Repository accession (PRIDE/MassIVE)** — No PRIDE/MassIVE (or other) repository accession is provided for the raw MS data or processed results.

## Unverifiable (raise as questions)
- **[Chemicals / drugs / dosing] AHA diet identity + concentration + schedule** — AHA pellets prepared by Inotiv 'as previously described17' (ref 17, McClatchy 2015 PALM). Route (ad libitum) and schedule (4 days AHA, 7 days chase) are given, but the AHA concentration in the diet is not stated and depends on the cited protocol, whose contents cannot be confirmed from the manuscript alone.
- **[Chemicals / drugs / dosing] Biotin-alkyne DADPS identity + concentration** — Click reactions 'performed as previously described with the biotin-alkyne DADPS18' (ref 18). Reaction conditions/time given (1h 30C, overnight 4C) but reagent concentration is not stated and depends on the cited protocol.
- **[Protocol provenance] AHA pellet preparation 'as previously described17'** — Delegated to ref 17 (McClatchy et al. 2015, J Proteome Res, DOI 10.1021/acs.jproteome.5b00653). Specific and resolvable; contents cannot be confirmed from the manuscript alone. This is a load-bearing reagent (AHA diet) whose concentration is not stated in the manuscript.
- **[Protocol provenance] Click reaction 'as previously described with biotin-alkyne DADPS18'** — Delegated to ref 18 (McClatchy et al. 2024, J Proteome Res, DOI 10.1021/acs.jproteome.4c00616). Resolvable citation; reagent concentration not confirmable from manuscript alone.
- **[Protocol provenance] Immunoblot development 'as previously described24'** — Delegated to ref 24 (McClatchy et al. 2018, ACS Chem Neurosci, DOI 10.1021/acschemneuro.8b00284). Resolvable; contents not confirmable from manuscript alone.
- **[Protocol provenance] Immunoblot quantitation 'as previously described7'** — Delegated to ref 7 (McClatchy et al. 2012, J Proteome Res, DOI 10.1021/pr201176v). Resolvable; contents not confirmable from manuscript alone.

## SOFT gaps — recommended
- **[Cross-cutting] Data-availability statement** — No data-availability statement appears in the manuscript; raw MS data and supplementary tables are referenced but no repository accession or deposition statement is given.
- **[Cross-cutting] Code availability for custom analysis** — Custom/bioinformatic analysis was performed (WGCNA via MetaNetwork, PACOM, Webgestalt, Cytoscape networks) but no code-availability statement or repository link is provided.
- **[Human subjects / clinical] Funding / COI statement** — No funding or conflict-of-interest statement is present in the manuscript.
- **[Computational / bioinformatics] Code availability** — Custom/bioinformatic pipelines (WGCNA, PACOM, network analysis) were used but no code repository or availability statement is given.

## Documented (for the record)
- **[Cross-cutting] Sample size n with what n represents** — Human: 13 AD and 14 non-AD post-mortem hippocampi (Methods). Mouse: 'Each biological replicate(N=4) for the Day7 samples were pooled from one male and one female mouse cortex'; Day0 samples pooled per genotype. n is explicitly biological replicates.
- **[Cross-cutting] Named statistical test** — ANOVA (ProteomeDiscoverer 2.5, human), Student t-test (mouse Day7/Day0), one-way ANOVA with Tukey's multiple comparison test (Fig 8E/F), Pearson correlation (Braak), WGCNA module eigenprotein comparisons.
- **[Cross-cutting] Software/tool/instrument versions** — ProteomeDiscoverer 2.5; Uniprot mouse v2024-01-24 and human v2022-08-03; Webgestalt 2017/2024; PACOM; Cytoscape; Prism Graphpad; Orbitrap Eclipse; EasynLC 1200. MetaNetwork is cited (ref 19) without an explicit version.
- **[Antibodies / immunodetection] Abeta ELISA kit vendor + catalog + application + dilution** — Abeta 1-42 Human Ultrasensitive Elisa (# KHB3544; ThermoFisher). Application (ELISA) and sample dilutions given for mouse (undiluted, 1:4, 1:100). Kit-based, so host/clonality not applicable.
- **[Model organisms / in vivo] Species + strain + source/RRID** — B6.C3-Tg (APPswe,PSEN1dE9)85Dbo/Mmjax; #034829-JAX from Jackson Laboratories; bred with C57BL/6 from Scripps breeding colony. JAX stock number given (RRID not stated).
- **[Model organisms / in vivo] Genotype and background** — APPswePS1delta9 hemizygote transgenics on B6.C3 background; WT littermates used as controls.
- **[Model organisms / in vivo] Sex** — 'Both females and male mice were used for this study'; Day7 replicates pooled from one male and one female.
- **[Model organisms / in vivo] Age** — Mice analyzed at 2, 5, and 12 months.
- **[Model organisms / in vivo] n per group** — N=4 biological replicates per genotype/timepoint/fraction (Day7), each pooled from one male + one female.
- **[Model organisms / in vivo] Housing conditions** — Housed in plastic cages in temperature/humidity-controlled colony, reversed day/night cycle, AAALAC-approved facility.
- **[Human subjects / clinical] Participant demographics** — Table S1 provides metadata including age, gender, and pathology report; Abeta42 ELISA confirms classification (Fig S1A).
- **[Chemicals / drugs / dosing] TMT labeling reagent + amount** — TMT 16plex 0.5mg vials, 25ug TMT added per sample, two rounds of 30-min incubation; hydroxylamine quench. Concentrations of TCEP (5mM), CAA (10mM), trypsin (1ug) stated.
- **[Mass spectrometry] Instrument + acquisition mode** — Orbitrap Eclipse Tribrid, data-dependent mode, MS3 SPS multinotch for TMT reporter ions, CID in ion trap, 120k MS1 resolution, 180-min gradient, EasynLC 1200.
- **[Mass spectrometry] Search engine + version** — ProteomeDiscoverer 2.5.
- **[Mass spectrometry] Database + version** — Uniprot mouse protein database with isoforms (v2024-01-24) and Uniprot human protein database with isoforms (v2022-08-03), plus common contaminants list.
- **[Mass spectrometry] FDR + modifications** — 1% FDR via reverse decoy database; static TMT on Lys/N-term (+304.2071), Cys carbamidomethylation (+57.021464); differential Met oxidation (+79.0711) for DADPS in mouse analysis.
- **[Computational / bioinformatics] Analysis software + versions** — MetaNetwork (ref 19) for WGCNA, Webgestalt for GO enrichment, PACOM (ref 21) for fraction uniqueness, Cytoscape for networks, Prism/Excel for statistics. Webgestalt versions cited (2017/2024); MetaNetwork version not specified.