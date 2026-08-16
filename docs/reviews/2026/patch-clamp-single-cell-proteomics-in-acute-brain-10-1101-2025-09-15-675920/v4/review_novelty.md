# Novelty & Contribution Reviewer

I have enough to write the review. Let me compose it.

SCORE: 3
CONFIDENCE: 4

---

# Novelty & Contribution Review

## Verdict

The core technical novelty — maintaining the gigaseal through soma retrieval and using capacitance measured during that retrieval to predict proteome yield — survives a related-work and preprint search and is genuinely new. The "framework" framing, however, is positioned against a debate the manuscript does not engage: a concurrent preprint from the Nemes lab (the group behind the Choi 2022 paper this manuscript cites) directly addresses the same whole-soma-retrieval-vs-aspiration question, and the manuscript neither cites nor acknowledges it. The contribution is real but its significance is overstated relative to the evidence offered (n=3 for the load-bearing correlation), and its positioning needs sharpening against this nearest neighbor.

## Load-bearing claims

**1. The gigaseal-preservation → capacitance → proteome-yield link is the paper's one genuinely new, testable claim — and it is under-supported as a contribution.** I searched related work and preprints for "patch-clamp proteomics gigaseal capacitance protein identifications" and found no prior report of this specific correlation; the claim survives preemption. But the entire quantitative edifice rests on n=3 neurons (Figure 3D, "F = 1577, p < 0.05, adjusted R² = 0.998"). With three points, a near-perfect R² is expected regardless of the true relationship, and the correlation could be driven entirely by the one large neuron (#7) versus the two smaller ones. The alternative account — that the correlation reflects not soma size per se but retrieval difficulty (the two smaller neurons were also the ones with compromised active properties) — is not excluded. What would distinguish the authors' account from "retrieval difficulty, not size, drives yield" is a larger sample or a within-neuron control (e.g., capacitance measured before and after retrieval on the same neuron, correlated with yield). As it stands, the claim "soma size plays a more direct role in protein recovery than RM" outruns the evidence. This is partly rigor's call, but the novelty claim (a quantitative bridge between electrophysiology and proteomics) is only as strong as that correlation, so it belongs here.

**2. The "framework" is positioned against a debate the manuscript does not engage.** The manuscript's central framing — that retrieval quality, not in situ electrophysiology, governs what the recovered proteome reflects — is exactly the question addressed by a concurrent preprint I found: Johnson, Choi, Zegers-Delgado, Kisner, Araneda, Polter, Nemes, "Proteome-Driven Phenotyping of Identified Single Neurons in Intact Brain Tissue by Aspiration Patch Proteomics" (2026, PPR, doi:10.64898/2026.04.22.720006). Its abstract explicitly notes that "recent patch-based studies have emphasized whole-soma retrieval" and argues for aspiration-based cytoplasmic sampling instead — the mirror-image position to this manuscript's whole-soma approach. The manuscript cites Choi 2022 (same lab) but does not acknowledge that the whole-soma-vs-aspiration tradeoff is an active, contested question with a directly competing answer. The delta over this neighbor is real (gigaseal preservation during retrieval; the capacitance correlation; the indiscriminate-collection strategy) but the manuscript should name the neighbor and state what it does that the neighbor does not. This is a HARD differentiation failure as written — the nearest competing work is not named.

**3. The "indiscriminate shotgun" collection strategy is a defensible but modest methodological contribution.** The contrast with the "all-or-nothing" inclusion criteria of Lee 2024 and Ghatak 2024 (both cited) is real and honestly drawn. But analyzing torn neurons as internal negative controls is standard QC practice dressed as a strategy; the genuinely useful part is the demonstration that protein counts alone do not distinguish compromised from intact retrievals (Figure 6A). That is a useful caution, but it is a methodological observation, not a breakthrough, and the manuscript mostly frames it at the right altitude. No HARD issue here.

## Sweep

- The claim "retrieval mechanics, rather than in situ electrophysiology alone, limit whether proteins associated with excitability and synaptic function are recovered" is a causal framing of what is, at n=6 (Figure 5C-D), a null correlation — the absence of an in situ correlation does not establish that retrieval mechanics is the cause; the causal claim outruns the evidence (rigor's call, but the novelty framing depends on it).
- The manuscript's own statement that "recent patch-based studies have emphasized whole-soma retrieval" (paraphrased in the Johnson abstract) shows the authors are aware of the aspiration alternative but never engage it in the body — a positioning gap, not just a citation gap.
- The "framework" (Figure 1) is a useful conceptual contribution and is honestly labeled as a framework rather than a discovery — good altitude control on that specific claim.
- The claim that gigaseal preservation "could provide future studies with an approach to either validate proteomic recovery or enhance interpretability" is appropriately hedged as a possibility, which is the right framing for n=3.
- The ion-channel/GPCR/transporter recovery lists (Figures 7, S4, S5) are presented as capability demonstrations, not as novelty claims — correctly scoped.
- The manuscript does not overclaim "first" anywhere in the abstract or text — it uses "framework," "strategy," and "proof-of-concept," which is honest; the overstatement is in the significance framing, not in priority language.

## Questions

1. Can you name and directly differentiate against the Johnson et al. 2026 aspiration-patch-proteomics preprint, which addresses the same whole-soma-retrieval question from the opposite position? What does your gigaseal-preservation approach provide that aspiration sampling does not, and vice versa?
2. For the capacitance→yield correlation (Figure 3D), can you report the same analysis with retrieval difficulty (e.g., spike-amplitude loss during retrieval) as a covariate, or with a larger n, to distinguish soma size from retrieval integrity as the driver?

## Strengths

- The capacitance→protein-yield correlation is a genuinely new, testable observation that no prior work (published or preprint) reports.
- The indiscriminate-collection strategy and the demonstration that protein counts do not distinguish compromised from intact retrievals is a useful, honest methodological caution.
- The framework is honestly labeled as a framework and the limitations (n=3, compartmental bias, distal-protein under-recovery) are stated candidly rather than buried.