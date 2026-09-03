# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 5

## Summary

This manuscript describes dnoise, a Rust tool that removes points from native Bruker timsTOF .d files while preserving analytical results. The work is reproducible in its essentials: raw data are publicly deposited, software is open-source with a versioned release, parameters are fully specified, and the authors provide complete search configurations. The benchmark is well-designed and results are reported with appropriate detail. One substantive reproducibility concern exists around parameter selection, and several minor gaps affect the completeness of the record, but none prevent independent reconstruction of the central claims.

## Strengths

1. Complete software release (v0.1.0) with MIT license, versioned on Zenodo and crates.io, and point-for-point validation of read/write fidelity through unfiltered round-trip testing.

2. Public raw data (PXD070049) with defined mixture ratios, enabling orthogonal validation of quantification accuracy claims across species and condition pairs.

3. All procedural parameters exposed in configuration (Table S1) and search commands fully specified (Section S7), with explicit software versions for Sage, DIA-NN, and timsrust.

## Weaknesses: Load-bearing claims

**Parameter selection introduces in-sample bias that is not fully disclosed.** The authors state (lines 91–109) that min_feature_length and max_internal_gap were selected by grid sweep on "one homogeneous sample, the six replicates of Condition A of the 15-minute ddaPASEF gradient," and then acknowledge (lines 107–109) that "the selection sample is part of the benchmark" and "the 15-minute ddaPASEF results are not fully out-of-sample." However, the framing obscures the severity: the parameters were tuned to maximize coverage and precision on the exact condition that appears in the final benchmark results (Table S5, rows for 15-min ddaPASEF Condition A). The authors then report those same results as evidence that default settings "preserve" quantification. This is not a hidden flaw—they flag it—but the presentation conflates a parameter-selection criterion (maximize coverage on Condition A) with a validation criterion (preserve coverage across all conditions). The 5-minute gradient and diaPASEF results are genuinely out-of-sample and do support the claim, but the 15-minute ddaPASEF arm is partially circular. The claim "default MS1-only denoising preserved LFQ accuracy in both modes" rests on all four arms equally; the 15-minute ddaPASEF arm should either be excluded from the main validation or reported separately with a confidence caveat. As written, a reader cannot immediately tell which results are independent evidence and which are not.

**Comparison to intensity threshold control does not isolate the streak filter's advantage.** Section 3.4 compares the streak filter to "a strict per-point intensity threshold calibrated to remove approximately the same fraction of points." The authors report (lines 260–276) that the streak filter "increasingly outperformed the per-point threshold as abundance fell" (Figure S5) and retained more quantified coverage in fragment frames (Figure S4). However, the control is not a fair comparison of the two filtering principles. The threshold was "calibrated separately for each tested acquisition" (line 261) to match removal fraction, but the streak filter's parameters were fixed across all four acquisition/gradient combinations. This means the threshold was tuned per-acquisition while the streak filter was not. If the threshold had been tuned once (as the streak filter was) and then applied to all four, it might have performed differently. The authors do not report whether the per-acquisition calibration of the threshold was necessary because the optimal cutoff differed across acquisitions, which would suggest the threshold is genuinely less robust. Without that information, the comparison shows only that a per-acquisition tuned threshold underperforms a fixed-parameter streak filter on the same data it was tuned on—a weaker claim than "the streak filter is better." The decoy-hit analysis (lines 277–285) is valuable and does support the streak filter, but it is a separate argument and should not be conflated with the abundance-dependent comparison.

**Centroiding results (Section 3.5) are presented without sufficient detail to reproduce.** The authors state that "the watershed centroider grows groups transitively and collapses each ion streak toward a single centroid" and "the box centroider instead tiles each streak into small fixed boxes" (lines 286–288), but do not specify the box size, the transitivity rule, or the intensity-weighting formula. They report that "the watershed reduced MS1 to 2% of the raw points and the frame binary to 34% of raw" and "the box centroider reduced MS1 to 10% (binary 40%)" (lines 289–290), but these are aggregate results. Figure S7 and Table S15 are referenced but not shown in the manuscript text provided. Without the algorithmic details and per-run breakdowns, a reader cannot verify that the centroiding stage works as claimed or reproduce it from the code alone without reverse-engineering from the output. The claim that "both preserved the label-free result" (line 291) rests on results that are not fully specified here.

## Weaknesses: Sweep

1. The halo filter is disabled by default in the configuration (Table S1, `halo_peak_fraction: 0.15` with no explicit disable flag shown), but the text states it "can be disabled" (line 87) without clarifying whether it is on or off by default or how to disable it in practice.

2. MS/MS filtering uses "relaxed msms_* parameters" (line 133) but Table S1 does not show what those parameters are or how they differ from the MS1 defaults, preventing reproduction of the optional mode.

3. The benchmark uses on-instrument denoising enabled for ddaPASEF but not diaPASEF (line 174), confounding the comparison of reduction between modes; the authors acknowledge this (lines 174–175) but do not quantify how much of the 54% difference in MS1 point removal is attributable to this versus acquisition design.

4. Precision is reported as "median pooled protein CV across conditions A and B" (line 162) but the pooling method (how CVs are combined across replicates and runs) is not specified in the main text, only referenced to Section S3.

5. The "percentile-bootstrap 95% confidence intervals" for accuracy (line 161) are calculated by "resampling shared contributing proteins" but the number of proteins in that shared set is not reported, making it impossible to assess whether the resampling is stable.

6. DIA-NN's "two-pass refinement" (line 149) is mentioned but not detailed; the manuscript does not specify what changed between passes or whether the same library was used in both.

7. The claim that "every denoised directory in this benchmark was processed by the same Sage and DIA-NN workflows as its unmodified original" (lines 309–310) is true for the tested arms, but the manuscript does not state whether the same .d directory was read multiple times or whether separate denoised copies were created for each arm, affecting reproducibility of the exact file I/O sequence.

8. Runtime measurements (Figure 6, Table S16) report "peak working-set memory" but do not specify the operating system, kernel version, or memory-mapping strategy, which affect reproducibility of memory profiles.

## Questions

1. For the 15-minute ddaPASEF arm: were the reported results (Table S5, rows for Condition A) generated with the parameters selected on that same condition, or were the parameters frozen before that arm was processed?

2. In Section 3.4, what was the optimal per-acquisition intensity threshold for the 5-minute ddaPASEF arm, and how did it differ from the 15-minute threshold, if at all?

3. Figure S7 and Table S15 are referenced for centroiding results but not provided in the manuscript text; are these in the Supporting Information PDF, and if so, do they include per-run breakdowns and the box-size parameter?

4. What is the exact formula for the intensity-weighted centroid coordinates in both the watershed and box centroiders, and what is the box size for the box centroider?