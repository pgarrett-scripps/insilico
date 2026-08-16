# Reproducibility Reviewer

SCORE: 3  
CONFIDENCE: 4

## Summary

This manuscript presents a proof-of-concept framework for combining patch-clamp electrophysiology with single-cell proteomics in acute brain slices, with a focus on how soma retrieval quality affects proteomic interpretation. The authors introduce a "shotgun" strategy of indiscriminate collection, demonstrate that gigaseal-preserved retrieval correlates with protein identifications via capacitance, and show that retrieval integrity influences synaptic protein recovery. The work is exploratory with n=12 neurons, and the authors are appropriately cautious about sample size. From a reproducibility standpoint, the paper is partially reproducible: data are deposited, but code availability is incomplete, and several procedural details are insufficiently specified for an independent group to rerun the workflow end-to-end.

## Strengths

1. Raw mass spectrometry data are deposited with working accessions (MassIVE MSV000099156, ProteomeXchange PXD068359), and videos of retrieval attempts are on Zenodo with a DOI.
2. The framework explicitly acknowledges and categorizes retrieval failure modes rather than discarding them, which is a useful methodological contribution.
3. The authors are candid about limitations, including the small sample size and the inability to recover complete ion channel assemblies.

## Weaknesses

### Load-bearing

**1. The central claim — that gigaseal-preserved retrieval links capacitance to protein identifications — rests on n=3 with a regression that is almost certainly overfit.** The authors report F = 1577, p < 0.05, adjusted R² = 0.998 for log-transformed capacitance versus protein identifications. With three points, any monotonic relationship will produce a near-perfect fit; the adjusted R² of 0.998 is not informative at this sample size. The claim that "soma size plays a more direct role in protein recovery than RM" is not established by this analysis. The authors should report the raw data points (capacitance and protein counts for each of the three neurons) and state explicitly that this is a descriptive observation, not a statistical association. A permutation test or a statement that no inference is intended would clarify the strength of the claim.

**2. The claim that "preservation of active properties during retrieval is associated with recovery of synaptic proteins" is based on a comparison of three neurons with different outcomes, but the authors do not control for the confounding variable of soma size.** Neuron #6, which had the poorest spiking, was also the smallest by capacitance. The authors themselves note that capacitance correlates with protein identifications. Therefore, the reduced synaptic enrichment in neuron #6 could be explained by size alone, not by retrieval integrity. To distinguish these, the authors would need to compare neurons of similar capacitance with different spike preservation, or at minimum acknowledge that size and spike integrity are confounded in this dataset. As written, the claim that "the physiological condition of soma retrieval... may be associated with the recovery of synaptic proteins" outruns the evidence.

**3. The PCA clustering (Figure 6A) is presented as evidence that "comprehensive analysis can distinguish between high- and low-context retrievals," but the clustering is not quantitatively validated.** The authors state that torn neurons cluster apart and that neuron #6 groups with no-gigaseal neurons, but no variance explained, loadings, or cluster stability metrics are reported. With 12 samples and thousands of protein features, PCA can produce apparent separation driven by a few outlier proteins (e.g., contamination or digestion artifacts) rather than meaningful biological signal. The authors should report the top contributing proteins to the principal components and show that the separation is not driven by a small number of high-variance features.

### Sweep

- **Code availability is incomplete:** the GitHub link (https://github.com/LarryThePharmacologist) is provided in the methods, but no repository name, commit hash, or archived DOI is given; the link as written resolves to a user profile, not a specific repository — HARD for any figure that depends on custom scripts.
- **The DIA-NN search parameters are underspecified:** the manuscript states "library-free mode with match-between-runs" and "oxidation as a variable modification," but does not report the precursor FDR threshold, the mass accuracy settings, the quantification strategy (MaxLFQ is mentioned but not the specific DIA-NN settings), or the version of the UniProt mouse proteome (download date given as 2024, but the exact release is not stated) — HARD for reproducing the protein identification lists.
- **The SynGO analysis pipeline is not reproducible from the text:** the authors state "GSEA filtering was performed under stringent conditions" without specifying the software, version, parameters, or the exact gene list input format; the custom scripts referenced in the GitHub link are not identifiable — HARD for reproducing Figures 4B-C, 6B, S2, and S3.
- **The sample processing protocol has a gap:** the manuscript states samples were digested at 37°C for 2 hours with 7 ng trypsin, but does not specify the digestion buffer composition (beyond 0.02% DDM), the reduction/alkylation steps (if any), or the quenching procedure details — an independent group would need to guess these settings.
- **The FAIMS compensation voltage and DIA window scheme are specified, but the gradient details are incomplete:** "36-minute gradient at 400 nL/min" is given, but the mobile phase composition (e.g., acetonitrile percentage, formic acid concentration) and the gradient shape are not described — SOFT, as these are standard but not recoverable without contacting the authors.
- **The electrophysiology analysis software NeuroExpress is cited, but the version and the specific parameters used for passive property extraction are not described** — the authors state "linear fits and extrapolated at I = 0 pA" but do not specify the fitting window or the criteria for accepting a fit — SOFT.
- **The "torn" neuron categorization is based on visual inspection during retrieval, but the criteria for categorizing a neuron as "torn" versus "gigaseal lost" are not operationally defined** — a replicator would not know how to classify ambiguous cases — SOFT.

## Questions

1. For the capacitance–protein identification regression (Figure 3D), can you report the three individual data points (capacitance values and protein counts) and state whether this is intended as a descriptive observation or a statistical claim?
2. Can you provide the specific GitHub repository name and commit hash for the custom analysis scripts, or deposit them in an archived repository (e.g., Zenodo) with a DOI?
3. For the SynGO analysis, can you specify the exact software version, the gene list input format, and the "stringent conditions" parameters (e.g., minimum gene set size, FDR method)?
4. Can you describe the reduction/alkylation steps (if any) in the digestion protocol, and the exact mobile phase composition and gradient shape for the LC-MS run?
5. For the PCA in Figure 6A, can you report the variance explained by the first two principal components and the top contributing proteins, to confirm the clustering is not driven by a few outlier features?