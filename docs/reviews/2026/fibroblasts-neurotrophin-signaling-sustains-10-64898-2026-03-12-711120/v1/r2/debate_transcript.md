# Debate Transcript

## Skeptic — round 1

The strongest case against acceptance is not any single flaw the panel found, but a convergent gap in verification that all five reports independently reached from different angles: **none of the load-bearing claims can be checked because the manuscript withholds the basic parameters needed to evaluate its statistics.**

The data_analysis, reporting_reproducibility, and scientific_validity reviewers each flag, independently of each other's specific framing, that sample sizes (n) are never stated in figure legends or Methods for the in vitro (Fig. 4), co-culture (Fig. 3), or explant (Fig. 6) experiments — the same headline numbers used to justify the abstract's central claims ("36–40%" aSMA reduction, "50–54%" PECAM1 reduction) are p-values without denominators. This is FIXABLE — report n, pairing structure, and raw points — but as submitted, a reader cannot verify the therapeutic claim that anchors the paper's translational hook.

More serious, and potentially FATAL to the paper's framing rather than its data: the data_analysis reviewer identifies that Fig. 1's headline finding — "vascular maturation persists despite treatment" — is calculated as vascular-cell-count divided by total-synovial-cell-area, where the denominator itself shrinks with immunosuppression-driven immune cell depletion (stated explicitly in the Introduction: "immunosuppression depletes infiltrating immune cells in RA synovia"). A proportion can rise mechanically as the denominator shrinks, with zero real change in vascular biology. The manuscript never reports absolute vascular cell counts per unit area to rule this out. This is the load-bearing claim of the entire paper — that vasculature is "treatment-resistant" — and it rests on a metric that a mechanical artifact could fully explain.

Collectively, the panel also converges on a blind spot: no report tested whether the fibroblast-to-mural-cell claim (versus mural cell activation/recruitment/proliferation) was addressed by lineage tracing — three reviewers raise it as the same unresolved gap, not three confirmations.

## Advocate — round 1

# Case for Acceptance

This manuscript should be accepted for review publication because it presents a genuinely novel, multiply-validated mechanistic finding with direct therapeutic implications, using a research design that is appropriately scaled to a preprint venue explicitly built for transparent public evaluation.

**The central contribution is real and clearly demonstrated.** The paper identifies, for the first time in RA, that NOTCH3 signaling induces fibroblast NGF production, which sensitizes fibroblasts to differentiate into mural cells via NGFR-potentiated TRKA signaling (Fig. 5, Fig. 3). Every reviewer's own "Strengths" sections concede this: the contribution_context reviewer calls it "novel in the RA context and mechanistically interesting"; the scientific_validity reviewer notes the pathway is "traced through multiple orthogonal approaches... creating internal consistency." This convergence across five independent methodologies — spatial transcriptomics, RNAscope, immunohistochemistry, siRNA knockdown, lentiviral overexpression, and pharmacology — is not incremental noise; it is the standard by which mechanistic claims are usually judged credible.

**The clinical translation angle is concrete and testable, not speculative.** Larotrectinib and entrectinib are FDA-approved, and the manuscript reports specific, quantified reductions in aSMA and PECAM1 in RA explants (Fig. 6E-G). Even the most skeptical reviewers accept this as "a meaningful proof-of-concept" (scientific_validity) and "a concrete path toward clinical translation" (contribution_context). The paper's own framing is appropriately modest: it calls this "an opportunity to repurpose" drugs, not a demonstrated clinical treatment — matching the claim to the evidence.

**Reproducibility concerns are revision-level, not fatal.** Missing n's, deposition links, and Seurat parameters are legitimate, fixable requests — not indications that the underlying biology is wrong. Ethics review found the study fully compliant (score 5/5).

The persistent vascular maturation finding (Fig. 1G-H) — that immunosuppression fails to normalize synovial vasculature — is itself a clinically important, statistically supported observation (Wilcoxon signed-rank, paired design) independent of the mechanistic claims, and stands as a valuable contribution on its own.

## Advocate — round 2

The skeptic's strongest point this round is the denominator argument for Fig. 1G/H, so I'll address it directly rather than repeat prior ground.

**The denominator artifact does not survive scrutiny of the paper's own data.** If immune-cell depletion mechanically inflated vascular proportions by shrinking the total-cell denominator, that inflation would apply uniformly across *all* vascular subtypes sharing the same denominator. But the manuscript reports the opposite pattern: capillary ECs, arteriolar ECs, pericytes, and VSMCs all increase significantly post-treatment, while venular ECs and lymphatic ECs — subject to the identical denominator — show no significant change ("the increase in synovial vascular maturation is specific to the capillary and arterial endothelia as the densities of venular ECs and lymphatic ECs did not change significantly between pre- and post-treatment"). A pure denominator-shrinkage artifact cannot produce this selectivity; it would inflate every subtype's proportion equally. The differential, subtype-specific pattern is precisely what one would expect from genuine arterial-side vascular maturation, not a mechanical byproduct of immune depletion. This doesn't make the concern illegitimate as a request for absolute counts in revision — it does make it far weaker as grounds for rejecting the central finding.

On missing n's: this is a real and fair reporting gap, conceded. But it is a disclosure failure, not evidence the effects are spurious — the same qualitative direction (NGF→pericyte markers, BDNF/NT3→VSMC markers, TRK inhibition→reduced maturation) recurs across five independent methodologies that don't share the same denominator or n problem (RNAscope, IHC, knockdown, overexpression, pharmacology).

On lineage tracing: a genuine limitation on the *fibroblast-origin* claim specifically, but it does not undermine the better-supported claim that neurotrophin signaling regulates mural marker/function acquisition and is druggable — which stands on its own.

## Skeptic — round 2

I'll concede the strongest part of the advocate's case: the core NOTCH3→NGF→NGFR/TRKA potentiation mechanism (Fig. 3, Fig. 5) genuinely converges across independent methods — RNAscope, siRNA, CRISPR KO, overexpression, phospho-blot. That narrow mechanistic claim is well-supported and no report disputes it.

But the advocate conflates "the mechanism is real" with "the paper's stated claims are supported," and that's where the case for acceptance overreaches. Two problems the advocate doesn't address:

First, on the abstract's title claim ("fibroblasts... differentiation into mural cells"): every method deployed — co-culture, RNAscope, IHC, organoid aSMA staining — measures marker co-expression or induction, never lineage. The scientific_validity, reporting_reproducibility, and contribution_context reviewers independently flag this as the same unresolved gap, which the advocate's "convergence across five methodologies" argument doesn't touch, because convergence of correlative markers is not convergence toward causal cell-fate evidence. This is FIXABLE (lineage tracing, scRNA-seq trajectory) but as written the title's central verb — "differentiation" — outruns the data.

Second, on the therapeutic claim: the advocate calls TRK-inhibitor reversal "concrete," but no viability/apoptosis control distinguishes reversal from endothelial toxicity in the 3-day explants — a gap the scientific_validity reviewer states explicitly and the advocate doesn't rebut. Calling unverified drug effects a "concrete path to translation" is precisely the overclaim the target journal's rubric warns against.

Neither issue is fatal; both require the authors to either add data or soften language.