# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall assessment

This is a competent empirical study comparing training objectives for machine-learned weather forecasting, with sound experimental design and honest reporting of limitations. The statistical analysis is appropriate to the claims made, though modest in scope. The work makes a useful incremental contribution — demonstrating that multivariate scoring rules can match CRPS-based training — but the evidence for this claim is narrower than presented, and the spectral analysis, while informative, does not isolate the mechanisms driving the observed differences. The paper is suitable for publication with minor revision.

## Strengths

1. The authors transparently acknowledge computational constraints and the reduced-scale nature of their experiments (section 5), avoiding overclaim of generality.

2. Multiple loss formulations are tested under identical architecture and data conditions, making the comparison of training objectives fair and interpretable.

3. Spectral analysis of accumulated tendencies provides a useful diagnostic of scale-dependent forecast realism beyond standard verification metrics.

## Load-bearing weaknesses

**Claim 1: Multivariate scores match CRPS-based training in forecast skill.**

The evidence is Figure 2, which shows CRPS, energy score, and graph energy score experiments. The comparison is visual; no statistical test is reported. The authors state "forecast skill is broadly similar" and note "small differences" in the extratropics, but do not quantify what constitutes similarity or report confidence intervals, standard errors, or a formal equivalence test. The sample is 84 initialization dates (stated in section 4.2). For a claim of equivalence, the absence of a pre-specified non-inferiority margin and a corresponding test is a HARD gap. The tropical region shows visible separation (graph energy best, global energy degraded), but no p-value, effect size, or test statistic is given. The statement "consistent when the fair energy score or fair graph energy score is used for verification" is mentioned but those results are not shown. Without reporting the actual CRPS values, their ranges, or a statistical test, the reader cannot distinguish whether the visual similarity reflects genuine equivalence or simply reflects the resolution of the figure. What would resolve this: report mean CRPS and 95% CI for each experiment and region, and state the equivalence margin (in CRPS units) that would support the claim of "broadly similar" skill.

**Claim 2: Scale-aware losses substantially improve small-scale variability.**

The evidence is Figures 3–14, which show accumulated tendency spectra and ratios. These are visual comparisons without statistical testing. The authors state "scale awareness alone does not guarantee realistic variability at all scales" and note "differences between scale-aware loss objectives are comparatively small," but do not quantify these differences or test whether they are significant. The spectra are computed from 84 forecasts; the variability across initialization dates is not shown (no error bars, confidence bands, or bootstrap intervals). The claim that "edge-CRPS experiment and the spectral magnitude CRPS experiment seem to be slightly more successful" uses the word "seem," signalling uncertainty, but no test is offered to support or refute it. The authors also note that "achieving realistic spectra for geopotential appears more challenging," but do not test whether the differences between experiments are consistent across variables or whether they reflect noise in the spectral estimate. What would resolve this: report the spectrum for each experiment with 95% confidence bands (e.g., from block bootstrap over initialization dates), and state which experiments differ significantly at which scales using a formal test (e.g., pointwise t-test with Bonferroni correction over wavenumber bands).

**Claim 3: Weighting factors matter as much as the choice of multivariate score.**

The authors state in section 5: "The weighting of different fields, scales, and variables can matter as much as, or more than, the specific mechanism that is used to inject spatial awareness into the loss." This is inferred from comparing spectral experiments with and without weighting (Figures 3, 5). However, the weighting factors are described as "ad hoc and were chosen only to be of the right order of magnitude — estimated from the data — rather than tuned." This is a critical limitation: if the weights were not systematically optimized, the comparison between weighted and unweighted experiments does not isolate the effect of weighting from the effect of arbitrary choices in weight magnitude. The claim would be stronger if the authors had either (a) reported the actual weight values and their sensitivity, or (b) tested a range of weight values to show that the conclusion holds across reasonable choices. As stated, the evidence supports "weighting can affect spectra" but not "weighting matters more than the score choice" because the weight choices were not controlled. What would resolve this: report the actual weight values used, and show spectra for at least one alternative weighting scheme to demonstrate robustness of the conclusion.

## Sweep

1. **Multiple comparisons:** Twelve experiments are compared in section 3.2 (Table 2), but no multiple-comparison correction is applied to any visual or statistical inference; the authors do not pre-register the experiments or state a primary hypothesis, so the family-wise error rate is uncontrolled.

2. **Sample size for spectral analysis:** The 84 initialization dates are stated, but the effective sample size for spectral estimates is not discussed; spectral estimates from adjacent wavenumbers are correlated, and the degrees of freedom are not reported.

3. **Hyperparameter tuning:** The graph connectivity (k=16 nearest neighbours) and smoothing kernel widths (100, 200, 400, 800 km) are stated but not justified; no ablation or sensitivity analysis is provided.

4. **Baseline comparison:** The paper does not compare against a simple baseline (e.g., climatology or persistence) to establish that all trained models are actually skillful; the CRPS values themselves are not reported.

5. **Spectral magnitude CRPS:** The authors state this score "constrains the distribution of spectral amplitudes, but does not penalize phase errors," but do not test whether phase errors are actually larger in this experiment or whether they matter for forecast skill.

6. **Ensemble size:** All experiments use 8-member ensembles; the sensitivity of results to ensemble size is not explored, despite ensemble size being a known source of bias in fair scoring rules.

7. **Generalization:** The authors acknowledge "experiments were conducted with smaller models, relatively low spatial resolution, and a shortened training schedule" but do not quantify how much smaller or shorter; the claim that "greater model capacity and longer training may improve the performance of losses without scale awareness" is speculative and untested.

8. **Figure quality:** Figures 3–14 are difficult to read; the line styles and colors are not clearly distinguished, and the legends are small; a table of spectral ratios at key wavenumbers would be more interpretable.

## Questions

- In Figure 2, what are the actual CRPS values (not just the skill anomaly) for each experiment and region, and what is the standard error across the 84 initialization dates?
- For the spectral analysis, were the spectra computed separately for each initialization date and then averaged, or were all 84 forecasts pooled before computing the spectrum? If pooled, what is the effective sample size (accounting for spectral correlation)?
- The global energy score experiment shows degradation in the tropics (Figure 2); is this degradation statistically significant, and does it persist if the experiment is re-run with different random seeds?