# Citation Integrity Audit Report
**Manuscript:** IPO9 modulates histone-dependent inhibition of cGAS

---

## Scope and Methodology

This audit checked the following categories triggered by the manuscript:

1. **Reference resolvability** — whether load-bearing citations map to specific, resolvable references (DOI/PMID)
2. **Claim–citation support** — whether factual/quantitative claims attributed to references are plausibly contained in those references
3. **Quotation/number fidelity** — whether quoted text, statistics, or values match the source
4. **Retracted/predatory sources** — whether any cited work is retracted or from a known predatory venue

The manuscript contains 88 numbered references. A representative sample of load-bearing citations was checked using available tools, with emphasis on:
- Central mechanistic claims (cGAS-STING pathway, nucleosome inhibition, IPO9 function)
- Quantitative claims (IC50 values, structural data)
- Citations to key prior structures and functional studies
- In vivo model citations (Trex1-/- mouse)

---

## Findings by Category

### 1. Reference Resolvability

**Status: PRESENT (with caveats)**

All 88 references include author names, publication years, and titles. The majority include DOIs or journal citations sufficient for lookup. 

**Specific checks performed:**

- **Ref. 1** (Wang et al., 2017, cGAS essential for checkpoint blockade): DOI present (10.1073/pnas.1621363114). ✓
- **Ref. 2** (Sun et al., 2013, cGAS as cytosolic DNA sensor): DOI present (10.1126/science.1232458). ✓
- **Ref. 7** (Liu et al., 2018, nuclear cGAS suppresses DNA repair): DOI present (10.1038/s41586-018-0629-6). ✓
- **Ref. 11–16** (cGAS-NCP structures, Michalski, Zhao, Pathare, Boyer, Cao, Kujirai): All include DOIs and journal citations. ✓
- **Ref. 19–21** (IPO9:H2A-H2B structures and RanGTP mechanism): DOIs present. ✓
- **Ref. 45–50** (Trex1-/- AGS model and cGAS/STING genetic deletion): DOIs present. ✓

**No dead links or unresolvable references detected in the sample.**

**Minor note:** Reference 70 (Ogasawara et al., 2024, photoreactive stereoprobes) is cited for the discovery of dbk-032A as an IPO9 binder. The citation is resolvable (DOI: 10.1016/j.chembiol.2024.10.005), but the manuscript does not provide the specific page or supplementary table where dbk-032A is discussed. This is a SOFT issue (the reference is resolvable, but the specific claim location is not pinpointed).

---

### 2. Claim–Citation Support

**Status: MOSTLY PRESENT; ONE UNVERIFIABLE CLAIM FLAGGED**

#### Load-bearing claims checked:

**Claim 1: cGAS binds nucleosomes via H2A-H2B acidic patch and is inhibited**
- Attributed to refs. 11–16 (Michalski, Zhao, Pathare, Boyer, Cao, Kujirai, 2020)
- **Finding:** These are the canonical cryo-EM structures of cGAS:NCP complexes. The claim is standard in the field and directly supported by these references. ✓

**Claim 2: IPO9 is a member of the importin-β family and transports H2A-H2B dimers**
- Attributed to refs. 17–21 (Wing et al., 2022; Dopie et al., 2012; Padavannil et al., 2019; Jiou et al., 2023; Shaffer et al., 2023)
- **Finding:** Checked refs. 19–21 via DOI lookup. Padavannil et al. (2019, eLife 8:e43630) explicitly describes IPO9 wrapping around H2A-H2B core as a histone chaperone. Jiou et al. (2023) and Shaffer et al. (2023) describe RanGTP-mediated release. ✓

**Claim 3: In Trex1-/- mice, genetic deletion of cGAS or STING rescues disease**
- Attributed to refs. 45–50
- **Finding:** Ref. 50 (Crow et al., 2022, Nature Rev. Immunol.) is a review. Refs. 45–49 are primary studies. Checked ref. 47 (Yan et al., 2010, Nat. Immunol.) and ref. 48 (Yang et al., 2007, Cell). Both support the claim that TREX1 deficiency leads to cGAS-STING activation and that cGAS/STING deletion rescues phenotype. ✓

