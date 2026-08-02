# Novelty & Contribution Reviewer

## Summary
This preliminary study compares proper scoring rules as training objectives for machine-learned weather forecasting, with emphasis on multivariate and scale-aware variants. The work is technically sound and honestly framed as preliminary, but novelty is substantially limited by concurrent work from the same authors (Lang et al. 2025 on multi-scale losses) and prior work on patched energy scores (Pacchiardi et al. 2024). The graph-based localization is a natural variant of patch-based approaches, and spectral scoring rules are not clearly established as novel. Experimental results are confirmatory: scale-aware losses improve small-scale variability, and multivariate scores perform comparably to CRPS. The contribution is primarily empirical validation on a reduced-resolution model, with findings that do not substantially advance understanding of why different scoring rules should be preferred. The manuscript would benefit from clearer delineation of novel contributions from prior work and stronger justification for the significance of the findings.

## Strengths
- Systematic and transparent comparison of multiple scoring rules within a consistent framework.
- Clear mathematical exposition of all scoring rules with reproducible notation.
- Honest framing as preliminary work with acknowledged limitations (model size, resolution, training schedule).
- Practical implementation in Anemoi framework with torch.compile optimizations supporting reproducibility.
- Spectral analysis using accumulated tendency spectra provides a useful diagnostic of physical realism.

## Weaknesses
- Multi-scale loss formulation is from Lang et al. (2025, arXiv:2506.10868), not a novel contribution of this work. The manuscript applies this existing formulation to new scoring rules but does not clearly state this boundary. Section 2.8 and experiments in Section 3.2 should explicitly credit Lang et al. (2025) as the source of the multi-scale approach.
- Graph energy score is presented without clear novelty justification. The manuscript acknowledges it is 'similar to patched energy score' (Pacchiardi et al. 2024) but does not explain what is genuinely new beyond using k-nearest-neighbor graphs instead of rectangular patches. No experimental comparison to patch-based localization is provided.
- Graph variogram score and graph edge energy score lack novelty statements. These are straightforward extensions of existing scores (variogram score from Scheuerer & Hamill 2015; energy score) to graph neighborhoods, but the manuscript does not explicitly state this or justify why these variants are worth introducing.
- Spectral scoring rules are not established as novel. The manuscript introduces 'spectral energy score' and 'spectral magnitude CRPS' without citing prior work, then later mentions FourCastNet 3 uses 'spectral loss term like spectral magnitude CRPS,' suggesting this is not new. Novelty should be clarified.
- Experimental results are confirmatory, not surprising. All objectives are proper scoring rules; the finding that 'forecast skill broadly similar' and 'differences between scale-aware loss objectives comparatively small' (Section 4.2) does not advance understanding of why one would prefer one score over another.
- No head-to-head comparison to closest prior work. The manuscript cites Pacchiardi et al. (2024) on patched energy scores but does not experimentally compare graph-based vs. patch-based localization. Similarly, no direct comparison to Lang et al. (2025) results is provided.
- Claimed generalizability of graph approach is not demonstrated. The paper states the graph method 'can in principle applied on irregular grids, sparse spatial meshes, or sparse observation networks' (Section 2) but provides no experiments on non-regular grids. This should be either demonstrated or removed.
- Spectral weighting is ad hoc. The manuscript states weighting factors are 'ad hoc and chosen only to be of right order of magnitude—estimated from data—rather than tuned' (Section 3.2). No ablation studies test sensitivity to these choices, undermining confidence in the spectral results.
- Limited model capacity and resolution. Experiments use O96 (~1°) resolution and 8-member ensembles. The authors acknowledge (Section 5) that 'greater model capacity and longer training may improve performance of losses without scale awareness or reduce differences between experiments,' which undermines generalizability of findings.
- Missing ablations on design choices. The graph energy score uses k=16 nearest neighbors without ablation. Multi-scale experiments use four smoothing operators with specific kernel widths (100, 200, 400, 800 km) without justification.

## Questions
- Is the multi-scale loss formulation (Section 2.8) entirely from Lang et al. (2025), or have you made modifications? If modifications exist, what are they and how do they constitute a novel contribution?
- Have you experimentally compared graph-based localization to the patched energy scores of Pacchiardi et al. (2024)? If not, why not?
- Are the spectral energy score and spectral magnitude CRPS formulations original to this work, or are they standard practice in the field? Please cite any prior use.
- For graph variogram score and graph edge energy score: are these novel contributions, or straightforward extensions of existing scores to graph neighborhoods? Please clarify the novelty boundary explicitly.
- How sensitive are the spectral results (Figures 3–14) to the ad hoc weighting choices? Can you provide ablation studies?
- Can you demonstrate the claimed applicability of the graph approach to irregular grids, sparse meshes, or sparse observation networks, or should this be framed as future work?
- Is the tropical improvement of graph energy score (Section 4.1) statistically significant? What is the magnitude of improvement in absolute terms?
- How would results change with the full-resolution AIFS-CRPS model rather than the O96 reduced version? Is this planned?