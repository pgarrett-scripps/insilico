# Decision Letter

VERDICT: minor

**Publication readiness:** 80/100

## Readiness Breakdown
- Scientific validity: 28/35
- Methods and evidence: 19/25
- Reproducibility and reporting: 16/20
- Clarity and completeness: 17/20

## Contribution Profile
- Novelty: moderate
- Significance: moderate
- Usefulness: high

## Score and Decision
The central claim — that default MS1-only denoising removes a large fraction of native timsTOF frame data (35–53% of the frame binary) while leaving the tested proteomics results essentially unchanged — is supported by the evidence presented. For ddaPASEF it is close to mechanically guaranteed (the searched MS/MS spectra are untouched, and identification counts are identical), and the quantitative validation on a defined three-species mixture with known ratios, replicated six times per condition across two gradients and two acquisition modes, is a disciplined test of the part of the claim that could have failed. Runtime and memory claims are descriptive measurements on stated hardware and are correctly reported as such. The software is released under MIT with a versioned Zenodo archive, the raw data are public, and the round-trip fidelity check (point-for-point identity of an unfiltered pass) is exactly the control a reader wants to see for a tool that rewrites a proprietary binary.

What lowers readiness is not the validity of the core result but the calibration of its presentation and several reporting gaps. The two geometric streak-filter parameters were selected on Condition A of the 15-minute ddaPASEF gradient, which then reappears inside the pooled headline result; the authors disclose this in Section 2.2 but the Abstract and Conclusion present a single pooled figure across all four arms without the qualifier. Related, the phrase "LFQ accuracy was preserved in both modes" implies symmetric evidentiary strength, whereas the diaPASEF case rests on a metric (fragment-based MaxLFQ) that MS1-only filtering does not directly touch, with the one MS1-sensitive check (Table S12) reported without the bootstrap treatment applied elsewhere. The DDA/DIA reduction differential is confounded by on-instrument denoising, which the manuscript warns against misreading but does not bound. Finally, the compliance audit identifies genuine gaps: search FDR thresholds are never stated, the analysis and figure-generation scripts are described but not deposited, the optional-mode `msms_*` parameters and centroider algorithms are underspecified, and two references have anomalous dates or DOIs.

Every one of these is fixable in text, tables, and deposited files. None requires a new acquisition, a new search, or a reanalysis whose outcome could overturn a conclusion. Where I would otherwise have asked for new work — a second sample type, a fair-stringency fragment control, a mechanistic test of the decoy-ratio inversion — the correct remedy at this venue is to scale the claim to the evidence rather than to demand the experiment, and I have routed those to suggestions and to a requalification requirement accordingly. That places this at minor revision. The score reflects a sound, useful, honestly reported tool paper whose current text overreaches its four benchmark arms in a few specific sentences and whose reproducibility record has repairable holes.

## Required Revisions

1. **Disaggregate the partially in-sample arm in the headline claims.** In the Abstract, Section 3.1/3.2, and the Conclusion, state explicitly that the streak-filter geometric parameters were selected on Condition A of the 15-minute ddaPASEF gradient and that this arm is therefore not fully out-of-sample. Either report the 15-minute ddaPASEF reduction and quantification results separately from the three out-of-sample arms, or attach the qualifier at the point where the pooled 35–53% range and the "preserved" language first appear. The disclosure in Section 2.2 is not sufficient on its own, because a reader of the Abstract cannot see which quarter of the evidence is affected.

2. **Requalify the diaPASEF LFQ-preservation claim to match its evidentiary basis.** The manuscript already notes that DIA-NN's reported MaxLFQ quantity derives from fragment chromatograms and is therefore not directly altered by MS1-only filtering. Say so where the claim is made, not only in the follow-up sentence: distinguish "unchanged because the quantified signal was not modified" (diaPASEF MaxLFQ) from "unchanged despite the quantified signal being modified" (ddaPASEF MS1 LFQ). Apply the same percentile-bootstrap CI treatment used in Tables S10/S11 to the Table S12 MS1-normalised check, or state plainly that this check is descriptive and uncorrected.

3. **State the FDR thresholds actually applied.** Report the PSM-level and peptide-level FDR (or q-value) cutoffs used for the Sage searches and the precursor- and protein-level q-value cutoffs used for DIA-NN, and clarify whether the 1% LFQ q-value mentioned in Section 3.3 is applied at search time or post hoc. This is load-bearing: every reported identification and quantified count depends on it.

