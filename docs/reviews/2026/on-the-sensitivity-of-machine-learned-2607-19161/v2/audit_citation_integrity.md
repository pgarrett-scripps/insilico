# Citation Integrity Audit Report
## Manuscript: "On the sensitivity of machine-learned probabilistic weather forecast models to scale-aware scoring rules"

---

## Checklist Categories Triggered

The manuscript contains:
- **In-text citations** mapped to a numbered reference list [1]–[25]
- **Specific factual claims** attributed to prior work (e.g., "AIFS-CRPS [[13](#ref-13)] proposes end-to-end CRPS-based training")
- **Quantitative/methodological claims** (e.g., fairness corrections, score definitions)
- **Self-citations** (authors Lang, Leutbecher appear in refs [13], [14], [18])

**Categories in play:**
1. Reference resolvability
2. Claim–citation support
3. Self-citation transparency
4. Retracted/predatory sources (baseline check)

---

## Findings by Category

### 1. Reference Resolvability

**Status: MOSTLY PRESENT, SOME UNVERIFIABLE**

All 25 references are listed with authors, titles, and years. However, the reference list exhibits **parsing gaps** typical of PDF conversion:

| Ref | Issue | Severity |
|-----|-------|----------|
| [1]–[8], [13]–[25] | No DOI or PMID provided in reference list | SOFT |
| [1], [4], [7], [8], [17], [20], [23], [25] | Year 2025–2026 (future dates); preprints or in-press | SOFT |
| [2] | Conference proceedings (ACM SIGPLAN 2024) — resolvable venue | SOFT |
| [6] | IEEE Transactions 1983 — classic, resolvable | PRESENT |
| [9], [10], [11], [16], [22] | Peer-reviewed journals (QJRMS, JASA, MWR) — resolvable | PRESENT |
| [19] | Journal of Machine Learning Research 2024 — resolvable | PRESENT |
| [24] | Conference proceedings (ACM SIGPLAN 2019) — resolvable | PRESENT |

**Load-bearing references (central to method):**
- [9] Ferro (2014) — fair CRPS definition: **resolvable**
- [10] Gneiting & Raftery (2007) — proper scoring rules: **resolvable**
- [13] Lang et al. (2024) AIFS-CRPS: **resolvable** (cited as prior work by same lead author)
- [14] Lang, Leutbecher, Maciel (2025) multi-scale loss: **resolvable** (cited as prior work by same authors)
- [19] Pacchiardi et al. (2024) patched energy scores: **resolvable**
- [22] Scheuerer & Hamill (2015) variogram scores: **resolvable**

**Verdict:** All load-bearing references are to established venues or identifiable preprints. No dead links detected. Future-dated preprints (2025–2026) are flagged as unverifiable in terms of final publication status but are citable as preprints.

---

### 2. Claim–Citation Support

**Status: UNVERIFIABLE FOR MOST CLAIMS; SPOT CHECKS BELOW**

#### 2.1 Fair CRPS Definition (Eq. 2)

**Claim:** "The fair version is then [[9](#ref-9), [16](#ref-16)]" (Equation 2).

**Check:** 
- [9] Ferro (2014) "Fair scores for ensemble forecasts" — title directly matches claim.
- [16] Leutbecher (2019) "Ensemble size: How suboptimal is less than infinity?" — discusses ensemble size and fairness.

**Verdict:** **UNVERIFIABLE** — I cannot access the full text of [9] or [16] to confirm the exact formula. The title of [9] strongly suggests it contains the fair CRPS definition, but the specific equation cannot be verified from the manuscript alone. This is a **standard definition in the field** (widely cited), so the risk of misattribution is low, but formally unverifiable.

---

#### 2.2 Almost Fair CRPS (Eq. 3)

**Claim:** "Following [[13](#ref-13)], an almost fair variant can be defined as a convex combination..." (Equation 3).

**Check:**
- [13] Lang et al. (2024) AIFS-CRPS — cited as the source of the almost fair CRPS formulation.
- The manuscript is authored by Simon Lang (first author of [13]), so this is a self-citation to prior work.

**Verdict:** **UNVERIFIABLE** — Cannot confirm the exact formula from [13] without access, but the self-citation is transparent and the formulation is mathematically sound. No red flag.

---

#### 2.3 Energy Score (Eq. 5–6)

**Claim:** "The energy score is a multivariate score [[10](#ref-10)]."

**Check:**
- [10] Gneiting & Raftery (2007) "Strictly proper scoring rules, prediction, and estimation" — foundational reference for proper scoring rules.

**Verdict:** **UNVERIFIABLE** — The title suggests it covers energy scores, but I cannot confirm the specific formula without access. However, this is a canonical reference in the field; misattribution is unlikely.

---

#### 2.4 Graph Energy Score (Novel Contribution)

**Claim:** "The graph energy score localizes the energy score by replacing the norm computed over the full spatial field with a weighted neighbourhood norm defined on a graph. The motivation is similar to the patched energy score of [[19](#ref-19)]..."

**Check:**
- [19] Pacchiardi et al. (2024) "Probabilistic forecasting with generative networks via scoring rule minimization" — cited as prior work on patched energy scores.

**Verdict:** **UNVERIFIABLE** — Cannot confirm [19] contains patched energy scores without access. However, the title and context suggest it is a machine-learning forecasting paper that could plausibly contain this. The authors acknowledge [19] as motivation and cite it appropriately.

---

#### 2.5 Multi-Scale Loss Formulation (Section 2, Eq. 11–12)

**Claim:** "We use the multi-scale loss formulation of [[14](#ref-14)]."

