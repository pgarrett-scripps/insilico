# Contribution & Prior-Work Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

The manuscript makes a real and substantial contribution by identifying neurotrophin signaling as a NOTCH3-dependent pathway sustaining pathological vascular maturation in RA synovial tissue, and by demonstrating that FDA-approved TRK inhibitors can reverse this process ex vivo. The core finding—that fibroblasts differentiate into mural cells via neurotrophin signaling—is novel in the RA context and mechanistically interesting. However, the work is situated within an existing framework (the authors' own 2020 Nature paper on NOTCH3 in RA fibroblasts) and the neurotrophin-vascular biology connection, while not previously described in RA, rests on established biology in other tissues. The contribution is solid and publishable but incremental rather than transformative.

## Strengths

1. The spatial transcriptomic analysis of paired pre- and post-treatment RA synovial biopsies is comprehensive and reveals a clinically important finding: vascular maturation persists despite immunosuppression, establishing a treatment-resistant stromal compartment.

2. The mechanistic pathway is well-dissected through complementary approaches (spatial transcriptomics, RNAscope, immunohistochemistry, co-culture, siRNA knockdown, lentiviral overexpression, and organoid models) that converge on NOTCH3 → NGF induction → NGFR/TRKA sensitization.

3. The therapeutic repurposing angle is pragmatic: demonstrating that larotrectinib and entrectinib reduce vascular maturation in human RA tissue explants provides a concrete path toward clinical translation.

## Weaknesses: Load-Bearing Claims

**Claim 1: Neurotrophins induce fibroblast-to-mural-cell differentiation in RA.**

The evidence is that NGF, BDNF, and NT3 stimulation of cultured synovial fibroblasts upregulates mural cell markers (ACTA2, MYH11, RGS5, CNN1) and that fibroblasts acquire contractile function (collagen gel contraction assay, Fig. 4D–F). However, marker upregulation does not establish true differentiation into functional mural cells. The contractility assay shows only modest effects (16–21% contraction for BDNF/NT3; NGF shows no significant effect, Fig. 4F). The critical gap: the manuscript does not demonstrate that these fibroblasts acquire the full phenotype and function of native pericytes or VSMCs—only that they express some markers and show limited contractility. Alternatively, neurotrophins could induce a partial, transient phenotypic shift without stable differentiation. The synovial explant experiments (Fig. 4K) show increased aSMA staining around vasculature after neurotrophin stimulation, but this is a static readout and does not prove the cells are newly differentiated fibroblasts rather than activation of existing mural cells or recruitment of circulating precursors. What would settle this: lineage tracing in explants or in vivo to confirm fibroblast origin of the aSMA+ cells, or single-cell RNA-seq of explant-derived mural cells before and after neurotrophin treatment to show a transcriptional trajectory from fibroblast to mural state.

**Claim 2: NOTCH3 initiates neurotrophin signaling by inducing NGF expression.**

The evidence is that NOTCH3 siRNA or CRISPR knockout reduces NGF expression in fibroblast-endothelial co-cultures (Fig. 5D–E), and that DLL4 (a NOTCH ligand) upregulates NGF (Fig. 5C). However, this does not establish that NOTCH3 is the *primary* or *sole* initiator of NGF in RA synovia. The manuscript shows NOTCH3 is *sufficient* to induce NGF in vitro, but the in vivo spatial transcriptomic data (Fig. 5K–M) show NGF/NGFR gene signature enrichment co-localized with NOTCH3, which is correlative. The alternative explanation: endothelial cells or other stromal cells produce NGF independently, and NOTCH3 merely amplifies or sustains it. The manuscript does not rule out baseline NGF production in the absence of NOTCH3 signaling or test whether blocking NOTCH alone (without blocking neurotrophins) is sufficient to deplete NGF in intact RA tissue. What would settle this: quantify NGF mRNA and protein in NOTCH3-knockout versus wild-type fibroblasts in the absence of endothelial co-culture, and measure NGF levels in DAPT-treated RA explants at multiple time points to establish whether NOTCH inhibition durably suppresses NGF or only transiently reduces it.

**Claim 3: TRK inhibitors reverse pathological vascular maturation in RA.**

The evidence is that larotrectinib and entrectinib reduce aSMA intensity (36–40%, Fig. 6E–F) and PECAM1+ vascular density (50–54%, Fig. 6G) in RA synovial explants after 3 days of treatment. However, this is an ex vivo system with a short treatment window, and the reduction in vascular density could reflect loss of endothelial cell viability or detachment rather than reversal of mural cell maturation. The manuscript does not report endothelial cell viability or PECAM1+ cell counts in control versus drug-treated explants separately; the PECAM1 quantification conflates vascular area with endothelial cell number. Additionally, the explants are from established RA tissue; it is unclear whether TRK inhibition can prevent *de novo* vascular maturation (as occurs during active inflammation) or only reverse already-mature vessels. The reduction in aSMA is modest and could represent partial dedifferentiation or apoptosis of mural cells rather than true reversal of maturation. What would settle this: (1) report PECAM1+ cell counts and viability markers (e.g., cleaved caspase-3) separately in control and drug-treated explants; (2) perform time-course experiments to determine whether TRK inhibition prevents maturation of newly forming vessels in inflamed explants, not just reduces density of established vessels; (3) use single-cell RNA-seq to characterize the transcriptional state of mural cells after TRK inhibition to confirm they revert to a fibroblast-like state rather than undergoing apoptosis.

## Weaknesses: Sweep

1. The manuscript cites its own 2020 Nature paper (ref. 14) establishing NOTCH3 in RA fibroblast differentiation but does not clearly delineate what is new here: the prior work showed NOTCH3 drives fibroblast identity; this work adds that NOTCH3 also drives neurotrophin signaling and mural cell differentiation, but the mechanistic novelty is the NOTCH→neurotrophin link, not NOTCH itself.

2. A 2025 preprint (Chalkidi et al., "Notch3 regulates pericyte phenotypic plasticity in colorectal cancer") describes NOTCH3 regulation of pericyte phenotype in a different tissue context, suggesting the NOTCH3-pericyte axis is not unique to RA and should be cited to contextualize the contribution.

3. A 2025 preprint (Luo et al., "Brain-derived neurotrophic factor supports pericyte and vascular homeostasis in the aging brain") demonstrates BDNF-dependent pericyte homeostasis, directly overlapping with the manuscript's claim that BDNF induces mural cell differentiation; the manuscript does not cite or discuss this work.

4. A 2014 paper (Ly et al., *Arthritis Research & Therapy*) reports neurotrophins are expressed in giant cell arteritis lesions and may contribute to vascular remodeling, establishing that neurotrophins have a vascular role in inflammatory arthritis; the manuscript does not cite this prior work in arthritis.

5. The claim that NGFR potentiates TRKA signaling (Fig. 5G–H) relies on overexpression in cultured fibroblasts; the physiological relevance is unclear because endogenous NGFR and TRKA expression in RA synovial tissue is low (acknowledged in the text), raising the question of whether the NGFR-TRKA complex is the operative mechanism in vivo or an artifact of overexpression.

6. The manuscript does not address why neurotrophins, which are canonically neuronal factors, are produced by fibroblasts in RA; the Discussion mentions coupling of vascular and neural remodeling but does not explain the evolutionary or functional logic of fibroblast-derived neurotrophins in a non-neural tissue.

7. The spatial transcriptomic analysis is limited to 22 RA patients and 2 healthy donors; the generalizability to other RA cohorts or to other inflammatory arthropathies is not established.

8. The therapeutic window for TRK inhibitors in RA is not explored: the manuscript shows ex vivo efficacy but does not discuss potential toxicity, off-target effects, or whether systemic TRK inhibition would be tolerable in RA patients already on immunosuppression.

## Questions

1. Figure 5J (RNA-seq of NGFR-overexpressing fibroblasts) shows upregulation of mural cell genes; were these cells also tested for contractility or other functional mural cell properties to confirm they are not just expressing markers?

2. In the synovial explant experiments (Fig. 4K, Fig. 6C–G), were the fibroblasts and endothelial cells confirmed to remain viable and in their original spatial relationship after 3 days of culture, or could the observed changes reflect cell death or tissue degradation?

3. The manuscript states that NOTCH3 expression persists in post-treatment RA synovia (Fig. 2A); if NOTCH3 is the driver of neurotrophin signaling, why does immunosuppressive therapy not reduce NOTCH3 expression, and what maintains NOTCH3 signaling in treated patients?