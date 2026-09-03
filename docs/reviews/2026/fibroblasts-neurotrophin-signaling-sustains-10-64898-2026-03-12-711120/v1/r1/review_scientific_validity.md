# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling sustains pathological vascular maturation in RA synovia despite immunosuppressive therapy, and demonstrates that FDA-approved TRK inhibitors can reverse this maturation ex vivo. The core claims are well-motivated and supported by substantial experimental work, but three load-bearing conclusions rest on evidence that does not fully exclude alternative explanations or establish causation as claimed. The work would benefit from clarification of mechanism, stronger causal evidence, and explicit narrowing of scope where correlational data are presented as mechanistic.

## Strengths

1. The spatial transcriptomic analysis is comprehensive and well-executed, with paired pre/post-treatment samples from 22 RA patients providing genuine longitudinal evidence of persistent vascular maturation despite therapy.

2. The authors validate neurotrophin receptor expression across multiple orthogonal methods (spatial transcriptomics, RNAscope, immunohistochemistry) and test functional consequences in both cultured cells and intact tissue explants.

3. The demonstration that FDA-approved TRK inhibitors reduce vascular maturation in human RA synovial explants is clinically relevant and represents a concrete therapeutic lead.

## Load-Bearing Weaknesses

**Claim 1: Neurotrophin signaling *drives* fibroblast differentiation into mural cells.**

The evidence presented is that neurotrophins (NGF, BDNF, NT3) induce expression of mural cell markers (ACTA2, MYH11, RGS5) in cultured fibroblasts and increase contractility and tube-support function. However, marker induction does not establish that fibroblasts have differentiated into functional mural cells, nor does it exclude the alternative that neurotrophins activate a mural cell gene expression program in fibroblasts without true lineage conversion. The collagen gel contraction assay (Fig. 4D–F) shows functional contractility, which is stronger evidence, but applies only to BDNF and NT3, not NGF. Critically, the authors do not show that neurotrophin-stimulated fibroblasts acquire the full transcriptomic signature of native pericytes or VSMCs, nor do they demonstrate that these cells stably maintain mural identity after neurotrophin withdrawal or in vivo. The micromass organoid experiments (Fig. S5) show enhanced tube formation and contractility but do not isolate the contribution of fibroblast-derived mural cells from endothelial or other stromal responses. To resolve this: provide bulk or single-cell RNA-seq comparing neurotrophin-stimulated fibroblasts to native pericytes and VSMCs, quantify overlap in differentially expressed genes, and test whether the mural phenotype persists after neurotrophin removal.

**Claim 2: NOTCH3 signaling *initiates* neurotrophin signaling by inducing NGF production.**

The evidence is that NOTCH3 siRNA or DAPT reduces NGFR, NTRK1, NTRK2, and NTRK3 expression in fibroblasts co-cultured with endothelial cells (Fig. 3C, Fig. S7), and that DLL4 stimulation increases NGF expression in a NOTCH3-dependent manner (Fig. 5C–E). However, the authors do not establish that NOTCH3 directly activates NGF transcription. The reduction in neurotrophin receptor expression following NOTCH3 knockdown could reflect indirect effects—loss of fibroblast activation, reduced endothelial contact, or altered metabolic state—rather than direct transcriptional regulation of NGFR, NTRK1, NTRK2, NTRK3. The NGF induction by DLL4 is consistent with NOTCH activation, but NOTCH3 knockdown or DAPT could block this through effects on fibroblast survival, proliferation, or endothelial signaling rather than through loss of direct NGF transcriptional control. The authors do not report ChIP-seq, ATAC-seq, or reporter assays identifying NOTCH3 binding sites in the NGF promoter or enhancers. To resolve this: perform chromatin immunoprecipitation or luciferase reporter assays on the NGF promoter/enhancer region to demonstrate direct NOTCH3 occupancy and transactivation, or use single-cell RNA-seq to show that NOTCH3 activation precedes NGF induction within the same cells.

**Claim 3: Persistent vascular maturation in post-treatment RA is *sustained* by neurotrophin signaling and can be *reversed* by TRK inhibitors.**

