# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 5

## Summary

dnoise is a well-engineered tool that removes points from native Bruker timsTOF .d files and writes reduced-size native-compatible output. The core claim—that 35–53% of MS1 frame data can be removed with negligible impact on label-free quantification and identification—is supported by a controlled benchmark on a three-species standard. The design is sound for the tested scope, the evidence is transparent, and the authors are candid about limitations. The work is incremental (denoising is not novel; the contribution is implementation and validation for this specific format) but solid and useful. One load-bearing claim requires clarification, and the generalizability boundary needs tightening in the abstract.

## Strengths

1. The benchmark is well-designed: a defined three-species mixture with known ratios, replicated across two gradients and two acquisition modes, with orthogonal validation (PSM/peptide/protein counts, LFQ accuracy, feature-level intensity agreement, precision).

2. The authors transparently report the confound (on-instrument MS1 denoising enabled only for ddaPASEF, not diaPASEF) and do not overstate the comparison between modes; they acknowledge this limits interpretation of the DDA–DIA reduction difference.

3. The streak filter is validated against a fair comparator (matched-intensity threshold), showing it preserves weak signal better and loses fewer true identifications when extended to MS/MS frames, with explicit decoy-hit analysis supporting the mechanism.

## Load-bearing claims

**Claim 1: Default MS1-only denoising preserves label-free quantification accuracy.**

Evidence: Figure 3 and Table S3 show median log₂ ratios for all condition pairs and species under original vs. MS1-denoised arms. The authors report that ratios "followed the same expected ratios over the full benchmark range" and that "neither accuracy nor precision showed a systematic degradation attributable to denoising."

The problem: The benchmark uses a *single* three-species standard at a *single* load (50 ng) on a *single* instrument (timsTOF Ultra 2) across two gradients. The claim as stated in the abstract—"Label-free quantification accuracy was preserved in both modes"—generalizes to the method, but the evidence is restricted to this one sample type and instrument. The authors do acknowledge this in Section 3.7 ("The replicated benchmark remains controlled and narrow"), but the abstract and headline do not. The alternative explanation is not that the result is false, but that it may not hold for sparse data, low input, different sample matrices, or other timsTOF models. This is not a design flaw; it is a scope mismatch between the claim and the evidence. The fix is to narrow the abstract claim to "in the tested three-species benchmark" or to move the generalization to a conditional statement ("*can* preserve accuracy when...").

**Claim 2: The default configuration removes 35–53% of the frame binary with negligible analytical cost.**

Evidence: Table S5 reports frame-binary reduction (49.5–53.4% for ddaPASEF, 34.7–39.6% for diaPASEF) and identification/quantification metrics. For ddaPASEF, PSM/peptide/protein counts are identical between original and MS1-denoised arms (as expected, since MS/MS is untouched). For diaPASEF, precursor and protein-group counts change by 0.2–2.2% and 0.2–1.6%, respectively.

The problem: The claim of "negligible analytical cost" rests on the assumption that small changes in precursor and protein-group counts are analytically acceptable. But the authors do not define what constitutes negligible, do not report confidence intervals around these percentages, and do not test whether the lost precursors are random or enriched for low-abundance or edge-case features. The 2.2% precursor loss at 15 minutes is not trivial if those precursors are systematically biased (e.g., all from one species, or all low-abundance). The authors note that DIA-NN derives MaxLFQ from fragment chromatograms, so MS1 filtering does not directly alter quantification, but they do not show that the lost precursors do not bias the protein-level result. A direct check: report the species composition and abundance distribution of the lost precursors, and test whether protein-level ratios change when those precursors are excluded from the original arm. This would show whether the loss is random or systematic.

**Claim 3: dnoise is fast enough for routine post-acquisition use.**

Evidence: Table S16 reports processing times of 7.4–68.7 seconds across 72 files on a single workstation (i7-12700H, 20 threads), all faster than the shortest gradient (5 minutes).

The problem: This is well-supported for the tested hardware and file sizes (up to ~7 GB). However, the claim "fast enough for routine post-acquisition use" depends on the user's workflow. If the user's bottleneck is data transfer (which the authors cite as a motivation), then 69 seconds is negligible. If the bottleneck is analysis turnaround, it is also fast. But if the user runs dnoise on every file immediately after acquisition and then transfers the reduced file, the wall-clock time is still 69 seconds per file, which at high throughput (e.g., 10 files per day) is 11.5 minutes of overhead. This is not a flaw in the result, but the claim should be conditional: "fast enough to run immediately post-acquisition without delaying transfer" is more precise than "fast enough for routine use." The evidence supports the narrower claim fully.

## Sweep

1. The parameter selection (Section 2.2) uses one homogeneous sample (Condition A, 15-minute ddaPASEF) as a grid-sweep benchmark, making the 15-minute ddaPASEF results not fully out-of-sample; the authors acknowledge this, but it weakens the claim that the defaults are universally optimal.

2. The optional MS/MS denoising trades 7–12% of peptide identifications for 70–74% frame reduction; the authors correctly recommend MS1-only as default, but do not provide guidance on when the tradeoff is acceptable (e.g., for archival vs. discovery).

3. The halo filter (Section 2.1) is disabled by default because "a sufficiently weak co-eluting ion could meet the same criteria," but no ablation shows how often this occurs or how much signal is lost by disabling it.

4. The streak filter's max_internal_gap and min_feature_length are fixed across all four acquisition/gradient combinations; no sensitivity analysis shows whether these should be tuned per-gradient or per-instrument.

5. The benchmark does not test whether denoising improves downstream analysis (e.g., does smaller file size enable faster database search, or does it reduce memory pressure in high-throughput pipelines?).

6. Native-format compatibility is validated by "point-for-point identical" round-trip through dnoise (Section 2.4), but not by testing whether third-party software (MaxQuant, Skyline, etc.) reads the denoised .d files without error.

7. The authors state that "every filter parameter is exposed in the configuration," but do not provide a user guide or worked example for adapting defaults to new sample types.

## Questions

- For diaPASEF, can you report the species composition and abundance rank of the 0.2–2.2% of lost precursors, and test whether protein-level MaxLFQ ratios change when those precursors are excluded from the original arm?
- Does the 2.2% precursor loss at 15-minute diaPASEF occur uniformly across all three species, or is it enriched for low-abundance or edge-case features?
- Have you tested whether third-party software (MaxQuant, Skyline, Spectronaut) reads the denoised .d files without error or warning?