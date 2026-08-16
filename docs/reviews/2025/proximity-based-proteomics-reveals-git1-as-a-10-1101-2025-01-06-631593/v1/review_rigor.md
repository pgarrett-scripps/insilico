# Rigor & Overclaiming Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This is a solid, well-executed proximity-proteomics study that identifies Git1 as a novel regulator of Grk2-mediated Smo phosphorylation in the primary cilium. The core claim — that Git1 is required for Grk2 translocation into the cilium and thereby for Smo phosphorylation and downstream Hh signaling — is supported by convergent genetic, imaging, and rescue experiments. However, several load-bearing claims are worded more strongly than the evidence licenses, particularly regarding the site of Grk2 phosphorylation and the causal chain from Git1 loss to reduced Hh signaling. The manuscript would benefit from targeted re-analysis and re-hedging rather than new experiments.

## Strengths

1. The time-resolved TurboID design is thoughtful and the validation of the Smo-TurboID cell line (expression level, no constitutive activation, cilium morphology) is exemplary.
2. The Git1 knockout phenotype is internally consistent across multiple readouts (pSmo, PKA-C, Gli1, Gli3R, Gli2 tip localization, GNP proliferation).
3. The ciliary-rescue experiment (Grk2-DArl13b restoring Gli1 in Git1-null cells) is a strong causal test that directly supports the proposed mechanism.

## Weaknesses

### Load-bearing

**1. HARD: "the cilium as the primary site where this phosphorylation occurs" (Abstract) is not established by the data.** The evidence is: (a) Git1 loss blocks Grk2 ciliary entry and also blocks Smo phosphorylation; (b) artificially tethering Grk2 to the cilium rescues signaling. But (a) is equally consistent with Git1 acting at the basal body to enable Grk2 to phosphorylate Smo *en route* to or at the base of the cilium — the pSmo antibody staining cannot resolve whether phosphorylation occurs in the ciliary shaft versus the ciliary base, and the imaging shown does not report sub-ciliary localization of pSmo. The rescue (b) shows ciliary Grk2 is *sufficient* for signaling, not that it is the *physiological* site. The claim that the basal-body Grk2 pool "is less likely contributing" (Discussion) is an inference from a negative (no Grk2 in cilium in Git1-null) that does not exclude basal-body phosphorylation followed by Smo transport into the cilium. To support the "primary site" claim, the authors would need to show pSmo is absent from the cilium when Grk2 is retained at the basal body but Smo is present — or re-hedge to "Grk2 entry into the cilium is required for Smo phosphorylation."

**2. HARD: "Loss of Git1 diminishes Hh signaling" is presented as a Git1-specific effect, but the Gli1 reduction in Git1-null cells is partial (~50-70% reduction), and the manuscript does not exclude a contribution from Git1's known ArfGAP activity on Smo trafficking or receptor recycling.** The authors note Git1 is biotinylated by Smo-TurboID before Shh stimulation (Fig. 4B), and Git1 is known to regulate GPCR endocytosis. The reduced Gli1 could reflect impaired Smo plasma-membrane retention (a trafficking phenotype) rather than (or in addition to) the Grk2-phosphorylation defect. The rescue experiment with ciliary Grk2 partially restores Gli1 but does not restore it to WT levels (Fig. 6H shows a significant but incomplete rescue), which is consistent with an additional Git1 function. The claim "Git1 regulates Hh signaling via controlling Grk2 transport into the cilium" (Discussion) is therefore over-strong; it should be "via, at least in part."

**3. SOFT: "Git1 localizes to the base of the primary cilium" (Abstract) — the localization data show YFP-Git1 at the centrosome/basal body, but the manuscript does not demonstrate Git1 at the ciliary base specifically (the transition zone or distal appendages) versus the centrosome generally.** The images (Fig. 4C) show overlap with pericentrin, which marks the entire centrosome. The functional claim (Git1 facilitates Grk2 entry) does not require a specific sub-centrosomal localization, but the wording "base of the primary cilium" implies a more precise localization than is shown.

### Sweep

- The claim that "the majority of known Smo-associated proteins" were recovered (Results) is not quantified — how many of the previously reported interactors were detected, and were any known interactors absent?
- The statement that Git1 loss "has no impact on ciliogenesis" is based on cilium length only; ciliary composition or function was not assessed.
- The GNP experiments use shRNA knockdown, not knockout, and the ~50-70% reduction in Gli1 in GNPs is attributed to Git1 without testing whether the residual Grk2 function explains the incomplete phenotype.
- The "time-resolved" aspect of the proteomics is under-exploited: the 15-min time point is described as capturing "initial transport" but no transport-related candidates are validated.
- The claim that PKA-C is "retained" in the cilium by active Smo (Fig. 3) is supported, but the cyclopamine control shows Smo accumulation without PKA-C — this is a good control, yet the text does not acknowledge that cyclopamine-treated Smo may be in a different conformational state than inactive Smo at the plasma membrane.

## Questions

1. Can the authors report the sub-ciliary distribution of pSmo (ciliary shaft vs. base) in WT cells, and does Grk2-DArl13b rescue produce pSmo in the same compartment?
2. Is the incomplete Gli1 rescue in Git1-null cells (Fig. 6H) statistically different from WT levels, and does the authors' model predict full rescue?
3. Were any known Smo interactors (e.g., β-arrestin, Kif7, Sufu) absent from the proteomic list, and if so, how does that affect the interpretation of the dataset's completeness?