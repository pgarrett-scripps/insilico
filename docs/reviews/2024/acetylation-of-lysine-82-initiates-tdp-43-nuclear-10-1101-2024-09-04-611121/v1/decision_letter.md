# VERDICT: major

## Summary of Evaluation

This manuscript proposes that an age-associated decline in proteasome activity drives acetylation of lysine 82 within the bipartite classical NLS of TDP-43, abolishing importin-α1 recognition and producing nuclear loss of function — the initiating step of TDP-43 proteinopathy. The panel was uniformly positive about the quality of the experimental work, and I share that assessment. The strongest elements are: (i) the unbiased TMT nuclear proteomics identifying TDP-43 as the most depleted nuclear protein after partial proteasome inhibition, which converts an assumption of specificity into a measurement; (ii) the systematic K→R mutagenesis panel across the bipartite NLS, which establishes that K82 is necessary but not sufficient and that K82 plus K95 or K97 restores importin-α1 binding — a genuinely new and well-resolved map of this NLS; (iii) the peptide–importin-α1 binding assay using *genuinely acetylated* peptides rather than mimics; and (iv) the FUS-PY-NLS swap, which is an elegant orthogonal demonstration that the cNLS is the lesion. The generation of ac-K82 antibodies and their application to sALS motor cortex is a valuable translational extension.

Two problems keep this from a minor-revision decision.

**First, the necessity gap.** Every load-bearing experiment demonstrates that K82 acetylation (or a mimic, or an isolated peptide) is *sufficient* to disrupt importin-α1 binding. No experiment shows that acetylation is *necessary* for the mislocalization observed under proteasome inhibition. The advocate's rebuttal in the debate — that the obvious control (an acetylation-resistant K82R construct) is confounded because K82R itself disrupts import (Fig. 4C–E) — is correct and I credit it; it is a genuine structural constraint, not an oversight, and the authors deserve credit for having generated the data that reveals it. But the constraint does not make the gap disappear. An alternative model remains live: proteasome inhibition could deplete nuclear TDP-43 through a mechanism independent of NLS acetylation (for example, sequestration of import machinery by accumulated ubiquitinated substrates), with K82 acetylation an accompanying but non-causal event. The manuscript's own mass spectrometry shows K79/K82/K84 are also *ubiquitinated* under these conditions, which the text notes but never disentangles from acetylation. Because the title and abstract assert causation ("initiates … by disrupting its nuclear import"; "sufficient to initiate"), and because the reader is invited to conclude that the proteasome→acetylation→mislocalization chain has been established, this gap must be closed either by data or by reframing. Notably, a non-confounded experiment does appear feasible and was not attempted: pharmacological manipulation of acetylation (HDAC/sirtuin inhibition to raise, or acetyltransferase inhibition to lower, K82 acetylation) in proteasome-inhibited neurons, read out with the authors' own ac-K82 antibody plus nuclear/cytoplasmic fractionation. Because the outcome of such an experiment could change a conclusion, this is a major revision rather than a minor one. I will accept, as an alternative route, a substantial reframing of the title, abstract and Results to sufficiency-and-correlation language — but the authors should understand that this materially reduces the claim.

**Second, the temporal-precedence claim.** The inference that acetylation precedes phosphorylation (Fig. 5C) rests on ac-K82 appearing in both soluble and insoluble fractions while pS409/410 appears only in the insoluble fraction. Solubility is not a clock. This point was raised by two reviewers and was not defended in the debate. It must be softened or removed; no new experiment is required for that, but it is not optional.

Beyond these, the compliance audits surface a substantial set of items that are individually fixable but collectively significant for a venue whose reviews are public and whose readers will attempt to judge the work from what is provided. Supplementary Tables S1, S2, S3 and S5 are referenced repeatedly but not supplied, which means antibody identities, plasmid maps, primer sequences and the entire clinical metadata for the human cohort are currently unavailable to a reader. The PTM mass spectrometry — the experiment that discovers the modifications on which the whole paper turns — is described in a paragraph that does not state the instrument, the search engine actually used ("MaxQuant or Proteome Discoverer"), the database, the FDR, or the mass tolerances. No proteomics data are deposited. Biological replicate numbers and per-figure statistical tests are largely absent. One cited reference (36) is missing from the bibliography entirely. And the manuscript carries no funding statement, no competing-interests declaration, and no IACUC approval for the mouse tissue in Fig. S1A.

