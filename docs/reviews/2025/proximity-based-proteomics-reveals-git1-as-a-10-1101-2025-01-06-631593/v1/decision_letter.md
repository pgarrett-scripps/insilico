# Decision Letter

VERDICT: major

## Summary of Evaluation

This manuscript reports a time-resolved TurboID proximity-labeling proteomics study of Smoothened (Smo), identifying Git1 as a novel regulator of Grk2-mediated Smo phosphorylation in the primary cilium. The work is well-conceived, the Smo-TurboID cell line is carefully validated, and the identification of Git1 as a new player in Hedgehog signaling is genuinely novel — no prior work links Git1 to this pathway. The functional follow-up (Git1 knockout, Grk2 localization, ciliary-targeted Grk2 rescue) is thoughtful and the rescue experiment is a strong causal test.

However, the panel's assessment converges on several load-bearing issues that prevent acceptance as written. The central mechanistic claim — that Git1 controls Grk2 *translocation into the cilium* — is not fully established by the evidence presented. The Grk2 localization data rely on lentivirally overexpressed Grk2-V5 with only a 1.2-fold WT ciliary increase, raising the possibility that "no translocation" in Git1-null cells reflects a detection floor rather than a true biological absence. The manuscript does not report whether the Grk2-V5 construct is functional or its expression level relative to endogenous Grk2. Relatedly, the claim that "the cilium is the primary site" of Smo phosphorylation outruns the data: the evidence shows ciliary Grk2 is *sufficient* for signaling, not that it is the *physiological* site, and basal-body phosphorylation followed by Smo transport is not excluded.

The proteomics resource — a central contribution — is not yet reproducible: raw mass spectrometry data are not deposited, no repository accession is provided, and the normalization/differential-expression pipeline is described in prose without deposited code. The statistical analysis of microscopy quantifications uses cell-level data as independent replicates (pseudo-replication), which inflates apparent significance. Several reagent traceability gaps (Git1 gRNA and shRNA sequences, antibody dilutions, mass spectrometer model) would prevent independent replication.

These issues are substantial but fixable. The core biology is promising and the Git1 finding is novel; the required revisions involve new control experiments, data deposition, and statistical re-analysis rather than a redesign of the study.

## Required Revisions

1. **Establish that the Grk2-V5 construct is functional and that its expression level does not confound the ciliary localization measurements.** Report Grk2-V5 expression relative to endogenous Grk2, and demonstrate that Grk2-V5 can rescue Smo phosphorylation in a Grk2-null background (or equivalent functional validation). Without this, the claim that Git1 controls Grk2 *translocation* (versus a detection artifact) is not supported.

2. **Re-analyze all microscopy quantifications using biological replicates as the independent unit.** For Figs. 3B, 3D, 4E, 4G, 4I, 5D, 5E, 6F, and 7E, report the mean per biological replicate (n=3) and perform the statistical test on those values, or use a mixed-effects model that accounts for clustering. State explicitly whether the reported n is cells or independent experiments.

3. **Deposit the mass spectrometry raw data and analysis code.** Provide a ProteomeXchange/PRIDE accession for the raw files and IP2 search output, active at the time of revision. Deposit the R code for normalization and differential expression (e.g., GitHub with a release tag or Zenodo DOI), including the exact TMM parameters, the "global scaling target" definition, and the eBayes contrasts. Specify the mass spectrometer model and software versions (ProLuCID, DTASelect2, Census2, IP2).

4. **Re-hedge the "primary site" claim.** The data show ciliary Grk2 is sufficient for signaling; they do not establish that the ciliary shaft is the physiological site of Smo phosphorylation. Revise the abstract and discussion to state that "Grk2 entry into the cilium is required for Smo phosphorylation" rather than "the cilium is the primary site." Optionally, report the sub-ciliary distribution of pSmo (shaft vs. base) in WT cells to strengthen the claim.

5. **Provide the missing reagent sequences and traceability information.** Include: (a) the Git1 gRNA sequence and Cas9 delivery method; (b) the Git1 shRNA target sequences (#1 and #2) and the control shRNA sequence; (c) the source or construction details for Smo-HA and Git1-Flag; (d) vendor/catalog numbers for SAG, recombinant ShhN, biotin, and EdU (with concentration); (e) dilutions for all primary antibodies used in NIH3T3 immunofluorescence; (f) the mass spectrometer model; (g) an IACUC protocol number and mouse sex for the GNP work; (h) STR authentication and mycoplasma testing statements for cell lines.

6. **Address the multiple-comparison issue in the proteomics analysis.** Report how many proteins survive a Benjamini-Hochberg correction (FDR < 0.05) at each time point, and provide a supplementary table with adjusted p-values. The current 1.5-fold/p<0.05 threshold without correction is not statistically defensible for ~1070 tests.

7. **Clarify the biotin-labeling timing for the 15-min Shh time point.** State explicitly whether biotin was added simultaneously with Shh (0–15 min) or after 15 min of Shh pre-incubation, and reconcile this with the other time points where biotin was added after Shh had already acted.

## Minor Suggestions

- Label each volcano plot panel in Fig. 2B–C with its time point, and either show GO enrichment per time point or state that the GO analysis pools all post-Shh time points.
- Define "basal body" and "ciliary" regions in Fig. 5C–E legends (e.g., γ-tubulin for basal body, Arl13b for cilium), and state which channel was used for cilium length measurements.
- State in the Fig. 4D–G legend that the pSmo antibody recognizes Grk2 phosphorylation sites on Smo.
- Replace the "(data not shown)" for the Smo–Git1 Co-IP with a deposited supplementary figure or remove the phrase.
- Update ref 18 (Steiner et al., bioRxiv) to the peer-reviewed version if one has appeared, and confirm which source supports the "cerebellar agenesis" claim for Git1-null mice.
- Add a sentence comparing the Smo-TurboID dataset to prior whole-cilium proteomes (Mick 2015, May 2021), stating what the Smo-anchored view adds beyond Smo-specificity.
- State whether the two Git1-null clones are independently derived and carry distinct genetic lesions.
- Specify whether the Gli2 tip measurement is restricted to the ciliary tip or the entire cilium.
- Report the knockdown efficiency of Git1 shRNA at the protein level in GNPs, not just transcript level.
- Ensure error-bar definitions (SD vs. SEM) are consistent across all figure legends, and show variance for control groups set to 1 in qPCR fold-change plots.