# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a solid, well-executed manufacturing and process development study for a clinical-stage HIV vaccine candidate. The quantitative work is competent and appropriately scaled to the claims. The paper documents a real translation from bench to cGMP with credible evidence of reproducibility and quality control. The statistical and analytical reporting is generally sound, though some quantitative claims lack the precision expected in a peer-reviewed venue, and a few key comparisons rest on single measurements or small sample sizes where replication would strengthen the conclusions. The work is suitable for publication with minor revision to clarify the statistical basis of several headline results.

## Strengths

1. **Reproducibility across scales and cell banks**: The authors demonstrate consistent productivity and quality metrics across three independent 50 L runs (RCB, MCB demonstration, MCB GMP) with reported VCC, viability, and titer values that track closely, lending credibility to the scalability claim.

2. **Orthogonal analytical methods for glycosylation**: Two independent mass spectrometry approaches (DeGlyPHER and LC-MS glycoproteomics) are used to characterize site-specific glycan occupancy, with results cross-validated and discrepancies acknowledged (e.g., N625 occupancy estimates differing between methods).

3. **Comprehensive viral clearance with stated model viruses and log reductions**: The study quantifies clearance for both enveloped (XMuLV) and non-enveloped (MMV) viruses across four unit operations, reports individual and cumulative log reductions with standard errors, and contextualizes results against industry benchmarks.

## Weaknesses: Load-Bearing Claims

**1. Clone productivity and quality ranking (Section 3.1.2–3.1.3): n and replication basis unclear.**

The paper claims clone C235 was selected as superior based on "growth characteristics, productivity, product quality and the presence of recombinant furin" (Section 3.1.3). However, the evidence presented is a single 14-day fed-batch run per clone (n=1 per clone, 24 clones screened). Figure 10 shows BG18 and PGT145 titers for each clone, but no statistical test, confidence interval, or replication is reported. The ranking criteria in Table 5 list "BG18/PGT145 detectable productivity ratio" and "efficiency of furin cleavage" but do not specify thresholds, weighting, or how ties were broken. Figure 11 (reduced SDS-PAGE) is qualitative and shows only presence/absence of bands, not quantified furin cleavage efficiency. The claim that C235 is "superior" rests on visual inspection of single runs. What would distinguish C235 from the next-best clone? Reporting the titer range, the ranking score for the top 5 clones, and whether a second run on the top 3 candidates would confirm the ranking would resolve this.

**2. Ambr250 process optimization: reference standard drift and titer comparisons across conditions.**

Figure 13 reports Day 14 BLI titers (mg/L) for 12 Ambr250 conditions, with Control + 7a bolus achieving 752 mg/L, compared to Control #1 (640 mg/L) and Control #2 (650 mg/L). The text states "the highest Day 14 titers were achieved with Control + 7a bolus (752 mg/L), High inoculation with 40% 7a bolus (721 mg/L), and 35% 7a bolus (715 mg/L)." However, no error bars, replicates per condition, or statistical test is reported. Section 3.2.3 later discloses that the 50 L RCB run used a different reference standard (IAVI/Scripps lot 19Apr0088) than the 50 L MCB demonstration run (KBI lot S-20210314-0001-SD2-E-M), and the GMP run used yet another (KBI lot P65), explicitly stating "absolute titers varied across runs (mainly due to different reference standards)." This undermines the claim that the Ambr250 optimization identified the best condition: if reference standards drift, the ranking of conditions in Figure 13 is potentially unreliable. Were the 12 Ambr250 runs assayed with the same reference standard? If not, were titers normalized to a common standard before comparison? If yes, report it; if no, the ranking is confounded by assay drift.

**3. Viral clearance: single-run study with no replication or sensitivity analysis.**

Table 12 reports log reductions (LRV) for XMuLV and MMV across four unit operations, with standard errors (e.g., XMuLV 2G12: 2.95 ± 0.57 LRV). The text states "a viral clearance study was conducted using material from the cGMP run" (Section 2.6), implying n=1 cGMP batch. The standard errors suggest multiple replicates within that single batch (e.g., replicate spikes or assay replicates), but the manuscript does not state how many independent spike experiments were performed per unit operation, whether spikes were done in parallel or series, or whether the same viral stock was used throughout. The claim that "the N332-GT5 gp140 purification unit operations can effectively achieve the target viral clearance" (Section 3.5) rests on a single manufacturing run. Reporting the number of independent spike replicates per unit operation and whether the study was repeated on a second batch would clarify the robustness of the clearance claim.

