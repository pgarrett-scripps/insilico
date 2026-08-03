# Reproducibility Reviewer

## Summary
The manuscript deposits MS data (PXD080813) and analysis code (Zenodo), enabling computational reproducibility, but omits critical wet-lab protocol details — LC-MS/MS acquisition parameters, click chemistry/enrichment conditions, and lysis buffer composition — that prevent full experimental replication. The in silico pipeline is well documented with software versions, but the proteomics sample preparation and acquisition steps lack sufficient specification for an independent group to reproduce the primary dataset.

## Strengths
- MS raw data deposited in PRIDE (PXD080813) and R analysis scripts archived on Zenodo with a resolvable DOI.
- Statistical thresholds (log2FC > 1, p < 0.05), software (limma, STRING v12.0/v11.5), and genome assemblies clearly cited.
- Cross-referencing of three genome assemblies (Dm28c 2014/2017/2018) strengthens robustness of protein identification.

## Weaknesses
- LC-MS/MS acquisition parameters absent: instrument model, column, gradient, MS1/MS2 settings, and acquisition mode (DDA/DIA) are not reported, making proteomics data acquisition irreproducible. The manuscript states only "LC-MS/MS analysis" without any instrumental parameters.
- Click chemistry and streptavidin enrichment protocol incomplete: probe concentration, incubation time, CuAAC reagent concentrations, streptavidin bead amount, wash buffers, and elution conditions are not specified, preventing replication of the enrichment step that defines the dataset.
- Lysis buffer composition and conditions not disclosed: the text mentions "optimisation of the lysis conditions" but provides no final recipe (detergents, salts, pH, temperature, duration), yet lysis efficiency directly affects which proteins are accessible for labelling and enrichment.
- Protein inference and LFQ processing pipeline not fully described: software (MaxQuant? FragPipe? Spectronaut?), search engine, FDR thresholds, match-between-runs, imputation method, and normalization strategy are omitted; the R scripts may contain this but the manuscript does not summarize it.
- Supplementary Data files 1–5 and Supplementary Figures S1–S3 are cited throughout but their availability is not confirmed in the data availability statement.
- No random seed reported for any stochastic step in the analysis pipeline.
- No computational environment capture (conda/container) provided for the R workflow, only scripts.
- AlphaFold model versions cited (v6) but no confirmation that the exact models are permanently archived.
- Genome assembly accession numbers for Dm28c 2014/2017/2018 not provided, only citations.
- Probe identities in Figure 2 lack chemical names or catalog numbers, relying on color coding only.

## Questions
- What are the exact LC-MS/MS instrument parameters (instrument, column, gradient, MS settings)?
- What is the complete click chemistry and streptavidin enrichment protocol (concentrations, times, buffers)?
- What is the final optimized lysis buffer composition and procedure?
- Which software and parameters were used for peptide/protein identification and LFQ quantification?
- Are Supplementary Data 1–5 and Supplementary Figures S1–S3 deposited in a public repository?
- Can the R scripts at Zenodo be run end-to-end from raw MS files to final figures without manual intervention?