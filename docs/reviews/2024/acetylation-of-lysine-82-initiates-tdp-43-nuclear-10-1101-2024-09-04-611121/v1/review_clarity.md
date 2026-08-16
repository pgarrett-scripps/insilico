# Clarity & Presentation Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This is a clearly written, well-organized manuscript reporting that partial proteasome inhibition causes TDP-43 cytoplasmic mislocalization via post-translational modification of its cNLS, with acetylation at K82 identified as the critical modification. The narrative is logical, the figures are well-referenced, and the claims are stated explicitly. The main presentation concerns are: (1) the PTM mass spectrometry evidence is described but not shown, leaving the reader unable to verify the central identification; (2) several quantitative comparisons lack the actual quantities; and (3) some figure legends are incomplete. These are fixable with revision.

## Strengths

1. The central claim is stated explicitly and repeatedly — K82 acetylation disrupts importin-α1 binding and drives TDP-43 nuclear loss — and the evidence chain is easy to follow.
2. The rescue experiment (PY-NLS swap) is a clean, well-described control that isolates the cNLS as the relevant element.
3. The manuscript is honest about limitations, including the variability in acetylation levels across sALS samples.

## Weaknesses

**Load-bearing:**

1. **The PTM mass spectrometry data — the foundation of the paper — is not inspectable.** Figure 3A–B describes the workflow and lists the modifications found (acetylation/ubiquitination at K79, K82, K84; phosphorylation at S91/S92), but no spectra, no peptide-level identifications, no localization scores, and no confidence metrics are shown anywhere in the main text or supplementary material. The reader cannot determine whether the K82 acetylation assignment is unambiguous (e.g., whether the modification could be mislocalized to a neighboring lysine, or whether the ubiquitination and acetylation calls are distinguished with the appropriate mass offsets). The claim that "acetylation and/or ubiquitination of lysines 79, 82, and 84 were identified" is the load-bearing evidence for the entire mechanistic story, and it is presented as a summary with no underlying data. I could not verify this from the text. What would settle it: a supplementary table listing the modified peptides, their sequences, the modification site localization probability (e.g., Ascore or phosphoRS-equivalent), and representative annotated MS2 spectra for the K82-acetylated peptide.

2. **The quantitative claims in Figure 1E–F are not quantified in the text.** The volcano plot shows TDP-43 as the most depleted nuclear protein, and the text says "reduced by more than 4 fold" — good — but the comparison to other ALS-linked RNA-binding proteins (Fig. 1F) is described only as "not (or barely) affected." A reader cannot tell from the text whether FUS, TAF15, EWSR1, etc., were depleted by 1.1-fold or 1.8-fold, which matters for the specificity claim. Similarly, Figure 3D quantifies nuclear TDP-43 variant levels but the text gives no numbers for the K82Q effect ("eliminated its nuclear import" is qualitative). What would settle it: report the actual fold-changes and confidence intervals for the proteins in Fig. 1F, and the mean ± SEM nuclear/cytoplasmic ratios for the K82Q variant versus WT in Fig. 3D.

**Sweep:**

3. **Figure 5C is referenced but its experimental logic is under-explained.** The text says acetylation was found in "both soluble and insoluble fractions" of sALS cortex, implying acetylation precedes phosphorylation, but the fractionation protocol (NP-40 soluble/insoluble) is not described in Methods, and the reader cannot tell whether the soluble fraction includes nuclear TDP-43 or only cytoplasmic. The claim that acetylation is "an earlier event" outruns what this single time-point postmortem experiment can show.

4. **The peptide binding assay (Fig. 3F) is described in Methods but the figure legend does not define the axis units or the negative/blank controls.** The legend says "conducted across a range of concentrations" but does not state what the x-axis is (peptide concentration? importin concentration?), nor what "random peptides" means. A reader cannot interpret the figure from the caption alone.

5. **Terminology inconsistency: "cNLS" vs "NLS."** The manuscript uses "cNLS" (classical NLS) in most places but "NLS" in Figure 4A and in the text around it ("Replacing all 6 lysines in the TDP-43 cNLS" vs. "TDP-43-6KR"). This is minor but could confuse a reader tracking the distinction between the classical NLS and the PY-NLS.

6. **The abstract claims "reduced proteasome activity, as naturally occurs during aging" but the aging data (Fig. S1A) shows a decline in mouse cortex by 1 year, not in human aging.** The human data in Fig. S1A is from sALS patients, not aged controls. The framing slightly overstates the aging link; the claim should be scoped to "age-related decline in mice and reduced activity in sALS."

7. **Figure 2G–H quantifications are described in the text but the time points (0–6 hr) are not justified.** The text says "0-6 hr" but the earlier experiments used 12–48 hr. A reader cannot tell whether 6 hr was chosen because the effect saturates, or because the experiment was shorter. A one-sentence justification would resolve this.

8. **The Methods section for the PTM mass spectrometry is incomplete.** It says "TDP-43 was digested using trypsin and chymotrypsin independently, and then peptides were combined and enriched using titanium dioxide chromatography" — but the enrichment step is for phosphopeptides, not acetylated or ubiquitinated peptides. The reader cannot determine whether acetylation/ubiquitination identifications came from the same enriched fraction or a separate analysis, and no search parameters for variable modifications (acetyl, ubiquitin remnant, phospho) are given.

## Questions

1. Can the authors provide the MS2 spectra and localization scores for the K82-acetylated peptide, and clarify whether the titanium dioxide enrichment was applied to all PTM identifications or only phosphorylation?

2. What are the actual nuclear/cytoplasmic ratios (mean ± SEM, n) for the K82Q variant versus WT in Figure 3D, and the fold-changes for the other ALS-linked RBPs in Figure 1F?

3. In Figure 5C, what fractionation protocol was used, and does the "soluble" fraction include nuclear TDP-43? How does the presence of acetylation in the soluble fraction support the claim that acetylation precedes phosphorylation, given that both could occur in different subcellular pools?