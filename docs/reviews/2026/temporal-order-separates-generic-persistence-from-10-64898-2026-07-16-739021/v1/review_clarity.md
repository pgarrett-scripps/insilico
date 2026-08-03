# Clarity & Presentation Reviewer

## Summary
The manuscript introduces a valuable temporal-order analysis framework for cell migration, supported by rigorous hierarchical statistics and multiple datasets. The claims are clearly stated and the evidence is transparently presented, though a few terminological inconsistencies and under-explained methodological choices create minor friction for the reader.

## Strengths
- The glossary (Table 1) and consistent term definitions allow a non-specialist to follow the novel metrics.
- The hierarchical bootstrap with simultaneous confidence bands is clearly motivated and correctly applied across all datasets.
- The accompanying workflow and deposited code enable full reproducibility of the analytical pipeline.

## Weaknesses
- Claim 1 (MYO10–collagen interaction carried by temporal order): The analytical order-null assumes that uniform permutation of steps is the appropriate reference for "no temporal order," which implicitly assumes step exchangeability. If trajectories exhibit non-stationary trends (e.g., systematic speed changes), the permutation destroys those trends and the sequence-excess will capture them as "temporal order," potentially conflating true serial correlation with non-stationarity. The manuscript tests early vs. late windows in an appendix but does not discuss this assumption in the main text, leaving the reader unaware of this interpretive caveat. A brief statement in Results or Methods clarifying that the null model assumes exchangeability and that the early-vs-late test addresses non-stationarity would resolve this ambiguity.
- Claim 3 (PFKL-N702T spares generic serial order): The non-inferiority margin of 0.10 SD for generic serial-order measures is described as "locked" but its justification is absent from the main text (only appearing in Methods as "the smallest meaningful loss\)). Without a stated rationale, the reader cannot judge whether this threshold is biologically appropriate or arbitrary. Additionally, the conclusion is explicitly at the track level because biological-replicate labels were missing; the manuscript notes this but does not emphasize that track-level non-inferiority may not imply replicate-level preservation. Adding a sentence in Results explaining the margin's origin and the inference level would improve clarity.
- Claim 2 (Haptotaxis geometry redistributes order): The distinction between "axis contribution" (activity-weighted) and "intrinsic axis order" (activity-normalized) is central to the interpretation but is only defined in Table 1. A reader who does not consult the table may miss that the lateral-axis contribution increase could simply reflect more lateral steps, whereas the intrinsic lateral order increase confirms those steps are more temporally correlated. The Results paragraph mentions this distinction once but would benefit from a parenthetical reminder of the definitions.
- The terms "sequence excess" and "sequence-dependent persistence" are used interchangeably; picking one as the primary term would reduce cognitive load.
- The non-stationary linear active-memory model and angular hidden-state model are described in detail, but the criteria for a target "passing" (80% coverage, observed mean within interval, sign probability ≥0.90) are only in Methods; a one-sentence summary in Results would help.
- "Lag-invariant cohort" is used in Results before its definition in Methods; define at first use.
- In the abstract, "stationary angular hidden-state model" differs from the main text's "nonlinear angular hidden-state model\); harmonize terminology.
- The cross-system validation (Figure 6) compares disparate experimental conditions; the caption notes this, but the figure panels (A–D) use identical axes, which may invite inappropriate quantitative comparison. A visual cue or a note in the legend would help.
- The PFKL analysis uses five perturbation series as "concordant mechanistic comparisons" but the main text does not list them all in the Results paragraph (only in Methods); a brief enumeration in Results would aid flow.
- The term "buffering interaction" is well-defined in Table 1 but the main text uses "positive factorial interaction" and "buffering" interchangeably; consistent use of "buffering" after definition would be smoother.

## Questions
- For the MYO10–collagen analysis, does the analytical order-null formula (Eq. 8) assume step exchangeability, and if so, is the early-vs-late window test sufficient to rule out non-stationarity as a driver of the sequence-excess interaction?
- What was the biological or statistical rationale for choosing 0.10 SD as the non-inferiority margin in the PFKL analysis?
- In the haptotaxis dataset, were the 131 trajectories from independent biological replicates, and if so, how many? The Methods mention "deposited block labels" but the Results do not state the replicate number.