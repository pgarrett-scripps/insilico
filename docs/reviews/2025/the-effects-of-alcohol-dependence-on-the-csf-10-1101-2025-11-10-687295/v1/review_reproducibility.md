# Reproducibility Reviewer

## Summary
The manuscript reports a detection-based (presence/absence) DIA-MS comparison of CSF proteomes between alcohol-dependent and non-dependent mice, with a secondary claim that an intraperitoneally administered anti-IL-6R antibody is detectable in CSF. The procedural detail for the MS pipeline is genuinely strong — DIA-NN version, search settings, filtering thresholds, detection criteria, and the rat-proteome search for the antibody are all specified to a level that an independent group could largely reconstruct. The blocking issues are availability: the R analysis code is explicitly gated ("private until published"), and the MassIVE accession cannot be verified from the manuscript text. Both are load-bearing for reproducing the figures and the analysis pipeline.

## Strengths
- The DIA-MS parameters are unusually complete: DIA-NN v 2.1.0, the exact search settings (protease, missed cleavages, mods, MBR disabled), the proteome version and download date, the 60-window/10 m/z isolation scheme, and the 1% FDR filtering thresholds are all stated.
- The detection criteria and group-preference thresholds (≥3/4 vs ≤1/5 for strong evidence, etc.) are explicitly defined, and the power limitation is candidly disclosed with a post-hoc calculation.
- The antibody-detection claim is backed by a described two-step procedure (rat-proteome DIA-NN search, then Skyline validation with named intensity/RT models), with the species-unique peptide DILLISQNAK identified as such.

## Weaknesses
- The analysis code is not available, and it is load-bearing. The R scripts that filter the DIA-NN output, apply the detection criteria, run the enrichment and power analyses, and generate Figures 1–5 are at a GitHub repository described as "private until published." Per the manuscript's own account, the code is gated behind publication, which for a preprint under review means it is not accessible now. An independent group could not reproduce the figures or the exact analysis pipeline without reconstructing the R code from the prose description. The fix is concrete: make the repository public or deposit an archived version (e.g., Zenodo DOI) at submission, and state the commit/tag.
- The MassIVE data accession cannot be verified, and it carries the raw MS data and sample annotations. The manuscript states the data "have been uploaded" with identifier C5GX4573B, but I cannot confirm from the text that this accession resolves and is public. If the identifier is live and open, this is fine; if it is a placeholder or gated, the underlying data for every load-bearing claim are unavailable. I could not verify this either way — please confirm the accession is public and resolvable, and note any access conditions.
- The power-analysis method is not specified (which test, what effect-size model, what assumptions produced 38% for 75% vs 20% detection) — a replicator cannot recompute it.
- No environment capture for the R analysis (no lockfile, conda env, or container), and the STRING web-tool version is not stated — SOFT, since the core pipeline is versioned.
- Supplementary Files 1–4 (filtered quantitative data, IGG2B peptides, Skyline exports, peak-area histograms) are referenced but not visible in the manuscript text provided, so I could not confirm their contents or format.
- Compute/hardware for the LC-MS runs is not noted — minor for this analysis, but relevant if the 15 spd method's performance is load-bearing for the detection-based comparison.

## Questions
- Can you confirm the MassIVE accession C5GX4573B is public and resolvable now, and state whether any access conditions apply?
- Will the GitHub repository be made public (or archived with a DOI) at the time of preprint posting rather than at journal publication, and can you state the commit/tag?
- What test and assumptions underlie the reported post-hoc power figures (38% for 75% vs 20% detection rates)?