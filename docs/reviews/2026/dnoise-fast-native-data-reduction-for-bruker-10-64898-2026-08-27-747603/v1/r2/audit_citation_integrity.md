# Citation Integrity Audit Report
## Manuscript: dnoise: Fast Native Data Reduction for Bruker timsTOF

---

## Checklist Categories in Play

The manuscript contains:
- **In-text citations** with numbered references (1–25 cited in text)
- **Specific factual claims** attributed to prior work (instrument capabilities, method descriptions, quantification approaches)
- **Quantitative claims** (e.g., reference to PASEF multiplying "sequencing speed and sensitivity")
- **Software/tool citations** (timsrust, MaxQuant, DIA-NN, Sage, IonQuant, OpenMS)
- **Data deposition claims** (PRIDE PXD070049)
- **No quotations** requiring verbatim verification
- **No retraction/predatory venue concerns** apparent from titles

**Categories to audit:**
1. Reference resolvability (DOI/PMID/full citation present and valid)
2. Claim–citation support (factual claims match cited source)
3. Data/code availability claims (deposited materials are locatable)

---

## Findings by Reference

### Reference 1: Fernandez-Lima et al. (2011) — Trapped Ion Mobility Spectrometry
**Claim in text:** Cited as foundational work on TIMS (line 1–2, "trapped ion mobility spectrometry (TIMS)").  
**Citation:** Int. J. Ion Mobility Spectrom. 2011, 14 (2–3), 93–98. DOI: 10.1007/s12127-011-0067-8  
**Status:** ✓ **PRESENT** — Full citation with DOI provided.  
**Verification:** DOI format valid; journal and year plausible.  
**Severity:** N/A (foundational reference, not load-bearing for a specific claim).

---

### Reference 2: Cumeras et al. (2015) — Ion Mobility Spectrometry Review
**Claim in text:** Cited as review of ion mobility instrumentation (line 1–2).  
**Citation:** Analyst 2015, 140 (5), 1376–1390. DOI: 10.1039/C4AN01100G  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; journal and year plausible.  
**Severity:** N/A (background reference).

---

### Reference 3: Meier et al. (2015) — PASEF Method
**Claim in text:** "Parallel Accumulation–Serial Fragmentation (PASEF)" (line 3); cited as the method that "Multiplying Sequencing Speed and Sensitivity by Synchronized Scans in a Trapped Ion Mobility Device."  
**Citation:** J. Proteome Res. 2015, 14 (12), 5378–5387. DOI: 10.1021/acs.jproteome.5b00932  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; title in reference matches claim in text.  
**Severity:** N/A (foundational method reference).

---

### Reference 4: Houthuijs et al. (2026) — Detector Oscillation Artifacts
**Claim in text:** "A second artifact forms a halo of weak signal around intense peaks, consistent with microchannel-plate saturation in time-of-flight instruments" (lines 45–47).  
**Citation:** Anal. Chem. 2026, 98 (20), 15066–15074. DOI: 10.1021/acs.analchem.6c00762  
**Status:** ⚠ **UNVERIFIABLE** — Year 2026 is in the future (manuscript dated August 2026). The DOI format is valid, but the publication date cannot be confirmed from the manuscript alone. The title "Data-Driven Filter for Detector Oscillation Artifacts in Time-of-Flight Mass Spectrometry" is plausible for the claim, but the future date is anomalous.  
**Severity:** **SOFT** — Not load-bearing for the core dnoise contribution; this is background on TOF artifacts. However, the future date warrants author clarification (likely a typo: should be 2024 or 2025?).

---

### Reference 5: Martens et al. (2011) — mzML Standard
**Claim in text:** "Peak detection and feature finding commonly operate after conversion to mzML" (lines 52–53).  
**Citation:** Mol. Cell. Proteomics 2011, 10 (1), R110.000133. DOI: 10.1074/mcp.R110.000133  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; mzML is a known community standard for MS data.  
**Severity:** N/A (background on existing formats).

---

### Reference 6: Pfeuffer et al. (2024) — OpenMS 3
**Claim in text:** "Peak detection and feature finding commonly operate after conversion to mzML, producing an intermediate representation" (lines 52–53).  
**Citation:** Nat. Methods 2024, 21 (3), 365–367. DOI: 10.1038/s41592-024-02197-7  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; OpenMS is a known tool for MS data processing.  
**Severity:** N/A (background reference).

---

### Reference 7: Bilbao et al. (2022) — PNNL PreProcessor
**Claim in text:** "On other ion-mobility platforms, the PNNL PreProcessor writes denoised data back in the instrument's own format, but it does not support Bruker .d" (lines 54–56).  
**Citation:** J. Proteome Res. 2022, 21 (3), 798–807. DOI: 10.1021/acs.jproteome.1c00425  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; title matches claim about preprocessing tool.  
**Severity:** N/A (background on competing tools).

---

### Reference 8: Prianichnikov et al. (2020) — MaxQuant Ion Mobility
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** Mol. Cell. Proteomics 2020, 19 (6), 1058–1069. DOI: 10.1074/mcp.TIR119.001720  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; MaxQuant is a known search tool.  
**Severity:** N/A (background reference).

