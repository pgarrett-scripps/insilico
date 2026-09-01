# Post-Debate Synthesis for the Editor

## Overview
Five specialist reports converge on a score of 4/5 (contribution_context, data_analysis, reporting_reproducibility, scientific_validity) with one N/A (ethics, no issues found). The debate identified two substantive issues, both judged "fixable" by both sides, plus one process concern raised late and not fully engaged.

## Issue 1: The two case studies cannot support the abstract's general "enablement" claim

**Manuscript evidence cited:** Abstract states mcp-proto-okn "enables AI assistants to discover, inspect, query and integrate scientific knowledge graphs through natural language" and "lowers the barrier for integrative discovery." The only supporting evidence is two "illustrative" case studies (spaceflight thymus analysis; cardiovascular ontology expansion), with chat transcripts linked externally on GitHub rather than included in the manuscript.

**Convergence note:** This point was raised independently, in different framings, by contribution_context ("no user study, benchmark, or comparative evaluation"), data_analysis ("whether the tool was tested on questions outside the two case studies... is unclear"), and scientific_validity ("whether the transcripts shown are representative or cherry-picked"). The skeptic correctly identifies this as one underlying blind spot surfaced three times by reviewers sharing a common model, not three independent corroborations — but also argues the underlying concern is real regardless of how many times it was voiced.

**Strongest case for treating it as serious (skeptic):** A systems paper whose only evidence for a capability claim is two self-selected success stories cannot establish a success/failure rate or rule out cherry-picking. Readers cannot currently tell whether either case study succeeded on the first attempt or after discarded failures.

**Strongest case for treating it as non-fatal (advocate):** No reviewer scored the paper below 4, and no reviewer identified evidence contradicting the demonstrated capability — the gap is "unknown failure rate," not "known failure." Data_analysis's own framing ("illustrative rather than empirical") is offered as a scope description, not a falsification. Panel-wide convergence at 4/5 across independently-angled reports is itself evidence the flaw is a quantification gap, not a validity failure.

**Concessions:** Advocate conceded the abstract's "enablement" language should be read as demonstrating feasibility rather than validated reliability at scale, and that this is a real gap. Skeptic conceded panel convergence at 4/5 is meaningful and that novelty need not be algorithmic for a tool paper to merit publication.

**Status: Unresolved but bounded.** Both sides agree the issue is real and both agree it is fixable via (a) reporting success/failure rates on a held-out set of natural-language questions, or (b) explicitly reframing the abstract's claims as proof-of-concept rather than validated capability. No side argued this is fatal to the paper as it stands; the disagreement is about how much this should weigh against an otherwise-convergent 4/5 assessment, and that disagreement was not resolved.

## Issue 2: The ontology-expansion recall claim is confounded and precision is unmeasured

**Manuscript evidence cited:** Case Study 2 reports expanding one MONDO URI (cardiovascular disorder, MONDO:0004995) into 1,592 descendant URIs, increasing retrieved datasets from 447 (root only) to 10,000+ (expanded), presented as evidence the mechanism "bridges user-level concepts and curator-level annotations while preserving recall."

**Convergence note:** Raised independently by data_analysis (the comparison "does not isolate the value of expansion from the structure of the annotation scheme itself," since descendant-tagged records are trivially excluded from a root-only query by ontology construction) and scientific_validity (no precision cost reported — e.g., whether datasets on rare cardiovascular syndromes like Brugada or Holt-Oram syndrome match a user's actual intent when asking about "cardiovascular disease"). This is the same underlying observation from two reports, not independent confirmation.

**Skeptic's case:** The 447-vs-10,000+ comparison is confounded by construction and overstates what was shown; the "preserving recall" language should be narrowed, and a precision/relevance sample is needed to support the framing as currently written.

**Advocate's case:** The mechanism itself is transparently described (batch count, UberGraph as descendant source) and scientific_validity itself calls the comparison "clear" and "direct." The precision question is a legitimate scope-narrowing request, not evidence the reported numbers are wrong or fabricated — the paper claims exactly what the mechanism does (expand and retrieve more), no more.

**Concession:** Advocate agreed the precision cost is unaddressed and that reporting a false-positive/relevance rate would strengthen the claim.

**Status: Resolved as a revision item.** Both sides agree the fix is narrowing the claim language (e.g., to "increases recall" rather than implying recall is "preserved" in a validated sense) and/or adding a precision/relevance sample. Neither side treated this as fatal.

## Issue raised late, not fully engaged: transcripts not in the manuscript record

Skeptic (round 2) noted that reporting_reproducibility observed the chat transcripts, though linked, are not included in the manuscript itself — meaning the paper's central evidentiary artifact is not inspectable within the record In Silico would be publishing alongside its review. The advocate's final turn did not address this point. It stands as an unrebutted but also unelaborated concern; its weight (formatting/process issue vs. a genuine reproducibility gap) was not adjudicated in the debate.

## Concerns from reports not engaged in the debate

- **Statistical reporting gaps in Case 1** (data_analysis): the Pearson r = 0.80 correlation is reported without p-value, CI, or clarification of whether genes are independent units (pseudo-replication concern); source and computation of the statistic are unspecified.
- **Missing procedural/methods detail** (reporting_reproducibility): LLM model(s) used, FastMCP/Python versions, decision logic for when ontology expansion triggers, and whether SPARQL queries are validated before execution — none of these were raised or contested in the debate.
- **Unclear division of labor between LLM and server tools** (contribution_context, scientific_validity): whether ortholog mapping, result merging, and cross-graph reasoning are native LLM behavior or explicit server-provided tools is unspecified in the text; not discussed in the debate.
- **No latency/failure-mode reporting** (multiple reports): endpoint downtime, query execution time, and batch-processing reliability (the "80 batches" in Case 2) are unaddressed in the manuscript and were not taken up by either debater.

These items were consistently noted across reports but never contested or defended in the debate; their absence from the transcript should not be read as resolution.