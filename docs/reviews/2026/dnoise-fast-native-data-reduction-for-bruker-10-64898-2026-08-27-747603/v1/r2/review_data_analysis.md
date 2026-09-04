# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a well-executed data-reduction tool paper with sound statistical validation on a defined benchmark. The quantitative claims are appropriately scaled to the evidence, the benchmark design is transparent, and the authors honestly report both what is preserved and what is sacrificed. The work is incremental but useful, and the statistical reporting meets publication standards for this venue. The main limitation is scope: validation on a single instrument, sample type, and pair of acquisition modes, which the authors acknowledge. This does not undermine the core claims but constrains their generalizability.

## Strengths

1. **Transparent benchmark construction and pre-specification**: The authors state upfront that parameter selection used one part of the benchmark (15-minute ddaPASEF) and that the 5-minute and diaPASEF arms were held out, making the scope of in-sample vs. out-of-sample results explicit and reproducible.

2. **Appropriate statistical framing of quantification results**: LFQ accuracy is reported as median log₂ ratios with percentile-bootstrap 95% CIs on shared proteins (2,000 resamples), and precision as pooled CV; the authors do not claim statistical significance where none is tested, and they report raw counts alongside summary statistics.

3. **Honest reporting of identification tradeoffs**: The optional MS/MS filtering is presented as a higher-reduction operating point with a documented cost (7–12% peptide loss), and the authors explain why the streak filter outperforms a matched intensity threshold by showing that weak but mobility-coherent signal is preserved and that fragment filtering preferentially removes already-false matches.

## Weaknesses: Load-Bearing Claims

**1. Claim: "Default MS1-only denoising preserves LFQ accuracy in both modes" (Abstract, Results 3.2)**

The evidence is median log₂ ratios and within-condition CV reported for three species across three condition pairs at two gradients. This is appropriate for a label-free benchmark with known ratios, but the claim conflates two different preservation statements: (i) accuracy of the *expected* ratios (the regulated species), and (ii) stability of the *observed* ratios between original and denoised arms. The paper reports both, but they are not the same test.

For ddaPASEF, Figure 3 shows that residual ratios (observed minus expected) are small and similar between arms, which supports the claim. For diaPASEF, the same figure shows the same pattern. However, the text states "Median protein-level LFQ CV and LFQ accuracy (Figures 3 and 4) were unchanged at both gradients" without reporting the actual CV values or their comparison statistics. Figure 4 shows distributions, but no test of whether the medians differ. The percentile-bootstrap CIs in Tables S10 and S11 (referenced but not shown in the main text) are the right approach, but their width and whether they exclude zero are not stated in the main narrative. 

**What would settle this**: Report the median CV for original and MS1-denoised arms side-by-side in the main text, with the bootstrap CI for their difference, for at least one gradient and acquisition mode. State whether the CI includes zero.

**2. Claim: "Every tested processing run completed in 69 seconds or less" (Abstract, Results 3.6)**

The evidence is Figure 6 and Table S16, which report runtimes on a single workstation (Intel Core i7-12700H, 20 threads) for 72 files. This is a descriptive summary, not a claim about generalizability, and it is correctly reported. However, the claim is used to argue that dnoise can run "immediately after acquisition, before data transfer, analysis, replication, or archival." This depends on the acquisition duration, which varies: the paper tested 5- and 15-minute gradients, and the longest runtime (68.7 seconds) is for a 15-minute diaPASEF file with MS/MS filtering. The claim is true for the tested conditions but does not address whether the tool scales to longer acquisitions or whether the 20-thread assumption holds on typical proteomics facility hardware.

**What would settle this**: State the relationship between acquisition duration and runtime (is it linear?), and report runtimes on a more typical facility machine (e.g., 8 threads) to show whether the claim holds under different hardware constraints.

**3. Claim: "The streak filter better preserves weak signal than a matched intensity threshold" (Results 3.4, Figure S5)**

The evidence is a comparison of LFQ intensities for shared ddaPASEF peptide-run pairs at both gradients, showing that the streak filter stays closer to the original while the threshold produces a downward bias toward faint peptides. This is shown in Figure S5 (not in the main text) and described as "increasingly outperformed the per-point threshold as abundance fell." The control is sound in design—both arms use the same acquisition-aware gates, differing only in the filter—but the quantification of "increasingly" is visual. The figure shows a scatter plot with Pearson *r* and median absolute Δlog₂, but no statistical test of whether the slope or intercept differs between the two filters as a function of abundance.

Additionally, the paper reports that the threshold lost more quantified coverage in diaPASEF (Figure S4, Section S5) and explains this via target-decoy search statistics: the threshold lost real identifications faster than false ones (decoy-to-target loss ratio 0.43–0.57 vs. 1.77–2.34 for the streak filter). This is a strong mechanistic argument, but it is based on counts of decoy vs. target hits, not a statistical test of whether the ratio differs significantly between filters. The paper does not report confidence intervals or a test of the hypothesis that the streak filter preferentially retains true signal.

