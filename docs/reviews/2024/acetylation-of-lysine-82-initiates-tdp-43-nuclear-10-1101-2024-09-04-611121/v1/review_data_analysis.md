# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall assessment

The statistical and data-analytic work is generally sound and well-executed. Quantitative claims are supported by appropriate tests, sample sizes are stated, and the authors apply multiple-comparison corrections where needed. The main contribution—that K82 acetylation disrupts TDP-43 nuclear import—rests on convergent evidence from multiple experimental modalities (live-cell imaging, biochemistry, mass spectrometry, human tissue) rather than a single statistical test, which strengthens the claim. One substantive concern about the nuclear proteome analysis and a few minor reporting gaps prevent a higher score, but these do not undermine the core findings.

## Strengths

1. Post-translational modification discovery by mass spectrometry is well-controlled: affinity purification of endogenously tagged TDP-43 with 98.3% peptide coverage (Fig. S3B) and independent confirmation by peptide-binding assays (Fig. 3F) reduce the risk of false positives.

2. The K82 mutagenesis panel (Fig. 4) is systematic and well-designed: single, double, and multiple lysine-to-arginine variants isolate K82's role without relying on a single comparison, and the finding that K82R alone causes mislocalization while K82 alone is insufficient for import is internally consistent.

3. Human tissue validation uses three independent polyclonal antibodies (Fig. 5A) with specificity confirmed by ELISA against acetylated and unacetylated peptides, reducing the risk of a single antibody artifact.

## Weaknesses: Load-bearing claims

**Nuclear proteome analysis (Fig. 1E–F): TDP-43 is claimed to be "the protein whose nuclear localization is most sensitive to reduced proteasome activity," with a >4-fold reduction. This is the key evidence that the effect is specific to TDP-43 rather than a general nuclear import defect. However, the statistical test and multiple-comparison correction are not stated.** The volcano plot shows unadjusted p-values from a one-sample t-test (stated in the figure legend), but no correction for the ~5,200 proteins tested is mentioned. The authors report that "nuclear content of other ALS-linked RNA-binding proteins was not (or barely) affected" (Fig. 1F), but do not quantify "barely" or state the threshold used to call a protein unaffected. If a Bonferroni or FDR correction were applied, would TDP-43 remain the most significant hit? The claim that this selectivity proves specificity to TDP-43 rather than a general import defect depends on the magnitude of the effect relative to the background—a 4-fold change in a protein with high baseline nuclear abundance could be less dramatic than a smaller fold-change in a rare protein. Reporting the corrected p-value, the effect size (fold-change with 95% CI), and the distribution of fold-changes across all proteins would clarify whether TDP-43 is a true outlier or one of several affected proteins.

**K82 acetylation is sufficient to abolish nuclear import (Fig. 3C–E), but the evidence is indirect: the K82Q acetylation-mimicking substitution eliminates nuclear localization and importin-α1 binding, but this is not the same as acetylation itself.** The authors do show that actual acetylation at K82 (on synthetic peptides) abolishes importin-α1 binding (Fig. 3F), which is strong support. However, in cells, the K82Q variant is expressed as a stable protein, whereas acetylation is a reversible modification that may be dynamic. The claim that acetylation "initiates" TDP-43 proteinopathy rests on the assumption that K82Q faithfully models the functional consequence of acetylation. The authors do not report whether K82Q-expressing neurons show the same loss of stathmin-2 splicing function as BTZ-treated neurons, nor do they measure the stoichiometry of K82 acetylation in sALS tissue (i.e., what fraction of TDP-43 molecules are acetylated?). If only a small fraction of TDP-43 is acetylated in vivo, the contribution to nuclear depletion may be modest. Reporting the percentage of K82-acetylated TDP-43 in sALS samples and comparing stathmin-2 splicing in K82Q-expressing neurons to BTZ-treated controls would test whether acetylation alone is sufficient to recapitulate the loss-of-function phenotype.

## Weaknesses: Sweep

1. **Sample size for human tissue (n=4 controls, n=6 sALS; Fig. 5B):** No power analysis is provided; with this sample size, a two-tailed t-test has ~60% power to detect a large effect (Cohen's d=1.2) but much less for moderate effects. The claim that ac-TDP-43(K82) is "increased in all six sALS patients" is descriptive and does not require a statistical test, but the comparison to controls (Fig. 5B) should report the test used, the p-value, and the effect size with CI.

2. **Multiple proteasome inhibitors (BTZ, MG132, MRZ; Fig. 1A–E) are used interchangeably without testing for differences in their effects on TDP-43 localization:** the authors show that all three inhibit proteasome activity and cause TDP-43 mislocalization, but do not report whether the kinetics or magnitude differ, which could indicate off-target effects or variable potency.

3. **Live-cell imaging quantification (Fig. 2E, S1G) reports "approximately half of TDP-43 mislocalized within 24 hr" but does not define the threshold used to classify a cell as "mislocalized"** or report the inter-rater reliability if manual scoring was used; automated image analysis methods should be described.

4. **Immunoblot densitometry (Figs. 1B, 3C–E, 4C–E, 5B) is not quantified in the main text:** band intensities are shown but fold-changes, error bars, and statistical tests are not reported for most comparisons; the figure legends state "representative" but do not indicate how many replicates were quantified.

5. **Lentiviral transduction efficiency is not reported (Figs. 3C–E, 4D–E):** if transduction is incomplete or variable, the apparent effect of a TDP-43 variant could reflect differences in expression level rather than function; co-expression of endogenous (siRNA-depleted) and exogenous TDP-43 could also confound the results.

6. **The stathmin-2 splicing assay (Fig. 1G, S2E) reports "full-length" and "truncated" mRNA levels but does not quantify the ratio or report the statistical test used to compare BTZ-treated and control neurons.**

7. **Proteasome activity assay (Fig. 1A, S1B–C) uses a luminescence-based readout but does not report the assay's dynamic range, sensitivity, or whether the 50% inhibition target was achieved consistently across replicates.**

8. **Fractionation efficiency is not reported:** nuclear and cytoplasmic fractions are assumed to be pure, but cross-contamination (e.g., cytoplasmic Lamin B1 or nuclear GAPDH) is not quantified, which could inflate or deflate the apparent mislocalization.

## Questions

1. For the nuclear proteome analysis (Fig. 1E–F), what multiple-comparison correction was applied, and does TDP-43 remain the top hit after correction? Report the corrected p-value and the fold-changes (with 95% CIs) for the top 10 proteins.

2. In sALS tissue (Fig. 5B–C), what is the stoichiometry of K82 acetylation—i.e., what percentage of total TDP-43 is acetylated at K82 in each sample, and does this correlate with the phosphorylation level or proteinopathy load?

3. Do neurons expressing TDP-43-K82Q show the same loss of stathmin-2 splicing function as BTZ-treated neurons, and if so, is the effect size comparable?