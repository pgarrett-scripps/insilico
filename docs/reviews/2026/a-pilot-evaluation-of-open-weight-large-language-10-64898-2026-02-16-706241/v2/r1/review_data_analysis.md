# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a well-executed empirical evaluation of open-weight LLMs for a practical metadata screening task. The statistical analysis is sound within its scope, the claims are appropriately scaled to the evidence, and the authors are transparent about limitations. The work makes a genuine contribution by demonstrating that locally executable models can match or exceed closed-model performance on a defined task, with careful attention to reproducibility and cost-benefit trade-offs. The main statistical concerns are modest: some analyses lack formal power justification, confidence-based filtering uses predefined rather than optimized thresholds, and the single-curator ground truth introduces unmeasured inter-rater variability. These do not undermine the core findings but should be acknowledged more explicitly.

## Strengths

1. **Reproducibility validation is rigorous**: Five independent runs on n=50 projects with identical outputs for binary labels and near-identical self-reported probabilities (Supplementary Table 3-4) provide genuine evidence of inference stability, and the authors correctly caveat that this does not guarantee determinism across all hardware/sessions.

2. **Precision-recall trade-off is properly visualized and analyzed**: Figure 3 and Table 2 show model-dependent effects of prompt strictness, with the authors correctly concluding that prompt effects are not universal and must be validated per task—avoiding the false generalization that stricter prompts always improve precision.

3. **Cost and speed analysis is grounded in measured runtime**: Supplementary Table 5 and Figure 2(e) provide per-project execution times across 10 local conditions, enabling readers to make informed model selection decisions rather than relying on accuracy alone.

## Weaknesses: Load-Bearing Claims

**1. Ground-truth labels assigned by a single curator without inter-rater agreement measurement.**

The evaluation rests entirely on binary labels (positive/negative) assigned by one curator to 150 projects (63 positive, 87 negative; Supplementary Table 9). The authors acknowledge this limitation (line 673) but do not quantify its impact. For a task where metadata are described as "unstandardized and described in heterogeneous natural language" (line 61), the boundary between positive and negative cases is inherently ambiguous. The four explicit criteria (lines 799–810: RNA-seq, *Arabidopsis thaliana*, exogenous ABA treatment, matched controls) are clear in principle, but their application to incomplete or inconsistent metadata requires judgment. 

The paper does not report: (i) whether a second curator independently labeled a subset and what inter-rater agreement (Cohen's κ or Krippendorff's α) was achieved; (ii) which projects were borderline and how the curator resolved them; or (iii) sensitivity of the model rankings to plausible alternative labelings. The authors' statement that they "conducted a cross-model comparison using two prompts with different levels of strictness" (line 675) as evidence of generality does not address curator bias—it only shows that model rankings are consistent across prompts, which is weaker. 

**What would settle this**: Report κ or α for a subset (e.g., 30 projects) labeled independently by a second curator, or conduct a sensitivity analysis in which 10–20 borderline projects are re-labeled and model rankings are recomputed. If inter-rater agreement is high, the concern is reduced; if it is low, the evaluation's foundation is shaken.

**2. Confidence-based filtering (HIGH condition) uses predefined cut-offs (p < 0.25 or p > 0.75) without justification or optimization.**

The authors exclude projects with 0.25 ≤ p ≤ 0.75 and recompute metrics on the remaining subset (Table 3, Figure 4). They state these are "predefined practical cut-offs for confidence-based grouping and were not selected by data-driven threshold optimization" (lines 259, 817). However, no justification is given for why 0.25 and 0.75 are the right boundaries. 

The observation that high-performing models output extreme values (0.05, 0.95) while lower-performing models produce intermediate values (0.40, 0.60, 0.75) is interesting, but it does not validate the chosen thresholds. For example, if the true optimal threshold is p < 0.30 or p > 0.80, the reported HIGH-condition metrics would change. Moreover, the authors note that self-reported probabilities are discrete (seven values: 0.05, 0.40, 0.60, 0.75, 0.80, 0.90, 0.95; Supplementary Table 1), which means the 0.25/0.75 boundaries do not align naturally with the model outputs—they fall between discrete values. This makes the cut-off appear arbitrary.

The practical claim—"self-reported probabilities may function as reliability indicators" (line 273)—depends on whether the HIGH condition actually identifies high-confidence, high-accuracy predictions. With arbitrary thresholds, this is not established.

**What would settle this**: Report HIGH-condition metrics for a range of thresholds (e.g., p < 0.20, p < 0.30, p < 0.40 paired with p > 0.80, p > 0.70, p > 0.60) and show that the conclusions (which models achieve perfect F1 in HIGH) are robust. Alternatively, optimize thresholds on a held-out subset of the 150 projects and report them transparently.

