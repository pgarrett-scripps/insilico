# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This paper compares machine-learned probabilistic weather forecast models trained with different proper scoring rules—CRPS, fair energy score, and graph energy score—and examines how scale-aware loss constraints affect forecast field spectra. The work is methodologically sound and addresses a relevant question for the field, but the central claims about multivariate scoring rules as viable alternatives to CRPS rest on evidence that does not fully support the strength of the conclusion. The spectral analysis is useful but secondary, and the paper's scope is deliberately limited in ways that weaken generalizability.

## Load-bearing Claims

**Claim 1: Multivariate scores (energy score, graph energy score) are viable alternatives to CRPS-based training for global machine-learned weather forecasting.**

The evidence offered is Figure 2, which shows forecast skill (CRPS, temperature, wind, geopotential) across three experiments. The authors state: "Forecast skill is broadly similar across the experiments" and note that "in the extratropics we do not find a noticeable difference." However, this conclusion conflates "similar large-scale skill" with "viable alternative." A viable alternative should perform comparably *across all tested conditions and metrics*. The tropical results show the graph energy score performs "somewhat better" while the global energy score "shows some degradation"—a directional difference that contradicts the claim of broad similarity. More critically, the paper does not report whether these differences are statistically significant, whether they persist across multiple initializations or years, or whether they hold at the higher resolutions (O96 ≈ 1°) where the authors acknowledge maintaining spatial coherence is "particularly challenging." The authors themselves note in the Discussion that "greater model capacity and longer training may improve the performance of losses without scale awareness or reduce the differences between experiments." This is not a minor caveat—it means the ranking of methods observed here may reverse under conditions closer to operational practice. The claim would be defensible if narrowed to "comparable large-scale extratropical skill" or if accompanied by confidence intervals and significance tests on the tropical differences, or if the authors had tested at higher resolution where the stakes are higher.

**Claim 2: Scale-aware losses substantially improve small-scale variability and lead to more realistic forecast fields.**

The evidence is Figures 3–14, which show accumulated tendency spectra for geopotential, wind, and temperature. The authors state: "Making the forecast scores scale-aware substantially improves small-scale variability." However, the figures themselves show that (i) differences between scale-aware methods are "comparatively small" (authors' own words), (ii) some experiments "show a slight overcompensation" (authors' own words), and (iii) achieving realistic spectra for geopotential "appears more challenging than realistic spectra for wind and temperature" (authors' own words). The paper does not establish what "substantially" means quantitatively—no threshold, no statistical test, no comparison to a baseline improvement target. The spectral plots show ratios of forecast to ERA5 tendency spectra, but without error bars, confidence intervals, or a statement of how many forecasts were averaged (stated only as "84 initialization dates"), it is impossible to judge whether observed differences exceed sampling variability. The claim that scale awareness "leads to more realistic forecast fields" is supported only for spectral shape, not for other measures of realism (e.g., physical balance, energy conservation, or skill metrics). The alternative explanation—that the observed spectral differences reflect different effective weightings per scale rather than fundamental improvements in realism—is acknowledged by the authors ("the largest differences are likely associated with different effective weights per scale") but not tested. To settle this, the authors would need to show that scale-aware losses improve spectra *beyond what can be explained by ad hoc reweighting of the same underlying score*, or to demonstrate that improved spectra correlate with improved forecast skill or physical consistency.

**Claim 3: The graph energy score is a promising localized multivariate alternative to patch-based energy scores.**

The paper proposes the graph energy score as an improvement over global energy scores and claims it offers flexibility for irregular grids. However, the evidence for superiority is limited to one experiment (Figure 2, tropical region) where it outperforms the global energy score but is not compared to the patched energy score of Pacchiardi et al. (2024), which the authors cite as motivating their work. The paper states the graph energy score "may fail to be strictly proper" and requires a "weak global anchor" (the fair energy score) to recover propriety. This is a significant limitation that is mentioned but not explored: how much of the graph energy score's performance comes from the graph component versus the added global anchor? Without an ablation (graph energy score alone vs. with anchor), the claim that the graph approach is superior cannot be separated from the effect of adding the global term. The flexibility argument for irregular grids is theoretical—no experiment tests the method on irregular grids or sparse networks.

## Strengths

1. The paper clearly defines and implements multiple proper scoring rules with fair variants, making the mathematical framework transparent and reproducible.

2. The spectral analysis using accumulated tendency spectra is a principled diagnostic that goes beyond standard skill metrics and reveals scale-dependent structure in forecast fields.

3. The authors are candid about limitations (smaller models, low resolution, shortened training, ad hoc weighting) and acknowledge that results may not generalize to operational settings.

## Weaknesses

**Load-bearing:**

1. **Tropical skill differences not quantified.** Figure 2 shows separation in tropical regions (graph energy best, global energy degraded) but no confidence intervals, significance tests, or statement of whether differences exceed inter-annual variability. The claim of "broad similarity" is not supported where differences are visible.

2. **Spectral improvements lack statistical grounding.** Figures 3–14 show ratios without error bars or significance tests; with only 84 initialization dates, sampling variability is unknown. The claim that scale-aware losses "substantially improve" small-scale variability is not quantified.

3. **Scale-aware loss superiority confounded with reweighting.** The authors acknowledge that "different effective weights per scale" may explain the spectral differences, but do not test whether improved spectra reflect genuine improvements in forecast realism or only reflect different weightings of the same underlying score. No ablation isolates the contribution of scale-aware structure from ad hoc per-variable, per-scale weighting.

4. **Graph energy score not isolated from global anchor.** The graph energy score is always combined with a fair energy score anchor (L_graph = fGES_graph + 0.1 fES). No experiment tests the graph component alone, so superiority cannot be attributed to the graph localization rather than the added global term.

5. **Comparison to patched energy score missing.** The authors cite Pacchiardi et al. (2024) as motivating the graph energy score, but do not compare against it. The claim that graph-based localization is superior to patch-based localization is not tested.

**Sweep:**

6. The paper does not report whether the three experiments in Section 3.1 used the same random seed, initialization, or data splits, raising the possibility that differences reflect stochastic variation rather than method differences.

7. The choice of α = 0.95 for the almost fair CRPS is not justified; sensitivity to this hyperparameter is not explored.

8. The "weak global anchor" weight (0.1) for the graph energy score appears ad hoc and is not justified or ablated.

## Questions

1. For Figure 2 (tropical region): what are the 95% confidence intervals on the CRPS differences, and are they statistically significant at the 5% level?

2. For Figures 3–14: what is the sampling uncertainty (e.g., standard error or 95% CI) on the spectral ratios, and do the differences between scale-aware methods exceed this uncertainty?

3. Was the same random seed and data split used for all three experiments in Section 3.1, or were they run independently?

4. How sensitive are the results to the choice of α = 0.95 for the almost fair CRPS, and to the weight 0.1 on the global energy score anchor in the graph energy experiment?