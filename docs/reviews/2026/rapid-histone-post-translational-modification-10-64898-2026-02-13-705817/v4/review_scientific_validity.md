# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a methodologically sound comparative study of protease and labeling strategies for histone PTM analysis that makes three load-bearing claims: (1) Arg-C Ultra with TMT labeling detects more total PTMs than Trypsin+propionylation; (2) TMT's tertiary amine rescues ionization of negatively charged acylations (succinylation, glutarylation) through charge compensation; (3) a dual-protease workflow (RIPUP) enables rapid, comprehensive histone PTM profiling. The first claim is well-supported by direct comparison. The second rests on a mechanistic explanation that is plausible but not directly tested. The third is demonstrated in proof-of-concept but not validated against ground truth. The work is honest about limitations, provides sufficient detail for reproduction, and makes a genuine contribution to an established field, but stops short of the experimental evidence needed to fully license its mechanistic claims.

## Strengths

1. Systematic design comparing 10 distinct conditions across three proteases with consistent metrics (CVs, sequence coverage, labeling efficiency, PTM diversity), providing a fair empirical foundation for protease selection.

2. Transparent reporting of labeling efficiency by two complementary metrics (site count and intensity-weighted), revealing that propionylation achieves only 29–71% efficiency while TMT reaches ~92–99%, a quantitative gap that directly explains downstream differences.

3. Honest acknowledgment of scope limitations (single cell line for main comparisons, no synthetic validation of succinylation/glutarylation sites, inability to distinguish endogenous from artifact propionylation) and clear statement of what would strengthen the findings.

## Weaknesses: Load-bearing claims

**Claim 1: TMT labeling rescues ionization of negatively charged acylations through charge compensation by the tertiary amine.**

The authors propose a mechanistic explanation: TMT's tertiary amine sequesters a mobile proton at the N-terminus, shifting fragmentation toward b-ions and improving PTM localization confidence for acidic modifications (Figure 3, text p. 17). The evidence is correlational: TMT-labeled peptides show 58 succinylation and 31 glutarylation sites versus near-zero in propionylated samples, and Figure 6 shows representative spectra with continuous b/y-ion series flanking succinyl-K. However, three alternative explanations remain unexcluded: (i) improved ionization efficiency of succinylated peptides under TMT labeling could arise from the hydrophobicity and polarity of the TMT moiety itself, independent of proton sequestration; (ii) the higher labeling efficiency of TMT (99% vs. 68% for propionylation) means more peptides carry the label, and the benefit could be purely statistical—more labeled substrate simply yields more detections—rather than mechanistic charge compensation; (iii) the authors do not report whether unlabeled Arg-C Ultra peptides (which retain free N-terminal amines) also show enhanced succinylation detection relative to propionylated samples, which would directly test whether charge at the N-terminus, rather than the specific TMT structure, drives the effect. To distinguish the authors' mechanism from these alternatives: report succinylation/glutarylation site counts for unlabeled Arg-C Ultra and r-Chymotrypsin (already in the dataset, Figure 5A), and compare to TMT-labeled and propionylated versions. If charge compensation is the driver, unlabeled peptides should show intermediate or high succinylation detection; if the TMT structure itself is essential, unlabeled should remain low.

**Claim 2: Arg-C Ultra with TMT labeling achieves detection of total PTM that exceeds Trypsin-based approaches.**

The authors report that "Arg-C Ultra with TMT labeling achieves a detection of total PTM that exceeds Trypsin-based approaches" (Abstract). The evidence is Figure 5A, which shows ~120 unique PTM sites for both Arg-C Ultra+TMT and Trypsin+Prop, with the difference not visually or statistically distinguished. The text states "TMT-labeled peptides from Arg-C Ultra and r-Chymotrypsin digestion achieved comparable PTM numbers to conventional 'Trypsin + Prop' methods (~120 PTMs)" (p. 15), which contradicts the Abstract claim of exceeding Trypsin. The Abstract also claims "58 succinylation and 31 glutarylation sites – a 'dark epigenome' largely undetected by propionylation-based methods," but these are detected in TMT-labeled Arg-C Ultra and r-Chymotrypsin samples, not Arg-C Ultra alone. The claim as stated conflates two separate findings: (i) Arg-C Ultra outperforms Trypsin in total peptide identifications and digestion efficiency (true, Figure 2C), and (ii) TMT labeling enables detection of acidic acylations (true, Figure 5B). But the Abstract implies Arg-C Ultra+TMT exceeds Trypsin+Prop in total PTM count, which the data do not show. Reword to: "Arg-C Ultra with TMT labeling achieves comparable total PTM detection to Trypsin+Prop (~120 sites) while uniquely enabling detection of succinylation and glutarylation" or provide a count showing Arg-C Ultra+TMT > Trypsin+Prop.

