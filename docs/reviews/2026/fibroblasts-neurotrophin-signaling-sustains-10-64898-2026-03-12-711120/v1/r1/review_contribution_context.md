# Contribution & Prior-Work Reviewer

Now I have sufficient information to write the review. Let me compile my findings:

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a spatial transcriptomic study identifying neurotrophin signaling as a driver of pathological vascular maturation in RA synovial tissue that persists despite immunosuppressive therapy. The work demonstrates that NOTCH3 signaling in endothelial cells induces fibroblast-derived neurotrophin production, which drives differentiation of fibroblasts into mural cells (pericytes and VSMCs), and shows that FDA-approved TRK inhibitors can reverse this process ex vivo. The contribution is real and mechanistically coherent, but builds incrementally on the authors' own prior work on NOTCH3-fibroblast crosstalk and sits within an established literature on neurotrophins in vascular biology. The novelty lies primarily in connecting these known pathways in the RA context and demonstrating therapeutic potential of TRK inhibition in synovial tissue.

## Strengths

1. Rigorous spatial transcriptomic characterization of paired pre- and post-treatment RA biopsies (n=22 patients) with high-resolution vascular cell subtyping, providing robust evidence that vascular maturation persists despite immunosuppression independent of clinical remission status.

2. Mechanistic pathway integration: the authors systematically connect NOTCH3 signaling to neurotrophin receptor induction (NGFR, NTRK1-3) and demonstrate differential receptor-ligand specificity (NGF→pericytes via NGFR/TRKA; BDNF/NT3→VSMCs via TRKB/TRKC), supported by receptor knockdown and pharmacologic inhibition experiments.

3. Functional validation in human tissue: the use of synovial explant cultures preserving tissue architecture and endothelial-fibroblast interactions, combined with demonstration that FDA-approved TRK inhibitors (larotrectinib, entrectinib) reduce vascular maturation markers, provides translational relevance.

## Weaknesses: Load-bearing Claims

**Claim 1: NOTCH3 signaling directly activates neurotrophin signaling through transcriptional induction of NGFR.**

The manuscript shows that NOTCH3 knockdown reduces NGFR, NTRK1, NTRK2, and NTRK3 expression in fibroblasts co-cultured with endothelial cells (Fig. 3C, Fig. S7), and that DLL4 (NOTCH ligand) stimulation upregulates NGF expression in a NOTCH-dependent manner (Fig. 5C-E). However, the evidence for direct transcriptional induction of NGFR by NOTCH3 is indirect: the manuscript shows correlation of NOTCH3 expression with NGFR in spatial data (Fig. 5M) and knockdown effects, but does not provide ChIP-seq, ATAC-seq, or reporter assays demonstrating that NOTCH3 directly binds regulatory elements of NGFR. The mechanism could alternatively involve NOTCH3-induced expression of intermediate transcription factors. This distinction matters because it affects whether NOTCH3 is a direct or indirect regulator of NGFR, and whether the pathway is as specific as claimed. **What would resolve this:** ChIP-seq or luciferase reporter assay showing NOTCH3 binding to NGFR promoter/enhancer elements, or demonstration that NOTCH3 intracellular domain (NICD) alone is sufficient to activate NGFR transcription in the absence of other NOTCH ligand signaling.

**Claim 2: NGFR expression potentiates TRKA signaling to enable fibroblasts to sense low-concentration NGF despite minimal NTRK1/TRKA expression.**

The authors show that NGFR overexpression increases TRKA Y490 phosphorylation at baseline and with 1 ng/ml NGF (Fig. 5G-H), and that NGFR-overexpressing cells show enhanced pericyte marker induction at low NGF doses (Fig. S8F-G). The mechanism proposed is that NGFR acts as a co-receptor to enhance TRKA binding affinity. However, the manuscript cites only one reference (ref. 33, which appears to be about p75NTR-TRKA complexes in general neurotrophin biology) and does not directly demonstrate the NGFR-TRKA complex formation in these fibroblasts. Critically, the baseline increase in TRKA phosphorylation in NGFR-overexpressing cells (without NGF stimulation) suggests NGFR may be activating TRKA through a ligand-independent mechanism (e.g., transactivation, heterodimerization) rather than purely enhancing NGF binding. The manuscript does not distinguish between these possibilities. **What would resolve this:** Co-immunoprecipitation of NGFR and TRKA in fibroblasts ± NGF stimulation; surface plasmon resonance or ELISA-based binding assay measuring NGF-TRKA interaction kinetics ± NGFR; or mutation of putative NGFR-TRKA interaction domains to show loss of potentiation.