None of these secondary items is grounds for rejection, and I want to be explicit that I regard the underlying science as good work that I expect to see published. The verdict is major because of the necessity experiment and because the PTM MS reporting gap currently prevents a reader from evaluating the discovery step independently.

## Required Revisions

**A. Central claim: necessity versus sufficiency**

1. **Test whether K82 acetylation is necessary for proteasome-inhibition-induced mislocalization, or reframe the causal claim.** Choose one:
   - *(Preferred)* Provide an experiment that manipulates K82 acetylation without mutating K82. For example: treat proteasome-inhibited iPSC-derived neurons with an acetyltransferase inhibitor (or overexpress/activate a candidate deacetylase, e.g. SIRT1, given ref. 35), quantify ac-K82 with your own antibodies, and determine whether nuclear TDP-43 is preserved by fractionation and imaging. A positive result would close the loop; a negative result should be reported and the model adjusted.
   - *(Acceptable alternative)* Revise the title, abstract and Results to state sufficiency rather than initiation — e.g. replace "initiates … by disrupting its nuclear import" with language that acetylation at K82 is *sufficient* to abolish importin-α1 binding and nuclear import, and that acetylation is *associated with* proteasome decline. If this route is taken, add an explicit paragraph in the Discussion stating that necessity was not tested, explaining the K82R confound (Fig. 4C–E) that makes the conventional control uninterpretable, and naming alternative mechanisms by which proteasome inhibition could deplete nuclear TDP-43.

2. **Address ubiquitination explicitly.** Fig. 3B reports ubiquitination as well as acetylation at K79/K82/K84 under proteasome inhibition. State in the Results whether the mass spectrometry can distinguish which modification predominates at K82, and discuss in the Discussion why acetylation rather than ubiquitination is proposed as the operative lesion. If the data cannot separate them, say so.

3. **Soften or remove the acetylation-precedes-phosphorylation claim.** The soluble/insoluble distribution in Fig. 5C is a compartmentalisation observation, not a temporal one. Either remove the precedence inference from the Results, figure legend and Discussion, or restate it as one of at least two interpretations and name the alternative (continuous acetylation of a soluble pool). If you retain any version of the claim, add quantification of the ac-K82 and pS409/410 signals in each fraction for each case.

**B. Methods and data that currently prevent independent evaluation**

4. **Report the PTM mass spectrometry in full.** The current description ("data-dependent or data-independent"; "MaxQuant or Proteome Discoverer") is not sufficient for a reader to judge the discovery on which Figs. 3–5 rest. Provide: instrument model, acquisition mode actually used, search engine and version, database and release, fixed and variable modifications searched, precursor and fragment mass tolerances, FDR threshold and level, localisation-probability threshold for the reported acetylation/ubiquitination/phosphorylation sites, and the number of independent biological replicates. Provide annotated MS/MS spectra for the K79, K82, K84, S91 and S92 modified peptides.

5. **Deposit the proteomics data and supply accession numbers.** Both the TMT nuclear proteome and the PTM datasets should be deposited (ProteomeXchange/PRIDE or equivalent) with accessions stated in the manuscript. Include the full TMT results as a supplementary table (protein, peptide count, fold change, p value).

6. **Supply Supplementary Tables S1, S2, S3 and S5.** These are cited throughout and carry the antibody identities and dilutions, plasmid constructs, clinical metadata and primer/probe sequences. Also provide the siRNA target sequence and vendor, and the exact synthetic peptide sequences used in Fig. 3F and Fig. 5A.

7. **State the statistics for each quantitative figure.** For Figs. 1A, 1D, 1F, 1G, 2E, 2G–H, 3D, 3F, 4E, 4G and 5B: the number of biological replicates and what a replicate is, the number of cells or fields per condition for imaging panels, the test applied, and the error-bar definition. Where "representative" blots are shown (Figs. 1B, 3E, 4C, 5B, S4), state how many independent experiments were performed and provide densitometry with a test where a comparison is being asserted in the text.

8. **Report the multiple-comparison treatment for the nuclear proteome.** State whether an FDR or family-wise correction was applied across the ~5,200 proteins, and whether TDP-43 remains the top-ranked hit after correction. If only unadjusted p values are used, say so plainly in the Results (not only the legend) and temper "the protein whose nuclear localization was the most sensitive" accordingly.

