# Contribution & Prior-Work Reviewer

Based on my systematic search of the prior-work literature, I can now write the contribution and prior-work review. The searches reveal that while the manuscript cites foundational work on neurotrophins and vascular biology, and builds on the authors' own prior work on NOTCH3 and fibroblasts in RA, the specific connection between neurotrophin signaling and vascular maturation in RA appears to be novel. Let me write the review.

---

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript identifies neurotrophin signaling as a driver of pathological vascular maturation in RA synovial tissue and proposes TRK inhibitors as a therapeutic approach. The work extends the authors' prior findings on NOTCH3-mediated fibroblast differentiation by uncovering a downstream neurotrophin axis. The contribution is real and contextually important for RA biology, but the novelty claim requires scrutiny: the manuscript rests on establishing that neurotrophins *induce* mural cell differentiation from fibroblasts in RA, yet foundational work on neurotrophin roles in vascular development is decades old. The critical question is whether the authors have demonstrated a *new* mechanism in RA, or whether they have applied known neurotrophin biology to a new tissue context.

## Strengths

1. **Spatial transcriptomics on paired pre/post-treatment biopsies** provides direct evidence that vascular maturation persists despite immunosuppression, a clinically important observation that motivates the mechanistic work.

2. **Mechanistic depth across multiple scales**: the manuscript traces a pathway from NOTCH3 → NGF induction → NGFR/TRKA signaling → mural cell differentiation, with supporting evidence from co-culture, genetic knockdown, pharmacologic inhibition, and tissue explants.

3. **Functional validation in human RA tissue explants** with FDA-approved drugs (larotrectinib, entrectinib) demonstrates that the proposed pathway is targetable in the disease-relevant context, not merely in cell lines.

---

## Load-Bearing Weaknesses

### 1. Neurotrophin roles in vascular mural cell development are established; the RA-specific novelty is unclear.

The manuscript's central claim is that "neurotrophin signaling sustains pathological vascular maturation in RA." However, the foundational literature already establishes that neurotrophins regulate mural cell biology. The authors cite TRKB-null mice exhibiting "defects in pericyte migration" (Donovan et al. 2000, ref. 36) and NT3-null mice showing "vascular abnormalities" (Tessarollo et al. 1994, ref. 37; Donovan et al. 1996, ref. 38). These are not new findings. The manuscript does not clearly delineate what is novel about neurotrophin signaling in RA versus what is a known property of neurotrophins being applied to RA tissue.

The critical distinction would be: does RA synovial tissue uniquely activate neurotrophin signaling in mural cells through a mechanism not seen in normal vascular development? Or does RA simply sustain normal developmental neurotrophin signaling pathways in a pathological context? The manuscript shows the latter—that NOTCH3 (which the authors previously linked to RA fibroblasts) induces NGF, which then acts on mural cells via known TRK receptors. This is an application of known biology to a new tissue context, not a discovery of a new mechanism. The authors should explicitly state whether the neurotrophin-mural cell axis they describe is RA-specific or a recapitulation of developmental vascular biology in a disease setting.

**What would resolve this**: A direct comparison showing that the neurotrophin signaling pathway in RA synovial mural cells differs qualitatively or quantitatively from the same pathway in normal synovial vasculature or in developing vasculature. Alternatively, identification of a disease-specific upstream trigger (beyond NOTCH3, which is already known to be activated in RA fibroblasts) that uniquely drives neurotrophin signaling in RA.

### 2. The claim that TRK inhibitors "reverse" vascular maturation is supported only by acute ex vivo treatment; durability and mechanism of reversal are not established.

The manuscript shows that 3-day treatment of RA synovial explants with larotrectinib or entrectinib reduces aSMA+ mural cells and PECAM1+ endothelial density (Fig. 6C–G). However, "reversal" implies restoration toward a normal state, not merely acute suppression of a pathological process. The manuscript does not show:

- Whether the reduction in mural cell markers reflects true dedifferentiation of existing mural cells, or selective loss/death of newly differentiated cells, or prevention of further differentiation.
- Whether the effect is reversible (i.e., whether mural cells re-accumulate after drug withdrawal).
- Whether the reduction in vascular density reflects loss of functional blood vessels or merely loss of mural cell coverage while endothelium persists.

The explant system preserves tissue architecture for 3 days (Fig. 4, G–I), but this is a short window. The authors show that neurotrophin stimulation *increases* aSMA expression in explants (Fig. 4K), and that TRK inhibitors *decrease* it, but this is a pharmacodynamic effect in an acute setting, not evidence of reversal of established pathological vascularization. The in vivo durability and clinical relevance of this effect remain unknown.

**What would resolve this**: Time-course data showing whether the effect of TRK inhibitors is sustained or reversible; lineage-tracing or single-cell analysis of explants to determine whether existing mural cells dedifferentiate or are lost; comparison of vascular function (e.g., perfusion, barrier integrity) before and after treatment.

---

## Sweep

1. **NOTCH3 as the initiator of neurotrophin signaling is not entirely novel**: the authors' 2020 Nature paper (ref. 14) already established NOTCH3 as a driver of fibroblast differentiation in RA; the present work extends this by showing NOTCH3 induces NGF, but the NOTCH3→fibroblast crosstalk axis was pre-established.

2. **The NGFR-TRKA potentiation mechanism (Fig. 5G–H) is presented as a discovery but is attributed to prior work** ("it has been suggested that the binding affinity of NGF to TRKA is potentiated through a NGFR-TRKA complex," citing ref. 33); the authors demonstrate this in RA fibroblasts but do not claim to have discovered the mechanism itself.

3. **Spatial transcriptomics data are from a single cohort** (22 RA patients + 2 healthy donors); no independent validation cohort is mentioned, limiting generalizability of the vascular cell type definitions and neurotrophin receptor expression patterns.

4. **The claim that neurotrophin signaling couples vascular remodeling with sensory nerve growth** (Discussion) is speculative and not directly tested; the authors cite their own prior work (ref. 15, Orange et al. 2023) on fibroblast-nerve interactions but do not experimentally link the neurotrophin axis to innervation in this manuscript.

5. **TRK inhibitor specificity is not addressed**: larotrectinib and entrectinib inhibit TRKA, TRKB, and TRKC; the manuscript does not determine which TRK isoform(s) are responsible for the vascular effect, limiting mechanistic clarity and potential for isoform-selective targeting.

6. **The manuscript does not address why immunosuppression fails to reverse vascular maturation**: the authors show that TNFi and csDMARDs do not reduce mural cell density (Fig. 1G–H), but do not test whether these therapies suppress neurotrophin production or NOTCH3 signaling, which would be necessary to understand why the neurotrophin axis persists despite immune suppression.

---

## Questions

- In normal synovial tissue or developing vasculature, is the NOTCH3→NGF→NGFR/TRKA→mural cell pathway active, and if so, how does its activity in RA differ quantitatively or qualitatively?
- Do larotrectinib or entrectinib reduce vascular density in healthy donor synovial explants, and if so, to what extent, to establish whether the effect is RA-specific or reflects general suppression of vascular maturation?
- Figure 5J shows RNA-seq of NGFR-overexpressing fibroblasts; were these cells derived from RA or healthy donors, and do healthy fibroblasts show the same gene signature upon NGFR overexpression?