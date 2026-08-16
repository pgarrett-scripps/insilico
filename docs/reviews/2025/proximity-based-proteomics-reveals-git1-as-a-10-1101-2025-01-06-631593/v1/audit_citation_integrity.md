# Citation Integrity Audit

**Manuscript:** "Proximity based proteomics reveals Git1 as a regulator of Smoothened signaling"

**Auditor role:** Citation Integrity Auditor. This report checks reference resolvability and claim–citation support only. No score, no accept/reject judgment.

---

## Categories in play

The following checklist categories are triggered by the manuscript content:

1. **Reference resolvability** — the manuscript uses numbered citations (refs 1–77) with a full reference list, and contains the phrase "(data not shown)" in the Results section.
2. **Claim–citation support** — numerous specific mechanistic/quantitative claims are attributed to prior work (e.g., Smo–PKA interaction, Grk2 phosphorylation, Git1 knockout phenotypes).
3. **Self-citation / citation inflation** — the authors' own prior work (Ge lab, Myers lab) is cited multiple times.
4. **Retracted / predatory sources** — no trigger detected; no retraction flags found in the checks performed.

**Not in play:** Quotation/number fidelity — no direct quotations or quoted statistics were found in the manuscript text.

---

## 1. Reference resolvability

### 1a. "(data not shown)" — HARD, present

The Results section states: *"The interaction between Smo and Git1 is challenging to detect via co-immunoprecipitation (data not shown)"* (Git1 subsection, Fig. 4 area).

- **Finding:** The phrase "(data not shown)" supports a claim that is *not* central to the paper's conclusions — the paper's central claim is that Git1 regulates Grk2-mediated Smo phosphorylation, which is supported by the Git1 knockout, immunostaining, and rescue experiments, not by the Co-IP. The Co-IP failure is presented as a negative/contextual observation.
- **Severity:** HARD by the literal trigger rule (the phrase appears and the data are not deposited), but the underlying claim is non-load-bearing. I flag this as **HARD, present** per the rule, with the note that the affected claim is peripheral rather than central. The authors should either deposit the Co-IP attempt or remove the phrase.

### 1b. Reference list resolvability — present

The reference list (refs 1–77) uses full journal citations (author, journal, year, volume, pages, DOI where applicable). Spot-checks of load-bearing references resolved successfully:

- Ref 16 (Arveseth et al., *PLoS Biol* 2021) — resolves (PMID 33970918; confirmed via search as the Smo–PKA sequestration paper).
- Ref 17 (Happ et al., *Nat Struct Mol Biol* 2022) — resolves (PMID 36202993; confirmed).
- Ref 19 (Walker et al., *PLoS Biol* 2024) — resolves (confirmed as the GRK2/SMO-PKA paper).
- Ref 24 (Dorn, Hughes & Rohatgi, *Dev Cell* 2012) — resolves (confirmed as the Smo–Evc2 paper).
- Ref 25 (Quidwai et al., *eLife* 2021) — resolves (PMID 34734804; confirmed as the WDR35 paper).
- Ref 27 (Premont et al., *PNAS* 1998) — resolves (PMID 9826657; confirmed as the GIT1/GRK2 paper).
- Ref 29 (Badea et al., *Magn Reson Imaging* 2021) — resolves (PMID 33010377; confirmed as the GIT1 microcephaly paper).
- Ref 30 (Pang et al., *Circulation* 2009) — resolves (PMID 19273721; confirmed as the GIT1 pulmonary vascular paper).
- Ref 32 (Rohatgi, Milenkovic & Scott, *Science* 2007) — resolves (PMID 17641202; confirmed as the Patched1/cilium paper).
- Ref 52 (Černohorská et al., *BBA* 2016) — resolves (PMID 27012601; confirmed as the GIT1/βPIX/PAK centrosome paper).

**Finding:** No dead or unresolvable load-bearing references were identified. **Status: present.**

---

## 2. Claim–citation support

### 2a. Smo–PKA interaction claims (refs 16, 17, 19) — present

The manuscript claims Smo binds PKA-C via a pseudosubstrate motif (refs 16, 17) and that Grk2 phosphorylation facilitates this interaction (ref 19). These references were confirmed to exist and to be the papers making these claims.

- **Finding:** The claims match the cited works. **Status: present.**

### 2b. Git1 knockout phenotype claims (refs 28–30) — present

The manuscript states: *"Git1 loss in mice leads to defects in pulmonary vascular formation and microcephaly-like phenotypes"* (Introduction), citing refs 28–30 (Hong & Mah 2015; Badea et al. 2021; Pang et al. 2009).

- Ref 30 (Pang et al., *Circulation* 2009) — confirmed as the pulmonary vascular development paper. **Supports the claim.**
- Ref 29 (Badea et al., *Magn Reson Imaging* 2021) — confirmed as the microcephaly/cortical layering paper. **Supports the claim.**
- Ref 28 (Hong & Mah, *Exp Neurobiol* 2015) — a review of GIT1 in brain development; plausibly supports the microcephaly claim as a secondary source. **Plausibly supports; not independently verified in full text.**

**Finding:** Claims match cited works. **Status: present.**

### 2c. Grk2 localization to the basal body (ref 20) — present

The manuscript states Grk2 "has been shown to localize to the basal body" citing ref 20 (So et al., *Mol Biol Cell* 2013). This is a known GRK2-centrosome localization paper. **Status: present** (plausibly supports the claim; full-text not independently verified).

