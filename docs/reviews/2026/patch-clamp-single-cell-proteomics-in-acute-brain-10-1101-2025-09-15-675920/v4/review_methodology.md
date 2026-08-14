# Methodology Reviewer

## Summary
This paper presents a conceptual framework for interpreting patch-clamp single-cell proteomics by monitoring neuron retrieval. The idea is interesting and the experimental workflow is generally sound, but the design does not support the core claims as stated. The central evidence rests on correlations and comparisons that are fatally under-powered—three neurons for the gigaseal-preserved condition, single examples per retrieval category—so the reported associations could arise from chance, pre-existing biological variation, or uncontrolled confounds. The contribution is a proof-of-concept and a useful framework to discuss, but the manuscript's conclusions substantially outrun what the design can establish.

## Strengths
- The idea of using patch-clamp single-cell proteomics to monitor neuron retrieval is conceptually interesting and addresses a real methodological gap.
- The experimental workflow for retrieving and processing single neurons for MS is generally sound and described in sufficient detail.
- The PCA-based observation that torn neurons cluster separately (Fig 6A), while underpowered, points toward a potentially useful diagnostic signal worth exploring.
- The 'shotgun' indiscriminate-collection framework is a thoughtful conceptual contribution even though the present evidence does not validate it.

## Weaknesses
- Correlation between capacitance and protein identifications (Figs 3D, 3E) is supported by a linear regression on n=3 points; with three data points any line fits almost perfectly, and the reported adjusted R² of 0.998 and p<0.05 are an artefact of the sample size. Three neurons may also differ in cell type, health, time from slice preparation, or operator skill, none of which is controlled.
- Association between active property preservation and synaptic protein recovery (Figs 4A–4C) rests on a single example per retrieval outcome (neuron #4 stable spiking, neuron #7 reduced amplitude, neuron #6 single spike). With n=1 per category, any difference in SynGO enrichment could reflect cell-to-cell variability, slice health, or technical variation in MS coverage.
- Retrieval outcomes (gigaseal preserved, lost, no gigaseal, torn) are not controlled—they arise from mechanical success or failure, not random assignment. Neurons easier to retrieve may differ systematically (size, adhesion, cell type, slice location). Proteomic differences between categories could reflect pre-existing biological differences rather than retrieval integrity.
- The 'shotgun' indiscriminate-collection strategy is presented as a framework but no comparison is made to the alternative (e.g., pre-specified inclusion criteria). The utility of the framework is asserted but not tested.
- Sample size (n=12 total, n=3 for the key gigaseal-preserved group) is too small for reliable statistical inference; no power analysis is provided.
- No blinding or randomisation is described for electrophysiology recordings, soma retrieval, or MS analysis; subjective decisions (e.g., when to apply suction) could influence outcomes.
- Per-neuron SynGO analyses use a single run per neuron; with n=1 per cell enrichment Q-values are unstable and should be interpreted as exploratory, not confirmatory.
- Number of neurons attempted vs successfully retrieved is not reported, so selection bias cannot be assessed.
- Correlation analysis in Figure 3 uses log-transformed capacitance without justification; with only three data points the transformation choice is arbitrary and inflates R².
- The claim that 'the smallest neuron (#6) exhibited the fewest enriched cellular component terms' confounds two explanations—smaller size and poorer retrieval—which the design cannot separate.
- No attempt is made to match or covary for neuron location (depth in slice), slice preparation time, or cell-type identity.

## Questions
- Can you provide data from additional neurons in the gigaseal-preserved category to support the correlation between capacitance and protein identifications? How many more recordings would be needed for a minimally convincing regression?
- How many neurons were patched in total, and what proportion were excluded from analysis (e.g., because the soma could not be retrieved or the sample was lost)? Is there any systematic bias in which neurons succeeded or failed retrieval?
- The PCA in Figure 6A shows clustering; have you tested whether the clusters correspond to measured confounds such as neuron depth, time after slice preparation, or cell size (from DIC images)?
- For the SynGO enrichment comparisons: were the gene lists used for each neuron normalised for the number of detected proteins? Could the apparent lack of synaptic enrichment in neuron #6 simply reflect lower total protein IDs rather than a selective loss?