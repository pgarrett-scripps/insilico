# Contribution & Prior-Work Reviewer

Perfect. I now have a clear picture of the prior work landscape. Let me compile my review based on the evidence I've gathered.

---

SCORE: 4
CONFIDENCE: 5

## Summary

This manuscript presents a pilot evaluation of open-weight LLMs for binary classification of RNA-seq projects in public databases, specifically screening for Arabidopsis thaliana samples with exogenous ABA treatment and matched controls. The work demonstrates that recent open-weight models (gpt-oss-120b, Qwen3) achieve near-perfect classification (F1 > 0.98) on this task, substantially outperforming keyword-search baselines (F1 = 0.59) and matching or exceeding earlier closed models. The contribution is real and useful, but the novelty is incremental: the core idea of applying LLMs to metadata curation is established in concurrent and recent work, and the manuscript's specific delta is a focused benchmark on one task with one organism and one treatment type.

## Strengths

1. **Rigorous empirical comparison across a diverse model landscape**: The authors evaluate 17 models (12 open-weight, 5 closed) under identical conditions with two prompt variants, providing a systematic snapshot of model performance that will be useful for practitioners choosing tools for similar tasks.

2. **Honest treatment of limitations and reproducibility**: The authors explicitly acknowledge that their evaluation is task-specific (Arabidopsis, ABA, bulk RNA-seq), report reproducibility experiments showing stable outputs within sessions but cross-session drift in some models, and clearly distinguish between self-reported confidence and calibrated probability.

3. **Practical workflow design with code release**: The authors provide a complete, configurable pipeline combining API-based retrieval with LLM classification, released on GitHub with clear documentation, enabling reuse and extension to other organisms and treatments.

---

## Weaknesses: Load-bearing Claims

**1. Novelty of the core contribution — LLM-based metadata screening for public datasets.**

The manuscript's central claim is that "open-weight LLMs can support scalable metadata screening in local environments as an initial step in broader curation workflows." However, this is not new. The preprint record shows at least three directly concurrent or very recent works making the same core claim on the same problem:

- **Ikeda et al. (2025, bioRxiv 2025.02.17.638570)**: "Extraction of biological terms using large language models enhances the usability of metadata in the BioSample database." This work demonstrates LLM-assisted extraction of biological terms from BioSample metadata to improve searchability—the same task (metadata curation via LLM) on the same database (NCBI repositories).

- **Gaio et al. (2025, bioRxiv 2025.04.24.650461)**: "Enhanced semantic classification of microbiome sample origins using Large Language Models (LLMs)." This work applies LLMs to classify sequencing records by sample origin, addressing the same bottleneck (heterogeneous metadata, poor searchability) in the same repositories (SRA/GEO).

- **CistromeMeta (2026, arXiv)**: "CistromeMeta: a large language model powered tool for automated ChIP-seq metadata extraction." This work applies LLMs to extract metadata from GEO ChIP-seq experiments, solving the same problem (heterogeneous free-text metadata limiting reuse) on the same platform.

The manuscript does not cite Ikeda et al. or Gaio et al., despite citing Ikeda et al. as reference 13 for a different (earlier) work on biological term extraction. This is a material omission: the Ikeda et al. 2025 preprint is directly on point and was available before this submission. The manuscript's claim to novelty rests on applying this established approach to a specific new task (ABA-treated Arabidopsis screening), but this is a task-specific instantiation, not a methodological advance. The authors acknowledge this limitation in the discussion ("the performance estimates reported here should be interpreted as specific to the evaluated Arabidopsis ABA-treatment bulk RNA-seq screening task"), but the introduction and abstract do not clearly signal that the core approach is not novel.

**What would resolve this:** Explicitly acknowledge in the introduction and abstract that LLM-based metadata curation is an established approach (citing Ikeda 2025, Gaio 2025, and CistromeMeta), and reframe the contribution as a focused benchmark on a new task domain (ABA-treated Arabidopsis) with a specific emphasis on open-weight model performance and local deployment. This is still a useful contribution, but it is incremental, not foundational.

**2. Claim that open-weight models match or exceed closed models — scope and generalizability.**

The manuscript claims that "open-weight models released in 2025, such as gpt-oss-120b and gpt-oss-safeguard-120b, achieved higher classification performance than the model released in 2023, gpt-3.5-turbo-0125" and "outperformed the models released in 2024, gpt-4o-2024-11-20 and gpt-4o-mini-2024-07-18." This is true for this specific task (binary classification of ABA-treated Arabidopsis projects), but the manuscript does not adequately signal that this result is task-specific and may not generalize. 

The evidence for this claim is a single benchmark on 150 projects with a single organism, treatment, and data type. The authors do acknowledge this limitation in the discussion, but the abstract and introduction present the finding as a general statement about model capabilities ("These results suggest that open-weight LLMs can support scalable metadata screening in local environments"). The LM Arena leaderboard comparison in Figure 1b is presented as evidence that open-weight models have caught up to closed models generally, but LM Arena scores are aggregate across many tasks, not specific to metadata screening. A model that performs well on general benchmarks may not perform well on domain-specific metadata tasks, and vice versa.