9. **Describe the image quantification.** Name the analysis software and version, the nuclear/cytoplasmic segmentation strategy, background subtraction, and the criterion by which a cell was scored as mislocalized (relevant to the "approximately half of TDP-43 mislocalized within 24 hr" statement).

10. **Report fractionation purity.** Provide the cross-contamination controls for the nuclear and cytoplasmic fractions used in Figs. 1B, S1H, S2B, S2D and 5C (e.g. quantified Lamin B1 in the cytosolic fraction and GAPDH in the nuclear fraction), since the central phenotype is measured by fractionation.

**C. Human cohort and antibody validation**

11. **Provide clinical metadata for all ten cases** (age, sex, postmortem interval, disease duration, site of onset, known ALS genotype where available, and neuropathological staging if determined), and state inclusion/exclusion criteria for both groups. State the test and effect size for the sALS-versus-control comparison in Fig. 5B, or, if the claim is purely categorical (detected in 6/6 versus 0/4), say so explicitly and do not imply a graded relationship.

12. **Add one orthogonal validation of the ac-K82 antibodies in tissue.** ELISA against synthetic peptides establishes epitope specificity but not specificity in a complex lysate. A blocking-peptide competition on the sALS blots (acetylated peptide abolishes signal, unmodified peptide does not) would be sufficient and requires no new tissue. Mass-spectrometric confirmation of the ac-K82 peptide in at least one sALS sample would be stronger.

**D. Compliance and citation integrity**

13. **Add an IACUC statement** for the mouse cortex used in Fig. S1A, naming the institution, committee and protocol number.

14. **Add a funding statement and a competing-interests declaration.** Note that two authors list current affiliations at Altos Labs and Genentech; declare these explicitly.

15. **Add a data-availability statement and a code-availability statement,** and supply Addgene deposit numbers (or an interim mechanism for obtaining plasmids) rather than "will be deposited at the time of publication."

16. **Supply the missing reference 36,** cited in the Discussion but absent from the bibliography.

17. **Verify the attribution to reference 33 (Lange et al., 2007).** The Discussion states that your findings "challenge an earlier hypothesis" that lysines in the NLS act "primarily through positive charge." Confirm that Lange et al. makes this claim, and quote or paraphrase the relevant passage; if the hypothesis is instead a general assumption in the field, attribute it as such.

18. **Delineate your contribution from Ko et al. (2024, ref. 30).** That work is cited only in passing as "consistent with a recent report" for the K82Q result. State clearly what Ko et al. reported and which of your findings (the K→R mutagenesis map, the acetylated-peptide binding data, the proteasome linkage, the patient-tissue detection) are new relative to it.

## Minor Suggestions

- Justify the choice of ~50% proteasome inhibition against the 20–60% range you measure in sALS cortex (Fig. S1A), and consider showing dose-sensitivity of the mislocalization phenotype.
- Report whether BTZ, MG132 and MRZ produce quantitatively comparable mislocalization kinetics, or state that they were used only as convergent evidence for the class effect.
- Test whether TDP-43-K82Q recapitulates the stathmin-2 cryptic splicing phenotype seen after BTZ. This would connect the mimic directly to loss of function and would strengthen the paper considerably, but I am not requiring it.
- Name candidate acetyltransferases and deacetylases for K82 and state whether their levels change with proteasome inhibition, even if only as a discussion point.
- Add cell-line authentication and mycoplasma status, RRIDs where they exist, and passage ranges.
- Report the postmortem interval per case and, if available, an indicator of tissue quality, so readers can judge whether ac-K82 variability tracks with sample quality rather than biology.
- Add DOIs or PMIDs to the bibliography.
- The iPSC-derived neurons are cortical rather than motor neurons; a sentence acknowledging this as a limitation would be appropriate given the motor-cortex tissue comparison.
- Note in the Discussion that the ac-K82 variability across sALS cases is currently unexplained and that correlation with clinical or pathological stage is a future question — this is candour, not weakness.

I look forward to seeing a revised version. If the authors elect the reframing route on point 1 rather than the new experiment, please make that choice explicit in the response letter so that it can be assessed directly against the revised title and abstract.