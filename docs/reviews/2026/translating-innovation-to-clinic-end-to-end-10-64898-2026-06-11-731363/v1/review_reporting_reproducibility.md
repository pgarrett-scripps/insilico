# Reporting & Reproducibility Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript describes the development and cGMP manufacturing of N332-GT5 gp140, an HIV vaccine candidate now in first-in-human trials. The work is thorough in scope—spanning cell line development, upstream process optimization, downstream purification, and product characterization—and the clinical material has been successfully administered. However, critical procedural details necessary for independent reproduction are missing or scattered, particularly around data analysis pipelines, reference material traceability, and the mapping between analytical outputs and key claims about product quality. The paper reads as a detailed technical report of what was done rather than a reproducible research record.

## Strengths

1. The manuscript provides extensive process development data across multiple scales (Ambr250, 50L, 200L) with explicit parameter tables and growth/productivity curves that document the optimization path.

2. Viral clearance studies include two orthogonal model viruses with individual step LRV values and clear summation to total reduction, meeting stated industry benchmarks quantitatively.

3. Site-specific glycosylation is characterized by two complementary MS methods (DeGlyPHER and LC-MS glycoproteomics) with explicit mass signatures and occupancy thresholds, providing orthogonal validation of glycan processing.

## Major Weaknesses: Load-Bearing Claims

**1. Product purity and trimer identity claims rest on reference material whose provenance and stability are not fully specified.**

The central claim is that the final drug substance achieves ">99% trimeric purity with preserved quaternary structure and native-like antigenicity" (Abstract). This is supported by three independent readouts: SE-HPLC (% Main peak), BLI binding assays (PGT145 and BG18_GL0), and nsEM. However, the reference material used to calibrate these assays changes across the campaign without explicit justification or cross-validation.

- For the 50L RCB run (Section 3.2.3), titer was determined using "IAVI/Scripps N332-GT5 reference material, 1.0 mg/mL, Lot: 19Apr0088."
- For the 50L MCB demonstration run, titer used "KBI Reference Material lot # S-20210314-0001-SD2-E-M (derived from Process Feasibility Run #2)."
- For the 50L GMP run, titer used "KBI Reference Material lot # P65."

The authors acknowledge (Section 3.2.3) that "absolute titers varied across runs (mainly due to different reference standards)" but do not provide: (i) the characterization or certification of each reference lot; (ii) the stability data for these materials over the time window they were used; (iii) a cross-calibration study showing these lots agree within acceptable limits; or (iv) the rationale for switching reference materials mid-campaign. This matters because BLI titer directly feeds into the calculation of step yields (Figure 16), which in turn support claims about process robustness and consistency. If reference materials drifted or were not equivalent, the reported yields and the conclusion that "step yields were again comparable to small- and pilot-scale" (Section 3.4) cannot be verified.

**What would resolve this:** Provide the COA or characterization data for each reference lot (19Apr0088, S-20210314-0001-SD2-E-M, P65), including purity by SE-HPLC and RP-HPLC, and report a cross-validation study (e.g., BLI titer of a common sample measured against all three lots) showing agreement within ±10%.

---

**2. The claim that the process is "scalable and reproducible" relies on comparing runs that used different reference standards and different cell banks, making it unclear whether observed differences reflect process variation or analytical drift.**

Section 3.2.3 states: "Similar cell growth, metabolite behavior and BLI titers, along with high harvest yields in both runs, demonstrate that the process parameters were suitable for clinical manufacturing." However, the three runs (50L RCB, 50L MCB demonstration, 50L GMP) show:

- Day 14 BLI titers of 562 mg/L (RCB), 355 mg/L (MCB demo), and 390.2 mg/L (GMP).
- The authors attribute this variation to "different reference standards" but do not quantify the expected magnitude of this effect or show that it is the only source of variation.

More problematically, the RCB and MCB runs used different cell banks, and the RCB run used a different reference standard than the two MCB runs. This confounds cell bank effects with analytical effects. The statement that "studies demonstrated robust production and high recovery efficiency under the same feed and control strategy" is therefore not fully supported: the feed and control were the same, but the cell bank and reference material were not, and these variables were not orthogonally separated.

**What would resolve this:** Report a fourth run using MCB with the IAVI/Scripps reference standard (19Apr0088), or provide a cross-calibration showing the ratio of titers measured with 19Apr0088 vs. P65 on a common sample, so that the RCB titer can be normalized and compared on the same scale.

---

**3. The downstream process yield and impurity clearance data are presented as consistent across scales, but the removal of the preparative SEC step at cGMP scale introduces an uncontrolled change that undermines the claim of process equivalence.**

Section 3.3.2 describes an evaluation of removing preparative SEC due to "supply constraints" and "procurement challenges." The authors state: "Since the product quality (SE-HPLC and RP-HPLC) and residual HCP levels are comparable, Superdex 200pg chromatography unit operation was removed from the process for cGMP run."

However, Table 10 shows only a single comparison (one "Control" execution with SEC vs. one "Preparative SEC Removal" execution without SEC), and the table caption does not specify whether these were run in parallel on the same load material or on different batches. The "Control" row shows "Superdex 200pg Load" and "Flowthrough" with <LOQ HCP, but the "Preparative SEC Removal" row shows "Final UF/DF Load" and "Final Retentate" with <LOQ HCP. These are different intermediates, making it unclear whether the comparison is apples-to-apples.

