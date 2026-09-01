# Ethics & Compliance Reviewer

SCORE: 4
CONFIDENCE: 5

## Summary

This is a well-executed process development and manufacturing manuscript describing the translation of a rationally designed HIV-1 envelope trimer (N332-GT5 gp140) from bench to cGMP production for a Phase 1 clinical trial (HVTN144). The work is sound, the compliance posture is transparent, and the contribution is genuine—establishing a reproducible platform for manufacturing structurally complex glycoprotein vaccines. The manuscript is appropriately scoped for a specialized audience and the evidence supports the claims made. No ethics or compliance concerns are identified.

## Compliance Assessment

**Human subjects and clinical trials:** The manuscript describes manufacturing of clinical material for HVTN144, a Phase 1 trial. The trial is registered (NCT05217641, cited). No human subject data, patient identifiers, or trial results are presented in this manuscript—it is a manufacturing and characterization study of the drug substance itself. No ethics approval statement is required for a manufacturing process paper; the trial approval is external and properly cited.

**Funding and competing interests:** Funding sources are clearly stated (NIH CHAVD, Gates Foundation). One author (WRS) is disclosed as an employee and shareholder of Moderna, Inc. This is appropriate transparency given the vaccine context. No other conflicts are declared, which is acceptable.

**Animal research:** No animal studies are presented. Preclinical rhesus macaque data are cited as published prior work (Steichen et al., 2024) motivating the clinical advance, not conducted here.

**Dual-use or biosafety risk:** Viral clearance studies use model retroviruses (XMuLV, MMV) in a controlled downstream purification context. This is standard pharmaceutical development practice and poses no biosafety concern as described.

**Data and materials:** Cell lines, plasmids, and reference materials are attributed to named sources (ATUM, IAVI/Scripps, KBI Biopharma). Sufficient detail is provided for process reproduction. No restricted-consent or biobank data are involved.

**Conclusion:** All required compliance statements are present and accurate. No hard or soft compliance issues identified.

---

## Strengths

1. The manuscript provides complete process lineage from cell line development through cGMP manufacturing with transparent reporting of scale-up parameters, intermediate hold-time stability, and robustness testing—enabling reproducibility and regulatory confidence.

2. Viral clearance data (≥18 logs for XMuLV, ≥11 logs for MMV) substantially exceed industry benchmarks and are supported by orthogonal unit operations with mechanistic detail (affinity capture, detergent inactivation, mixed-mode chromatography, nanofiltration).

3. Site-specific glycosylation is characterized by two complementary mass spectrometry methods (DeGlyPHER and LC-MS glycoproteomics), providing both occupancy and glycoform identity, with results cross-validated and aligned to design specifications.

## Weaknesses: Load-Bearing Claims

**Claim 1: The process scales reproducibly from bench to cGMP while maintaining product quality and structural integrity.**

The evidence rests on three data points: (i) Ambr®250 optimization (12 conditions, Figure 13), (ii) 50-L pilot runs (RCB in XDR-50, MCB in XDR-200), and (iii) 50-L GMP run (MCB in XDR-200). Cell growth kinetics and viability are comparable across scales (Figure 14). However, a confound exists: the reference standard used for BLI titer measurement differs between runs (IAVI/Scripps Lot 19Apr0088 for RCB; KBI Lot S-20210314-0001 for MCB; KBI Lot P65 for GMP). The authors acknowledge this ("mainly due to different reference standards") but do not quantify the impact. Absolute titers vary substantially (RCB 562 mg/L, MCB 355 mg/L, GMP 390 mg/L), and without a common reference or cross-calibration, it is unclear whether these differences reflect true process variation, reference drift, or both. This undermines the claim of reproducibility at the quantitative level. A reanalysis of all three runs using a single reference standard, or a cross-calibration table, would resolve this. As stated, the conclusion that "the process parameters were suitable for clinical manufacturing" rests partly on titers that may not be directly comparable.

**Claim 2: The downstream process achieves >99% trimeric purity with preserved quaternary structure and native-like antigenicity.**

SE-HPLC shows %Main >98.6% (pilot) and 99.4% (GMP) (Table 11), and nsEM confirms native-like trimers with no monomers or dimers observed (Figure 19, 6,086 particles analyzed). However, the nsEM analysis is qualitative—no quantitative occupancy or particle count is reported. The statement "nearly 100% native-like trimers" is inferred from the absence of other oligomeric states in the 2D classes shown, but the figure does not report what fraction of particles were classified, whether any were rejected as non-native, or the distribution of conformational states within the trimer class. BG18_GL0 BLI binding (116% of reference, pilot run; Table 11) is used as a proxy for antigenicity, but this is a single antibody and does not establish that the full quaternary epitope landscape is preserved. A quantitative nsEM occupancy analysis (percentage of particles in each oligomeric state) and binding to a panel of quaternary-dependent antibodies (e.g., PGT145, VRC34) would strengthen this claim. As written, the evidence supports high purity by size but does not fully establish quaternary integrity.

