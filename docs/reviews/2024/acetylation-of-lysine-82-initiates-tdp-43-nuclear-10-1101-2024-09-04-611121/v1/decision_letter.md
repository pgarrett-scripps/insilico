# Decision Letter

**Decision:** major

## Summary of Evaluation
The manuscript identifies K82 acetylation within the TDP‑43 bipartite NLS as a modification that disrupts importin‑α1 binding and nuclear import, and presents preliminary evidence that this modification is elevated in sALS motor cortex. The core experimental design (unbiased proteomics, mutagenesis, peptide-binding assays, rescue by PY‑NLS swap) is sound. However, the statistical analysis of the nuclear proteome screen lacks multiple‑testing correction, the central claim that K82 acetylation 'initiates' the cascade outruns the evidence (no temporal order established, glutamine mimics rather than endogenous acetylation, cross‑sectional human tissue data), and several quantitative claims are unsupported (25% expression level lacks densitometry). Multiple HARD reproducibility gaps (missing MS spectra, no repository accession, no IACUC statement, incomplete resource tables, unspecified software versions) must be closed. The aggregate panel signal (confidence‑weighted 2.53/5, with 4/8 reviewers recommending rejection) reflects these unresolved issues. Nevertheless, the biological model is plausible and the peptide‑binding and mutagenesis data provide a strong sufficiency argument. Major revision addressing the statistical, interpretive, and reproducibility gaps—with the causal framing softened—could bring the manuscript to an acceptable standard. The required revisions are concrete and checkable; none require new lines of experimentation that would fundamentally change the paper's scope.

## Required Revisions
1. 1. Soften causal claims throughout. Replace 'initiates' in the title, abstract, and discussion with language reflecting correlation and sufficiency (e.g., 'triggers', 'is sufficient to disrupt', 'is associated with'). Explicitly state in the Discussion that the human tissue data are cross-sectional and cannot distinguish initiation from consequence.
2. 2. Address the multiple‑testing problem in the nuclear proteome screen (Fig. 1E). Re‑analyse the TMT data with an appropriate FDR correction (e.g., Benjamini‑Hochberg q<0.05) and report the number of proteins that survive correction and the rank/adjusted p‑value of TDP‑43. If few or no proteins survive, state this limitation and adjust the claim accordingly.
3. 3. Provide densitometric quantification for the claim that 'TDP‑43‑K82R … induced TDP‑43 mislocalization even when accumulated at only 25% the level of endogenous TDP‑43 (Fig. S4A)'. Show the individual values, error bars, and the calculation supporting the 25% figure.
4. 4. Provide annotated MS/MS spectra for all reported post‑translational modifications within the TDP‑43 cNLS (acetylation at K79, K82, K84; ubiquitination; phosphorylation at S91/92) and deposit the raw mass spectrometry data in a public repository (e.g., PRIDE or MassIVE) with an accession number included in the manuscript.
5. 5. Repeat the key mislocalization experiments (immunofluorescence and live‑cell imaging) at the dose that produces ~50% proteasome inhibition (2 nM BTZ) in Figures 1C–D and 1E, or clearly state in the figure legends and Results that the 20 nM dose was used and provide evidence that it also yields partial (~50%) inhibition at that dose in your system.
6. 6. Add a quantified, statistical comparison of the ac‑K82 immunoblot signals from the human motor cortex samples (Fig. 5B), including densitometry normalized to total TDP‑43, individual values, effect size, and a test (e.g., Mann‑Whitney U). Limit the conclusion to what the sample size (6 sALS, 4 controls) supports, and discuss the cross‑sectional, correlative nature of the data.
7. 7. Provide quantification of the stathmin‑2 cryptic splicing results (Fig. 1G) as qRT‑PCR data with statistics, or as a quantified gel with error bars, to support the claim of TDP‑43 loss of function.
8. 8. For all co‑immunoprecipitation experiments, include a negative control IP (e.g., IgG or beads alone) and provide quantification across biological replicates (e.g., band intensity ratios) with appropriate statistical tests.
9. 9. Provide an IACUC approval statement (with protocol number) for the mouse experiments in Fig. S1A, or a statement that the tissue was obtained from an approved source.
10. 10. Provide a funding disclosure and a competing‑interests declaration.
11. 11. Document the generation of the TDP‑43‑Clover homozygous knock‑in cell line: parental line, editing strategy (gRNA sequences, Cas variant), number of clones screened, validation of homozygosity (e.g., PCR, sequencing), and mycoplasma testing status.
12. 12. Provide full, uncropped immunoblots for all key figures (including molecular weight markers) as a supplementary file, and deposit source data for blots and micrographs in a public repository (e.g., Figshare).
13. 13. State the software versions used for RawConverter, DTASelect2, Census2, MaxQuant/Proteome Discoverer, the R package used for the volcano plot, and image‑quantification software.
14. 14. Provide the target sequences for the human TDP‑43 siRNAs used.
15. 15. Provide strain, source, sex, and group sizes for the mice used in Fig. S1A.
16. 16. State the vehicle (e.g., DMSO) and its final concentration for all drug treatments.
17. 17. Provide a data‑availability statement.
18. 18. Discuss and differentiate the findings from Ko et al. (2024) explicitly in the Discussion, stating what the present work adds over that prior report.

## Minor Suggestions
- Figure 1C-D: state the effective proteasome inhibition at the dose actually used for imaging (20 nM BTZ) or repeat the experiment at 2 nM.
- Peptide-binding assay (Fig. 3F): provide number of replicates and a statistical comparison (e.g., AUC or endpoint binding at a high concentration) across conditions.
- Overlay individual data points on all bar graphs (Figs. 1D, 3D, 4E, 4G, and related supplementary panels).
- Specify the choice between data-dependent and data-independent acquisition in the PTM mass spectrometry methods.
- Add the sequential siRNA+transduction protocol to the Methods section rather than only in figure legends.
- Add a biosafety approval statement for lentiviral work if applicable.
- Provide the number of cells/fields imaged per condition and the number of independent differentiations for all quantification of TDP-43 nuclear fluorescence.
- Cite the original derivation or consent status of the WTC11 iPSC line.
- Shorten the 68‑word sentence beginning 'While a proportion of importin‑α1…' for readability.