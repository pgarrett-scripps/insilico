# Statistics & Data-Analysis Reviewer

-ORE: 2
CONFIDENCE: 4

**Overall**

This is a method-development paper whose central quantitative claims are either unsupported by the statistics presented or are not tested at all. The core finding—that capacitance measured during retrieval correlates with protein identifications—rests on a regression of three points with no reported uncertainty or validation. More fundamentally, the paper's own framework is undermined by the absence of any statistical test for the qualitative claims about synaptic enrichment, and the sample size is too small to support the strong conclusions drawn. The paper would benefit from either a much larger dataset or a substantial scaling back of its claims to match the evidence. The authors have identified an important problem, but the current analysis does not yet establish the framework they propose.

**Strengths**

1.  The authors are transparent about the exploratory nature of the work and the small sample size, which is commendable.
2.  The idea of using electrophysiological measurements during retrieval as a quality metric is a valuable conceptual contribution to the field.
3.  The inclusion of all retrieval outcomes, rather than only the "best" ones, is a rigorous approach that strengthens the interpretability of the data.

**Weaknesses**

**Load-Bearing**

1.  **The central claim—that capacitance correlates with protein identifications—is based on a linear regression of n=3 data points.** The reported p-value (p<0.05) is not meaningful with such a small sample size, and the adjusted R² of 0.998 is a statistical artifact of overfitting. The claim that this "links soma size to proteome yield" is a HARD overstatement. The authors must report the raw data for all three points and provide a clear justification for how a correlation from n=3 can be considered evidence for a biological relationship, or temper the claim to a hypothesis-generating observation. The same applies to the non-significant finding for RM, which is used to claim a "more direct role" for capacitance, a claim not supported by a non-significant p-value in a tiny sample.

2.  **The central qualitative claim—that "preservation of active properties during retrieval is associated with recovery of synaptic proteins"—is not supported by any statistical test.** The paper states that neuron #6 "lacked significant enrichment for synaptic signaling," but no statistical comparison is made between the neurons. The claim appears to rest on a visual inspection of a heatmap (Figure 4C) and a list of enriched GO terms. To make this claim, the authors need to perform a formal statistical test for differential enrichment between the neurons (e.g., a Fisher's exact test or a GSEA-style comparison) and report the resulting p-values. As it stands, the conclusion is an interpretation of the data, not a finding.

**Sweep**

3.  The "shotgun" strategy of including all samples is sound, but the paper does not report a power analysis or any justification for the final sample size, making it impossible to know if the study was adequately powered to detect the effects of interest.
4.  The PCA in Figure 6A is used to support the claim that "comprehensive analysis can distinguish between high- and low-context retrievals," but this is a post-hoc interpretation of a clustering result with no quantitative support; a PERMANOVA or similar test would be needed to support this claim.
5.  The paper does not report any correction for multiple testing when discussing the "consistently enriched" GO terms across neurons, which could lead to an overestimation of the consistency of the findings.
6.  The claim that "torn samples still showed impressive protein recovery" is based on a comparison to what, exactly? A formal statistical comparison of the number of proteins identified in "torn" vs. "gigaseal-preserved" neurons is missing, and the high variance within the "no gigaseal" group (1,400-2,300 proteins) suggests the analysis is underpowered to detect a difference even if one exists.
7.  The paper does not report the number of biological replicates (animals) used, only the number of neurons, so it is impossible to assess the impact of inter-animal variability on the results.
8.  The paper claims that "the recovery of ion channel subunits could vary widely," but this is presented without any statistical measure of variance or a formal test for differences between the groups, making it impossible to know if this variability is meaningful or just noise.

**Questions**

1.  What is the exact p-value and 95% confidence interval for the slope of the regression line in Figure 3D, and what is the biological justification for treating this relationship as linear?
2.  Can you provide the results of a formal statistical test (e.g., a permutation test or a Mann-Whitney U test) comparing the enrichment of SynGO terms between neuron #4 and neuron #6, rather than relying on a qualitative comparison of a heatmap?