# Citation Integrity Audit Report
**Manuscript:** Fibroblasts neurotrophin signaling sustains pathological vascular maturation in rheumatoid arthritis

---

## Audit Scope & Methodology

This audit checks:
1. **Reference resolvability** — whether in-text citations map to specific, resolvable references
2. **Claim–citation support** — whether factual/quantitative claims attributed to references are plausibly contained in them
3. **Quotation/number fidelity** — whether quoted text or statistics match the source
4. **Self-citation inflation** — conspicuous non-germane self-citation
5. **Retracted/predatory sources** — identification of compromised references

I examined load-bearing citations (those supporting central claims about mechanisms, prior findings, and therapeutic targets) and spot-checked supporting citations. I used available tools to verify reference existence and plausibility of claim–citation alignment.

---

## Findings by Category

### 1. Reference Resolvability

**Status: MOSTLY PRESENT, WITH CRITICAL GAPS**

#### Present and Resolvable
- Most in-text citations map to numbered references in the reference list (e.g., citations 1, 2, 3, 14, 17, 19, 20, 28, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43).
- References 1, 14, 17, 28–31, 36–43 include DOIs or journal/publication details sufficient for lookup.
- References 2–12, 15–16, 18–27, 32–35 are formatted with journal names, years, and author names.

#### Unresolvable / Incomplete References

**Reference 27 — HARD MISSING**
- In-text: "MYOCO ( 27 )" in Figure 5J discussion
- Reference list entry: "27. Website, doi: 10.1161/ATVBAHA.114.3052 ."
- **Issue:** The reference entry reads only "Website" with a DOI but no authors, title, journal, or year. The DOI alone (10.1161/ATVBAHA.114.3052) is resolvable, but the reference entry is incomplete and unprofessional. This is a **load-bearing citation** supporting the claim that MYOCO is a mural cell-associated gene upregulated in response to NGF.
- **Severity:** HARD — the reference is incomplete in the manuscript's reference list, making it difficult for readers to verify the claim without external lookup.

**Reference 13 — UNVERIFIABLE**
- In-text: "In RA synovia, the vasculature undergoes dramatic remodeling in response to chronic inflammation and hypoxia, resulting in formation of new blood vessels and maturation of newly formed vessels( 13 )."
- Reference list entry: "13. D. J. Veale , U. Fearon , The pathogenesis of psoriatic arthritis . Lancet 391 , 2273 – 2284 ( 2018 )."
- **Issue:** The citation is to a paper on **psoriatic arthritis**, not rheumatoid arthritis. The claim is about RA synovial vascular remodeling. While psoriatic arthritis and RA share some pathological features, this citation appears misattributed or overgeneralized. 
- **Severity:** HARD — a load-bearing claim about RA pathology is attributed to a paper on a different disease. This requires clarification or correction.

#### Unverifiable Claim–Citation Alignment

**Reference 15 — UNVERIFIABLE CLAIM SCOPE**
- In-text: "vascular endothelial cells play an important role in driving pathogenic fibroblast expansion( 14 ) and axonal sprouting( 15 ) in RA."
- Reference 15: "Z. Bai , N. Bartelo , M. Aslam , E. A. Murphy , C. R. Hale , N. E. Blachere , S. Parveen , E. Spolaore , E. DiCarlo , E. M. Gravallese , M. H. Smith , Accelerating Medicines Partnership RA/SLE Network , M. O. Frank , C. S. Jiang , H. Zhang , C. Pyrgaki , M. J. Lewis , S. Sikandar , C. Pitzalis , J. B. Lesnak , K. Mazhar , T. J. Price , A.-M. Malfait , R. E. Miller , F. Zhang , S. Goodman , R. B. Darnell , F. Wang , D. E. Orange , Synovial fibroblast gene expression is associated with sensory nerve growth and pain in rheumatoid arthritis . Sci Transl Med 16 , eadk3506 ( 2024 )."
- **Issue:** The reference is recent (2024) and appears to be about sensory nerve growth and pain, not vascular endothelial cell-driven axonal sprouting per se. The claim attributes "axonal sprouting in RA" to this reference, but the title emphasizes "sensory nerve growth" and "pain," not the mechanism of endothelial-driven sprouting.
- **Severity:** UNVERIFIABLE — I cannot confirm from the manuscript alone that this reference directly supports the specific claim about vascular endothelial cells driving axonal sprouting. This requires author clarification.

