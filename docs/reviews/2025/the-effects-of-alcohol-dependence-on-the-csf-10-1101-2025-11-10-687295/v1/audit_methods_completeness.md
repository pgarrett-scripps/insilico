# Methods Completeness & Reagent Traceability Auditor

## Summary
This is an in vivo mouse proteomics study (CSF DIA-MS) comparing alcohol-dependent vs non-dependent mice. Detected checklist categories: cross-cutting items (sample size, statistics/error bars, software versions, data/code availability), Model organisms/in vivo, Mass spectrometry, Chemicals/drugs/dosing, and Protocol provenance. The Antibodies/immunodetection category is NOT triggered (the anti-IL-6R antibody is administered as a therapeutic, not used for detection, and is therefore covered under Chemicals/drugs/dosing). The Computational/ML category is not triggered (no model training; the R/enrichr/STRING analyses are standard bioinformatics, with code availability covered under cross-cutting). Overall the manuscript is strong on reagent traceability (antibody vendor+catalog, strain+source, IACUC #, MS database+version, repository accessions). The main HARD gaps are the absence of animal age (only body weight given), and the absence of any randomization/blinding statement. A formal between-group statistical test is not named (comparisons are detection-based with post-hoc power analysis); error bars are fully described. MS precursor/fragment tolerances are not explicitly stated (DIA-NN does not use classic tolerances). Two load-bearing protocols (CIE-2BC model, FASP sample prep) are delegated to citations whose contents cannot be verified from the manuscript alone and are flagged as unverifiable questions.

## Categories checked
- Cross-cutting (sample size, statistics/error bars, software versions, data/code availability)
- Model organisms / in vivo
- Mass spectrometry (proteomics)
- Chemicals / drugs / dosing
- Protocol provenance

**HARD gaps (blocking): 3** · SOFT gaps: 0 · unverifiable: 2

## HARD gaps — reproduction blockers
- **[Model organisms / in vivo] Age** — Only body weight is given (29.2±1.63 g and 22.4±0.55 g); no age (weeks/months) is stated anywhere in the manuscript. Age is required for reproduction of the in vivo model.
- **[Model organisms / in vivo] Randomization / blinding statement** — No randomization or blinding statement is present. Groups were 'assigned ... with groups matched for baseline ethanol and water consumption', but no randomization/blinding procedure is described.
- **[Mass spectrometry (proteomics)] Tolerances** — No precursor or fragment mass tolerance is stated. DIA-NN does not use classic precursor/fragment tolerances (handled internally), so this may be a non-issue, but it is not documented; flagged for confirmation.

## Unverifiable (raise as questions)
- **[Protocol provenance] CIE-2BC model 'as described 9,10,69,70' resolves to a protocol** — Methods: 'chronic intermittent ethanol vapor-2 bottle choice paradigm (CIE-2BC) as described 9,10,69,70'. Refs 9 (Lopez & Becker 2014), 10, 69 (Patel 2019), 70 (Warden 2020) are plausible published sources, but their contents cannot be confirmed from the manuscript alone. The CIE-2BC model is load-bearing (central to the paper's claims); authors should confirm these citations contain the full protocol.
- **[Protocol provenance] FASP sample prep 'as previously described 71' resolves to a protocol** — Methods/Proteomics Sample Preparation: 'modified filter-aided sample preparation protocol, as previously described 71' (Turner 2022). The full protocol is written out in the manuscript, so this delegation is not load-bearing; the citation's contents cannot be verified from the manuscript alone.

## Documented (for the record)
- **[Cross-cutting] Sample size n with what n represents (biological vs technical)** — Methods/Animals: 'male and female C57BL/6J mice (n = 4 and 5...)'; Results: 'Non-dep (n = 5) and Dep groups (n = 4)'. n = individual mice (biological replicates); CSF collected per mouse.
- **[Cross-cutting] Named statistical test and what error bars represent** — Figure 1a legend fully describes box-and-whiskers (25th/75th percentile, mean X, median line, min/max error bars). Post-hoc power analysis is described (>0.99 large, 0.38 moderate effects). NOTE: no formal inferential test comparing groups is named — group differences are established by detection thresholds (>=2/4 vs <=1/5) rather than a statistical test; flagged for the editor/authors.
- **[Cross-cutting] Software, tool, and instrument versions** — DIA-NN v2.1.0; R; enrichR v3.4; STRING (string-db.org); Skyline v25.1.0.237; Fusion Lumos Tribrid MS; Evosep nano-LC; Agilent 7820A GC/7697A headspace-FID.
- **[Cross-cutting] Data-availability statement** — Supporting Information: raw MS files + sample annotations uploaded to MassIVE, dataset identifier C5GX4573B; final filtered quantitative data in Supplementary File 1.
- **[Cross-cutting] Code availability (custom analysis)** — Supporting Information: 'All R scripts used for data analysis and figure generation can be found at the GitHub repository https://github.com/NataliePTurner/MouseCSF (private until published).' Note: repository is private until publication — confirm it is made public.
- **[Model organisms / in vivo] Species + strain + source/RRID** — Methods/Animals: 'C57BL/6J mice ... obtained from The Jackson Laboratory (Bar Harbor, ME)'. No RRID given (SOFT omission).
- **[Model organisms / in vivo] Genotype and background** — C57BL/6J wild-type background stated (Jackson Laboratory).
- **[Model organisms / in vivo] Sex** — Methods/Animals: 'male and female C57BL/6J mice (n = 4 and 5; 29.2±1.63 g and 22.4±0.55 g, respectively)'; PCA shows sex segregation.
- **[Model organisms / in vivo] n per group** — Non-dep n=5, Dep n=4 (individual mice); stated in Results and Methods.
- **[Model organisms / in vivo] IACUC protocol number** — Methods/Animals: 'approved by The Scripps Research Institute (TSRI) Institutional Animal Care and Use Committee (IACUC #09-0006)'.
- **[Model organisms / in vivo] Housing** — Methods/Animals: 'housed in a temperature- and humidity-controlled room (12 h reverse light cycle) and provided with food and water ad libitum'; singly housed during 2BC sessions.
- **[Model organisms / in vivo] Power justification** — Post-hoc power analysis reported (>0.99 large effects, 0.38 moderate); future n=12-15/group for 0.8 power stated in Limitations.
- **[Mass spectrometry (proteomics)] Instrument + acquisition mode** — Methods/LC-MS/MS: 'Fusion Lumos Tribrid Mass Spectrometer (Thermo Scientific) ... coupled to a Evosep nano-LC system ... in DIA mode'; 60 fixed 10 m/z windows, 300-900 m/z, HCD, orbitrap MS/MS.
- **[Mass spectrometry (proteomics)] Sample prep / digestion / enrichment** — Methods/Proteomics Sample Preparation: modified FASP on Nanosep 30K filters, reduction (DTT), alkylation (iodoacetamide), trypsin digestion overnight at 37 °C, Evotips desalting, 350 ng loaded.
- **[Mass spectrometry (proteomics)] Search engine + version** — Methods/Data analysis: 'searched in DIA-NN v 2.1.0'.
- **[Mass spectrometry (proteomics)] Database + version** — Methods/Data analysis: 'Mus musculus reference proteome (downloaded from Uniprot on 3 March 2025; 21,803 sequences)'; separate Rattus norvegicus search (21,800 entries, 12 Sept 2024).
- **[Mass spectrometry (proteomics)] FDR + modifications** — Methods/Data analysis: 'at 1% FDR'; 'C carbamidomethylation, Ox(M) were enabled'; additional filtering at Q.Value, PG.Q.Value, Global.Q.Value <= 0.01.
- **[Mass spectrometry (proteomics)] Repository accession (PRIDE/MassIVE)** — Supporting Information: MassIVE dataset identifier C5GX4573B; comparator dataset PXD053568 (ProteomeXchange) cited.
- **[Mass spectrometry (proteomics)] Quant method** — Methods/Data analysis: 'diann_maxlfq function from the R package diann' for protein quantities; MBR disabled; detection threshold >=2 replicates per group.
- **[Mass spectrometry (proteomics)] Replicates** — Biological replicates n=4-5 per group (individual mice); no technical replicates stated.
- **[Chemicals / drugs / dosing] Anti-IL-6R antibody identity (vendor + catalog #)** — Methods/CIE-2BC: 'InVivoMAb anti-mouse IL-6R antibody (#BE0047, BioXCell)'.
- **[Chemicals / drugs / dosing] Anti-IL-6R antibody dose / route / schedule** — Methods: 'injected ... intraperitoneally (200 microgram/day) for 7 consecutive days'; first injection 24 h after last vapor exposure; CSF collected 2-4 h post final injection.
- **[Chemicals / drugs / dosing] Ethanol + pyrazole dose / route / schedule** — Methods: dependent mice injected i.p. with '1.75 g/kg ethanol + 68.1 mg/kg pyrazole (Sigma, St Louis, MO)'; Non-dep with 68.1 mg/kg pyrazole; BELs 150-250 mg/dL; 6 cycles of 4 days CIE + 3 days abstinence + 5 days 2BC + 2 days abstinence.
- **[Protocol provenance] Deviations from cited protocols stated** — FASP is described as a 'modified' protocol and the modifications are written out in full; no other deviations flagged.