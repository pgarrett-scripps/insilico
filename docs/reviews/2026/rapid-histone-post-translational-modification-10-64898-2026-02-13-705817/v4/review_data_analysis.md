# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a methodologically sound comparative study of protease and labeling strategies for histone post-translational modification analysis. The quantitative claims are generally well-supported by appropriate statistical methods, and the authors transparently report their data handling and filtering criteria. The main contribution—that TMT labeling rescues detection of acidic acylations through charge compensation—is supported by the evidence presented, though the mechanistic explanation rests partly on inference rather than direct measurement. The work is suitable for publication with minor revisions to clarify a few statistical reporting gaps and one potential confound in the quantitative experiment.

## Strengths

1. **Transparent data handling and filtering**: The authors pre-specify their inclusion criteria (≥3 replicates for HEK293T, ≥2 for rat tissue; ≤1 missed cleavage; CV filtering) before reporting outcomes, and explicitly acknowledge the post-hoc nature of some comparisons (e.g., the Trypsin KR vs R cleavage specificity search in SI Figure S2F).

2. **Appropriate statistical framework for the primary quantitative experiment**: The NAM dose-response analysis uses histone-level normalization with limma moderated t-statistics and Benjamini-Hochberg correction, which is defensible for the peptidoform-level quantification problem and avoids the pseudo-replication trap of treating technical replicates as independent units.

3. **Complementary validation across two proteases and multiple conditions**: The dual-protease design with orthogonal sequence coverage provides built-in replication of PTM sites across different cleavage patterns, reducing the risk that a single protease artifact drives the reported PTM landscape.

---

## Major Weaknesses

### 1. Charge compensation mechanism for succinylation/glutarylation detection is inferred, not directly measured

The central novel finding is that TMT's tertiary amine "rescues ionization of succinylated peptides" by providing charge compensation (Figure 3, Results section "Enhanced identification of histone succinylation and glutarylation with TMT"). The authors argue that succinylation introduces a carboxylic acid that impairs positive-mode ESI via charge state reduction, and that TMT provides a compensating protonation site. However, this explanation is mechanistic inference rather than direct evidence. The manuscript reports the *outcome* (58 succinylation sites detected with TMT vs. far fewer with propionylation) but does not measure the intermediate claim: that succinylated peptides actually have lower charge states or ionization efficiency with propionylation than with TMT. 

To establish this, the authors would need to show: (1) extracted ion chromatograms or mass spectra of the same succinylated peptide under both labeling conditions, with explicit charge state distributions or ionization efficiency metrics; or (2) a synthetic or semi-synthetic succinylated histone peptide tested side-by-side under both conditions. Figure 6 shows annotated spectra for three succinylated peptides in TMT-labeled samples, but provides no propionylated counterpart for direct comparison. Without this, the charge compensation explanation is plausible but remains a post-hoc rationalization of the observed difference in detection frequency. The alternative—that TMT labeling simply improves chromatographic separation or MS/MS fragmentation efficiency for all peptides, and succinylated ones happen to benefit more—is not ruled out.

**What would settle this**: Report the precursor charge state distribution and/or MS1 peak intensity for at least one succinylated peptide in both TMT-labeled and propionylated forms, measured under identical LC-MS/MS conditions. Alternatively, synthesize or semi-synthesize a single succinylated histone peptide and measure its ionization efficiency and fragmentation pattern under both labeling schemes.

### 2. NAM-induced missed cleavage redistribution confounds the quantitative comparison between Arg-C Ultra and r-Chymotrypsin

The authors note that "NAM induced dose-dependent missed cleavage redistribution in Arg-C Ultra digests, evidenced by 259 peptidoforms detected exclusively in NAM-treated samples" (Results, "Quantitative analysis of histone peptides from RIPUP"). They justify their choice to quantify individual peptidoforms rather than peptide families by stating that "conventional peptide-family ratio and site-occupancy approaches were unsuitable because NAM induced dose-dependent missed cleavage redistribution." 

However, this creates a statistical problem: if the treatment (NAM) changes the distribution of cleavage states, then the set of observable peptidoforms changes with dose, and the quantitative comparison is no longer a simple test of PTM abundance—it is confounded by cleavage efficiency. The authors' solution (quantify all peptidoforms individually with histone-level normalization) is reasonable, but it means the reported fold-changes in Figure 7A and 7B are measuring a mixture of (1) true changes in PTM occupancy and (2) redistribution of the same PTM across different backbone lengths due to altered cleavage efficiency. The authors do not disentangle these. 

For example, if H3 K9ac/K23ac increases in abundance in NAM-treated samples, is this because K9 and K23 are more acetylated, or because NAM treatment reduces missed cleavages in that region, making the peptide more detectable? The motif analysis (SI Figures S6–S7) shows that D at P1′ and E at P2 are enriched near missed cleavage sites, suggesting that local charge environment affects cleavage. If NAM treatment alters histone charge (e.g., by increasing acetylation), it could secondarily alter cleavage efficiency independent of the PTM change being measured.

