# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

dnoise is a well-engineered tool that removes points from native Bruker timsTOF .d files and writes native-compatible output. The core claims—that MS1-only denoising reduces frame binary by 35–53% while preserving label-free quantification accuracy and identification counts—are supported by the benchmark evidence on a defined three-species mixture. The design is sound for its stated scope, controls are appropriate, and the authors are candid about limitations. The work is incremental but useful: it fills a practical gap (no prior open-source tool writes reduced native .d files) and demonstrates the feasibility of point-level denoising without analytical loss in the tested regime. The main validity concern is scope: a single instrument, one sample type, two gradients, and two acquisition modes do not establish that the defaults generalize. The optional MS/MS mode trades identifications for reduction in a way the authors acknowledge but do not fully characterize mechanistically. Minor issues include a confounded comparison between DDA and DIA reduction, and incomplete reporting of the matched-intensity control. These do not undermine the MS1-only claims but limit confidence in some secondary conclusions.

## Strengths

1. The authors provide complete parameter values, software release, raw data, and reproducible configurations, enabling independent verification of every reported result.

2. The streak filter is validated against a fair comparator (matched-intensity threshold) showing it preserves weak signal better than absolute cutoffs, with mechanistic explanation via decoy-hit enrichment.

3. The paper is transparent about limitations: single instrument, controlled sample, narrow gradient range, and the confound between on-instrument denoising and acquisition mode are all stated explicitly.

## Load-Bearing Claim 1: MS1-only denoising reduces frame binary by 35–53% while preserving label-free quantification accuracy

**Evidence:** Figure 2 and Table S5 report frame-binary reduction (ddaPASEF 53.4% and 49.5% at 5 and 15 min; diaPASEF 39.6% and 34.7%) alongside quantified protein counts and LFQ accuracy (Figure 3, residual log₂ ratios). ddaPASEF PSM, peptide, and protein counts are unchanged. diaPASEF precursor and protein counts change by 0–2.2%. Precision (Figure 4) shows no systematic degradation.

**Alternative explanation:** The reduction could be an artifact of the benchmark's particular composition or acquisition parameters rather than a general property of timsTOF data. The three-species mixture at 50 ng is a commercial standard with known ratios; it is not representative of complex proteomes, single-cell inputs, or low-abundance samples. The authors acknowledge this ("one timsTOF Ultra 2 instrument, one laboratory, one 50 ng three-species sample") but do not test whether the same parameters preserve quantification on a different sample type, load, or instrument. A user applying these defaults to a novel sample has no empirical basis to expect the same outcome.

**What would settle it:** The claim as stated ("a substantial fraction of native timsTOF frame data can be removed with little analytical change") is defensible if narrowed to the tested conditions: "on a defined three-species benchmark at 50 ng load on a timsTOF Ultra 2, MS1-only denoising with default parameters reduces frame binary by 35–53% while preserving LFQ accuracy and identification counts." The current wording invites generalization beyond the evidence. Alternatively, a second independent sample (different species mix, load, or instrument) processed with the same defaults would establish whether the result is robust or sample-specific.

## Load-Bearing Claim 2: The streak filter preserves weak signal better than a per-point intensity threshold

**Evidence:** Section 3.4 and Figure S5 compare the streak filter to a matched-intensity threshold calibrated to remove approximately the same fraction of points. Within shared ddaPASEF peptide-run pairs, the streak filter stays closer to the original LFQ intensity as abundance falls, whereas the threshold produces downward bias. The explanation offered is that the streak filter retains mobility-coherent signal that a fixed cutoff discards. Section 3.4 also reports that fragment filtering removes decoy hits faster than target hits under the streak filter (decoy-to-target loss ratio 1.77–2.34) but inverts this ratio under the threshold (0.43–0.57).

