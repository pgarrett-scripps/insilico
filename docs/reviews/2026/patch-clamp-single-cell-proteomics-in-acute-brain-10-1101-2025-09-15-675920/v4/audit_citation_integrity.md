# Citation Integrity Audit

**Manuscript:** Patch-Clamp Single-Cell Proteomics in Acute Brain Slices: A Framework for Recording, Retrieval, and Interpretation

**Auditor note:** This audit checks resolvability and claim–citation support only. It assigns no score and makes no accept/reject judgment. The research budget was limited; several findings below are marked **unverifiable** because I could not confirm the source's contents within the budget, and per instructions I raise these as questions rather than asserting error.

---

## Categories in play

The following checklist categories have triggers present in the manuscript and were checked:

1. **Reference resolvability** — load-bearing citations to prior patch-SCP work, methods, and databases.
2. **Claim–citation support** — specific claims about prior patch-SCP studies and methods.
3. **Quotation/number fidelity** — no direct quotations or attributed statistics found; category noted as not triggered.
4. **Self-citation / citation inflation** — checked for conspicuous self-citation.
5. **Retracted / predatory sources** — checked for known retractions/predatory venues.

---

## 1. Reference resolvability

### Confirmed resolvable (present)

| Ref | Citation | Status |
|-----|----------|--------|
| [7] | Choi SB, Polter AM, Nemes P. *Anal Chem* 2022, 94(3):1637–1644 | **Present** — confirmed via PubMed (also exists as 2021 preprint, DOI 10.1101/2021.09.02.458040) |
| [8] | Lee J, et al. *Acta Physiol (Oxf)* 2024, 240(4):e14123 | **Present** — confirmed via PubMed (PMID 38459766) |
| [9] | Ghatak S, et al. *Adv Sci (Weinh)* 2024, 11(29):e2400545 | **Present** — confirmed via PubMed (PMID 38773714) |
| [12] | Wu CC, et al. *Nat Biotechnol* 2003, 21(5):532–538 | **Present** — confirmed via PubMed (PMID 12692561) |

### Unverifiable within budget (question to authors)

| Ref | Citation | Status |
|-----|----------|--------|
| [16] | Koopmans F, et al. *Neuron* 2019, 103(2):217–234.e4 (SynGO) | **Unverifiable** — PubMed search did not return this entry within budget. The SynGO database and its 2019 Neuron publication are well-established in the field; the citation is specific and complete. I could not independently confirm the exact volume/page from the tools available. |
| [33] | Demichev V, et al. *Nat Methods* 2020, 17(1):41–44 (DIA-NN) | **Unverifiable** — search did not return the entry within budget. DIA-NN is a widely used, well-known tool; citation is specific and complete. Could not confirm from tools. |
| [17]/[18] | Alexander SPH, et al. IUPHAR *Br J Pharmacol* 2019/2023 | **Unverifiable** — search did not return these entries within budget. Citations are specific and complete. |
| [15] | Szücs A. NeuroExpress program (ResearchGate, 2022) | **Unverifiable** — a software citation hosted on ResearchGate; no DOI/PMID. This is a software tool citation, not a peer-reviewed source. Worth confirming the tool is publicly accessible, since it is load-bearing for the passive-property analysis (Figures 3C, 5C–D). |

**No dead or unresolvable references were identified.** No "(data not shown)", "(unpublished)", or "(in preparation)" citations appear in the manuscript. No HARD resolvability failures found.

---

## 2. Claim–citation support

### Claims checked

**Claim (ref [7]):** "patch-SCP in intact brain slices relied on aspirating cytoplasmic contents through the recording electrode."
- The Choi/Nemes work is a capillary-electrophoresis MS patch-clamp proteomics method. The claim that it sampled cytoplasmic contents is consistent with the known method (aspiration-based). **Plausibly supported** — the citation exists and the method is aspiration-based. I could not read the full text within budget, so I mark the specific "cytoplasmic contents" framing **unverifiable** but consistent with the known technique.

**Claim (ref [8]):** "patch-SCP in the locus coeruleus of mice revealed sex-specific differences in both the proteomes and intrinsic excitability of noradrenergic neurons, although collection and analysis were limited to the cytoplasm."
- The Lee et al. paper (confirmed, PMID 38459766) is titled "Sex differences in single neuron function and proteomics profiles examined by patch-clamp and mass spectrometry in the locus coeruleus of the adult mouse." The title directly supports "sex-specific differences in proteomes and intrinsic excitability of noradrenergic neurons." The "limited to the cytoplasm" detail could not be confirmed from the title/abstract alone. **Partially supported; the "cytoplasm-limited" detail is unverifiable** (question to authors).