## Weaknesses: Sweep

1. **Intermediate hold-time stability (Section 3.3.3, Figure 15)**: The criterion for instability is stated as "an intermediate was considered unstable if the % HMW or % LMW increased by more than 0.7%" but no justification for this threshold is given, and it is not clear whether this is a pre-specified acceptance criterion or a post-hoc choice based on observed data.

2. **Ambr250 peak VCC and viability (Table 6)**: Peak VCC ranges from 16.5 to 25.2 × 10⁶ cells/mL across 12 conditions, but no statistical test compares conditions, and the text does not state whether differences are meaningful or within assay variability.

3. **SE-HPLC and RP-HPLC purity (Tables 8–9)**: The final product is reported as ">99% trimeric purity" and "%Main Peak: 99.4%" (Table 11, GMP batch) but no confidence interval or measurement uncertainty is provided; a single measurement of a complex glycoprotein may not capture batch-to-batch or run-to-run variability.

4. **Negative-stain EM (Section 3.6.2)**: The paper states "6,086 particles analyzed" and "no other oligomeric states (dimers, monomers) were observed," but does not report the fraction of particles classified as trimers, the inter-rater or algorithmic reliability of the 2D classification, or whether the 82 micrographs are independent replicates or a single grid.

5. **Residual impurity limits of quantification (LOQ)**: Multiple assays report "<LOQ" (e.g., Table 9, resProA <LOQ in several intermediates) but the LOQ values are not consistently stated in the methods or results, making it impossible to assess whether the final product truly meets specifications or is simply below detection.

6. **Feasibility run robustness cycles (Table 7)**: Three robustness conditions are tested for 2G12 capture (centerpoint, WCPQ, WCY) but only one or two cycles per condition are shown; the text does not state whether these are independent replicates or technical replicates of the same preparation.

7. **BLI relative potency (Table 9)**: Relative potency is reported as "100%" for the preparative SEC eluate (defined as reference) but no confidence interval or assay variability is given for the other intermediates, and the basis for the 15% acceptance criterion for hold-time stability (Section 2.5.3) is not justified.

8. **Harvest yield calculation (Section 3.2.3)**: The 50 L RCB run reports "approximately 57.7 kg of clarified harvest was recovered at 399 mg/L, corresponding to a harvest yield of 91.4%." The denominator for this yield is not explicitly stated; if it is the Day 14 bioreactor titer (562 mg/L) multiplied by bioreactor volume, the calculation should be shown to verify the 91.4% figure.

## Questions

1. **Clone ranking (Section 3.1.3)**: Were the top 5 clones re-tested in a second independent 14-day fed-batch run to confirm the ranking, or was C235 selected based on a single run per clone?

2. **Ambr250 reference standard (Figure 13)**: Were all 12 Ambr250 conditions assayed with the same BLI reference standard, or were titers normalized post-hoc to account for standard drift?

3. **Viral clearance replication (Table 12)**: How many independent spike experiments (not assay replicates) were performed per unit operation, and was the study repeated on a second cGMP batch?

4. **Hold-time stability threshold (Section 3.3.3)**: Was the 0.7% HMW/LMW change criterion pre-specified before data collection, or determined post-hoc from the observed data?

5. **EM particle classification (Section 3.6.2)**: What fraction of the 6,086 particles were classified as trimers vs. other oligomeric states, and what is the inter-rater or algorithmic agreement for the 2D classification?

---

## Technical Notes for Other Reviewers

- **Bioprocess engineering**: The upstream process optimization (Ambr250 → 50 L scale-up) and downstream purification (2G12 capture, MabSelect SuRe, Capto adhere, viral filtration) follow established CHO cell and protein A chromatography platforms; the novelty is in the application to N332-GT5 rather than the methods themselves. The process is well-documented and appears reproducible.

- **Glycosylation analysis**: The two mass spectrometry methods are complementary and well-chosen; the discrepancy in N625 occupancy (50% by DeGlyPHER, <50% by LC-MS) is acknowledged and likely reflects the different information content of the two approaches (occupancy vs. glycoform identity). This is appropriate candor.

- **Regulatory context**: The paper is framed as supporting a Phase 1 clinical trial (HVTN144) and cites cGMP compliance; however, the manuscript does not provide a formal cGMP batch record, stability data, or regulatory filing summaries. This is appropriate for a research publication but limits independent verification of GMP compliance claims.