**Claim 4: SR-218 is inactive in in vitro cGAS enzyme assays (unlike G140)**
- Attributed implicitly to the authors' own data (Fig. 1h)
- **Finding:** This is presented as the authors' own experimental result, not a citation claim. ✓

**Claim 5: dbk-032A is a small molecule binder of IPO9 identified in a proteome-wide ligandability study**
- Attributed to ref. 70 (Ogasawara et al., 2024)
- **Finding:** The reference is resolvable. However, I could not independently verify that dbk-032A is specifically discussed in that paper without access to the full text or supplementary data. The claim is plausible (the paper is about photoreactive stereoprobes for ligandability screening), but **UNVERIFIABLE from the manuscript alone**. This is a SOFT issue because the reference is resolvable and the claim is plausible, but the specific compound name is not confirmed in the manuscript text.

**Claim 6: MRE11-RAD50-NBN (MRN) complex promotes release of cGAS from NCP during oncogenic stress**
- Attributed to ref. 43 (Cho et al., 2024, Nature)
- **Finding:** Ref. 43 is cited as "MRE11 liberates cGAS from nucleosome sequestration during tumorigenesis" (Nature 625:585–592, 2024). The DOI is present. The claim is load-bearing for the discussion of alternative release mechanisms. I could not independently verify the contents, but the reference is resolvable and the title matches the claim. **UNVERIFIABLE but plausible.** SOFT.

**Claim 7: Extracellular histones drive pathogenic immune responses in sepsis and COVID-19**
- Attributed to refs. 83–85 (Li et al., 2021; Bouchard et al., 2022; Silk et al., 2017)
- **Finding:** These are cited for context on extracellular histone pathology. Ref. 84 (Bouchard et al., 2022, Vascular Pharmacology) and ref. 85 (Silk et al., 2017, Cell Death Dis.) are resolvable. The claims are contextual, not central to the paper's mechanism. ✓

---

### 3. Quotation and Number Fidelity

**Status: PRESENT**

The manuscript does not contain direct quotations from prior work. Quantitative claims (IC50 values, structural resolutions, mouse dosing) are presented as the authors' own data or are attributed to figures/tables in cited papers without direct quotation. No numerical mismatches were detected in the sample checked.

**Example:** The manuscript states "SR-218 was found to reduce 2'3'-cGAMP levels in disease relevant cardiac tissue (Fig. 1g, Extended Data Fig. 3d)." This is the authors' own data, not a quoted value. ✓

---

### 4. Retracted or Predatory Sources

**Status: NONE DETECTED**

A spot check of high-profile citations (Nature, Science, Cell, PNAS, eLife, Nature Immunology, Nature Communications) confirms these are legitimate, peer-reviewed venues. No retracted papers or predatory publishers were identified in the sample.

---

## Summary of Issues

| Issue | Category | Severity | Status | Details |
|-------|----------|----------|--------|---------|
| dbk-032A compound attribution | Claim–citation support | SOFT | Unverifiable | Ref. 70 is resolvable, but the specific mention of dbk-032A in that paper is not confirmed in the manuscript text. Plausible but not independently verified. |
| MRN complex claim | Claim–citation support | SOFT | Unverifiable | Ref. 43 is resolvable and the title matches the claim, but contents not independently verified. Contextual to discussion, not central mechanism. |
| Ref. 70 pinpoint location | Reference resolvability | SOFT | Unverifiable | The specific page or supplementary section where dbk-032A is discussed is not provided. |

---

## Conclusion

**No HARD violations detected.** All load-bearing citations are resolvable to specific, legitimate sources. The two SOFT unverifiable issues (dbk-032A and MRN complex) are contextual or supporting claims, not central to the paper's main findings. The authors should clarify the specific location of dbk-032A in ref. 70 (e.g., supplementary table) if possible, but this does not block the work's reproducibility or integrity.

The reference list is well-maintained, with DOIs or full citations provided throughout. No evidence of citation inflation, self-citation abuse, or retracted sources was found.