4. **Deposit the analysis and figure-generation scripts.** The Acknowledgment states these scripts computed every reported value and figure. Add them to the GitHub repository and the Zenodo archive (or a second archived record), and cite the location in the Data Availability Statement. Without them, Figures 2–6 and Tables S5–S16 cannot be regenerated from the deposited raw data.

5. **Fully specify the optional modes.** (a) List the `msms_*` parameter values used for the MS1+MS/MS arm alongside the MS1 defaults in Table S1. (b) For both centroiders, give the box size, the transitivity/grouping rule, and the intensity-weighted centroid formula. (c) State whether Sage and DIA-NN successfully read the centroided `.d` directories, since the native-compatibility claim is the paper's main selling point and Section 3.5 currently reports label-free results without confirming this.

6. **Temper the unqualified generalization in the Conclusion and Abstract.** "A substantial fraction of native timsTOF frame data can be removed with little analytical change" should carry the scope already given in Section 3.7: one timsTOF Ultra 2, one laboratory, one 50 ng three-species standard, two gradients, two acquisition modes. Section 3.7 is candid; the summary sentences should not be broader than it.

7. **Bound or explicitly disclaim the DDA/DIA reduction differential.** The on-instrument MS1 denoising confound is already flagged. Either give a rough estimate of its contribution (for example, the MS1 point density per frame in the two acquisitions before dnoise, which you have) or state in the Figure 2 caption that the two modes' reduction percentages are not comparable and should not be read as a mode effect.

8. **Report the removal-matching basis for the intensity-threshold control on fragment frames.** Section 3.4 states the threshold was calibrated to match MS1 removal, then extends both filters to fragment frames and compares decoy-to-target loss ratios. Report the fraction of *fragment* points removed by each filter in that comparison. If they differ materially, say so and qualify the conclusion as stringency-confounded rather than a clean filter-design comparison. Also note in the text that the threshold was calibrated per acquisition while the streak filter was held fixed, and say whether the optimal cutoff differed across acquisitions.

9. **Correct the two citation anomalies.** Reference 4 (Houthuijs et al.) carries a 2026 date matching the manuscript date — confirm the year or the in-press/preprint status. Reference 19 has a non-standard DOI prefix (10.64898/2026.01.29.702266); verify or replace it. Reference 18 (10.6019/PXD070049) appears to be the valid primary deposition.

10. **Add the small procedural details needed to reproduce the numbers as stated.** The m/z and mobility padding values used for the benchmark's precursor-selection gate (referenced in the Figure 1 caption but not given numerically in the main text); whether the halo filter is on or off in the default configuration and how to disable it; the pooling method for the "median pooled protein CV"; the number of shared contributing proteins entering each bootstrap; the operating system used for the timing and memory measurements; and whether the six replicates per condition are independent preparations or repeated injections.

## Minor Suggestions

- A brief note on the Bruker type-2 `analysis.tdf_bin` encoding — how the encoder was validated beyond the round-trip test, and whether any public or reverse-engineered specification was used — would strengthen the native-compatibility claim without requiring proprietary disclosure.
- The decoy-to-target loss ratio argument (Section 3.4) would be more convincing with a bootstrap CI on the ratio, and the alternative explanation raised in review — that decoy enrichment may follow from removing sparse spectra generally rather than from mobility-coherence specifically — deserves a sentence acknowledging it. A comparison of the decoy-to-target ratio under the matched threshold applied to fragment frames would test it directly if the numbers already exist.
- Justify or flag the choice to leave both intensity floors at zero as a deliberate design decision, since it is the parameter setting that makes the filter purely geometric.
- Section 3.5 (centroiding) currently reads as an appendix inserted into the Results. A one-sentence statement of the intended use case (precursor-level quantification at reduced mobility resolution) at the top of the section would orient the reader better.
- Guidance on when the MS1+MS/MS mode is an acceptable trade — for example, archival of runs already searched, versus primary storage of runs that may be re-searched — would make that section more actionable.
- A single runtime measurement on a lower-core-count machine would let readers judge whether the "fast enough for routine use" claim survives on typical facility hardware; the current claim is true as measured but hardware-specific.
- Independent validation of the halo filter's effect on identifications, and any sensitivity analysis across load or sample complexity, would be valuable future work rather than a requirement here, given the honest scoping in Section 3.7.

We look forward to receiving the revised manuscript. The work is a genuinely useful addition to the timsTOF toolchain, and the revisions above are aimed at making the claims exactly as strong as the benchmark supports — no more and no less.