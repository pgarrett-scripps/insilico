# Contribution & Prior-Work Reviewer

Now let me assess the contribution systematically. Based on my searches, I have identified:

1. **Prior patch-SCP work exists**: The manuscript cites Lee et al. 2024 (locus coeruleus), Ghatak et al. 2024 (Alzheimer's iPSC neurons), and Choi et al. 2022 (capillary electrophoresis-MS). These are all recent patch-SCP studies.

2. **The Johnson et al. 2026 preprint** on "Proteome-Driven Phenotyping of Identified Single Neurons in Intact Brain Tissue by Aspiration Patch Proteomics" appears to be concurrent or very recent work in the same space.

3. **Patch-seq precedent**: Cadwell et al. 2016 established the framework for combining electrophysiology with transcriptomics (Patch-seq), which the manuscript builds on.

Now I'll write the review.

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a framework for interpreting patch-clamp single-cell proteomics (patch-SCP) in acute brain slices, with emphasis on soma retrieval quality as a determinant of proteomic depth and biological fidelity. The authors collected 12 rat mPFC pyramidal neurons using a "shotgun" strategy (analyzing all retrieval outcomes regardless of success) and correlated electrophysiological properties during retrieval with proteome yield and composition. The work is technically sound, clearly reported, and makes a useful methodological contribution by systematizing how retrieval mechanics influence proteomic interpretation. However, the novelty is incremental and the empirical scope is limited.

## Strengths

1. **Honest treatment of retrieval variability**: Rather than discarding failed or partial retrievals, the authors analyze all outcomes and use them to define contextual limitations, which is methodologically mature and practical for small-scale exploratory work.

2. **Explicit linking of electrophysiology to proteome yield**: The correlation between soma capacitance (measured during retrieval) and protein identifications (r² = 0.998, n=3) provides a quantitative bridge between passive membrane properties and proteome recovery, a relationship not previously demonstrated in patch-SCP.

3. **Comprehensive data deposition and reproducibility**: Raw MS data, search files, and videos of all soma retrievals are publicly available, enabling inspection of the retrieval process and reanalysis of the proteomes.

## Weaknesses: Load-Bearing Claims

**1. Gigaseal preservation during retrieval predicts proteome recovery and synaptic enrichment.**

The manuscript claims that maintaining the gigaseal during soma relocation enables "continued electrophysiological monitoring of soma properties" that can predict both proteome yield and the recovery of synaptic proteins. However, the evidence rests on n=3 neurons, all successfully retrieved with gigaseals intact. The correlation between capacitance and protein identifications (Figure 3D) is extraordinarily tight (r² = 0.998), which is suspicious for a biological system and suggests either overfitting to a tiny sample or that the relationship is driven by a confound (e.g., pipette geometry or technical factors correlated with both capacitance measurement and protein recovery). More critically, the claim that gigaseal preservation predicts *synaptic enrichment* is supported only by qualitative GO term comparison across three neurons (Figure 4B–C). Neuron #6, which had a gigaseal but poor spiking, showed reduced synaptic GO enrichment, but neuron #7 (also gigaseal-preserved, also poor spiking) showed robust synaptic enrichment—contradicting the hypothesis. The authors acknowledge this inconsistency but do not resolve it. The sample size is too small to establish that spike integrity during retrieval causally predicts synaptic protein recovery rather than reflecting post-hoc selection bias or confounding by neuron size. A larger dataset with stratified retrieval outcomes would be needed to test this claim rigorously.

**2. Retrieval loss decouples in situ electrophysiology from proteome composition.**

The manuscript argues that in situ recordings (made before retrieval) do not predict proteome recovery because mechanical disruption during extraction can cause unpredictable material loss. This is supported by showing that pre-retrieval capacitance and resistance do not correlate with protein identifications in the larger cohort (n=6, Figure 5C–D). However, this finding is not surprising: of course, if a soma tears during extraction, the pre-retrieval recording becomes irrelevant. The more interesting and unresolved question is whether the *quality* of retrieval (as assessed by gigaseal preservation and spike integrity) can be predicted *prospectively* from in situ properties, or whether retrieval outcome is essentially stochastic. The manuscript does not show that in situ recordings are uninformative for predicting retrieval success; it only shows they do not predict final protein count. This is a weaker claim than advertised. Moreover, the manuscript does not quantify the extent of soma loss during retrieval (estimated at 25–50%, stated as preliminary), which is central to interpreting the decoupling.

**3. The "shotgun" strategy of analyzing all retrievals provides actionable benchmarking of retrieval quality.**

The authors claim that comprehensive analysis of all patch outcomes (including failures) enables "benchmarking retrieval integrity and molecular coverage" better than selective inclusion. However, the evidence is largely qualitative: PCA clustering (Figure 6A) shows that torn neurons separate from others, and GO enrichment patterns (Figure 6B) vary across outcome categories. These observations are sensible but do not demonstrate that the shotgun approach yields *more* interpretable or *more* reliable conclusions than selective inclusion would. The authors do not compare their framework to a selective-inclusion approach on the same dataset, nor do they show that the additional information from failed retrievals changes any biological conclusions. The claim that this approach "reduces the risk of overinterpreting protein counts in isolation" is stated but not empirically validated.

## Weaknesses: Sweep

- **Sample size and generalizability**: n=12 neurons from one region (mPFC L2/3) in one species (rat) is insufficient to establish whether the framework generalizes to other neuronal types, brain regions, or species, particularly given the high variability observed.

- **Incomplete recovery of transmembrane proteins**: The manuscript acknowledges that several GPCR families of "high biological interest" (opioid, adrenergic, serotonergic, CRF1) were not detected, and ion channel subunit recovery ranged from 4 to 27 proteins per neuron; this undermines the claim that the workflow reliably captures the molecular basis of electrophysiological properties.

- **Confounding of soma size with retrieval quality**: Larger neurons yield more proteins (Figure 3D), but the manuscript does not disentangle whether this reflects better retrieval of large somas or whether large somas are inherently easier to retrieve without damage; this distinction matters for interpreting whether the framework applies to smaller neurons.

- **DIA vs. DDA comparison absent**: The manuscript uses DIA (data-independent acquisition) rather than the DDA (data-dependent acquisition) used in prior patch-SCP studies (Lee et al., Ghatak et al.), but does not compare the two approaches on the same samples, so the contribution of DIA to improved protein recovery is unclear.

- **Capacitance-protein correlation driven by n=3**: The extraordinarily high r² (0.998) for the capacitance–protein correlation (Figure 3D) is based on only three neurons and is not validated in the larger cohort (n=6, Figure 5C–D shows no correlation), suggesting the relationship may not be robust.

- **SynGO enrichment as a proxy for retrieval quality is not validated**: The manuscript uses GO term enrichment patterns to infer retrieval quality (e.g., neuron #6 lacked synaptic enrichment despite high protein count), but does not independently verify this inference (e.g., via imaging, morphological reconstruction, or orthogonal markers).

- **Concurrent work not discussed**: A recent preprint (Johnson et al. 2026, bioRxiv) on "Proteome-Driven Phenotyping of Identified Single Neurons in Intact Brain Tissue by Aspiration Patch Proteomics" appears to address overlapping questions about soma retrieval and proteome recovery; this work is not cited or compared.

- **Framework applicability to cytoplasmic patch-SCP unclear**: The manuscript focuses on soma retrieval but acknowledges that prior patch-SCP work relied on cytoplasmic aspiration; the framework's applicability to that modality is not discussed.

## Questions

- **Figure 3D**: Can you provide the raw data and fit diagnostics for the capacitance–protein correlation (n=3)? The r² = 0.998 is unusually high; are there any outliers, and does the fit remain significant if one neuron is removed?

- **Figure 4C**: Neuron #7 shows robust synaptic GO enrichment despite poor spike integrity during retrieval, contradicting the hypothesis that spike preservation predicts synaptic enrichment. How do you reconcile this?

- **Methods**: What is the basis for the 25–50% soma loss estimate? Can you provide quantitative measurements (e.g., from capacitance changes, protein recovery curves, or imaging) to support this range?

- **Supplementary data**: Are the raw DIA-NN outputs (report.pg_matrix.tsv) and custom analysis scripts available at the GitHub link provided, and have they been tested for reproducibility by an independent user?

---

## Overall Assessment

This is a competent methodological paper that makes a useful but incremental contribution to patch-SCP. The key insight—that retrieval mechanics, not just in situ electrophysiology, determine proteomic recovery—is sound and well-motivated. The framework for contextualizing patch-SCP outcomes is practical and the data are transparently reported. However, the empirical scope is narrow (n=12 neurons, one region, one species), the sample size for the load-bearing claims is very small (n=3 for the capacitance correlation), and the novelty over prior patch-SCP work (Lee et al. 2024, Ghatak et al. 2024, Choi et al. 2022) is primarily methodological rather than biological. The manuscript does not establish that gigaseal preservation prospectively predicts retrieval success or that the shotgun analysis strategy yields more reliable conclusions than selective inclusion. The work is suitable for publication as a methods paper with appropriate caveats about generalizability, but it does not represent a major advance in the field.