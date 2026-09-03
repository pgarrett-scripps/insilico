# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Overall Assessment

This manuscript presents a substantial spatial transcriptomic study identifying neurotrophin signaling as a driver of pathological vascular maturation in RA synovial tissue, with supporting ex vivo and cell culture experiments. The core finding—that TRK inhibitors reverse vascular maturation in RA explants—is novel and potentially clinically relevant. However, critical statistical and analytical issues prevent acceptance in current form. The spatial transcriptomic analysis lacks multiple-comparison correction despite testing many cell types and genes; key mechanistic claims rest on underpowered or uncontrolled comparisons; and several quantitative results are reported without sufficient methodological detail to verify them. These problems are concentrated in the load-bearing claims and are fixable, but they must be addressed before publication.

## Strengths

1. The spatial transcriptomic cohort is substantial (22 RA patients with paired pre/post biopsies, 2 healthy controls, 2M+ cells) and the experimental design (pre-treatment vs. 6-month post-treatment) directly addresses the clinically important question of treatment resistance.

2. The authors validate neurotrophin receptor expression across three independent modalities (Xenium, RNAscope, immunohistochemistry) and use both gain-of-function (DLL4 stimulation, NGFR overexpression) and loss-of-function (siRNA, CRISPR) approaches to establish causality.

3. The final experiment testing FDA-approved TRK inhibitors (larotrectinib, entrectinib) on human RA explants is clinically grounded and represents a concrete therapeutic lead.

---

## Major Weaknesses: Load-Bearing Claims

### 1. Persistent vascular maturation despite treatment (Figure 1G–H): Multiple comparisons without correction

**The claim:** Six months of immunosuppressive therapy does not reduce synovial microvascular density; instead, capillary ECs, arteriolar ECs, pericytes, and VSMCs all increase significantly.

**The evidence:** Figure 1G reports p-values for 6 comparisons (capillary, arteriole, venule, lymphatic, pericyte, VSMC densities) across pre-treatment vs. post-treatment RA, and 6 more against healthy controls. The text states "p = 0.00036" for capillary ECs post-treatment vs. healthy, "p = 0.0065" for arteriolar ECs, "p = 1.6e-05" for pericytes, "p = 0.0031" for VSMCs. No multiple-comparison correction (Bonferroni, FDR, or pre-registered family) is disclosed. The Methods section (Xenium Data Cell Typing) does not mention correction.

**The problem:** With ~12 independent tests on the same tissue samples, an uncorrected α = 0.05 family-wise error rate is ~0.46. The reported p-values, especially those near 0.05 (arteriolar ECs p = 0.0065 vs. healthy), may not survive Bonferroni correction (threshold 0.05/12 ≈ 0.004). The claim that vascular maturation "persists" is the paper's central justification for targeting neurotrophin signaling; if the effect does not survive correction, the motivation collapses.

**What would resolve it:** Report all p-values from Figure 1G with a pre-specified multiple-comparison correction applied. If any of the key comparisons (pericytes, VSMCs, capillary ECs) fall below the corrected threshold, the claim holds; if not, reframe the finding or acknowledge it as exploratory. Alternatively, pre-register the family of comparisons and report discovery vs. confirmation separately.

---

### 2. NOTCH3 induces neurotrophin signaling (Figure 5C–E): Underpowered and confounded by DLL4 dose

**The claim:** NOTCH3 signaling initiates neurotrophin signaling by inducing NGF expression in fibroblasts; DLL4 stimulation upregulates NGF, and this is blocked by DAPT (γ-secretase inhibitor) or NOTCH3 knockout.

**The evidence:** Figure 5C shows NGF secretion (ELISA) in fibroblasts treated with DLL4 ± DAPT. The text reports "DLL4-stimulation upregulated NGF expression (1.2-fold, p = 0.01)." Figure 5D shows qRT-PCR of NGF mRNA with similar results. Figure 5E shows NOTCH3 KO fibroblasts treated with DLL4 have reduced NGF.

**The problem:** (a) No sample size (n) is stated for any of these experiments. Are these n=3 biological replicates, n=1 repeated 3 times, or something else? Without n, the p-value is uninterpretable. (b) The fold-change (1.2-fold) is modest and the p-value (0.01) is marginal; confidence intervals are not provided. (c) Figure 5C and 5D appear to show the same experiment (DLL4 + DAPT) but report different statistics; it is unclear whether these are independent replicates or the same samples measured two ways. (d) DAPT is a broad γ-secretase inhibitor affecting all NOTCH pathways, not NOTCH3-specific; the NOTCH3 KO is more specific, but no n is given for it either.

**What would resolve it:** State the sample size (n = independent biological replicates) for each experiment in Figure 5C–E. Report 95% confidence intervals alongside fold-changes. Clarify whether Figure 5C and 5D are independent or the same samples. If the fold-change is 1.2-fold, discuss whether this magnitude is biologically meaningful in the context of the downstream effects claimed (e.g., does 1.2-fold NGF induction actually drive the observed fibroblast-to-mural-cell differentiation?).

---

### 3. TRK inhibitors reverse vascular maturation (Figure 6C–G): Quantification method not fully specified, and effect sizes modest

