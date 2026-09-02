# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 5

## Summary

This manuscript presents dnoise, a Rust tool that removes points from native Bruker timsTOF .d files while preserving analytical results. The work is reproducible in its essentials: raw data are publicly deposited, software is released with version control, parameters are fully specified, and the end-to-end workflow from raw .d through denoising to database search is documented. The authors have made a genuine effort to enable independent verification. However, one critical gap in the reporting of the parameter-selection process undermines confidence in whether the default configuration was truly optimized fairly, and a second issue around the benchmark's representativeness creates ambiguity about generalizability claims that the paper does not adequately flag.

## Load-bearing claims

**Claim 1: Default MS1-only denoising reduces frame binary by 35–53% while preserving label-free quantification accuracy and identification counts.**

The evidence is Figure 2, Table S5, and Figures 3–5. The reduction figures are straightforward and reproducible from the code. The preservation claim rests on three separate assertions: (1) ddaPASEF PSM/peptide/protein counts are identical (Table S5); (2) LFQ accuracy (median log₂ ratios) is preserved across species and condition pairs (Figure 3, Tables S10–S11); and (3) feature-level intensities remain tightly correlated (Figure 5). 

The first assertion is sound—the default mode leaves MS/MS untouched, so identical search results are expected and observed. The second and third are empirically supported by the reported data. However, the authors do not report whether the quantified *protein set* is identical between original and denoised arms, only that accuracy and precision of *shared* proteins are preserved (Section 3.2: "quantified proteins and median within-condition CV changed slightly"). This is a weaker claim than "quantification is preserved"—if denoising causes some proteins to drop below the two-peptide, two-replicate reporting threshold while others cross it, the quantified set could shift even if shared proteins remain accurate. The paper acknowledges this happens under MS/MS filtering (Section 3.3, explaining the apparent inconsistency in Table S5) but does not clearly state whether it occurs under MS1-only filtering. Table S5 shows quantified protein counts for the original and MS1-only arms; inspection reveals small changes (e.g., 5-minute ddaPASEF: 2,847 vs. 2,851 proteins). The authors should explicitly report whether these differences are due to proteins crossing reporting thresholds or other causes, and whether the set of quantified proteins overlaps sufficiently that the "preservation" claim is accurate as stated.

**Claim 2: The parameter defaults (min_feature_length=5, max_internal_gap=2) are appropriate and were selected objectively.**

The evidence is Section 2.2 and Table S2. The authors performed a grid sweep on "one homogeneous sample, the six replicates of Condition A of the 15-minute ddaPASEF gradient" and selected parameters that "removed a large fraction of MS1 points while quantifying slightly more peptides and proteins than the unfiltered data at unchanged precision." They then state: "The sweep was a selection aid rather than an objective to maximize benchmark coverage. We chose gap 2 and length 5 to prioritize stricter local continuity and greater point removal over maximizing coverage on the selection sample."

This is a critical transparency failure. The authors do not report the full grid-sweep results (Table S2 is referenced but not shown in the main text or Supporting Information as provided). The phrase "prioritize stricter local continuity and greater point removal" is vague—it does not specify which cells of the grid were considered, which had higher coverage, or why the chosen cell represents a defensible tradeoff rather than an arbitrary choice. The statement that "the 15-minute ddaPASEF results are not fully out-of-sample" acknowledges the circularity but does not resolve it. Without seeing the full sweep table and the authors' explicit reasoning for rejecting other parameter combinations, a reader cannot determine whether the defaults were selected to optimize the benchmark results post-hoc or whether they represent a principled choice that would generalize. This is a HARD reproducibility issue: the parameter selection process cannot be independently verified or critiqued because the decision rationale is not documented.

**Claim 3: The benchmark is representative enough that results generalize to typical timsTOF proteomics workflows.**

The evidence is Section 2.5 and the limitations discussion (Section 3.7). The authors tested one instrument (timsTOF Ultra 2), one laboratory, one sample type (three-species standard), two gradients (5 and 15 minutes), and two acquisition modes (ddaPASEF and diaPASEF). Section 3.7 explicitly acknowledges: "The replicated benchmark remains controlled and narrow" and "Validation across laboratories, sample loads, and sparse acquisitions remains necessary."

