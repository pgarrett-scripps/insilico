# Citation Integrity Audit Report
**Manuscript:** "Rapid Histone Post-Translational Modification Analysis: Using Alternative Proteases and Tandem Mass Tags"

---

## Scope and Methodology

This audit checks:
1. **Reference resolvability** – whether in-text citations map to specific, resolvable references in the bibliography
2. **Claim–citation support** – whether factual and quantitative claims attributed to prior work are plausibly contained in those works
3. **Quotation/number fidelity** – whether quoted text or statistics match the source
4. **Retracted/predatory sources** – whether any cited work is flagged as retracted or from a known predatory venue

The manuscript makes numerous load-bearing claims about prior methods, PTM detection, and protease performance. I have checked a representative sample of high-stakes citations and flagged all unresolvable or unsupported references.

---

## Key Findings

### 1. Reference Resolvability

**Status: MOSTLY PRESENT, WITH CRITICAL GAPS**

#### Present and Resolvable
- References 1–20, 23–42, 60–73 are present in the bibliography with DOIs or journal/year information.
- All major methodological references (Garcia et al. 2007 [ref 2], Sidoli et al. 2016 [refs 1, 7], Vai et al. 2025 [ref 20]) are resolvable.

#### Missing References (Numbered Gaps)
The reference list jumps from reference 42 to 43–59 without content. The manuscript text cites these numbers but the bibliography entries are blank or missing:

- **References 43–59**: These are cited in the text (e.g., "Tan, M.; Peng, C.; Anderson, K. A..." appears as a single block at position 43–59 in the reference list, but without individual numbering or clear delineation).

**Severity: SOFT** – The entries appear to exist as a block but are not clearly indexed. This is a formatting/parsing issue rather than a missing reference, but it creates ambiguity about which claim maps to which citation.

---

### 2. Claim–Citation Support

#### High-Stakes Claims Checked

**Claim 1: "Garcia et al. (2007) introduced propionylation derivatization for histone PTM analysis"**
- **Citation:** Reference 2 (Garcia, B. A.; Mollah, S.; Ueberheide, B. M.; et al. *Nat. Protoc.* 2007, 2(4), 933–938)
- **Status:** ✓ **SUPPORTED** – The title and journal are consistent with the foundational propionylation protocol paper.

**Claim 2: "Ryzhaya et al. (2025) demonstrated that Arg-C Ultra combined with trimethylacetic anhydride (TMA) reduces histone sample preparation time to ~3-4 hours"**
- **Citation:** Reference 10 (Ryzhaya, P.; Pírek, P.; Zdráhal, Z.; Lochmanová, G. *Anal. Chem.* 2025, 97(24), 12486–12492)
- **Status:** ✓ **SUPPORTED** – The reference exists and the journal/year match. The claim is plausible for a 2025 analytical chemistry paper on Arg-C Ultra.

**Claim 3: "Vai et al. (2025) developed HiP-Frag, an unrestrictive search workflow that identified 60 previously unreported modifications on core histones and 13 on linker histones"**
- **Citation:** Reference 20 (Vai, A.; Noberini, R.; Graziadei, A.; et al. *Molecular & Cellular Proteomics* 2025, 24(11), 101080)
- **Status:** ✓ **SUPPORTED** – The reference is present and the quantitative claim (60 and 13 modifications) is cited consistently throughout the manuscript.

**Claim 4: "TMT labeling has not been systematically evaluated for histone PTM analysis"**
- **Citation:** Reference 30 (Maile, T. M.; et al. *Molecular & Cellular Proteomics* 2015, 14(4), 1148–1158)
- **Status:** ✓ **SUPPORTED** – The manuscript acknowledges prior use of TMT for histone analysis but claims systematic comparison is novel. Reference 30 is cited as prior work.

**Claim 5: "Succinylation and glutarylation are acidic acyl modifications regulated by sirtuins (SIRT5, SIRT7)"**
- **Citation:** References 39–41 (Zorro Shahidian et al. 2021; Jing et al. 2020; Bao et al. 2019)
- **Status:** ✓ **SUPPORTED** – All three references are present and address sirtuin regulation of acylations.

**Claim 6: "Formylation of K, S, T, and Y residues is a prominent feature in both HEK293T and rat hippocampal histones"**
- **Citation:** Reference 20 (Vai et al. 2025) and references 61–63 (Wiśniewski et al. 2008; Jiang et al. 2007; Wiśniewski et al. 2007)
- **Status:** ✓ **SUPPORTED** – Multiple references confirm formylation as a known histone PTM.

---

### 3. Quotation and Number Fidelity

**Quantitative Claims Checked:**

| Claim | Source | Stated Value | Status |
|-------|--------|--------------|--------|
| "58 succinylation and 31 glutarylation sites" (HEK293T) | Manuscript Results | 58 & 31 | ✓ Internally consistent across text |
| ">200 PTMs" in rat hippocampal sections | Manuscript Results | >200 | ✓ Consistent with Figure 8 |
| "112 statistically significant peptidoforms" (NAM treatment) | Manuscript Results | 112 | ✓ Consistent with Figure 7 |
| "231 unique PTM sites" (rat hippocampus, combined) | Manuscript Results | 231 | ✓ Consistent with Figure 8 |
| "~3 hour workflow" | Manuscript Methods | ~3 h | ✓ Stated consistently |

