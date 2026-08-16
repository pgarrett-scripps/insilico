# Clarity & Presentation Reviewer

SCORE: 4  
CONFIDENCE: 4

## Summary

This is a clearly written, well-structured methods paper that introduces a framework for interpreting patch-clamp single-cell proteomics (patch-SCP) outcomes in acute brain slices. The central contribution — that retrieval mechanics, not in situ electrophysiology alone, determine whether recovered proteomes reflect the neuron's physiology — is stated explicitly and supported by the data presented. The manuscript is unusually candid about its limitations, and the presentation is generally precise. My concerns are mostly SOFT issues of terminology consistency and a few places where the reader must infer procedural details that are stated only implicitly.

## Strengths

1. The central claim is stated explicitly and early: "retrieval mechanics, rather than in situ electrophysiology alone, limit whether proteins associated with excitability and synaptic function are recovered" — this gives the reader a clear through-line for the entire paper.
2. The framework figure (Figure 1) is a genuinely useful conceptual contribution that maps patch-clamp outcomes to interpretability, and it is referenced appropriately throughout.
3. The authors' decision to include torn/aspirated neurons as internal negative controls, and to report them transparently, is methodologically honest and strengthens the interpretive framework.

## Weaknesses

### Load-bearing

**1. The claim that "gigaseal preservation links neuron size to proteome recovery" rests on n = 3, and the correlation is presented without any indication of its fragility.** The manuscript reports "F = 1577, p < 0.05, adjusted R² = 0.998, n = 3" for the capacitance–protein-identification correlation. With three points, a single outlier drives the entire relationship, and the p-value threshold is barely crossed. The text does not acknowledge that this correlation would not survive a single additional data point that deviates from the trend. The claim is appropriately hedged elsewhere ("preliminary assessment"), but the figure legend and Results text present it with more confidence than n = 3 warrants. What would settle this: a statement of the confidence interval on the slope, or an explicit acknowledgment that the correlation is illustrative rather than inferential.

**2. The claim that "preservation of active properties during retrieval is associated with recovery of synaptic proteins" is supported only by a single case comparison, and the alternative explanation is not excluded.** The argument rests on neuron #6 (compromised spiking, no synaptic signaling enrichment) versus neurons #4 and #7 (stable/reduced spiking, enrichment present). But neuron #6 was also the smallest neuron by capacitance, and the authors themselves show that size correlates with protein yield. The observed difference in synaptic enrichment could therefore be explained entirely by soma size rather than by retrieval integrity. The manuscript does not attempt to separate these two variables — which is understandable given n = 3, but the claim as worded ("preservation of active properties... is associated with") implies a causal or at least independent relationship that the data cannot distinguish from the size effect. What would settle this: an explicit statement that size and retrieval integrity are confounded in this dataset, or a comparison of synaptic enrichment between two neurons of similar capacitance with different spike preservation.

### Sweep

- **Terminology inconsistency (SOFT):** "gigaseal-preserved retrieval," "gigaseal preserved during retrieval," and "retrieved under a gigaseal" are all used to describe the same condition; the reader must track that these are synonymous across Figures 3, 4, and 7.
- **Figure 5A color legend is ambiguous (HARD):** the text says "Colors denote the success-level of electrophysiological characterization throughout the patch-SCP process," but the figure caption does not define which color corresponds to which outcome category; the reader must infer from the text that red = no gigaseal, orange = gigaseal lost, green = gigaseal preserved, grey = torn. The caption should state this explicitly.
- **Methods order of operations is partially recoverable but has a gap (HARD):** the text states that pipettes were "immediately transferred to a 384-well non-binding microplate containing 15 µL of 0.02% DDM," then "the pipette tip was carefully snapped in the well plate." It is not stated whether the pipette is removed from the microplate before snapping, or whether the tip is snapped while still in the well — a reader attempting to replicate this step cannot determine the geometry of the procedure.
- **"Shotgun" is used in two senses (SOFT):** the abstract uses "shotgun" to describe the indiscriminate collection strategy, while the Methods section uses "shotgun" implicitly to describe the DIA acquisition mode; the term is never defined for either usage, and a reader unfamiliar with either convention may conflate them.
- **Figure 6A PCA is described but the variance explained is not reported (SOFT):** the text states that PCA "revealed clear separation of extreme cases," but no percentage of variance explained is given for the principal components shown; the reader cannot judge whether the separation is driven by the first two components or is an artifact of low-dimensional projection.
- **The phrase "higher-context retrievals shown in Figure S3" (in the Results section on transmembrane proteins) is a dangling reference (HARD):** Figure S3 is a SynGO cellular component heatmap, not a figure about retrieval context; the reader must infer that "higher-context" refers to the clustering pattern in Figure 6A, which is not stated at that point in the text.

## Questions

1. In Figure 5A, can the color legend be added directly to the figure caption so the reader does not have to cross-reference the text to identify outcome categories?
2. For the capacitance–protein-identification correlation (Figure 3D), what is the 95% confidence interval on the slope, and would the correlation survive if neuron #6 (the smallest) were excluded?
3. In the Methods, when the pipette tip is "snapped in the well plate," is the pipette still positioned vertically in the well, or is it removed and snapped at the rim? A one-sentence clarification would make the procedure reproducible.