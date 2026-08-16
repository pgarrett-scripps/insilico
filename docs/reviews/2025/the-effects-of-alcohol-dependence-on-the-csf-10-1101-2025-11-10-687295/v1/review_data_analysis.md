# Statistics & Data-Analysis Reviewer

## Summary
The paper's central claim — that alcohol dependence produces a qualitatively distinct CSF proteome with BBB breakdown and neuroinflammation — rests on a qualitative presence/absence analysis of 9 mice (4 Dep, 5 Non-dep), with no quantitative comparison, no multiple-testing correction, and a post-hoc power analysis that the authors themselves concede gives only 38% power for the moderate effect sizes that dominate their lists. The headline numbers (140 vs 67 group-specific proteins) are counts of proteins detected in ≥2 of 4 vs ≤1 of 5 animals, a threshold with no stated error rate, and the entire differential analysis is unadjusted for the ~600 proteins tested. The manuscript is candid about its limits, but the conclusions outrun the evidence as presented.

## Strengths
- The authors explicitly disclose the small sample size and report a post-hoc power analysis (38% power for moderate effects), correctly framing their protein lists as minimum estimates.
- The manuscript is unusually candid about the contamination question (keratins, hemoglobin) and addresses it with a comparator study rather than ignoring it.
- The DIA-MS pipeline and 1% FDR filtering at the peptide level are clearly described and reproducible.

## Weaknesses
- LOAD-BEARING: The differential claim (140 Dep-specific vs 67 Non-dep-specific proteins) is a qualitative detection analysis with no statistical test and no multiple-testing correction across ~600 proteins. The threshold (≥2/4 vs ≤1/5) has no stated error rate, and the authors' own power analysis shows only 38% power for the moderate effects that dominate their lists — so the 'distinct proteome' conclusion is not supported by any inferential statistic, only by descriptive counts.
- LOAD-BEARING: The 'protective mechanisms lost in dependence' claim (CALB1, SUMO2/3, TAGL3, immunoglobulin variable regions) is inferred from proteins detected in Non-dep but not Dep mice. But with n=4-5 and a detection threshold, absence of detection is not evidence of absence — a protein below the detection limit in one group is treated as 'lost,' and the paper's own power analysis concedes this is exactly the regime where false negatives dominate. The claim that these mechanisms are 'lost' rather than merely undetected is unsupported.
- LOAD-BEARING: The BBB-disruption claim rests on MMP2, BIP, VE-cadherin, VCAM1, ACTA, LAMB2, fibulins — but these are presence/absence calls in 9 animals with no quantitative abundance comparison. The paper never reports whether these proteins are more abundant in Dep CSF, only that they were detected there; a protein detected at trace levels in 2/4 Dep mice (VCAM1, CX3CL1, CADH5) is treated as equivalent evidence to one detected in 4/4. The detection-rate threshold conflates effect size with detection probability.
- The PCA plot (Figure 1c) is described as showing Dep clustering, but with n=4-5 and no stated variance decomposition, the separation is not quantified; one Non-dep animal clusters within the Dep group and is not discussed as a potential outlier or excluded.
- The IGG2B/IL-6R antibody detection is reported as a single peptide (DILLISQNAK) identified in all samples, but no quantitative comparison is made between groups, and the claim that it 'crosses the BBB' is not supported by any abundance data — only by presence in CSF.
- Sweep: no exact p-values, effect sizes, or confidence intervals are reported anywhere; every quantitative claim is a detection count.
- Sweep: the 'sex segregation along PC2' observation in Non-dep mice is made from n=2-3 per sex and is not statistically testable at this n.
- Sweep: the enrichment analyses (EnrichR, STRING, KEGG) are run on the group-specific protein lists, but the lists themselves are unadjusted for multiple testing, so the pathway enrichments inherit the same unquantified error rate.

## Questions
- What is the false-discovery rate of the ≥2/4 vs ≤1/5 detection threshold across ~600 proteins? Please report the expected number of proteins that would pass this threshold by chance alone.
- For the BBB-disruption proteins (MMP2, BIP, VE-cadherin, VCAM1), can you report quantitative abundance (e.g., MaxLFQ intensities) with a stated test and n, rather than presence/absence only?
- For the 'protective mechanisms lost' claim (CALB1, SUMO2/3, TAGL3), what evidence distinguishes true loss from detection-limit effects given the 38% power for moderate effects?
- How was the one Non-dep animal that clusters within the Dep group in Figure 1c handled — was it excluded, and if so, was the exclusion pre-specified?