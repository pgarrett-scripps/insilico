# Reproducibility Reviewer

## Summary
The study is well-executed and unusually candid, and the proteomics data is genuinely deposited (PXD076102) with detailed analysis parameters — a real strength. But the two most load-bearing claims rest on artifacts that are not reproducible as described: the proteomic analysis code is unversioned and the search library is not fully specified, and the co-culture/cryo-TEM evidence is gated behind "reasonable request" with unspecified image-analysis parameters. These are fixable, but as written an independent group could not rerun the analysis end-to-end. Score 3.

## Strengths
- The mass-spectrometry data is deposited with a working PRIDE accession (PXD076102), and the DIA-NN/MSstats versions and processing parameters are specified in unusual detail.
- The vFC assay is described with calibration standards, controls (buffer/reagent/detergent, dilution series), and MISEV/MIFlowCyt-EV compliance, making that measurement reproducible.
- The manuscript explicitly flags its own uncertainties (e.g., 'trended towards a wider, though not significantly different, size distribution'), which aids honest evaluation.

## Weaknesses
- LOAD-BEARING — Proteomic signature (the 170/184 differentially abundant proteins and the 'failed AEV biogenesis' autophagy argument): the data is deposited, but the search was run against a 'predicted Homo sapiens library containing 20,405 reviewed sequences (downloaded from Uniprot: 22 Oct 2024)' — a DIA-NN predicted library is generated from a FASTA, and neither the FASTA accession/version nor the library-generation parameters are given, so the exact search space cannot be reproduced. The analysis code is at a GitHub URL with no commit/tag or archived DOI, so the exact version that produced the results is not pinned. Both are HARD for rerunning this analysis; the data deposit is the strength, the code/library specification is the gap.
- LOAD-BEARING — Co-culture transfer and increased intratissue Aβ in WT (Fig 7): the quantification rests on Arivis image analysis (Cellpose nucleus model, Simple Threshold operator, ROUT outlier removal), but the threshold and segmentation parameters are not specified, the raw images are not deposited ('available on reasonable request'), and the n=27 vs n=49 are image counts with no stated number of independent organoids/replicates, so the unit of replication is unclear. Without the threshold settings and raw data, the 'significant increase in Aβ XP segment volume per cell' cannot be reproduced or independently verified. I could not inspect the figures.
- LOAD-BEARING — Cryo-TEM morphology (MLVs and luminal fibrils in AD EVs, Fig 4): the fibril identification is qualitative manual inspection, the authors state '2D class averaging did not yield identifiable features,' and the micrographs are not deposited. The claim that AD EVs contain fibrillar material 'resembling PHF-type tau' is a key structural finding that I cannot verify from the text and whose raw data is on-request.
- The organoid differentiation protocol is 'performed in accordance with a previously established protocol (Labra et al. 2026)'; that reference appears to be in press/2026, so if it is not yet published or deposited, the core culture procedure is not resolvable to an independent group.
- No computational environment is captured (no conda env, lockfile, or container) for the R/DIA-NN analysis, and no random-seed or seed-averaging statement is given for the stochastic steps (DIA-NN search, Cellpose segmentation).
- The vFC EV-count comparison (3.1e9 vs 1.6e9 EVs/mL) is reported as a single measurement per condition with no replicate count stated, so its reproducibility cannot be assessed.
- The STED FWHM vesicle-size estimate is derived from a single representative punctum per condition with no replicate statistics.

## Questions
- Can you provide the Uniprot FASTA accession/version and the DIA-NN library-generation parameters, and pin the analysis code to a commit/tag or archived DOI?
- What are the exact Arivis Simple Threshold and Cellpose segmentation parameters, how many independent organoids (not images) underlie each co-culture condition, and can the raw images be deposited?
- Is the Labra et al. 2026 protocol currently published or deposited anywhere an independent group can access it now?
- Can the cryo-TEM micrographs supporting the MLV/fibril claim be deposited, and what explicit criteria were used to classify a structure as a fibril?