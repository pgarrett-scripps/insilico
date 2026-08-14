# Methods Completeness & Reagent Traceability Auditor

## Summary
This is a bioprocess/cGMP manufacturing manuscript (CHO cell line development, upstream/downstream process, viral clearance, product characterization) for an HIV Env trimer vaccine candidate. The manuscript is unusually thorough on process parameters (media, feeds, column chemistries, buffers, hold times, step yields) and on protocol provenance (the downstream process is described in full and anchored to Dey et al. 2018; glycan and EM methods cite resolvable references). The main completeness gaps cluster in reagent/biological traceability: detection/capture antibodies lack catalog/RRID/clonality; the parental CHO line lacks RRID, STR authentication and mycoplasma testing; the expression constructs and verification primers lack sequences or a depository accession; and the mass-spec section lacks repository accessions, search-engine/database versions and tolerances. Cross-cutting items (software versions, data-availability and code-availability statements) are also absent. No in vivo or human-subjects experiments are performed in this manuscript (macaque and HVTN144 data are cited prior/ongoing work), so those categories were not scored as gaps.

## Categories checked
- Cross-cutting (n, statistics, software versions, data/code availability)
- Antibodies/immunodetection
- Cell lines
- Chemicals/drugs/dosing
- Oligos/plasmids/constructs
- Genomics/sequencing
- Mass spec (proteomics/glycoproteomics)
- Microscopy/imaging (negative-stain EM)
- Protocol provenance

**HARD gaps (blocking): 19** · SOFT gaps: 3 · unverifiable: 1