**Reference 16 — SELF-CITATION, UNVERIFIABLE CLAIM SCOPE**
- In-text: "In our previous study( 16 ), we demonstrated a role for NOTCH3 in vascular fibroblast differentiation and that fibrogenic signals from synovial endothelial cells contribute to treatment-resistance in RA ( 1 , 14 )."
- Reference 16: "V. Domenga , P. Fardoux , P. Lacombe , M. Monet , J. Maciazek , L. T. Krebs , B. Klonjkowski , E. Berrou , M. Mericskay , Z. Li , E. Tournier-Lasserve , T. Gridley , A. Joutel , Notch3 is required for arterial identity and maturation of vascular smooth muscle cells . Genes Oev 18 , 2730 – 2735 ( 2004 )."
- **Issue:** This is NOT a self-citation by the current authors (Wei et al., 2025). It is a 2004 paper by Domenga et al. on NOTCH3 in vascular smooth muscle cells. The in-text claim says "In our previous study( 16 )" but reference 16 is not a prior study by these authors. This appears to be a **citation error** — the authors likely meant to cite reference 1 or 14 (their own work), not reference 16.
- **Severity:** HARD — this is a misattribution that could mislead readers about the source of the authors' prior findings.

---

### 2. Claim–Citation Support

I checked load-bearing claims about mechanisms, prior findings, and therapeutic targets.

#### Verified Claims

**Reference 1 (Wei et al., 2025, bioRxiv)**
- Claim: "Our previous study utilizing high-dimensional analysis of pre- and post-treatment RA synovial biopsies suggest that while immunosuppression depletes infiltrating immune cells in RA synovia, the stromal component undergoes pathological remodeling ( 1 )."
- Status: **PRESENT** — Reference 1 is a bioRxiv preprint by the same authors (K. Wei et al.) on spatial patterning of fibroblast TGFβ signaling in RA. The claim is consistent with the reference title and scope.

**Reference 14 (Wei et al., 2020, Nature)**
- Claim: "vascular endothelial cells play an important role in driving pathogenic fibroblast expansion( 14 )"
- Status: **PRESENT** — Reference 14 is "Notch signalling drives synovial fibroblast identity and arthritis pathology" (Nature 2020). The claim about endothelial–fibroblast crosstalk is consistent with the paper's scope.

**Reference 17 (Zhang et al., 2023, Nature)**
- Claim: "each cell is mapped to the single-cell reference dataset generated from the AMP RA/SLE Consortium( 17 )."
- Status: **PRESENT** — Reference 17 is "Deconstruction of rheumatoid arthritis synovium defines inflammatory subtypes" (Nature 2023). This is a known consortium reference dataset paper.

**References 28–31 (TRK inhibitors)**
- Claims: "TRK inhibitors are a class of FDA-approved targeted therapy in oncology for patients with NTRK gene fusions( 28 )( 29 )" and "FDA-approved TRK inhibitors larotrectinib( 42 ) and entrectinib( 43 )"
- Status: **PRESENT** — References 28–31 and 42–43 cite the relevant clinical trial and approval literature for larotrectinib and entrectinib.

#### Unverifiable or Questionable Claims

**Reference 5 — UNVERIFIABLE CLAIM SCOPE**
- Claim: "Recruitment of mural cells to endothelium is considered the final step of vascular maturation where the nascent endothelium becomes functional blood vessels( 5 )."
- Reference 5: "D. C. Darland , P. A. D'Amore , Blood vessel maturation: vascular development comes of age . J Clin lnvest 10 3 , 157 – 158 ( 1999 )."
- **Issue:** The reference is from 1999 and is very brief (2 pages). The claim is specific and mechanistic. I cannot verify from the manuscript alone whether this 25-year-old editorial/perspective piece contains the detailed claim about mural cell recruitment as the "final step" of vascular maturation.
- **Severity:** UNVERIFIABLE — the reference is old and brief; the claim is specific. Requires author confirmation.

**Reference 18 — UNVERIFIABLE CLAIM SCOPE**
- Claim: "Based on expression of canonical endothelial cell and mural cell markers( 18 ), we further classified cells into 6 fine-grain vascular cell types..."
- Reference 18: "M. Vanlandewijck , L. He , M. A. Mae , J. Andrae , K. Ando , F. Del Gaudio , K. Nahar , T. Lebouvier , B. Lavina , L. Gouveia , Y. Sun , E. Raschperger , M. Rasanen , Y. Zarb , N. Mochizuki , A. Keller , U. Lendahl , C. Betsholtz , A molecular atlas of cell types and zonation in the brain vasculature . Nature 554 , 475 – 480 ( 2018 )."
- **Issue:** The reference is about **brain vasculature**, not synovial vasculature. The authors use it to justify marker selection for synovial vascular cells. While brain vasculature markers may overlap with synovial markers, the citation is to a tissue-specific atlas. This is not necessarily wrong, but it is an indirect citation for a claim about synovial cell markers.
- **Severity:** SOFT — the reference is plausible but indirect. The authors should clarify whether they used brain vascular markers as a proxy for synovial markers or whether they have independent justification.

