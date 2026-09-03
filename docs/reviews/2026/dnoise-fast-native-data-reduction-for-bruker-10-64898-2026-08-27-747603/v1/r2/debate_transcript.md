# Debate Transcript

## Advocate — round 1

I'll make the case for acceptance of dnoise as a sound, useful contribution to In Silico.

**A genuine, well-scoped contribution.** Every specialist agrees the core engineering claim holds: no prior open-source tool writes denoised data back to native Bruker .d format. The contribution_context reviewer confirmed this against the literature (Wilding-McBride exports MGF/features, PNNL PreProcessor doesn't support Bruker), finding "no contradicting published or preprint work." This is a real gap the paper fills, not an overstated one.

**The central quantitative claim is well-supported for its stated scope.** Default MS1-only denoising leaves ddaPASEF PSM/peptide/protein counts *identical* (Figure 2, Table S5) — an expected but verified result, since MS/MS spectra are untouched. The scientific_validity reviewer calls this "well-executed" with "appropriate" controls, and independently notes the mechanism is transparent: MS1 filtering cannot alter fragment-based identification. For diaPASEF, precursor/protein changes of 0.2–2.2% alongside unchanged CV and accuracy (Figures 3–4) support preservation of the analytical result, not just non-degradation.

**The authors' candor is itself a strength, not merely a mitigated weakness.** They explicitly flag that the 15-minute ddaPASEF parameter-selection sample is "not fully out-of-sample" (lines 107–109), that on-instrument denoising confounds the DDA/DIA reduction comparison (lines 174–175), and that the benchmark is narrow (Section 3.7, "Limitations"). Every reviewer credits this transparency; the reporting_reproducibility reviewer calls it something the authors "flag" rather than hide. A paper that states its own limits in a dedicated section should be rewarded for candor per the venue's own stated criteria.

**The streak-filter-vs-threshold control is a genuine mechanistic strength.** The decoy-to-target loss ratio inversion (1.77–2.34 vs. 0.43–0.57, Figure S6) is a concrete, checkable falsification test the authors ran against their own method — exactly the kind of self-skeptical control that should count in favor of trustworthiness, even if its full stringency-matching isn't documented.

**Reproducibility is exemplary**: versioned Zenodo release, public raw data, complete parameters (Table S1) — unanimously confirmed by the ethics and reproducibility reviewers.

The identified gaps (parameter robustness, single instrument/sample) are revision-scoped clarifications of claim boundaries, not defects in the evidence presented.

## Skeptic — round 1

**Lead objection (FIXABLE, but currently misrepresented in the headline claims): the benchmark's four "combinations" are not evidentially equal, and the abstract does not say so.**

Section 2.2 states the streak-filter parameters (min_feature_length, max_internal_gap) were selected by a grid sweep "scored on quantified coverage, replicate precision, and intensity fidelity" on the *same* 15-minute ddaPASEF Condition A that later appears as validation evidence in Figure 3/Table S5. The authors disclose this ("not fully out-of-sample," lines 107–109), but the Abstract and Conclusion state the pooled result — "default MS1-only denoising reduced the frame binary by 35 to 53%" and "LFQ accuracy was preserved in both modes" — without disaggregating the one arm that was optimized on the metrics it is later used to demonstrate. That is circular for that cell of the design, and a reader skimming the headline has no way to know one-quarter of the evidence is in-sample.

**Second (FIXABLE, disclosed but not quantified): the DDA-vs-DIA reduction contrast is confounded by unequal instrument settings.** The authors state Bruker's on-instrument denoising was enabled for ddaPASEF but not diaPASEF (lines 174–175), yet Figure 2's side-by-side percentages (81.2% vs. 93.5% MS1 points removed) are presented as a acquisition-mode comparison. The magnitude of this confound is never estimated.

**Third (FIXABLE): scope overreach.** The Conclusion's "a substantial fraction of native timsTOF frame data can be removed" generalizes from one instrument, one 50 ng three-species mixture, and two short gradients — a narrower base than the sentence implies.

**Panel blind spot:** no reviewer executed the code or inspected the cited S-tables/figures (S1, S2, S4–S16) directly; confidence in secondary claims (ablations, centroiding, threshold-matching) rests on trust in unseen supplementary material.

## Advocate — round 2

The skeptic's points are real, but each is exactly what the venue instructs reviewers to reward, not punish: the authors flagged all three limitations themselves, in the text the skeptic quotes.

**On circularity**: the skeptic is right that one arm (15-min ddaPASEF Condition A) fed the parameter sweep. But the sweep, per Section 2.2, was "a selection aid rather than an objective to maximize benchmark coverage," and three of the four tested combinations — 5-min ddaPASEF and both diaPASEF gradients — are genuinely out-of-sample, as the authors state directly: "The 5-minute gradient and both diaPASEF acquisitions played no role in parameter selection." That the pooled Abstract sentence doesn't disaggregate this is a wording fix, not a design flaw — a revision can simply add "(one arm partially in-sample; see Section 2.2)" to the headline claim. It does not require new data, and the underlying result — identical ddaPASEF PSM/peptide/protein counts — holds mechanically regardless of parameter tuning, since MS1 filtering cannot touch untouched MS/MS spectra.

**On the DDA/DIA confound**: again, self-disclosed at lines 174–175, and the manuscript explicitly warns against the misreading the skeptic worries about: "This difference should not be interpreted as an inherent advantage of one acquisition mode." That sentence exists precisely to prevent the overreach being alleged.

**On scope wording**: the Limitations section (3.7) already narrows the claim to "one timsTOF Ultra 2 instrument, one laboratory, one 50 ng three-species sample." Tightening the Conclusion's phrasing to match is a one-sentence edit.

None of this is evidence the central claim is wrong — only that two sentences need scoping language the paper's own limitations section already supplies.

## Skeptic — round 2

**Lead objection (FIXABLE): the diaPASEF quantification claim leans on a metric that structurally cannot detect what MS1 denoising might break.** The advocate is right that ddaPASEF's identical PSM/peptide/protein counts are a trivial but honestly-reported non-result. But the diaPASEF "LFQ accuracy preserved" claim needs to carry more weight, and the data_analysis reviewer already flagged why it can't: DIA-NN's MaxLFQ is derived from fragment chromatograms, so "the default MS1-only filter does not directly alter the signal used for quantification" (manuscript's own words, Section 3.2). The one metric that *could* be sensitive — the direct Ms1.Normalised check in Table S12 — is called "reassuring but indirect" by the contribution reviewer and is not brought into the main text with the same bootstrap-CI rigor applied elsewhere (Tables S10/S11). Concede: this doesn't invalidate the claim, but the headline "LFQ accuracy was preserved in both modes" implies symmetric evidentiary strength across modes that the panel's own reports show does not exist.

**Second, unresolved rather than merely undocumented (FIXABLE):** the advocate calls the decoy-ratio inversion (1.77–2.34 vs 0.43–0.57) a self-skeptical strength. The scientific_validity reviewer's alternative explanation — that decoy enrichment reflects general spectral sparsity rather than streak-specific logic — was raised but never tested by any specialist or by the manuscript itself. That's a genuine open mechanistic question, not resolved by candor.

**Blind spot, unchanged:** no reviewer opened S1–S16 directly; several "complete values" claims rest on unverified supplementary material.

None of this is fatal. It argues for disaggregating claims by mode and adding the missing stringency/CI detail in revision.