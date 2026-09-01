# Contribution & Prior-Work Reviewer

Based on my comprehensive prior-work search, I can now write the contribution and prior-work review. Let me compile my findings:

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript describes mcp-proto-okn, a Python MCP server that wraps the Proto-OKN ecosystem of 30+ knowledge graphs and enables natural-language querying through LLM assistants. The core contribution is engineering integration of existing tools (FastMCP, SPARQL endpoints, UberGraph) into a unified interface for a specific ecosystem, with two illustrative case studies. The work is sound and addresses a real access barrier, but the novelty is primarily in application and integration rather than methodological innovation. The closest prior work—TogoMCP (Kinjo et al. 2026, cited)—implements nearly identical functionality (schema-guided LLM querying, MCP-based SPARQL generation, ontology expansion) for a different ecosystem (DBCLS RDF Portal). The manuscript acknowledges this parallel work but does not clearly articulate what is genuinely novel beyond scope and domain.

## Strengths

1. The manuscript clearly identifies and addresses a real fragmentation problem in the Proto-OKN ecosystem, where 30+ graphs with heterogeneous schemas and no common conventions require domain-specific expertise to query.

2. The case studies are concrete and well-executed: the spaceflight thymus analysis demonstrates multi-step cross-graph reasoning, and the cardiovascular disease ontology expansion case quantitatively shows the value of hierarchical term expansion (1 URI → 1,592 descendants, 447 → 10,000+ datasets).

3. The work is reproducible and openly available (GitHub repository, example transcripts, client configuration), and the authors provide sufficient implementation detail for readers to understand the architecture and deploy it.

## Weaknesses: Load-Bearing Claims

**Claim 1: mcp-proto-okn enables novel multi-graph querying and ontology-aware federation for Proto-OKN that prior work does not address.**

The manuscript positions itself as addressing the Proto-OKN setting specifically because "over 30 graphs span biomedical, environmental, and other domains, share few entities, and follow no common schema convention — requiring routing between graphs, hierarchical reasoning over reference ontologies, and provenance tracking across multi-graph queries." However, the actual technical contributions—schema inspection, SPARQL generation, ontology expansion via UberGraph, multi-graph coordination—are not novel. TogoMCP (Kinjo et al. 2026, cited in the reference list) implements schema-guided LLM-based SPARQL generation, entity resolution through external APIs, and orchestrated tool calls over a federated RDF ecosystem (DBCLS RDF Portal, 70+ databases). The manuscript acknowledges TogoMCP but claims it "targets curated ecosystems" whereas Proto-OKN "requires routing between graphs, hierarchical reasoning over reference ontologies, and provenance tracking." This distinction is not substantiated: TogoMCP also handles schema heterogeneity and multi-endpoint coordination; the difference is scope (DBCLS vs. Proto-OKN), not capability. The ontology expansion mechanism (fetching descendants from UberGraph, injecting into SPARQL) is standard practice in biomedical KG querying and is not presented as novel. What remains is application to a specific ecosystem and implementation in FastMCP, which is engineering contribution, not methodological innovation.

**Claim 2: The case studies demonstrate capabilities that require the specific design of mcp-proto-okn and could not be achieved with prior systems.**

The spaceflight case study (Case 1) involves querying spoke-genelab for differential expression, then spoke-okn for disease associations, then mapping mouse to human genes. This is a multi-step LLM-orchestrated workflow, but the steps themselves (SPARQL query, result interpretation, cross-species mapping, second SPARQL query) are standard LLM agent patterns. The case study does not isolate what mcp-proto-okn specifically enables that TogoMCP or a generic LLM+SPARQL system could not. The cardiovascular disease case (Case 2) demonstrates ontology expansion: mapping "cardiovascular disease" to MONDO:0004995, fetching 1,592 descendants from UberGraph, and querying NDE with the expanded URI set. This is valuable and well-executed, but ontology expansion for biomedical KG queries is established practice (the Gene Ontology and MONDO papers cited in my search predate this work). The case study shows the value of the feature for the NDE use case, not that the feature itself is novel. Neither case study reports a comparison with a baseline (e.g., naive single-URI query, or a non-ontology-aware LLM approach) that would isolate the contribution of mcp-proto-okn's design choices.

## Weaknesses: Sweep

1. The manuscript claims mcp-proto-okn "supports graph routing, ontology expansion with UberGraph, coordinated multi-graph querying, and creating chat transcripts" but does not report quantitative evaluation of routing accuracy, query success rates, or latency across the 30+ graphs, making it unclear whether the system is robust in practice.

2. The reference to Emonet et al. 2025 (arXiv:2410.06062) describes a RAG framework with "curated question–query pairs" and "validation step to improve accuracy," but the manuscript does not explain why mcp-proto-okn does not employ similar validation or how it avoids hallucinated SPARQL.

3. The manuscript states that "the AI assistant handles identifier conversion, result merging, and cross-graph reasoning," but does not specify whether this is LLM-native reasoning or whether mcp-proto-okn provides explicit tools for these tasks, leaving the division of labor unclear.

4. The case studies are presented as "illustrative" but are the only evidence of system utility; no user study, benchmark, or comparative evaluation against TogoMCP or other baselines is provided.

5. The manuscript acknowledges "dependence on the availability and schema quality of upstream OKN Fabric endpoints" but does not report failure modes, endpoint downtime, or schema inconsistencies encountered during development or case study execution.

6. The claim that mcp-proto-okn "lowers the barrier for integrative discovery across biomedicine and beyond" is not empirically validated; no evidence is presented that end users can successfully use the system without SPARQL expertise.

## Questions

1. How does the routing mechanism (route_query tool) decide which graphs are relevant to a natural-language question, and has this been evaluated against a held-out set of questions with ground-truth graph assignments?

2. The cardiovascular disease case study expanded MONDO:0004995 to 1,592 descendants; what is the computational cost and latency of this expansion, and are there configurable bounds to prevent runaway expansion?

3. TogoMCP is cited as prior work but the manuscript does not report a direct comparison (e.g., same question posed to both systems, success/failure rates, query quality); what prevents such a comparison, and how would readers distinguish the two systems' capabilities?

4. The case studies reference "chat transcripts" in the GitHub repository; are these verbatim LLM outputs, or have they been curated or edited, and if edited, what changes were made?

---