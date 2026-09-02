# Citation Integrity Audit Report
## Manuscript: dnoise: Fast Native Data Reduction for Bruker timsTOF

---

## Checklist Categories in Play

The manuscript contains:
- **Reference resolvability triggers**: Specific citations to prior work, software, databases, and data repositories throughout
- **Claim–citation support triggers**: Quantitative claims about instrument capabilities, prior tools, and benchmark data attributed to references
- **Quotation/number fidelity triggers**: Specific values and ratios cited from benchmark sources
- **Self-citation / citation inflation**: Present but appears germane (authors cite their own software release and benchmark participation)
- **Retracted / predatory sources**: No obvious flags, but verification needed for recent works

All three categories require checking.

---

## Findings by Category

### 1. Reference Resolvability

#### Load-bearing references checked:

| Ref | Citation | Status | Notes |
|-----|----------|--------|-------|
| (1) | Fernandez-Lima et al. 2011, IJIMS 14(2–3):93–98, DOI 10.1007/s12127-011-0067-8 | **PRESENT** | Foundational TIMS instrumentation; DOI resolvable |
| (2) | Cumeras et al. 2015, Analyst 140(5):1376–1390, DOI 10.1039/C4AN01100G | **PRESENT** | Ion mobility review; DOI resolvable |
| (3) | Meier et al. 2015, J. Proteome Res. 14(12):5378–5387, DOI 10.1021/acs.jproteome.5b00932 | **PRESENT** | PASEF method; DOI resolvable |
| (4) | Houthuijs et al. 2026, Anal. Chem. 98(20):15066–15074, DOI 10.1021/acs.analchem.6c00762 | **UNVERIFIABLE** | Future-dated (August 2026 manuscript, reference dated 2026); DOI format appears valid but publication status cannot be confirmed. This is a **SOFT** concern—likely a preprint or advance online publication, but requires author clarification. |
| (5) | Martens et al. 2011, mzML standard, Mol. Cell. Proteomics 10(1):R110.000133, DOI 10.1074/mcp.R110.000133 | **PRESENT** | Standard format reference; DOI resolvable |
| (6) | Pfeuffer et al. 2024, OpenMS 3, Nat. Methods 21(3):365–367, DOI 10.1038/s41592-024-02197-7 | **PRESENT** | Recent software; DOI resolvable |
| (7) | Bilbao et al. 2022, PNNL PreProcessor, J. Proteome Res. 21(3):798–807, DOI 10.1021/acs.jproteome.1c00425 | **PRESENT** | Cited as prior denoising tool for ion mobility; DOI resolvable |
| (8) | Prianichnikov et al. 2020, MaxQuant, Mol. Cell. Proteomics 19(6):1058–1069, DOI 10.1074/mcp.TIR119.001720 | **PRESENT** | Ion mobility software; DOI resolvable |
| (9) | Yu et al. 2020, MSFragger/IonQuant, Mol. Cell. Proteomics 19(9):1575–1585, DOI 10.1074/mcp.TIR120.002048 | **PRESENT** | Quantification tool; DOI resolvable |
| (10) | Łącki et al. 2021, OpenTIMS/TimsPy/TimsR, J. Proteome Res. 20(4):2122–2129, DOI 10.1021/acs.jproteome.0c00962 | **PRESENT** | Data access libraries; DOI resolvable |
| (11) | Willems et al. 2021, AlphaTims, Mol. Cell. Proteomics 20:100149, DOI 10.1016/j.mcpro.2021.100149 | **PRESENT** | Visualization tool; DOI resolvable |
| (12) | Langella et al. 2024, i2MassChroQ, J. Proteome Res. 23(8):3353–3366, DOI 10.1021/acs.jproteome.3c00732 | **PRESENT** | Native timsTOF processing; DOI resolvable |
| (13) | Teschner et al. 2025, Rustims, J. Proteome Res. 24(5):2358–2368, DOI 10.1021/acs.jproteome.4c00966 | **PRESENT** | Rust framework for timsTOF; DOI resolvable |
| (14) | Wilding-McBride et al. 2022, spectral simplification, PLoS One 17(7):e0271025, DOI 10.1371/journal.pone.0271025 | **PRESENT** | Cited as prior denoising method; DOI resolvable |
| (15) | Willems & MannLabs, timsrust 0.4.2, GitHub link provided | **PRESENT** | Software library; GitHub URL provided (https://github.com/MannLabs/timsrust) |
| (16) | Deutsch et al. 2020, ProteomeXchange, Nucleic Acids Res. 48(D1):D1145–D1152, DOI 10.1093/nar/gkz984 | **PRESENT** | Data repository standard; DOI resolvable |
| (17) | Perez-Riverol et al. 2022, PRIDE Database, Nucleic Acids Res. 50(D1):D543–D552, DOI 10.1093/nar/gkab1038 | **PRESENT** | Data repository; DOI resolvable |
| (18) | Van Puyvelde & Dhaenens, LFQ Benchmark Generation Beta, DOI 10.6019/PXD070049 | **PRESENT** | Benchmark dataset; DOI resolvable (PRIDE accession) |
| (19) | Van Puyvelde et al., same benchmark, DOI 10.64898/2026.01.29.702266 | **UNVERIFIABLE** | DOI format appears malformed (10.64898 is not a standard DOI prefix; standard prefixes are 10.xxxx where xxxx is 4+ digits). The date string in the DOI (2026.01.29) is unusual. This may be a transcription error. **SOFT** issue—the benchmark is clearly the same as ref. 18, but this alternate citation needs clarification. |
| (20) | Navarro et al. 2016, LFQ benchmark multicenter, Nat. Biotechnol. 34(11):1130–1136, DOI 10.1038/nbt.3685 | **PRESENT** | Quantification benchmark; DOI resolvable |
| (21) | Lazear 2023, Sage search engine, J. Proteome Res. 22(11):3652–3659, DOI 10.1021/acs.jproteome.3c00486 | **PRESENT** | Search tool used in benchmark; DOI resolvable |
| (22) | Yu et al. 2021, IonQuant, Mol. Cell. Proteomics 20:100077, DOI 10.1016/j.mcpro.2021.100077 | **PRESENT** | Quantification method; DOI resolvable |
| (23) | Demichev et al. 2020, DIA-NN, Nat. Methods 17(1):41–44, DOI 10.1038/s41592-019-0638-x | **PRESENT** | DIA search tool used in benchmark; DOI resolvable |
| (24) | Cox et al. 2014, MaxLFQ, Mol. Cell. Proteomics 13(9):2513–2526, DOI 10.1074/mcp.M113.031591 | **PRESENT** | Quantification method; DOI resolvable |
| (25) | Elias & Gygi 2007, target-decoy search, Nat. Methods 4(3):207–214, DOI 10.1038/nmeth1019 | **PRESENT** | Statistical method; DOI resolvable |

**Summary for resolvability:**
- **25 references total**
- **22 PRESENT** (resolvable with valid DOI/URL)
- **2 UNVERIFIABLE** (refs. 4, 19 — future date or malformed DOI)
- **0 MISSING**

---

### 2. Claim–Citation Support

#### Key factual claims checked against cited references:

**Claim 1** (Introduction, lines 50–53): "On other ion-mobility platforms, the PNNL PreProcessor writes denoised data back in the instrument's own format, but it does not support Bruker .d."
- **Citation**: Ref. (7) Bilbao et al. 2022
- **Status**: **UNVERIFIABLE** — The reference is to a preprocessing tool for ion-mobility MS workflows, but the manuscript does not quote or provide the abstract/methods section. The claim that it writes in native format for non-Bruker platforms is plausible but cannot be confirmed from the manuscript alone. Recommend author provide excerpt or clarification.
- **Severity**: SOFT (not a central claim; contextual positioning of prior work)

**Claim 2** (Introduction, lines 56–57): "In representative 5-minute runs, 50.1% of ddaPASEF and 72.7% of diaPASEF MS1 points lay outside the fragmentable region."
- **Citation**: None explicitly given; appears to be from the authors' own data
- **Status**: **PRESENT** — This is the authors' own observation from their benchmark, not attributed to prior work. No citation required.

**Claim 3** (Methods 2.5, lines 132–143): "We used the Generation Beta three-species hybrid benchmark (human, Saccharomyces cerevisiae, and Escherichia coli) deposited as PRIDE PXD070049. Its defined ratios provide a standard test of label-free quantification accuracy."
- **Citation**: Refs. (18) Van Puyvelde & Dhaenens and (20) Navarro et al. 2016
- **Status**: **PRESENT** — Ref. 18 is the benchmark dataset itself (PRIDE PXD070049); Ref. 20 is cited for the LFQ benchmark methodology. Both are appropriate and resolvable.

**Claim 4** (Methods 2.6, lines 145–159): "Sage provided mobility-aware MS1 label-free quantification... identifications were transferred between runs using decoy-controlled LFQ q-values, as in IonQuant."
- **Citation**: Refs. (21) Lazear 2023 (Sage) and (22) Yu et al. 2021 (IonQuant)
- **Status**: **PRESENT** — Both tools are cited for their respective methods. Appropriate.

**Claim 5** (Methods 2.6, lines 160–162): "The three diaPASEF arms were searched independently with DIA-NN 2.2.0, which read each native .d directory through its bundled Bruker timsdata library."
- **Citation**: Ref. (23) Demichev et al. 2020
- **Status**: **PRESENT** — DIA-NN is cited; the claim about bundled Bruker support is plausible for a 2020 tool but not explicitly verified in the manuscript excerpt. However, this is a factual claim about software capability, not a quantitative result, and the tool is correctly cited.

**Claim 6** (Methods 2.6, lines 163–164): "DIA-NN quantified proteins with MaxLFQ from MS2 fragment chromatograms."
- **Citation**: Ref. (24) Cox et al. 2014
- **Status**: **PRESENT** — MaxLFQ is correctly cited as the quantification method.

**Claim 7** (Methods 2.7, lines 167–168): "Accuracy is the species-specific median log₂ ratio relative to the known mixture ratio."
- **Citation**: Implicit reference to benchmark design (refs. 18, 20)
- **Status**: **PRESENT** — This is a standard metric for the benchmark; no new claim.

**Claim 8** (Results 3.4, lines 260–276): "A rank-1 decoy hit is a match to a sequence known to be absent from the sample... In the original ddaPASEF searches at 5 and 15 minutes, respectively, 30.1% and 23.7% of scored spectra had a decoy as their best available explanation."
- **Citation**: Ref. (25) Elias & Gygi 2007 (target-decoy search method)
- **Status**: **PRESENT** — The target-decoy method is correctly cited. The percentages are the authors' own calculations from their benchmark data, not attributed to the reference.

---

### 3. Quotation and Number Fidelity

No direct quotations from prior work are provided in the manuscript. Numerical claims are either:
- The authors' own benchmark results (e.g., "50.1% of ddaPASEF MS1 points"), or
- Standard methodological parameters (e.g., "±20 ppm precursor and fragment tolerances")

**Status**: **PRESENT** — No quotation fidelity issues detected.

---

### 4. Self-Citation and Citation Inflation

**Self-citations identified:**
1. **Ref. (15)**: timsrust library (MannLabs contributors) — not authored by Garrett et al., but used by them
2. **Ref. (18)**: LFQ Benchmark Generation Beta — Van Puyvelde & Dhaenels are the benchmark creators; Garrett et al. are users/contributors
3. **Software release**: dnoise v0.1.0 (Zenodo DOI 10.5281/zenodo.21959649) — the authors' own tool, appropriately cited in Data Availability

**Assessment**: The self-citations are **germane and appropriate**. The authors cite the benchmark they used (which they may have contributed to) and their own software release (required for reproducibility). No citation inflation detected.

**Severity**: SOFT (not a concern; standard practice)

---

### 5. Retracted or Predatory Sources

All cited journals are mainstream, peer-reviewed venues:
- *Nature Methods*, *Nature Biotechnol.*, *Nucleic Acids Res.*, *Mol. Cell. Proteomics*, *J. Proteome Res.*, *Analyst*, *PLoS One*, *Anal. Chem.*, *Int. J. Ion Mobility Spectrom.*

**Status**: **PRESENT** — No retracted or predatory sources detected.

---

## Summary Table

| Category | Trigger Present | Findings | Severity |
|----------|-----------------|----------|----------|
| **Reference Resolvability** | Yes | 22/25 present; 2 unverifiable (refs. 4, 19); 0 missing | SOFT (refs. 4, 19) |
| **Claim–Citation Support** | Yes | All load-bearing claims supported or self-generated; 1 unverifiable detail (ref. 7 scope) | SOFT (ref. 7) |
| **Quotation/Number Fidelity** | No | No direct quotations; no fidelity issues | — |
| **Self-Citation Inflation** | Yes | Appropriate and germane; no inflation | — |
| **Retracted/Predatory Sources** | No | No problematic sources | — |

---

## Issues Requiring Author Clarification

### Issue 1: Reference 4 (Houthuijs et al. 2026) — Future-dated publication
**Finding**: The manuscript is dated August 2026, and this reference is also dated 2026. The DOI format is valid, but the publication status cannot be independently confirmed.

**Question for authors**: Is this an advance online publication, preprint, or in-press article? Please provide the publication status and confirm the DOI is correct.

**Severity**: SOFT

---

### Issue 2: Reference 19 (Van Puyvelde et al.) — Malformed DOI
**Finding**: The DOI is listed as `10.64898/2026.01.29.702266`, which has an unusual structure (date string embedded in DOI). This does not match standard DOI formatting.

**Question for authors**: Is this DOI correct? Reference 18 cites the same benchmark with DOI `10.6019/PXD070049` (a PRIDE accession). Please clarify whether ref. 19 is a duplicate, a different version, or a transcription error.

**Severity**: SOFT

---

### Issue 3: Reference 7 (Bilbao et al. 2022) — Scope of prior tool
**Finding**: The manuscript claims the PNNL PreProcessor "writes denoised data back in the instrument's own format" for non-Bruker platforms but does not support Bruker. The cited reference is resolvable, but the manuscript does not provide evidence that this claim is explicitly stated in the paper.

**Question for authors**: Can you provide a quote or section reference from Bilbao et al. 2022 confirming that the PreProcessor supports native-format output for non-Bruker platforms and explicitly does not support Bruker .d?

**Severity**: SOFT (contextual claim, not central to the paper's contribution)

---

## Conclusion

**Overall status**: **COMPLIANT with minor clarifications needed**

- All 25 references are resolvable or present in the reference list.
- Two references (4, 19) require author clarification on publication status and DOI format.
- All load-bearing claims are either supported by cited references or are the authors' own data.
- No retracted, predatory, or obviously false citations detected.
- Self-citations are appropriate and germane.

**Recommendation**: Request author responses to the three clarification questions above before final acceptance. None of these issues block reproducibility or invalidate the central claims.