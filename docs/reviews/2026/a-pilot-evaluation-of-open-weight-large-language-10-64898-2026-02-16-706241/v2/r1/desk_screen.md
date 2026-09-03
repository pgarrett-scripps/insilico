# Desk Screen Assessment

## Scope and Fit
This manuscript presents a pilot evaluation of open-weight large language models (LLMs) for automated screening of RNA-seq metadata in public databases. The work is clearly within scope for In Silico: it is original research with empirical and methodological components, makes checkable claims, and provides sufficient detail and materials for inspection.

The target journal's scope explicitly welcomes "empirical, theoretical, computational and methodological work" across any discipline. This manuscript fits squarely within computational methodology applied to bioinformatics.

## Threshold Issues

**Completeness and Intelligibility**: The manuscript is well-structured, clearly written, and complete. Methods are detailed, data are deposited (Figshare), and code is publicly available on GitHub. No fundamental unintelligibility or incompleteness.

**Central Claims and Evidence**: The authors make three main claims:
1. LLM-based semantic filtering substantially improves on keyword-search-only baselines for metadata screening (F1: 0.59 → >0.98)
2. Open-weight models now achieve performance comparable to closed models
3. Self-reported confidence scores can help identify high-confidence predictions suitable for automated processing

These claims are supported by:
- A well-defined benchmark task (150 Arabidopsis RNA-seq projects, 63 positive/87 negative)
- Systematic evaluation of 17 models across two prompts
- Reproducibility testing on a 50-project subset
- Runtime and accuracy trade-off analysis
- AUPRC analysis complementing F1 scores

The evidence is proportionate to the claims. The authors appropriately acknowledge limitations (single curator labeling, task-specific evaluation, limited to bulk RNA-seq, etc.).

**Fundamental Flaws**: No unfixable methodological problems are evident. The design choices are defensible:
- Using a single curator for ground truth is a limitation the authors acknowledge; this is appropriate for a pilot evaluation
- The predefined confidence cutoffs (0.25/0.75) are stated as practical rather than optimized, which is honest
- The task is narrow but deliberately so, as an initial proof-of-concept
- Reproducibility testing shows stable outputs within session, with appropriate caveats about cross-session drift

**Venue Bar**: The work is solid and useful. It is not groundbreaking—the application of LLMs to metadata curation is not novel in principle—but the systematic benchmarking across multiple models, the focus on open-weight models suitable for local deployment, and the practical guidance for operational design represent genuine contributions. The paper is well-executed within its scope and would be of interest to researchers in bioinformatics, data curation, and applied LLM evaluation.

## Minor Observations
- The paper is somewhat lengthy but the detail is justified given the benchmarking scope
- The limitations section is appropriately candid about what the evaluation does and does not show
- The work would benefit from full review to examine whether the confidence-based filtering analysis is sufficiently rigorous and whether the generalizability claims are appropriately hedged

---

**DESK DECISION: proceed**

This manuscript should proceed to full review. It is in scope, complete, methodologically sound within its stated scope, and makes claims proportionate to its evidence. The authors are appropriately transparent about limitations. Reviewers should assess whether the pilot evaluation is sufficiently rigorous for the claims made and whether the practical guidance is actionable, but there are no threshold problems that warrant desk rejection.