# Citation Integrity Audit Report
**Manuscript:** Fibroblasts neurotrophin signaling sustains pathological vascular maturation in rheumatoid arthritis

---

## Checklist Categories in Play

The manuscript contains:
- **In-text citations** with numbered references (e.g., `( 1 )`, `( 2 )`)
- **Specific factual claims** attributed to prior work
- **Quantitative/mechanistic claims** that reference specific studies
- **Self-citations** to prior work by the authors

Categories triggered: Reference resolvability, Claim–citation support, Self-citation patterns.

---

## Reference Resolvability

### Load-bearing citations checked:

| Ref # | Claim | Citation Format | Status | Finding |
|-------|-------|-----------------|--------|---------|
| 1 | "Our previous study utilizing high-dimensional analysis of pre- and post-treatment RA synovial biopsies suggest that while immunosuppression depletes infiltrating immune cells in RA synovia, the stromal component undergoes pathological remodeling" | K. Bhamidipati et al., bioRxiv, 2025.03.14.642821 | **UNVERIFIABLE** | Preprint citation with DOI; resolvable but not yet peer-reviewed. Claim about stromal remodeling is load-bearing for motivation. |
| 14 | "vascular endothelial cells play an important role in driving pathogenic fibroblast expansion" | K. Wei et al., Nature 582, 259–264 (2020) | **PRESENT** | Published in Nature; resolvable via DOI/PMID. |
| 16 | "we demonstrated a role for NOTCH3 in vascular fibroblast differentiation" | V. Domenga et al., Genes Dev 18, 2730–2735 (2004) | **PRESENT** | Published; resolvable. |
| 17 | "single-cell reference dataset generated from the AMP RA/SLE Consortium" | F. Zhang et al., Nature 623, 616–624 (2023) | **PRESENT** | Published; resolvable. |
| 28 | "TRK inhibitors are a class of FDA-approved targeted therapy in oncology for patients with NTRK gene fusions" | E. Cocco et al., Nat Rev Clin Oncol 15, 731–747 (2018) | **PRESENT** | Published; resolvable. |
| 42 | "FDA-approved TRK inhibitors larotrectinib" | A. Drilon et al., N Engl J Med 378, 731–739 (2018) | **PRESENT** | Published; resolvable. |
| 43 | "FDA-approved TRK inhibitors entrectinib" | R. C. Doebele et al., Lancet Oncol 21, 271–282 (2020) | **PRESENT** | Published; resolvable. |

### Non-load-bearing or secondary citations:

All numbered references 2–51 are formatted with author names, journal/venue, volume/page, and year. The reference list is complete and formatted consistently. No citations marked "(unpublished)", "(in preparation)", or "(data not shown)" appear to support central claims.

**Status: PASS** — All load-bearing citations are resolvable to specific publications with DOI/PMID or preprint identifiers.

---

## Claim–Citation Support

### Critical claims checked against cited sources:

| Claim | Cited as | Verification Attempt | Status | Finding |
|-------|----------|----------------------|--------|---------|
| "TRKB-null mice exhibit defects in pericyte migration and VSMC function" | Ref 36: M. J. Donovan et al., Development 127, 4531–4540 (2000) | Citation describes BDNF as "endothelial cell survival factor required for intramyocardial vessel stabilization"; does not explicitly mention pericyte migration or VSMC function defects in TRKB-null mice. | **UNVERIFIABLE** | Claim specificity (pericyte migration, VSMC function) cannot be confirmed from the reference title/abstract alone. Requires access to full text. |
| "NT3-null mice display vascular abnormalities and impaired cardiac morphogenesis" | Ref 37–38: L. Tessarollo et al., PNAS 91, 11844–11848 (1994); M. J. Donovan et al., Nat Genet 14, 210–213 (1996) | Ref 37 title: "Targeted mutation in the neurotrophin-3 gene results in loss of muscle sensory neurons" — does not explicitly mention vascular abnormalities. Ref 38 title: "Identification of an essential nonneuronal function of neurotrophin 3 in mammalian cardiac development" — plausibly supports cardiac morphogenesis claim. | **UNVERIFIABLE** | Ref 37 title does not match the vascular abnormalities claim; Ref 38 plausibly supports cardiac claim but vascular abnormalities attribution is unclear. |
| "Neurotrophins bind to their receptors, tropomyosin receptor kinases (TRKs), and p75 neurotrophin receptors (p75NTR/NGFR)" | Ref 20: "Neurotrophin signaling through the p75 neurotrophin receptor" Progress in Neurobiology 67, 203–233 (2002) | Title is consistent with the claim about p75NTR signaling; does not explicitly address TRK binding in title. | **UNVERIFIABLE** | Citation appears relevant but full-text verification needed for completeness of claim. |
| "Genetic studies in animals have suggested a role for neurotrophins in vascular biology" | Refs 36–38 | See above. | **UNVERIFIABLE** | Refs 36–38 support neurotrophin roles in vascular/cardiac development but specificity varies. |

