# Methodology Reviewer

SCORE: 3  
CONFIDENCE: 4  

## Summary

The central design question is whether the time-resolved TurboID proteomics and the Git1 loss-of-function experiments support the conclusion that Git1 facilitates Grk2 translocation into the cilium, enabling Smo phosphorylation and downstream Hh signaling. The proteomic screen is well-constructed, with appropriate negative controls (no-biotin, no-Shh) and a stable cell line selected for near-endogenous Smo expression. The Git1 knockout and knockdown experiments are internally consistent and the ciliary Grk2 rescue is a strong design element. However, the causal chain from Git1 loss to reduced Smo phosphorylation rests on a single antibody-based readout and on Grk2 localization data that may be confounded by overexpression. The claim that Git1 is required for Grk2 ciliary entry is not fully earned by the data as presented.

## Strengths

1. The Smo-TurboID cell line was carefully screened for near-endogenous expression and lack of constitutive pathway activation, which is a genuine methodological strength.
2. The time-resolved design with multiple Shh time points and matched no-biotin controls is appropriate for capturing transient Smo-proximal interactions.
3. The ciliary-targeted Grk2 rescue experiment (Grk2-V5-DArl13b) is a well-designed test of the causal role of ciliary Grk2 in Git1-null cells.

## Weaknesses

### Load-bearing

**1. The claim that Git1 is required for Grk2 translocation into the cilium is not established by the Grk2 localization data.** The manuscript reports that in Git1-null cells, Grk2 levels at the basal body are slightly lower than WT, and that no detectable Grk2 is observed in the cilium at any time point after Shh stimulation. However, the Grk2 signal is measured from lentivirally expressed Grk2-V5, not endogenous Grk2. If the transgene is expressed at levels that are already near the detection threshold in WT cilia (the reported WT increase is only 1.2-fold), then the absence of signal in Git1-null cilia could reflect a sensitivity floor rather than a true absence of translocation. The authors do not report the expression level of Grk2-V5 relative to endogenous Grk2, nor do they show that the Grk2-V5 construct is functional (e.g., that it can rescue Smo phosphorylation in a Grk2-null background). A positive control showing that the Grk2-V5 construct is capable of ciliary localization and Smo phosphorylation in WT cells under the same imaging conditions would distinguish "no translocation" from "below detection." This is the key experiment that would settle the claim.

**2. The conclusion that Git1 loss reduces Smo phosphorylation in the cilium rests on a single phospho-specific antibody, with no orthogonal validation.** The pSmo antibody (7TM0239A-IC) is used for both immunofluorescence and the conclusion that Git1-null cells fail to phosphorylate Smo. The manuscript does not report validation of this antibody in Git1-null cells (e.g., peptide competition, or a Grk2-inhibitor control). If the antibody's signal depends on Smo conformation or ciliary accumulation rather than phosphorylation per se, the reduced pSmo signal in Git1-null cilia could reflect a change in Smo state rather than a loss of Grk2-mediated phosphorylation. A Western blot of total Smo and pSmo from cilia-enriched fractions, or a phospho-site-specific rescue experiment, would corroborate the immunostaining result.

**3. The claim that Git1 is a Smo-proximal protein is supported only by TurboID biotinylation, not by a direct interaction.** The manuscript states that co-immunoprecipitation of Smo and Git1 was attempted and failed, and the TurboID result shows Git1 biotinylation that is only slightly increased after Shh. This is consistent with Git1 being in the vicinity of Smo, but it does not establish that Git1 and Smo interact directly, nor that the interaction is regulated by Hh signaling. The subsequent functional experiments (Git1 knockout, Grk2 localization) are the real evidence for Git1's role, but the proteomic claim that Git1 is a "Smo interactor" should be hedged accordingly.

### Sweep

- The PKA-C ciliary recruitment time course (Fig. 3) uses the Smo-TurboID cell line, which the authors acknowledge has slightly elevated Smo levels; the claim that PKA-C recruitment is Hh-dependent would be stronger if confirmed in a cell line with strictly endogenous Smo levels.
- The Git1 knockout clones were selected for complete loss of Git1 protein, but the manuscript does not report whether the two clones have identical genetic lesions or whether they were independently derived; if they are sister clones, the "two clones" claim is weaker.
- The Gli2 ciliary tip quantification (Fig. 6E-F) is reported as a single intensity measurement; the manuscript does not specify whether the measurement is restricted to the tip versus the whole cilium, which is a known distinction in the field.
- The GNP experiments use shRNA knockdown rather than genetic knockout, and the manuscript does not report the knockdown efficiency at the protein level (only transcript level), which leaves open the possibility of residual Git1 function.
- The rescue experiment (Grk2-V5-DArl13b) restores Gli1 transcription but not Smo phosphorylation or PKA-C recruitment; the manuscript does not show that the rescue is specific to ciliary Grk2 versus a general effect of Grk2 overexpression.

## Questions

1. What is the expression level of Grk2-V5 relative to endogenous Grk2 in the cells used for the localization experiments, and can the Grk2-V5 construct rescue Smo phosphorylation in a Grk2-null background?
2. Can the pSmo antibody signal be validated by peptide competition or by a Grk2 inhibitor control in Git1-null cells?
3. Are the two Git1-null clones independently derived, and do they carry distinct genetic lesions?
4. For the Gli2 tip measurement, is the intensity quantified only at the ciliary tip or across the entire cilium?