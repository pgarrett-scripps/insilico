# Clarity & Presentation Reviewer

SCORE: 4  
CONFIDENCE: 4  

## Summary

This is a well-organized, unusually detailed process-development manuscript describing the full path from CHO cell-line engineering through cGMP manufacture of the N332-GT5 gp140 HIV immunogen for the HVTN144 trial. The writing is dense but generally clear, and the authors are commendably explicit about process decisions, deviations, and the rationale for each. My remit is clarity and presentation; on that dimension the manuscript is largely successful, with a handful of specific ambiguities that a careful reader would stumble on. The central claim — that a scalable, reproducible, clinical-grade process was established — is stated explicitly and supported by the evidence presented, though some quantitative comparisons are hard to follow because reference standards and assay versions shift between runs.

## Strengths

1. The process narrative is genuinely end-to-end and recoverable: a reader can reconstruct the order of operations from cell-line development through viral clearance without guessing.
2. The authors flag their own deviations (e.g., removal of preparative SEC, medium adaptation) with explicit rationale and supporting data, which is exemplary reporting practice.
3. The hold-time stability study is presented with clear, actionable recommendations tied to specific observed changes.

## Weaknesses

### Load-bearing

**1. Titer comparisons across runs are not interpretable as written because the reference standard changes mid-narrative.** In Section 3.2.3, the authors report Day 14 BLI titers of 562 mg/L (RCB run), 355 mg/L (MCB demonstration), and 390 mg/L (GMP run), then state that "the difference in titer was mainly due to the reference material used" — three different reference standards are named. A competent reader cannot determine whether the process is reproducible in absolute terms, because the measurement scale itself shifts. The claim that the process "scaled efficiently" and produced "consistent product quality" is supported by the growth and viability data, but the titer comparison as presented is not a comparison. What would settle it: report all three titers re-assayed against a single reference standard, or state explicitly that absolute titer comparability was not assessed and restrict the reproducibility claim to growth, viability, and product quality.

**2. The ">99% trimeric purity" claim in the abstract is not traceable to a single, consistently defined measurement.** The abstract states ">99% trimeric purity," but the SE-HPLC data in Table 11 report %Main Peak (98.6% pilot, 99.4% GMP), which is not the same as trimeric purity — %Main includes monomeric and other species that co-elute. The nsEM data (Section 3.6.2) report "nearly 100% native-like trimers," but this is a qualitative 2D-classification assessment of 6,086 particles, not a quantitative purity measurement. A reader cannot determine which measurement supports the abstract's ">99% trimeric purity" claim, or whether the claim refers to SE-HPLC %Main, nsEM particle classification, or something else. What would settle it: state explicitly which assay supports the abstract claim, or reword the abstract to match the specific measurements reported.

### Sweep

- **Figure 14 is referenced but its panels are not individually described in the text** — the caption lists (a) VCC, (b) viability, (c) BLI titer, but the text never tells the reader which panel supports which statement, and the three runs are plotted together without a legend key in the text description.
- **The term "detectable productivity" is used throughout Section 3.1 without ever being defined** — it appears to mean BLI-measured titer using a specific antibody, but the reader must infer this from context.
- **Table 6 lists "High inoc, 40% 7a slow, 34C Day 5" with a peak VCC of 25.2 but the text says the same condition reached 25.2 on Day 6** — the table gives only the value, not the day, and the text gives the day for this condition but not for others, making cross-condition comparison of peak timing impossible.
- **Section 3.3.1 reports ">100% yield for 2G12 step" in Figure 16 but the text attributes this to "titer assay variability" without quantifying the discrepancy** — a reader cannot tell whether this is 101% or 150%, which matters for assessing whether the step-yield calculation is meaningful.
- **The term "WCPQ" and "WCY" appear in Tables 3, 7, 8, and 9 without expansion** — these are presumably "worst-case product quality" and "worst-case yield" but are never defined at first use.
- **Section 2.5.4.3 states the Triton X-100 inactivation is "quenched by loading onto a pre-equilibrated Amberlite adsorption resin"** — "quenched" is the wrong verb for an adsorption step; the reader must infer that quenching means removal by adsorption, not chemical neutralization.
- **The abstract's "exceeded 18-log and 11-log reductions" is clear, but the viral clearance section does not state whether these values are additive across steps or measured independently** — Table 12 shows individual step LRVs and an "Overall" row, but the text never explains that the overall is a sum, which a non-specialist reader might misread as a single-step measurement.

## Questions

1. Can the three production-run titers be re-reported against a single reference standard, or is absolute titer comparability explicitly out of scope for the reproducibility claim?
2. Which specific assay supports the abstract's ">99% trimeric purity" — SE-HPLC %Main, nsEM classification, or a combination?
3. What do "WCPQ" and "WCY" stand for at first use in Table 3?