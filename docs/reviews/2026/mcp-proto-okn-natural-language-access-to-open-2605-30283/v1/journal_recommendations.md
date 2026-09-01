# Venue Recommendations

## as_is
**In Silico** (intended target)

The manuscript is already suitable for In Silico in its current form. The editor's verdict is "minor revision," which is a clear acceptance signal at this venue. The paper presents a working tool with public code and transcripts, makes modest claims about feasibility (not reliability), and is transparent about limitations. In Silico's scope explicitly includes methodological and applications work, and its review-as-publication model means the required revisions will be visible to readers alongside the work itself. The two case studies provide sufficient evidence for the venue's standard: checkable claims supported by deposited materials, not a claim to universal reliability. Submission as-is would likely receive acceptance pending the listed revisions, which are editorial rather than scientific.

---

## after_revision

**Bioinformatics** (Oxford University Press)

Once the revisions are complete—particularly the version pinning, persistent archiving of transcripts, and clarified division of labour between server and LLM—this becomes a strong fit for Bioinformatics. The journal publishes tools and databases for computational biology, and mcp-proto-okn is a genuine infrastructure contribution that lowers access barriers to a funded national resource (Proto-OKN). The two case studies, once their provenance is fully documented, will serve as adequate validation for an applications note. The candid limitations section and public code repository align with the journal's standards for reproducibility.

**Journal of Biomedical Semantics**

After revision, this is a natural home for the work. The journal explicitly covers knowledge graphs, ontologies, semantic web tools, and integration of biomedical data sources. The ontology-expansion mechanism (UberGraph integration, MONDO/UBERON/HP/GO/ChEBI handling) and the multi-graph routing problem are directly in scope. Once the ontology-expansion claim is narrowed and the statistics are documented (revision 2), the contribution becomes a clean fit: a tool for bridging user-level queries to curator-level ontology annotations in a fragmented graph ecosystem.

**Database** (Oxford University Press)

After revision, this is also a strong candidate. Database publishes papers on biological databases, data integration tools, and query interfaces. The paper's focus on making 30+ heterogeneous graphs queryable through natural language, with schema inspection and routing tools, is exactly the kind of infrastructure contribution Database values. The case studies provide sufficient evidence of utility; the required revisions mainly strengthen traceability and honesty about scope.

---

## alternative

**bioRxiv** (preprint server)

If the target venues prove competitive or if the authors prefer to publish the work as a preprint first, bioRxiv is the natural home. The manuscript is already well-suited to preprint circulation: it describes a released tool with public code, and the two case studies are sufficient to establish proof of concept. Posting to bioRxiv before journal submission also allows the community to test the tool and provide feedback, which could inform a stronger follow-up paper with quantitative evaluation.

**Workshop or Special Issue on Knowledge Graphs and LLMs**

If the paper's scope is narrowed to focus on the MCP-as-interface contribution rather than the full Proto-OKN ecosystem, it could fit a workshop on LLMs for knowledge graph querying (e.g., at ISWC, ESWC, or a bioinformatics conference). This would be a lower-pressure venue for establishing the tool's utility before attempting a full journal submission with quantitative benchmarking.

**F1000Research** (open peer review)

As a fallback, F1000Research accepts tools and applications papers with rapid, transparent peer review. The open-review model and lower barrier to acceptance make it suitable if the paper faces rejection at higher-tier venues, though the journal's impact is lower. The public code and transcripts would be a strong asset here.

---

## Notes on fit and confidence

- **Confidence in as_is (In Silico):** Very high. The editor has already signalled acceptance pending minor revisions. The venue's scope and review model are explicitly designed for this type of work.

- **Confidence in after_revision (Bioinformatics, Journal of Biomedical Semantics, Database):** High, conditional on completing the revisions listed in the decision letter. All three journals publish tools and applications; the revisions mainly ensure claims are scoped correctly and provenance is documented. None of these venues requires new experiments or quantitative benchmarking as a condition of acceptance.

- **Confidence in alternative (bioRxiv, workshops, F1000Research):** These are fallbacks if the paper faces unexpected rejection at the headline venues, or if the authors choose to preprint first. bioRxiv is a natural intermediate step and carries no risk; workshops are lower-stakes venues for establishing community interest.

- **What would substantially improve prospects at any venue:** A quantitative evaluation (30–50 queries with reported routing accuracy, first-attempt SPARQL validity, and failure taxonomy) would convert the paper from "demonstrated feasibility" to "measured performance" and would be the natural core of a follow-up paper. The editor explicitly encourages this but does not require it for acceptance at In Silico or the journals listed above.