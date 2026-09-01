# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Overall Assessment

This manuscript presents a methodological framework for patch-clamp single-cell proteomics with careful attention to retrieval quality and its relationship to proteomic recovery. The statistical analysis is generally sound where present, but several load-bearing quantitative claims rest on very small sample sizes (n=3 for the primary gigaseal-preserved analysis) that cannot support the generality implied, and critical comparisons lack formal statistical tests. The work is honest about its exploratory scope and limitations, which is commendable, but the gap between what the data can establish and what is claimed requires substantial revision.

## Strengths

1. The authors explicitly adopt an indiscriminate collection strategy and analyze all retrieval outcomes rather than selecting only successful cases, enabling assessment of how retrieval mechanics influence proteomic recovery rather than hiding this variability.

2. The framework connecting electrophysiological properties (capacitance, spike integrity) to proteomic outcomes is conceptually sound and the authors transparently acknowledge that in situ recordings do not guarantee proteomic recovery, a non-obvious finding that challenges common assumptions in the field.

3. The manuscript is candid about limitations—compartmental bias, incomplete channel assembly recovery, the constraint that soma-focused sampling will underrepresent distal proteins—and does not overstate what soma retrieval can capture.

## Major Weaknesses

### 1. Primary correlation (capacitance vs. protein identifications) rests on n=3 neurons with gigaseal preservation

The headline quantitative claim is stated as: "total protein identifications correlated with the log-transformed capacitance (F = 1577, p < 0.05, adjusted R² = 0.998, n = 3, Y = 884.2*X + 197.7)" (Figure 3D). This is presented as evidence that "soma size plays a more direct role in protein recovery than RM." 

Three independent observations cannot support a regression model with an adjusted R² of 0.998 and an F-statistic of 1577. With n=3, the degrees of freedom for error is 1, making the F-statistic and p-value mathematically meaningless as inferential statistics. The near-perfect fit is expected by chance alone when fitting a line to three points. The authors do not disclose that this is a saturated model (two parameters, three observations) and cannot be used to test whether the relationship holds in a broader population. The claim that capacitance "provides a means of linking soma size to proteome recovery" is not established by this analysis—it shows only that in three neurons, larger somas yielded more proteins, which is consistent with the hypothesis but does not distinguish it from confounds (e.g., larger somas are easier to retrieve intact, and retrieval integrity itself—not size—drives protein recovery).

**What would resolve this:** Report the three data points explicitly (capacitance and protein count for each neuron), acknowledge the saturated model, and reframe as a descriptive observation rather than a statistical finding. If the authors have additional gigaseal-preserved neurons in the full dataset, include them. Alternatively, test whether retrieval integrity (measured by spike preservation or other metrics) predicts protein recovery independently of size.

### 2. Comparison of protein identifications across retrieval categories (Figure 5A) lacks statistical test

The manuscript states that neurons with torn/aspirated somas "produced the fewest detected proteins of all categories" and that "analysis of passive membrane properties measured prior to retrieval from the brain slice showed that neither log-transformed capacitance nor RM correlated with protein identifications (p > 0.05; n = 6; Figures 5C-D)." However, Figure 5A shows protein counts across multiple retrieval categories (no gigaseal, gigaseal lost, torn, and gigaseal preserved), yet no formal comparison (ANOVA, Kruskal-Wallis, or pairwise tests) is reported. The claim that torn neurons produced "the fewest detected proteins of all categories" is visual inspection of a bar plot without a statistical test. With n=12 total neurons distributed across four categories, the sample size per category is small (n=1–3), making group comparisons underpowered, but the absence of any test is the immediate problem.

**What would resolve this:** Report the median and range of protein identifications per category, state the sample size per category explicitly, and either perform a formal test (naming it and reporting the p-value) or acknowledge that the sample size is too small for statistical comparison and present the data as descriptive only.

### 3. SynGO enrichment analysis (Figures 4B–C, 6B) does not account for multiple comparisons across neurons

The manuscript reports that "SynGO analysis revealed 53 biological processes (BPs; Figure 4B; Table S2) and 24 cellular components (CCs; Table S3) significantly enriched (Q-value < 0.05)" across the three gigaseal-preserved neurons. The use of Q-values (adjusted p-values) suggests a multiple-testing correction was applied within each neuron's analysis, which is appropriate. However, the manuscript does not state whether the same correction was applied across neurons when comparing enrichment patterns (e.g., "neuron #4 exhibited the greatest diversity of enriched terms"). Figure 4C is a heatmap of "top BP terms, sorted by enrichment significance," but it is unclear whether the selection of "top" terms was pre-specified or post-hoc, and whether the comparison of term counts across neurons (e.g., "neuron #6 lacked significant enrichment for synaptic signaling") accounts for the multiple tests performed across the three neurons. If the authors selected the most significant terms post-hoc for display, this introduces selection bias.

