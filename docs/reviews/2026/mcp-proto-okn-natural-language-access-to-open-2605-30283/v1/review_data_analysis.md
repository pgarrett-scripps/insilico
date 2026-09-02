# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 3

## Overall Assessment

This is a software tool paper describing mcp-proto-okn, an MCP server enabling natural-language access to Proto-OKN knowledge graphs. The work is sound in scope and execution, with clear utility for its intended audience. However, the manuscript contains no quantitative claims requiring statistical validation, no hypothesis tests, no power analyses, and no comparative performance metrics. The two case studies are illustrative rather than empirical — they demonstrate capability but do not measure it against baselines or quantify accuracy, latency, or failure modes. For a software tool paper this is acceptable, but it limits what can be evaluated from a data-analysis perspective.

## Strengths

1. The ontology-expansion case study (Case 2) provides concrete numbers (1,592 descendant URIs, 10,000+ datasets retrieved vs. 447 with naive approach) that transparently show the mechanism's effect, with no hidden filtering or post-hoc selection.

2. The spaceflight case study reports a specific correlation coefficient (Pearson r = 0.80) with defined subsets (322 genes at both timepoints), making the claim verifiable even though no statistical test is reported.

3. The manuscript honestly flags limitations (endpoint availability, schema quality variation, identifier coverage) rather than overselling the tool's scope.

## Weaknesses: Load-Bearing Claims

**Claim: Ontology expansion retrieves substantially more relevant records than naive single-URI queries.**

The evidence is a single comparison: 447 datasets with the root MONDO:0004995 URI vs. >10,000 with 1,592 descendant URIs. This is presented as a case study, not a controlled experiment, so the authors are not claiming statistical significance. However, the generating process itself creates ambiguity about what the numbers measure. The "447 datasets" count is the number of records *directly annotated* with the root term; the ">10,000" is the count across all descendants. These are not independent samples from the same annotation process — they are different subsets of the same underlying dataset, and the expansion is deterministic (every record tagged with a descendant is also tagged with an ancestor in an ontology). The comparison therefore does not isolate the value of expansion from the structure of the annotation scheme itself. A more informative comparison would report: (1) how many of the >10,000 records are *not* directly tagged with the root term (i.e., how many would be missed by naive query), and (2) whether the expanded set includes false positives (records tagged with descendants that are not actually relevant to the user's intent). The manuscript does not provide either. The claim that expansion "bridges user-level concepts and curator-level annotations while preserving recall" is supported only by the observation that more records are retrieved, not by evidence that those records are relevant or that recall is actually preserved.

**Claim: The assistant successfully performs multi-step cross-graph reasoning (Case 1: spaceflight gene expression).**

The case study reports that the assistant "mapped mouse genes to human orthologs," "switched to the spoke-okn KG," and "identified associations with cardiovascular, metabolic, inflammatory, autoimmune, neurological, coagulation, and liver diseases." No accuracy metric is provided for any of these steps. The ortholog mapping is not validated against a reference set; the disease associations are not checked against literature or curated databases; and the "strong concordance" (r = 0.80) between spaceflight conditions is reported without stating what test produced it or what the null expectation is. The concordance could reflect genuine biological signal or could reflect shared technical artifacts (batch effects, library-size normalization, or other preprocessing applied identically to both conditions). The case study demonstrates that the tool can be used end-to-end, but does not establish that the intermediate steps are accurate or that the final interpretation is correct. To support the claim, the authors would need to validate the ortholog calls against a reference (e.g., Ensembl or NCBI Homologene), report precision and recall for disease associations against a gold-standard set, and explain the source of the concordance statistic and its interpretation.

## Weaknesses: Sweep

1. The Pearson correlation coefficient (r = 0.80) in Case 1 is reported without a p-value, confidence interval, sample size (n = 322 genes), or statement of whether the test is one- or two-sided; the denominator (322) is the number of genes, not the number of independent replicates, which raises a pseudo-replication concern if genes are not independent units.

2. The claim that the NDE query returned ">10,000 individual datasets" is imprecise — does this mean unique dataset records, or does it count the same dataset multiple times if it is tagged with multiple descendant URIs?

3. No information is provided on query execution time, endpoint latency, or failure rates, which are relevant to the tool's practical utility.

4. The manuscript does not report whether the SPARQL queries generated by the assistant were validated by a human or checked against the schema before execution.

5. The "80 batches" mentioned for the NDE query are not explained — what is the batch size, why was batching necessary, and were results merged correctly?

6. No comparison is provided to alternative approaches (e.g., keyword search, manual SPARQL writing, or other LLM-based tools), so the relative contribution is unclear.

7. The chat transcripts are referenced as evidence but are not included in the manuscript itself, making them difficult to verify.

8. The paper does not report whether the tool was tested on questions outside the two case studies, or what fraction of arbitrary user queries succeed.

## Questions

1. For the spaceflight case study, what is the source of the Pearson correlation coefficient (r = 0.80), and is it a correlation between the log-fold-change values of the 322 genes across the two timepoints, or something else?

2. In Case 2, how many of the >10,000 datasets retrieved by the expanded query were *not* retrieved by the naive single-URI query, and is that number the key metric for the claim?

3. Were the SPARQL queries generated by the assistant manually inspected for correctness, and if so, what fraction were correct on first attempt?

4. The paper states that the assistant "generated assay-design diagrams, concordance plots, disease-association summaries" — are these outputs of the MCP server itself, or are they generated by the LLM client after receiving results from the server?