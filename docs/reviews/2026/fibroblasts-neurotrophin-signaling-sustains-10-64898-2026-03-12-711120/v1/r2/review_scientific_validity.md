# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This study uses spatial transcriptomics to identify neurotrophin signaling as a driver of pathological vascular maturation in RA synovia, and demonstrates that FDA-approved TRK inhibitors can reverse this maturation ex vivo. The core mechanistic claim—that NOTCH3-induced neurotrophin signaling drives fibroblast-to-mural-cell differentiation—is supported by coherent evidence from tissue profiling, cell culture, and organoid experiments. However, the causal interpretation of the spatial transcriptomic findings rests on correlational data, and the functional significance of the observed vascular changes for RA pathology remains undemonstrated. The work is technically sound within its scope but makes claims about disease mechanism and therapeutic potential that exceed what the evidence establishes.

## Strengths

1. The spatial transcriptomic profiling is comprehensive and well-executed, with paired pre- and post-treatment samples from 22 RA patients providing robust evidence for persistent vascular maturation despite immunosuppression.

2. The mechanistic pathway is traced through multiple orthogonal approaches: spatial transcriptomics, RNAscope, immunohistochemistry, cell culture, siRNA knockdown, and organoid models, creating internal consistency.

3. The authors test FDA-approved drugs (larotrectinib, entrectinib) in human tissue explants rather than only in cell lines, strengthening translational relevance.

## Major Weaknesses

**Claim 1: Neurotrophin signaling drives pathological vascular maturation in RA.**

The evidence for this claim is correlational at the tissue level. The spatial transcriptomics shows that (i) mural cells express neurotrophin receptors, (ii) these receptors are induced by endothelial-fibroblast contact in vitro, and (iii) vascular maturation persists post-treatment. However, the manuscript does not establish that neurotrophin signaling is *necessary* for the observed vascular expansion in RA synovia. The in vitro experiments (Fig. 3, Fig. 4) show that neurotrophins *can* induce mural cell differentiation from cultured fibroblasts, but this does not prove they are the primary driver *in vivo*. Multiple pathways regulate mural cell recruitment (angiopoietin-Tie, PDGF-B, TGF-β signaling), and the authors do not exclude these as alternative or redundant mechanisms sustaining the observed vascular phenotype. The organoid experiments (Fig. 4K, Fig. 6) show that neurotrophin stimulation increases aSMA and that TRK inhibitors reduce it, but organoids are not intact tissue with the full complement of immune and stromal cells present in RA synovia. To establish necessity, the authors would need to show that blocking neurotrophin signaling in RA tissue explants reduces vascular maturation *more* than blocking other known mural cell recruitment pathways, or that genetic deletion of neurotrophin receptors in fibroblasts impairs vascular maturation in an in vivo RA model.

**Claim 2: NOTCH3 initiates neurotrophin signaling by inducing NGF expression and NGFR-mediated sensitization of TRKA.**

The evidence for NOTCH3 → NGF induction is solid (Fig. 5C–E: DLL4 stimulation increases NGF; DAPT and NOTCH3 knockout abolish this). However, the claim that NGFR acts as a co-receptor to sensitize TRKA signaling to low-dose NGF is supported only by overexpression experiments (Fig. 5G–H, Fig. S8F–G). The authors show that NGFR-overexpressing fibroblasts exhibit enhanced TRKA phosphorylation at 1 ng/ml NGF compared to control cells. This is consistent with the proposed mechanism, but it does not prove that endogenous NGFR levels are rate-limiting for TRKA signaling in native RA fibroblasts or that this is the mechanism by which NOTCH3 sensitizes cells to NGF. The alternative explanation—that NOTCH3 simply induces both NGFR and NTRK1 transcription independently, and the overexpression experiment happens to show a synergistic effect that is not physiologically relevant—cannot be excluded. The authors report that NTRK1 expression is "extremely low" in synovial tissue (Fig. 2C, Fig. 3C), yet they do not quantify baseline NGFR and NTRK1 levels in control vs. NOTCH3-activated fibroblasts to show that NGFR induction is the limiting step. A dose-response experiment in which endogenous NGFR is knocked down in DLL4-stimulated fibroblasts, followed by measurement of TRKA phosphorylation and RGS5 induction at physiologically relevant NGF concentrations, would settle this.

**Claim 3: TRK inhibitors reverse pathological vascular maturation in RA and represent a therapeutic opportunity.**

The evidence is restricted to ex vivo organoid experiments (Fig. 6). Larotrectinib and entrectinib reduce aSMA staining and vascular density in 3-day synovial explant cultures. This is a meaningful proof-of-concept, but it does not establish that these drugs would reverse vascular maturation in vivo, or that doing so would improve RA outcomes. The explants lack circulating immune cells, systemic cytokines, and the chronic inflammatory milieu that sustains RA pathology. The 3-day treatment window is far shorter than the 6-month clinical course. Critically, the authors do not show that reducing vascular maturation improves any functional outcome relevant to RA—e.g., reduced synovial inflammation, decreased fibroblast activation, improved joint function, or reduced pain. The title and abstract claim that TRK inhibitors "reverse abnormal vascular maturation," which is supported, but the broader claim that this represents a therapeutic strategy for RA (stated in the Discussion) is not. To support that claim, the authors would need to demonstrate in an in vivo RA model that TRK inhibition reduces vascular maturation *and* improves disease activity, joint damage, or another clinically relevant outcome.

## Minor Weaknesses

1. The persistent vascular maturation post-treatment (Fig. 1G–H) could reflect incomplete immune suppression or a time lag in vascular remodeling rather than evidence that vasculature is a "treatment-resistant compartment"; the 6-month window may be too short to observe normalization.

2. The spatial transcriptomic annotation relies on integration with a single-cell reference (AMP RA/SLE Consortium); if that reference has batch effects or misclassifies vascular subtypes, downstream conclusions about mural cell expansion are affected, but no sensitivity analysis is provided.

3. The fibroblast-endothelial co-culture uses a 1:3 ratio in vitro, which may not reflect the spatial organization or cell density in RA synovia, limiting the relevance of the induced gene expression patterns.

4. Figure 5J (bulk RNA-seq of NGFR-overexpressing fibroblasts) is presented as evidence that the NGF/NGFR gene signature is active in RA tissue, but the comparison is between overexpression in vitro and spatial transcriptomics in vivo; the magnitude and cell-type specificity of the signature in native tissue are not quantified.

5. The authors do not report whether TRK inhibitor treatment affects endothelial cell viability or function in organoids, raising the possibility that reduced vascular density reflects toxicity rather than reversal of maturation.

6. The claim that neurotrophin signaling "sustains" vascular maturation (title, abstract) uses language implying ongoing necessity, but the evidence shows correlation and that acute pharmacologic blockade reduces aSMA; chronic necessity is not tested.

## Questions

1. In RA synovial explants treated with TRK inhibitors, is the reduction in aSMA staining accompanied by loss of mural cell coverage (assessed by pericyte and VSMC markers) or by dedifferentiation of existing mural cells, and does endothelial cell density or function change?

2. Do NOTCH3-activated fibroblasts express NTRK1 at levels sufficient to support TRKA signaling without NGFR co-receptor activity, and does NGFR knockdown in DLL4-stimulated fibroblasts impair RGS5 induction at physiologically relevant NGF doses (≤10 ng/ml)?

3. In an in vivo RA model, does systemic or local TRK inhibition reduce synovial vascular maturation and, if so, does it improve disease activity, joint damage, or functional outcomes compared to vehicle or standard DMARD therapy?