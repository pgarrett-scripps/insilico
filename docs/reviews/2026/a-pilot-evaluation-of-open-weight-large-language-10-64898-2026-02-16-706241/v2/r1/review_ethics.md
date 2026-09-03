# Ethics & Compliance Reviewer

SCORE: 5
CONFIDENCE: 4

## Summary

This is a well-executed pilot evaluation of open-weight LLMs for a real metadata-screening task in genomics. The authors retrieve 150 Arabidopsis RNA-seq projects, manually label them for presence of ABA-treated samples with matched controls, and benchmark 17 models (open-weight and closed) on binary classification. They find that several open-weight models achieve F1 > 0.98, comparable to closed models, and that self-reported confidence scores may help identify high-confidence predictions suitable for automation. The work is transparent about its scope and limitations, the evaluation is sound, and the contribution is genuine: demonstrating that local open-weight models can now perform semantic metadata filtering at scale without reliance on proprietary APIs. For a journal serving researchers across disciplines, this is a clear accept.

## Strengths

1. **Honest scope and limitations.** The authors explicitly state that their task is narrow (Arabidopsis, ABA, bulk RNA-seq, n=150), acknowledge that single-cell and multi-omics would require different validation, and note that incomplete metadata can mislead even high-confidence LLM outputs—this candour is rare and valuable.

2. **Reproducible and transparent methodology.** Code and data are public on GitHub; the workflow is configurable; ground-truth labels, prompts, and all model outputs are deposited; and reproducibility testing on a 50-project subset shows stable binary outputs across five runs for the tested models.

3. **Practical trade-off analysis.** The paper does not just report accuracy but examines precision–recall shifts across prompts, runtime costs for local execution, and the F1–runtime frontier for open-weight models, enabling practitioners to choose based on their constraints rather than a single "best" model.

## Weaknesses: Load-bearing claims

**Claim 1: Open-weight models now match or exceed closed models on this task.**

The evidence is Table 1: gpt-oss-120b_low achieves F1=0.992 (prompt 2), qwen3-next-80b-a3b-thinking achieves F1=0.984, and both exceed gpt-4o-mini (F1=0.653) and gpt-3.5-turbo (F1=0.630). However, the comparison is not entirely clean. The closed models tested (gpt-3.5-turbo-0125, gpt-4o-mini-2024-07-18, gpt-4o-2024-11-20) are from 2024 or earlier; the newest closed model (gpt-5.1-2025-11-13) achieves F1=0.984 under prompt 2, matching the best open-weight models. The claim that open-weight models "outperform" closed models released in 2024 is supported, but the framing in the abstract and introduction that they are "comparable to" closed models is more accurate than "outperform." The paper does not test the very latest closed models (e.g., Claude 3.5 Sonnet, Gemini 2.0) side-by-side with the open-weight models, so the claim of parity is relative to a moving target. What would settle this: explicit statement that the comparison is to 2024 closed models, or inclusion of the latest closed-model releases available at submission time.

**Claim 2: Self-reported confidence scores reliably identify high-confidence predictions suitable for automation.**

The evidence is Table 3 and the HIGH condition analysis: for three models (gpt-oss-120b_high, qwen3-30b-a3b-thinking, qwen3-next-80b-a3b-thinking), restricting to p < 0.25 or p > 0.75 yields precision=recall=F1=1.0 on 88–137 projects. However, this result is model-dependent and does not generalize. For gpt-3.5-turbo-0125 and gpt-4o-mini-2024-07-18, the HIGH condition shows F1 scores of 0.286 and 0.000 respectively, meaning high confidence does not predict accuracy in those models. The paper acknowledges this ("for models with sufficiently high performance") but the claim that confidence scores "may help identify high-confidence cases" is only true for a subset of models. The authors do not provide a method to predict in advance which models will show this property, so a practitioner cannot know whether confidence will be useful without first validating on a labeled subset—which undermines the automation claim. What would settle this: either a predictor of which model families show reliable confidence (e.g., reasoning-enabled models, MoE architectures) or explicit restatement that confidence-based filtering requires per-model validation before use.

