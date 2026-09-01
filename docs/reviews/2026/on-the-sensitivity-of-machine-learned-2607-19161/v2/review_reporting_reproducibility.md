# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript compares training objectives for machine-learned probabilistic weather forecasting, testing whether multivariate scoring rules can match CRPS-based training and how scale-aware losses shape forecast spectra. The work is technically sound in design and makes a useful empirical contribution, but critical reproducibility gaps prevent independent verification of the central results. The authors provide insufficient detail on model initialization, random seed handling, ensemble generation, and the exact preprocessing pipeline. Code is stated to be "implemented in the Anemoi framework" but no repository link, version, or commit hash is given. The spectral analysis in Section 4.2 is the paper's main novel finding, yet the figures (3–14) are referenced but their content is not described in the text, making it impossible to verify what the spectra actually show or whether the claimed differences are visually or statistically meaningful. Without access to trained model weights, code artifacts, or explicit reproduction instructions, a reader cannot rerun the experiments or validate the core claim that "scale-aware losses improve spectral fidelity" against the alternative that differences are within noise or arise from uncontrolled variation.

## Strengths

1. The paper clearly defines six novel scoring rules (energy score, graph energy score, graph variogram score, graph edge energy score, CRPS edge score, and spectral variants) with explicit mathematical formulations that can be inspected and implemented independently.

2. The experimental design isolates the effect of loss function by holding architecture, data, and training schedule constant across the three main experiments (Section 3.1), a sound approach for the stated question.

3. The authors acknowledge limitations (Section 5: "smaller models, relatively low spatial resolution, shortened training schedule") and note that model capacity and resolution may change conclusions, which is candid about scope.

## Weaknesses: Load-bearing claims

**Claim 1: Multivariate scores are viable alternatives to CRPS for global machine-learned weather forecasting.**

The evidence is Figure 2, which shows CRPS, energy score, and graph energy score experiments. The text states "forecast skill is broadly similar across the experiments" with "only small differences" in the extratropics and the graph energy score "appears to perform best" in the tropics while the energy score "shows some degradation." This comparison does not establish viability because: (a) no confidence intervals, error bars, or statistical significance tests are reported for any of the three experiments, so "small differences" and "degradation" are unquantified; (b) the figure itself is not described—what do the panels show, what are the units, what is the baseline, and are differences visually distinguishable from noise?; (c) no ablation or sensitivity analysis shows whether the graph energy score's tropical advantage persists across different random seeds, ensemble sizes, or initialization schemes. The claim rests on a visual comparison of three curves with no uncertainty quantification. An alternative explanation is that all three losses converge to similar skill because the model capacity and architecture dominate the loss choice, and the apparent tropical separation is within the noise of a single training run.

**Claim 2: Scale-aware losses improve spectral realism of forecast fields.**

The evidence is Figures 3–14, which show "accumulated tendency spectra" for geopotential, meridional wind, and temperature. The text states "making the forecast scores scale-aware substantially improves small-scale variability" and "differences between scale-aware loss objectives are comparatively small." However: (a) Figures 3–14 are not described in the text—no caption explains what is plotted, what the y-axis represents, what the reference line is, or how to read the ratio plots; (b) no quantitative metric (e.g., spectral slope, integrated small-scale power, or L2 distance from ERA5) is reported, so "substantially improves" cannot be verified; (c) no error bars or confidence intervals across the 84 initialization dates are shown, making it impossible to assess whether differences between experiments exceed sampling variability; (d) the twelve experiments (Table 2) use ad hoc weighting factors "chosen only to be of the right order of magnitude—estimated from the data—rather than tuned," which introduces an uncontrolled degree of freedom that could explain observed differences; (e) the paper does not report whether the same random seed was used across all twelve experiments, so differences could reflect stochastic variation rather than loss function effects. The claim that scale-aware losses improve spectra is supported only by visual inspection of unlabeled figures with no quantitative comparison to noise or to a null model.

**Claim 3: The graph energy score with weak global anchor is a promising alternative to CRPS.**

Section 5 concludes "localized multivariate training objectives are a promising alternative to CRPS-based training, whereas the purely global energy score appears less robust." This rests on the tropical results in Figure 2 and the spectral results in Figures 3–14. Neither provides sufficient evidence: the tropical separation is not quantified and may not be statistically significant; the spectral differences are not quantified and may reflect uncontrolled weighting choices rather than the score itself. The claim is also not isolated—the graph energy score experiment uses a "weak global fair energy score anchor" (0.1 × fES), so the improvement could come from the anchor, the localization, the graph structure, or their interaction. No ablation isolates the contribution of each component.

## Weaknesses: Sweep

1. **Code and data availability:** The manuscript states all scores are "implemented in the Anemoi framework" but provides no repository URL, version number, commit hash, or link to trained model weights; readers cannot access or run the code.

2. **Random seed and stochasticity:** No random seed is reported for any experiment; it is unclear whether results are from a single run or averaged over multiple runs, and whether the same seed was used across experiments to isolate loss effects.

3. **Ensemble generation:** The paper states "we generate 8-member ensembles" but does not explain how ensemble members are sampled from the trained model (e.g., are they independent forward passes with different random noise, or deterministic samples from a learned distribution?).

4. **Figure descriptions:** Figures 3–14 lack captions explaining axes, units, reference lines, or how to interpret ratio plots; the text does not describe what is shown, making verification impossible.

5. **Preprocessing and grid details:** The O96 reduced Gaussian grid is mentioned but the exact preprocessing (normalization, masking, handling of missing data) is not described; the k-nearest-neighbor graph uses k=16 but no justification or sensitivity analysis is provided.

6. **Training reproducibility:** The learning-rate schedule (cosine with warmup, then fixed rates) and AdamW hyperparameters (weight decay 0.1) are specified, but the batch size, data shuffling, and number of training examples per epoch are not stated.

7. **Spectral weighting ad hoc:** The paper acknowledges weighting factors for multi-scale and spectral experiments are "ad hoc" and "not tuned," yet does not report the actual values used or test sensitivity to them, leaving a major uncontrolled variable.

8. **Statistical testing:** No significance tests, confidence intervals, or bootstrap resampling are reported for any comparison; all claims of difference rely on visual inspection.

## Questions

1. What are the exact numerical values of the ad hoc weighting factors (ζ_i for scales, per-variable weights for geopotential and MSLP, and spectral-band weights) used in Section 3.2, and how sensitive are the spectral results to ±50% variation in these weights?

2. Were the same random seed(s) used across all experiments in Section 3.2, and if so, which seed; if not, how many independent runs were performed and what are the standard deviations of the reported differences?

3. What do Figures 3–14 show on the y-axis (power spectral density, variance, or another quantity), what is the reference line (ERA5 mean, ERA5 ±1σ, or another baseline), and are the ratio plots (Figures 5, 6, 9, 10, 13, 14) computed as forecast/ERA5 or ERA5/forecast?

4. Can the authors provide a link to the Anemoi repository, version number, and commit hash used for these experiments, or a standalone implementation of the six scoring rules sufficient to reproduce the loss values?

5. For the three experiments in Section 3.1, what are the 95% confidence intervals on the CRPS values shown in Figure 2, computed either from multiple runs or from the ensemble spread?