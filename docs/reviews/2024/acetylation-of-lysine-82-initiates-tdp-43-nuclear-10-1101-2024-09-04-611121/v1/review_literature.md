# Related-Work & Citations Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript identifies acetylation of lysine 82 within the TDP-43 bipartite cNLS as a driver of TDP-43 nuclear loss of function and cytoplasmic accumulation, linking reduced proteasome activity (as occurs in aging) to TDP-43 mislocalization. The authors use quantitative proteomics, mutagenesis, peptide-binding assays, and newly generated acetylation-specific antibodies to show that K82 acetylation disrupts TDP-43 binding to importin-α1, and they detect K82 acetylation in sALS motor cortex but not controls. The citation record is largely sound, with a few gaps worth addressing.

## Strengths

1. The authors verify their central mechanistic claims with multiple independent approaches (mass spectrometry, mutagenesis, peptide-binding assays, acetylation-specific antibodies).
2. The use of a PY-NLS swap as a rescue experiment cleanly isolates the cNLS as the site of the proteasome-inhibition effect.
3. The human postmortem validation with newly generated acetylation-specific antibodies is a strong translational anchor.

## Weaknesses

**Load-bearing claim 1: "Partial reduction in proteasome activity inhibits TDP-43 nuclear localization through ubiquitination and acetylation within its cNLS."** The mass spectrometry identified acetylation and/or ubiquitination at K79, K82, K84, but the manuscript does not report which modification (acetylation vs. ubiquitination) was present at each site, nor the stoichiometry or relative abundance of each modification. The authors conclude that acetylation is the driver, but the MS data as presented cannot distinguish whether ubiquitination at K82 (which would also neutralize the lysine charge and could disrupt importin binding) is the primary event. The peptide-binding assay (Fig. 3F) tests only acetylated and phosphorylated peptides, not ubiquitinated ones. What would settle this: report the site-level localization of each modification type (acetylation vs. ubiquitination) from the MS data, and ideally test a ubiquitinated K82 peptide in the binding assay.

**Load-bearing claim 2: "Acetylation at K82 is sufficient to abolish TDP-43 binding to importin-α1 and subsequent nuclear import."** The evidence rests on the K82Q acetylation-mimic (Fig. 3C-E) and the peptide-binding assay (Fig. 3F). The K82Q mutation is a charge-neutralizing substitution, and the authors themselves show (Fig. 4) that even the conservative K82R mutation (which preserves positive charge) disrupts importin-α1 binding and nuclear localization. This raises the question of whether the effect is specific to acetylation per se or is a general consequence of any perturbation at K82 — including the K82R mutation that does not mimic acetylation. The claim that acetylation "is sufficient" is supported, but the claim that acetylation is mechanistically distinct from other K82 perturbations is not established. What would settle this: acknowledge that K82 is a gatekeeper residue whose modification (of any type) disrupts importin binding, and frame acetylation as the physiologically relevant modification rather than a uniquely disruptive one.

**Load-bearing claim 3: "Acetylation of lysine 82 is detected in the motor cortex of sporadic ALS patients but not control subjects."** The antibody validation (Fig. 5A) shows specificity against the acetylated vs. unacetylated peptide by ELISA, and the BTZ-treated neuron control (Fig. S5) supports specificity. However, the manuscript does not report whether the ac-K82 signal in sALS samples was competed by the acetylated peptide (a standard specificity control for a new antibody on tissue lysates), nor whether the signal colocalizes with TDP-43 aggregates by immunohistochemistry. The correlation between ac-K82 and p-TDP-43 (S409/410) is suggestive but based on n=6 sALS and n=4 controls. What would settle this: peptide competition on the sALS lysates, and ideally IHC showing ac-K82 in TDP-43 inclusions.

**Sweep items:**

1. The claim that "proteasome activity declines during aging of metazoans" cites refs 20-22, but the mouse data in Fig. S1A showing ~50% decline by one year is the authors' own data — the citation support for the general claim is fine, but the specific aging-neuron link is only partially supported by the cited literature (ref 20 is spinal cord, ref 21 is Drosophila, ref 22 is mouse brain).

2. The manuscript cites ref 30 (Ko et al., 2024) for the K82Q effect on importin-α1/β signaling, which is appropriate and current; good that this directly competing recent work is acknowledged.

3. Ref 34 (Kametani et al., 2016) is cited for prior MS detection of K82 acetylation in ALS — this is correctly attributed and appropriately acknowledged as prior evidence.

4. The claim that "TDP-43 is the protein whose nuclear localization is most perturbed upon reduction in proteasome activity" (Fig. 1E) is a strong claim resting on a single TMT experiment; the manuscript does not report whether the nuclear proteome changes were validated for a subset of proteins by orthogonal methods (e.g., immunoblot of fractionated lysates for a few of the most- and least-affected proteins).

5. The manuscript does not cite work on TDP-43 acetylation at other lysines (e.g., K136, K145, K192) in the introduction or discussion of the acetylation cascade — refs 9 and 35 are cited in the discussion, which is adequate, but the introduction could better situate the acetylation field.

6. The reference list appears to have a formatting issue: ref 24 (Melamed et al.) and ref 25 (Klim et al.) are both cited for stathmin-2 loss, which is correct, but the reference list shows "Nat. Neurosci. 22, 180-190 (2019). 39." — the "39" appears to be a stray artifact of the PDF conversion, not a real citation issue.

7. The manuscript's claim that "nuclear export of TDP-43 is thought to be achieved by passive diffusion" cites refs 16-18, which is accurate — these papers (Ederle 2018, Archbold 2018, Pinarbasi 2018) do support this claim.

8. The authors should verify that ref 19 (Doll et al., 2022) actually demonstrates importin-α1/β recognition of the TDP-43 cNLS as claimed — this is a recent and directly relevant citation, and the attribution appears correct from the title.

## Questions

1. In the MS analysis (Fig. 3B), can you report whether K79, K82, and K84 carry acetylation, ubiquitination, or both, and the relative abundance of each modification at each site?

2. Did you test a ubiquitinated K82 peptide in the importin-α1 binding assay (Fig. 3F), and if so, what was the result?

3. For the sALS tissue immunoblots (Fig. 5B), was the ac-K82 signal competed by pre-incubation with the acetylated peptide, and was ac-K82 localization examined by immunohistochemistry in TDP-43 inclusions?

4. Given that K82R (charge-preserving) also disrupts importin binding, do you interpret acetylation as mechanistically distinct from other K82 perturbations, or is K82 a gatekeeper whose modification of any type disrupts import?

5. Was the nuclear proteome change (Fig. 1E) validated for a subset of proteins by orthogonal methods (e.g., immunoblot of fractionated lysates)?