**What would settle this**: Report the decoy-to-target loss ratio for each filter with a 95% CI (e.g., via bootstrap on the contingency table), and test whether the ratios differ significantly. Alternatively, report the precision-recall curve for the two filters on the ddaPASEF fragment data and state the AUC or the precision at a fixed recall level.

## Weaknesses: Sweep

1. **Parameter selection was performed on a subset of the benchmark (15-minute ddaPASEF, Condition A, six replicates) using a grid sweep on "quantified coverage, replicate precision, and intensity fidelity" (Section 2.2, Table S2), but the paper does not state how these three objectives were weighted or combined into a single selection criterion.** The authors chose "gap 2 and length 5 to prioritize stricter local continuity and greater point removal," but the trade-off between these goals and the coverage/precision/fidelity objectives is not quantified, making it unclear whether the choice was optimal or merely defensible.

2. **The benchmark uses a single three-species mixture at a fixed 50 ng load on a single timsTOF Ultra 2 instrument, and the authors acknowledge this limits generalizability (Section 3.7), but they do not report whether the default parameters are robust to variation in sample complexity, load, or instrument age/calibration—all factors that could affect the streak filter's behavior.** A sensitivity analysis varying one of these factors would strengthen the claim that the defaults are broadly applicable.

3. **For diaPASEF, the paper states that "Bruker's on-instrument denoising was enabled for the ddaPASEF survey scans but not for the diaPASEF scans" (Results 3.1), which confounds the comparison of reduction between the two acquisition modes and makes it impossible to isolate whether the larger reduction in diaPASEF (93.5% vs. 81.2% of MS1 points at 5 minutes) is due to the acquisition mode or the on-instrument preprocessing.** The paper acknowledges this as a limitation but does not quantify its effect.

4. **The optional MS1 centroiding (Section 3.5) is presented as an alternative operating point, but the paper does not report how many users might benefit from this trade-off or provide guidance on when to use it instead of the default MS1-only mode.** The claim that "both centroiders are off by default" is correct, but the paper does not explain why they are not recommended or what use case would justify their adoption.

5. **The paper reports that "at the 5-minute gradient the MS1+MS/MS arm quantified more proteins and peptides than the original arm, at lower median CV, despite identifying fewer peptides" (Results 3.3), and explains this via the LFQ q-value gate and cross-run transfer.** However, the paper does not report whether this pattern holds at the 15-minute gradient or whether it is specific to the 5-minute data, which would affect the interpretation of whether MS/MS filtering is a reliable way to improve quantification coverage.

6. **The paper uses Sage for ddaPASEF and DIA-NN for diaPASEF, which are different search engines with different quantification methods (IonQuant for Sage, MaxLFQ for DIA-NN), making it impossible to isolate the effect of denoising from the effect of the search engine on the reported identification and quantification results.** A cross-validation using the same search engine for both acquisition modes would strengthen the claim that the results are due to denoising rather than the choice of software.

7. **The percentile-bootstrap CIs for LFQ accuracy (Tables S10 and S11) are referenced in the text but not reported in the main narrative, and the paper does not state the CI width or whether they exclude zero for any of the reported ratios.** This makes it difficult to assess whether the observed differences between original and denoised arms are within the noise of the measurement or represent a meaningful shift.

8. **The paper states that "every denoised directory in this benchmark was processed by the same Sage and DIA-NN workflows as its unmodified original" (Results 3.6), but it does not report whether the search engines were re-run on the denoised data or whether the same search results were re-scored against the denoised frames.** If the latter, the comparison is not valid because the search results were optimized for the original data.

## Questions

1. In Table S2 (parameter selection), what were the values of "quantified coverage, replicate precision, and intensity fidelity" for the chosen setting (gap 2, length 5) relative to the unfiltered baseline and the other tested settings, and how were these three metrics combined to select the final parameters?

2. For the optional MS1 centroiding (Section 3.5), the paper reports that the watershed centroider "gave up 1.3% of the proteins and 2.2% of the peptides quantified by the original arm" but does not state the absolute counts; what are the quantified protein and peptide counts for the watershed centroider at the 5-minute gradient?

3. The paper reports that DIA-NN "read each native .d directory through its bundled Bruker timsdata library" (Section 2.6); was the denoised .d directory read by the same library version as the original, and were there any differences in how the library handled the reduced frame data?

---

**Minor point for the methods reviewer**: The paper states that "both intensity floors were left at zero" (Section 2.2) but does not explain why zero was chosen or whether non-zero floors were tested; this is a defensible choice but should be justified or at least flagged as a design decision.