**Claim 3: Intermediate hold-time stability data confirm that the process produces product stable under manufacturing operations.**

The hold-time study (Figure 15, Table 4) tests SE-HPLC and relative potency at 15–25 °C and 2–8 °C for up to 7 days. A ≤1-day hold is recommended for UF/DF1 retentate due to a 3–4% increase in %HMW by Day 1. However, the criterion for instability is stated as ">0.7% change in HMW or LMW" (Section 3.3.3), yet the UF/DF1 retentate shows a 3–4% change and is flagged as unstable. This is internally consistent but the threshold itself is not justified—why 0.7%? Is this a regulatory standard, a process-specific choice, or a conservative estimate? The relative potency assay shows a "decreasing trend" over hold time but is deemed acceptable because it remains "within the target potency range"—yet no potency range is specified in the text. Without knowing the acceptance criteria, it is unclear whether the hold times are truly adequate or merely permissive. Specification of the potency range and justification of the 0.7% HMW/LMW threshold would clarify whether the stability data support the manufacturing timeline claimed.

## Weaknesses: Sweep

1. **Genetic stability qualification:** Clone C235 is tested at 60 population doublings (PD0, PD60±Gln) with productivity and transgene copy number as indicators (Section 2.3.8), but the results are not reported in the Results section—only the protocol is described. Confirmation that the clone meets stability criteria is absent from the narrative.

2. **Preparative SEC removal:** The decision to omit Superdex 200pg SEC from the cGMP process due to supply constraints (Section 3.3.2) is supported by a small parallel study (Table 10) showing comparable product quality and HCP clearance, but only one alternative execution is shown; a second replicate would strengthen the equivalence claim.

3. **Amberlite resin adsorption:** Residual Triton X-100 is reported as "below LOQ (<0.002%)" in final material (Table 9), but the LOQ itself is not stated numerically, making it impossible to assess whether clearance is adequate for clinical use.

4. **Furin cleavage completeness:** SDS-PAGE (Figures 8, 11) is used to assess furin cleavage, but no quantitative densitometry or mass spectrometry confirmation of cleavage efficiency is provided; the claim of "close to complete" is visual.

5. **Glycosylation occupancy discrepancy:** DeGlyPHER and LC-MS glycoproteomics show different occupancy at some sites (e.g., N625: 50% by DeGlyPHER, unoccupied by LC-MS; N611: 80–90% vs. absent), and the authors note "higher variation between analytical approaches" but do not resolve which is correct or why.

6. **Viral clearance model viruses:** XMuLV and MMV are used as surrogates for retroviruses and parvoviruses, but no justification is given for why these specific models are appropriate for CHO-derived product or whether they represent worst-case clearance scenarios.

7. **Reference material stability:** KBI Reference Material lots are used for BLI titer in pilot and GMP runs, but no stability or characterization data for these lots are provided, raising questions about whether titer drift contributed to the observed differences.

8. **Scope for In Silico journal:** This is a manufacturing and process development paper with no computational, theoretical, or in silico component; it is a solid experimental bioprocess study but may be outside the stated scope of In Silico (which emphasizes empirical, theoretical, computational, and methodological work). Confirm fit with the journal's editorial scope.

## Questions

1. **BLI titer reference standards (Section 3.2.3, Figure 14):** Can the authors provide a cross-calibration between the three reference standards used (IAVI/Scripps Lot 19Apr0088, KBI Lot S-20210314-0001, KBI Lot P65) or re-analyze all three runs using a single standard to establish whether the titer differences reflect true process variation?

2. **Genetic stability results (Section 2.3.8):** What were the productivity, transgene copy number, and mRNA identity outcomes for the PD60 stability cultures, and did they meet predefined acceptance criteria?

3. **Potency acceptance range (Section 3.3.3, Figure 15c):** What is the specified potency range for the bulk drug substance, and how was the 0.7% HMW/LMW change threshold selected?

4. **Glycosylation site occupancy (Section 3.6.1, Figures 17–18):** Which method (DeGlyPHER or LC-MS) is considered the reference for sites where occupancy differs (N625, N611, N185e), and what explains the discrepancy?

5. **nsEM quantitation (Section 3.6.2, Figure 19):** What percentage of the 6,086 particles analyzed were classified as native-like trimers, and were any rejected as non-native or misfolded?