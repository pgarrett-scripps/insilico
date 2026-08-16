# Related-Work & Citations Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents a methodological framework for patch-clamp single-cell proteomics (patch-SCP) in acute brain slices, with a focus on how soma retrieval quality affects proteomic measurements. The authors introduce a "shotgun" strategy where all patched neurons are collected regardless of electrophysiological outcome, and they demonstrate that gigaseal preservation during retrieval correlates with protein identifications and synaptic enrichment. The work is positioned as a proof-of-concept framework rather than a definitive biological finding, which is appropriate given the small sample size (n=12 neurons). The citation record is largely sound, but there are several areas where the related-work coverage could be strengthened, particularly regarding the rapidly evolving patch-SCP literature.

## Strengths

1. The authors are appropriately candid about the exploratory nature of their work and scale their claims to match the small sample size.
2. The framework's explicit treatment of retrieval outcomes as an interpretive variable, rather than a binary pass/fail criterion, is a genuinely useful conceptual contribution.
3. The indiscriminate collection strategy, including torn neurons as internal controls, is a thoughtful experimental design choice.

## Weaknesses

**Load-bearing claim 1: The claim that gigaseal preservation during retrieval enables quantitative prediction of proteome recovery via capacitance.** The correlation between log-transformed capacitance and protein identifications (F = 1577, p < 0.05, adjusted R² = 0.998, n = 3) is presented as evidence that soma size links to proteome yield. With n = 3, this correlation is driven by three data points, and the adjusted R² of 0.998 is almost certainly overfit. The authors do acknowledge the small sample size, but the strength of the claim ("providing a means of linking soma size to proteome recovery") outruns what three points can support. A more defensible statement would frame this as a suggestive observation requiring validation. The alternative explanation — that the correlation reflects variability in retrieval mechanics rather than soma size per se — is not excluded, since the three neurons also differed in retrieval difficulty (as the authors themselves note in the discussion of neurons #6 and #7).

**Load-bearing claim 2: The claim that preservation of spiking during retrieval is associated with synaptic protein enrichment.** The comparison of neurons #4, #6, and #7 is used to argue that spike integrity during relocation tracks synaptic enrichment. With n = 1 per condition, this is a case study, not a comparison. The authors acknowledge this limitation, but the framing in the Results ("preservation of neuronal spiking during relocation tended to be associated with broader synaptic enrichment") is presented as a finding rather than an anecdote. The alternative explanation — that the differences reflect neuron-to-neuron biological variability in synaptic protein content rather than retrieval integrity — is not excluded. The authors would need multiple neurons per retrieval-integrity category to distinguish these.

**Load-bearing claim 3: The claim that in situ recordings do not predict proteome recovery.** The finding that neither capacitance nor RM measured in situ correlates with protein identifications (n = 6, p > 0.05) is used to argue that retrieval mechanics decouple proteomics from electrophysiology. This is a null result from a small sample, and the absence of a correlation in six neurons is weak evidence for a true absence of association. The authors frame this appropriately as a limitation, but the conclusion ("retrieval loss decouples proteomic measurements from electrophysiology") is stated more strongly than the evidence supports. A power analysis or a statement about what effect size this sample could detect would strengthen the claim.

**Sweep items:**

- The reference to Choi et al. (2022) [7] as an example of cytoplasmic patch-SCP in brain slices is accurate, but the manuscript does not engage with the more recent work by the same group on patch-clamp proteomics in tissue, which would strengthen the positioning of the present contribution (SOFT).
- The claim that "early efforts combined patch-clamp electrophysiology with targeted transcript detection using single-cell RT-PCR" is attributed to Lambolez et al. (1992) [5], which is the correct primary source; however, the manuscript does not cite the more recent Patch-seq methodological reviews that would contextualize the current state of the field (SOFT).
- The reference to Ghatak et al. (2024) [9] as an example of patch-SCP in hiPSC-derived neurons is accurate, but the manuscript does not acknowledge that this work also reported challenges with compartment-specific protein recovery, which is directly relevant to the present framework's motivation (SOFT).
- The citation of Gatto et al. (2023) [13] for methodological guidelines is appropriate, but the manuscript could also cite the more recent single-cell proteomics benchmarking literature that has emerged since 2023 (SOFT).
- The reference to Bernaerts et al. (2025) [25] for the Patch-seq modeling work is current and appropriate; however, the manuscript does not cite the earlier Patch-seq papers that established the transcriptomic-electrophysiological correlation approach, which would help position the proteomic contribution (SOFT).
- The self-citation pattern is proportionate; the authors cite their own prior work on mPFC electrophysiology (e.g., [10], [26-31]) where it is genuinely relevant (no issue).
- The reference list is generally resolvable, but several entries lack DOIs (e.g., [15], [16], [17], [18]), which would be a minor improvement for reproducibility (SOFT).
- The claim that "patch-SCP in the locus coeruleus of mice revealed sex-specific differences" [8] is accurately attributed, but the manuscript does not acknowledge that this work also used a selection strategy (only neurons with stable recordings were analyzed), which is directly relevant to the present framework's contrast with that approach (SOFT).

## Questions

1. For the capacitance–protein identification correlation (Figure 3D), can the authors report the same analysis with a larger sample of gigaseal-preserved retrievals, or state the minimum effect size their current n = 3 could detect?
2. Can the authors confirm whether the SynGO enrichment differences between neurons #4, #6, and #7 persist when the analysis is restricted to proteins detected in at least two of the three neurons, to control for single-neuron stochasticity?
3. For the claim that in situ recordings do not predict proteome recovery, can the authors report the power of their n = 6 comparison to detect a meaningful correlation, or provide a confidence interval for the correlation coefficient?