**3. AUPRC analysis conflates discrete confidence scores with continuous probabilities.**

The authors construct precision-recall curves using self-reported positive probabilities as the prediction score (lines 300–310, Supplementary Figure 1(c), Supplementary Table 2). However, they later acknowledge that probabilities are concentrated at seven discrete values (line 309), not continuous. AUPRC is designed for continuous scores; applying it to discrete values produces an AUPRC that reflects the ordering of those discrete values but not a true probability calibration.

The authors state: "the self-reported positive probabilities did not behave as precise continuous probability values... the AUPRC values reported in this study should not be interpreted as metrics based on precise continuous probability values. Rather, they should be interpreted as summary metrics based on the ordering information contained in discrete confidence scores" (lines 580–583). This is a fair caveat, but it undermines the claim that AUPRC "strongly agrees" with F1 rankings (line 302). A ranking agreement between two metrics does not validate either metric; it only shows they rank models similarly. The AUPRC values themselves (ranging from 1.000 to 0.490; line 301) are not interpretable as probabilities and should not be reported as if they were.

**What would settle this**: Either (i) report AUPRC only as a ranking metric and remove the numerical values, or (ii) recompute AUPRC after interpolating or smoothing the discrete scores, with explicit disclosure of the method. Alternatively, use a ranking metric designed for discrete scores (e.g., Spearman's ρ between F1 rank and AUPRC rank) instead of AUPRC.

## Weaknesses: Sweep

1. **No a priori power analysis or sample size justification**: The choice of n=150 projects is not justified; no power calculation is provided for detecting a meaningful difference in F1 between models (e.g., F1 ≥ 0.05).

2. **Multiple comparisons across 17 models and 2 prompts (34 conditions) without correction**: No Bonferroni, FDR, or other family-wise error control is applied; the paper reports raw p-values and metrics without acknowledging the multiple-testing problem, though the focus on F1 scores (not p-values) mitigates this somewhat.

3. **Baseline ("Keyword Search Only") is not a real competing method**: It assumes all keyword-retrieved projects are positive, which is a strawman; a fairer baseline would be a rule-based filter or a simpler LLM prompt, making the LLM advantage less obvious.

4. **Reproducibility experiment (n=50) is underpowered to detect cross-session drift**: Five runs on 50 projects is a small sample; the observed drift in openai/gpt-oss-120b_low (4 of 50 projects changed from 0.95 to 0.75) could reflect random variation or systematic session effects—the paper does not distinguish them.

5. **Runtime measurements lack confidence intervals or variability estimates**: Supplementary Table 5 reports mean per-project runtime but no SD, SEM, or range; without variability, the F1–runtime trade-off (Supplementary Figure 2(e)) cannot be assessed for statistical significance.

6. **Sample-level information extraction (Supplementary Table 7) is not evaluated**: The authors acknowledge this ("the accuracy of this detailed information output was not verified or evaluated in this study"; lines 403–404) but still present it as a workflow capability; this is honest but leaves a gap in the claimed contribution.

7. **Prompt 1 vs. Prompt 2 comparison is not a controlled experiment**: Both prompts are author-designed; no independent prompt validation or user study is provided to confirm that prompt 2 actually reduces FPs in practice (as opposed to in this specific task).

8. **Metadata integration procedure (consolidating project- and sample-level info) is not validated**: The authors state they "reduce the input length while preserving the information required" (line 738) but do not show that this consolidation does not lose critical information or introduce bias.

## Questions

1. **Inter-rater agreement (line 673)**: Did a second curator label any subset of the 150 projects? If so, what was the agreement statistic? If not, how confident are you that the ground-truth labels are stable?

2. **Confidence threshold optimization (lines 259, 817)**: Why were 0.25 and 0.75 chosen specifically, and have you tested sensitivity to these thresholds (e.g., 0.20, 0.30, 0.80, 0.70)?

3. **Discrete vs. continuous probabilities (line 309)**: Given that self-reported probabilities are discrete, should AUPRC be reported as a ranking metric rather than a numerical value, or should the scores be interpolated before computing AUPRC?

4. **Baseline comparison (line 412)**: Would a rule-based filter or a simpler LLM prompt (e.g., "Is this ABA-treated Arabidopsis RNA-seq with controls? Answer yes or no.") serve as a more realistic baseline than keyword search alone?

5. **Generalization scope (lines 639–660)**: The task is specific to Arabidopsis + ABA + bulk RNA-seq. Have you tested the workflow on a different organism, treatment, or data type to assess whether model rankings and prompt effects generalize?