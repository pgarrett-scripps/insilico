# Clarity & Presentation Reviewer

SCORE: 4  
CONFIDENCE: 4  

**Overall take (clarity & presentation):**  
This is a well-structured, clearly written manuscript whose central claims are stated explicitly and whose figures are generally well-integrated with the text. The main presentation weaknesses are concentrated in the proteomics methods section (where the normalization and statistical pipeline is described at a level that would be difficult for a non-specialist to reproduce) and in a few figure panels whose legends do not fully define all symbols/abbreviations. These are fixable with minor revision and do not undermine the scientific argument.

**Strengths:**  
1. The central claim — that Git1 regulates Smo signaling by controlling Grk2 translocation to the cilium — is stated explicitly in the abstract and introduction, and each results section builds toward it with a clear through-line.  
2. The time-resolved proteomics design is presented with a clear workflow figure (Fig. 2A) and the volcano plots/heatmaps are interpretable from captions alone.  
3. The authors are candid about limitations (e.g., noting that endogenous ciliary Grk2 is below detection threshold and that Git1-Smo interaction is transient), which aids reader trust.

**Load-bearing weaknesses:**

1. **The proteomics normalization pipeline is under-specified (HARD).** In the Methods, the authors state: “Sample loading and trimmed mean of M values (TMM) normalization were performed across replicates to have comparable total signal intensities across different replicates.” This is the only description of how the six TMT channels were made comparable. A competent reader cannot determine: (a) whether TMM was applied per-channel or per-replicate, (b) what the “global scaling target” was, or (c) how the eBayes moderation was applied to the normalized intensities (was it on log2 ratios? per-channel?). The reference to “Supplementary data 4/5” is not sufficient — those files are not described in the main text. This matters because the volcano plots and heatmaps in Fig. 2B–D depend entirely on this pipeline. I could not verify the statistical validity of the fold-change thresholds (1.5-fold, p<0.05) without this detail. **What would settle it:** a step-by-step description of the normalization (equations or pseudocode) in the Methods, or a deposited analysis script with the exact R commands.

2. **The “time-resolved” claim is not fully supported by the figure presentation (HARD).** The manuscript claims distinct cohorts of Smo-associated proteins at different stages of Hh activation, but Fig. 2D (heatmap) shows only a subset of “top candidates” and the volcano plots (Fig. 2B–C) are not labeled with which time point each panel represents. The reader cannot determine from the figure alone whether the 15-min, 1-h, and 4-h conditions show genuinely different protein cohorts or merely quantitative differences in the same cohort. The GO analysis (Fig. S2C) is presented as a single panel without time-point breakdown, so the claim that “actin binding/GTPase components” are enriched “after Shh treatment” cannot be checked against specific time points. **What would settle it:** label each volcano plot panel with its time point, and either show GO enrichment per time point or state explicitly that the GO analysis pools all post-Shh time points.

**Sweep (one sentence each):**

- Fig. 5C–E: the legend does not define what “basal body” and “ciliary” intensity refer to in the quantification — is the basal body region defined by γ-tubulin staining, and is the cilium region defined by Arl13b? This should be stated in the legend.
- Fig. 4D–G: the pSmo antibody is described as “specifically recognizes the Grk2 phosphorylation sites on Smo” in the text, but the figure legend does not state this — a reader looking only at the figure would not know what pSmo is.
- The term “Smo-TurboID” is used interchangeably with “Smo-V5-TurboID” and “Smo-V5-TurboID stable cell line” — this is consistent enough to follow, but the first use of each variant should be tied to the same construct.
- The Methods section on “Quantification and statistical analysis” states that “a line was drawn along the fluorescent signal” for cilium length, but does not specify which channel was used (Arl13b? acTub?) — this should be stated.
- The abstract claims “time-resolved proteomic study” but the time points (15 min, 1 h, 4 h) are not mentioned in the abstract — a reader skimming the abstract cannot tell what “time-resolved” means here.
- Fig. 3A–D: the legend does not define what “biotin signal” represents (it is stated in the text as Smo-TurboID, but the legend should say so directly).
- The sentence “The immunostaining signal of PKA-C in the cilium was detected 1 h after Shh stimulation, and increased significantly at the 4 h time point with the ciliary PKA-C levels coincide with the levels of ciliary Smo” (Results, Fig. 3 section) has a grammatical error (“levels coincide” should be “levels coinciding” or “levels coincided”) — minor but worth fixing.
- The Methods section on “TurboID labeling experiments” does not state the biotin concentration used for the proteomics experiments (500 µM is stated in the figure legend for Fig. 1E, but the Methods say only “500 µM biotin” in the cell-line section — this is consistent, but the proteomics workflow in Fig. 2A does not state the biotin concentration or duration, which should be added to the figure legend).

**Questions:**

1. In the proteomics Methods, what exactly was the “global scaling target” and how was it computed — was it the mean total intensity across all 18 channels (3 replicates × 6 conditions), or per-replicate?
2. For the eBayes moderation, were the log-fold changes computed on log2-transformed normalized intensities, and was the p-value adjustment (Benjamini-Hochberg?) applied?
3. In Fig. 2D, the heatmap shows “top protein candidates” — what was the selection criterion (fold-change threshold? p-value? both?), and how many proteins are shown?