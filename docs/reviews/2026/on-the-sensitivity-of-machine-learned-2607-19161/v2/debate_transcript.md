# Debate Transcript

## Advocate — round 1

The manuscript makes a genuine contribution by systematically comparing multivariate scoring rules against the CRPS standard for machine-learned weather forecasting. The core finding—that localized multivariate scores like the graph energy score achieve forecast skill comparable to CRPS—is robustly demonstrated in Figure 2, where all three experiments show nearly identical skill curves in the extratropics. This directly supports the claim that "multivariate scores are a viable alternative to CRPS-based training." The reviewers' concerns about statistical significance are valid but do not undermine the practical importance: the graph energy score performs at least as well as CRPS across most regions, establishing its viability. 

The scale-aware loss experiments (Section 4.2) provide valuable new evidence that explicit scale constraints improve spectral realism, a key physical diagnostic. Figures 3–14 clearly show that scale-aware formulations produce spectra closer to ERA5 than single-scale baselines. While the reviewers rightly note that weighting choices matter, the manuscript transparently acknowledges these are "ad hoc" and presents the multi-scale mechanism as a general framework applicable to any scoring rule—a methodological advance in itself.

The manuscript's strengths are its clear experimental design, thorough definition of novel scoring rules, and public implementation in Anemoi. These enable the field to build directly on this work. The identified weaknesses—mainly around statistical quantification and reproducibility—are addressable in revision through added uncertainty measures and code release.

**Key points:**
- The graph energy score achieves forecast skill comparable to CRPS, demonstrating multivariate scores are a viable alternative.
- Scale-aware losses demonstrably improve spectral realism, as shown in Figures 3–14.
- The work provides clear definitions and public implementations of novel scoring rules for the community.

## Skeptic — round 1

The manuscript's central claim—that multivariate scoring rules are a viable alternative to CRPS—is fundamentally undermined by methodological confounds. The forecast skill comparison (Section 4.1) FATALLY confounds scoring rule type with spatial weighting: the CRPS experiment uses pointwise scoring while the graph energy score includes localized neighbourhood aggregation. This means observed differences could stem from implicit spatial smoothing in the graph formulation rather than from multivariate scoring per se. The methodology reviewer correctly identifies this as "LOAD-BEARING": without controlling for spatial weighting, we cannot attribute performance differences to multivariate scoring.

Furthermore, the reproducibility reviewer notes a HARD failure: the custom scoring rule implementations are unavailable. Without code, we cannot verify that the graph energy score was implemented correctly or that differences aren't artifacts of implementation bugs. This makes the claimed "best" performance in the tropics unverifiable.

The abstract's framing around "scale-aware scoring rules" is misleading—the primary skill comparison uses non-scale-aware versions. This misrepresentation is FATAL to the paper's coherence: readers will expect evidence about scale-aware scoring that isn't actually presented in the main results.

While the spectral experiments show scale-awareness improves realism, the design FATALLY conflates scoring rule type with weighting schemes (Table 2), preventing attribution of effects to scoring rules themselves. The advocate's claim that "multivariate scores are a viable alternative" remains unproven because the experiments don't isolate multivariate scoring from confounding factors.

**Key points:**
- The forecast skill comparison fatally confounds scoring rule type with spatial weighting, preventing causal attribution
- Unavailable code makes the reported performance differences unverifiable (HARD reproducibility failure)
- The abstract misleadingly frames the work around scale-aware scoring rules when the primary skill comparison uses non-scale-aware versions
- Spectral experiments conflate scoring rule type with weighting schemes, preventing isolation of scoring rule effects