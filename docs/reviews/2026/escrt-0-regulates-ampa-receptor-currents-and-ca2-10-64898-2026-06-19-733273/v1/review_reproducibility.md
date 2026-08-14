# Reproducibility Reviewer

## Summary
On the reproducibility dimension this is a mixed paper. The wet-lab protocols are given in genuinely usable detail, the mass spectrometry raw data is deposited with an explicit ProteomeXchange accession (PXD073715), and analysis thresholds are quantified rather than hand-waved. But the two load-bearing genetic manipulations — the shRNA knockdowns and the HA-Hrs overexpression — are not obtainable from the text, and the custom R analysis that produced the phosphoproteomics figures is not deposited. Those gaps are HARD but all fixable by deposit or full specification, hence major revision rather than rejection.

## Strengths
- Wet-lab procedures (PSD fractionation, surface biotinylation, slice electrophysiology) contain enough step-level and parameter detail to follow without contacting the authors.
- The mass spectrometry raw data is accessioned (PXD073715) with search and quantification thresholds stated (FDR 1%, S/N 100, localization 75%).
- Electrophysiological inclusion/exclusion and measurement windows are specified numerically (series resistance >30 MΩ or >30% variation excluded; NMDAR sweeps <5 pA excluded; 20–80% rise, 100–37% decay).

## Weaknesses
- _Load-bearing: the knockdown reagents are unidentifiable._ The AAV-shHrs used for all physiology is identified only as "VectorBuilder, Chicago, IL," with no target sequence, scrambled-control sequence, backbone, promoter, or titer; the lentivirus used for the Figure S3 knockdown validation has no source at all. The knockdown-efficiency evidence shown is from dissociated neurons transduced with lentivirus, not from the organotypic slices in which the recordings were made. An independent group cannot reproduce the manipulation, and a different target site could plausibly give a different phenotype. Remedy: publish both target and scrambled sequences (with reference transcript and species), vector backbones, titers, and knockdown quantification in organotypic slices.
- _Load-bearing: the phosphoproteomics analysis code is absent._ The Figure 4/S5 pipeline is described in unusually good prose (normalization to unmodified intensities, Welch t-test, unadjusted p<0.05), and the raw data is accessioned, but the R code is not deposited, and one decision is genuinely ambiguous: for phosphopeptides mapping to multiple UniProt IDs "only a single uniprot ID was considered" — by what rule? Without the scripts, the figures are not rederivable from the accession without an unverifiable reconstruction. Remedy: deposit the analysis and figure-generation scripts with the PXD record, and state the disambiguation rule.
- _Load-bearing: the HA-Hrs overexpression cassette is underspecified._ No species of the Hrs cDNA, tag position, plasmid backbone, or deposit; "AAV-GFP" is not stated to be the same backbone with the insert swapped out. The capsid (CAP-B10) is traceable to Goertsen et al. 2022 and the titer is given, but the transgene itself cannot be obtained identically. Remedy: report the full expression cassette and deposit the plasmid.

## Questions
- What are the shRNA target and scrambled-control sequences for both the lentiviral and AAV reagents, with vector backbones and titers — none of these appear in the text?
- Which species' Hrs cDNA is encoded in AAV-Hrs-HA, where is the HA tag, and where is the plasmid deposited?
- Where are the R scripts that produced Figures 4 and S5, and what rule selects the single UniProt ID when a phosphopeptide maps to several?
- How many biological replicates underlie the surface-biotinylation quantification in Figure 3N?