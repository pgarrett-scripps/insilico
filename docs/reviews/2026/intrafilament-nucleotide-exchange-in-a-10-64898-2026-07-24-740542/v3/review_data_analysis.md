# Statistics & Data-Analysis Reviewer

## Summary
The paper makes several striking mechanistic claims about MreB filament dynamics, but the statistical support for the load-bearing conclusions is weak. Filament-level measurements are repeatedly treated as independent replicates despite originating from only 1–2 experimental repeats (SLB preparations), constituting pseudo-replication. Key comparisons lack any stated statistical test, p-values, or confidence intervals. The Monte Carlo model parameters are presented without uncertainty quantification. These issues undermine the evidentiary basis for the central claims.

## Strengths
- The experimental design combines multiple complementary imaging modalities (TIRF, HS-AFM, TEM, QCM-D) to address the same biological question from different angles.
- The use of ATPase-deficient mutants (E136A, D158A) as mechanistic probes is well-conceived and internally consistent across assays.
- The Monte Carlo model integrates measured kinetic parameters into a coherent framework that generates testable predictions.

## Weaknesses
- Claim of symmetrical elongation (Fig 2G): the ratio metric (shorter/longer growth) is bounded [0,1] by construction; n=13 filaments from an unstated number of SLBs; no test of whether the mean ratio differs from the polar-growth expectation, no p-value, and no accounting for non-independence of filaments on the same bilayer.
- Claim that ATP hydrolysis is dispensable for polymerization (Fig 3D): elongation rates compared across WT, E136A, D158A with n=318, 68, 39 filaments from only two independent experiments; filaments on the same SLB are not independent replicates; no statistical test (ANOVA, Kruskal-Wallis, or mixed model) is reported, so 'similar kinetics' is unsupported.
- Claim of intrafilament nucleotide exchange (Fig 3I): ATP* incorporation rates compared across three genotypes (n=19, 12, 17 filaments) with no statistical test; 'about twice as fast' for D158A vs WT is a quantitative claim without a confidence interval or p-value; again, filaments are not independent experimental units.
- Claim that free ADP triggers rapid depolymerization (Fig 4B): disassembly rates reported for six conditions with large filament counts (n=60–408) but only two independent experiments; no within-genotype test of buffer vs ADP; the >5-fold acceleration for WT+ADP is dramatic but statistically unevaluated.
- Pervasive pseudo-replication: across Figures 2, 3, 4, and S8–S10, the independent unit of replication is the SLB preparation/experiment (n=1–2), yet filament counts (n=10s–100s) are used as n for error bars and implied precision. This inflates degrees of freedom and invalidates any parametric inference.
- Monte Carlo model (Fig 4D, S8–S10, Table 1) uses 10+ kinetic parameters, some from literature and some fitted, but reports no parameter uncertainties, no sensitivity analysis, and no goodness-of-fit metrics beyond visual agreement. Model predictions (e.g., Fig 4I) are presented as deterministic curves without confidence bands.
- In vivo CCCP experiment (Fig 4J) is purely qualitative — no segmentation, no filament intensity quantification, no statistics, no replication stated. The claim that E136A 'remained stable' while WT 'became progressively delocalized' rests on representative images alone.
- Error bars are inconsistently defined (sometimes 'mean ± SD', sometimes 'SD on top only') and it is unclear whether they reflect filament-level variability or experiment-level variability. SEM is never used, but SD of pseudo-replicates is equally misleading.

## Questions
- How many independent SLB preparations (biological/technical replicates) were performed for each condition in Figures 2, 3, and 4? The text says 'two independent experiments' for some assays but filament n is in the hundreds.
- For the photobleaching symmetry assay (Fig 2G), what is the expected ratio distribution under the null hypothesis of polar growth, and was a one-sample test against that null performed?
- Were mixed-effects models (with SLB as random effect) considered for the multi-genotype elongation/depolymerization comparisons? If not, why were filament-level n used directly?
- For the Monte Carlo model, what fitting procedure was used to estimate the parameters in Table 1 (e.g., k_hyd, k_Pir, k_+n, k_-n), and what are their confidence intervals?
- In the CCCP experiment (Fig 4J), how many cells were imaged per condition per time point, and was the delocalization quantified (e.g., membrane-to-cytoplasm fluorescence ratio)?