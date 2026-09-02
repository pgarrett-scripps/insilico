# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript describes RIPUP, a multi-protease workflow for histone PTM analysis that reduces sample preparation time to ~3 hours while claiming to improve detection of acidic acylations through TMT labeling. The work is methodologically sound, reproducible in its essentials, and makes a genuine contribution to an established field. Data and code are deposited; protocols are detailed; and the central claims about TMT's charge-compensation advantage for succinylation/glutarylation detection are well-supported by the evidence presented. The quantitative experiment (NAM treatment) is appropriately designed and analyzed. Minor gaps in reproducibility and one unresolved alternative explanation prevent a higher score, but these do not undermine the core findings.

## Strengths

1. Complete data and code deposition (ProteomeXchange PXD073683, GitHub repository) with explicit FragPipe versions and search parameters (SI Table S1) enables end-to-end reconstruction of the proteomics pipeline.

2. The mechanistic explanation for TMT's advantage—tertiary amine sequestration of mobile protons during HCD fragmentation (Figure 3, mobile proton model)—is grounded in established fragmentation theory and directly tested through comparison of b-ion vs. y-ion series in succinylated peptides (Figure 6).

3. Dual-protease design with orthogonal sequence coverage (Arg-C Ultra for N-terminal tails, r-Chymotrypsin for H2A/H1 regions) is validated by explicit proteotypic coverage maps (Figure 2D, SI Figure S1) showing complementary rather than redundant coverage.

## Load-Bearing Weaknesses

**1. TMT's charge-compensation advantage for succinylation is demonstrated only in HEK293T cells; alternative explanations for enhanced detection are not excluded.**

The central claim is that TMT's tertiary amine rescues ionization of negatively charged acylations by providing charge compensation (Figure 3, text p. 17: "TMT tertiary amine sequesters a mobile proton at the N-terminal region"). The evidence is: (i) 58 succinylation and 31 glutarylation sites detected with TMT-Arg-C Ultra vs. fewer with propionylation (Figure 5B); (ii) representative MS/MS spectra showing continuous b-ion series flanking succinylated lysines (Figure 6); (iii) motif analysis showing succinylation enriched at first/second position K or near C-terminus (text p. 17). 

However, three alternative mechanisms could produce the same result without invoking charge compensation: (a) TMT's higher labeling efficiency (~99% by intensity, Figure 4A) could simply yield more total peptides, increasing the probability of detecting rare modifications by sampling alone; (b) TMT's earlier retention time (Figure 3A–B) could reduce co-elution and improve peptide-level signal-to-noise for acidic peptides without changing ionization efficiency; (c) the stepped collision energy protocol (30%, 40%, 50% NCE) used for TMT but not propionylated samples (text, LC-MS/MS section) could independently enhance b-ion generation regardless of the label. 

To distinguish the charge-compensation mechanism from sampling/chromatography/collision-energy effects: report the same succinylation count for propionylated Arg-C Ultra digests analyzed with stepped NCE (30/40/50) instead of fixed 30% NCE, and for TMT-labeled samples with fixed 30% NCE. If charge compensation is the driver, TMT should retain its advantage even with fixed energy; if stepped NCE or labeling efficiency dominates, the advantage should shrink. The current design does not isolate the mechanism.

**2. Quantitative analysis of NAM-treated samples uses histone-level normalization rather than peptide-family normalization, justified by NAM-induced missed-cleavage redistribution; this choice is not validated against the standard approach.**

The authors state (text p. 18, Results section): "Conventional peptide-family ratio and site-occupancy approaches were unsuitable because NAM induced dose-dependent missed cleavage redistribution in Arg-C Ultra digests, evidenced by 259 peptidoforms detected exclusively in NAM-treated samples." They then normalize by histone-level intensity and test for differential abundance of individual peptidoforms (Figure 7A–B).

The problem: if missed-cleavage redistribution is real and dose-dependent, it will create spurious peptidoforms (different backbone lengths of the same modification site) that appear to increase with NAM dose simply because cleavage efficiency changed, not because the PTM abundance changed. The histone-level normalization corrects for loading but does not remove this backbone-redistribution signal. The authors acknowledge this for r-Chymotrypsin (text p. 18: "12 of these were unmodified peptidoforms reflecting backbone redistribution"), but do not report how many of the 112 significant Arg-C Ultra peptidoforms (Figure 7A) are unmodified backbone variants vs. modified peptidoforms. 

To validate: stratify the 112 significant peptidoforms into modified vs. unmodified, and report the count of each. If the majority are unmodified, the quantitative result is confounded by cleavage redistribution rather than true PTM changes. Alternatively, restrict quantitative analysis to peptidoforms detected in all three dose groups (0, 3, 10 mM NAM) before imputation, which would exclude backbone variants appearing only in treated samples.

