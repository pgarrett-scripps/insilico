# Debate Transcript

## Advocate — round 1

## Case for Acceptance

The panel converges on a consistent picture: this is scientifically sound, mechanistically detailed work that all five reviewers scored at 4/5 or higher, with no reviewer identifying a claim that "does not survive the evidence." That baseline matters — this is solid middle-of-the-scale work by the panel's own calibration standard, not borderline.

The central strength, acknowledged across reports, is convergent multi-modal evidence for a specific, falsifiable mechanism. The Contribution reviewer calls the K82 mutagenesis panel "elegant" and notes it identifies "a level of mechanistic detail not previously reported for TDP-43" (K82 necessary; K82+K95/K97 sufficient). Critically, the sufficiency claim for acetylation itself — not just the K82Q mimic — is independently supported: Fig. 3F shows synthetic peptides *actually acetylated* at K82 fail to bind importin-α1, while K79/K84 acetylation only reduces binding. This directly addresses the "K82Q isn't real acetylation" concern that recurs across reports; the peptide data close that gap for the biochemical claim even if full-length-protein dynamics remain untested.

The TMT proteomics (Fig. 1E–F) demonstrating TDP-43 as the most nuclear-import-sensitive protein among 5,202 quantified, combined with the stathmin-2 functional readout (Fig. 1G) and the PY-NLS rescue (Fig. 2E–I) that mechanistically confirms cNLS-dependence, together build a genuinely convergent case rather than resting on one assay.

The human-tissue finding — ac-K82 in six of six sALS motor cortices, absent in four controls (Fig. 5B) — is disease-relevant evidence rare in mechanistic cell-biology papers, and the Ethics reviewer confirms IRB documentation is proper.

The remaining gaps (stoichiometry, temporal ordering vs. phosphorylation, deacetylase identity) are appropriately flagged by reviewers as directions for revision/future work, not as flaws that invalidate the claims as stated, which are already appropriately hedged ("plausible initiator").

## Skeptic — round 1

The strongest case against acceptance is not any single flaw the panel found, but a gap none of them fully names: **necessity was never tested, only sufficiency**, and the manuscript's title and abstract claim causal initiation despite this.

Every load-bearing experiment in this paper demonstrates that a modification-mimicking mutant (K82Q) or an isolated synthetic peptide is *sufficient* to block importin-α1 binding. None demonstrates that acetylation at K82 is what *actually happens* to endogenous TDP-43 during proteasome inhibition and drives the mislocalization observed in Fig. 1. The scientific_validity reviewer states this precisely: "the acetylation-inhibition experiment does not prove it is *necessary*... An alternative explanation is that proteasome inhibition causes mislocalization through a different mechanism... and the acetylation is a secondary consequence or bystander." The proposed control — an acetylation-resistant TDP-43 (K79R/K82R/K84R etc.) tested for rescue of nuclear import under proteasome inhibition — is absent from the manuscript. Without it, the causal chain from "proteasome decline → K82 acetylation → mislocalization" (the paper's central mechanistic claim, stated flatly in the Abstract: "acetylation at lysine 82 is sufficient to abolish TDP-43 binding to importin-α1... driving TDP-43 nuclear loss of function") is asserted, not shown. This is FIXABLE — it requires one clean rescue experiment, not new theory — but as submitted it is a real gap, not a stylistic quibble.

Compounding this, the "acetylation precedes phosphorylation" claim (Fig. 5C) is explicitly conflated evidence, as both reporting_reproducibility and contribution_context independently note: solubility fractionation is not a temporal assay. This claim should be softened or removed, not merely hedged.

I do not regard the ethics reviewer's animal-IACUC and funding-statement gaps as scientifically fatal, but they are real omissions requiring correction before publication.

Given convergent identification of the necessity gap as load-bearing, I'd score this a 3, not a 4: the central causal claim, not just a peripheral one, remains untested.

## Skeptic — round 2

The advocate's rebuttal doesn't actually engage my strongest point — it restates the K82Q/peptide sufficiency evidence I already conceded closes the "K82Q isn't real acetylation" gap for the biochemical claim. It does not address the necessity gap: nothing in the manuscript shows that blocking acetylation at K79/K82/K84 rescues nuclear import under proteasome inhibition. Every reviewer's proposed fix converges on this same missing control, independently phrased: scientific_validity calls for an "acetylation-resistant lysines" rescue variant; data_analysis asks whether K82Q-expressing neurons even show BTZ-comparable loss of stathmin-2 function; reporting_reproducibility asks whether *endogenous* ac-K82 TDP-43 shows reduced importin-α1 co-IP. None of these experiments exists in the paper. That's not five independent findings — it's one experiment missing, described five ways — but the convergence on *which* experiment is missing, from reviewers focused on different axes (stats, reproducibility, mechanism), is meaningful.

This matters because the title itself asserts causal initiation: "Acetylation of lysine 82 initiates TDP-43 nuclear loss of function by disrupting its nuclear import." That is a necessity claim dressed as established fact, not a sufficiency claim. The Abstract's hedge ("plausible initiator") is inconsistent with the title's unhedged verb "initiates." A reader who only reads the title and Fig. 3 will conclude causality has been shown; it has not.

I am not calling this fatal — it is squarely FIXABLE, requiring one rescue experiment (acetylation-resistant TDP-43 in BTZ-treated neurons) or, short of new data, a revision of the title/abstract to match what was actually shown (sufficiency of a mimic, correlation in patients). But I disagree with the advocate that this is merely a "direction for future work." A causal verb in the title resting on sufficiency-only evidence is a claim/evidence mismatch, which is the paper's most important axis per the venue's own priorities. That keeps this at 3, not 4.

## Advocate — round 2

## Response to the necessity argument

The skeptic's point is real but I think it proves less than claimed, for a reason grounded in the manuscript's own data that the skeptic's proposed fix overlooks.

The proposed control — an acetylation/phospho-resistant K79R/K82R/K84R/S91A/S92A mutant tested for rescue under proteasome inhibition — is not actually interpretable given what Fig. 4 already shows. The paper demonstrates that **K82R alone**, a conservative substitution that removes the acetylatable lysine while preserving positive charge, "induced TDP-43 mislocalization" and abrogated the "TDP-43/importin-α1 interaction" (Fig. 4C–E). That means converting K82 to a non-modifiable residue is *not neutral* with respect to import — it independently breaks the importin-α1 contact regardless of acetylation status. Any acetylation-resistant construct built on K82R would therefore be cytoplasmic for reasons unrelated to blocking the modification, making the "clean" necessity experiment the skeptic wants uninterpretable by the logic of the authors' own mutagenesis. This is a genuine structural constraint, not an excuse.

Given that constraint, the authors' actual strategy — testing real acetylation on isolated peptides (Fig. 3F), where K82-acetylated peptide specifically abolishes importin-α1 binding while K79/K84-acetylated and phosphorylated peptides only reduce it — is the most direct causal test available short of that confounded experiment, and it does test genuine acetylation, not a mimic.

I'll concede the title's "initiates" oversells relative to the abstract's own carefully hedged language ("sufficient," "plausible initiator") — worth softening in revision, but not a reason to reject sound sufficiency evidence plus disease-correlative data (6/6 sALS).