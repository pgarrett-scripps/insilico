# Citation Integrity Audit Report
## LATTICE: Graph Self-Supervised Learning for Multimodal Spatial Omics Integration

---

## Checklist Categories in Play

The manuscript contains:
- **Reference resolvability triggers**: Multiple in-text citations to prior work (refs [1]–[20])
- **Claim–citation support triggers**: Specific factual claims attributed to references (e.g., "GraphST [[3](#ref-3)] and related models use graph neural networks")
- **Self-citation triggers**: References [4] (SARSIM) and implicit internal tools (ReCAST) authored by the same group
- **Quotation/number fidelity triggers**: None detected (no direct quotations from sources)

---

## Findings by Category

### 1. Reference Resolvability

**Status: PRESENT with UNVERIFIABLE elements**

All 20 references are listed in the reference section with author names and publication venues. However, several entries lack complete identifiers:

| Ref | Title/Venue | DOI/PMID | Status | Severity |
|-----|-------------|----------|--------|----------|
| [1] | Ståhl et al., *Science* 2016 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [2] | Kaya-Okur et al., *Nat. Commun.* 2019 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [3] | Long et al., *Nat. Commun.* 2023 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [4] | Dwarampudi et al., *bioRxiv* 2026 | Not provided | **UNVERIFIABLE** – future date, preprint | HARD |
| [5] | Dong & Zhang, *Nat. Commun.* 2022 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [6] | Hu et al., *Nat. Methods* 2021 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [7] | Yang et al., *Nat. Commun.* 2025 | Not provided | **UNVERIFIABLE** – future date | HARD |
| [8] | Zhang et al., *Cell Genomics* 2026 | Not provided | **UNVERIFIABLE** – future date | HARD |
| [9] | Zhu & Ma, *Nat. Biotechnol.* 2024 | Not provided | **UNVERIFIABLE** – future date | HARD |
| [10]–[13] | Software/methods papers | arXiv IDs or URLs provided for [11], [13] | Resolvable | SOFT |
| [14], [15], [17] | 10x Genomics URLs | URLs provided; accessed 2026-05-06 | **UNVERIFIABLE** – future access date | HARD |
| [16] | Strehl & Ghosh, *JMLR* 2002 | Not provided | Resolvable (established venue, specific year) | SOFT |
| [18] | Rousseeuw, *J. Comput. Appl. Math.* 1987 | Not provided | Resolvable (classic reference, specific year) | SOFT |
| [19] | Traag et al., *Sci. Rep.* 2019 | Not provided | Resolvable (high-impact journal, specific year) | SOFT |
| [20] | McInnes et al., arXiv 2018 | arXiv ID provided | Resolvable | SOFT |

**Key Issues:**

- **References [4], [7], [8], [9]** are dated 2025–2026, which is in the future relative to a 2024 preprint. This is a red flag for either:
  - Manuscript date error (should be 2026 or later)
  - Reference date error (should be 2024 or earlier)
  - Speculative/in-preparation citations

- **References [14], [15], [17]** cite 10x Genomics URLs with an access date of 2026-05-06, which is in the future. This is internally inconsistent with a preprint dated 2024.

- **Reference [4] (SARSIM)** is a bioRxiv preprint by the same authors. It is load-bearing (cited in Section 1, Figure 1 caption, Section 2, Section 4.1, and Appendix F). The future date makes it unverifiable.

---

### 2. Claim–Citation Support

**Status: MOSTLY PRESENT with CRITICAL UNVERIFIABLE CLAIM**

#### Load-bearing claims checked:

**Claim 1:** "GraphST [[3](#ref-3)] and related models use graph neural networks and self-supervision on expression and spatial proximity."
- **Citation:** [3] Long et al., *Nat. Commun.* 2023
- **Verification:** Title states "Spatially informed clustering, integration, and deconvolution of spatial transcriptomics with graphst" — plausibly supports claim of graph-based spatial method
- **Status:** PLAUSIBLE (not directly verified but title is consistent)
- **Severity:** SOFT

**Claim 2:** "SARSIM [[4](#ref-4)] is a framework for spatially anchored regulatory inference that integrates paired Visium and single-cell multiome data, learns a soft cell-to-spot mapping, and projects accessibility and motif activity into tissue space."
- **Citation:** [4] Dwarampudi et al., *bioRxiv* 2026
- **Verification:** Cannot verify — reference is dated 2026 (future date) and is a preprint by the same authors
- **Status:** UNVERIFIABLE
- **Severity:** HARD (this is a central upstream dependency for the entire LATTICE pipeline)

