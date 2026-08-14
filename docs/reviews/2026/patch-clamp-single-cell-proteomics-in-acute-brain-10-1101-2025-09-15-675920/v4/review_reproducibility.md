# Reproducibility Reviewer

## Summary
This manuscript presents a genuinely useful framework for patch-SCP, and the authors have made a good-faith effort to deposit data (MassIVE/PXD accession, Zenodo videos). However, the reproducibility artifacts are incompletely specified: the custom code is at a non-versioned user URL, the Supporting Information DOI is a literal placeholder, and the analysis pipeline (SynGO parameters, PCA preprocessing, figure-to-script mapping) is not described at the level needed for an independent group to rerun the work end-to-end. These are fixable, but they are HARD issues as written.

## Strengths
- The authors specify instrument and software versions for the MS acquisition (Orbitrap Astral, DIA-NN v1.8.1, R 4.3.1) and give detailed DIA parameters (resolution, mass range, window width, NCE, FAIMS CV).
- The inclusion policy is stated explicitly ("we did not impose selection or exclusion criteria for either soma retrieval or MS analysis"), which is important for reproducibility.
- The data deposit is described with a MassIVE/PXD accession, which is the right venue for raw MS data.

## Weaknesses
- The central quantitative claim — protein identifications correlate with log-transformed capacitance (Figure 3D, F = 1577, R² = 0.998, n = 3) — cannot be independently recomputed from the manuscript as written. The supporting tables (S1–S3) are referenced throughout but the Supporting Information DOI is a literal placeholder ("https://pubs.acs.org/doi/xxxxxxxxxxx/"), so the per-neuron capacitance values and protein counts are not accessible. With n = 3, the correlation is also statistically fragile (data_analysis's call), but from a reproducibility standpoint the raw values must be in the deposit for the claim to be checkable. The MassIVE/PXD accession is given, but I cannot verify it resolves; the placeholder DOI is verifiably broken.
- The SynGO enrichment analysis (Figures 4B–C, 6B; Tables S2–S3) is not reproducible as specified. The manuscript states "Gene set enrichment analyses were performed on gene lists derived from DIA-NN's protein-level output" but does not give the SynGO database version, the enrichment algorithm, the background distribution, or the minimum gene-set size. The custom scripts are said to be "available at https://github.com/LarryThePharmacologist" — a user profile URL with no repository name, commit hash, or tag. An independent group cannot know which code version produced the reported enrichment terms.
- The PCA (Figure 6A) that supports the claim that retrieval outcomes cluster by proteomic content is underspecified. The manuscript does not state the preprocessing applied to the protein intensity matrix (normalization, imputation, scaling) before PCA, nor which script produces the figure. Without this, the clustering pattern cannot be reproduced.
- R package versions (ComplexHeatmap, ggplot2, UpSetR) are not specified — SOFT.
- UniProt reference proteome is given only as "downloaded 2024" with no release number — SOFT.
- No figure-to-script mapping is provided for any key figure; the manuscript never names a script that produces a specific figure — HARD.
- The "performed as previously described [10, 26-31]" citations resolve to published procedures, which is acceptable, but I could not verify the references contain the full protocol — SOFT.
- The Zenodo DOI for videos is given, but I cannot verify it resolves — SOFT (peripheral artifact).

## Questions
- Can the authors provide a specific repository URL with a commit hash or tag for the custom scripts?
- Can the authors provide the resolved DOI for the Supporting Information, and confirm Tables S1–S3 are accessible there?
- Can the authors specify the SynGO database version and the exact GSEA parameters (algorithm, background, minimum gene-set size) used for the enrichment analysis?