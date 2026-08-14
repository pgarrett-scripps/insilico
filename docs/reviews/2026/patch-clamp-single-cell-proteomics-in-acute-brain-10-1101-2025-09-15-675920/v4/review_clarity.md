# Clarity & Presentation Reviewer

## Summary
This is a clearly written, well-structured methods paper whose central claims are appropriately scaled to a small exploratory dataset. The framework for categorizing retrieval outcomes is articulated cleanly and the narrative flows from motivation to results to interpretation without orphaned findings. The main clarity concerns are that several load-bearing inferences are stated with causal or generalizing force that the n=3 and n=1-per-condition data cannot support, and a few quantitative claims lack the specific values a reader needs. These are fixable with tightening rather than structural problems.

## Strengths
- The framework for categorizing retrieval outcomes (gigaseal preserved, lost, or never formed) is clearly articulated and provides a useful interpretive scaffold for the field.
- The authors are candid about limitations, including the small sample size and the inability to distinguish technical from biological variability.
- The indiscriminate collection strategy, including torn neurons as negative controls, is a thoughtful design choice that strengthens the interpretive framework.

## Weaknesses
- The claim that capacitance correlates with protein identifications (Figure 3D) is stated as a general finding ('soma size... plays a more direct role in protein recovery') but rests on n=3 neurons; the reported F=1577, adjusted R²=0.998 is a regression on three points, and the text does not state that this cannot distinguish a real relationship from noise. The authors should report the raw data points and explicitly scale the claim to n=3.
- The inference that spike integrity during retrieval is 'associated with the recovery of synaptic proteins' (Figure 4) is presented as a general association but rests on one neuron per condition (neuron #4 stable, #7 reduced amplitude, #6 single spike). The sentence 'preservation of active properties during retrieval is associated with recovery of synaptic proteins' should be explicitly framed as a hypothesis-generating observation, not a demonstrated association.
- The PCA clustering (Figure 6A) is used to support the claim that torn neurons cluster apart and that neuron #6 groups with no-gigaseal neurons, but the text does not report the variance explained by the first two principal components or whether clustering reflects retrieval quality rather than total protein yield driving the first component. A reader cannot determine what the axes represent or how much of the variance the separation captures.
- Several quantitative claims state direction without the actual quantity: e.g., 'torn or aspirated neurons produced the fewest detected proteins' and '1,400-2,300 proteins detected per soma' for no-gigaseal retrievals are given, but the torn-neuron protein counts are not stated, so the reader cannot compare the categories quantitatively.
- The estimate that '25-50% of the soma could be lost over the course of collection' is presented without any description of how this was measured or derived, leaving the reader unable to determine what evidence supports the range.
- The term 'shotgun patch-SCP' is introduced in the abstract and used throughout but is never formally defined at first use; the reader must infer it means indiscriminate collection of all patch attempts, which is stated only later in the Results.

## Questions
- Could the authors report the raw capacitance and protein identification values for the three gigaseal-preserved neurons, so readers can assess the correlation without relying on the regression fit?
- For the PCA in Figure 6A, could the authors report the variance explained by the first two principal components and state whether the clustering is robust to normalization or scaling choices?
- How was the 25-50% soma loss estimate derived, and what measurement supports it?