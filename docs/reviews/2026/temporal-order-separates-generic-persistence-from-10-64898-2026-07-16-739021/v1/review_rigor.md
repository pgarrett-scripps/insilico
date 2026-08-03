# Rigor & Overclaiming Reviewer

## Summary
The manuscript introduces a rigorous temporal-order framework that cleanly separates motility, generic persistence, and cue-aligned commitment across three distinct migration systems. Claims are well-matched to evidence, limitations are explicitly acknowledged (low replicate count in discovery, missing replicate labels in PFKL, cross-system confounding), and statistical safeguards are extensive. The work is sound, useful, and ready for publication.

## Strengths
- Analytical order-null and exact displacement-memory decomposition avoid permutation noise and guarantee algebraic closure, a major methodological advance over simulation-based nulls.
- Hierarchical bootstrap with simultaneous confidence bands, lag-invariant cohorts, and leave-one-FOV-out sensitivity protect against pseudoreplication and cohort drift — rare in migration analysis.
- Locked post-hoc robustness plans (HC3, propensity matching, overlap weighting, non-inferiority margins) for the PFKL analysis prevent HARKing and show directional effects survive speed/duration balancing.

## Weaknesses
- The MYO10–collagen discovery rests on only three biological repeats (R1–R3), with R3 noted as disproportionately large and phenotypically distinct; while hierarchical weighting and leave-one-FOV-out checks mitigate this, the inference remains limited to this specific experimental batch and cannot support broad generalizations about MYO10–collagen biology.
- PFKL track-level non-inferiority testing (0.10-SD margin) is explicitly not replicate-level inference because biological-replicate labels were lost in the public deposit; the paper honestly states this boundary, but readers may still overinterpret the 'preservation of generic serial order' as a biological conclusion rather than a track-level statistical statement.
- Cross-system comparison (HUVEC, MDA-MB-231, MDCK) confounds cell type, species, substrate, imaging interval, and tracking pipeline; the authors correctly treat this as descriptive transportability evidence, but the framing 'distinguished sustained, short-lived, and sign-reversing regimes' could be read as a biological taxonomy rather than a methodological demonstration.

## Questions
- For the MYO10–collagen experiment: could the 70% sequence-excess fraction be inflated by the drift-correction or FOV-level median-velocity subtraction, which might remove shared-flow contributions that also carry temporal order?
- In the haptotaxis reversal analysis, the 'transient reorganization of step order beyond the pseudo-event reference' is compared to matched pseudo-events from the same tracks — does this control for the fact that reversal detection itself selects for order changes, potentially biasing the contrast?