**What would resolve this:** State explicitly whether the comparison of enrichment patterns across neurons was pre-specified or exploratory. If exploratory, apply a correction for multiple comparisons across neurons (e.g., Bonferroni or FDR) or present the analysis as descriptive. Report the number of terms tested per neuron and the correction method used.

## Minor Weaknesses

1. **Passive membrane properties (Figure 3C) lack error bars or measures of variability:** The ladder plots show individual measurements but no confidence intervals or standard deviations, making it impossible to assess the precision of the estimates or whether changes during retrieval are within measurement error.

2. **PCA (Figure 6A) is presented without variance explained:** The manuscript states that "principal component analysis (PCA) of all neurons (Figure 6A) revealed clear separation of extreme cases" but does not report the percentage of variance explained by PC1 and PC2, making it difficult to assess whether the separation is meaningful or driven by noise.

3. **Correlation analyses (Figures 5C–D) lack effect sizes and confidence intervals:** The statement "log-transformed capacitance nor RM correlated with protein identifications (p > 0.05; n = 6)" reports only the p-value; Pearson or Spearman correlation coefficients and 95% CIs should be provided to characterize the strength and direction of the relationship.

4. **Video evidence of retrieval quality is qualitative:** The manuscript references Videos S1–3 as evidence of retrieval integrity (e.g., "Neuron #4 represents an ideal retrieval") but does not provide a quantitative scoring rubric or inter-rater reliability, making the classification of retrieval quality subjective.

5. **Protein identification thresholds and FDR filtering are stated but not justified:** The manuscript reports "1% false discovery rate (FDR) at both the precursor and protein group level" but does not justify why 1% was chosen or whether this threshold was optimized for this dataset.

6. **No power analysis or sample size justification:** The authors acknowledge the exploratory scope ("small-scale gigaseal preservation study") but do not state a priori how many neurons were needed to test the primary hypothesis or whether the final n=12 was determined by practical constraints or statistical planning.

7. **Torn neurons as negative controls lack independent verification:** The classification of neurons #11 and #12 as "torn" is based on visual inspection during retrieval (Video S3 referenced), but no quantitative metric (e.g., membrane resistance change, capacitance drop) is provided to confirm that these somas were indeed compromised relative to other categories.

8. **GO term overlap (Figure 4B, UpSet plot) does not test whether overlap is greater than expected by chance:** The UpSet plot shows which terms are shared across neurons, but no statistical test (e.g., hypergeometric test) is performed to determine whether the observed overlap is significant or expected given the total number of terms detected per neuron.

## Questions

1. In Figure 3D, were the three gigaseal-preserved neurons selected from a larger set of attempted gigaseal retrievals, or are these the only three gigaseal-preserved neurons in the dataset? If the former, what was the success rate for gigaseal preservation, and does this affect the representativeness of the n=3 sample?

2. For the claim that "preservation of neuronal spiking during relocation tended to be associated with broader synaptic enrichment" (Abstract), is "tended to be" supported by a statistical test, or is this a visual observation? If the latter, what is the effect size (e.g., difference in number of enriched terms between neurons with preserved vs. compromised spiking)?

3. The manuscript states that "25–50% of the soma could be lost over the course of collection" (Results section) but does not provide a calculation or reference for this estimate. How was this range derived, and what is the uncertainty?

4. In Figure 7, the binary heatmap shows ion channel detection across neurons, but the manuscript does not report whether the presence/absence of specific channels (e.g., SCN2A) correlates with electrophysiological properties (e.g., spike amplitude or frequency). Was this analysis performed, and if not, why not?

---

## Minor Comments for Other Reviewers

- **Methodology (Electrophysiology & Sample Prep):** The patch-clamp protocol and LC-MS/MS acquisition are well-described and appear sound; DIA-NN analysis parameters and FDR filtering are standard. No concerns in this domain.
- **Interpretation (Neurobiology):** The discussion of compartmental bias and the limitations of soma-focused sampling is thorough and appropriately cautious; the authors do not overstate what the proteome can reveal about distal ion channels or synaptic proteins.