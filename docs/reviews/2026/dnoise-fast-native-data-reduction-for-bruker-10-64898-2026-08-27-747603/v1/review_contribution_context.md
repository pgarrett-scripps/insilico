# Contribution & Prior-Work Reviewer

Based on my searches, I have gathered sufficient information about the prior work landscape. Let me now compile my review.

---

SCORE: 4
CONFIDENCE: 4

## Summary

dnoise is a practical engineering contribution that fills a real operational gap: removing uninformative points from native Bruker timsTOF .d files while preserving the native format for downstream analysis. The manuscript is well-executed within its scope, with honest reporting of limitations and a clear experimental design. The contribution is real and useful but narrowly scoped—it is a specialized tool for a specific instrument format and acquisition mode, not a methodological advance. The work is sound and the claims are supported by the evidence presented.

## Strengths

1. **Honest scope and limitations**: The authors clearly state that their benchmark is "controlled and narrow" (one instrument, one lab, one sample type, two gradients), explicitly flag that on-instrument denoising was enabled only for ddaPASEF (confounding the DDA/DIA comparison), and recommend retaining originals for future analyses—this candor is rare and valuable.

2. **Native-format compatibility verified**: The authors demonstrate point-for-point identity on unfiltered read/write round-trips and validate that denoised .d directories work with existing downstream tools (Sage, DIA-NN), removing a major barrier to adoption that would exist if the output required conversion.

3. **Quantitative fidelity tested across two independent search pipelines**: Label-free quantification accuracy and precision are validated in both ddaPASEF (Sage + IonQuant) and diaPASEF (DIA-NN MaxLFQ) on a defined three-species benchmark with known ratios, and feature-level intensities are shown to track the original across replicates.

## Weaknesses: Load-Bearing Claims

**1. Claim: "No open-source tool removes points and writes the result as a new native-compatible Bruker .d directory."**

The manuscript positions dnoise as filling a unique gap: existing approaches either convert to mzML (losing native format), apply general compression (preserving uninformative points), or export to MGF/feature lists (not native .d). The Wilding-McBride et al. (2022) work on spectral simplification is cited as exporting MGF or feature lists rather than native .d, and the PNNL PreProcessor (Bilbao et al. 2022, reference 7) is stated not to support Bruker .d. I verified that Wilding-McBride does indeed export MGF and feature lists, not native .d. However, the manuscript does not explicitly state whether the PNNL PreProcessor *could* support Bruker .d or whether it is architecturally incompatible. The claim as stated appears accurate based on the cited evidence, but the boundary between "does not support" and "cannot support" is not established. This is a soft issue: the novelty claim holds if the PNNL tool is indeed limited to other platforms, but the manuscript does not provide enough detail to verify that independently.

**2. Claim: "Default MS1-only denoising reduced the frame binary by 35 to 53% while preserving LFQ accuracy in both modes."**

The evidence supports this for ddaPASEF (PSM/peptide/protein counts identical, LFQ accuracy and precision unchanged across all species and condition pairs). For diaPASEF, the claim is more qualified: precursor and protein-group counts changed by 0.2–2.2% and 0.2–1.6% respectively, and the authors note that DIA-NN derives MaxLFQ from fragment chromatograms, so MS1 filtering does not directly alter the quantification signal. The direct precursor MS1-area field showed ratios moving *toward* expected values after denoising (Table S12). This is consistent with the claim, but the diaPASEF result is less clean than ddaPASEF: a small identification cost is present, and the authors do not fully explain why MS1 denoising should improve direct precursor ratios if the removed points are truly uninformative. One possibility is that the removed points introduce noise that biases the area integration; another is that the benchmark's on-instrument denoising for ddaPASEF but not diaPASEF creates an asymmetry in what dnoise encounters. The authors acknowledge the confound but do not resolve it. The quantification preservation claim is supported, but the mechanism is not fully transparent for diaPASEF.

**3. Claim: "The streak filter better preserves weak signal than a matched intensity threshold."**

