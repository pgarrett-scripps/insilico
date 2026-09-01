# Desk Screen Report: mcp-proto-okn

## Summary
This manuscript describes mcp-proto-okn, a Python-based Model Context Protocol (MCP) server that enables natural-language access to biomedical and scientific knowledge graphs hosted on the OKN Fabric. The work is presented as a software tool paper with two illustrative case studies.

## Scope Assessment

**In Scope for In Silico:** Yes. The manuscript describes original research software with a clear methodological contribution (MCP-based federation of heterogeneous knowledge graphs) and provides concrete evidence of utility through documented case studies. It makes checkable claims about functionality and demonstrates them with reproducible workflows.

## Threshold Issues

### 1. Completeness and Verifiability
The manuscript references:
- Public GitHub repository (https://github.com/sbl-sdsc/mcp-proto-okn)
- Documented example transcripts with full chat logs
- Public OKN Fabric endpoints and registry
- Reproducible case studies with specific dataset identifiers (e.g., OSD-244)

All central evidence appears inspectable. ✓

### 2. Fundamental Soundness
The technical approach is sound:
- MCP as a standard interface for LLM-tool integration is well-established
- The routing, schema inspection, and ontology expansion strategies are reasonable
- The use of UberGraph for descendant expansion is appropriate and well-motivated
- Multi-graph coordination via SPARQL federation is standard practice

No fundamental design flaws are evident. ✓

### 3. Clarity and Presentation
The manuscript is clearly written, well-structured, and honest about limitations (endpoint availability, schema heterogeneity, identifier coverage). The workflow diagram and case studies effectively communicate the contribution. ✓

### 4. Novelty and Contribution
The work is **incremental but legitimate**:
- MCP-based access to knowledge graphs is not entirely novel (TogoMCP is cited as prior work)
- However, the application to the fragmented Proto-OKN ecosystem with 30+ heterogeneous graphs, automatic ontology expansion, and multi-graph coordination represents a meaningful extension
- The case studies demonstrate practical utility beyond what prior work (TogoMCP, Emonet et al.) addressed

The contribution is appropriately scoped and acknowledged. ✓

### 5. Evidence-Claims Alignment
- Claims about functionality are supported by working code and documented examples
- Claims about utility are supported by two detailed case studies with real data
- Limitations are stated (endpoint availability, schema variation)
- No overclaiming is evident

✓

## Minor Observations (Not Grounds for Desk Rejection)

1. **Evaluation scope:** The manuscript presents two case studies rather than systematic benchmarking. This is acceptable for a tool paper, but full review should assess whether the evidence is sufficient to support the utility claims.

2. **Comparison to related work:** The distinction from TogoMCP could be slightly more detailed (e.g., quantitative comparison of graph coverage, schema heterogeneity handled). This is a minor point for reviewers to consider.

3. **Reproducibility details:** The manuscript could specify Python version, FastMCP version, and dependency versions more explicitly, though the GitHub repository likely contains this.

## Venue Fit

This manuscript is well-suited to In Silico:
- It is original research software with a clear methodological contribution
- All central claims can be evaluated from the manuscript and public materials
- It is neither a clinical trial, diagnostic guidance, nor marketing material
- The work is sound enough to merit expert review, even if some claims require scrutiny

---

## DESK DECISION: proceed

**Rationale:** This is a legitimate software contribution with adequate evidence of functionality and utility. While the novelty is incremental (building on prior MCP-based approaches), the application to the heterogeneous Proto-OKN ecosystem and the specific technical solutions (ontology expansion, multi-graph coordination) represent a meaningful advance. The manuscript is complete, clearly presented, and all central claims are verifiable. Send to full review.