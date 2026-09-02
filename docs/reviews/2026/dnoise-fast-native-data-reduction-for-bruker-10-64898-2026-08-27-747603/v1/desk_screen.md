# Desk Screen: dnoise – Fast Native Data Reduction for Bruker timsTOF

## Summary

This manuscript presents dnoise, an open-source Rust tool that removes uninformative points from Bruker timsTOF mass spectrometry data while preserving the native .d file format. The work combines ion-mobility streak filtering, halo removal, and acquisition-aware geometric gates to reduce frame data volume by 35–53% (MS1-only mode) while maintaining label-free quantification accuracy and identification counts across ddaPASEF and diaPASEF acquisitions.

## Scope Assessment

**In Scope for In Silico:** Yes. This is original methodological research with:
- A clearly stated computational problem (timsTOF data volume)
- A novel technical solution (native-format denoising tool)
- Empirical validation on a defined benchmark
- Open-source code and public data deposits
- Claims that can be evaluated from the manuscript and deposited materials

The work is neither clinical guidance nor marketing material, and its central evidence is presented and reproducible.

## Threshold Issues

### 1. Completeness of Evidence
**Status: Adequate.** The manuscript provides:
- Complete parameter tables (Table S1, extensive Supporting Information)
- Public raw data (PRIDE PXD070049)
- Software release with DOI (zenodo.org, crates.io)
- Reproducible search configurations (Sage, DIA-NN)
- Sufficient procedural detail to repeat the work

### 2. Soundness of Method
**Status: Sound, with appropriate caveats.** The design is reasonable:
- Benchmark uses a defined three-species standard with known ratios
- Comparisons include both MS1-only and optional MS/MS modes
- Controls are present (matched intensity-threshold comparison, Section 3.4)
- Quantification validated via label-free approaches in both DDA and DIA modes
- Authors acknowledge limitations (Section 3.7): single instrument, single laboratory, controlled sample, need for validation on sparse/low-input data

The parameter selection (Section 2.2) uses one homogeneous subset of the benchmark for grid sweep, which the authors transparently note makes the 15-minute ddaPASEF results not fully out-of-sample. This is a minor methodological point, not a fundamental flaw.

### 3. Claims vs. Evidence
**Status: Well-calibrated.** The headline claims are:
- "35–53% reduction in frame binary" — directly measured and reported per-run
- "LFQ accuracy preserved" — demonstrated across species and condition pairs with confidence intervals
- "ddaPASEF PSM/peptide/protein counts unchanged" — expected and confirmed (MS/MS untouched)
- "diaPASEF precursor/protein counts changed only slightly" — quantified (0.2–2.2% change)
- "Processing in <69 seconds" — measured on all 72 runs

All claims are supported by the evidence presented. The authors appropriately flag MS/MS denoising as a tradeoff (7–12% identification loss for 70–74% frame reduction) and recommend MS1-only as default.

### 4. Novelty and Contribution
**Status: Incremental but useful.** The authors acknowledge prior work:
- PNNL PreProcessor exists for other ion-mobility platforms but not Bruker
- Peak detection and feature finding operate post-conversion to mzML
- Search pipelines read native .d but do not write reduced .d

The specific contribution — removing points directly from native Bruker .d while preserving format compatibility — appears novel and fills a practical gap. The work is not groundbreaking algorithmically (streak filtering and geometric gates are standard techniques), but the engineering and validation are solid.

### 5. Reproducibility
**Status: Excellent.** The manuscript provides:
- Open-source code (MIT licensed, github.com/pgarrett-scripps/dnoise)
- Versioned software release (v0.1.0, Zenodo DOI)
- Public benchmark data (PRIDE, no access restrictions)
- Complete configuration files and search parameters (Section S7)
- Sufficient detail to rerun the benchmark

### 6. Clarity and Honesty
**Status: High.** The authors:
- Clearly state the problem and motivation
- Explain each filter stage with examples (Figure 1)
- Provide ablations (Table S4)
- Acknowledge the parameter-selection bias (Section 2.2)
- Discuss limitations explicitly (Section 3.7)
- Recommend MS1-only mode despite MS/MS being available
- Advise retention of original files

The writing is clear and the tone is appropriately cautious about generalization.

## Potential Concerns (Not Desk-Reject Level)

1. **Limited scope of validation:** Single instrument, single laboratory, one sample type (three-species digest), two gradients. The authors acknowledge this and recommend further validation. This is a limitation to flag in review, not grounds for rejection.

2. **Parameter selection bias:** The 15-minute ddaPASEF results use part of the benchmark for parameter tuning. The 5-minute gradient and both diaPASEF modes are out-of-sample, and the bias is disclosed. Reviewers may ask whether the results hold with fully independent parameters, but this is not a fundamental flaw.

3. **On-instrument denoising confound:** ddaPASEF had on-instrument MS1 denoising enabled; diaPASEF did not. This explains part of the difference in reduction between modes but is not a flaw in the work — it reflects real-world instrument configuration.

4. **Streak filter assumptions:** The method assumes ions are sampled over consecutive mobility scans. The authors note this may require relaxation for sparse or single-cell data. This is an appropriate caveat, not a disqualifying limitation.

## Venue Fit

**In Silico scope:** The manuscript is in scope. It presents original research with checkable claims, deposited materials, and public code. The review will be useful to both specialists in timsTOF proteomics and adjacent researchers evaluating whether the tool is trustworthy for their own use.

---

## DESK DECISION: proceed

**Rationale:** This is a well-executed methodological paper with sound design, complete evidence, excellent reproducibility, and appropriate caveats. The contribution is incremental but fills a practical gap (native-format denoising for Bruker timsTOF). The authors are transparent about limitations and parameter selection. The work is suitable for full peer review. Reviewers should assess whether the benchmark scope is sufficient for the claims and whether validation on additional instruments and sample types is necessary before widespread adoption, but these are questions for the panel, not grounds for desk rejection.