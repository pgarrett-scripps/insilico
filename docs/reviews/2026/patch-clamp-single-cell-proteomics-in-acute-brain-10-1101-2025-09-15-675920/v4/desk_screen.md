# Desk Screen Report

## Summary

This is a methodological paper describing a framework for combining patch-clamp electrophysiology with single-cell proteomics (patch-SCP) in acute rat brain slices. The authors develop an "indiscriminate shotgun" collection strategy to assess how soma retrieval quality influences proteomic measurements, with emphasis on relating electrophysiological context to protein recovery.

## Scope Assessment

**In scope for In Silico:** Yes. This is original methodological research with empirical data, deposited materials (mass spectrometry data in ProteomeXchange, videos on Zenodo), and checkable claims about the relationship between electrophysiological parameters and proteomic yield.

## Threshold Issues

### 1. Completeness and Verifiability
- Raw MS data deposited (PXD068359, MSV000099156)
- Videos of soma retrieval publicly available (Zenodo DOI provided)
- Code for analysis available on GitHub
- Sufficient procedural detail for understanding the workflow
- **Status: Adequate**

### 2. Fundamental Soundness
The core experimental design is sound:
- Systematic collection of all patch attempts (not just successful ones) to assess retrieval variability
- Preservation of gigaseal during retrieval to monitor soma properties in real time
- Correlation of electrophysiological parameters (capacitance, spike integrity) with proteomic outcomes
- Use of appropriate bioinformatic tools (DIA-NN, SynGO) for analysis

The framework itself is conceptually coherent and addresses a genuine technical problem in the field.

### 3. Evidence-Claim Alignment
The manuscript makes appropriately scaled claims:
- **Primary claim:** Soma size (capacitance) correlates with protein identifications; retrieval integrity influences synaptic protein recovery. **Supported** by the data shown (Figure 3D, 4B-C).
- **Secondary claim:** In situ electrophysiology alone does not predict proteomic recovery after mechanical retrieval. **Supported** (Figure 5C-D).
- **Interpretive framework:** The three-category classification of retrieval outcomes provides useful context for interpreting patch-SCP results. **Reasonable** as a conceptual contribution.

The authors are appropriately cautious about limitations (small sample size n=12, inability to distinguish technical from biological variability in some cases, compartmental bias inherent to soma-only sampling).

### 4. Significance and Novelty
- **Novelty:** Moderate. Patch-SCP exists; the contribution is a systematic framework for interpreting retrieval variability and demonstrating that gigaseal preservation during retrieval can serve as a quantitative bridge to proteome yield. This is useful methodological progress rather than a breakthrough.
- **Significance:** The work addresses a real bottleneck in patch-SCP (mechanical retrieval variability) and provides practical guidance for future studies. The finding that protein counts alone are insufficient quality metrics (Figure 6) is valuable for the field.
- **Audience:** Appropriate for neuroscientists doing single-cell work, proteomics method developers, and electrophysiologists. The framework is generalizable beyond the specific mPFC pyramidal neurons studied.

### 5. Clarity and Honesty
- The manuscript is well-written and clearly structured.
- Limitations are explicitly discussed: small sample size, inability to resolve whether some variability is technical or biological, compartmental bias, spatial fidelity issues with voltage clamp in extended neurons, incomplete recovery of some ion channel families.
- The authors acknowledge that their approach is "best suited for benchmarking retrieval integrity in relatively large neurons" rather than making definitive claims about subtype-specific efficiency.
- Negative findings are reported (e.g., RM does not correlate with protein identifications; some GPCR families not detected).

### 6. Potential Red Flags
- **Sample size (n=12):** Small, but acknowledged and appropriate for a proof-of-concept methodological study. The authors do not overstate generalizability.
- **Single brain region and cell type:** Limits scope, but not a fatal flaw for a framework paper. Acknowledged in limitations.
- **Incomplete recovery of some proteins:** The authors discuss whether this reflects technical limitations or biological compartmentalization but cannot definitively resolve it. This is honest and appropriate given the exploratory scope.
- **No statistical comparison between retrieval categories:** The paper is largely descriptive rather than inferential. This is acceptable for an exploratory framework paper but limits some claims. The authors do not claim statistical significance where they have not performed tests.

## Specific Concerns (Not Desk-Reject Level)

1. **Figure 3D correlation:** The correlation is based on n=3 neurons with gigaseal preservation. This is very small for a quantitative claim, though the authors do not overstate it. A full review should examine whether the fit is robust or driven by outliers.

2. **Generalizability of framework:** The framework is developed on pyramidal neurons in mPFC. Whether it applies to other neuron types, brain regions, or species is unclear. The authors acknowledge this limitation.

3. **Compartmental bias:** The paper identifies but does not solve the problem that distal proteins (axonal, dendritic) are under-represented. This is inherent to soma-only sampling and acknowledged, but it means the framework cannot fully bridge electrophysiology to proteomics for spatially distributed ion channels.

4. **Missing comparisons:** No direct comparison to prior patch-SCP methods (e.g., cytoplasmic aspiration). The authors discuss this as future work but it would strengthen the paper.

## Verdict

This manuscript presents sound, honest methodological work that addresses a real technical problem in patch-SCP. The evidence supports the main claims, the framework is useful, and the limitations are clearly stated. The sample size is small but appropriate for a proof-of-concept study. The work is neither groundbreaking nor trivial—it is solid incremental progress with practical value for the field.

The paper is suitable for full peer review. It should not be desk-rejected.

---

**DESK DECISION: proceed**

The manuscript is in scope, methodologically sound, evidence-claim alignment is appropriate, and limitations are honestly reported. Send to full review.