The control experiment compares the streak filter to a per-point intensity threshold calibrated to remove approximately the same fraction of points. The streak filter outperformed the threshold on weak peptides (Figure S5), and when extended to fragment frames, the threshold lost more quantified coverage, especially in diaPASEF (Figure S4). The authors attribute this to the threshold removing unidentifiable spectra (rank-1 decoys) faster than real identifications. However, the comparison is not orthogonal: the threshold was calibrated to match *overall* removal, not removal *per frame or per feature*. A threshold that removes 50% of points globally may remove 70% from weak features and 30% from strong ones, whereas the streak filter removes based on mobility structure. The control therefore shows that mobility-aware filtering outperforms a naive intensity cutoff, but it does not isolate whether the advantage comes from the mobility criterion itself or from the fact that the threshold was poorly calibrated for the task. A better control would be a mobility-aware threshold (e.g., "remove points below intensity X *within each mobility scan*"), which would separate the benefit of mobility awareness from the benefit of not using a global cutoff. The evidence supports that the streak filter works well, but does not fully isolate why it works better than the alternative tested.

## Weaknesses: Sweep

- The benchmark uses only one instrument (timsTOF Ultra 2) and one sample type (three-species digest); generalization to other timsTOF models, complex samples, or sparse data (e.g., single-cell) is explicitly flagged as unvalidated but remains a real limitation for users considering adoption.

- Parameter selection (min_feature_length=5, max_internal_gap=2) was optimized on the 15-minute ddaPASEF condition (part of the benchmark), making those results not fully out-of-sample; the authors acknowledge this but do not report how sensitive the results are to parameter choice across the other three acquisition/gradient combinations.

- The optional MS/MS denoising trades 7–12% of peptide identifications for 70–74% frame reduction; the authors recommend MS1-only as default, but do not provide guidance on when the MS/MS mode would be justified or how to tune the relaxed msms_* parameters for different sample types.

- The halo filter (removing weak halos around intense peaks) is described as a "small final trim" but is not independently validated; its contribution to the overall reduction and its potential to remove weak co-eluting ions are mentioned but not quantified.

- Runtime (7–69 seconds) is fast enough for post-acquisition use, but the manuscript does not compare to the time cost of converting to mzML or running other preprocessing pipelines, so the practical advantage is not contextualized.

- The manuscript does not discuss how dnoise handles edge cases: missing or malformed analysis.tdf entries, frames with no surviving points, or runs where the precursor-selection polygon is absent (though gates are stated to "silently do nothing" in such cases).

## Questions

- Table S2 reports the parameter sweep on Condition A (15-minute ddaPASEF); what are the quantification and precision results for the other parameter combinations (gap 1, 3, 4; length 3, 4, 6, 7) on the same sample, to assess robustness?

- For diaPASEF, why do the direct precursor MS1-area ratios move toward expected values after MS1 denoising (Table S12) if the removed points are uninformative noise? Is this consistent with the removal of weak co-eluting background, or does it suggest the filter is removing signal?

- Section S4 mentions "representative frames and parameter sweeps" for MS/MS filtering; what are the msms_min_feature_length and msms_max_internal_gap defaults, and how were they chosen?

---

## Overall Assessment from Contribution & Prior-Work Specialty

The manuscript makes a genuine and useful contribution: a fast, open-source tool that reduces timsTOF file size by 35–53% while preserving quantification and identification in the tested workflows. The prior-work landscape supports the novelty claim—Wilding-McBride exports to MGF, the PNNL PreProcessor does not support Bruker, and existing tools either convert formats or preserve uninformative points. The work is narrowly scoped (one instrument, one sample type, two gradients) and the authors are transparent about this. The experimental design is sound, the controls are appropriate, and the claims are supported by the evidence, though the mechanism of MS1 denoising in diaPASEF and the advantage of the streak filter over alternatives could be more fully explained. This is solid, useful engineering work that will be valuable to the timsTOF community, but it is not a methodological advance and does not claim to be one.