**Claim 3:** "Spatial transcriptomics [[1](#ref-1)] enable genome-wide gene expression across sections"
- **Citation:** [1] Ståhl et al., *Science* 2016
- **Verification:** Title "Visualization and analysis of gene expression in tissue sections by spatial transcriptomics" directly supports this claim
- **Status:** PLAUSIBLE
- **Severity:** SOFT

**Claim 4:** "Spatial CUT&Tag [[2](#ref-2)] add section-level chromatin and histone-modification context"
- **Citation:** [2] Kaya-Okur et al., *Nat. Commun.* 2019, "CUT&tag for efficient epigenomic profiling of small samples and single cells"
- **Verification:** Title supports claim about epigenomic profiling; plausibly includes histone modifications
- **Status:** PLAUSIBLE
- **Severity:** SOFT

**Claim 5:** "Noise-contrastive estimation [[12](#ref-12)]"
- **Citation:** [12] Gutmann & Hyvärinen, AISTATS 2010
- **Verification:** Title "Noise-contrastive estimation: A new estimation principle for unnormalized statistical models" directly supports the method name
- **Status:** CONFIRMED
- **Severity:** SOFT

---

### 3. Self-Citation and Citation Inflation

**Status: PRESENT**

- **Reference [4] (SARSIM):** Authored by Dwarampudi et al., same first author as the LATTICE manuscript. Cited 6+ times as a load-bearing upstream dependency. This is appropriate (not inflated) because SARSIM is genuinely a prerequisite for the multimodal feature construction (Section 4.1, Appendix F).

- **ReCAST pipeline:** Described in Appendix F as "an internal engineering pipeline" by the same authors. Not formally cited as a reference but mentioned throughout. This is appropriate transparency (not self-citation inflation) because it is disclosed as internal work.

- **No evidence of non-germane self-padding detected.**

**Severity:** SOFT (appropriate self-citation for genuine dependencies)

---

### 4. Retracted or Predatory Sources

**Status: NONE DETECTED**

All cited venues are established:
- *Science*, *Nature Communications*, *Nature Methods*, *Nature Biotechnology* (high-impact)
- *Cell Genomics*, *Scientific Reports* (peer-reviewed)
- *JMLR*, *AISTATS* (established conferences)
- arXiv, bioRxiv (preprint servers, not predatory)

No retracted papers identified.

---

### 5. Quotation and Number Fidelity

**Status: NOT APPLICABLE**

The manuscript does not include direct quotations from cited sources or specific numerical claims attributed to references (e.g., "Smith et al. found X% improvement"). Claims are paraphrased rather than quoted.

---

## Summary of Critical Issues

| Issue | Ref(s) | Severity | Status | Action Required |
|-------|--------|----------|--------|-----------------|
| Future publication dates (2025–2026) on preprint | [4], [7], [8], [9] | HARD | UNVERIFIABLE | Authors must clarify: are these in-preparation works, or is the manuscript date incorrect? |
| Future access dates on URLs | [14], [15], [17] | HARD | UNVERIFIABLE | Authors must verify and correct access dates. |
| SARSIM (ref [4]) is load-bearing but unverifiable | [4] | HARD | UNVERIFIABLE | Central to multimodal feature construction (Section 4.1, Figure 1). Cannot verify claims about SARSIM's functionality without access to the actual preprint. |
| No DOIs provided for any reference | All | SOFT | PRESENT | Recommended: add DOIs or PubMed IDs where available for reproducibility. |

---

## Questions for Authors

1. **Reference [4] (SARSIM):** The citation is dated bioRxiv 2026, which is in the future. Is this:
   - A manuscript date error (should the LATTICE preprint be dated 2026)?
   - A reference date error (should SARSIM be dated 2024)?
   - An in-preparation work that should be marked as such?

2. **References [7], [8], [9]:** These are dated 2025–2026. Are these published, in press, or in preparation? If in preparation, please mark them explicitly.

3. **References [14], [15], [17]:** The access date is listed as 2026-05-06, which is in the future. Please provide the actual access date when the URLs were retrieved.

4. **Verification of SARSIM functionality:** The manuscript claims SARSIM "learns a soft cell-to-spot mapping, and projects accessibility and motif activity into tissue space." Can you provide a preprint link or DOI so reviewers can verify these claims?

---

## Conclusion

**Overall Status:** The manuscript's reference list is **structurally complete** but contains **critical date inconsistencies** that make several load-bearing references **unverifiable**. The most serious issue is **Reference [4] (SARSIM)**, which is central to the entire LATTICE pipeline but cannot be verified due to its future publication date. 

**Recommendation:** Authors must resolve the date inconsistencies and provide verifiable access to SARSIM before the manuscript can be fully audited for citation integrity.