**What would resolve this:** Qualify the claim in the abstract and introduction to state that open-weight models match closed models on this specific task (ABA-treated Arabidopsis bulk RNA-seq screening), and note that generalization to other organisms, treatments, and data types requires independent validation. The current framing risks misleading readers into assuming the result applies broadly.

**3. Confidence-based filtering as a practical operational tool — validation on low-performing models.**

The manuscript proposes that "for models with sufficiently high performance, self-reported probabilities may practically function as reliability indicators" and suggests an operational design where "samples with intermediate probabilities are routed to humans, whereas those with high confidence probabilities are processed automatically." However, the evidence for this claim is mixed and model-dependent.

The authors show that for three high-performing models (gpt-oss-120b_high, qwen3-30b-a3b-thinking, qwen3-next-80b-a3b-thinking), restricting to high-confidence predictions (p < 0.25 or p > 0.75) yields perfect F1 scores (1.00). But for lower-performing models (gpt-3.5-turbo-0125, gpt-4o-mini-2024-07-18), the same filtering yields F1 scores of 0.286 and 0.000, respectively, despite the model reporting high confidence. The authors acknowledge this ("for models with sufficiently high performance, self-reported probabilities may practically function as reliability indicators"), but the practical implication is unclear: how is a user supposed to know in advance whether their chosen model falls into the "sufficiently high performance" category? The authors do not provide a diagnostic test or threshold for determining this.

**What would resolve this:** Provide a practical diagnostic: for a given model and task, what is the minimum F1 score or other metric that predicts that confidence filtering will work? Alternatively, recommend that users validate confidence filtering on a small manually labeled subset before deploying it at scale. The current guidance is too vague to be actionable.

---

## Weaknesses: Sweep

- **Single-curator ground truth without inter-annotator agreement**: The benchmark labels were assigned by one curator (acknowledged in line 673), raising the risk that the evaluation reflects one person's interpretation of ambiguous metadata rather than an objective standard. This is particularly concerning for a task where the authors themselves note that "metadata is incomplete, ambiguous, or inconsistent" (line 606).

- **Prompt design not optimized or validated on held-out data**: The authors compare two prompts but do not report whether these were selected a priori or chosen after observing results. The statement "This comparison was not intended as an exhaustive prompt-engineering optimization" (line 189) suggests exploratory design, which risks overfitting to the specific 150-project dataset.

- **Reproducibility experiment limited to two models and 50 projects**: While the authors test reproducibility on a subset, the finding of cross-session drift in self-reported probabilities for gpt-oss-120b_low (5 of 50 projects changed) suggests that reproducibility may be fragile; testing on only two models and 50 projects is insufficient to characterize this risk across the full model set.

- **AUPRC analysis based on discrete, not continuous, probability values**: The authors note that self-reported probabilities are concentrated at seven discrete values (0.05, 0.40, 0.60, 0.75, 0.80, 0.90, 0.95) rather than continuous, which undermines the interpretation of AUPRC as a continuous ranking metric; the authors acknowledge this but do not adjust their interpretation accordingly.

- **No comparison to rule-based or hybrid baselines**: The manuscript compares LLM classification only to keyword search, not to rule-based extraction methods or hybrid approaches that might be faster or more transparent; this limits the evidence for the practical advantage of LLMs over simpler alternatives.

- **Metadata integration strategy not validated**: The authors consolidate project- and sample-level metadata into a single text input, but do not report whether this integration strategy affects LLM performance compared to alternative input formats (e.g., structured JSON, separate project and sample sections).

- **Generalization to other data types not addressed**: The authors acknowledge that single-cell RNA-seq and multi-omics datasets are "more complex" (line 641) but provide no preliminary results or analysis of whether the workflow would work for these data types, limiting the scope of the claimed contribution.

- **Cost comparison incomplete**: The manuscript discusses "cost" broadly but does not provide concrete numbers for API fees (closed models) or computational cost (local open-weight models), making it difficult for readers to assess the practical trade-off.

---

## Questions

- **Line 189–190**: Were prompts 1 and 2 designed a priori based on the task definition, or were they selected after observing initial results on the 150-project dataset? If the latter, was the dataset split into train/validation to avoid overfitting?

- **Line 673**: What was the inter-annotator agreement between the single curator and a second independent annotator on a subset of the 150 projects? This is essential for validating the ground truth.

- **Table 3, gpt-3.5-turbo-0125 HIGH condition**: The model reports high confidence (p < 0.25 or p > 0.75) for only 30 of 150 projects, yet achieves F1 = 0.286 on those 30. What is the distribution of true positives and false positives in this high-confidence subset? This would clarify whether the model is systematically wrong or just uncertain.

- **Line 596–597**: The authors state that self-reported probabilities "did not behave as precise continuous probability values" and were concentrated at discrete values. Was this discrete distribution specified in the prompt, or did it emerge from the model's behavior? If specified, what was the exact wording?

---

## Minor Issues for Other Reviewers

- **Methodological reviewer**: The choice of 0.25 and 0.75 as confidence cutoffs is acknowledged as "predefined practical" rather than data-driven, but no sensitivity analysis is provided to show how results change with alternative cutoffs (e.g., 0.33/0.67, 0.40/0.60).

- **Statistics reviewer**: The F1 scores are reported without confidence intervals or significance tests; given the small sample size (n=150), reporting 95% CIs would strengthen claims about model performance differences.