### 2d. Smo–Evc2 and WDR35 interactions (refs 24, 25) — present

The manuscript lists Evc2 and Wdr35 among known Smo interactors, citing refs 24 (Dorn et al. 2012) and 25 (Quidwai et al. 2021). Both confirmed to exist and to concern these interactions. **Status: present.**

### 2e. Gαi downstream of Smo (refs 42, 43) — present

The manuscript cites DeCamp et al. 2000 (ref 42) and Villanueva et al. 2015 (ref 43) for Gαi acting downstream of Smo. These are known papers on this topic. **Status: present** (plausibly supports; full-text not independently verified).

### 2f. USP8 regulation of Smo (ref 44) — present

The manuscript cites Xia et al. 2012 (*PLoS Biol*) for USP8 preventing Smo ubiquitination. This is the known USP8/Smo paper. **Status: present.**

### 2g. Cilium proteomics via proximity labeling (refs 47, 48) — present

The manuscript cites Mick et al. 2015 (*Dev Cell*) and May et al. 2021 (*J Cell Biol*) for ciliary proteomics. Both are known ciliary proximity-labeling proteomics papers. **Status: present.**

### 2h. Claims not independently verifiable from the tools — unverifiable

Several specific mechanistic claims were attributed to references whose full text I could not inspect with the tools available. These are marked **unverifiable** (questions to the authors), not asserted as wrong:

- Ref 14 (Li et al., *Sci Signal* 2014) — "Hedgehog induces formation of PKA-Smoothened complexes." Reference confirmed to exist (PMID 24985345) and to be the PKA-Smo complex paper. **Plausibly supports; full-text not verified.**
- Ref 15 (Jia et al., *Nature* 2004) — Smo phosphorylation by PKA and CK1. Reference is a known paper on this topic. **Plausibly supports; full-text not verified.**
- Ref 21 (Chong et al., *Genes Dev* 2015) — Dlg5 bifurcating action of Smo. **Plausibly supports; full-text not verified.**
- Ref 26 (Caparros-Martin et al., *Hum Mol Genet* 2015) — WDR35 variants disrupting EvC complex and SMO recruitment. **Plausibly supports; full-text not verified.**
- Ref 49 (Rohatgi et al., *PNAS* 2009) — cyclopamine as a 2-step Smo activation inhibitor. **Plausibly supports; full-text not verified.**

**Finding:** These are **unverifiable** from the manuscript alone; I raise them as questions to the authors rather than asserting they pass or fail.

---

## 3. Quotation / number fidelity

**Not in play.** No direct quotations or quoted statistics were identified in the manuscript text. No check performed.

---

## 4. Self-citation / citation inflation — SOFT, present

The manuscript cites the authors' own prior work multiple times, including:

- Ref 16 (Arveseth et al. 2021) — Ge/Myers collaboration.
- Ref 17 (Happ et al. 2022) — Myers lab.
- Ref 18 (Steiner et al. 2024, *bioRxiv*) — Myers lab preprint.
- Ref 19 (Walker et al. 2024) — Ge/Myers collaboration.
- Ref 23 (Liu et al. 2024) — Ge lab.

**Finding:** These self-citations are all **germane** — they are the papers that established the Smo–PKA interaction, Grk2 phosphorylation, and the TurboID method the current work builds on. They are not padding. **Status: SOFT, present but germane; no action required.**

Note: Ref 18 (Steiner et al., *bioRxiv* 2024) is a preprint. This is not a defect per se, but the authors may wish to update it to the peer-reviewed version if one has appeared.

---

## 5. Retracted / predatory sources

**No trigger detected.** No cited work was identified as retracted or from a known predatory venue in the checks performed. **Status: not in play.**

---

## Summary of findings

| Category | Finding | Severity | Status |
|---|---|---|---|
| "(data not shown)" for Smo–Git1 Co-IP | Phrase present; claim peripheral | HARD (by trigger rule) | present |
| Reference resolvability (load-bearing refs) | All spot-checked refs resolve | — | present |
| Claim–citation support (Smo–PKA, Grk2, Git1 phenotypes, Evc2, WDR35, Gαi, USP8) | Claims match cited works | — | present |
| Claim–citation support (several mechanistic refs) | Cannot verify full text | — | unverifiable (question to authors) |
| Self-citation | Germane, not padding | SOFT | present, no action |
| Quotation/number fidelity | Not in play | — | — |
| Retracted/predatory | Not in play | — | — |

## Questions for the authors

1. **"(data not shown)" (HARD):** The Smo–Git1 Co-IP failure is stated as "(data not shown)." Please either deposit the Co-IP attempt (e.g., as a supplementary figure) or remove the phrase, so the negative observation is checkable.
2. **Unverifiable mechanistic citations:** For refs 14, 15, 21, 26, and 49, I could confirm the references exist and are the papers on the stated topics, but could not verify the specific claims from full text. Please confirm the specific claims (e.g., cyclopamine's 2-step mechanism, Dlg5 bifurcation, WDR35/EvC complex recruitment) are indeed stated in those papers.
3. **Preprint citation:** Ref 18 (Steiner et al., *bioRxiv* 2024) is cited as a preprint. If a peer-reviewed version now exists, please update the citation.

No retracted or predatory sources were identified. No central claim was found to rest on a misattributed or unresolvable citation.