## HARD gaps — reproduction blockers
- **[Antibodies/immunodetection] PGT145 detection antibody (BLI/Octet trimer titer)** — Used throughout (Sections 2.1.2, 3.1.1-3.1.3, 3.2.2) at 10 µg/mL. No vendor, catalog #, clone, RRID, or host species/clonality given. Only concentration (10 µg/mL) is stated.
- **[Antibodies/immunodetection] BG18_GL0 detection antibody (BLI/Octet)** — Used for trimer titer and clone ranking (Sections 2.1.2, 3.1.2, 3.1.3). No vendor, catalog #, clone, RRID, or clonality given.
- **[Antibodies/immunodetection] DEN3 negative-control antibody** — Used as negative control in BLI assay (Section 2.1.2), cited to Steichen et al. 2019 but no vendor/catalog/RRID/clonality in this manuscript.
- **[Antibodies/immunodetection] 2G12 capture antibody (affinity chromatography) and residual-2G12 ELISA** — Vendor given as 'Polymun Scientific, Austria' (Sections 2.5.4.1, 2.2.7) but no catalog #, clone, RRID, or clonality. Residual 2G12 ELISA (2.2.7) uses Protein A capture and an unspecified secondary antibody with no identifiers.
- **[Antibodies/immunodetection] CHO HCP ELISA antibodies** — Section 2.2.4: 'third-generation CHO HCP ELISA kit (Cygnus Technologies)' — kit catalog # and antibody details not given.
- **[Cell lines] Cell line RRID/CVCL identifier** — HD BIOP3 and clone C235 are named but no RRID/CVCL accession is provided for the parental line or the production clone.
- **[Cell lines] Authentication (STR profiling)** — No STR or other identity-authentication statement for HD BIOP3 or clone C235 is present.
- **[Cell lines] Mycoplasma testing** — No mycoplasma testing statement for the parental line, RCB, or MCB is present anywhere in the manuscript.
- **[Oligos/plasmids/constructs] N332-GT5 gp140 coding sequence** — Section 2.3.3: 'codon-optimized coding sequence' for N332-GT5 gp140 — the sequence is not provided and no GenBank/Addgene/depository accession is given. This is the central product of the paper.
- **[Oligos/plasmids/constructs] Human furin ORF sequence** — Section 2.3.3: codon-optimized human furin ORF co-expressed for cleavage — sequence not provided, no accession.
- **[Oligos/plasmids/constructs] Plasmid/vector source (Addgene # or full description)** — Leap-In1 transposon backbone and GS cassette described (Section 2.3.3) but no Addgene #, depository, or full vector map/sequence is given.
- **[Oligos/plasmids/constructs] Primer sequences for transcript/Sanger verification** — Section 2.1.3: RT-PCR and Sanger sequencing of N332 and furin messages use 'gene-specific primers' — primer sequences are not provided.
- **[Mass spec (proteomics/glycoproteomics)] Repository accession (PRIDE/MassIVE)** — DeGlyPHER and LC-MS glycoproteomics data (Section 2.7.1, Figures 17-18) have no PRIDE/MassIVE or other repository accession.
- **[Mass spec (proteomics/glycoproteomics)] Search engine versions (ProLuCID, Byos)** — Section 2.7.1 names ProLuCID and Byos but gives no version numbers.
- **[Mass spec (proteomics/glycoproteomics)] Database + version (CHO proteome background)** — Section 2.7.1: searched 'against the known protein sequence of N332-GT5 within a CHO proteome background' — the CHO database and its version are not specified.
- **[Mass spec (proteomics/glycoproteomics)] Precursor/fragment mass tolerances** — Section 2.7.1 gives FDR (1%) and static/variable modifications but no precursor or fragment mass tolerance values.
- **[Microscopy/imaging (negative-stain EM)] Analysis software versions (Leginon, CryoSPARC)** — Section 2.7.2 names Leginon and CryoSPARC (Blob Picker, 2D classification) but gives no software versions.
- **[Cross-cutting] Named statistical test and error-bar definition** — No inferential statistical test is named anywhere. Error bars are described as SEM in glycan figures (Figure 17-18) and SD in some tables (e.g., '58.9±1.3'), but the manuscript never states which statistic each error bar represents or which test (if any) was applied.
- **[Cross-cutting] Software/tool/instrument versions** — Many tools lack versions: CryoSPARC, Leginon, ProLuCID, Byos, IP2, DTASelect2, Census2, GlycoMSQuant, CFX Manager, SoloVPE, Octet/ForteBio system. Instruments are named but versions/firmware are not.

## Unverifiable (raise as questions)
- **[Protocol provenance] Antibody provenance (DEN3, PGT145, BG18_GL0)** — Antibodies are attributed to Steichen et al. 2019 (Science, DOI given) but the manuscript does not state whether the antibody reagents themselves (clone, source) are described in that reference; this cannot be confirmed from the manuscript alone.

## SOFT gaps — recommended
- **[Genomics/sequencing] Sequencing platform/mode and accession** — Section 2.1.3: transcript verification by Sanger chemistry with 100% double-stranded coverage; platform and primer sequences not given and no sequence accession deposited. This is a QC step, not a primary dataset.
- **[Cross-cutting] Data-availability statement** — No data-availability statement is present; mass-spec data have no repository accession and no statement about where raw data can be obtained.
- **[Cross-cutting] Code availability (custom analysis)** — Custom analysis pipelines are used (DeGlyPHER, GlycoMSQuant, ProLuCID search) but no code availability statement or repository link is given.

## Documented (for the record)
- **[Cell lines] Parental cell line source** — Section 2.3.1: 'HD BIOP3 is a GS-null cell line derived from ECACC CHOK1 established by Horizon Discovery.' Source and derivation stated.
- **[Cell lines] Media/supplements** — Media and feeds are specified: EX-CELL AFB (SAFC), Dynamis (Thermo Fisher), Cell Boost 7a/7b (Cytiva), Cellvento 4, Advanced CHO Feed, Cellboost 7, antifoam 10% ADCF, 1 M sodium carbonate.
- **[Chemicals/drugs/dosing] Reagent traceability (vendor + catalog #)** — Most reagents carry vendor and catalog # (e.g., NuPAGE buffers NP0008/NP0009, gels NP0329BOX, InstantBlue ISB1L-1L, NEM E3876-5G, TSKgel UltraSW 22856, Acquity C4 186004497, ZORBAX C8 865750-906, Kinetics Buffer 18-1105). Common buffers (Tris, NaCl, MgCl2, Triton X-100) are named without catalog #, acceptable for standard reagents.
- **[Mass spec (proteomics/glycoproteomics)] Instrument + acquisition mode; FDR; modifications** — Instruments given (Q Exactive HF-X, Orbitrap Eclipse), data-dependent HCD acquisition, 1% spectrum-level FDR, and static/variable modifications (C+57.02146, N+2.988261, N+203.079373, M+15.994915, N-term Q-17.026549) are stated.
- **[Microscopy/imaging (negative-stain EM)] Instrument, detector, acquisition settings** — Section 2.7.2: FEI Tecnai Spirit TEM, FEI Eagle 4K CCD, 120 keV, 2.06 Å pixel size, 52,000× nominal magnification, 82 micrographs, 6,086 particles, 2% uranyl formate stain.
- **[Cross-cutting] Sample size n and what it represents** — n values are stated in many places (213 clones, 56, 24, 12 Ambr250 bioreactors, 82 micrographs, 6,086 particles, 8 macaques in cited prior work). However, biological vs technical replicate identity is not always explicit (e.g., glycan abundance means).
- **[Protocol provenance] Downstream process basis (BG505 SOSIP.664)** — Section 2.5: 'developed based on the process established for BG505 SOSIP.664 (Dey et al., 2018)' — Dey et al. 2018 (Biotechnol Bioeng, DOI 10.1002/bit.26498) is resolvable and the final process is additionally described in full (Section 2.5.4), so it is self-contained with provenance.
- **[Protocol provenance] Glycan analysis methods (DeGlyPHER, LC-MS)** — DeGlyPHER cites Baboo et al. 2021/2023 (DOIs given); LC-MS glycoproteomics cites Watanabe 2020, Behrens 2017, Cao 2017, Go 2017 — all resolvable and the methods are also summarized in-text.
- **[Protocol provenance] nsEM comparison references** — nsEM results compared to Dey et al. 2018 and Bale et al. 2025 (npj Vaccines) — resolvable journal references.
- **[Protocol provenance] HVTN144 trial registration** — Ref 10 gives ClinicalTrials.gov Identifier NCT05217641 for HVTN144; resolvable. (This manuscript reports manufacturing, not clinical outcomes, so IRB/consent/demographics are not applicable to its own data.)
- **[Protocol provenance] Any 'as previously described' / '(data not shown)' / '(unpublished)' delegation** — No '(data not shown)', '(unpublished)', or '(in preparation)' citations were found; delegated methods resolve to published, DOI-bearing references. Deviations from the cited BG505 process (removal of preparative SEC) are explicitly stated and justified (Section 3.3.2).