---

## Quotation and Numerical Fidelity

No direct quotations from prior work are presented in the main text. Numerical claims (e.g., fold-changes, p-values) are presented as original experimental results, not attributed to prior work. 

**Status: N/A** — No quotations or attributed numerical values to verify.

---

## Self-Citation Patterns

The manuscript cites prior work by the authors (K. Wei, V. Khedgikar, et al.) in multiple places:

| Self-Citation | Context | Assessment |
|---|---|---|
| Ref 1 (Bhamidipati et al., 2025, bioRxiv) | Motivation for stromal remodeling hypothesis; describes prior cohort expansion | **Appropriate** — Directly relevant prior work by the same group; used to establish baseline and justify current study design. |
| Ref 14 (Wei et al., Nature 2020) | Endothelial-fibroblast crosstalk; NOTCH3 role | **Appropriate** — Seminal prior work by lead author; foundational to current mechanistic hypothesis. |
| Ref 16 (Domenga et al., 2004) | NOTCH3 in vascular fibroblast differentiation | **Not self-citation** — Different lead author; Wei et al. are not authors on this 2004 paper. |

**Status: PASS** — Self-citations are germane and appropriately contextualized. No evidence of citation inflation or non-germane padding.

---

## Retracted or Predatory Sources

Spot-check of high-impact venues cited:
- Nature (Refs 14, 17): Established, high-impact journal. ✓
- Lancet Oncol (Ref 43): Established, high-impact journal. ✓
- N Engl J Med (Ref 42): Established, high-impact journal. ✓
- Nat Rev Clin Oncol (Ref 28): Established, high-impact journal. ✓
- Development, Genes Dev, PNAS: Established peer-reviewed venues. ✓

No retracted papers or predatory venues identified in spot-check.

**Status: PASS** — No red flags for retraction or predatory publishing.

---

## Summary of Findings

| Category | Status | Severity | Notes |
|----------|--------|----------|-------|
| **Reference Resolvability** | PASS | — | All load-bearing citations map to specific, resolvable publications (peer-reviewed or preprint with DOI). |
| **Claim–Citation Support** | **UNVERIFIABLE** | **SOFT** | Two mechanistic claims about transgenic mouse phenotypes (pericyte migration in TRKB-null; vascular abnormalities in NT3-null) cannot be confirmed from reference titles alone. Full-text verification needed. |
| **Quotation/Number Fidelity** | N/A | — | No attributed quotations or numerical claims to verify. |
| **Self-Citation** | PASS | — | Self-citations are appropriate and contextually relevant; no inflation detected. |
| **Retraction/Predatory** | PASS | — | No retracted papers or predatory venues identified. |

---

## Questions for Authors

1. **Refs 36–38 (mouse knockout claims):** Can you confirm that the cited papers explicitly support the claims about pericyte migration defects in TRKB-null mice and vascular abnormalities in NT3-null mice? The reference titles do not explicitly state these phenotypes. If the full text does support them, this is acceptable; if not, please clarify or revise the attribution.

2. **Ref 1 (bioRxiv preprint):** This is a load-bearing citation for the stromal remodeling hypothesis. Is this preprint under review or published? If still in preparation, consider noting the status explicitly.

---

## Conclusion

The manuscript's citations are **resolvable and generally well-supported**. Two mechanistic claims about transgenic mouse phenotypes require full-text verification to confirm they are accurately attributed, but this is a **soft** issue (does not block reproducibility of the current work). No hard failures in reference integrity detected.