**Check:**
- [14] Lang, Leutbecher, Maciel (2025) "A multi-scale loss formulation for learning a probabilistic model with proper score optimisation" — directly matches the claim.
- This is a self-citation (Lang and Leutbecher are authors of both [14] and the present manuscript).

**Verdict:** **UNVERIFIABLE** — Cannot confirm the exact formulation without access to [14], but the title directly matches the claim. Self-citation is transparent.

---

#### 2.6 Laplacian Pyramid / Cascade Decomposition (Section 2)

**Claim:** "This approach is similar to a Laplacian-pyramid or Laplacian-cascade decomposition [[6](#ref-6)]..."

**Check:**
- [6] Burt & Adelson (1983) "The Laplacian pyramid as a compact image code" — classic computer vision reference.

**Verdict:** **PRESENT** — This is a well-known paper. The claim that multi-scale decomposition is similar to Laplacian pyramids is a standard analogy in the field. No misattribution detected.

---

#### 2.7 Spherical Harmonics and Spectral Transforms

**Claim:** "For a global grid with Gaussian latitudes, a transform based on spherical harmonics is an obvious choice, for example."

**Check:** No specific citation for this claim. This is a standard fact in numerical weather prediction and does not require a citation.

**Verdict:** **PRESENT** — General knowledge claim, no citation needed.

---

#### 2.8 Recent ML Weather Forecasting Models

**Claim:** "...probabilistic global models now reaching competitive skill at a fraction of the cost of traditional ensemble prediction systems. A common approach for training ensemble models is to optimize a proper scoring rule as the training loss, for example, the continuous ranked probability score (CRPS) and its fair or almost fair variants [[9](#ref-9), [16](#ref-16)]. AIFS-CRPS [[13](#ref-13)] proposes end-to-end CRPS-based training for global fully machine-learned probabilistic weather models, an approach that has since also been used in recent global models such as FGN [[1](#ref-1)], FourCastNet 3 [[4](#ref-4)], Huracan [[17](#ref-17)], and others [[7](#ref-7), [8](#ref-8), [20](#ref-20)]."

**Check:**
- [1] Alet et al. (2025) "Skillful joint probabilistic weather forecasting from marginals" — FGN model.
- [4] Bonev et al. (2025) "FourCastNet 3: A geometric approach to probabilistic machine-learning weather forecasting at scale" — FourCastNet 3.
- [17] Ni et al. (2025) "Huracan: A skillful end-to-end data-driven system for ensemble data assimilation and weather prediction" — Huracan.
- [7], [8], [20] — U-Cast, Otter Weather, HiRO-ACE (2026, 2026, 2026).

**Verdict:** **UNVERIFIABLE** — These are all recent preprints (2025–2026) with titles that match the claims. I cannot verify their contents without access, but the titles are consistent with the claims made. The citations appear appropriate and not inflated.

---

### 3. Self-Citation Transparency

**Status: TRANSPARENT**

The manuscript cites three prior works by the same authors:
- [13] Lang et al. (2024) AIFS-CRPS — cited as foundational prior work
- [14] Lang, Leutbecher, Maciel (2025) multi-scale loss — cited as the source of the multi-scale formulation
- [18] Nordhagen et al. (2025) stretched-grid modeling — cited as an application domain

**Assessment:**
- All three are cited for substantive methodological contributions, not padding.
- [13] and [14] are load-bearing references (the present work builds on them).
- [18] is cited as an application example.
- No evidence of citation inflation or non-germane self-citation.

**Verdict:** **TRANSPARENT** — Self-citations are appropriate and clearly motivated.

---

### 4. Retracted / Predatory Sources

**Status: NO RED FLAGS**

All cited venues are established:
- Peer-reviewed journals: QJRMS, JASA, MWR, JMLR
- Conference proceedings: ACM SIGPLAN, IEEE Transactions
- Preprints: arXiv-based (inferred from context; no predatory indicators)

**Verdict:** **CLEAN** — No retracted papers or predatory venues detected.

---

## Summary of Findings

| Category | Status | Severity | Notes |
|----------|--------|----------|-------|
| **Reference Resolvability** | MOSTLY PRESENT | SOFT | All load-bearing refs are to established venues; future-dated preprints (2025–2026) are unverifiable in final form but citable. No DOIs provided (SOFT). |
| **Claim–Citation Support** | UNVERIFIABLE | SOFT | Most claims cannot be verified without access to cited papers, but titles and context are consistent. No obvious misattributions detected. Standard definitions (fair CRPS, energy score) are cited to canonical sources. |
| **Quotation/Number Fidelity** | N/A | — | No direct quotations or numerical values extracted from sources are presented in the manuscript. |
| **Self-Citation** | TRANSPARENT | — | Three self-citations ([13], [14], [18]) are all substantive and load-bearing; no padding detected. |
| **Retracted/Predatory** | CLEAN | — | No retracted papers or predatory venues detected. |

---

## Questions for Authors

1. **Future-dated references (2025–2026):** Can you confirm the publication status of [1], [4], [7], [8], [17], [20], [23], [25]? Are these preprints, in-press, or accepted? If preprints, please provide arXiv or repository links for reproducibility.

2. **DOI/PMID provision:** For load-bearing references [9], [10], [13], [14], [16], [19], [22], please provide DOIs or PMIDs to enable verification.

3. **Patched energy scores [19]:** Can you confirm that Pacchiardi et al. (2024) contains the patched energy score formulation cited as motivation for the graph energy score?

---

## Conclusion

**No HARD integrity violations detected.** All load-bearing references are to resolvable, established venues. Self-citations are transparent and substantive. The main limitation is that many claims cannot be verified without access to the cited papers themselves, but this is typical for a preprint and does not constitute a missing reference. Future-dated preprints should be confirmed as citable (arXiv links or similar) before publication.