**Claim 3: RIPUP enables detection of >200 PTMs in rat hippocampal tissue within 3 hours.**

The authors report "Application of RIPUP to frozen-thawed rat hippocampal sections within a 3-hour workflow identified >200 PTMs" (Abstract) and "Combined, both enzymes detected 231 unique PTM sites" (p. 20). This is presented as a proof-of-concept, but no ground truth or orthogonal validation is provided. The 231 sites are identified from n=5 animals with detection threshold ≥2 replicates (Methods, p. 19), which is a low bar for a tissue sample where biological and technical variation are both present. The authors acknowledge this is "proof-of-principle" (p. 20) but do not report: (i) how many of these 231 sites are detected in all 5 animals versus only 2–3; (ii) whether the same sites are recovered by both Arg-C Ultra and r-Chymotrypsin (orthogonal validation); (iii) comparison to a published histone PTM map from rat brain or hippocampus, if one exists. The claim that RIPUP "identifies" these sites is supported; the claim that this represents a comprehensive or validated landscape is not. Restrict the claim to "detected 231 unique PTM sites across n=5 animals" and report the distribution of detection frequency (all 5 vs. 2–3 replicates) and the overlap between proteases.

## Weaknesses: Sweep

1. The quantitative NAM experiment (Figure 7) uses histone-level normalization to correct for loading, but does not report whether the same 112 significant peptidoforms are detected in all three dose groups or whether some are dose-exclusive, which would affect the validity of the limma model and the interpretation of fold-changes.

2. The authors claim TMT labeling efficiency is ~92–99% by site count and ~99% by intensity, but do not report the absolute number of labeled vs. unlabeled sites per peptide or whether efficiency varies by histone type, which could bias PTM detection toward certain proteins.

3. Missed cleavage motif analysis (SI Figures S6–S7) identifies enrichment of modifiable sites (K/R/STY) and basic residues near missed cleavage sites, but does not test whether this is specific to histones or a general property of these proteases, limiting the mechanistic insight.

4. The paper does not report whether the 58 succinylation and 31 glutarylation sites overlap between Arg-C Ultra and r-Chymotrypsin digests, which would strengthen the claim that these are genuine biological modifications rather than artifacts of one digestion strategy.

5. Figure 2D shows H3 sequence coverage is only ~10–20% with r-Chymotrypsin, yet the authors claim r-Chymotrypsin provides "complementary coverage"; this is true for H2A and H1, but the low H3 coverage limits the practical complementarity for one of the most heavily modified histones.

6. The authors use 1% FDR at PSM and peptide levels but do not report the number of PSMs or peptides passing FDR filtering, making it impossible to assess whether the PTM identifications are driven by high-confidence matches or marginal hits.

7. The cost analysis (SI Table S5) claims RIPUP reduces per-sample cost to ~$9 (unlabeled) or ~$16 (TMT), but does not account for instrument time, which is often the dominant cost in high-throughput workflows.

8. The paper does not discuss whether the enhanced detection of succinylation and glutarylation with TMT is reproducible in other cell types or tissues, limiting generalizability of the "dark epigenome" claim.

## Questions

1. For the unlabeled Arg-C Ultra and r-Chymotrypsin samples (Figure 5A), what are the succinylation and glutarylation site counts, and how do they compare to TMT-labeled and propionylated versions?

2. In the NAM quantitative experiment, how many of the 112 significant peptidoforms are detected in all three dose groups versus only 2 of 3, and does this affect the statistical model or interpretation?

3. For the rat hippocampal RIPUP analysis, what is the distribution of detection frequency across the 231 PTM sites (all 5 animals vs. 2–3 replicates), and how many sites are detected by both Arg-C Ultra and r-Chymotrypsin?

4. Can the authors provide the absolute number of PSMs and peptides passing 1% FDR filtering, stratified by condition, to assess the confidence of the PTM identifications?