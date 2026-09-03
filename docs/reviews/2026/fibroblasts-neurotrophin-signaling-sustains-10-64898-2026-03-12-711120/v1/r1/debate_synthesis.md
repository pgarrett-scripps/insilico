# Post-Debate Synthesis for the Editor

## Issue 1: Denominator problem in the "persistent vascular maturation" claim

**Issue and evidence cited:** The paper's central claim — that vascular maturation persists post-treatment "independent of clinical remission" — rests on Fig. 1G (vascular cell density) and Fig. 1H (cell proportion changes). The data_analysis reviewer identified that both metrics may be confounded: if immunosuppression depletes immune infiltrates without changing absolute mural cell numbers, any denominator including total cellularity would mechanically inflate vascular proportions, mimicking "persistence" that isn't real. This underpins the title's "sustains," the Discussion's "treatment-resistant disease compartment," and the entire rationale for the TRK-inhibitor experiments.

**Strongest case for each side:** The advocate argued Fig. 1G is normalized to tissue *area* (not total cell count, per the Methods text: "proportion of vascular cells as a function of total surface area"), which would not be mechanically sensitive to immune depletion, and that two independently-computed metrics (Fig. 1G, 1H) showing the same direction is corroborating. The skeptic countered that Fig. 1H is explicitly a proportion of total cells (per the manuscript's own figure legend, "absolute cell proportion changes" is still a proportion), and that the claim of cross-validation between the two figures requires other-lineage denominator data that no reviewer found reported in the manuscript — the advocate's inference was not shown to be textually supported.

**What was conceded:** The advocate conceded this is at minimum a request for additional clarity (absolute counts alongside existing metrics) that the authors have not provided. The skeptic conceded the point is "fixable" with a reanalysis, not necessarily fatal to the biology.

**Where it stands:** **Unresolved.** The debate did not establish whether Fig. 1G's area-based denominator is actually immune-depletion-independent, nor whether Fig. 1H's proportion-based metric corroborates or merely repeats the same artifact risk. No absolute mural-cell-density-per-tissue-area data, independent of total cellularity, was shown to exist in the manuscript. This is a central, load-bearing empirical claim and the debate leaves the resolution to the authors' provision of new/reanalyzed data — it was not resolved by argument.

## Issue 2: Fibroblast-specific causal attribution outruns whole-tissue perturbation data

**Issue and evidence cited:** The title and abstract attribute pathogenic neurotrophin production specifically to fibroblasts, but the scientific_validity and contribution_context reviewers independently noted that spatial co-localization and explant TRK-inhibitor/DAPT experiments perturb whole tissue (Fig. 6) and cannot isolate fibroblasts from endothelial or immune sources of neurotrophins.

**Strongest case for each side:** The advocate did not dispute the substance but reframed it as a scope-of-claim fix — soften "fibroblast neurotrophin signaling" to "stromal/fibroblast-associated," noting the isolated co-culture knockdown/rescue experiments remain valid mechanistic evidence regardless of which cell dominates in vivo. The skeptic maintained that the advocate never actually engaged with the mismatch between the causal, cell-type-specific title claim and the whole-tissue Fig. 6 data, which cannot support that specificity.

**What was conceded:** The advocate explicitly conceded this point ("conceded, partially"), agreeing the title outruns the explant evidence.

**Where it stands:** **Resolved as a scope/framing issue, not a fatal flaw.** Both sides agree this is fixable by narrowing the title/claims or by adding fibroblast-selective perturbation data; it does not undermine the mechanistic backbone (NOTCH3→NGF→NGFR/TRK→mural differentiation) established in isolated co-culture.

## Issue 3: Mechanistic gaps in the NOTCH3→NGFR→TRKA signaling chain

**Issue and evidence cited:** Three specialist reports (contribution_context, data_analysis, scientific_validity, reporting_reproducibility) converged on the same three sub-claims lacking direct mechanistic proof: (a) whether NOTCH3 directly transcriptionally induces NGFR versus acting through intermediates; (b) whether NGFR potentiates TRKA via a co-receptor/binding mechanism versus ligand-independent transactivation (the baseline pY-TRKA increase in NGFR-overexpressing cells without NGF stimulation was flagged as ambiguous); (c) whether neurotrophin signaling is the primary versus merely a contributing driver of vascular maturation, given other pathways (PDGF, Ang1/Tie2, TGFβ) were not tested in the same explants.

**Strongest case for each side:** The advocate treated these as answerable, named, feasible follow-up experiments (co-IP, ChIP/reporter assays, dose-response, parallel pathway inhibition) that don't require redoing the study's foundation, and noted the AC should register that this is one underlying critique restated by multiple reviewer instances of the same model family, not four independent confirmations. The skeptic explicitly agreed with this framing in round 2, conceding these are answerable follow-ups rather than fatal design flaws.

**Where it stands:** **Resolved as non-fatal, revision-scale.** Both sides agree; note for the editor that this cluster reflects duplicate observations across reports rather than independent corroboration, though the underlying concern is legitimate and well-specified.

## Issue 4: Multiple-comparisons correction in Fig. 1G

**Issue and evidence cited:** The skeptic raised (introducing new material in round 1, drawing on the data_analysis reviewer's sweep point) that Fig. 1G's ~24 group×celltype comparisons lack disclosed family-wise error correction, with marginal p-values (e.g., 0.029) treated as significant.

**Strongest case for each side:** The advocate responded that directional consistency across two metrics and multiple cell types is not the pattern expected from cherry-picked marginal p-values. The skeptic did not further rebut this in the final round.

**Where it stands:** **Unresolved but not pressed further.** Raised once, answered once with a plausibility argument rather than a statistical rebuttal, and dropped. Compounds the Issue 1 concern about the reliability of the persistence claim.

## Concerns raised in reports but not engaged in debate

- **NGF's functional dissociation from contractility** (NGF fails to induce collagen gel contraction while BDNF/NT3 succeed, despite NGF being the primary NOTCH3-induced ligand) — flagged by data_analysis and scientific_validity, never debated.
- **Reproducibility gaps**: undisclosed RNAscope segmentation parameters, undeposited bulk RNA-seq data underlying the NGFR gene signature (circularity concern raised by data_analysis and reporting_reproducibility), unreported explant replication structure (risk of pseudo-replication), unvalidated NOTCH3 CRISPR knockout efficiency.
- **Ex vivo-to-in vivo extrapolation**: TRK inhibitor concentrations (1–10 µM) exceeding typical clinical Cmax; no viability/apoptosis controls distinguishing "reversal" from cytotoxicity; short 3-day culture window.
- **Missing competing-interests statement** (ethics reviewer; procedural, not scientific).
- **Only 2 healthy donor controls** in the spatial cohort, limiting baseline robustness.

These were substantive, specifically-evidenced points in the individual reports that the debate transcript never took up; their absence from the debate should not be read as resolution.