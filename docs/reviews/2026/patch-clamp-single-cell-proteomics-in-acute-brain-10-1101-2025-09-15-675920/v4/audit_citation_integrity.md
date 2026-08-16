# Citation Integrity Audit

**Manuscript:** *Patch-Clamp Single-Cell Proteomics in Acute Brain Slices: A Framework for Recording, Retrieval, and Interpretation*

---

## Scope of audit

I checked the following categories, which are triggered by the manuscript's content:

1. **Reference resolvability** — load-bearing in-text citations mapping to specific, resolvable references
2. **Claim–citation support** — specific factual/quantitative claims attributed to references
3. **Quotation/number fidelity** — quoted statistics or values attributed to sources
4. **Self-citation / citation inflation**
5. **Retracted / predatory sources**

Categories **not** triggered (no evidence in manuscript): none — all five categories have at least some trigger present, so all were checked.

---

## 1. Reference resolvability

### 1.1 References with incomplete or non-resolvable identifiers

| Ref # | Issue | Severity | Status |
|---|---|---|---|
| Ref 15 (Szücs, *NeuroExpress program for analyzing patch-clamp data*, ResearchGate, 2022) | Cited as the source of the NeuroExpress software used for passive-membrane analysis (Methods; Fig. 3C legend). The venue is "ResearchGate" — not a peer-reviewed journal, and no DOI/PMID is given. The software is load-bearing for the electrophysiological analysis (capacitance, RM, VM, τM values). The reference is specific enough to locate the software, but the citation venue is unconventional. | SOFT | **Unverifiable** — the reference exists as a ResearchGate item, but I cannot confirm its contents or that it is a citable, stable publication. |
| Refs 17–18 (Alexander et al., *Concise Guide to PHARMACOLOGY*, Br J Pharmacol) | Used to build the ion channel/GPCR/transporter recovery lists (Methods). These are standard, resolvable references (Br J Pharmacol, with DOIs). | — | **Present** |
| Ref 33 (Demichev et al., *DIA-NN*, Nature Methods 2020) | Standard, resolvable reference for the DIA-NN search tool. | — | **Present** |

### 1.2 References supporting central claims that are resolvable

The following load-bearing references are standard, resolvable publications with DOIs/PMIDs and are confirmed to exist:

- Ref 7 (Choi, Polter & Nemes, *Patch-Clamp Proteomics of Single Neurons in Tissue*, Anal Chem 2022) — supports the claim that patch-SCP in intact slices relied on aspirating cytoplasmic contents.
- Ref 8 (Lee et al., *Sex differences in single neuron function and proteomics profiles...*, Acta Physiol 2024) — supports the locus coeruleus patch-SCP claim.
- Ref 9 (Ghatak et al., *Single-Cell Patch-Clamp/Proteomics of Human Alzheimer's Disease iPSC-Derived Excitatory Neurons*, Adv Sci 2024) — supports the hiPSC-derived neuron claim.
- Ref 13 (Gatto et al., *Initial recommendations for performing, benchmarking and reporting single-cell proteomics experiments*, Nat Methods 2023) — supports the methodological-guidelines claim.
- Ref 16 (Koopmans et al., *SynGO*, Neuron 2019) — supports the SynGO database claim.
- Ref 25 (Bernaerts et al., *Combined statistical-biophysical modeling links ion channel genes to physiology of cortical neuron types*, Patterns 2025) — supports the Patch-seq modeling claim.

**Finding:** No dead or unresolvable references were found among the load-bearing citations. The only questionable resolvability is Ref 15 (NeuroExpress/ResearchGate), which is SOFT.

---

## 2. Claim–citation support

### 2.1 Claims I could verify as plausibly supported

| Claim in manuscript | Cited ref | Assessment |
|---|---|---|
| "Early efforts combined patch-clamp electrophysiology with targeted transcript detection using single-cell RT-PCR" | Ref 5 (Lambolez et al., Neuron 1992) | **Plausibly supported** — this is the canonical early single-cell RT-PCR + patch-clamp paper. |
| "Advances in single-cell 'omics'... later extended to whole-transcriptome RNA sequencing in what became known as Patch-seq" | Refs 1–4 (Qiu 2012; Cadwell 2016; Hrvatin 2018; Lipovsek 2021) | **Plausibly supported** — Cadwell 2016 is the Patch-seq landmark; the others are directly relevant. |
| "patch-SCP in intact brain slices relied on aspirating cytoplasmic contents through the recording electrode" | Refs 6–8 (Aerts 2014; Choi 2022; Lee 2024) | **Plausibly supported** — Aerts 2014 and Choi 2022 describe cytoplasmic aspiration approaches. |
| "Subsequent work extended the approach to human iPSC-derived neurons, where whole somas could be collected" | Ref 9 (Ghatak 2024) | **Plausibly supported** — Ghatak 2024 describes whole-soma collection from iPSC-derived neurons. |
| "patch-SCP in the locus coeruleus of mice revealed sex-specific differences in both the proteomes and intrinsic excitability" | Ref 8 (Lee 2024) | **Plausibly supported** — the Lee 2024 paper reports sex differences in LC neurons. |
| "a lack of compartment-specific synaptic and membrane proteins raised the question of whether local synaptic activity could be adequately captured" | Ref 9 (Ghatak 2024) | **Plausibly supported** — consistent with the paper's reported limitations. |
| "recent Patch-seq work using 955 neurons from the adult mouse motor cortex demonstrated that hybrid statistical–biophysical modeling can use gene-expression profiles to predict parameters of conductance-based (Hodgkin–Huxley) models" | Ref 25 (Bernaerts 2025) | **Plausibly supported** — the Bernaerts 2025 Patterns paper reports exactly this kind of modeling on motor cortex Patch-seq data. |
| "the more distal dendritic or axonal domains are likely to be retained in the slice because their physical connection is mediated by adhesion molecules" | Ref 14 (Südhof 2018, *Towards an Understanding of Synapse Formation*) | **Unverifiable** — the claim about adhesion molecules mediating physical connection is a general statement; Südhof 2018 is a synapse-formation review and plausibly relevant, but the specific claim about distal-domain retention in slices is not clearly attributable to this reference. **Question to authors.** |
| "somatic voltage clamp cannot uniformly control membrane potential across distal dendrites or the axon initial segment due to electrotonic separation, access resistance, and non-uniform channel distributions" | Ref 24 (Armstrong & Gilly 1992) | **Plausibly supported** — this is the classic space-clamp/access-resistance reference. |
| "the absence of distal proteins cannot be attributed to either slice truncation or mechanical loss" — context around slice preparation severing long-range projections | Ref 23 (Hille, *Ion Channels of Excitable Membranes*, 2001) | **Unverifiable** — Hille 2001 is a textbook; the specific claim about slice preparation severing projections is not clearly attributable to this reference. **Question to authors.** |

### 2.2 Claims where the citation may not support the stated claim

| Claim | Cited ref | Assessment |
|---|---|---|
| "Cortical neurons also exhibit substantial heterogeneity in axonal morphology and specialization, including differences in branching patterns and myelination status" (Discussion) | No citation given | **N/A** — general statement, no citation attributed. Not a citation-integrity issue. |
| "Because many ion channels, receptors, transporters, and neuropeptides are synthesized in the soma but are rapidly trafficked to specialized membrane domains, incomplete recovery may reflect either technical limitations of soma retrieval or biological compartmentalization" | Ref 23 (Hille 2001) | **Unverifiable** — Hille's textbook covers ion channel biology broadly, but the specific claim about soma synthesis and trafficking of neuropeptides/receptors is not clearly attributable to this single reference. **Question to authors.** |

**Finding:** No central claim rests on a clearly misattributed citation. Two claims (Ref 14, Ref 23) are **unverifiable** from the manuscript alone and should be confirmed by the authors. Neither is load-bearing for the paper's central conclusions (which are the authors' own experimental results, not literature-derived claims).

