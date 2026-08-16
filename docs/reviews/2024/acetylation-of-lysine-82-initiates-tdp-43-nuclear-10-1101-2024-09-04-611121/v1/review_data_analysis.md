# Statistics & Data-Analysis Reviewer

SCORE: 2
CONFIDENCE: 4

## Summary

This manuscript reports that partial proteasome inhibition causes TDP-43 mislocalization to the cytoplasm in human iPSC-derived cortical neurons, and identifies acetylation of lysine 82 within the TDP-43 cNLS as the key post-translational modification disrupting importin-α1 binding. The authors further report detection of K82-acetylated TDP-43 in sALS motor cortex but not controls. The central claims are biologically plausible and potentially important, but the quantitative evidence as presented is substantially under-specified. Several headline statistics lack stated tests, n's, or definitions of variability; the mass spectrometry experiment appears to lack replication; and the human tissue data are presented without statistical analysis despite the small sample sizes involved. The paper needs major revision to make its quantitative claims verifiable.

---

### Load-Bearing Weaknesses

**1. The TMT nuclear proteomics experiment (Fig. 1E-F) has no stated replication or statistical framework that supports the headline claim.** The volcano plot shows 5202 proteins with a 4-fold reduction in nuclear TDP-43, but the methods describe "three forward labelling groups and three reverse labelling groups" without stating whether these are biological replicates (independent neuronal differentiations) or technical replicates (aliquots of one differentiation). The P values are described as "unadjusted" and calculated with a one-sample Student's t-test, but the degrees of freedom are never stated. If the three forward/reverse pairs are technical replicates from a single differentiation, the n=3 is pseudo-replication and the p-value is meaningless for generalizing to neurons. The authors need to state the number of independent differentiations, and if it is one, the proteomics claim should be downgraded to a single observation. This matters because the entire paper's premise — that TDP-43 is *selectively* sensitive to proteasome inhibition — rests on this volcano plot.

**2. The sALS versus control comparison in Figure 5B is presented without any statistical analysis.** Six sALS and four control motor cortices are shown, with the claim that "ac-TDP-43(K82) was increased in immunoblotting of lysates of motor cortex in all (six of six) sALS patients tested, while no signal was detected in similar analyses of motor cortex from four non-neurologic disease controls." This is a binary outcome (detectable/not detectable) with n=6 and n=4. A Fisher's exact test would give p=0.0048, which would support the claim — but no test is reported. More importantly, the immunoblots are not quantified; the claim of "increased" is visual. The authors should provide densitometric quantification with normalization (e.g., to total TDP-43 or a loading control), state the test used, and report the p-value. Without this, the central human-tissue finding is an anecdote, not a result.

**3. The peptide-importin-α1 binding assay (Figure 3F) is presented without any error bars, n, or statistical test.** The figure shows binding curves across a concentration range, but the text does not state how many independent experiments were performed, whether the curves are means ± SEM or single representative experiments, or whether the differences between acetylated/phosphorylated peptides and the unmodified control were tested. The claim that "peptides acetylated at K82 did not bind to importin-α1" is the mechanistic core of the paper, and it needs at least an n and a stated comparison (e.g., IC50 values with CIs, or a two-way ANOVA on the binding curves). As written, this is a figure with no statistics attached.

---

### Sweep

- **Figure 1A/B and S1A:** Proteasome activity and TDP-43 localization time courses show error bars but no n, no test, and no definition of the error bar (SEM vs SD); the 12-hr time point claim of "as early as 12 hr" needs a stated test and n.
- **Figure 1G:** Stathmin-2 cryptic splicing is shown as a gel image with no quantification; the claim of "reduced full-length" and "generated truncated" needs densitometry with n and test.
- **Figure 2E:** The quantification of Clover-TDP-43 variants (WT, ΔNLS, PY-NLS) has no stated n, test, or error bar definition; the claim that PY-NLS rescues mislocalization needs a paired comparison across the same time points.
- **Figure 3C-D:** The acetylation/phosphorylation mimic quantification (K82Q eliminating nuclear import) has no n, test, or error bars; this is a headline claim and needs a stated comparison (e.g., one-way ANOVA with Dunnett's vs. WT).
- **Figure 4E:** The K82R mislocalization claim has no n or test; the statement "even when accumulated at only 25% the level of endogenous TDP-43" (Fig. S4A) is a single immunoblot with no quantification.
- **Figure 5B:** The correlation between ac-TDP-43(K82) and phospho-TDP-43 is asserted ("sALS samples with the highest ac-TDP-43(K82) signal also had higher phosphorylated TDP-43") but no correlation coefficient or test is reported.
- **Multiple comparisons:** The TDP-43 variant screen (Fig. 4) tests many constructs; no correction is mentioned. If the authors are claiming K82R is uniquely mislocalized, they need to state whether the other variants were tested against a corrected threshold.

---

### Questions

1. For the TMT experiment (Fig. 1E), how many independent neuronal differentiations were used, and were the three forward/reverse labelling groups biological or technical replicates?
2. For Figure 5B, can you provide densitometric quantification of the ac-K82 and phospho-TDP-43 bands with a stated test (e.g., Mann-Whitney U) and exact p-values?
3. For Figure 3F, how many independent binding experiments were performed, and what are the error bars and statistical comparisons between the modified and unmodified peptides?

---

### Strengths

1. The design of the TDP-43-PY-NLS swap experiment (Fig. 2D-I) is a clean, well-controlled test that isolates the cNLS as the relevant determinant of mislocalization.
2. The use of acetylation-specific antibodies validated against the unmodified peptide (Fig. 5A) is a rigorous approach to detecting the modification.
3. The mutagenesis strategy (Fig. 4F) systematically dissecting which lysines are necessary and sufficient for import is a thoughtful and thorough approach.

---

### Overall

The paper has a strong mechanistic hypothesis and a plausible experimental design, but the quantitative reporting is not at the standard required for the claims made. The central claims — that TDP-43 is specifically sensitive to proteasome inhibition, that K82 acetylation abolishes importin-α1 binding, and that K82 acetylation is present in sALS — all lack the statistical detail needed to evaluate them. The human tissue data in particular is presented as a binary observation without quantification. I cannot recommend acceptance until the authors provide the n's, tests, and error bars for the key figures.