**What would settle this**: Restrict the quantitative analysis to peptidoforms with 0 missed cleavages only, and report the results separately for Arg-C Ultra and r-Chymotrypsin. This would isolate the true PTM changes from cleavage redistribution artifacts. If the sirtuin-target sites (H3 K9ac, H4 K16ac, etc.) still show the expected dose-dependent increase in this subset, the finding is robust to the confound.

---

## Minor Weaknesses

1. **Labeling efficiency metrics conflate site-level and intensity-weighted measures without justifying the choice**: Figure 4A reports both "by site count" and "by intensity" efficiency, but the text does not explain why intensity weighting is more informative than site count for the downstream claim that TMT enables better PTM detection. If a few highly abundant peptides drive the intensity-weighted efficiency, the practical benefit for rare PTMs may be overstated.

2. **Missing values imputation (kNN, k=10) is applied without sensitivity analysis**: The authors impute missing values in the NAM dose-response experiment using k-nearest neighbors with k=10, but do not report how many values were imputed, in which dose groups, or whether results are robust to alternative imputation methods (e.g., mean imputation, deletion). This is particularly important because they restrict imputation to cases with ≥2 measured replicates, which may introduce bias if missingness is non-random across dose groups.

3. **Coefficient of variation filtering is mentioned but not quantified**: The authors state that "CV filtering" was applied to ensure "high-confidence assignments" (Discussion, "Computational stringency enables large-scale PTM discovery") but do not report the CV threshold, how many peptidoforms were excluded, or whether the threshold was pre-specified or chosen post-hoc.

4. **Comparison of Arg-C Ultra and r-Chymotrypsin quantitative performance lacks a direct statistical test**: Figure 7B and 7D show dose-response correlations (r = 0.803 and r = 0.791, respectively) but do not test whether one protease is significantly more sensitive or reproducible than the other. A paired comparison of effect sizes or CVs for overlapping peptidoforms would strengthen the claim that both are suitable for quantification.

5. **Rat hippocampal analysis uses n=5 animals but does not report inter-animal variability**: The RIPUP proof-of-concept identifies 231 PTM sites across 5 rat hippocampi, but Figure 8 aggregates data without reporting how many sites were detected in all 5 animals vs. fewer replicates, or whether the PTM landscape is consistent across individuals. This limits confidence in the generalizability of the findings.

6. **FDR control at 1% PSM and peptide level is stated but not justified relative to the variable modification search space**: The authors apply 1% FDR but do not report the total number of PSMs searched, the size of the variable modification list (SI Table S1 is referenced but not summarized in the main text), or whether the FDR threshold is appropriate given the expanded search space of HiP-Frag. A larger search space typically requires more stringent FDR control.

7. **Propionylation efficiency comparison is biased by the choice of buffer**: The authors acknowledge that "ammonium-containing buffers in this protocol introduce competing amine reactivity that reduces labeling efficiency" (Discussion, "Labeling efficiency of propionic anhydride vs TMT"), but they do not test whether optimized propionylation buffers (e.g., TEAB instead of ammonium bicarbonate) would close the efficiency gap. The comparison in Figure 4A may overstate TMT's advantage.

8. **Succinylation and glutarylation sites are not validated orthogonally**: The authors note that "future studies could prioritize synthetic validation of the most abundant or biologically relevant succinylation and glutarylation sites" (Discussion, "Computational stringency enables large-scale PTM discovery"), but they do not provide even a single synthetic or semi-synthetic validation in the current work. The 58 succinylation and 31 glutarylation sites rest entirely on computational assignment without independent confirmation.

---

## Questions

1. **Figure 4A, labeling efficiency by intensity**: How many peptides contribute to the intensity-weighted efficiency calculation, and what is the distribution of intensities? If a small number of highly abundant peptides dominate, does the efficiency metric reflect the practical benefit for detecting rare PTMs?

2. **NAM dose-response experiment, missing data**: How many peptidoforms were imputed, in which dose groups, and what fraction of the 112 significant peptidoforms in Figure 7A contain imputed values? Are the results robust to complete-case analysis (deletion of peptidoforms with any missing values)?

3. **Rat hippocampal PTM landscape, inter-animal consistency**: Of the 231 unique PTM sites reported in Figure 8, how many were detected in all 5 animals, and how many in only 1 or 2 animals? Does the PTM landscape vary substantially across individuals?

---

## Technical Notes for Other Reviewers

- **Methods reviewer**: Verify that the histone extraction protocol (SI Methods) is consistent with the Garcia et al. 2007 standard and that the Arg-C Ultra and r-Chymotrypsin digestion conditions match manufacturer recommendations.
- **Proteomics reviewer**: Assess whether the HiP-Frag variable modification list (SI Table S1) is comprehensive and whether the 1% FDR threshold is appropriate for the expanded search space; also evaluate the biological plausibility of the 58 succinylation and 31 glutarylation sites against prior literature on histone acylation.
- **Cell biology reviewer**: Evaluate whether the NAM treatment (3 and 10 mM, 18 h) is appropriate for inducing global acetylation changes and whether the expected sirtuin targets (H3 K9ac, H4 K16ac) are indeed the primary responders.