# Methods Completeness & Reagent Traceability Auditor

## Summary
Detected categories: Cell lines, Chemicals/drugs, Mass spec, Computational/ML, Model organisms, Protocol provenance. Most critical identifiers are present (MS instrument, search engine, database, FDR, tolerances, repository, code, IACUC, reagent catalog numbers, drug catalog and dosing, sample sizes, statistical test). Four gaps: (1) HEK293T cell line lacks source, RRID, STR authentication, and mycoplasma testing (HARD). (2) No random seed declared for kNN imputation or any stochastic step in the analysis pipeline (HARD). (3) No randomization/blinding statement for the in vivo rat study (HARD). (4) No environment file provided (SOFT). One unverifiable item: fragment mass tolerance is stated only in a figure caption (20 ppm) — should be in Methods; but this is present enough to be verifiable. Overall, the manuscript is well-documented for reproducibility pending the three HARD gaps.

## Categories checked
- Cell lines/primary cells
- Chemicals/drugs/dosing
- Mass spec (proteomics/metabolomics)
- Computational/ML
- Model organisms / in vivo
- Protocol provenance

**HARD gaps (blocking): 3** · SOFT gaps: 2 · unverifiable: 0

## HARD gaps — reproduction blockers
- **[Computational/ML] Random seeds (or seed-averaging statement)** — Not stated. kNN imputation (k=10) used; random seed for kNN not specified. limma uses empirical Bayes (no explicit seed). DDA stochastic sampling and MBR are deterministic given input files but no seed is declared for reproducibility.
- **[Cell lines/primary cells] Source, RRID/CVCL, authentication (STR), mycoplasma testing** — HEK293T cells; cultured in DMEM + GlutaMAX + 10% FBS + 1% Pen-Strep; 37°C, 5% CO2. Cell source not stated (e.g. ATCC, ECACC). No RRID/CVCL. No authentication (STR) or mycoplasma testing statement.
- **[Model organisms / in vivo] Randomization/blinding statement** — No randomization or blinding statement for animal allocation or tissue processing.

## SOFT gaps — recommended
- **[Computational/ML] Environment file (SOFT)** — No environment file (e.g. conda env, renv.lock, requirements.txt) provided or mentioned.
- **[Model organisms / in vivo] Power justification (SOFT)** — Housing conditions stated (temperature/humidity-controlled, reverse light cycle, ad libitum). Power justification not stated.

