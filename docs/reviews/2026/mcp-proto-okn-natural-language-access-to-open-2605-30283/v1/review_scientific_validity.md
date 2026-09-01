# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a well-executed systems paper that makes a genuine contribution to accessibility of fragmented biomedical knowledge graphs through natural language. The core claims—that mcp-proto-okn enables discovery and querying of Proto-OKN graphs without SPARQL expertise, and that ontology expansion recovers relevant records missed by naive queries—are both supported by the evidence presented. The work is sound, the use cases are concrete and reproducible, and the limitations are acknowledged. It merits publication with minor revision to clarify one design choice and strengthen the scope statement.

## Strengths

1. The paper demonstrates a real problem (30+ heterogeneous graphs with no common schema, requiring domain expertise to query) and a pragmatic solution that integrates naturally with existing LLM infrastructure.

2. Both use cases are end-to-end and reproducible: the authors provide chat transcripts, specific study identifiers (OSD-244), and quantified outcomes (322 concordant genes, 1,592 descendant URIs, 10,000+ datasets retrieved).

3. The ontology expansion mechanism is well-motivated and shows clear impact: expanding one MONDO URI from 447 to 10,000+ datasets by retrieving descendants, with concrete disease subtypes listed to show the method captures both common and rare conditions.

## Load-Bearing Claims

**Claim 1: mcp-proto-okn enables natural-language access to Proto-OKN graphs without requiring SPARQL expertise.**

The evidence is the two use cases, both conducted "entirely through natural language queries" (Results, Case Study 1). However, the manuscript does not report whether the LLM assistant succeeded on first attempt, required iterative refinement, or failed on any queries. The chat transcripts are linked but not included in the paper itself, so I cannot inspect them. The claim that the system "enables" access is supported by the fact that queries were executed and results were returned, but the ease, reliability, and failure rate remain opaque. This is not a design flaw—the system clearly works—but the scope of the claim ("enables access") is not distinguished from the stronger claim ("reliably and intuitively enables access without expert intervention"). The paper would benefit from stating explicitly whether the transcripts shown are representative or cherry-picked, and whether any queries failed or required assistant prompting to reformulate.

**Claim 2: Ontology expansion via UberGraph descendants recovers relevant records that naive single-URI queries miss.**

The evidence is Case Study 2: a query for "cardiovascular disease" (MONDO:0004995) returned 447 datasets with the root URI alone, but 10,000+ datasets when the query was rewritten to include 1,592 descendant URIs. This is a direct comparison and the mechanism is clear. However, the paper does not report the precision cost: how many of the 10,000+ results are false positives (e.g., datasets tagged with rare cardiovascular syndromes that are not actually relevant to a user asking about "cardiovascular disease" broadly)? The expansion is automatic and configurable, but the manuscript does not show what happens when the user did not intend such breadth. A user asking "what datasets study cardiovascular disease?" might reasonably expect datasets on heart failure, but might not expect datasets on Brugada syndrome or Holt-Oram syndrome, even though these are cardiovascular. The paper frames this as a feature (surfacing rare conditions) but does not quantify the trade-off between recall and precision, or show how the assistant handles the expanded result set in conversation. This is a SOFT weakness: the claim is defensible if narrowed to "ontology expansion increases recall," but the current framing ("bridges user-level concepts and curator-level annotations") glosses over the precision question.

## Sweep

1. The paper claims mcp-proto-okn supports "multi-graph querying" and "coordinated execution across multiple graphs," but the two use cases each query one or two graphs sequentially; no example shows a single query that joins across three or more graphs, so the scope of "coordinated" is unclear.

2. The spaceflight case study (Case Study 1) maps mouse genes to human orthologs and then queries spoke-okn for disease associations, but the manuscript does not report how many orthologs were successfully mapped, whether any were ambiguous, or whether the mapping step introduced errors that propagated downstream.

3. The paper states that mcp-proto-okn "mitigates" schema heterogeneity through "schema-inspection tools" and "warning metadata," but does not show an example of a warning or explain what happens when two graphs use the same predicate with different semantics.

4. The availability statement links to a GitHub repository but does not specify whether the code is versioned, whether dependencies are pinned, or what Python version is required.

5. The paper does not discuss latency: federated SPARQL queries across 30+ endpoints, especially with ontology expansion requiring 80 batches, may take minutes; user experience implications are not addressed.

6. The claim that mcp-proto-okn "lowers the barrier for integrative discovery" is not quantified: no comparison to the time or expertise required to write equivalent SPARQL queries by hand, or to the error rate of LLM-generated queries without the server's schema-inspection tools.

7. The paper mentions "configurable expansion bounds" for ontology expansion but does not show what bounds were used in Case Study 2 or how a user would set them.

8. The introduction cites Emonet et al. 2025 and Kinjo et al. 2026 as prior work on LLM-to-SPARQL translation, but does not explain what mcp-proto-okn does differently beyond "routing between graphs" and "hierarchical reasoning over reference ontologies"—these are stated as differences but not demonstrated as novel.

## Questions

- The chat transcripts are linked but not included in the manuscript; can you confirm they are permanently archived and accessible to readers who may not have GitHub access?

- In Case Study 2, what was the wall-clock time to execute the expanded query across 80 batches, and did the assistant present all 10,000+ results to the user or summarize them?

- How does the system handle cases where a user's natural-language question is ambiguous between two graphs (e.g., "genes" could refer to spoke-okn or spoke-genelab)—does the assistant ask for clarification, query both, or use heuristics to choose?