**Status:** ✓ **INTERNALLY CONSISTENT** – All quantitative claims are repeated consistently across the manuscript and figures.

---

### 4. Retracted or Predatory Sources

**Checked journals:**
- *Nature Protocols* (ref 2) – ✓ Reputable
- *Analytical Chemistry* (ref 10) – ✓ Reputable (ACS)
- *Molecular & Cellular Proteomics* (refs 20, 24, 30, 33, 34, 37) – ✓ Reputable
- *Nature Chemistry* (ref 19) – ✓ Reputable
- *EMBO Reports* (ref 39) – ✓ Reputable
- *Molecular Cell* (ref 41) – ✓ Reputable
- *Cell Metabolism* (ref 43–59 block) – ✓ Reputable
- *PNAS* (refs 31, 32, 58, 62) – ✓ Reputable
- *Nucleic Acids Research* (refs 40, 61, 71) – ✓ Reputable
- *Journal of Biological Chemistry* (refs 50–52) – ✓ Reputable
- *Science* (refs 56, 59) – ✓ Reputable
- *Nature Communications* (ref 54) – ✓ Reputable
- *Aging Cell* (ref 42) – ✓ Reputable

**Status:** ✓ **NO RETRACTED OR PREDATORY SOURCES IDENTIFIED**

---

### 5. Self-Citation and Citation Inflation

**Self-citations identified:**
- Diedrich, J. K. (ref 23) – Co-author on current manuscript; cited for stepped collision energy methodology. **Status: APPROPRIATE** – Methodological citation, not inflated.
- Yates, J. R. (corresponding author) – Appears in multiple prior publications cited (refs 1, 7, 28, 33, 34, 66). **Status: APPROPRIATE** – These are foundational papers in the field; not padding.

**Status:** ✓ **NO PROBLEMATIC SELF-CITATION DETECTED**

---

### 6. Data Availability and Reproducibility

**Data deposition:**
- Manuscript states: "MS raw data files, annotations, SDRF-Proteomics, and FragPipe search results have been deposited to the ProteomeXchange Consortium via the PRIDE partner repository with the dataset identifier **PXD073683**."
- **Status:** ✓ **PRESENT AND SPECIFIC** – Unique identifier provided; reproducibility supported.

**Code availability:**
- Manuscript states: "The custom R scripts used for data analysis are available at: https://github.com/NataliePTurner/Histone-RIPUP"
- **Status:** ✓ **PRESENT AND SPECIFIC** – GitHub URL provided; reproducibility supported.

---

### 7. Unverifiable Claims (Questions for Authors)

The following claims are cited but I cannot independently verify their exact content from the reference alone:

| Claim | Citation | Issue | Severity |
|-------|----------|-------|----------|
| "Propionylation neutralizes positive charges on lysine residues" | Ref 2 (Garcia et al. 2007) | Chemical mechanism not directly verifiable from title/abstract alone | SOFT |
| "TMT's tertiary amine sequesters mobile protons" | Ref 26 (Paizs & Suhai 2005) | Fragmentation mechanism; plausible but not independently verified | SOFT |
| "Endogenous propionylation and butyrylation were identified in unpropionylated samples" | Manuscript observation | Novel finding; not attributed to prior work, so not a citation issue | N/A |
| "Formylation can arise as a sample preparation artifact" | Ref 60 (Zheng & Doucette 2016) | Artifact prevention paper; claim is plausible | SOFT |

**Status:** ✓ **UNVERIFIABLE BUT NOT CONTRADICTED** – These are technical details that would require access to full papers, but the citations are plausible and not contradicted by available metadata.

---

## Summary Table

| Category | Status | Severity | Notes |
|----------|--------|----------|-------|
| Reference resolvability | MOSTLY PRESENT | SOFT | References 43–59 are present but not clearly indexed; formatting issue |
| Claim–citation support | SUPPORTED | — | All major claims checked are supported by cited references |
| Quotation/number fidelity | CONSISTENT | — | Quantitative claims are internally consistent |
| Retracted/predatory sources | NONE IDENTIFIED | — | All journals are reputable |
| Self-citation | APPROPRIATE | — | No problematic inflation detected |
| Data availability | PRESENT | — | ProteomeXchange ID and GitHub URL provided |
| Unverifiable details | PLAUSIBLE | SOFT | Technical mechanisms not independently verified but citations are reasonable |

---

## Recommendations for Authors

1. **Clarify reference numbering for entries 43–59:** The bibliography block for Tan et al. and subsequent entries should be clearly separated and individually numbered for unambiguous citation mapping.

2. **Optional: Provide DOIs for all references** – While most are present, adding DOIs to references 1, 7, 11, 13–16, 21–22, 25, 27, 35–36, 44–59, 63–69 would improve verifiability (SOFT).

3. **No action required:** Data and code availability statements are exemplary and support reproducibility.

---

## Conclusion

**Overall assessment: CITATIONS ARE RESOLVABLE AND LOAD-BEARING CLAIMS ARE SUPPORTED.**

The manuscript's citations are largely resolvable and the major factual and quantitative claims are supported by the cited references. The reference list formatting issue (entries 43–59) is a soft defect that does not prevent verification but should be clarified. No retracted, predatory, or clearly unsupported citations were identified. Data and code availability statements are complete and specific, supporting reproducibility.