**Alternative explanation:** The matched-intensity threshold may be an unfair comparator. The authors calibrate it "separately for each tested acquisition while holding the streak-filter configuration fixed" to achieve "comparable removal." However, "comparable" is defined only as removing "approximately the same fraction of points." Figure S5 shows the threshold removes ~81% of MS1 points in ddaPASEF (matching the streak filter's 81.2%), but the figure does not report whether the two filters remove the same fraction of *fragment* points, where the mechanistic claim is tested. If the threshold removes a different fraction of fragment peaks, the comparison is not removal-matched and the decoy-hit enrichment difference could reflect different stringency rather than filter design. The decoy-hit analysis is compelling, but it rests on the assumption that the two filters are equally stringent on fragment spectra.

**What would settle it:** Report the fraction of fragment points removed by both filters in the matched-intensity control (ddaPASEF at both gradients), alongside the current MS1 comparison. If the threshold removes a substantially different fraction of fragment peaks, the comparison is confounded and the mechanistic claim requires a fair-stringency control.

## Load-Bearing Claim 3: Optional MS/MS denoising trades identifications for greater reduction in a predictable way

**Evidence:** Section 3.3 reports that MS1+MS/MS denoising reduces the frame binary by 70.7–74.3% while identified peptide counts fall by 7–12% in ddaPASEF and precursor/protein-group counts change by several percent in diaPASEF. The authors explain the apparent inconsistency (more quantified proteins despite fewer identified peptides) as a filtering-induced shift in the decoy-to-target ratio: weakly supported identifications are enriched for false matches, so removing them raises the fraction passing the LFQ q-value gate. Figure S6 shows that rank-1 decoy hits fall by 42.7–48.1% while target hits fall by 18.2–27.2%.

**Alternative explanation:** The explanation is plausible but incomplete. The authors show that fragment filtering removes decoys faster than targets, but they do not show that this effect is *caused* by the streak filter's design rather than by the fact that weak spectra (which are enriched for decoys) happen to contain fewer mobility-coherent peaks. A spectrum with a weak true signal and a weak false signal might both be removed by the streak filter for the same reason: sparse mobility structure. The decoy enrichment could be a side effect of removing sparse spectra generally, not evidence that the streak filter preferentially identifies false matches. This does not invalidate the result, but it leaves the mechanism unclear.

**What would settle it:** Compare the decoy-to-target loss ratio under MS/MS denoising for the streak filter versus the matched-intensity threshold. If the streak filter's decoy enrichment is due to its mobility-coherence logic, it should differ from the threshold's ratio. If both filters show similar decoy enrichment, the effect is driven by sparsity rather than streak structure, and the mechanistic claim should be reworded.

## Sweep

1. **Confounded DDA vs. DIA comparison:** On-instrument denoising was enabled for ddaPASEF but not diaPASEF, so the larger reduction in diaPASEF (93.5% vs. 81.2% of MS1 points) cannot be attributed to acquisition mode alone; the authors acknowledge this but do not quantify its magnitude.

2. **Parameter selection bias:** The geometric parameters (min_feature_length=5, max_internal_gap=2) were selected by grid sweep on Condition A of the 15-minute ddaPASEF gradient, which is part of the benchmark; the 5-minute gradient and both diaPASEF acquisitions are out-of-sample, but the 15-minute ddaPASEF results are not fully independent.

3. **Incomplete centroiding characterization:** Section 3.5 reports that the watershed centroider reduces MS1 to 2% of raw points and preserves the label-free result, but does not report whether downstream tools (Sage, DIA-NN) can read the centroided .d files or whether the native-format compatibility claim holds for this extreme reduction.

4. **Missing ablation for halo filter:** Table S4 shows the halo filter removes a small fraction of MS1 points, but does not report its effect on MS/MS frames or on identification counts in either mode.

5. **Quantification method asymmetry:** ddaPASEF uses Sage's mobility-aware MS1 LFQ (precursor integration across retention time and mobility), while diaPASEF uses DIA-NN's fragment-based MaxLFQ; the two methods are not directly comparable, and MS1 denoising affects them differently by design.

6. **Runtime comparison missing:** The paper reports that dnoise completes in ≤69 seconds but does not report the time cost of downstream analysis (Sage or DIA-NN searches) or the total wall-clock savings from reduced file size during transfer or analysis.

## Questions

1. **Figure 1 caption and padding:** The caption states "the benchmark configuration pads its edges to protect the isotopic envelopes of edge precursors"—what are the padding values in m/z and mobility, and how sensitive are the results to this choice?

2. **Fragment-frame removal in matched-intensity control:** Does Figure S4 report the fraction of fragment points removed by the threshold filter, and if so, does it match the streak filter's removal rate?

3. **Centroiding and downstream compatibility:** Can Sage and DIA-NN read the centroided .d files produced by the watershed and box centroiders, or is native-format compatibility limited to the point-removal modes?