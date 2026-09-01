# Methods Completeness & Reagent Traceability Audit

## Scope & Trigger Detection

This manuscript describes **mcp-proto-okn**, a Python-based Model Context Protocol server for querying biomedical knowledge graphs. The work is primarily a **software tool/infrastructure paper** with two illustrative case studies. 

**Triggered checklist categories:**
- Cross-cutting items (software versions, data/code availability)
- Computational/ML/modeling (tool implementation, case study workflows)
- Genomics/sequencing/omics (Case Study 1 references RNA-seq data)
- Human subjects/clinical (Case Study 1 involves NASA spaceflight studies; Case Study 2 involves dataset discovery)

**Not triggered:** Antibodies, cell lines, model organisms (in vivo), chemicals/drugs, oligos/plasmids, mass spec, microscopy, direct human subject recruitment.

---

## Cross-Cutting Items (Apply to All Manuscripts)

### Software, Tool, and Instrument Versions

**Status: HARD MISSING**

- **FastMCP framework version:** Not specified. Manuscript states "implemented in Python using the FastMCP framework" but provides no version number, release date, or commit hash.
- **Python version:** Not stated.
- **Dependency versions:** No requirements.txt, setup.py, pyproject.toml, or environment specification provided in the manuscript. The GitHub repository is referenced but version pinning is not documented in the text.
- **UberGraph version/access date:** The manuscript references UberGraph for ontology expansion but does not specify which version of UberGraph was queried or when the queries were executed (UberGraph is a live service; snapshot dates matter for reproducibility).
- **SPARQL endpoint versions:** The OKN Fabric SPARQL endpoint (https://frink.apps.renci.org/federation/sparql) is referenced, but no version, deployment date, or schema snapshot is provided.

**Impact:** A researcher attempting to reproduce the case studies cannot guarantee they are using the same software stack or querying the same endpoint state.

---

### Data Availability Statement

**Status: HARD MISSING**

- **No formal data-availability statement** is present in the manuscript.
- **Case Study 1 (spaceflight RNA-seq):** References NASA GeneLab study OSD-244 but does not provide a persistent identifier, accession number, or URL where the raw data can be accessed. The chat transcript is linked to GitHub but the underlying genomic data is not cited with a repository accession (GEO, SRA, or NASA GeneLab direct link).
- **Case Study 2 (NDE dataset discovery):** The NIAID Data Ecosystem (NDE) is queried, but no snapshot, query results, or derived data are deposited or linked.
- **Knowledge graph snapshots:** The Proto-OKN graphs are live services on the OKN Fabric. No versioned snapshots, RDF dumps, or query result sets are provided to allow future reproduction if the graphs change.

**Impact:** The case studies cannot be independently verified or reproduced because the underlying data sources are not persistently archived or cited with accessions.

---

### Code Availability

**Status: SOFT PRESENT; HARD UNVERIFIABLE**

- **Manuscript statement:** "mcp-proto-okn is available at https://github.com/sbl-sdsc/mcp-proto-okn."
- **Status in manuscript:** The GitHub URL is provided, but the manuscript does not specify:
  - A release version, tag, or commit hash pinned to the version used for the case studies.
  - Whether the repository is public and open-source (license not stated in the manuscript).
  - Whether the code is complete and runnable as-is, or whether additional setup/secrets are required.
  
- **Case study code:** The chat transcripts are linked (e.g., "https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke-genelab-OSD-244_verbatim.md"), but these are conversation logs, not reproducible scripts. The underlying LLM prompts and assistant logic are not provided.

**Impact:** The GitHub repository is referenced but not pinned to a specific version. A reader cannot confirm which exact code version produced the results shown.

---

## Computational/ML/Modeling Category

### Dataset(s) with Version and Train/Val/Test Split

**Status: HARD MISSING / UNVERIFIABLE**

- **Case Study 1 (Spaceflight gene expression):**
  - Dataset: NASA GeneLab OSD-244 (Rodent Research-6, SpaceX-13 mission).
  - **Missing:** No accession number (e.g., GEO GSE#, SRA #) provided in the manuscript.
  - **Missing:** No specification of which samples were included (n per group, time points, replicates).
  - **Missing:** No reference to the raw RNA-seq data repository or a persistent link.
  - The chat transcript mentions "matched Space Flight versus Ground Control comparisons at ~30 and ~60 days" and "thousands of significant genes," but no sample size (n) is stated for the differential-expression analysis.

- **Case Study 2 (NDE dataset discovery):**
  - Dataset: NIAID Data Ecosystem (NDE), queried for MONDO disease URIs.
  - **Missing:** No snapshot date, version, or accession for the NDE data used.
  - **Missing:** No specification of how many datasets were in the NDE at the time of query, or whether results are reproducible if the NDE is updated.
  - The result states "over 10,000 individual datasets" but does not provide a persistent link to the query results or a downloadable dataset.

---

### Architecture/Algorithm and Hyperparameters

**Status: SOFT PRESENT**

- **Architecture:** The manuscript describes the tool's functional organization (five categories of tools: discovery, schema/query-construction, query execution, ontology/federation, documentation). This is adequate for understanding the system design.
- **Hyperparameters:** 
  - Ontology expansion batching: "expanded URI set was queried in 80 batches to respect endpoint limits" — the batch size is not specified (SOFT MISSING).
  - No tuning parameters, thresholds, or configuration options are documented.

---

### Training Procedure, Optimizer, Learning Schedule, Early Stopping

**Status: NOT APPLICABLE**

This is a tool/infrastructure paper, not a machine-learning model paper. The case studies use an LLM assistant (Claude or similar) but do not train or fine-tune models. No training procedure applies.

---

### Library Versions and Hardware

**Status: HARD MISSING**

- **Python libraries:** No requirements.txt or dependency list is provided in the manuscript.
- **FastMCP version:** Not specified (see Cross-Cutting section above).
- **Hardware:** No specification of where the server runs, what computational resources are required, or what hardware was used for the case studies.
- **LLM model:** The case studies reference "AI assistants" and mention "Claude Desktop, ChatGPT, or another compatible assistant," but do not specify which model version (e.g., Claude 3.5 Sonnet, GPT-4) was used for the case studies.

**Impact:** Reproducibility requires knowing the exact LLM model and version, as different models may generate different SPARQL queries and results.

---

### Random Seeds or Seed-Averaging Statement

**Status: NOT APPLICABLE / SOFT MISSING**

- The case studies do not involve stochastic processes or machine learning with random initialization.
- However, LLM outputs are non-deterministic. The manuscript does not state whether the case study results are single runs or averaged over multiple LLM calls, nor does it discuss variability in LLM-generated SPARQL queries.

---

### Code Availability (Reproducible Scripts)

**Status: HARD UNVERIFIABLE**

- **GitHub repository:** Provided (https://github.com/sbl-sdsc/mcp-proto-okn).
- **Reproducible scripts for case studies:** The chat transcripts are provided as Markdown logs, not as executable Python scripts or prompt templates. A reader cannot re-run the exact same prompts and queries without manually reconstructing them from the transcript.
- **LLM prompt templates:** Not provided in the manuscript or (as far as can be verified from the text) in the repository.

**Impact:** The case studies are illustrative but not reproducible as executable workflows.

---

## Genomics/Sequencing/Omics Category (Case Study 1 Trigger)

### Platform, Mode, Library-Prep Kit, Depth/Coverage, Reference Genome

**Status: HARD MISSING / UNVERIFIABLE**

- **Case Study 1 references:** "RNA-seq" from NASA GeneLab study OSD-244 (Rodent Research-6, SpaceX-13 mission).
- **Missing from manuscript:**
  - Sequencing platform (Illumina, PacBio, Oxford Nanopore, etc.) — not stated.
  - Read length and single/paired-end — not stated.
  - Library-prep kit — not stated.
  - Sequencing depth/coverage — not stated.
  - Reference genome (species, build, version) — not stated.
  
- **Delegation to external source:** The manuscript does not provide a DOI, PMID, or accession number for the OSD-244 study. The chat transcript references "NASA GeneLab study OSD-244" but does not cite a publication or data repository link that would contain these details.

**Impact:** The RNA-seq methods cannot be verified from the manuscript alone. A reader cannot confirm the data quality, alignment parameters, or differential-expression methodology.

---

### Alignment/Analysis Tools WITH Versions and Key Parameters

**Status: HARD MISSING**

- **Differential-expression analysis:** The case study mentions "Differential-expression analysis revealed thousands of significant genes" and reports "Pearson correlation coefficient = 0.80" between time points, but does not specify:
  - Which tool was used (DESeq2, edgeR, limma, etc.).
  - Tool version.
  - Statistical test (e.g., Wald test, likelihood-ratio test).
  - Significance threshold (p-value, adjusted p-value, log-fold-change cutoff).
  - Whether results came from the SPOKE-GeneLab KG directly or were re-computed.

- **Cross-species ortholog mapping:** The case study states "The assistant then mapped mouse genes to human orthologs," but does not specify:
  - Which tool or database was used (Ensembl, NCBI HomoloGene, InParanoid, etc.).
  - Version.
  - Ortholog confidence/quality filtering.

**Impact:** The differential-expression results and cross-species translation cannot be independently verified.

---

### Repository Accession (GEO/SRA/ENA)

**Status: HARD MISSING**

- **Case Study 1:** No GEO, SRA, or NASA GeneLab accession number is provided for OSD-244 in the manuscript.
- **Case Study 2:** No accession or snapshot of NDE query results is provided.

**Impact:** The data cannot be retrieved or verified by independent readers.

---

## Human Subjects/Clinical Category (Case Study 1 & 2 Triggers)

### IRB Approval and Informed Consent

**Status: NOT APPLICABLE / UNVERIFIABLE**

- **Case Study 1 (Spaceflight study):** References a NASA GeneLab study (OSD-244, Rodent Research-6). This is a **rodent study, not human subjects research**, so IRB approval does not apply. However, IACUC approval would be required (see below).
- **Case Study 2 (NDE dataset discovery):** This is a **secondary analysis / data discovery task**, not primary human subjects research. The datasets in NDE may contain human data, but the manuscript does not involve recruiting or consenting participants. IRB approval is not applicable to the manuscript itself.

---

### IACUC Protocol # (Case Study 1 Trigger — Rodent Study)

**Status: HARD MISSING**

- **Case Study 1 references:** "Rodent Research-6 spaceflight study" involving "Mus musculus thymus by RNA-seq."
- **Missing:** No IACUC protocol number, approval date, or institution is provided.
- **Delegation:** The manuscript references "NASA GeneLab study OSD-244" but does not cite a publication or repository entry that would contain IACUC details.

**Impact:** Animal welfare compliance cannot be verified.

---

### Randomization and Blinding Statement

**Status: HARD MISSING / UNVERIFIABLE**

- **Case Study 1:** The case study mentions "matched Space Flight versus Ground Control comparisons" but does not state:
  - Whether animals were randomly assigned to flight vs. ground control.
  - Whether sample processing or sequencing was blinded.
  - Whether analysis was blinded to group assignment.

**Impact:** Bias assessment is not possible.

---

## Summary of Findings

| **Category** | **Item** | **Severity** | **Status** | **Note** |
|---|---|---|---|---|
| **Cross-Cutting** | FastMCP version | HARD | Missing | No version, release date, or commit hash. |
| **Cross-Cutting** | Python version | HARD | Missing | Not specified. |
| **Cross-Cutting** | Dependency versions | HARD | Missing | No requirements.txt or environment file in manuscript. |
| **Cross-Cutting** | UberGraph version/snapshot date | HARD | Missing | Live service; snapshot date needed for reproducibility. |
| **Cross-Cutting** | SPARQL endpoint version/snapshot | HARD | Missing | OKN Fabric endpoint state not documented. |
| **Cross-Cutting** | Data-availability statement | HARD | Missing | No formal statement; underlying data not persistently archived. |
| **Cross-Cutting** | Code version pinning | HARD | Unverifiable | GitHub URL provided but no release tag or commit hash. |
| **Computational** | Case Study 1: Dataset accession (RNA-seq) | HARD | Missing | No GEO/SRA accession for OSD-244. |
| **Computational** | Case Study 1: Sample size (n per group) | HARD | Missing | Number of animals/samples not stated. |
| **Computational** | Case Study 2: NDE snapshot/version | HARD | Missing | No date or version for NDE query. |
| **Computational** | Case Study 2: Query results archive | HARD | Missing | Results not deposited or persistently linked. |
| **Computational** | Ontology expansion batch size | SOFT | Missing | "80 batches" mentioned but batch size not specified. |
| **Computational** | LLM model version | HARD | Missing | Claude/GPT model version not specified for case studies. |
| **Genomics** | Sequencing platform | HARD | Missing | Not stated for OSD-244. |
| **Genomics** | Read length, single/paired-end | HARD | Missing | Not stated. |
| **Genomics** | Library-prep kit | HARD | Missing | Not stated. |
| **Genomics** | Sequencing depth/coverage | HARD | Missing | Not stated. |
| **Genomics** | Reference genome (build/version) | HARD | Missing | Not stated. |
| **Genomics** | Differential-expression tool & version | HARD | Missing | Tool not named; version not provided. |
| **Genomics** | DE statistical test & thresholds | HARD | Missing | Test type, p-value cutoff, log-FC threshold not stated. |
| **Genomics** | Ortholog mapping tool & version | HARD | Missing | Tool not named; version not provided. |
| **Genomics** | Repository accession (GEO/SRA) | HARD | Missing | No accession provided. |
| **Human Subjects** | IACUC protocol # (rodent study) | HARD | Missing | OSD-244 is a rodent study; IACUC approval not documented. |
| **Human Subjects** | Randomization statement | HARD | Missing | Flight vs. control assignment method not stated. |
| **Human Subjects** | Blinding statement | HARD | Missing | No mention of blinding in sample processing or analysis. |

---

## Key Questions for Authors

1. **Software reproducibility:** Please provide a pinned version (release tag or commit hash) for mcp-proto-okn, FastMCP, and all dependencies (requirements.txt or environment.yml).

2. **Case Study 1 data:** Please provide the GEO or SRA accession number for NASA GeneLab OSD-244, or a persistent link to the raw RNA-seq data. Include sample size (n per group), sequencing platform, library-prep kit, and reference genome build.

3. **Case Study 1 analysis:** Please specify the differential-expression tool (e.g., DESeq2), version, statistical test, and significance thresholds used. Specify the ortholog mapping tool and version.

4. **Case Study 1 compliance:** Please provide the IACUC protocol number and approval date for the Rodent Research-6 spaceflight study.

5. **Case Study 2 data:** Please provide a snapshot date for the NDE query, or a persistent link to the query results and dataset list.

6. **LLM reproducibility:** Please specify which LLM model and version (e.g., Claude 3.5 Sonnet, GPT-4 Turbo) was used for the case studies. Provide the exact prompts or a template that readers can use to reproduce the workflows.

7. **Knowledge graph versions:** Please document the version or snapshot date of the OKN Fabric SPARQL endpoint and each Proto-OKN graph queried.

---

## Conclusion

This manuscript describes a useful infrastructure tool but lacks the methodological detail and data traceability required for independent reproduction of the case studies. The most critical gaps are:

- **No persistent data identifiers** for the RNA-seq study (Case Study 1) or NDE snapshot (Case Study 2).
- **No software version pinning** for the tool itself, its dependencies, or the LLM models used.
- **No genomics methods details** (platform, kit, tool versions, thresholds) for Case Study 1.
- **No IACUC documentation** for the rodent study.

These are HARD missing items that prevent independent verification and reproduction.