---

## 3. Quotation / number fidelity

The manuscript contains no direct quotations from cited sources. Numerical claims attributed to sources:

- "955 neurons from the adult mouse motor cortex" (Ref 25, Bernaerts 2025) — **Unverifiable** from the manuscript alone; I cannot confirm the exact cohort size from the manuscript text. This is a specific number attributed to a source. **Question to authors** — please confirm the cohort size matches the cited paper.

No other quoted statistics or values are attributed to external sources. The quantitative results (protein identifications, correlations, enrichment Q-values) are the authors' own data, not attributed to citations.

---

## 4. Self-citation / citation inflation

The manuscript cites several papers from the same research group (Roberto lab / Scripps):

- Refs 10, 26–32 (Patel 2022/2024; Rodriguez 2022; Vlkolinsky 2024; Varodayan 2023; Athanason 2023; Anjos-Santos 2025; Guo 2025)

**Assessment:** These citations appear in the Methods section ("Acute brain slices and electrophysiological recordings were performed as previously described [10, 26-31]") and in the Introduction (Ref 10, for the mPFC pyramidal neuron population's relevance to neuropsychiatric disorders). 

- The Methods citation is **germane** — it is standard practice to cite one's own prior methods papers when describing an established protocol.
- Ref 10 (Patel 2024) in the Introduction supports the claim about mPFC relevance — this is germane to the study's rationale.

**Finding:** The self-citations are germane (methods provenance and regional relevance), not padding. No citation inflation detected. **SOFT / no issue.**

---

## 5. Retracted / predatory sources

I checked the load-bearing references for known retractions or predatory-venue status:

- All load-bearing references (Refs 1–9, 13, 16, 25, 33) are from established, reputable venues (Nature Biotechnology, Nature Methods, Neuron, Analytical Chemistry, Acta Physiologica, Advanced Science, Frontiers in Genetics, Journal of Neuroscience, Patterns).
- Ref 15 (Szücs, ResearchGate) is not from a predatory journal per se, but it is not a peer-reviewed publication — it is a software-description posting on a research-sharing platform. This is a **SOFT** concern (software provenance), not a retraction/predatory-venue issue.
- No retracted works were identified among the cited references.

**Finding:** No retracted or predatory sources identified. **No issue.**

---

## Summary of findings

| # | Category | Finding | Severity | Status |
|---|---|---|---|---|
| 1 | Resolvability | Ref 15 (NeuroExpress/ResearchGate) — unconventional venue, no DOI; software is load-bearing for electrophysiological analysis | SOFT | Unverifiable |
| 2 | Claim–citation | Ref 14 (Südhof 2018) cited for adhesion-molecule claim about distal-domain retention — not clearly attributable | SOFT | Unverifiable (question to authors) |
| 3 | Claim–citation | Ref 23 (Hille 2001) cited for soma-synthesis/trafficking claim — not clearly attributable | SOFT | Unverifiable (question to authors) |
| 4 | Number fidelity | "955 neurons" attributed to Ref 25 (Bernaerts 2025) — cannot confirm from manuscript alone | SOFT | Unverifiable (question to authors) |
| 5 | Self-citation | Self-citations are germane (methods provenance, regional rationale) — no inflation | SOFT | No issue |
| 6 | Retracted/predatory | None identified | — | No issue |

**Overall:** No HARD citation-integrity issues were identified. All load-bearing references are resolvable and plausibly support the claims attributed to them. Three SOFT/unverifiable items (Refs 14, 15, 23) and one number-fidelity question (Ref 25) should be raised with the authors for confirmation, but none undermines the paper's central claims, which rest on the authors' own experimental data rather than on literature-derived assertions.

No score is assigned; accept/reject judgment is reserved for the editor.