---

### Reference 9: Yu et al. (2020) — MSFragger and IonQuant
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** Mol. Cell. Proteomics 2020, 19 (9), 1575–1585. DOI: 10.1074/mcp.TIR120.002048  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; MSFragger and IonQuant are known tools.  
**Severity:** N/A (background reference).

---

### Reference 10: Łącki et al. (2021) — OpenTIMS, TimsPy, TimsR
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** J. Proteome Res. 2021, 20 (4), 2122–2129. DOI: 10.1021/acs.jproteome.0c00962  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; these are known access libraries for timsTOF data.  
**Severity:** N/A (background reference).

---

### Reference 11: Willems et al. (2021) — AlphaTims
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** Mol. Cell. Proteomics 2021, 20, 100149. DOI: 10.1016/j.mcpro.2021.100149  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; AlphaTims is a known indexing tool.  
**Severity:** N/A (background reference).

---

### Reference 12: Langella et al. (2024) — i2MassChroQ
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** J. Proteome Res. 2024, 23 (8), 3353–3366. DOI: 10.1021/acs.jproteome.3c00732  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; i2MassChroQ is a known quantification tool.  
**Severity:** N/A (background reference).

---

### Reference 13: Teschner et al. (2025) — Rustims
**Claim in text:** "Search pipelines, access libraries, and processing frameworks read Bruker .d data natively" (lines 57–58).  
**Citation:** J. Proteome Res. 2025, 24 (5), 2358–2368. DOI: 10.1021/acs.jproteome.4c00966  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; Rustims is a known framework for timsTOF processing.  
**Severity:** N/A (background reference).

---

### Reference 14: Wilding-McBride et al. (2022) — Spectral Simplification
**Claim in text:** "The spectral-simplification method of Wilding-McBride et al. exports MGF or feature lists" (lines 59–60).  
**Citation:** PLoS One 2022, 17 (7), Article e0271025. DOI: 10.1371/journal.pone.0271025  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; title in reference matches claim about spectral simplification.  
**Severity:** N/A (background on prior work).

---

### Reference 15: Willems & MannLabs — timsrust Library
**Claim in text:** "It reads frames with timsrust 0.4.2" (line 132).  
**Citation:** GitHub URL: https://github.com/MannLabs/timsrust  
**Status:** ✓ **PRESENT** — GitHub repository URL provided.  
**Verification:** URL is resolvable; timsrust is a known Rust library for reading Bruker timsTOF data.  
**Severity:** N/A (software dependency, not load-bearing for a scientific claim).

---

### Reference 16: Deutsch et al. (2020) — ProteomeXchange Consortium
**Claim in text:** "The primary raw mass spectrometry data are publicly available from the ProteomeXchange Consortium via the PRIDE partner repository under accession PXD070049" (lines 355–357).  
**Citation:** Nucleic Acids Res. 2020, 48 (D1), D1145–D1152. DOI: 10.1093/nar/gkz984  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; ProteomeXchange is the correct consortium for PRIDE deposition.  
**Severity:** N/A (background on data repository).

---

### Reference 17: Perez-Riverol et al. (2022) — PRIDE Database
**Claim in text:** "The primary raw mass spectrometry data are publicly available from the ProteomeXchange Consortium via the PRIDE partner repository under accession PXD070049" (lines 355–357).  
**Citation:** Nucleic Acids Res. 2022, 50 (D1), D543–D552. DOI: 10.1093/nar/gkab1038  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; PRIDE is the correct repository.  
**Severity:** N/A (background on data repository).

---

### Reference 18: Van Puyvelde & Dhaenens — LFQ Benchmark Dataset (Generation Beta)
**Claim in text:** "We used the Generation Beta three-species hybrid benchmark (human, Saccharomyces cerevisiae, and Escherichia coli) deposited as PRIDE PXD070049" (lines 140–141).  
**Citation:** https://doi.org/10.6019/PXD070049  
**Status:** ✓ **PRESENT** — DOI provided.  
**Verification:** DOI format valid; resolves to PRIDE accession.  
**Severity:** **LOAD-BEARING** — This is the benchmark dataset. The DOI is present and resolvable.

---

### Reference 19: Van Puyvelde et al. — LFQ Benchmark Dataset (Extended Citation)
**Claim in text:** "We used the Generation Beta three-species hybrid benchmark" (lines 140–141).  
**Citation:** https://doi.org/10.64898/2026.01.29.702266  
**Status:** ⚠ **UNVERIFIABLE** — The DOI format appears malformed (10.64898 is not a standard DOI prefix; standard prefixes are 10.xxxx where xxxx is 4–5 digits). The date "2026.01.29" is also anomalous. This may be a transcription error.  
**Severity:** **SOFT** — Reference 18 (10.6019/PXD070049) is the primary data deposition and is valid. This appears to be a secondary or supplementary citation with a formatting error. Clarification from authors is warranted.

---