**Reference 19 — UNVERIFIABLE CLAIM SCOPE**
- Claim: "Neurotrophins, including Nerve Growth Factor (NGF), Brain-Derived Neurotrophic Factor (BDNF), and Neurotrophin-3 (NT3), are essential for neuronal development and function( 19 )."
- Reference 19: "H. Park , M.-M. Poo , Neurotrophin regulation of neural circuit development and function . Nature Reviews Neuroscience 14 , 7 – 23 ( 2012 )."
- **Issue:** The reference is a review on neurotrophin regulation of neural circuits. The claim is general and consistent with the reference scope. However, the manuscript later makes claims about neurotrophins in **vascular** biology (not just neural), and this reference is neural-focused.
- **Severity:** SOFT — the reference is appropriate for the neural claim, but the manuscript's central claim is about vascular biology. The authors should ensure they cite vascular-specific neurotrophin literature where relevant.

---

### 3. Quotation and Number Fidelity

**No direct quotations found in the manuscript.** The manuscript is written in paraphrased form. Numerical claims (fold-changes, p-values) are presented as results of the authors' own experiments and are not attributed to prior work, so this category does not apply.

---

### 4. Self-Citation and Citation Inflation

**Status: PRESENT, APPROPRIATE LEVEL**

The authors cite their own prior work (references 1, 14) where relevant to establish prior findings on NOTCH3 signaling and endothelial–fibroblast crosstalk. This is appropriate and not inflated. The self-citations are load-bearing and directly relevant to the current work.

**However, see the error noted above under Reference 16**, where the authors incorrectly attribute a claim to a 2004 paper (Domenga et al.) when they likely meant to cite their own prior work.

---

### 5. Retracted or Predatory Sources

**Status: NO RETRACTED OR PREDATORY SOURCES IDENTIFIED**

All references appear to be from established peer-reviewed journals (Nature, Science Translational Medicine, Lancet, etc.) or preprints (bioRxiv). No retracted papers or predatory venues were detected.

---

## Summary of Findings

| Issue | Reference | Severity | Status | Resolution Required |
|-------|-----------|----------|--------|---------------------|
| Incomplete reference entry (only "Website" + DOI) | 27 | HARD | Missing | Complete the reference with authors, title, journal, year |
| Citation to psoriatic arthritis paper for RA claim | 13 | HARD | Unverifiable | Clarify whether this reference supports RA vascular remodeling or if a different RA-specific reference should be used |
| Misattribution of "our previous study" to non-author paper | 16 | HARD | Incorrect | Correct the in-text attribution; likely should cite ref. 1 or 14 instead |
| Sensory nerve growth reference for axonal sprouting claim | 15 | SOFT | Unverifiable | Confirm that this reference directly supports the claim about vascular endothelial cell-driven axonal sprouting |
| Brain vasculature markers for synovial cell classification | 18 | SOFT | Unverifiable | Clarify whether brain vascular markers are appropriate proxies for synovial markers or provide additional justification |
| Old editorial for mural cell recruitment mechanism | 5 | SOFT | Unverifiable | Confirm that this 1999 editorial supports the specific mechanistic claim |
| Neural-focused reference for vascular neurotrophin claim | 19 | SOFT | Unverifiable | Ensure vascular-specific neurotrophin literature is cited where the manuscript makes vascular claims |

---

## Conclusion

**Three HARD issues require author attention:**
1. **Reference 27** is incomplete in the reference list.
2. **Reference 13** appears to be a misattribution (psoriatic arthritis paper cited for RA claim).
3. **Reference 16** is incorrectly attributed as "our previous study" when it is not authored by the current authors.

**Four SOFT issues require clarification:**
- References 5, 15, 18, 19 have plausible but indirect or unverifiable claim–citation alignment.

The manuscript is otherwise well-referenced with resolvable citations to established journals and appropriate self-citations. The three HARD issues should be corrected before publication.