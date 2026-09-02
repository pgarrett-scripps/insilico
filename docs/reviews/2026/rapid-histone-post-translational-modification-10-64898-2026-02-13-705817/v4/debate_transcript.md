# Debate Transcript

## Advocate — round 1

This manuscript deserves acceptance as a methodologically transparent, empirically grounded contribution that the panel itself scores at 4/5 across every dimension — contribution, statistics, reproducibility, and validity — with no dimension flagged as unsound. That consistency across independent specialist lenses, not just repetition, is itself informative: reviewers approaching from different angles converged on "solid, useful, with specific fixable gaps" rather than "fundamentally flawed."

**The core empirical findings survive scrutiny.** The panel does not dispute that Arg-C Ultra achieves ~84% zero-missed-cleavage peptides versus a heterogeneous Trypsin distribution (Figure 2C), that TMT labeling efficiency reaches ~92-99% versus 29-71% for propionylation (Figure 4A), or that 58 succinylation and 31 glutarylation sites were identified with TMT that are largely absent from propionylated data (Figure 5B). These are measured outcomes, not inferences. The contribution reviewer's own numbers show Arg-C Ultra+TMT yields 416 fully-cleaved peptides versus 179 for Trypsin+Prop — a real, reported result.

**The mechanistic explanation is appropriately hedged, not fabricated.** Reviewers want additional experiments (fixed-vs-stepped NCE controls, unlabeled-vs-labeled charge-state comparisons) to fully isolate charge compensation from competing explanations. This is legitimate revision guidance, not evidence the claim is wrong. The manuscript grounds its mechanism in established fragmentation theory (the mobile proton model, ref 26-27) and shows consistent, testable signatures (b-ion enhancement in Figure 6 spectra) — a defensible inference from data, clearly presented as such.

**The authors already demonstrate scientific honesty that should count in their favor**: they explicitly flag that ammonium buffers may bias the propionylation comparison, that formylation could be artifactual, that Trypsin+TMT comparison was deliberately not performed and why, and that succinylation/glutarylation sites await synthetic validation. The Discussion's "Limitations" section anticipates nearly every sweep-level criticism raised.

**Reproducibility is genuinely strong**: full data/code deposition (PXD073683, GitHub), detailed FragPipe parameters, and a working 3-hour protocol applied successfully to real tissue (231 PTM sites, Figure 8).

The identified gaps are revision items, not disqualifying flaws.

## Skeptic — round 1

**Load-bearing objection (FIXABLE, but currently unaddressed): the mechanistic claim underpinning the paper's central "dark epigenome" finding is confounded by the experimental design itself, not just by missing controls.**

The Methods state plainly: "For non-TMT peptides, a fixed collision energy of 30% was applied, while TMT-labeled peptides were fragmented using a stepped normalized collision energy (NCE) of 30%, 40%, and 50%." The paper then attributes enhanced b-ion coverage and rescued succinylation/glutarylation detection specifically to "TMT's tertiary amine provides charge compensation" (Abstract; Results, "Enhanced identification of histone succinylation and glutarylation with TMT"). But TMT and non-TMT samples were never fragmented under matched energy — so the enhanced b-ions and improved acidic-PTM detection could equally derive from more thorough fragmentation at 40–50% NCE, independent of any proton-sequestration mechanism. This is a genuine design confound baked into the primary comparison, not merely an inferential gap the reviewers speculated about — it is stated in the authors' own Methods. The abstract's flagship claim (58 succinylation, 31 glutarylation sites, "a dark epigenome") rests entirely on this unmatched-energy comparison, with zero orthogonal or synthetic-peptide validation offered anywhere in the manuscript (the Discussion itself concedes "future studies could prioritize synthetic validation").

Compounding this, the scientific_validity report caught a direct internal contradiction: the Abstract claims Arg-C Ultra+TMT "exceeds Trypsin-based approaches" in total PTM detection, while the Results state TMT-labeled samples achieved only "comparable PTM numbers to conventional 'Trypsin + Prop' methods (~120 PTMs)." The paper's strongest quantitative claim is not even internally consistent.

Given these unresolved confounds behind the headline discovery, and the absence of any independent validation, I cannot support acceptance without a revision that either matches collision energies across conditions or substantially tempers the causal/mechanistic language.

## Advocate — round 2

The skeptic identifies two real issues, and I'll concede both rather than dispute them — but neither is disqualifying.

**On collision energy:** yes, the Methods explicitly state fixed 30% NCE for non-TMT and stepped 30/40/50% for TMT samples, and this is a genuine confound for attributing the b-ion shift specifically to proton sequestration rather than to more thorough fragmentation. This is worth flagging prominently in the review. But it's also worth noting the choice wasn't arbitrary: stepped HCD for TMT-labeled peptides is standard practice specifically because TMT tags are known to require different fragmentation energy than unlabeled peptides (the authors cite their own prior work on this, ref 23, Diedrich et al.). That doesn't resolve the confound for isolating *mechanism*, but it means the design choice reflects established practice, not an oversight — and critically, **the empirical outcome (58 succinylation, 31 glutarylation sites recovered with TMT that are absent from propionylated data) stands regardless of which specific mechanism is correct.** The Discussion already treats the tertiary-amine explanation as inference ("This mechanistic explanation accounts for why...") rather than proven fact, which is honest framing given the data.

**On the Abstract/Results tension:** this is a real internal inconsistency worth fixing, but it reads as imprecise wording in the Abstract's synthesis of a multi-condition comparison — not a fabricated or unsupported number, since the Results text (~120 PTMs comparable) is itself clearly stated a few paragraphs earlier. An editorial revision — not rejection — resolves it.

Neither point undermines the reproducible, useful core contribution.

## Skeptic — round 2

**FATAL for the claim as currently framed; FIXABLE for the paper as a whole.** I stand by the confound I raised in round 1, and I note it is not my invention alone — the reporting_reproducibility reviewer independently flagged the identical point: TMT samples got stepped 30/40/50% NCE while propionylated/unlabeled samples got fixed 30% NCE, so "the advantage should shrink" test was never run. That two reviewers converged on this from different entry points is real corroboration, not model-multiplicity noise, because they identified different textual evidence (Methods vs. mechanism narrative) for the same structural problem.

The advocate's strongest move — panel consensus at 4/5 across dimensions — is real but doesn't answer the confound; a paper can be uniformly "solid with fixable gaps" while its single most novel, abstract-level claim (58 succinylation, 31 glutarylation sites, "dark epigenome") remains unvalidated. I concede the authors are unusually candid about limitations elsewhere, and I concede Arg-C Ultra's digestion-efficiency advantage (Figure 2C) is measured, not inferred. But candour about *other* limitations doesn't retroactively fix *this* one, and the scientific_validity reviewer's catch — Abstract says Arg-C Ultra+TMT "exceeds" Trypsin, Results say "comparable ~120 PTMs" — is a plain textual contradiction, not an interpretive dispute.

Blind spot: no reviewer pulled the manuscript's own unlabeled-vs-propionylated (both fixed-NCE) succinylation counts to partially isolate energy from labeling — that comparison is buildable from Figure 5A/5B data already in hand but nobody did it.