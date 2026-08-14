# Related-Work & Citations Reviewer

## Summary
The manuscript cites relevant foundational work on scoring rules and machine-learned weather forecasting, but has several citation issues. The literature review is reasonably current but misses some directly competing work on multivariate scoring for weather forecasting. Attribution accuracy is generally good, but there are specific claims about scoring rule properties that need verification. The reference list appears complete but contains formatting inconsistencies.

## Strengths
- Cites foundational scoring rule literature (Gneiting & Raftery 2007, Ferro 2014) appropriately
- References recent major machine-learned weather forecasting systems (AIFS-CRPS, FourCastNet 3, Huracan, etc.)
- Acknowledges related work on scale-aware losses (Lang et al. 2025)

## Weaknesses
- The manuscript claims "The graph energy score, however, may fail to be strictly proper because different distributions can lead to the same local score even though they differ in their long-range dependence." This is presented as a known property but lacks citation. A search reveals no literature establishing this specific property for graph energy scores. The authors should either provide a citation or demonstrate this claim mathematically, as it's central to their motivation for adding a global anchor.
- The manuscript references Pacchiardi et al. (2024) [19] for patched energy scores performing best in weather forecasting experiments, but doesn't acknowledge that this work specifically compared multivariate scoring rules for weather forecasting. This omission understates the novelty of their own contribution, as Pacchiardi et al. already established the viability of multivariate scores for weather forecasting.

## Questions
- Please provide a citation or mathematical demonstration for the claim that "The graph energy score, however, may fail to be strictly proper because different distributions can lead to the same local score even though they differ in their long-range dependence."
- Can you confirm that reference [12] (Lakatos 2026) is published or in press, and if not, provide alternative citations for the claim about composite-loss graph neural networks for multivariate post-processing?
- Have you considered comparing your approach to the signature kernel scoring rule (arXiv:2510.19110v2, 2025) which specifically addresses spatio-temporal diagnostics for probabilistic weather forecasting?