The spatial transcriptomic data show that mural cell density increases from pre- to post-treatment RA (Fig. 1G–H), and that neurotrophin receptors are expressed on these cells (Fig. 2). The authors then show that TRK inhibitors reduce aSMA and vascular density in RA synovial explants cultured ex vivo for 3 days (Fig. 6C–G). However, the explant system is not a faithful model of the in vivo post-treatment RA microenvironment: it lacks circulating immune cells, systemic factors, and the full stromal context. More critically, the authors do not demonstrate that neurotrophin signaling is *necessary* for the persistence of vascular maturation in vivo. The explant experiments show that TRK inhibition *can* reduce vascular maturation in vitro, but do not prove that neurotrophin signaling is the rate-limiting driver of the persistent maturation observed in post-treatment patients. Alternative explanations include: (i) vascular maturation is driven by other signals (hypoxia, VEGF, Ang-1/Tie2, TGFβ) that persist despite immunosuppression, and neurotrophin signaling is permissive but not necessary; (ii) the maturation observed at 6 months is a legacy of pre-treatment inflammation, and neurotrophin signaling maintains but does not initiate it; (iii) TRK inhibition reduces vascular density in explants through off-target effects or toxicity unrelated to mural cell differentiation. The authors do not report whether TRK inhibitors reduce vascular maturation in explants from healthy donors (a key negative control) or whether they selectively affect mural cells versus endothelial cells. To resolve this: (a) test TRK inhibitors on healthy donor explants to establish specificity to RA tissue; (b) perform single-cell RNA-seq on treated explants to confirm that mural cell identity is lost rather than merely marker expression reduced; (c) test whether blocking other maturation pathways (VEGF, Ang-1, TGFβ) produces similar or synergistic effects; (d) if possible, perform in vivo studies in a mouse RA model to test whether TRK inhibition prevents or reverses vascular maturation in situ.

## Sweep

1. The claim that endothelial cells "induce" neurotrophin signaling in fibroblasts (Fig. 3, Results section) rests on co-culture data, but the authors do not exclude the possibility that fibroblasts self-activate or that the matrigel substrate drives the response independently of endothelial contact.

2. Figure 5J shows bulk RNA-seq of NGFR-overexpressing fibroblasts, but the authors do not report the full list of upregulated genes or provide the raw data, making it impossible to verify the NGF/NGFR gene signature or assess whether it reflects mural cell identity or a more general fibroblast activation state.

3. The spatial transcriptomic analysis uses a reference dataset from the AMP RA/SLE Consortium for cell-type annotation, but the authors do not report the accuracy of this annotation on their own data (e.g., via manual curation or cross-validation), raising uncertainty about whether vascular cell subtypes are correctly assigned.

4. The authors state that vascular maturation persists "regardless of whether or not patients reached criteria for clinical remission" (Results), but do not provide the DAS28-ESR values, remission status, or treatment response data for individual patients, making it impossible to assess whether the finding holds across the full cohort or only in a subset.

5. The RNAscope quantification (Methods) uses Cellpose for nuclear segmentation and scikit-image for nuclear expansion to approximate cell boundaries; the authors do not report the accuracy of this segmentation or validate it against manual annotation, which could introduce systematic bias in cell-type assignment.

6. The collagen gel contraction assay (Fig. 4D–F) is performed on fibroblasts alone; the authors do not test whether neurotrophin-stimulated fibroblasts contract differently when co-cultured with endothelial cells or in the presence of other stromal cells, which could reveal context-dependent effects.

7. The explant experiments use Matrigel embedding, which is not present in native synovial tissue; the authors do not test whether the same TRK inhibitor effects are observed in explants cultured without Matrigel or in alternative 3D systems.

8. The manuscript does not report whether larotrectinib or entrectinib have off-target effects on other kinases expressed in synovial tissue (e.g., FGFR, PDGFR, c-KIT), which could confound the interpretation of the TRK inhibitor results.

## Questions

- Can the authors provide the bulk RNA-seq data (counts, normalized expression, or processed tables) for NGFR-overexpressing versus GFP-control fibroblasts to enable independent verification of the gene signature and assessment of mural cell identity?

- Do TRK inhibitors reduce vascular maturation in explants from healthy donors, and if so, to what degree and through what mechanism?

- What is the annotation accuracy of the spatial transcriptomic cell-type labels, assessed via manual curation or cross-validation against known marker genes in a held-out subset of the data?