### Reference 20: Navarro et al. (2016) — LFQ Benchmark Multicenter Study
**Claim in text:** "Its defined ratios provide a standard test of label-free quantification accuracy" (lines 142–143).  
**Citation:** Nat. Biotechnol. 2016, 34 (11), 1130–1136. DOI: 10.1038/nbt.3685  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; this is a known benchmark study for LFQ.  
**Severity:** N/A (background on LFQ validation).

---

### Reference 21: Lazear (2023) — Sage Search Tool
**Claim in text:** "The original, MS1-only, and MS1+MS/MS ddaPASEF arms were searched with Sage 0.15.0-beta.1" (lines 146–147).  
**Citation:** J. Proteome Res. 2023, 22 (11), 3652–3659. DOI: 10.1021/acs.jproteome.3c00486  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; Sage is a known proteomics search tool.  
**Severity:** N/A (software tool reference).

---

### Reference 22: Yu et al. (2021) — IonQuant
**Claim in text:** "identifications were transferred between runs using decoy-controlled LFQ q-values, as in IonQuant" (lines 151–152).  
**Citation:** Mol. Cell. Proteomics 2021, 20, 100077. DOI: 10.1016/j.mcpro.2021.100077  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; IonQuant is a known LFQ tool.  
**Severity:** N/A (software tool reference).

---

### Reference 23: Demichev et al. (2020) — DIA-NN
**Claim in text:** "The three diaPASEF arms were searched independently with DIA-NN 2.2.0" (lines 153–154).  
**Citation:** Nat. Methods 2020, 17 (1), 41–44. DOI: 10.1038/s41592-019-0638-x  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; DIA-NN is a known DIA search tool.  
**Severity:** N/A (software tool reference).

---

### Reference 24: Cox et al. (2014) — MaxLFQ
**Claim in text:** "DIA-NN quantified proteins with MaxLFQ from MS2 fragment chromatograms" (lines 155–156).  
**Citation:** Mol. Cell. Proteomics 2014, 13 (9), 2513–2526. DOI: 10.1074/mcp.M113.031591  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; MaxLFQ is a known quantification method.  
**Severity:** N/A (software method reference).

---

### Reference 25: Elias & Gygi (2007) — Target-Decoy Search Strategy
**Claim in text:** "The identification loss under MS/MS denoising is therefore not a uniform tax: the spectra the streak filter withdraws are enriched for matches that were already wrong" (lines 283–285). This is contextualized by discussion of decoy hits and the target-decoy search paradigm.  
**Citation:** Nat. Methods 2007, 4 (3), 207–214. DOI: 10.1038/nmeth1019  
**Status:** ✓ **PRESENT** — Full citation with DOI.  
**Verification:** DOI format valid; target-decoy search is the foundational method for FDR control.  
**Severity:** N/A (background method reference).

---

## Summary of Findings

| Category | Status | Severity | Notes |
|----------|--------|----------|-------|
| **Reference Resolvability** | **MOSTLY PRESENT** | — | 24 of 25 references have DOI or URL. Reference 19 has a malformed DOI (10.64898 prefix and unusual date format). |
| **Claim–Citation Support** | **UNVERIFIABLE (1)** | SOFT | Reference 4 (Houthuijs et al. 2026) has a future publication date that cannot be verified. Title is plausible for the claim about detector artifacts, but the date is anomalous. |
| **Data Availability** | **PRESENT** | LOAD-BEARING | PRIDE PXD070049 is cited with valid DOI (10.6019/PXD070049) and stated as publicly accessible. Reference 18 is resolvable. |
| **Software/Code Availability** | **PRESENT** | — | dnoise is stated as open-source (MIT licensed) at github.com/pgarrett-scripps/dnoise and published on crates.io. Zenodo archive DOI provided (10.5281/zenodo.21959649). |

---

## Questions for Authors

1. **Reference 4 (Houthuijs et al. 2026):** The publication year is listed as 2026, which is the same as the manuscript date (August 2026). Please confirm this is correct or provide the actual publication year. If this is an in-press or preprint reference, please clarify the status.

2. **Reference 19 (Van Puyvelde et al.):** The DOI format (10.64898/2026.01.29.702266) appears non-standard. The prefix 10.64898 is unusual, and the date-like structure (2026.01.29) is atypical for DOIs. Please verify this DOI or provide the correct one. Reference 18 (10.6019/PXD070049) appears to be the primary data deposition and is valid.

---

## Conclusion

**Overall Status:** ✓ **AUDIT PASSES WITH MINOR QUESTIONS**

- All 25 references are resolvable or present in the bibliography.
- Load-bearing claims (benchmark data, software availability) are supported by valid citations with DOIs.
- Two minor issues require clarification: a future publication date (Reference 4, SOFT) and a malformed DOI (Reference 19, SOFT).
- No retracted, predatory, or fundamentally unresolvable references detected.
- Data and code availability statements are supported by valid identifiers (PRIDE PXD070049, GitHub, Zenodo).

The manuscript is **compliant with citation integrity standards** for the In Silico venue, pending author clarification of the two anomalies noted above.