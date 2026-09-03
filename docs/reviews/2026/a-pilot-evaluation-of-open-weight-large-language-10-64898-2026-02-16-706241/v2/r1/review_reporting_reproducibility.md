# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a reproducible workflow for screening RNA-seq metadata using large language models, with code and data publicly available. The core claim—that open-weight LLMs can achieve near-perfect classification (F1>0.98) on a binary task (ABA-treated Arabidopsis samples with controls)—is well-supported by the reported results. The workflow is transparent, the benchmark dataset is small but clearly defined, and the authors acknowledge major limitations. The work is sound as a pilot evaluation of a specific, narrow task. However, the generalizability claims substantially outrun the evidence, and several procedural details needed for independent reproduction are scattered or missing.

## Strengths

1. Code, data, prompts, and detailed model parameters are publicly released on GitHub and Figshare, enabling inspection and replication of the core classification task.
2. The authors transparently report limitations (single-curator labels, narrow task scope, incomplete metadata constraints) and explicitly scale claims to the evaluated setting.
3. Reproducibility testing on a 50-project subset shows stable binary outputs across five runs for the tested models, and AUPRC analysis corroborates F1-based rankings.

## Weaknesses: Load-Bearing Claims

**Claim 1: Open-weight LLMs achieve comparable performance to closed models for metadata screening.**

The evidence is the F1 scores in Table 1, where gpt-oss-120b_low (F1=0.992, prompt 2) and qwen3-next-80b-a3b-thinking (F1=0.984) match or exceed gpt-4o-2024-11-20 (F1=0.846) and gpt-5.1-2025-11-13 (F1=0.984). However, this comparison is confounded by prompt strictness. Under prompt 1, gpt-5.1-2025-11-13 achieves F1=0.907, while gpt-oss-120b_low achieves F1=0.961—a smaller gap. More critically, the closed models were run via API in December 2025, while open-weight models were quantized versions downloaded from Hugging Face. Quantization can degrade performance, yet no ablation compares the same model in quantized vs. unquantized form, nor are the quantization schemes (GGUF, MLX 4bit) validated as equivalent to the original. The claim that open-weight models "outperformed" 2024 closed models (lines 186–187) rests on a single prompt and a single task; the authors do not show whether this holds across different metadata domains or task definitions. The alternative—that quantization artifacts or prompt-specific tuning favor the open-weight models on this particular task—is not ruled out.

**Claim 2: Self-reported confidence scores reliably identify high-confidence predictions suitable for automated processing.**

The evidence is Table 3 and the HIGH condition analysis: for three models (gpt-oss-120b_high, qwen3-30b-a3b-thinking, qwen3-next-80b-a3b-thinking), excluding intermediate probabilities (0.25 ≤ p ≤ 0.75) yields perfect F1=1.00 on the remaining subset. However, this result is circular: the ground truth was assigned by a single curator using the same integrated metadata text provided to the LLM. If the LLM's confidence reflects how "easy" the metadata are to interpret (not how correct the decision is), then high confidence on unambiguous metadata will trivially correlate with curator agreement. The authors acknowledge this in lines 599–600 but do not test the alternative: whether self-reported confidence predicts accuracy on *out-of-distribution* metadata (different organisms, treatments, or metadata quality). For gpt-3.5-turbo-0125 and gpt-4o-mini-2024-07-18, high-confidence predictions are unreliable (F1=0.286 and 0.000, respectively), yet the authors do not explain why confidence fails for these models or provide a test to predict which models' confidence is trustworthy before deployment. The claim that confidence "may practically function as a reliability indicator" (line 307) is supported only for a subset of models on a single task.

**Claim 3: The workflow is reproducible and can be independently executed.**

The authors provide GitHub code and Figshare data, but several load-bearing procedural details are missing or scattered. (1) The integrated metadata text (Supplementary File 4) is provided, but the exact preprocessing steps—which fields were consolidated, which were retained at sample level, how redundancy was detected—are not fully specified in the Methods (lines 711–730). (2) The ground-truth labels (Supplementary Table 9) are provided, but the curator's decision process is described only in lines 782–813, with no inter-annotator agreement or secondary review. A reader cannot verify whether the labels are correct or whether ambiguous cases were handled consistently. (3) The reproducibility experiment (lines 745–763) tests only two models on 50 projects under one prompt and temperature setting; it does not test whether the reported F1 scores in Table 1 (which used a single run) are stable across sessions. The cross-session drift in self-reported probabilities for gpt-oss-120b_low (lines 605–609) suggests that even "stable" outputs may shift slightly, yet the authors do not report whether binary classifications changed across the original Table 1 run and a later rerun. Without this, a reader cannot confirm that Table 1 is reproducible.

## Weaknesses: Sweep

1. The keyword search strategy (lines 676–682) is task-specific; the authors note (line 652) that different keywords or search strategies would change the retrieved candidate pool and affect LLM performance ranking, yet they do not provide a sensitivity analysis or guidance on how to adapt the search for other organisms/treatments.

2. The confidence-based grouping (p < 0.25 or p > 0.75) is described as "predefined practical cut-offs" (line 261) rather than data-driven, but no justification is given for these thresholds, and Supplementary Table 1 shows that models output discrete values (0.05, 0.40, 0.60, 0.75, 0.80, 0.90, 0.95), suggesting the thresholds may not align with the model's actual confidence distribution.

3. The AUPRC analysis (lines 564–580) uses self-reported probabilities that are concentrated at seven discrete values, not continuous; the authors acknowledge this but still compute AUPRC, which assumes a ranking of continuous scores—a methodological mismatch not fully addressed.

4. Prompt 2 is described as "stricter" and designed to reduce false positives, but no ablation isolates which specific rule changes (e.g., requiring "explicit evidence" vs. "conservative classification") drive the precision-recall shift observed in Table 2.

5. The F1–runtime trade-off (Supplementary Figure 2(e)) compares only ten locally executed open-weight conditions; closed models are excluded from this analysis, so the practical speed advantage of local execution is not quantified against the API-based alternative.

6. The authors state (line 411) that the workflow "automatically generates a table" of extracted sample attributes (Supplementary Table 7), but accuracy of this extraction is not evaluated; they acknowledge this limitation (lines 408–410) but do not provide even a spot-check of extraction correctness.

7. The benchmark is limited to 150 Arabidopsis ABA-treatment bulk RNA-seq projects; the authors correctly note (lines 641–660) that generalization to other organisms, treatments, or data types requires independent validation, but this severely constrains the scope of the "scalable metadata screening" claim.

8. The ground-truth labels were assigned by a single curator; no inter-annotator agreement or secondary review is reported, and the authors do not provide a subset of projects independently labeled by a second curator to estimate label reliability.

## Questions

1. Were the binary classifications in Table 1 stable across the original single run and a later rerun on the full 150-project set, or was reproducibility tested only on the 50-project subset?

2. For the three models where self-reported confidence achieved perfect F1 in the HIGH condition, how many projects were excluded (n′), and what fraction of the original 150 projects does this represent—i.e., what is the coverage cost of filtering for high confidence?

3. Can the authors provide a spot-check (e.g., 10–20 projects) showing whether the extracted sample attributes in Supplementary Table 7 match the ground truth from the integrated metadata, to bound the accuracy of the extraction feature?

4. How sensitive are the F1 scores in Table 1 to the specific quantization scheme (GGUF vs. MLX 4bit) used for open-weight models, and were the quantized versions validated against unquantized baselines?