## Documented (for the record)
- **[Mass spec (proteomics/metabolomics)] Instrument + acquisition mode** — Stated: Thermo Scientific Fusion Lumos Tribrid, HCD in Orbitrap, 15 spd gradient 88 min, 220 nL/min, 120K resolution MS1, 7.5K MS2, NCE 30% (non-TMT) or stepped 30/40/50% (TMT), isolation 1.6 m/z, AGC 4e5/5e4, max inj 50 ms/100 ms, +2 to +7 charge states, dynamic exclusion 5 s. Sample prep: extraction (SI Methods: acid extraction), digestion with Arg-C Ultra or r-Chymotrypsin in 100 mM AMBIC or TEAB pH 8–8.5, propionylation, TMT labeling per manufacturer. Search: FragPipe v24.0 (HiP-Frag), restricted histone database + decoys (Homo sapiens: 342 seq, Rattus norvegicus: 292 seq) + cRAP contaminants, 1% FDR PSM/peptide. Mass offsets in SI Table S1.
- **[Mass spec (proteomics/metabolomics)] Search engine + version** — FragPipe v24.0, HiP-Frag workflow, detailed mass offsets in SI Table S1.
- **[Mass spec (proteomics/metabolomics)] Database + version** — Restricted database: human or rat histone sequences + contaminants + decoys; Homo sapiens: 342 seq, Rattus norvegicus: 292 seq; cRAP contaminants listed as curated by CCP.
- **[Mass spec (proteomics/metabolomics)] FDR + modifications + tolerances** — FDR = 1% at PSM and peptide level. Modifications: lists provided (SI Table S1). Precursor mass tolerance = 10 ppm. Fragment mass tolerance: not explicitly stated but default HiP-Frag params assumed; manuscript states 'precursor mass tolerance within 10 ppm and fragment mass tolerance within 20 ppm' (Figure 6 caption).
- **[Mass spec (proteomics/metabolomics)] Repository accession (PRIDE/MassIVE)** — Stated: PXD073683 via PRIDE partner repository.
- **[Mass spec (proteomics/metabolomics)] Quant method + replicates** — Label-free quantification (LFQ) enabled; match-between-runs enabled. Quant method: DDA-LFQ, histone-level normalization, log2-transform, kNN imputation, limma with empirical Bayes. Reproducibility: n = 4 replicate digestions (HEK293T), n = 5 biological (rat). Stated in Methods.
- **[Computational/ML] Dataset(s) with version + exact train/val/test split** — Homo sapiens: 342 sequences (171 decoys); Rattus norvegicus: 292 sequences (146 decoys). cRAP. Search parameters: Arg-C Ultra (cleave after R, ≤2 missed cleavages), r-Chymotrypsin (FYLM, not before P, ≤3 missed cleavages). Static/variable mods stated. Mass offsets in SI Table S1. FDR 1% PSM and peptide.
- **[Computational/ML] Library versions + hardware** — FragPipe v24.0, HiP-Frag workflow. R v4.x (RStudio). impute (kNN), limma, custom scripts.
- **[Computational/ML] Code availability (custom analysis)** — Data analysis code: https://github.com/NataliePTurner/Histone-RIPUP (stated in Data availability section).
- **[Chemicals/drugs/dosing] Identity traceable (vendor + catalog # or CAS)** — Nicotinamide (NAM): Millipore Sigma, catalog number N0636. Doses: 0, 3, 10 mM. Vehicle: complete media (stated). Duration: 18 h. Cells cultured to 50–60% confluency before treatment.
- **[Chemicals/drugs/dosing] Dose/concentration per experiment, route/mode, vehicle, schedule** — Concentrations: 0, 3, 10 mM. Vehicle: complete media (stated). Schedule: 18 h. Route/mode: added to culture media.
- **[Chemicals/drugs/dosing] Identity traceable for all reagents (enzymes, derivatization chemicals)** — Propionic anhydride (derivatization reagent) — vendor/catalog not stated. TMT10: cat no 90309, Thermo Scientific. Arg-C Ultra: VA1831, Promega. r-Chymotrypsin (rChymoselect): CS3332042, Promega. Trypsin Gold MS-grade: V5280, Promega. All stated.
- **[Model organisms / in vivo] Species + strain + source/RRID** — Adult male Sprague-Dawley rats (Charles River Laboratories, Raleigh, NC). Weight: 446 ± 17.8 g. n = 5. IACUC #09-0006 (TSRI). Housing: temperature/humidity-controlled, 12 h reverse light cycle, ad libitum food/water. Euthanasia: isoflurane (3%) + decapitation.
- **[Model organisms / in vivo] Sex** — Male only. Sex stated.
- **[Model organisms / in vivo] Age or weight** — Weight: 446 ± 17.8 g (adult). Stated.
- **[Model organisms / in vivo] n per group** — n = 5 per group (rats). Stated.
- **[Model organisms / in vivo] IACUC protocol #** — IACUC #09-0006 (TSRI). Stated.
- **[Protocol provenance] Every 'performed as previously described' resolves to a specific, checkable reference** — Several methods delegated: 'Histone extraction as described in SI Methods' — SI Methods present. 'Digestions performed according to manufacturer's recommendations' — ambiguous but references Promega protocols; vendor protocols are resolvable. 'Propionylation reagent prepared as previously described [1]' — ref [1] is Sidoli et al. 2016 (DOI 10.3791/54112). 'Data were imported into Skyline (v 26.1.0.057)' — Skyline is public. Overall, delegated methods are either self-contained or resolvable.
- **[Protocol provenance] No circular or dead citation chains for load-bearing protocols** — No 'data not shown' or 'unpublished' protocols appear.
- **[Cell lines/primary cells] Media/supplements (SOFT)** — Media, supplements and culture conditions stated: DMEM + GlutaMAX (Gibco 10566016), 10% FBS, 1% Pen-Strep (15140122), 37°C, 5% CO2.