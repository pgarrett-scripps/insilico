# Novelty & Contribution Reviewer

SCORE: 3
CONFIDENCE: 4

## Novelty & Contribution Review

**Overall take.** The core methodological contribution — a dual-protease (Arg-C Ultra + r-Chymotrypsin) workflow that avoids chemical derivatization and is compatible with TMT labeling — is real, useful, and largely new in its specific combination, though its components are individually prefigured in recent work. The strongest and most defensible novelty claim is the TMT charge-compensation mechanism for detecting acidic acylations (succinylation/glutarylation), which is mechanistically argued and supported by data. The weakest is the implicit "first to" positioning of the overall workflow, which needs sharper differentiation from Ryzhaya et al. 2025. The contribution is incremental-but-useful and should be framed as such; it is not a breakthrough, and the manuscript's own framing occasionally drifts toward that.

**Strengths.**
1. The TMT tertiary-amine charge-compensation explanation for enhanced succinylation/glutarylation detection is a genuinely novel mechanistic insight, not just an observation.
2. The systematic 10-condition comparison with auditable metrics (labeling efficiency, IHP, missed cleavages) is a solid empirical foundation.
3. The dual-protease orthogonal coverage argument (r-Chymotrypsin for H2A variants/linker histones) is well demonstrated.

**Load-bearing weaknesses.**

**1. The workflow's novelty is partially preempted by Ryzhaya et al. 2025 (Anal. Chem. 97:12486–12492), which the manuscript cites but does not differentiate from sharply enough.** Ryzhaya et al. already demonstrated Arg-C Ultra with a single post-digestion derivatization step (TMA) reducing histone prep to ~3–4 h, with superior specificity over Trypsin. The manuscript's RIPUP differs by (a) omitting derivatization entirely and (b) adding r-Chymotrypsin as a second orthogonal protease. These are real deltas, but the manuscript does not state them as such — it presents RIPUP as a coherent new workflow without a head-to-head against the closest neighbor. The delta over Ryzhaya et al. should be stated explicitly and, where feasible, quantified. This is a SOFT-to-HARD boundary; I score it SOFT because the delta is real, but the positioning needs fixing.

**2. The "dark epigenome" claim (58 succinylation, 31 glutarylation sites) rests on a single cell line and a single labeling condition, and its significance is asserted rather than established.** The claim that these sites are "largely undetected by propionylation-based methods" is plausible and mechanistically supported, but the manuscript does not demonstrate that the same sites are *undetectable* in propionylated samples from the same digest — it shows they are detected in TMT samples. The stronger claim requires a matched comparison showing the same peptides fail to ionize when propionylated. Without that, the "dark epigenome" framing overstates what is shown. This is a SOFT issue (the mechanism is sound) but the significance claim outruns the evidence.

**Sweep.**
- The quantitative NAM experiment is presented as demonstrating RIPUP's quantitative capacity, but the claim that it "quantified 112 statistically significant peptidoforms" is a demonstration of the pipeline, not a biological finding — the framing should not imply the latter.
- The manuscript claims TMT "has not been systematically evaluated for histone PTM analysis," but TMT has been used for histone analysis in prior work (e.g., middle-down H3, chromatin cross-linking studies); the claim should be narrowed to "not systematically evaluated as a *derivatization alternative to propionylation in bottom-up histone workflows*."
- The missed-cleavage motif analysis (salt-bridge effects on Arg-C Ultra/r-Chymotrypsin) is presented as novel; a search did not surface direct prior work on this for these specific enzymes, so this passes, but the claim is modest and should be scaled to match.
- The "first report of how histone PTMs at adjacent residues affect Arg-C Ultra and r-Chymotrypsin cleavage efficiency" is a priority claim I could not preempt after searching — it passes, but the authors should confirm no concurrent preprint exists.
- The cost analysis (Table S5) is a useful addition but is not a novelty claim; it should not be used to inflate the contribution's significance.

**Questions.**
1. Can you provide a matched comparison showing the same succinylated/glutarylated peptides fail to be detected (or are detected at much lower intensity) when propionylated, from the same digest — to support the "dark epigenome" framing?
2. What exactly does RIPUP do that Ryzhaya et al.'s Arg-C Ultra + TMA workflow does not, stated as a head-to-head rather than as separate workflow descriptions?

**Auditability of searches.** I ran `find_related_work` and `search_preprints` queries for: "Arg-C Ultra histone PTM mass spectrometry," "histone succinylation glutarylation TMT labeling," "alternative proteases histone post-translational modification analysis," and "histone propionylation alternative derivatization." The searches surfaced Ryzhaya et al. 2025 as the closest prior work (already cited by the authors), Vai et al. 2025 (HiP-Frag, cited), and no preempting preprint for the TMT charge-compensation mechanism or the missed-cleavage motif analysis. No HARD preemption found.