**The claim:** Larotrectinib and entrectinib reduce aSMA expression (36–40% reduction) and vascular density (24–27% reduction in vascular area, 50–54% reduction in PECAM1+ structures) in RA synovial explants.

**The evidence:** Figure 6E reports "aSMA intensity was reduced by 36% (p = 0.044) and 40% (p = 0.034)" with larotrectinib and entrectinib, respectively. Figure 6F reports vascular area reduction of 27% (p = 0.004) and 24% (p = 0.035). Figure 6G reports PECAM1 reduction of 54% (p = 0.04) and 50% (p = 0.031).

**The problem:** (a) The Methods section states "Quantification of aSMA-positive vascular structures per tissue section" but does not specify the denominator: is this the number of aSMA+ structures per unit area, total aSMA+ area, mean aSMA intensity per structure, or something else? "aSMA intensity" in Figure 6F is undefined—is this mean pixel intensity, integrated intensity, or a threshold-based count? (b) No sample size is stated (how many explants per condition?). (c) The p-values are marginal (0.031–0.044) and confidence intervals are not provided; without knowing the variability and n, it is unclear whether these are robust effects or borderline. (d) The effect sizes, while substantial in percentage terms, are reductions from a baseline that is itself pathological; the absolute magnitude of vascular density in treated vs. healthy tissue is not reported, so it is unclear whether treatment normalizes the vasculature or merely reduces it partway.

**What would resolve it:** Define precisely how aSMA intensity and vascular density were quantified (e.g., "mean aSMA pixel intensity per aSMA+ structure," "total aSMA+ area as a fraction of tissue area"). State n (number of explants per condition, number of tissue sections per explant if applicable). Report 95% CIs alongside p-values. Compare treated RA explants to healthy controls to show whether treatment approaches normalization or merely reduces pathology.

---

## Minor Weaknesses: Sweep

1. **Figure 1H (cellular composition):** The text reports "significant expansion of VSMC (p = 0.0031, p = 0.029 compared to healthy)" but lists two p-values without clarifying which comparison each refers to (pre-treatment vs. post-treatment? post-treatment vs. healthy?); the figure legend should disambiguate.

2. **Figure 3D–E (siRNA knockdown of neurotrophin receptors):** No sample size is stated, and the bar plots do not show individual data points, making it impossible to assess variability or detect outliers; overlaying raw points is standard practice for n < 20.

3. **Figure 4F (collagen gel contraction):** The text reports "NT3 stimulation induced the greatest contractile response (21%, p = 0.002), followed by BDNF (16%, p = 0.01), whereas NGF had no significant effect" but does not state n or provide error bars in the figure; without these, the claim that NT3 and BDNF differ significantly from NGF cannot be verified.

4. **Figure 5F–H (TRKA phosphorylation):** The immunoblots show representative lanes but no quantification of band intensity across replicates; the text claims "marked increase in TRKA Y490 phosphorylation" but does not report the fold-change or p-value for the densitometry.

5. **Spatial transcriptomic cell-type annotation (Methods):** The integration procedure uses Harmony and Louvain clustering with resolution 0.3, but no justification is given for this choice, and no sensitivity analysis is reported (e.g., results with resolution 0.2 or 0.4); the robustness of the vascular cell subtype assignments is therefore unclear.

6. **Figure 5J (bulk RNA-seq of NGFR-overexpressing fibroblasts):** The text states "upregulation of multiple mural cell-associated genes, including KCNJ8, ABCC9, and MYOCO" but does not report the fold-changes, p-values, or adjusted p-values; without these, the claim is unquantified.

7. **Figure 6A (DAPT treatment of RA explants):** The text reports "reduction of aSMA expression (0.65-fold, p = 0.021)" but does not state n or provide error bars; a single p-value without sample size is uninterpretable.

8. **Exclusion criteria and data filtering:** The Methods section does not state a priori exclusion criteria for cells (e.g., minimum transcript count, maximum mitochondrial percentage) or whether any samples or cells were excluded post-hoc; this is important because spatial transcriptomic data are sensitive to tissue quality and segmentation artifacts.

---

## Questions

1. **Figure 1G:** Were the p-values corrected for multiple comparisons, and if so, what method was used? If not, what is the family-wise error rate?

2. **Figure 5C–E:** What is the sample size (n = independent biological replicates) for the DLL4, DAPT, and NOTCH3 KO experiments, and are Figure 5C and 5D independent replicates or the same samples?

3. **Figure 6E–G:** How were aSMA intensity and PECAM1+ vascular density quantified (exact definition of the metric), and what is n (number of explants per condition)?

4. **Figure 5J:** What are the fold-changes and adjusted p-values for the differentially expressed genes (KCNJ8, ABCC9, MYOCO) in NGFR-overexpressing vs. control fibroblasts?

---

## Technical Notes for Other Reviewers

- **Experimental design (Methods):** The fibroblast-endothelial co-culture system uses a 1:3 ratio, but no justification is given for this choice, and no dose-response or ratio-response experiment is shown; it is unclear whether the results generalize to other ratios.
- **Cell culture:** Synovial fibroblasts are cultured for 3–6 passages; passage number can affect gene expression and differentiation capacity, but no analysis of passage effects is reported.