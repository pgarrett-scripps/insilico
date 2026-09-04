# Desk Screen Assessment: dnoise

## Summary

This manuscript describes dnoise, an open-source Rust tool for removing uninformative points from native Bruker timsTOF mass spectrometry data while preserving analytical results. The work is evaluated against In Silico's scope and standards.

## Scope Assessment

**In scope.** The manuscript presents original research on a computational method for data reduction. It includes:
- A clearly described algorithm (streak filter, halo filter, acquisition-aware gates)
- Empirical validation on a defined benchmark (three-species mixture, ddaPASEF and diaPASEF modes, 5- and 15-minute gradients)
- Reproducible evidence: public raw data (PRIDE PXD070049), open-source code (github.com/pgarrett-scripps/dnoise, v0.1.0 archived at Zenodo), complete parameter tables, and search configurations
- Quantitative outcomes (data reduction, identification retention, label-free quantification accuracy, precision, runtime)

The work is methodological and computational, not clinical guidance or diagnostic recommendation. It makes checkable claims against deposited materials.

## Threshold Issues

**None identified.**

1. **Completeness:** The manuscript is complete. Raw data, code, parameters, and configurations are all publicly available and versioned. The authors explicitly state what was used and where to find it.

2. **Clarity:** The manuscript is clearly written. The filtering logic is explained step-by-step, the benchmark design is transparent, and limitations are acknowledged (single instrument, one laboratory, controlled sample, need for validation across sparse/low-input data).

3. **Evidence-claim alignment:** The central claim—that default MS1-only denoising removes 35–53% of frame data while preserving quantification and identification—is directly supported by the benchmark results. The optional MS/MS mode trades identifications for greater reduction, which is honestly reported. The authors do not overstate the scope of validation.

4. **Soundness of design:** The benchmark is well-designed for its stated purpose. The three-species mixture with known ratios is a standard for LFQ validation. The use of both ddaPASEF and diaPASEF, two gradients, and six replicates per condition provides reasonable coverage. The comparison to a matched-intensity-threshold control (Section 3.4) is a useful ablation. The authors acknowledge that the 15-minute ddaPASEF results are not fully out-of-sample (parameter selection used Condition A of that arm), but the 5-minute gradient and both diaPASEF acquisitions were held out.

5. **Reproducibility:** All materials are in place. The authors used publicly available tools (Sage, DIA-NN, timsrust) with versioned releases and explicit configurations. The code is open-source and archived.

## Minor Observations

- The paper is positioned as a tool paper with a narrow but well-defined validation scope. This is appropriate for the venue.
- The authors are transparent about limitations: single instrument, controlled sample, need for validation across sparse data and other labs. This is candid reporting.
- The optional centroiding modes (Section 3.5) are interesting but secondary; they do not affect the main claim.
- The use of AI tools (Claude) for manuscript drafting and analysis-script development is disclosed, with the caveat that no AI tool generated images or altered experimental data. This is acceptable transparency.

## Recommendation

The manuscript is in scope, complete, clearly written, and supported by reproducible evidence. The claims are appropriately scaled to the evidence. The work will be of interest to proteomics researchers and to adjacent fields concerned with data reduction and storage efficiency in high-throughput mass spectrometry. The public availability of code and data, combined with the honest treatment of limitations, makes this suitable for open review.

**DESK DECISION: proceed**