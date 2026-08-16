# Clarity & Presentation Reviewer

SCORE: 4  
CONFIDENCE: 4

## Summary

This is a clearly written, well-structured methods paper that introduces a framework for interpreting patch-clamp single-cell proteomics (patch-SCP) outcomes in acute brain slices. The central contribution — that retrieval quality, not just in situ electrophysiology, determines proteomic yield and biological content — is stated explicitly in the abstract and introduction, and the manuscript is unusually candid about its own limitations. The narrative flows logically from motivation to methods to results to interpretation, and the figures are generally well-referenced and legible. The main presentation issues are concentrated in the figures (missing panel references, unlabeled axes) and a few places where the quantitative claims are stated only directionally. These are fixable with minor revision.

## Strengths

1. The central claim is explicitly stated and the framework is clearly motivated — the reader never has to guess what question is being asked.
2. The manuscript is candid about its limitations (small sample size, incomplete recovery of membrane proteins, spatial fidelity of recordings), which strengthens rather than weakens the contribution.
3. The figures are generally well-designed and the narrative panel order is logical; the use of ladder plots and UpSet plots is effective.

## Weaknesses

**Load-bearing:**

1. **The claim that "gigaseal preservation links neuron size to proteome recovery" (Figure 3D) is not supported by the evidence presented.** The correlation between log-transformed capacitance and protein identifications is based on n=3 neurons, and the reported F-statistic (F=1577, p<0.05, adjusted R²=0.998) is implausibly high for a biological dataset of this size — an adjusted R² of 0.998 with three points is essentially a perfect linear fit, which is more consistent with overfitting or a coincidental alignment than a meaningful relationship. The manuscript does not report the raw data points or confidence intervals, so a reader cannot assess whether this correlation is robust or an artifact of the small sample. What would settle this: report the individual data points, the 95% confidence intervals for the slope, and ideally a permutation-based p-value or a bootstrap estimate of the correlation, given the tiny n. The claim as stated outruns the evidence.

2. **The claim that "preservation of active properties during retrieval is associated with recovery of synaptic proteins" (Figure 4) is not established by the evidence.** The manuscript shows that neuron #4 (stable spiking) had the greatest diversity of enriched SynGO terms, neuron #7 (reduced spike amplitude) had fewer unique terms, and neuron #6 (single spike) lacked enrichment for synaptic signaling. But this is a comparison of three individual neurons, not a statistical association. The manuscript does not report any quantitative measure of "spike integrity" (e.g., spike amplitude, number of spikes, or a composite score) that could be correlated with synaptic enrichment across the three neurons. The claim is presented as a finding but is really an anecdotal observation from n=3. What would settle this is a quantitative metric of spike integrity (e.g., mean spike amplitude or number of spikes during depolarization) reported for each neuron, alongside the number of enriched SynGO terms, so the reader can see whether the relationship holds beyond the three examples shown.

3. **The claim that "retrieval loss decouples proteomic measurements from electrophysiology recordings" (Figure 5) is supported by the data, but the presentation of the negative control is unclear.** The manuscript states that torn neurons (#11 and #12) "produced the fewest detected proteins of all categories," but the figure (Figure 5A) does not show the actual protein counts for each neuron — it shows a bar chart with categories but no individual values or error bars. The reader cannot determine from the figure whether the difference between torn neurons and other categories is large or small, or whether the "fewest" claim is based on a meaningful difference. What would settle this is a table or figure with the actual protein identification counts for each of the 12 neurons, with the category labels clearly marked.

**Sweep:**

4. **Figure 3D and 3E: the axes are not labeled with units** — the x-axis is labeled "log-transformed C" and "log-transformed RM" without specifying the units (pF and MΩ, presumably), and the y-axis is labeled "Protein identifications" without specifying whether this is the total number of protein groups or something else. A reader cannot determine the scale of the effect from the figure alone.

5. **The abstract claims "we detected thousands of proteins from single neuronal soma" but does not state the range or median** — the reader cannot tell whether "thousands" means 1,500 or 5,000, which matters for assessing the sensitivity of the workflow. The manuscript later reports "at least 1700 total proteins" for the gigaseal-preserved neurons, but this is not in the abstract.

6. **The term "shotgun patch-SCP" is introduced in the abstract and used throughout, but is never defined** — the reader must infer that it means "indiscriminate collection of all patch attempts," which is not stated until the Results section. This is a SOFT issue but it affects the abstract's standalone intelligibility.

7. **The Discussion repeats the Results** — the paragraph beginning "We found that measurements of somal capacitance made during retrieval were associated with protein identifications" restates the finding from Figure 3D without adding new interpretation. This could be condensed.

8. **The manuscript uses "gigaseal-preserved" and "gigaseal preserved" interchangeably** — this is a minor terminology inconsistency that could confuse a reader scanning the figures.

## Questions

1. For Figure 3D, what are the actual capacitance values (in pF) and protein counts for each of the three neurons? The regression is reported but the raw data points are not shown.

2. For Figure 5, what are the exact protein identification counts for neurons #11 and #12 (torn) versus the other categories? The figure shows categories but not individual values.

3. In the abstract, "thousands of proteins" — what is the actual range across all neurons? The manuscript reports "at least 1700" for the gigaseal-preserved neurons, but the range across all 12 is not stated.

4. Is the "shotgun" term defined anywhere in the methods or a glossary? If not, it should be defined at first use.