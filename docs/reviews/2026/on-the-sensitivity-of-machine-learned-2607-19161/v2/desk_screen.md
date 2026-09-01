# Desk Screen Report

## Summary

This manuscript compares different proper scoring rules (CRPS, energy scores, graph-based scores) as training objectives for machine-learned probabilistic weather forecasting models, and investigates how scale-aware loss formulations affect forecast field spectra.

## Scope Assessment

**In Scope**: The work is original research in machine learning applied to weather forecasting. It presents empirical comparisons of training objectives, methodological development (graph energy score variants), and analysis of resulting model properties. The claims are checkable from the manuscript and cited materials. This fits clearly within In Silico's scope for computational and methodological work.

## Threshold Issues

**No fundamental blockers identified:**

1. **Completeness**: The manuscript is complete. Methods are described with sufficient detail (architecture, training schedule, loss formulations, verification approach). Experiments are clearly specified.

2. **Intelligibility**: The paper is well-written and organized. Mathematical notation is consistent. The progression from score definitions through experiments to results is logical.

3. **Evidence-claim alignment**: Claims are appropriately scaled to evidence:
   - Claim: "multivariate scores are a viable alternative to CRPS-based training" — supported by comparable skill across experiments (Figure 2)
   - Claim: "scale-aware losses improve spectral fidelity" — supported by spectral analysis (Figures 3–14)
   - Authors explicitly acknowledge limitations (smaller models, lower resolution, shortened training schedule)

4. **Reproducibility**: Sufficient detail is provided. Code is stated to be in the Anemoi framework. Training hyperparameters, data sources (ERA5), and model configurations are specified. Some experimental choices are noted as "ad hoc" (e.g., weighting factors), which is honest.

## Substantive Observations (for reviewers, not grounds for desk rejection)

- The first experiment set (Section 3.1) is relatively modest in scope: three loss objectives on one model size/resolution. The differences are small, particularly in extratropics.
- The second experiment set (Section 3.2) is more extensive (12 configurations) but uses a smaller, cheaper model variant, limiting generalizability of conclusions.
- The paper does not claim to resolve which loss is "best" — it explores whether alternatives work, which is a reasonable framing given the constraints.
- The spectral analysis is thorough and the finding that weighting matters as much as the scoring mechanism itself is useful.
- Some figures (3–14) are repetitive and could be condensed, but this is a presentation issue, not a scientific one.

## Recommendation

The manuscript addresses a real question in an active area (machine-learned weather forecasting), uses sound methodology, reports results honestly including limitations, and contributes both methodological variants (graph energy scores) and empirical insights (scale-awareness effects on spectra). It is not groundbreaking, but it is competent, complete, and suitable for expert review.

**DESK DECISION: proceed**

The work should go to full review. Reviewers can assess whether the experimental scope is sufficient, whether the conclusions about multivariate scores and scale-awareness are justified, and whether the contribution merits publication.