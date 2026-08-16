# Statistics & Data-Analysis Reviewer

SCORE: 2  
CONFIDENCE: 4  

## Summary

This is a proof-of-concept study with n=12 neurons, of which only 3 were recorded during retrieval. The central quantitative claims — that capacitance correlates with protein identifications, that spike integrity during retrieval predicts synaptic enrichment, and that retrieval loss decouples proteomics from electrophysiology — are each supported by at most 3 data points, with no statistical test that can bear the weight assigned to it. The framework is sensible and the indiscriminate-collection design is a genuine strength, but the paper's headline findings are not established by the evidence presented. The manuscript is honest about its limitations, which is to its credit, but the gap between the claims and the evidence is too wide for the current form.

## Strengths

1. The indiscriminate collection of all patch outcomes, including torn neurons as negative controls, is a thoughtful design choice that enables the qualitative clustering analysis.
2. The authors explicitly acknowledge the compartmental bias of soma retrieval and the risk of false negatives for membrane proteins.
3. The framework's distinction between quantitative yield (capacitance) and qualitative integrity (spike preservation) is conceptually useful.

## Weaknesses

### Load-bearing

**1. The capacitance–protein-identification correlation is computed on n=3 and reported with an adjusted R² of 0.998.** This is the paper's central quantitative claim, and it is unsupported as stated. With three points, a linear regression has one degree of freedom for error; the adjusted R² is essentially meaningless, and the F-statistic (F=1577) is driven entirely by the spread of the three points. The claim that "soma size plays a more direct role in protein recovery than RM" is a comparison of two correlations on the same three points — no test of the difference between the correlations is provided, and with n=3 no such test could be meaningful. The authors should either present this as a descriptive observation with the n=3 caveat prominently stated, or collect more gigaseal-preserved retrievals before claiming a correlation. The one thing that would settle this: report the raw data points (C, RM, protein IDs) for all three neurons in a table, and state explicitly that no inferential claim is being made from n=3.

**2. The claim that "preservation of neuronal spiking during relocation tended to be associated with broader synaptic enrichment" is based on a comparison of three neurons, one of which (neuron #6) was partially aspirated.** The SynGO enrichment analysis is performed on each neuron individually, and the comparison of "diversity of enriched terms" across neurons #4, #6, and #7 is a comparison of three single observations. There is no statistical test comparing the groups — the UpSet plot and heatmap are descriptive. The claim that "neuron #6 lacked significant enrichment for synaptic signaling" is presented as evidence that compromised retrieval reduces synaptic recovery, but with n=1 per condition, this is an anecdote, not a finding. The authors should either present this as a case study with explicit caveats, or collect enough neurons per retrieval category to support a comparison.

**3. The claim that "retrieval loss decouples proteomic measurements from electrophysiology" is supported by a null result in an unpowered sample.** The authors report that neither capacitance nor RM measured in situ correlated with protein identifications (p > 0.05, n = 6). This is presented as evidence that in situ recordings do not predict proteomic recovery. But a non-significant result in n=6 is not evidence of absence — it is consistent with a true correlation that the study is underpowered to detect. The authors should either present this as "we could not detect a correlation in this small sample" or perform an equivalence test. The claim that "robust in situ recordings cannot compensate for severe retrieval loss" is supported only by the two torn neurons (#11, #12), which is again n=2.

### Sweep

- The PCA in Figure 6A is descriptive and the clustering is interpreted post hoc; no variance explained is reported, and the claim that "neuron #6 grouped more closely with neurons lacking gigaseals" is a visual interpretation of a 2-D projection that is not quantified.
- The SynGO enrichment analysis is performed per cell, but the multiple-comparison correction is applied within each cell's gene list, not across the 12 cells; the family-wise error rate across the study is not controlled.
- The ion channel, GPCR, and transporter recovery lists are presented as binary heatmaps with no quantification of detection reliability; a protein detected in one cell with one peptide is treated identically to a protein detected with many peptides.
- The claim that "torn samples still showed impressive protein recovery" (1,400–2,300 proteins) is presented without a comparison to a negative control — no empty pipette or buffer-only sample is analyzed to establish the background protein identification rate.
- The correlation between capacitance and protein identifications uses log-transformed capacitance but the raw data are not shown; the choice of log transform is not justified and could be inflating the apparent linearity.
- The statement that "25–50% of the soma could be lost over the course of collection" is an estimate with no measurement basis — no imaging or quantitative comparison of the soma before and after retrieval is provided.
- The paper does not state whether the three gigaseal-preserved neurons were recorded from the same animal or different animals; if they are from one animal, the n is effectively 1 for biological replication.

## Questions

1. Were the three gigaseal-preserved neurons (#4, #6, #7) from the same animal or different animals? If the same, what is the justification for treating them as independent replicates?
2. Was a blank pipette or empty-well sample processed through the same workflow to establish the background protein identification rate?
3. For the capacitance–protein correlation, can the authors report the raw values (C, RM, protein IDs) for the three neurons, and state explicitly whether they are making an inferential claim from n=3?
4. What was the multiple-testing correction applied across the SynGO enrichment analyses for the 12 individual neurons — was the family of 12 analyses treated as a single experiment?