# Reproducibility Reviewer

## Summary
The paper's three load-bearing claims — fibrillar material inside AD organoid EVs, differential EV proteomics, and EV-mediated Aβ transfer in co-culture — rest on pipelines of very uneven reproducibility. The proteomics is exemplary: instrument, software versions, search parameters, and statistical settings are all specified, with data deposited at PRIDE and code at GitHub. But the structural claim (fibrils) rests on cryo-EM micrographs that are not deposited anywhere, the reported EV concentrations cannot be reproduced because the final concentration factor is unspecified, and the co-culture Aβ quantification lacks a stated threshold and biological n. These are missing specifications, not missing evidence — fixable, but currently blocking independent verification of the paper's most novel findings.

## Strengths
- The proteomics pipeline is a model of reproducibility: DIA-NN v2.2.0 and MSstats v4.16.1 settings, the Uniprot library (dated), the cRAP filtering, and the PRIDE accession (PXD076102) are all given.
- The vFC assay follows MISEV/MIFlowCyt-EV guidance with calibration standards, detergent controls, and a dilution series to exclude swarm effects.
- The EV purification is described with device models (HBM-TFF/1, Izon qEV 35nm, VS0102) and volumes sufficient to repeat the core isolation.

## Weaknesses
- The fibrillar-material claim rests on cryo-EM micrographs that are not deposited. The central structural finding — AD organoid EVs contain "luminal fiber-like structures" and "fibrils with amyloid-like twists, resembling PHF-type tau" (Figure 4I) — is a visual identification. The micrographs are not deposited in EMPIAR or any accessible repository, and the data availability statement gates "all other data" behind "reasonable request," which is not availability. An independent group cannot verify the fibril identification or distinguish it from membrane fragments or staining artifacts. The fix: deposit the cryo-EM movies/micrographs with an EMPIAR accession and state the classification criteria for "fibril" vs. artifact.
- The reported EV concentrations are not reproducible because the final concentration factor is unspecified. The vFC reports "~3.1 e9 EVs/mL in the concentrated media compared to 1.6 e9/mL for the WT" (Figure 3), but the protocol says the 2 mL SEC eluate was concentrated "until the desired volume was reached" — the final volume, and hence the concentration factor from the 120 mL conditioned media, is not given. The reported per-mL concentrations cannot be reproduced or compared back to the original media. The fix: state the final volume and the overall concentration factor.
- The co-culture Aβ quantification cannot be rerun without the threshold value and biological n. The Aβ puncta analysis uses "Simple Threshold analysis operator" with no threshold value given, and the n=27 (WT+AD) / n=49 (WT+WT) images are not tied to a stated number of independent organoids per condition. The threshold directly determines the segment volume, so the reported increase in WT+AD cannot be reproduced. The fix: report the threshold value and the number of organoids per condition.
- The GitHub analysis code has no commit/tag or archived DOI, so the exact analyzed version is not pinned (SOFT).
- The custom Python scripts for the cryo-TEM violin plots are not deposited (SOFT).
- I could not verify that the PRIDE accession PXD076102 resolves; the format is correct but the link is unverified.
- The ThT assay compares 20 µg of EV protein against 2.5e6 liposomes without matching vesicle number or lipid content — a design-adequacy issue for methodology.
- The co-culture transfer claim lacks a transwell or EV-depleted-media control to distinguish EV-mediated transfer from free dye/Aβ in the media — a design-adequacy issue for methodology.

## Questions
- What is the final volume of the concentrated EV sample after the 10K MWCO spin column, and the overall concentration factor from the 120 mL conditioned media?
- Are the cryo-EM micrographs deposited (EMPIAR accession)? If not, can they be made available?
- What threshold value was used in the Arivis "Simple Threshold" operator, and how many independent organoids contributed to the n=27 and n=49 images?
- Does the GitHub repository have a tagged release or commit hash?