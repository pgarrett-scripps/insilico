# Contribution & Prior-Work Reviewer

Now let me check the reference list more carefully and search for specific citations that are central to the novelty claims.

Based on my systematic search of the prior-work literature, I can now write the contribution review. The searches confirm that the manuscript cites Ryzhaya et al. (2025) ref 10 and Vai et al. (2025) ref 20 as key recent works, and I found the manuscript itself in preprint form. Let me now assess the contribution claims.

---

SCORE: 4
CONFIDENCE: 4

## Summary

RIPUP is a methodological contribution that combines existing tools (Arg-C Ultra, r-Chymotrypsin, TMT labeling, HiP-Frag search) into a streamlined workflow and characterizes their comparative performance on histone PTM analysis. The central novelty claim—that TMT's tertiary amine rescues ionization of negatively charged acylations (succinylation, glutarylation)—is mechanistically plausible and supported by empirical observation, but the manuscript does not isolate this mechanism from simpler explanations. The work is sound, well-executed, and practically useful, but the core contribution is narrower than framed: it is primarily a systematic comparison and application of existing methods rather than a fundamental discovery about PTM detection or ionization chemistry.

## Strengths

1. Comprehensive and rigorous systematic comparison across 10 conditions and 40 samples with robust technical replication (median CVs <5%), providing a rare head-to-head evaluation of proteases and labeling strategies in a single controlled study.

2. Clear mechanistic hypothesis linking TMT's tertiary amine to enhanced b-ion formation and charge compensation for acidic PTMs, supported by fragmentation pattern analysis and consistent with the mobile proton model.

3. Practical workflow (RIPUP) reduces sample preparation to 3 hours while maintaining or exceeding PTM coverage of the 18-year-old propionylation standard, with data and code deposited for reproducibility.

## Weaknesses: Load-Bearing Claims

**1. TMT charge compensation mechanism for succinylation/glutarylation detection**

The manuscript claims that TMT's tertiary amine "rescues ionization" of succinylated peptides by providing charge compensation (Figure 3, Results section on succinylation). The evidence is: (i) TMT-labeled samples detect 58 succinylation and 31 glutarylation sites versus ~0–5 in propionylated samples; (ii) propionylation neutralizes lysine charge (+1 to 0) while TMT's tertiary amine retains a protonation site; (iii) fragmentation patterns show enhanced b-ions in TMT samples. However, this does not isolate the mechanism from a simpler alternative: TMT's much larger mass (+229 Da vs +56 Da) and different hydrophobicity may simply improve chromatographic separation and ionization efficiency of all peptides, including those bearing acidic modifications, independent of charge compensation. The manuscript does not report: (a) whether succinylated peptides are preferentially enhanced relative to unmodified peptides in TMT vs. propionylated samples (a ratio that would support charge compensation); (b) whether the enhancement is specific to acidic PTMs or general across all PTM classes; or (c) a direct comparison of ionization efficiency (e.g., extracted ion current normalized to peptide abundance) for succinylated vs. unmodified peptides across labeling conditions. The claim that succinylation has been "systematically under-detected" rests on this mechanism being the primary driver, but the data are consistent with TMT simply being a better label for all peptides in this context.

**2. Arg-C Ultra superiority over Trypsin for histone PTM analysis**

The manuscript claims Arg-C Ultra "exceeds Trypsin-based approaches" in PTM detection (Abstract, Results). The evidence is: (i) Arg-C Ultra + TMT yields 416 fully cleaved peptides vs. 179 for Trypsin + Prop (Figure 2C, SI Figure S2C); (ii) Arg-C Ultra shows ~84% peptides with 0 missed cleavages vs. heterogeneous distribution for Trypsin. However, this comparison is confounded by labeling strategy: Arg-C Ultra is paired with TMT (post-digestion labeling only) while Trypsin is paired with propionylation (pre- and post-digestion). The manuscript acknowledges this in Methods ("We did not perform a direct comparison to Trypsin labeled with TMT for two reasons...") but then uses the Trypsin + Prop result as the benchmark throughout. A fair test would compare Arg-C Ultra + Prop to Trypsin + Prop, or both with TMT. The current comparison conflates protease choice with labeling chemistry, making it impossible to attribute the improvement to Arg-C Ultra itself. The manuscript does report Arg-C Ultra + Prop (254 peptides, Figure 2C), which is only marginally better than Trypsin + Prop (179), suggesting the protease advantage is modest when labeling is held constant.

