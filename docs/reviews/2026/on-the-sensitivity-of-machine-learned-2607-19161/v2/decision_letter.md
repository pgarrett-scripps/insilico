# Decision Letter

**Decision:** major

## Summary of Evaluation
The manuscript presents a timely comparison of scoring rules for machine-learned weather forecasting, with a focus on multivariate and scale-aware formulations. The review panel acknowledges the study's clear technical definitions and its exploration of an important methodological question. However, several critical issues prevent acceptance in the current form.

The primary concern is methodological: the forecast skill comparison (Section 4.1) confounds the choice of scoring rule with differences in spatial weighting, making it impossible to attribute observed performance differences to multivariate scoring per se. Additionally, claims about relative performance ("best," "degradation") lack statistical support (confidence intervals, significance testing), rendering them unsubstantiated.

Reproducibility is another major hurdle. The custom implementations of novel scoring rules are unavailable, creating a HARD barrier to verification. The spectral weighting schemes are described only as "ad hoc" without specific values or estimation procedures.

The abstract misleadingly frames the work around "scale-aware scoring rules," while the primary skill comparison uses non-scale-aware versions—a disconnect that must be corrected.

While the spectral experiments (Section 4.2) provide valuable evidence that explicit scale constraints improve realism, the design there also conflates scoring rule type with weighting schemes, limiting causal inference.

The panel's average score (3.79/5) reflects these substantive concerns, with three reviewers recommending major revision. The work has merit but requires substantial revision to support its claims and enable verification.

## Required Revisions
1. 1. Statistical support for comparative claims: For the forecast skill comparison (Section 4.1), provide quantitative measures of uncertainty (e.g., confidence intervals via bootstrapping across forecast dates) and formal significance testing where claims of superiority or degradation are made. Revise all qualitative performance descriptions (e.g., 'best,' 'degradation') to align with the statistical evidence.
2. 2. Controlled experimental design: Conduct new experiments that isolate the effect of scoring rule type from spatial weighting. Specifically: (a) For the forecast skill comparison, add a 'multi-scale CRPS' experiment with the same model size and training schedule as the graph energy experiment, to provide a baseline where scale-awareness is controlled. (b) For the spectral analysis, design experiments that apply the same multi-scale or spectral weighting scheme to each scoring rule variant, enabling attribution of differences to the scoring rule itself.
3. 3. Code availability: Provide a versioned repository (GitHub commit hash or Zenodo DOI) containing the exact code used to implement all novel scoring rules (graph energy score, graph variogram score, edge scores, multi-scale loss, spectral losses) and the training/evaluation scripts that generated the figures. This is essential for verifying the reported results.
4. 4. Correct misleading framing: Revise the abstract and introduction to clarify that the primary forecast skill comparison (Section 4.1) uses standard, non-scale-aware versions of scoring rules, while scale-awareness is explored separately in Section 4.2. Remove claims that the study compares 'scale-aware scoring rules' in the context of the skill comparison.
5. 5. Specification of weighting procedures: Provide the exact numerical weighting factors used for geopotential and mean sea-level pressure in multi-scale experiments, and for spectral bands in spectral loss experiments. Describe the method used to 'estimate' these weights from data (e.g., inverse variance, scaling factors) so the procedure is reproducible.
6. 6. Citation verification: Provide complete citations for references [9], [10], and [11], and verify that references [13], [15], [18], and [19] support the specific claims made about them. For the claim that the graph energy score 'may fail to be strictly proper,' either provide a citation or include a brief mathematical demonstration.

## Minor Suggestions
- Clarify ambiguous pronoun reference in Section 4.1: Revise 'the other two experiments' to explicitly state which experiments are being compared (CRPS and graph energy score).
- Add a brief explicit definition of 'scale-aware' early in the manuscript to aid non-specialist readers.
- Provide software environment details (PyTorch version, Anemoi commit) and primary hardware specifications to facilitate computational replication.
- Discuss the rationale for choosing α=0.95 for the 'almost fair' CRPS rather than fair (α=1) or standard (α=0) versions, particularly in relation to comparability with fully fair energy score variants.
- Include random seeds or a statement on seed averaging for stochastic processes.
- Add signposting sentences in Section 4.2 to clarify which variable's spectra are being discussed in each paragraph.