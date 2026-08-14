# Debate Transcript

## Advocate — round 1

I want to start by acknowledging several points the other side will almost certainly make, because conceding where the skeptics are right strengthens the case for the genuine contributions that remain standing after those concessions are taken into account.

Let me concede directly:

1. The clarity issues are genuine and need fixing. The swapped Figure 4 caption, the self-contradictory volcano legend, the 37/7 protein count inconsistency, and the numeric discrepancy (238+1323≠1436) are all correctable errors that should have been caught before submission.
2. The reproducibility gaps are real. No repository accession for raw MS data, no normalization description, no WGCNA parameters stated — these are fixable but currently absent.
3. The ethics omissions (no IRB statement, no funding disclosure, no competing-interests declaration) are required statements. They do not suggest misconduct, but they need to be supplied.
4. The methodological concern about the “degradation” claim vs. relocalization is well-taken. The authors themselves flag this in the Discussion, and the abstract should carry the same hedge.
5. The “initiating features of AD” language overstates what six proteins from an uncorrected overlap can support. The authors should requalify this.

Now let me make the case for acceptance despite these flaws.

**Genuine contribution: the core spatial-proteoform finding is real and novel.**

Bai et al. (Neuron 2020) used three fractions (soluble, membrane/organelle, insoluble), but the present study uses four fractions with 75% protein overlap across fractions, deliberately maximizing the detection of spatial proteoforms across compartments. The 78% fraction-specificity statistic — even after FDR correction — is unlikely to vanish entirely; it would shrink, but the qualitative pattern would remain, because the same uncorrected analysis was applied uniformly across all four fractions. A skeptic can argue about magnitude, but they cannot plausibly argue that fraction-specificity is an artifact of multiple testing when the analysis is symmetric across fractions.

**The VPS35 result survives the aggregation confound consideration.”**

VPS35 is not in the insoluble-fraction overlap lists (Supplementary Table 12). It was not among the 37 proteins previously reported as aggregating. Its redistribution between S2 and P3 — confirmed by immunoblot (Fig. 7D) — while total homogenate is unchanged, is a clean demonstration that fraction-specific analysis reveals signals missed by bulk approaches. Even if the mechanism is “relocalization” rather than “mislocalization to a different functional compartment,” the finding that a retromer core component is redistributed in AD is mechanistically interesting because retromer trafficking is functionally linked to endosomal-lysosomal dysfunction, itself a well-established early pathway in AD.

**The human–mouse cross-comparison is a useful methodological extension even if the 2-month overlap is not yet proven.**

The QUAD design applied to two fractions across three ages is more than Fornasiero et al. (2018) or Yarbro et al. (2025) did — neither fractionated in the AD context. The observation that degradation rates diverge between fractions and genotypes (Figs. 8E–H) is descriptive but valuable: it motivates the explicit hypothesis that Abeta pathology alters protein turnover differently in different subcellular compartments, which can be tested with orthogonal methods. Even if the six-protein overlap is inflated by uncorrected testing, the enrichment of vesicle-transport and protein-folding pathways in the larger 155-protein human–mouse correlation (Fig. 9E–F) is a more robust pattern that is unlikely to be a false discovery, because it emerges from two entirely independent datasets (human and mouse, AD and WT) using different quantification strategies (steady-state abundance vs. degradation kinetics).

**The core descriptive observation is the real advance.**

What this paper shows, better than any previous work, is that the AD hippocampal proteome is not simply a list of up- and downregulated proteins. It is a set of compartment-specific redistributions and discordant patterns. The 78% fraction-specificity statistic, even if refined by FDR correction, will remain a large majority. The GO enrichment of vesicle trafficking and protein-folding pathways across both WGCNA and ANOVA is consistent and internally reproducible within the dataset. These are descriptive but robust enough to be published, because they change how the field should design AD proteomics experiments.

**What would settle the revision:**
- Apply FDR correction to the human ANOVA and recompute the 78% statistic.
- Add a mixed-effects model or per-animal summary for the QUAD genotype comparisons.
- Report the six-protein overlap with hypergeometric test against the true denominator N.
- Add raw data deposition, normalization description, WGCNA parameters, and ethics/funding statements.
- Fix the presentation errors (Figure 4 caption, volcano legend, numeric inconsistencies).
- Requalify “initiating” to “early-associated” and “degradation” to carry the relocalization caveat in the abstract.

These revisions are substantial but achievable. The paper should be accepted pending them, because the core descriptive finding — that most AD proteomic changes are fraction-specific — is robust enough to withstand statistical tightening, and the mechanistic follow-ups (VPS35 redistribution, degradation-rate divergence) are intriguing enough to warrant publication even if they are not yet fully proven.

In sum: the paper has errors that must be fixed, but the errors are fixable, and the genuine contributions — the spatial resolution itself, the VPS35 distribution finding, and the human–mouse pathway concordance — justify acceptance after a major revision cycle.

**Key points:**
- Concede clarity, reproducibility, ethics, and methodological gaps — all fixable.
- The 78% fraction-specificity statistic is robust to FDR correction because it is measured symmetrically across fractions.
- VPS35 redistribution is demonstrated by immunoblot, total-homogenate unchanged, and is not in the insoluble-fraction overlap, distinguishing it from aggregation artifacts.
- The human–mouse 155-protein pathway concordance (vesicle transport, protein folding) emerges from two independent datasets using different quantification strategies, strengthening its robustness.
- Recommended revision path (FDR correction, mixed-effects model, hypergeometric test, data deposition, presentation fixes) is achievable without new experiments.

## Skeptic — round 1

...

**Key points:**
- ...