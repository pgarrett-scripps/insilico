# Contribution & Prior-Work Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a competent empirical study that makes a real but incremental contribution to machine-learned weather forecasting. The manuscript compares several multivariate and scale-aware scoring rules as training objectives for probabilistic ensemble models, finding that graph-localized energy scores and spectral losses can match or slightly exceed CRPS-based training in large-scale skill while improving small-scale spectral fidelity. The work is honest about its preliminary scope and limitations, but the novelty is modest: the core methodological components (fair CRPS, energy scores, variogram scores, multi-scale losses, spectral losses) are all established, and the graph energy score is presented as a straightforward localization of existing multivariate scores rather than a fundamentally new approach. The contribution lies in the systematic empirical comparison and the finding that scale-aware losses improve spectral realism, not in methodological innovation.

## Strengths

1. The paper provides a useful empirical comparison of multiple scoring rules on a consistent architecture and dataset, filling a gap in the literature where such systematic comparisons for global weather forecasting are rare.

2. The authors are transparent about limitations (smaller models, low resolution, shortened training, ad hoc weighting choices) and frame the work as preliminary, which is appropriate and honest.

3. The implementation of multiple scoring rules in the Anemoi framework and the focus on spectral diagnostics provide practical value to the community.

## Weaknesses: Load-Bearing Claims

**Claim 1: Multivariate scores are a viable alternative to CRPS for global machine-learned weather forecasting.**

The evidence is that three experiments (CRPS, global energy score, graph energy score) show "broadly similar" large-scale skill (Figure 2), with only small differences in the extratropics and some tropical separation where graph energy performs best and global energy shows degradation. However, this result does not establish that multivariate scores are a viable *alternative* in the sense of being interchangeable or preferable. The global energy score—the purely multivariate baseline—actually underperforms in the tropics, which is the opposite of what a claim of viability would require. The graph energy score performs comparably, but it is a hybrid: it combines local multivariate structure with a global energy score anchor (0.1 × fES term), making it not a pure multivariate alternative but a constrained version. The manuscript does not isolate whether the graph energy score's tropical advantage comes from the localization, the global anchor, or their interaction. Without ablation (e.g., graph energy score alone without the anchor), the claim that "multivariate spatial training objectives can match the large-scale forecast skill obtained with CRPS-based training" remains ambiguous—the graph energy score succeeds partly because it includes a CRPS-like global constraint. A fairer statement would be that localized multivariate scores with global anchors can match CRPS, not that multivariate scores alone do.

**Claim 2: Scale-aware losses improve spectral realism and small-scale variability.**

The evidence is Figures 3–14, which show accumulated tendency spectra for geopotential, wind, and temperature at 500 hPa across 12 loss configurations. The authors state: "Making the forecast scores scale-aware substantially improves small-scale variability and leads to more realistic forecast fields." However, the figures themselves are not inspectable in detail from the text alone—I cannot verify the magnitude of differences, the statistical significance, or whether the improvements are consistent across variables and lead times. The text notes that "differences between scale-aware loss objectives are comparatively small" and that "some experiments show a slight overcompensation for some variables, where the early lead-time tendencies contain less small-scale variability than the ERA5 reference." This hedging undermines the strength of the claim. The comparison also lacks a quantitative metric: the authors show ratios of forecast to ERA5 spectra but do not report, for example, integrated spectral error or a summary statistic that would allow readers to judge whether the improvements are practically significant. The ad hoc weighting of scales and variables (acknowledged as "not tuned") further clouds whether the observed differences reflect the scoring rule or the choice of weights. Without a quantitative summary and ablation on weighting, the claim that scale-aware losses "substantially improve" realism is not fully supported—the figures suggest modest, variable improvements that depend heavily on configuration choices.

## Weaknesses: Sweep

1. The graph energy score is presented as novel, but it is a straightforward application of graph-based localization to the energy score, similar in spirit to the patched energy score of Pacchiardi et al. (2024, arXiv:2112.08217), which the authors cite; the key difference is using graph neighbourhoods instead of fixed patches, which is an engineering choice rather than a conceptual advance.

2. The multi-scale loss formulation (Section 2.5) is attributed to Lang et al. (2025, ref. 14), which appears to be concurrent or very recent work by the same lead author; the manuscript does not clarify whether this is a novel contribution here or a reuse of an established method.

3. The spectral losses (spectral energy score, spectral magnitude CRPS) are standard applications of existing scores to spectral coefficients; the manuscript does not claim novelty here but the framing as part of the contribution could be clearer.

4. The paper does not compare against other recent scale-aware or spectral approaches mentioned in the discussion (e.g., FourCastNet 3's spectral loss, Mosaic's sparse attention for spectral fidelity by Zhdanov et al. 2026), so the relative merit of the proposed losses is unclear.

5. The choice of k=16 for the graph neighbourhood and the Gaussian smoothing kernel widths (100, 200, 400, 800 km) are stated as fixed but not justified or ablated, leaving open whether results are sensitive to these hyperparameters.

6. The manuscript uses ERA5 reanalysis for training and 2022 for inference, but does not discuss whether 2022 is representative or whether results would hold for other years or different climate regimes.

7. The claim that the graph energy score "may fail to be strictly proper" (Section 2.3) is acknowledged, but the practical consequence for training is not explored; the authors add a global anchor to recover propriety, but do not test whether the non-proper version would perform differently.

8. The paper is framed as a "preliminary study" with "smaller models, relatively low spatial resolution, and a shortened training schedule" (Discussion), which limits the generalizability of findings to operational or high-resolution settings.

## Questions

1. In Figure 2, what is the statistical significance of the tropical differences between CRPS, global energy, and graph energy? Are they within the noise of the experimental setup?

2. For the spectral experiments (Figures 3–14), can you provide a single quantitative summary metric (e.g., integrated squared error in log-space, or a skill score relative to ERA5) that allows comparison across all 12 configurations?

3. Does the graph energy score without the global energy score anchor (i.e., fGES_graph alone) match CRPS skill, or is the anchor essential for the tropical improvement?