**3. Labeling efficiency for propionylation is measured only for post-digestion derivatization; pre-digestion propionylation of Trypsin samples cannot be directly assessed, making the comparison in Figure 4A potentially biased.**

The authors state (text p. 13, Results section): "Trypsin cleavage at non-propionylated K resulted in the loss of ~58% of peptides (considering fully cleaved peptides) with 'Trypsin + Prop', which also prohibits the direct assessment of propionylation efficiency for Trypsin-digested samples (Figure S1F)." They then compare propionylation efficiency for Arg-C Ultra and r-Chymotrypsin (post-digestion only) to TMT efficiency, but note in the Discussion (p. 19): "the ammonium-containing buffers in this protocol introduce competing amine reactivity that reduces labeling efficiency relative to optimized approaches."

The issue: Figure 4A presents propionylation efficiency for Arg-C Ultra (~68% by intensity) and r-Chymotrypsin (~33% by intensity) as representative of the propionylation method, but these are post-digestion derivatizations in 50 mM AMBIC. The Trypsin + propionylation workflow uses pre-digestion propionylation in 50 mM AMBIC (text, Methods), which is the same buffer, but the efficiency cannot be directly measured because unlabeled K residues are cleaved by Trypsin. This means the comparison in Figure 4A conflates two different propionylation protocols (pre- vs. post-digestion) and buffer conditions, and the reported efficiency for propionylation may not reflect what actually occurred in the Trypsin + Prop samples. The TMT efficiency is measured post-digestion in 100 mM TEAB, a different buffer. 

To resolve: either (i) measure post-digestion propionylation efficiency for Trypsin-digested samples by using a Trypsin cleavage specificity that includes K (as done in SI Figure S2F), or (ii) re-run Arg-C Ultra and r-Chymotrypsin propionylation in the same buffer and pre-digestion timing as Trypsin to make the comparison fair.

## Sweep

1. FragPipe version (v24.0) and HiP-Frag workflow parameters are specified, but the exact variable modification list and mass-offset thresholds are relegated to SI Table S1, which is not provided in the manuscript text—readers cannot verify the search space without accessing the supplement.

2. The rat hippocampus experiment (RIPUP proof-of-concept) uses n=5 animals but reports results as combined across all animals without per-animal replication counts; it is unclear whether each PTM site was detected in all 5 animals or only a subset, affecting confidence in the biological reproducibility claim.

3. Missed-cleavage motif analysis (SI Figures S6–S7) identifies enrichment of D at P1′ (Arg-C Ultra) and E at P2 (r-Chymotrypsin) but does not report statistical significance or effect sizes, making it unclear whether these are strong predictors or marginal associations.

4. The paper claims TMT labeling efficiency of ~99% by intensity (Figure 4A) but does not report the absolute number of labeled vs. unlabeled sites or the distribution across peptides—a single highly abundant peptide could drive the intensity metric while many low-abundance peptides remain unlabeled.

5. Endogenous propionylation and butyrylation are detected in unlabeled samples (text p. 15) but not quantified or distinguished from chemical artifacts; the extent to which these confound the unlabeled Arg-C Ultra and r-Chymotrypsin results is not addressed.

6. The HiP-Frag computational framework is applied with 1% FDR at PSM and peptide levels, but no orthogonal validation (synthetic peptides, targeted PRM, or independent MS method) is provided for the 58 succinylation and 31 glutarylation sites, which are the paper's headline discovery.

7. NAM treatment is performed at 3 mM and 10 mM doses for 18 hours; no dose-response curve or time-course is shown, so it is unclear whether these doses and timing are optimal or whether the observed changes plateau or continue at higher doses.

8. The paper states that r-Chymotrypsin is available "under the Early Access program (Promega)" and pricing has not been established (Discussion, p. 19), which may limit reproducibility and adoption until the reagent is commercially available.

## Questions

1. In Figure 5B, the count of succinylation sites detected with TMT-Arg-C Ultra (58) vs. propionylated Arg-C Ultra (appears to be ~5–10 from the figure) is striking; does this difference persist if both are analyzed with the same collision-energy protocol (stepped vs. fixed), and if not, what is the magnitude of the collision-energy effect alone?

2. For the 112 significant Arg-C Ultra peptidoforms in Figure 7A, how many carry a PTM (acetylation, methylation, etc.) vs. are unmodified backbone variants, and do the modified peptidoforms show the expected dose-response direction (increase with NAM for acetylation at sirtuin sites)?

3. SI Table S1 is referenced for variable modifications and mass offsets but is not included in the provided manuscript text; can this be confirmed as deposited in the ProteomeXchange repository or GitHub so readers can access it?