More critically, Figure 16 and Table 11 present the cGMP batch results without preparative SEC and claim they are "comparable" to the pilot-scale demonstration run (which included SEC). But "comparable" is not quantified: what is the acceptable tolerance for % Main peak, % HMW, % LMW, and residual HCP between the two processes? If the cGMP batch had slightly higher % LMW or HCP, would that still be acceptable? The absence of pre-specified acceptance criteria makes it impossible to assess whether the removal of SEC was truly justified or whether it introduced an unacceptable change.

**What would resolve this:** (i) Clarify whether Table 10 compares parallel runs on the same load material; (ii) define the acceptance criteria for "comparable" (e.g., ±2% for % Main peak, ±0.5% for % HMW); (iii) report the full analytical profile (SE-HPLC, RP-HPLC, residual HCP, residual DNA, residual Protein A) for both the pilot-scale and cGMP batches side-by-side, with the acceptance criteria explicitly stated.

---

## Minor Weaknesses: Sweep

1. **Cell line genetic stability:** Section 3.1.2 states that clone C235 was selected based on "growth characteristics, productivity, product quality and the presence of recombinant furin," but the genetic stability data (Section 2.3.8) are mentioned only in the methods and not reported in the results; it is unclear whether the 60 population doubling study was actually completed and what the outcome was.

2. **Intermediate hold-time stability criteria:** Section 2.5.3 defines instability as ">0.7% change in HMW or LMW" and ">15% variation in relative potency," but these thresholds are not justified or referenced to regulatory guidance; it is unclear whether they are conservative, appropriate, or lenient.

3. **Viral clearance model virus selection:** The choice of XMuLV and MMV is not justified; no explanation is given for why these two viruses are representative of the viral contamination risk for CHO-derived products, or whether other model viruses (e.g., MuLV, XMRV) were considered and rejected.

4. **DeGlyPHER mass signature assignment:** Figure 17 shows glycan occupancy by DeGlyPHER, but the figure legend does not specify the threshold for calling a site "occupied" vs. "unoccupied" (e.g., is a site with 10% occupancy counted as occupied or unoccupied?); this affects the interpretation of sites like N625 (50% unoccupied).

5. **nsEM particle classification:** Section 3.6.2 states that "6,086 particles analyzed for native-like trimeric properties by comparison to previously published HIV Env SOSIP production runs," but does not specify the classification criteria (e.g., how many lobes, what aspect ratio, what size range) or report the number of particles rejected as non-trimeric; without this, the claim of "nearly 100% native-like trimers" cannot be verified.

6. **Ambr250 reference standard drift:** The BLI titer results in Figure 13 show absolute values (e.g., 752 mg/L for Control + 7a bolus), but the figure legend does not specify which reference standard was used for this assay; if the same reference standard was used for all 12 conditions, this is fine, but if different lots were used, the comparison is confounded.

7. **Downstream process intermediate stability:** Table 4 lists "equivalent intermediates" for hold-time testing (e.g., "UF/DF1 Load" is equivalent to "UF/DF1 Retentate"), but the criteria for equivalence (same buffer, pH, protein concentration) are not quantified; what tolerance is acceptable for pH or protein concentration to call two intermediates equivalent?

8. **cGMP batch manufacturing dates and conditions:** The manuscript does not report the calendar dates of the cGMP manufacturing run, the ambient temperature during hold times, or the actual hold times used (only the maximum allowed hold times are specified); without this, it is impossible to assess whether the hold-time stability data actually apply to the clinical material.

## Questions

1. **Reference material traceability:** Were the three reference lots (19Apr0088, S-20210314-0001-SD2-E-M, P65) all characterized by the same analytical methods (SE-HPLC, RP-HPLC, BLI), and if so, are the results available for cross-comparison?

2. **Preparative SEC removal justification:** In Table 10, were the "Control" and "Preparative SEC Removal" runs performed on the same load material (split into two parallel paths) or on different batches, and were they run on the same calendar date?

3. **Genetic stability completion:** Was the 60 population doubling study (Section 2.3.8) completed for clone C235, and if so, what were the results for transgene copy number and mRNA identity at PD0, PD60+Gln, and PD60-Gln?

4. **nsEM classification:** What were the specific morphological criteria used to classify particles as "native-like trimers" vs. other oligomeric states, and how many of the 6,086 particles were rejected as non-trimeric?

5. **Capto adhere worst-case yield:** Section 3.3.1 reports that Capto adhere yield dropped from ~60% (centerpoint) to ~24% (worst-case yield); was this worst-case condition actually used in the cGMP run, or were conditions adjusted to avoid it, and if so, what were the actual loading and pH conditions used?

---

## Assessment

This is a competent technical report of a complex manufacturing campaign, and the clinical material has been successfully used in a human trial, which is a strong signal that the process works. However, the manuscript does not meet the standard for reproducibility required by In Silico. The three load-bearing claims—product purity, process scalability, and downstream equivalence—all rest on comparisons that are confounded by changes in reference materials, cell banks, or process steps, and these confounds are not adequately controlled or disclosed. A reader cannot independently verify whether the reported improvements in yield or purity reflect genuine process optimization or analytical drift. The removal of preparative SEC at cGMP scale is presented as justified by a single small-scale comparison without pre-specified acceptance criteria, making it unclear whether this change was truly equivalent or whether it introduced unacceptable risk. These are not minor documentation issues; they are gaps in the logical chain that connects the evidence to the conclusion. The paper would benefit from a focused revision addressing the reference material traceability, the cross-validation of analytical methods across scales, and the explicit pre-specification of acceptance criteria for process equivalence.