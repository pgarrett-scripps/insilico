# Decision Letter

VERDICT: major

## Summary of Evaluation

This manuscript addresses a question of central importance to ALS and related TDP-43 proteinopathies: what initiates the nuclear loss of TDP-43 that precedes cytoplasmic aggregation? The authors propose that age-related decline in proteasome activity leads to acetylation of lysine 82 within the TDP-43 cNLS, disrupting binding to importin-α1 and thereby blocking nuclear import. The work combines quantitative proteomics, systematic mutagenesis, peptide-binding assays, live-cell imaging, and human postmortem tissue analysis. The core mechanistic logic is coherent, and the proteasome-trigger → NLS-acetylation → import-failure axis is a genuinely novel contribution that plausibly connects aging to TDP-43 proteinopathy.

The panel's assessments converged on a clear picture: the work is potentially important and the experimental design is largely sound, but the manuscript as written does not fully support its headline claims. The central issues are:

1. **The acetylation-specificity claim is not secured.** The manuscript's own data show that even the charge-preserving K82R mutation disrupts importin-α1 binding and nuclear localization (Fig. 4C–E). This means the K82Q acetylation mimic does not demonstrate that acetylation *specifically* drives the effect — it demonstrates that *any* perturbation at K82 does. The mass spectrometry identified both acetylation and ubiquitination at K79, K82, and K84, but the peptide-binding assay (Fig. 3F) tested only acetylated and phosphorylated peptides, not ubiquitinated ones. The claim that acetylation specifically initiates the proteinopathy therefore outruns the evidence.

2. **The "initiates" language implies temporal priority that no experiment establishes.** The human data are cross-sectional, and the soluble-versus-insoluble fractionation (Fig. 5C) is a single case and is not a temporal marker. The time-course experiments show mislocalization at 12 hr but do not measure acetylation at time points before mislocalization. The title claim should be requalified to "can initiate" or "is sufficient to initiate."

3. **The translational claim rests on an antibody whose biological specificity is not demonstrated.** The ac-K82 antibody is validated against synthetic peptides (Fig. 5A) and shows increased signal in BTZ-treated neurons (Fig. S5), but no K82R or knockdown control is shown in the immunoblot format used for the sALS tissue (Fig. 5B). Without this, the signal could track total TDP-43 load or cross-react with a co-migrating acetylated species.

4. **The mass spectrometry evidence for the PTM identifications is not inspectable.** No spectra, peptide-level identifications, localization scores, or confidence metrics are shown for the K82 acetylation assignment. The reader cannot verify whether the modification is unambiguously localized to K82 versus a neighboring lysine, nor whether acetylation and ubiquitination calls are distinguished with appropriate mass offsets.

5. **Quantitative reporting is substantially under-specified.** The TMT proteomics experiment lacks stated biological replication; the sALS versus control comparison (Fig. 5B) is presented without statistical analysis; the peptide-binding assay (Fig. 3F) has no error bars, n, or stated comparisons; and multiple figure panels lack n's, tests, and error-bar definitions.

6. **Several HARD procedural gaps prevent reproducibility.** These include missing antibody identifiers, CRISPR reagent sequences, siRNA sequences, mass spectrometry repository accessions, software versions, and mouse strain/source information.

The panel was split (3 minor, 3 major, 2 reject), with the reject votes reflecting the view that the acetylation-specificity problem is fatal as framed. I do not concur with rejection: the model is plausible, testable, and the tools to resolve the objections exist. However, the required fixes go beyond text revision — they require new data (ubiquitinated-peptide binding, biological antibody controls, quantitative PTM comparison, replication statements) whose outcomes could change a conclusion. This is therefore a major revision, not a minor one.

The genuinely novel contribution — the proteasome-trigger link and the antibody-based detection of endogenous K82 acetylation in sALS tissue — is real and worth publishing. The manuscript must be repositioned to lead with these, and the K82-acetylation-disrupts-import finding must be framed as confirmation of Ko et al. 2024 with a new upstream trigger, not as the primary discovery.

---

## Required Revisions

1. **Distinguish acetylation from ubiquitination at K82.** The mass spectrometry identified both modifications at K79/K82/K84, but the manuscript concludes acetylation is the driver without testing ubiquitination. Provide one of: (a) a ubiquitinated-K82 peptide in the importin-α1 binding assay (Fig. 3F), (b) a K82E (charge-neutral, non-acetyl-mimicking) comparison in the nuclear-import assays, or (c) quantitative MS showing acetylation occupancy is substantially higher than ubiquitination occupancy at K82 under proteasome inhibition. Without this, the claim that acetylation *specifically* initiates the effect is unsupported.

2. **Provide the mass spectrometry evidence for the PTM identifications.** Show the modified peptides, their sequences, modification-site localization probabilities (e.g., Ascore or equivalent), and representative annotated MS2 spectra for the K82-acetylated peptide. Report whether K79, K82, and K84 carry acetylation, ubiquitination, or both, and the relative abundance of each modification in BTZ-treated versus untreated cells. The claim that proteasome inhibition "induces" these modifications requires a quantitative comparison, not just identification.

3. **Establish biological specificity for the ac-K82 antibody.** Show that the antibody signal in the immunoblot format used for Fig. 5B disappears or is markedly reduced (a) in cells expressing K82R TDP-43, (b) after TDP-43 knockdown, and (c) after pre-incubation with the acetylated peptide (peptide competition). Without these controls, the sALS versus control difference could reflect total TDP-43 load or cross-reactivity.

