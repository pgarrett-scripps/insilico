# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling via NOTCH3-dependent fibroblast differentiation sustains pathological vascular maturation in RA synovia despite immunosuppressive therapy, and that FDA-approved TRK inhibitors can reverse this maturation ex vivo. The core claims are substantially supported by the spatial transcriptomic data and mechanistic experiments, but the causal architecture rests on correlational observations and ex vivo models that do not fully establish the in vivo mechanism or clinical relevance. The work makes a solid incremental contribution to understanding stromal drivers of RA pathology, but several load-bearing claims require either narrower framing or additional evidence.

## Strengths

1. High-dimensional spatial transcriptomics on paired pre- and post-treatment RA biopsies provides robust characterization of persistent vascular maturation that conventional immunosuppression does not reverse.

2. Mechanistic pathway is traced through multiple complementary approaches: spatial mapping, single-cell knockdown, pharmacologic inhibition, and lentiviral overexpression, with consistent directionality across methods.

3. Demonstration that FDA-approved TRK inhibitors reduce mural cell markers and vascular density in human RA explants offers a concrete therapeutic lead grounded in existing clinical tools.

## Major Weaknesses: Load-Bearing Claims

**Claim 1: Neurotrophin signaling from fibroblasts drives mural cell differentiation in RA synovia.**

The evidence for this claim rests on three pillars: (i) spatial co-localization of neurotrophin receptors on mural cells with NOTCH3+ fibroblasts; (ii) in vitro differentiation of cultured fibroblasts into mural cells upon neurotrophin stimulation; and (iii) reduction of mural cell markers in explants treated with TRK inhibitors. However, the causal direction is not established. The spatial data show that mural cells express neurotrophin receptors and that NOTCH3+ fibroblasts are nearby, but proximity does not prove fibroblasts are the source of neurotrophins or that receptor-bearing mural cells are responding to fibroblast-derived ligands rather than endothelial or immune cell sources. The in vitro experiments use cultured fibroblasts isolated from RA tissue, which may not recapitulate the in vivo microenvironment or the cell-cell interactions that govern differentiation in intact synovia. The explant experiments show that TRK inhibition reduces aSMA and mural cell markers, but this is consistent with any neurotrophin source (endothelial, immune, fibroblast) and does not isolate the fibroblast contribution. A fibroblast-specific knockout of NGF or NGFR in explants, or selective depletion of fibroblasts followed by neurotrophin add-back, would distinguish fibroblast-driven from bystander neurotrophin signaling.

**Claim 2: NOTCH3 signaling in fibroblasts initiates neurotrophin production and sensitizes them to NGF via NGFR transactivation.**

The evidence shows that DLL4 stimulation upregulates NGF expression in cultured fibroblasts (Fig. 5C), that DAPT or NOTCH3 knockout blocks this (Fig. 5D–E), and that NGFR overexpression enhances TRKA phosphorylation at low NGF concentrations (Fig. 5G–H). These results are internally consistent and well-controlled. However, the claim that NOTCH3 "initiates" neurotrophin signaling conflates two separate observations: (i) NOTCH3 induces NGF production, and (ii) NGFR potentiates TRKA signaling. The first is shown in cultured fibroblasts stimulated with a NOTCH ligand; the second is shown in fibroblasts overexpressing NGFR. Neither experiment demonstrates that endothelial NOTCH ligands in vivo trigger this cascade in fibroblasts, or that the NGFR-TRKA complex is the rate-limiting step in vivo rather than NGF availability or NOTCH ligand availability. The spatial enrichment of an NGF/NGFR gene signature near NOTCH3+ fibroblasts (Fig. 5K–M) is suggestive but correlational. A co-culture experiment in which endothelial cells are co-cultured with fibroblasts and mural cells, with and without NOTCH inhibition, measuring NGF secretion and mural cell differentiation, would test whether endothelial NOTCH signaling drives the full cascade.

**Claim 3: Persistent vascular maturation in post-treatment RA is a treatment-resistant pathological feature that can be reversed by TRK inhibitors.**

The spatial data convincingly show that mural cell density and vascular maturation markers persist or increase 6 months after immunosuppressive therapy (Fig. 1G–H). However, the claim that this is "pathological" and "treatment-resistant" rests on the assumption that vascular maturation is harmful in RA. The manuscript does not establish whether mature vasculature drives inflammation, joint damage, or clinical outcomes, or whether its persistence correlates with treatment failure or poor prognosis. The explant experiments show that TRK inhibitors reduce aSMA and PECAM1 in ex vivo tissue, but explants are not perfused, do not contain circulating immune cells, and lack the systemic inflammatory milieu of active RA. The reduction in vascular density in explants does not establish that TRK inhibition would reverse vascular maturation in vivo or improve clinical outcomes. The claim that TRK inhibitors "reverse" vascular maturation is supported only by ex vivo data; in vivo efficacy and the functional consequence of reduced vascular maturation remain unknown.

## Minor Weaknesses: Sweep

1. The 6-month treatment window is relatively short; longer follow-up would strengthen the claim that vascular maturation is truly "persistent" rather than slowly resolving.

2. The manuscript does not report whether patients with clinical remission (DAS28-ESR < 2.6) differ from non-remitters in vascular maturation, which would test whether vascular changes are independent of systemic inflammation.

3. The spatial transcriptomic panel covers 5K genes; it is unclear whether the neurotrophin receptors and ligands are expressed at levels sufficient to drive the observed phenotypes, or whether expression levels correlate with functional activity.

4. The fibroblast-endothelial co-culture uses a 1:3 ratio; the sensitivity of the results to this ratio is not explored, and it is unclear whether this ratio reflects in vivo stoichiometry.

5. The collagen gel contraction assay (Fig. 4D–F) shows that NT3 and BDNF, but not NGF, enhance contractility; this dissociation is not explained and raises questions about the functional significance of NGF-induced pericyte differentiation.

6. The manuscript claims that fibroblast-derived neurotrophins may "couple" vascular remodeling with sensory nerve growth, but this is speculative and not tested.

## Questions

1. **Figure 1G–H**: Do patients who achieved clinical remission (DAS28-ESR < 2.6) show different vascular maturation trajectories than non-remitters, and does this differ by treatment arm (csDMARD vs. TNFi)?

2. **Figure 5**: In the co-culture system, what is the relative contribution of endothelial-derived vs. fibroblast-derived NGF to mural cell differentiation, measured by selective neutralization or genetic deletion?

3. **Figure 6**: Do TRK inhibitors reduce vascular maturation in RA explants from patients who achieved clinical remission, or only in those with persistent inflammation?

4. **Methods**: What is the range of NGFR, NTRK1, NTRK2, and NTRK3 expression levels (transcripts per cell or normalized counts) in mural cells vs. fibroblasts, and do these levels correlate with responsiveness to neurotrophin stimulation?

---

## Assessment from Specialty

The manuscript makes a credible case that neurotrophin signaling is associated with mural cell expansion in RA synovia and that TRK inhibition can suppress this in ex vivo tissue. The spatial transcriptomics are of high quality and the mechanistic pathway is plausible. However, the causal claim that fibroblasts drive mural cell differentiation via neurotrophins rests on correlational spatial data and in vitro models that do not exclude alternative sources of neurotrophins or alternative mechanisms of mural cell recruitment. The clinical relevance of reversing vascular maturation is not established, and the in vivo efficacy of TRK inhibitors remains untested. The work is suitable for publication with major revision to narrow claims about causality and to clarify the distinction between what is shown in vitro and what remains to be tested in vivo.