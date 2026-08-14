# Statistics & Data-Analysis Reviewer

## Summary
This is a hypothesis-generating discovery study with a defensible design (DIA-MS on CSF from a well-established CIE-2BC mouse model) but a statistical framework that does not support the strength of the claims made. The central findings — 140 "Dep-specific" vs 67 "Non-dep-specific" proteins — rest entirely on detection-rate differences with no statistical test applied, an arbitrary detection threshold with no sensitivity analysis, and an unverified assumption that missing values mean "below limit of detection." The contamination question (keratins, hemoglobin concentrated in the Dep group) is acknowledged but not resolved with a measured metric. The work has genuine value as a hypothesis-generating resource, but the conclusions outrun the evidence as presented.

## Strengths
- Defensible design: DIA-MS on CSF from a well-established CIE-2BC mouse model.
- The work has genuine value as a hypothesis-generating resource.

## Weaknesses
- The central detection-rate comparisons are never tested statistically: no test is applied to any detection-rate difference (e.g., MMP2 at 4/4 Dep vs 0/5 Non-dep, GFAP at 3/4 vs 0/5, or the 140-vs-67 protein counts). A Fisher's exact test on the MMP2 table gives p = 0.0079 (two-sided); with ~600 proteins screened, even a single uncorrected comparison at this level is marginal, and none would survive any reasonable multiple-testing correction.
- The 'Strong'/'Moderate' evidence classification in Tables 1–2 is an arbitrary detection-rate threshold, not a statistical result; the claim that 140 proteins are 'Dep-specific' is a descriptive observation, not a tested finding.
- The detection threshold is arbitrary and the headline counts are threshold-dependent: the 140 vs 67 counts depend on the ≥2-replicate detection rule, and the asymmetry between the Dep criterion (≥3/4 = 75%) and Non-dep criterion (≥4/5 = 80%) means the two counts are not directly comparable.
- No sensitivity analysis is reported — the counts at ≥1 replicate, or at ≥3 replicates, would likely change substantially, and the manuscript does not show that the biological interpretation survives threshold variation.
- The 'top 10' selection for Figure 2 is undefined as a criterion.
- Missing values are assumed to be 'below limit of detection' without verification: no spike-in controls, no technical replicates, no QC metrics (e.g., coefficient of variation across replicates, ion injection time distributions) support the MNAR assumption; in DIA-MS, missing values arise from ion suppression, co-elution, and technical variability as well as true absence.
- The contamination question is not resolved for the specific claim it threatens: keratins (K2C5, K1C10, K2C1B) and hemoglobin are concentrated in the Dep group, and the cited methodological defense addresses whether these proteins can appear in clean CSF, not whether differential contamination occurred between groups; if BBB disruption makes CSF collection more difficult in Dep mice, the contamination signature would concentrate exactly where the manuscript reports it, and the 'BBB disruption' claim would be partly an artifact of the collection process.
- Post-hoc power analysis is circular — it uses observed detection rates to claim the study was underpowered, which is always true for non-significant results; report confidence intervals for detection rates instead.
- The 404 shared proteins are never compared quantitatively, despite DIA providing quantitative peak areas — a missed opportunity and a partial control for the presence/absence framework.
- Enrichment analyses (EnrichR, STRING, KEGG) inherit the arbitrary detection threshold and are not corrected for the hundreds of pathways/terms tested.
- Sex is a potential confound: PCA shows Non-dep separates by sex along PC2 but Dep does not — with n=2 per sex in the Dep group, this could be a power artifact rather than a biological signal.
- The IL-6R antibody treatment is a confound for all comparisons; the claim that it 'did not ameliorate' Dep effects is unsupported by any data shown (no vehicle control is reported).
- The single-peptide identification of the IL-6R antibody (DILLISQNAK) is weak evidence; the manuscript discloses this but should flag it as a limitation rather than presenting it as confirmation.

## Questions
- What are the 140-vs-67 protein counts at detection thresholds of ≥1 and ≥3 replicates, and does the biological interpretation survive?
- What is the per-sample hemoglobin concentration (or equivalent contamination metric), and does it correlate with the Dep-specific protein detection pattern?
- Were any technical replicates or QC metrics (e.g., peptide CVs, injection time distributions) collected to support the MNAR assumption for missing values?
- What is the sex breakdown of the 140 Dep-specific proteins — are any driven predominantly by one sex?