4. **Requalify the causal and temporal language throughout.** The title, abstract, and discussion use "initiates" and "induces" in ways that outrun the evidence. Change to "can initiate" or "is sufficient to initiate" for the title claim. The statement that acetylation is "an earlier event than phosphorylation" (based on Fig. 5C) must be explicitly hedged as a single-case observation that is suggestive but not demonstrative of temporal order. The Discussion's "acetylation initiates and drives TDP-43 proteinopathy" should be requalified to distinguish sufficiency in cell models from initiation in human disease.

5. **State the biological replication for the TMT nuclear proteomics (Fig. 1E–F).** State whether the "three forward labelling groups and three reverse labelling groups" are biological replicates (independent differentiations) or technical replicates (aliquots of one differentiation). If the latter, the claim that TDP-43 is "the protein whose nuclear localization is most perturbed" must be downgraded to a single observation. Report the degrees of freedom for the t-test and the fold-changes with confidence intervals for the ALS-linked RNA-binding proteins in Fig. 1F.

6. **Add statistical analysis to the human tissue data (Fig. 5B).** Provide densitometric quantification of the ac-K82 and phospho-TDP-43 bands normalized to total TDP-43 or a loading control, with a stated test (e.g., Mann-Whitney U) and exact p-values. The current presentation as a binary "detectable/not detectable" observation without quantification is not sufficient for the claim.

7. **Add statistics to the peptide-binding assay (Fig. 3F).** State the number of independent experiments, whether curves are means ± SEM or representative, and provide a statistical comparison between modified and unmodified peptides (e.g., IC50 values with confidence intervals, or a two-way ANOVA).

8. **Add n's, tests, and error-bar definitions to the key cell-based quantifications.** Specifically: Fig. 1B (time course), Fig. 1G (stathmin-2 splicing — provide densitometry), Fig. 2E, Fig. 3C–D (K82Q versus WT with a stated test, e.g., one-way ANOVA with Dunnett's), and Fig. 4E. State whether n refers to biological or technical replicates.

9. **Address the dose discrepancy between experiments.** The PTM mass spectrometry (Fig. 3A–B) and the nuclear proteomics (Fig. 1E) used 20 nM BTZ, while the functional mislocalization assays (Fig. 1B–D) and the PTM-mimic experiments used 2 nM. State explicitly which dose was used for which experiment, and confirm that the PTM identifications were made at a dose that produces the ~50% inhibition used in the functional assays, or justify the higher dose.

10. **Provide the missing procedural identifiers for reproducibility.** At minimum: (a) antibody vendor/catalog/RRID/dilution for all antibodies (currently only in unreproduced supplementary tables — either reproduce the tables or deposit them); (b) gRNA sequences and validation for the TDP-43-Clover knock-in line; (c) siRNA target sequences or vendor; (d) qRT-PCR primer sequences; (e) mass spectrometry repository accessions (PRIDE or MassIVE) for both the TMT and PTM datasets; (f) versions for DTASelect2, Census2, RawConverter, and the UniProt database; (g) image-analysis software and version; (h) mouse strain, source, n per group, and IACUC protocol number.

---

## Minor Suggestions

1. **Reposition the novelty framing.** The abstract and introduction lead with the K82-acetylation-disrupts-import finding, which was already reported by Ko et al. 2024 (ref 30, cited). Lead instead with the genuinely novel contributions: the proteasome-trigger link and the antibody-based detection of endogenous K82 acetylation in sALS tissue with its soluble/insoluble distribution. State the delta over Ko et al. explicitly in the Discussion.

2. **Add a control for pathway-wide importin-α1 effects.** The FUS control (Fig. 2B–C) shows that importin-β2–mediated import is unaffected, but this does not rule out a general effect on importin-α1–mediated import. Testing a second cNLS-dependent importin-α1 cargo under identical conditions would strengthen the specificity claim.

3. **Add a K82R rescue experiment.** Expressing K82R TDP-43 (acetylation-dead) under proteasome inhibition and showing rescue of nuclear localization and stathmin-2 splicing would provide the epistasis evidence needed to support the causal claim. This is listed as a minor suggestion because the required revision items above already address the specificity question; this experiment would further strengthen the manuscript.

4. **Clarify the PTM enrichment workflow.** The Methods state that peptides were "enriched using titanium dioxide chromatography," which is a phosphopeptide enrichment method. Clarify whether acetylation/ubiquitination identifications came from the same enriched fraction or a separate analysis, and state the search parameters for variable modifications (acetyl, ubiquitin remnant, phospho).

5. **Report the efficiency of siRNA depletion.** State the residual endogenous TDP-43 level after the 48-hr siRNA pre-treatment, as this could confound the nuclear-localization measurements of the expressed variants.

6. **Clarify the Fig. 2G–I co-expression experiment.** State whether the mRuby-TDP-43 signal was verified to be free of spectral bleed-through from the Clover channel, and whether the co-IP in Fig. 2F directly tests heterodimer formation between the PY-NLS and cNLS constructs.

7. **Add a funding statement and competing-interests declaration.** These are absent and are required for this venue.

8. **Verify the cited statistics.** Please confirm that ref 1 (Neumann 2006) contains the "97% of ALS cases" figure, that ref 7 (Nelson 2019) contains the "20–50% of people older than 80 years" and "100-fold" figures, and that ref 34 (Kametani 2016) reports K82 acetylation in "one out of two" ALS samples. If these figures originate from other sources, cite those sources.

9. **Clarify the tissue-handling description.** The Methods describe the repository as using formalin-fixed tissue, but the study uses fresh frozen motor cortex. Clarify whether the fresh frozen samples were collected under the same IRB protocol or a separate one.

10. **Add a data-availability statement.** State where the raw mass spectrometry data, image quantifications, and any custom analysis scripts can be accessed.