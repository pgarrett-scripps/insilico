# Reproducibility Reviewer

## Summary
This is a substantial and interesting neurobiology manuscript, but from a reproducibility standpoint it is not yet rerunnable end-to-end. The central load-bearing claims — that Hrs depletion alters AMPAR kinetics and that Hrs overexpression drives GluA1-S831 phosphorylation — rest on electrophysiology and biochemistry whose raw data, analysis code, and procedural parameters are not deposited or fully specified. Several load-bearing datasets are gated behind 'available on request' or 'upon publication' promises, which is a HARD flag for this venue.

## Strengths
- The manuscript reports a clear, falsifiable central claim — Hrs bidirectionally modulates AMPAR function — and provides multiple independent lines of evidence (electrophysiology, biochemistry, phosphoproteomics) that could in principle be cross-checked.
- The authors describe the PSD purification and synaptosome isolation protocols in enough stepwise detail that an independent group could reproduce the biochemical fractionation.
- The mass spectrometry pipeline is described with instrument, gradient, and search parameters, and the raw data are promised to a public repository (PXD073715).

## Weaknesses
- The electrophysiology data — the load-bearing evidence for altered AMPAR kinetics and AMPA/NMDA ratio — are not deposited anywhere. The manuscript reports only summary statistics and representative traces; there is no raw trace archive, no per-cell dataset, and no analysis script. An independent group could not reproduce the reported rise-time, decay-slope, and slow-current percentages from the described inputs. This is a HARD reproducibility break on the paper's central claim.
- The phosphoproteomics raw data are promised 'upon publication' (PXD073715) but no accession is live; the manuscript states the data 'is publicly available in the ProteomExchange depository (PXD073715)' — a promise, not a working accession. For a load-bearing dataset this is a HARD flag under the 'upon publication' rule.
- The AAV-Hrs-HA overexpression and Hrsf/fSyn1-Cre experiments report only densitometric western blot quantifications; the underlying blot images, replicate-level values, and the analysis pipeline are not deposited. The GluA1-S831 and PKC-substrate claims therefore cannot be independently recomputed.
- The manuscript does not state random seeds or a seed-averaging statement for any of the analyses, and the mass spectrometry search and TMT normalization parameters are described in prose but not consolidated into a single reproducible pipeline document.
- The 'surface biotinylation' assay is described with reagent and steps, but the exact biotinylation time, temperature, and wash conditions are not fully specified, and the input-normalization step is not described in enough detail to reproduce the reported 40% reduction.

## Questions
- Can you provide the raw electrophysiology traces and the per-cell dataset (rise time, decay slope, AMPA/NMDA ratio, slow-current classification) as a deposited supplementary file or repository, with the analysis script used to compute the reported statistics?
- Can you confirm the PXD073715 accession is live and provide the raw and processed phosphoproteomics data, with the TMT normalization and search parameters consolidated into a single reproducible pipeline document?
- Can you specify the exact biotinylation conditions (time, temperature, wash steps) and the input-normalization procedure for the surface biotinylation assay, so an independent group could reproduce the reported 40% reduction in surface GluA1?