This is honest but creates a tension with the paper's framing. The abstract and introduction present dnoise as a general solution to a widespread problem ("high-throughput proteomics," "every tested processing run"), and the results are stated without qualification (e.g., "default MS1-only denoising reduced the frame binary by 35 to 53%"). A reader might reasonably infer these numbers apply broadly. The limitations section correctly flags that they do not, but the paper does not clearly distinguish between what is demonstrated (one instrument, one lab, one sample type) and what is claimed (applicability to timsTOF proteomics generally). The confound between ddaPASEF on-instrument denoising being enabled and diaPASEF being disabled (acknowledged in Section 3.7) further complicates interpretation of the mode-specific reduction figures. The paper would be stronger if it reframed the results as "on this instrument and sample type" rather than as general timsTOF results, or if it included data from a second instrument or sample type to support generalization.

## Strengths

1. **Complete software release with version control and archival:** dnoise is published on crates.io, tagged on GitHub, and archived at Zenodo (doi.org/10.5281/zenodo.21959649), allowing exact reproduction of the reported results.

2. **Full parameter specification and native-format compatibility verification:** Table S1 lists all defaults; Section 2.4 documents the read/write round-trip validation (point-for-point identical decoding with timsrust), and the authors provide Sage and DIA-NN configurations in Section S7.

3. **Transparent handling of optional MS/MS filtering and its tradeoffs:** The authors clearly separate the default MS1-only mode from optional MS/MS denoising, explain why the latter changes identifications (Section 3.3, Figure S6), and recommend against it, rather than presenting it as a neutral option.

## Weaknesses

**Load-bearing:**

1. **Parameter-selection process is not fully documented.** The grid-sweep results (Table S2) are referenced but not provided in the text or Supporting Information excerpt. The authors state they "chose gap 2 and length 5 to prioritize stricter local continuity and greater point removal" but do not report which other parameter combinations were evaluated, what their coverage/precision tradeoffs were, or why the chosen cell was selected over alternatives. Without this information, the objectivity of the parameter choice cannot be verified, and the risk of post-hoc optimization to the benchmark cannot be ruled out. Providing the full grid-sweep table with all tested combinations and their quantification outcomes would resolve this.

2. **Quantified protein-set changes under MS1-only filtering are not clearly reported.** Table S5 shows small changes in quantified protein counts between original and MS1-only arms (e.g., 2,847 vs. 2,851 at 5-minute ddaPASEF), but the paper does not explain whether these are due to proteins crossing reporting thresholds, measurement noise, or other causes. The claim that "quantification is preserved" is ambiguous when the set of quantified proteins shifts. Reporting the overlap of quantified proteins between original and denoised arms, and the distribution of proteins that enter or exit the quantified set, would clarify whether the preservation claim is accurate.

3. **Benchmark scope is narrow and confounded, but generalizability is not clearly qualified in main claims.** One instrument, one lab, one sample type, and on-instrument denoising enabled only for ddaPASEF create a limited and confounded test. The abstract and introduction present results as general timsTOF findings without qualification, while limitations are relegated to Section 3.7. Reframing headline results as instrument- and sample-specific, or adding data from a second instrument/sample type, would better align claims with evidence.

**Sweep:**

4. The matched intensity-threshold control (Section 3.4, Figure S5) is valuable but uses a per-acquisition calibration rather than a single global threshold; it is unclear whether this introduces bias in favor of the streak filter or whether the comparison is fair.

5. The halo filter's parameter (halo_peak_fraction = 0.15) is not justified by any ablation or sweep; its contribution to the final result is small (Table S4) but its optimality is not demonstrated.

6. DIA-NN's MaxLFQ quantification is derived from fragment chromatograms, so MS1-only denoising should not affect it directly; the authors note this (Section 3.2) but do not explain why they report MS1-level accuracy (Table S12) as a validation metric for a tool that does not use MS1 for quantification in that workflow.

7. The centroiding modes (Section 3.5, Section S6) are presented as optional but are not integrated into the main benchmark; their interaction with the default filters and their parameter choices (watershed vs. box) are not fully characterized.

8. Runtime and memory measurements (Figure 6, Table S16) are on a single workstation; scaling behavior on larger datasets or lower-spec hardware is not reported.

## Questions

- Can the authors provide the full grid-sweep results from Table S2, including all tested (min_feature_length, max_internal_gap) pairs, their quantification outcomes, and the explicit decision rule used to select the final defaults?

- For the MS1-only denoising arm, what fraction of quantified proteins are shared with the original arm, and how many proteins enter or exit the quantified set due to crossing the two-peptide or two-replicate thresholds?

- Why is the matched intensity-threshold control (Section 3.4) calibrated per-acquisition rather than using a single global threshold, and does this choice affect the fairness of the comparison?