**3. Novelty of dual-protease strategy and complementary coverage**

The manuscript presents the dual-protease approach (Arg-C Ultra + r-Chymotrypsin) as a key contribution, claiming orthogonal coverage of H2A variants, linker histones, and regions poorly represented by arginine-specific cleavage. However, the use of multiple proteases for improved sequence coverage is well-established in proteomics (refs 64–66 in the manuscript). The specific pairing of Arg-C Ultra and r-Chymotrypsin is new, but the principle is not. Moreover, the manuscript does not quantify the added value: it does not report how many PTM sites are uniquely detected by r-Chymotrypsin that would be missed by Arg-C Ultra alone, or vice versa. Figure 8 shows that both enzymes together detect 231 PTM sites in rat hippocampus, but does not break down the contribution of each. This makes it difficult to assess whether the dual-protease strategy is essential or merely incremental.

## Weaknesses: Sweep

1. **Ryzhaya et al. (2025, ref 10) is not adequately distinguished**: Ryzhaya also demonstrated Arg-C Ultra + peptide-level derivatization (TMA) reduces preparation time to 3–4 hours and improves coverage; the manuscript cites this but does not clearly state what RIPUP adds beyond Ryzhaya's work (TMT instead of TMA? Dual proteases? Application to tissue?).

2. **HiP-Frag computational framework is not novel to this work**: The manuscript applies Vai et al.'s (2025) HiP-Frag search strategy but does not develop or modify it; the succinylation/glutarylation findings are presented as a discovery but are a consequence of using HiP-Frag on TMT-labeled samples, not a methodological innovation.

3. **Quantitative experiment (NAM treatment) is limited in scope**: Only HEK293T cells are used; the claim that RIPUP is "suitable and sensitive" for quantification rests on a single cell-line experiment with a known sirtuin target (acetylation), which does not test the method's generalizability to other PTM classes or biological systems.

4. **Formylation is presented as a discovery but acknowledged as potentially artifactual**: The manuscript notes formylation is "prominent" in both HEK293T and rat hippocampal histones (Results) and cites prior work showing it can arise from sample preparation (ref 60), yet does not experimentally exclude this artifact or explain why it should be trusted as biological.

5. **Cost analysis (SI Table S5) is incomplete**: The manuscript claims RIPUP reduces per-sample cost from ~$25 to ~$9 (unlabeled) or ~$16 (TMT), but does not account for instrument time, researcher time beyond hands-on preparation, or the cost of r-Chymotrypsin, which is still under "Early Access" with unestablished pricing.

6. **Missed cleavage motif analysis (SI Figures S6–S7) is post-hoc and not integrated into the main narrative**: The finding that modifiable sites and acidic residues flank missed cleavages is interesting but presented without mechanistic explanation or validation in independent samples.

7. **Hippocampal tissue application is proof-of-concept only**: The manuscript applies RIPUP to rat hippocampus and identifies 231 PTM sites, but does not validate any of these findings against prior literature, synthetic standards, or orthogonal methods, limiting confidence in the biological relevance of the discoveries.

8. **Propionylation efficiency comparison may be unfair**: The manuscript notes that the Garcia et al. (2007) protocol uses ammonium-containing buffers that reduce labeling efficiency (Discussion), then compares against this suboptimal version rather than optimized propionylation protocols, potentially overstating TMT's advantage.

## Questions

1. **For the charge compensation claim**: Can the authors report the ratio of succinylated to unmodified peptide intensity (or extracted ion current) for the same peptide sequences across TMT, propionylation, and unlabeled conditions? This would directly test whether charge compensation is the mechanism or whether TMT simply improves ionization generally.

2. **For Arg-C Ultra superiority**: Can the authors provide a direct comparison of Arg-C Ultra + Prop vs. Trypsin + Prop (both with post-digestion labeling only) to isolate the protease effect from labeling chemistry?

3. **For dual-protease value**: Can the authors quantify how many of the 231 PTM sites in rat hippocampus are uniquely detected by r-Chymotrypsin vs. Arg-C Ultra, and how many are detected by both?

4. **For formylation**: Can the authors experimentally rule out formic acid artifact (e.g., by using alternative solvents or comparing to a formylation-free control) or cite evidence that formylation is biological in these samples?