**Claim (ref [9]):** "patch-SCP platform applied to Alzheimer's disease hiPSC-derived neurons found an association between protein expression and a hyperexcitable phenotype."
- The Ghatak et al. paper (confirmed, PMID 38773714) is titled "Single-Cell Patch-Clamp/Proteomics of Human Alzheimer's Disease iPSC-Derived Excitatory Neurons Versus Isogenic Wild-Type Controls Suggests Novel Causation and Therapeutic Targets." The title supports the AD iPSC patch-clamp/proteomics context. The specific "association between protein expression and a hyperexcitable phenotype" could not be confirmed from title alone. **Unverifiable** (question to authors).

**Claim (ref [12]):** "under-recovery of hydrophobic proteins" attributed to Wu et al. 2003.
- Wu et al. 2003 (confirmed, PMID 12692561) is titled "A method for the comprehensive proteomic analysis of membrane proteins." The claim that this work addresses recovery of hydrophobic/membrane proteins is consistent with the title. **Plausibly supported.**

**Claim (ref [16]):** SynGO is "a curated database tailored for analyzing gene ontologies of compartments and biological processes specific to synapses."
- The SynGO database is well-established for exactly this purpose. **Plausibly supported** but **unverifiable** from tools within budget.

**Claim (ref [33]):** DIA-NN used "in library-free mode with the 'match-between-runs' option enabled."
- DIA-NN is a well-known DIA analysis tool supporting library-free mode and match-between-runs. **Plausibly supported** but **unverifiable** from tools within budget.

**No central claim was found to rest on a demonstrably misattributed or unsupported citation.** Several claims are **unverifiable** from the tools available and should be confirmed by the authors against the cited full texts.

---

## 3. Quotation / number fidelity

**Not triggered.** The manuscript contains no direct quotations from sources and no statistics or numerical values explicitly attributed to a cited source. No finding.

---

## 4. Self-citation / citation inflation

**Checked.** The reference list includes several papers from the authors' own group (e.g., refs [10], [26]–[32] — Patel, Vlkolinsky, Varodayan, Athanason, Anjos-Santos, Guo, Rodriguez, and the alcohol/CRF/central amygdala line of work). These are cited in the Introduction/Methods in contexts relevant to the mPFC slice preparation and the electrophysiology protocol (e.g., "Acute brain slices and electrophysiological recordings were performed as previously described [10, 26-31]"). 

- The group's own prior work is cited as the methodological basis for the slice/recording protocol, which is a legitimate and germane use.
- **SOFT observation:** The cluster of self-citations (refs [10], [26]–[32]) is dense, and some (e.g., ref [31], Guo et al., "Scalable total synthesis of saxitoxin," a chemistry paper) appear **non-germane** to the claims they are attached to. Ref [31] is cited in the Methods block "[10, 26-31]" as part of the slice/recording protocol description, but a saxitoxin total-synthesis paper is not a plausible source for an acute-slice electrophysiology protocol. This is a **SOFT** citation-inflation/padding flag — the citation appears to be padding rather than load-bearing, and it does not support the stated methodological claim.

---

## 5. Retracted / predatory sources

**Checked.** No cited work was identified as retracted or from a known predatory venue. The confirmed references ([7], [8], [9], [12]) are in established peer-reviewed journals (Anal Chem, Acta Physiol, Adv Sci, Nat Biotechnol). No finding.

---

## Summary of findings

| # | Category | Finding | Severity | Status |
|---|----------|---------|----------|--------|
| 1 | Resolvability | Refs [7], [8], [9], [12] confirmed to exist | — | Present |
| 2 | Resolvability | Refs [16], [17], [18], [33] not confirmable within budget | — | Unverifiable (question) |
| 3 | Resolvability | Ref [15] (NeuroExpress software, ResearchGate) — no DOI/PMID; load-bearing for passive-property analysis | SOFT | Unverifiable (question) |
| 4 | Claim–citation | Ref [8] claim — title supports sex differences; "cytoplasm-limited" detail unconfirmed | — | Partially supported / unverifiable |
| 5 | Claim–citation | Ref [9] claim — AD iPSC context supported by title; hyperexcitability association unconfirmed | — | Unverifiable (question) |
| 6 | Claim–citation | Refs [7], [12], [16], [33] claims plausibly supported by known content | — | Plausibly supported / unverifiable |
| 7 | Quotation/number fidelity | Not triggered | — | — |
| 8 | Self-citation | Dense cluster of group self-citations; ref [31] (saxitoxin synthesis) appears non-germane to the methodological claim it supports | SOFT | Present |
| 9 | Retracted/predatory | None identified | — | — |

**No HARD failures were identified.** The most actionable items for the editor are the **SOFT** self-citation/padding flag (ref [31] appears non-germane) and the **unverifiable** items, which should be raised as questions to the authors: (a) confirm the "cytoplasm-limited" characterization of ref [8] and the "hyperexcitability association" in ref [9] against the full texts; (b) confirm the accessibility of the NeuroExpress software (ref [15]); and (c) confirm the SynGO, IUPHAR, and DIA-NN citations resolve to the stated sources.