**Claim 3: The workflow scales to large metadata-screening tasks.**

The paper demonstrates the workflow on 150 projects and reports runtimes (Supplementary Table 5, Supplementary Figure 2). The fastest open-weight model (qwen3-30b-a3b-instruct) processes projects in ~4.2 s/project; the slowest reasoning-enabled model (qwen3-next-80b-a3b-thinking) takes ~38.3 s/project. For 10,000 projects, this scales to 11–107 hours of compute on a single Mac Studio. The paper does not discuss parallelization, batch processing, or deployment to multi-GPU systems, so the claim of "scalable" is relative to manual curation but not absolute. The paper also does not test on projects with longer or more complex metadata (e.g., multi-omics, single-cell), which could increase token counts and runtimes. What would settle this: either demonstration on a larger dataset (e.g., 1,000+ projects) or explicit statement that "scalable" means "more scalable than manual review" rather than "suitable for millions of projects."

## Weaknesses: Sweep

1. **Single-curator ground truth:** Labels were assigned by one person without inter-annotator agreement; the authors note this but do not quantify the risk that ambiguous cases were mislabeled (e.g., projects where ABA is mentioned but treatment is unclear).

2. **Keyword-search bias:** The evaluation is restricted to the 150 projects returned by the specific keyword queries used; if different keywords or search strategies were used, the retrieved pool would change and model rankings might shift, limiting generalizability of the performance estimates.

3. **Discrete probability outputs:** Self-reported probabilities cluster at seven discrete values (0.05, 0.40, 0.60, 0.75, 0.80, 0.90, 0.95) rather than continuous values, reflecting prompt guidance; this limits the precision of AUPRC and confidence-based filtering.

4. **No evaluation of structured extraction:** The paper demonstrates sample-level metadata extraction (genotype, tissue, treatment concentration) but does not validate accuracy, acknowledging that ground-truth creation for complex outputs is difficult—this is a real limitation but honestly stated.

5. **Metadata completeness assumption:** The workflow assumes that project and sample metadata retrieved via API are sufficient; if key information is only in associated papers or supplementary files, the LLM will miss it, but the paper does not quantify how often this occurs.

6. **Cross-session drift in probabilities:** For gpt-oss-120b_low, self-reported probabilities shifted for 5 of 50 projects between the original run and reproducibility runs (0.95→0.75 or 0.75→0.80), though binary labels remained stable; this suggests confidence scores are less stable than binary outputs.

7. **No comparison to rule-based baselines:** The paper compares LLM classification to keyword-search-only but not to rule-based or regex-based extraction methods that might be faster and sufficient for simple tasks.

## Questions

1. **Table 1, gpt-5.1-2025-11-13:** This model was released in November 2025, the same month the search was executed (December 7, 2025)—was it available for testing at the time, or was it added post-hoc? If post-hoc, does this affect the claim that open-weight models match "current" closed models?

2. **Supplementary Table 1:** The discrete probability values (0.05, 0.40, 0.60, 0.75, 0.80, 0.90, 0.95) appear to be hard-coded in the prompt guidance; can you provide the exact prompt text that elicited these values, and did you test whether continuous probabilities would improve AUPRC?

3. **Figure 3c and Table 1:** Among the top-performing models (F1 ≥ 0.98), is there a pattern in model size, architecture (dense vs. MoE), or reasoning mode that predicts which will show reliable confidence scores (Table 3, HIGH condition F1=1.0)?

4. **Supplementary Table 8:** The 150 projects include 104 common to both GEO and BioProject and 23 unique to each database; did you test whether model performance differs between the two sources, or whether the mapping process (GEO→BioProject) introduced errors?

---

## Ethics & Compliance

**Funding and competing interests:** Funding is disclosed (JST COI-NEXT, BOOST). No competing interests are stated. ✓

**Human subjects, animal research, clinical trials, dual-use, or restricted data:** None. This is a computational analysis of public, non-human genomic metadata. ✓

**Data and code availability:** Code is public on GitHub under MIT license; data are deposited on Figshare with DOI. ✓

No ethics or compliance concerns.