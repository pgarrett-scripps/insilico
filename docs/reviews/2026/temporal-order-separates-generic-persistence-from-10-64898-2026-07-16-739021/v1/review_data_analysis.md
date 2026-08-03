# Statistics & Data-Analysis Reviewer

## Summary
The manuscript introduces a valuable analytical framework that separates motility, generic persistence, and cue-aligned commitment using temporal-order analysis. However, the two primary biological conclusions rest on datasets with critically low biological replication (n=3 repeats for MYO10–collagen; zero replicate labels for PFKL), making population-level inference unreliable despite sophisticated hierarchical bootstrapping and simultaneous bands. The haptotaxis analysis also relies on an unspecified block hierarchy. These are not fixable by re-analysis; they require new experiments or explicit limitation statements. The method itself is mathematically sound and well-documented.

## Strengths
- The analytical order-null (exact permutation expectation) is a rigorous, computationally efficient way to isolate sequence-dependent persistence without simulation.
- The workflow is fully documented, versioned, and accepts standard tracking tables, enabling adoption and audit.
- Frozen analysis plans, lag-invariant cohorts, simultaneous confidence bands, and exact decomposition closure demonstrate high analytical discipline.

## Weaknesses
- The MYO10–collagen discovery claim relies on only three biological repeats (R1–R3), with R3 noted as disproportionately large and phenotypically distinct. Hierarchical bootstrapping at the repeat level with n=3 produces a discrete bootstrap distribution (≤27 unique resamples) that cannot support reliable simultaneous confidence bands or generalizable inference; the sign-consistency and leave-one-FOV-out criteria mitigate but do not resolve this fundamental design limitation. The manuscript acknowledges this but presents the buffering interaction as a supported finding rather than a hypothesis-generating observation.
- The PFKL chemotaxis conclusion (cue-aligned commitment lost, generic serial order preserved) is based entirely on track-level inference (150 tracks per group) because biological-replicate identity was lost in the public data. Tracks from the same replicate are not independent, so the reported HC3, propensity-matched, and non-inferiority intervals underestimate true uncertainty and cannot support population-level claims. The five perturbation series come from a single study, not independent replications.
- The haptotaxis analysis cites 'deposited block labels' for hierarchical bootstrap but never states the number of blocks, their size, or the experimental unit. With only 131 total tracks across five widths, if blocks are few (e.g., one experiment per width), the same low-replication problem recurs. The early-minus-late and 6h-vs-3h contrasts are also underpowered for interaction testing.

## Questions
- For the MYO10–collagen data: were the three biological repeats (R1–R3) performed on different passages, different days, or fully independent cell preparations? The manuscript says 'operational independence of R1–R3 could not be verified beyond the public metadata.'
- For the PFKL data: can the original authors provide biological-replicate labels for the 1,691 tracks, or is the track-level structure the only level available?
- For the haptotaxis data: how many independent experimental blocks (e.g., separate microfluidic devices, imaging sessions, or cell passages) underlie the 131 tracks, and how many tracks per block?