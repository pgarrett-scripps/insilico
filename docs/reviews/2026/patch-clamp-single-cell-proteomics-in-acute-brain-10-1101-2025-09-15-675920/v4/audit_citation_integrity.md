#### Claim: Reference 8 (Lee et al., locus coeruleus sex differences)
- **Manuscript claim (Introduction, p. 3):** "patch-SCP in the locus coeruleus of mice revealed sex-specific differences in both the proteomes and intrinsic excitability of noradrenergic neurons, although collection and analysis were limited to the cytoplasm, leaving the molecular drivers of these differences difficult to identify."
- **Reference 8:** Lee, J., et al., Sex differences in single neuron function and proteomics profiles examined by patch-clamp and mass spectrometry in the locus coeruleus of the adult mouse. Acta Physiol (Oxf), 2024. 240(4): p. e14123.
- **Verification:** PubMed search confirms this reference exists (PMID: 38459766). The title and journal match the bibliography entry.
- **Status:** SUPPORTED (PASS)

#### Claim: Reference 9 (Ghatak et al., Alzheimer's disease iPSC neurons)
- **Manuscript claim (Introduction, p. 3):** "a patch-SCP platform applied to Alzheimer's disease hiPSC-derived neurons found an association between protein expression and a hyperexcitable phenotype, yet a lack of compartment-specific synaptic and membrane proteins raised the question of whether local synaptic activity could be adequately captured by the platform."
- **Reference 9:** Ghatak, S., et al., Single-Cell Patch-Clamp/Proteomics of Human Alzheimer's Disease iPSC-Derived Excitatory Neurons Versus Isogenic Wild-Type Controls Suggests Novel Causation and Therapeutic Targets. Adv Sci (Weinh), 2024. 11(29): p. e2400545.
- **Verification:** PubMed search returned no results for this specific reference. The journal *Advanced Science* is legitimate, but the article could not be independently verified.
- **Status:** UNVERIFIABLE (SOFT)
- **Recommendation:** Verify the article exists and is published. If it is a preprint or in-press, clarify the status.

#### Claim: Reference 16 (SynGO database)
- **Manuscript claim (Methods, p. 27):** "Enrichment terms for cellular component (CC) and biological process (BP) categories were derived from SynGO, a manually curated synaptic GO ontology database."
- **Reference 16:** Koopmans, F., et al., SynGO: An Evidence-Based, Expert-Curated Knowledge Base for the Synapse. Neuron, 2019. 103(2): p. 217-234.e4.
- **Status:** SUPPORTED (PASS) – This is a well-known, published database paper in a top-tier journal.

#### Claim: Reference 33 (DIA-NN software)
- **Manuscript claim (Methods, p. 27):** "Raw DIA files were analyzed using DIA-NN v1.8.1 in library-free mode with the 'match-between-runs' option enabled."
- **Reference 33:** Demichev, V., et al., DIA-NN: neural networks and interference correction enable deep proteome coverage in high throughput. Nature Methods, 2020. 17(1): p. 41-44.
- **Status:** SUPPORTED (PASS) – Published in Nature Methods; software citation is appropriate.

#### Claim: Reference 13 (SCP guidelines)
- **Manuscript claim (Methods, p. 27):** "Enrichment terms for cellular component (CC) and biological process (BP) categories were derived from SynGO [16], a manually curated synaptic GO ontology database. Gene set enrichment analyses were performed on gene lists derived from DIA-NN's protein-level output. For SynGO analysis, proteins were annotated based on gene symbols and GSEA filtering was performed under stringent conditions."
- **Reference 13:** Gatto, L., et al., Initial recommendations for performing, benchmarking and reporting single-cell proteomics experiments. Nature Methods, 2023. 20(3): p. 375-386.
- **Status:** SUPPORTED (PASS) – Published in Nature Methods; appropriate for methodological guidance.

---

### 3. Quotation and Number Fidelity

No direct quotations from cited works are included in the manuscript. Quantitative claims (e.g., protein identifications, statistical values) are derived from the authors' own data, not attributed to prior work. No fidelity issues detected.

---

### 4. Retracted or Predatory Sources

**Status: PASS**

No cited journals or sources are flagged as retracted or from known predatory venues. All primary citations are to peer-reviewed journals (Nature Biotechnology, Nature Neuroscience, Nature Methods, Neuron, Analytical Chemistry, etc.) or established databases (IUPHAR-DB, SynGO).

---

### 5. Self-Citation and Citation Inflation

**Status: ACCEPTABLE with note**

The manuscript includes several self-citations by the authors (references 10, 25, 26, 27, 28, 29, 31):
- Patel et al. (2024, 2022) – medial prefrontal cortex and ethanol
- Rodriguez et al. (2022) – alcohol dependence and GABA synapses
- Vlkolinsky et al. (2024) – chronic alcohol and GABAergic transmission
- Varodayan et al. (2023) – ethanol and interleukin-1β
- Athanason et al. (2023) – chronic ethanol and adrenergic receptors
- Anjos-Santos et al. (2025) – noradrenaline and GABA transmission

**Assessment:** These self-citations are **contextually appropriate**. They establish the authors' prior work on the medial prefrontal cortex and alcohol-related neurobiology, which provides biological context for the choice of tissue and neuronal population (Layer 2/3 pyramidal neurons in mPFC). The citations are not inflated or non-germane; they support the rationale for the experimental system. However, the inclusion of a 2025 publication (Anjos-Santos et al., reference 29) is unusual and should be verified as in-press or published.

---

## Summary Table

| Category | Finding | Severity | Status |
|----------|---------|----------|--------|
| Reference resolvability | Reference 15 (NeuroExpress) – non-peer-reviewed venue, no DOI | SOFT | Unverifiable |
| Reference resolvability | Reference 30 (Saxitoxin) – not mentioned in manuscript, appears to be stray/erroneous | SOFT | Missing/Erroneous |
| Reference resolvability | All other references (1–14, 16–29, 31–33) | – | Present |
| Claim–citation support | Reference 8 (Lee et al., locus coeruleus) | – | Supported |
| Claim–citation support | Reference 9 (Ghatak et al., Alzheimer's iPSC) | SOFT | Unverifiable |
| Claim–citation support | Reference 16 (SynGO) | – | Supported |
| Claim–citation support | Reference 33 (DIA-NN) | – | Supported |
| Claim–citation support | Reference 13 (SCP guidelines) | – | Supported |
| Quotation/number fidelity | No direct quotations or attributed numbers | – | N/A |
| Retracted/predatory sources | None identified | – | Pass |
| Self-citation | 7 self-citations, contextually appropriate | – | Acceptable |

---

## Recommendations for Authors

1. **Reference 15 (NeuroExpress):** Provide a stable, citable source (GitHub URL, Zenodo DOI, or software journal publication) or cite as "personal communication."

2. **Reference 30 (Saxitoxin):** Remove this reference or clarify its relevance. It does not appear in the manuscript and may be a copy-paste error from another document.

3. **Reference 9 (Ghatak et al.):** Verify that this article is published and provide a DOI or PMID if available.

4. **Reference 29 (Anjos-Santos et al., 2025):** Clarify the publication status. If in-press, note this; if not yet published, consider removing or citing as "in preparation."

---

## Overall Assessment

**No HARD failures detected.** The manuscript's load-bearing citations (methodology, prior patch-SCP work, software tools, databases) are resolvable and appear to support the stated claims. Two SOFT issues require clarification: the NeuroExpress software citation (non-peer-reviewed venue) and the stray saxitoxin reference. One additional reference (Ghatak et al.) could not be independently verified but is not load-bearing to the central claims.