**Claim 3: Neurotrophin signaling is the primary pathway sustaining pathological vascular maturation in RA, and TRK inhibitors reverse it.**

The manuscript demonstrates that TRK inhibitors reduce aSMA, PECAM1, and mural cell markers in RA synovial explants (Fig. 6C-G). However, the explant experiments are conducted ex vivo in culture for 3 days with pharmacologic doses of inhibitors (1-10 µM for larotrectinib/entrectinib; typical clinical Cmax ~1-2 µM). The manuscript does not establish that neurotrophin signaling is the *primary* driver—only that it is *a* driver. Other pathways known to regulate mural cell differentiation (PDGF, Ang1/Tie2, TGFβ) are not systematically interrogated in the same explants. Additionally, the 6-month post-treatment biopsies show persistent vascular maturation, but the manuscript does not demonstrate that this persistence is due to ongoing neurotrophin signaling rather than, for example, structural stabilization of already-mature vessels or other stromal remodeling. The claim that TRK inhibitors "reverse" maturation is supported by the explant data, but reversibility in 3-day ex vivo culture does not necessarily predict in vivo reversibility in established disease. **What would resolve this:** (1) Parallel inhibition of PDGF, Ang1/Tie2, and TGFβ pathways in the same explant system to quantify their relative contributions; (2) direct measurement of neurotrophin ligand levels (NGF, BDNF, NT3) in pre- vs. post-treatment biopsies to confirm that neurotrophin signaling is active in vivo; (3) in vivo mouse model of RA with TRK inhibitor treatment to assess reversibility of vascular maturation in intact disease.

## Weaknesses: Sweep

1. The authors' prior work (Wei et al. Nature 2020, ref. 14) already established NOTCH3-driven fibroblast differentiation and endothelial-fibroblast crosstalk in RA; the present work extends this by identifying neurotrophins as downstream effectors, which is incremental rather than foundational.

2. The role of neurotrophins in vascular development is well-established (TRKB-null mice show pericyte defects, NT3-null mice show vascular abnormalities; refs. 36-38), so the application to RA vascular pathology, while novel in context, does not represent a new biological principle.

3. The manuscript does not measure neurotrophin ligand concentrations (NGF, BDNF, NT3) in synovial tissue or explants, relying instead on receptor expression and mRNA induction; direct quantification would strengthen claims about pathway activation.

4. The spatial transcriptomic analysis is limited to 6-month post-treatment timepoint; longer follow-up or intermediate timepoints would clarify whether vascular maturation is truly persistent or eventually resolves with extended immunosuppression.

5. The fibroblast-endothelial co-culture system uses a 1:3 ratio in vitro, which may not reflect the actual cellular density and architecture in synovial tissue, potentially affecting the generalizability of mechanistic findings.

6. The manuscript does not address whether the neurotrophin-mural cell differentiation pathway is specific to RA or represents a general response to chronic inflammation and hypoxia, limiting disease specificity claims.

7. TRK inhibitor experiments use concentrations (1-10 µM) that may exceed clinically achievable synovial tissue levels; pharmacokinetic data or tissue penetration studies are not provided.

8. The claim that fibroblast-derived neurotrophins couple vascular remodeling with sensory nerve growth (Discussion) is speculative and not directly tested in this manuscript.

## Questions

1. Do NGF, BDNF, and NT3 protein levels differ between healthy, pre-treatment, and post-treatment RA synovial biopsies, and do they correlate with vascular maturation markers?

2. In the NGFR-overexpressing fibroblasts, does NGFR-TRKA complex form as demonstrated by co-IP, and is this complex required for the enhanced phosphorylation at baseline (without NGF)?

3. What is the relative contribution of PDGF-PDGFR, Ang1-Tie2, and TGFβ-TGFBR signaling to mural cell differentiation in the same RA synovial explants treated with TRK inhibitors?

4. Do TRK inhibitors achieve sufficient synovial tissue penetration at clinically relevant doses to produce the observed effects, and has this been assessed in vivo?

5. Is the persistence of vascular maturation post-treatment specific to the neurotrophin pathway, or do other mural cell-supporting pathways remain active?