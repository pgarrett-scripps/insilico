# Rigor & Overclaiming Reviewer

SCORE: 3  
CONFIDENCE: 4  

## Summary

This is a process-development and manufacturing manuscript describing the scale-up and cGMP production of the N332-GT5 gp140 HIV vaccine candidate. The core claims are: (1) a stable, high-titer CHO clone was developed and scaled reproducibly; (2) a three-step purification yields >99% trimeric purity with preserved structure and antigenicity; (3) the process meets regulatory standards for viral clearance and impurity removal; and (4) the resulting material has been administered in HVTN144. The manuscript is generally careful in its wording, and the evidence is substantial. However, several load-bearing claims outrun the data presented, particularly regarding reproducibility, the removal of the preparative SEC step, and the significance of the glycan occupancy results. The work is sound and useful, but the claims need tightening.

## Strengths

1. The manuscript honestly reports process variability (e.g., step-yield differences between runs) rather than presenting only best-case data.
2. The hold-time stability study is a thoughtful, practical addition that directly supports manufacturing decision-making.
3. The viral clearance data substantially exceed industry benchmarks and are presented with appropriate caveats about model viruses.

## Weaknesses

### Load-bearing

**1. Claim: "The manufacturing process scaled efficiently from Ambr® 250 miniature bioreactors to 200-L single-use systems, delivering consistent product quality across multiple cGMP batches."**  
The evidence is two pilot-scale runs (one RCB/XDR-50, one MCB/XDR-200) plus one GMP run. The BLI titers differ substantially across these runs (562, 355, and 390 mg/L), and the authors attribute this to different reference standards. That is a plausible explanation, but it means the "consistent product quality" claim rests on comparability of *quality attributes* (SE-HPLC, residual impurities), not on titer consistency. The quality data are presented for only the pilot and GMP runs (Table 11), not for the material-supply run. The claim of "multiple cGMP batches" is also overstated — the text describes one GMP batch. The claim should be requalified to "consistent product quality across pilot and GMP scale" and the titer discrepancy addressed head-on, ideally with a re-assay of all three harvests against a single reference standard.

**2. Claim: "A streamlined three-step purification strategy—affinity capture, multimodal polishing, and viral clearance—yielded >99% trimeric purity with preserved quaternary structure and native-like antigenicity."**  
The "three-step" description is misleading: the actual process includes 2G12 capture, UF/DF1, detergent inactivation, Amberlite adsorption, MabSelect SuRe, Capto adhere, virus filtration, and UF/DF2 — eight unit operations. The claim also rests on the removal of the preparative SEC step, which was justified by a single small-scale study (Table 10) comparing two executions. The study shows comparable SE-HPLC and residual HCP, but the sample size is n=1 per condition, and the study was performed on demonstration-run material, not on the actual GMP load. The claim that the process "yielded >99% trimeric purity" is supported for the pilot and GMP runs, but the "three-step" framing and the SEC-removal justification are both over-strong as worded.

**3. Claim: "Orthogonal LC-MS analyses confirmed site-specific glycan occupancy matching design specifications."**  
The two methods (DeGlyPHER and traditional LC-MS glycoproteomics) show substantial disagreement at several sites. For example, DeGlyPHER reports N625 as ~50% unoccupied, while the traditional method reports it as predominantly occupied. The authors acknowledge this discrepancy in the text but then conclude "high glycan occupancy at most sites," which is defensible. However, the phrase "matching design specifications" is unsupported — no design specification for glycan occupancy is stated anywhere in the manuscript. What is the target? If the design intent was full occupancy at all 27 PNGS, then the data show that intent was not met at N625 and partially not met at four other sites. The claim should be requalified to "site-specific glycan occupancy was characterized and is consistent with a native-like trimer profile," with the N625 discrepancy discussed as a potential product-quality attribute rather than a confirmed match to specification.

### Sweep

- The claim ">18-log and >11-log reductions for model retroviruses" is presented as a single summed value; the authors should state explicitly that this is a cumulative estimate across orthogonal steps, not a validated single-step clearance, and that the summation assumes independence.
- The "genetic stability through 60 population doublings" claim is supported only by productivity and transcript-sequence data; the authors should state whether copy-number stability was assessed at PD60 or only at the RCB stage.
- The statement that "clinical material manufactured through this platform has been successfully administered in HVTN144" is a factual claim about an ongoing trial; the authors should clarify whether this refers to the specific batch described here or to material from the same process, and whether any immunogenicity or safety data from that trial are available to cite.
- The negative-stain EM claim of "nearly 100% native-like trimers" is based on 2D class averages from 6,086 particles; the authors should report the proportion of particles that did not classify as trimers, rather than only showing representative classes.
- The ">99% trimeric purity" claim in the abstract is supported by SE-HPLC %Main Peak data, but the RP-HPLC %Main values are lower (not reported in Table 11); the authors should clarify which method supports the headline number.
- The claim that the process "maintains structural conformity" is supported only by nsEM and BLI binding; no high-resolution structure (cryo-EM) of the GMP material is presented, so "structural conformity" should be hedged to "antigenic and gross structural integrity."

## Questions

1. Can the three harvests (RCB/XDR-50, MCB/XDR-200, GMP) be re-assayed for titer against a single reference standard to resolve whether the observed titer differences are assay-related or process-related?
2. What was the design specification for glycan occupancy, and how was it defined — was it based on the BG505 SOSIP profile, on the N332-GT5 preclinical material, or on a computational prediction?
3. For the SEC-removal study, was the final UF/DF execution performed at the same scale and with the same membrane lot as the GMP run, and was the GMP load material tested for HCP after the combined UF/DF step?
4. What proportion of particles in the nsEM analysis failed to classify as trimers, and were any non-trimeric classes (dimers, monomers, aggregates) observed at all?