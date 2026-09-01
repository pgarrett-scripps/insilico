# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a systems paper describing a working tool that integrates fragmented knowledge graphs through natural language. The contribution is real—mcp-proto-okn solves a genuine access problem for the Proto-OKN ecosystem—and the implementation appears sound. The manuscript is honest about scope and limitations. Reproducibility is adequate for the core claims, though some procedural details are scattered and one use case lacks sufficient specificity to fully verify the reported result. The work merits publication with minor revision.

## Strengths

1. The authors provide a public GitHub repository with working code, documentation, and complete chat transcripts for both use cases, enabling readers to inspect the actual queries and outputs.

2. The ontology-expansion mechanism (Case Study 2) is well-motivated and the reported numbers (1 input URI → 1,592 descendants, 447 → 10,000+ datasets) are concrete and traceable to a specific query strategy.

3. The paper honestly acknowledges dependence on upstream endpoint availability and schema quality, and does not overstate the generality of the approach beyond the Proto-OKN setting.

## Weaknesses: Load-Bearing Claims

**Claim 1: mcp-proto-okn enables multi-step integrative analysis across heterogeneous graphs without SPARQL expertise.**

The evidence is Case Study 1 (spaceflight thymus analysis). The authors report that the assistant "queried the spoke-genelab KG to recover study metadata and assay design," then "mapped mouse genes to human orthologs and switched to the spoke-okn KG to retrieve disease associations," ultimately identifying 322 concordant genes and disease associations. The chat transcript is provided (linked in the paper), which is commendable. However, the manuscript does not specify:
- How the assistant performed the mouse-to-human ortholog mapping (is this a built-in tool, an external service call, or LLM-generated?).
- Whether the 322 concordant genes were identified by the assistant or by manual post-processing of the results.
- What "strong concordance" (Pearson r = 0.80) means operationally—correlation of what, across which samples or conditions?

The linked transcript would resolve this, but a reader should not need to leave the paper to verify the central workflow. The claim that the assistant performed this "entirely through natural language queries" is plausible but not fully specified in the text itself. **What would settle this:** Report in the manuscript (or in a supplementary methods section) the exact sequence of MCP tool calls the assistant made, the parameters passed to each, and which steps required LLM reasoning versus deterministic tool output.

**Claim 2: Ontology expansion automatically recovers 10,000+ datasets that a naive single-URI query would miss.**

Case Study 2 reports that a query on MONDO:0004995 (cardiovascular disorder) directly returned 447 datasets, but expansion to 1,592 descendants yielded 10,000+. This is a striking improvement and is the paper's clearest technical contribution. The mechanism is transparent: fetch descendants from UberGraph, rewrite the SPARQL FILTER clause, execute in batches. The linked transcript confirms the query structure. However, the manuscript does not state:
- How many of the 10,000+ datasets are *new* (i.e., not already in the 447)?
- Whether the 1,592 URIs were all successfully expanded, or whether some failed and were excluded.
- Whether the batch size (80 batches) was chosen empirically or by design, and whether any batches timed out or returned partial results.

The claim as stated is that expansion "retrieved from over 10,000 individual datasets," which is ambiguous: does it mean 10,000 unique datasets, or 10,000 dataset-disease pairs? **What would settle this:** Report the count of unique datasets in the 447-dataset set, the count in the expanded set, and the overlap; also report the success rate of the UberGraph expansion and any endpoint errors encountered.

## Weaknesses: Sweep

1. The paper does not specify the LLM model(s) used in the case studies (GPT-4, Claude 3.5, etc.), which affects reproducibility and generalizability of the results.

2. The FastMCP framework version and Python version are not stated; the GitHub README may specify these, but they should appear in the Methods section.

3. The paper claims the server "automatically expands ontology identifiers" but does not explain the decision logic for *when* to expand (e.g., does the assistant always expand, or only when a query returns few results?).

4. The multi_graph_query tool is described as supporting "coordinated execution across multiple graphs," but no example is given and it is unclear whether coordination means sequential execution, parallel execution, or join logic across results.

5. The paper does not report wall-clock time, endpoint latency, or failure rates for any of the queries, making it difficult to assess practical usability.

6. The "query-analysis metadata and warnings about common issues" mentioned for the query tool are never exemplified or listed.

7. The get_join_strategy tool is mentioned but not used in either case study, leaving its utility and correctness undemonstrated.

## Questions

- In Case Study 1, how were the "thousands of significant genes" identified—by what statistical threshold and multiple-testing correction?
- Does the server cache UberGraph descendants or fetch them fresh on each query, and what is the latency impact?
- The paper mentions "configurable expansion bounds" for ontology expansion; what are the defaults and how are they set?