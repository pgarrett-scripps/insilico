# Citation Integrity Audit Report

## Scope and Method

This manuscript presents a pilot evaluation of open-weight large language models (LLMs) for screening RNA-seq metadata. The audit checks:

1. **Reference resolvability**: whether in-text citations map to specific, resolvable references
2. **Claim–citation support**: whether factual claims attributed to cited works are plausibly contained in those works
3. **Quotation/number fidelity**: whether quoted or numerical claims match their sources
4. **Retracted/predatory sources**: whether any cited work is flagged as retracted or from a known predatory venue

The manuscript contains 19 numbered references in the reference list. I will check load-bearing citations (those supporting core claims about methods, prior work, or results) and verify a sample of factual claims.

---

## Findings by Category

### 1. Reference Resolvability

**Status: CRITICAL GAPS IDENTIFIED**

The reference list provided is **severely incomplete and malformed**. The entries are:

```
bay146 (2019).
Rev. Genet. 10, 57–63 (2009).
Res. 50, D387–D390 (2022).
update. Nucleic Acids Res. 52, D138–D144 (2024).
acid-related abiotic stresses in Arabidopsis thaliana. Front. Plant Sci. 15, 1343787 (2024).
```

These are **fragments only**—they lack:
- Author names
- Full titles
- Complete journal names (e.g., "Rev. Genet." is incomplete; "Res." is a fragment)
- DOIs or PMIDs
- In most cases, the first author or any author name

The manuscript text references 19 numbered citations (e.g., "1", "2", "3"... "19" in the Methods and Discussion), but the reference list provided contains only 5 partial entries. **The remaining 14 references are not present in the provided reference list block.**

**Severity: HARD**

This is a **blocking issue**. A reader cannot:
- Verify any claim against its source
- Locate the cited work
- Assess whether the citation supports the claim
- Reproduce or build on the work

---

### 2. Load-Bearing Citations: Spot Checks

I attempted to verify several key claims against the reference list. Because the reference list is incomplete and fragmented, I cannot confirm support for the following load-bearing claims:

#### Claim: "GEOmetaDB has been proposed as a local database and query layer" (line 7, Methods intro)
- **Cited as**: Reference 7
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD (this is a foundational prior-work claim)

#### Claim: "PysRADB supports large-scale retrieval of study and sample metadata" (line 8, Methods intro)
- **Cited as**: Reference 8
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD

#### Claim: "PubTator assists in biocuration by automatically extracting and normalizing major entities" (line 9, Methods intro)
- **Cited as**: Reference 9
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD

#### Claim: "PubTator 3.0 enables semantic and relational search over biomedical literature using AI techniques" (line 10, Methods intro)
- **Cited as**: Reference 10
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD

#### Claim: "LLMs learn from large text corpora and can capture complex patterns in natural languages" (line 11, Introduction)
- **Cited as**: Reference 11
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: SOFT (general background claim, not central to the study's novel contribution)

#### Claim: "GPT-4 was released in 2023 and marked a clear expansion in practical capabilities of LLMs" (line 12, Introduction)
- **Cited as**: Reference 12
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: SOFT (factual background, but not central to the study's methodology or results)

#### Claim: "LLM-assisted methods have been shown to improve extraction performance compared with traditional rule-based methods" (line 13, Introduction)
- **Cited as**: Reference 13
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD (this is a key motivation for the study)

#### Claim: "Generative models can support curation workflows that consider ontologies" (line 14, Introduction)
- **Cited as**: Reference 14
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: HARD (cited as evidence that LLMs can support curation)

#### Claim: "LM Arena evaluates model performance by running the same tasks with two anonymized models on a website and collecting user votes in an A/B test setting" (lines 15–16, Introduction)
- **Cited as**: References 15 and 16
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (references missing from list)
- **Severity**: SOFT (background on evaluation methodology, not central to the study's own evaluation)

#### Claim: "gpt-oss-20B and gpt-oss-120B are open-weight models released by OpenAI in August 2025" (line 17, Introduction)
- **Cited as**: Reference 17
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: SOFT (factual claim about model release, but not central to the study's results)

#### Claim: "Qwen3 adopts a highly sparse MoE design wherein, despite having 30 B or 80 B parameters, only approximately 3 B parameters are selectively used" (line 18, Results)
- **Cited as**: Reference 18
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: SOFT (technical detail about model architecture)

#### Claim: "TogoID is an exploratory ID converter to bridge biological datasets" (line 19, Methods)
- **Cited as**: Reference 19
- **Reference list entry**: Not present in provided list
- **Status**: UNVERIFIABLE (reference missing from list)
- **Severity**: SOFT (tool description, not central to the study's methodology)

---

### 3. Claim–Citation Support

**Status: CANNOT ASSESS**

Because 14 of 19 references are missing from the provided reference list, I cannot verify whether the claims attributed to them are actually supported by those works. The 5 partial entries provided are too fragmented to assess claim support:

- Entry 1: "bay146 (2019)" — no title, no authors, no journal. Unresolvable.
- Entry 2: "Rev. Genet. 10, 57–63 (2009)" — no authors, no title, journal name incomplete.
- Entry 3: "Res. 50, D387–D390 (2022)" — no authors, no title, journal name is a fragment.
- Entry 4: "update. Nucleic Acids Res. 52, D138–D144 (2024)" — appears to be a fragment of a title or subtitle; no authors.
- Entry 5: "acid-related abiotic stresses in Arabidopsis thaliana. Front. Plant Sci. 15, 1343787 (2024)" — appears to be a fragment of a title; no authors.

**Severity: HARD**

---

### 4. Quotation and Number Fidelity

**Status: CANNOT ASSESS**

The manuscript does not appear to contain direct quotations from cited works (it paraphrases throughout). However, it does cite specific numerical claims (e.g., "GPT-4 was released in 2023", "gpt-oss models released in August 2025"). These cannot be verified against the reference list because the references are missing or fragmented.

**Severity: HARD**

---

### 5. Retracted or Predatory Sources

**Status: CANNOT ASSESS**

Because the reference list is incomplete and fragmented, I cannot reliably identify the full citations or check them against retraction databases or predatory venue lists. However, I note that the journals mentioned in the fragments (e.g., *Nucleic Acids Research*, *Frontiers in Plant Science*) are legitimate, peer-reviewed venues.

---

## Summary of Audit Findings

| Category | Status | Severity | Finding |
|----------|--------|----------|---------|
| **Reference Resolvability** | CRITICAL FAILURE | HARD | 14 of 19 references are missing from the provided reference list; 5 remaining entries are fragmented (missing authors, titles, complete journal names, DOIs/PMIDs). |
| **Claim–Citation Support** | UNVERIFIABLE | HARD | Cannot verify whether claims are supported by cited works because references are missing or incomplete. |
| **Quotation/Number Fidelity** | UNVERIFIABLE | HARD | Cannot verify numerical claims against sources because references are missing. |
| **Retracted/Predatory Sources** | CANNOT ASSESS | — | Insufficient information to check; journals mentioned appear legitimate. |

---

## Recommendations for Authors

1. **Provide the complete reference list** with all 19 references in full format, including:
   - All author names
   - Full article titles
   - Complete journal names
   - Volume, issue, and page numbers
   - DOI or PMID for each entry

2. **Verify that all in-text citations (1–19) have corresponding entries** in the reference list.

3. **Ensure each reference is resolvable** via DOI, PMID, or other standard identifier.

4. **Confirm that each cited claim is actually supported** by the cited work (spot-check a sample after providing the full list).

---

## Conclusion

**This manuscript cannot be audited for citation integrity in its current form.** The reference list is incomplete and fragmented, making it impossible to verify whether the manuscript's claims are supported by cited works or whether the work can be reproduced or built upon by readers. This is a **blocking issue** that must be resolved before the manuscript can proceed to peer review.