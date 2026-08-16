# Related-Work & Citations Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a proximity-labeling (TurboID) proteomics study of Smoothened (Smo) in NIH3T3 cells, identifying Git1 as a new regulator that promotes Grk2 translocation into the primary cilium, enabling Smo phosphorylation and subsequent PKA inhibition. The proteomic dataset is time-resolved (15 min, 1 h, 4 h post-Shh) and validated against known Smo interactors. The authors characterize Git1 loss-of-function in NIH3T3 cells and primary cerebellar granule neuron precursors, showing reduced Hh signaling. The citation record is generally accurate and current, with a few soft gaps and one attribution worth verifying.

## Load-Bearing Claims

**Claim 1: Git1 is a new Smo interactor/regulator.** The evidence is the TurboID proteomic hit (Fig. 4A) plus YFP-Git1 biotinylation by Smo-TurboID (Fig. 4B). The biotinylation signal for Git1 is modest and the authors themselves note the interaction is not detectable by co-IP. The alternative explanation — that Git1 is biotinylated because it sits at the basal body near the ciliary base where Smo transits, rather than forming a specific Smo–Git1 complex — is not excluded. The functional data (Git1 loss reduces Grk2 ciliary entry and Smo phosphorylation) are the stronger evidence for a regulatory role, but they do not establish a direct Smo–Git1 interaction. The claim "Git1 is a new Smo regulator" is supported; the claim "Git1 interacts with Smo" (implied by "Smo-associated proteins") is only weakly supported by the proximity data alone. Distinguishing experiment: a Git1 mutant lacking the ArfGAP domain or a Git1 construct targeted away from the basal body, tested for rescue of Grk2 translocation, would separate scaffolding at the basal body from a specific Smo interaction.

**Claim 2: Git1 controls Grk2 translocation into the cilium, and this is the mechanism by which Git1 regulates Smo phosphorylation.** The evidence is that Grk2-V5 levels in the cilium increase in WT but not Git1-null cells after Shh (Fig. 5C–E), and that ciliary-targeted Grk2 rescues Hh signaling in Git1-null cells (Fig. 6G–H). The rescue experiment is the load-bearing piece and it is convincing in design. One caveat: the rescue is measured by Gli1 transcript, not by Smo phosphorylation or PKA-C recruitment, so the causal chain (Git1 → Grk2 ciliary entry → Smo phosphorylation → PKA inhibition → Gli1) is only tested at its two ends. The middle links are inferred from the correlation between reduced ciliary Grk2 and reduced pSmo in Git1-null cells. This is a reasonable inference but not a closed loop. A direct test — measuring pSmo or PKA-C in the cilium of Git1-null cells expressing ciliary Grk2 — would close it.

**Claim 3: Git1 loss does not affect Smo ciliary accumulation.** The evidence is that Shh-induced Smo levels in the cilium are comparable between WT and Git1-null cells (Fig. 4F–G). This is important because it isolates the defect to phosphorylation rather than trafficking. The quantification is straightforward and the claim is well-supported by the data shown. No alternative explanation is apparent.

## Sweep

- **Attribution check (HARD-adjacent):** The claim that Git1 loss causes "microcephaly-like phenotypes" (refs 28–30) is supported by the cited Badea et al. 2021 paper, but the claim that Git1-null mice show "cerebellar agenesis" is stronger than what the cited sources appear to establish — Badea et al. report microcephaly with altered cortical layering; I could not verify cerebellar agenesis from the abstract. Ask the authors to confirm which source supports the cerebellar agenesis claim.
- **Missing foundational work (SOFT):** The paper cites Grk2's role in Smo signaling (ref 18, Walker et al. 2024) but does not cite the earlier work establishing Grk2's requirement in Hh signaling downstream of Smo (Zhao et al., EMBO Rep 2016, ref 39 in the reference list — this is actually cited, so this is not a gap; retract).
- **Missing directly-competing work (SOFT):** The time-resolved ciliary proteomics of May et al. (J Cell Biol 2021, ref 47) is cited, but the authors do not explicitly compare their Smo-TurboID dataset to the ciliary proteome from that study. A brief comparison of overlap would strengthen the claim that the Smo-proximal dataset captures distinct, Smo-specific interactions beyond general ciliary proteins.
- **Currency (SOFT):** The reference list is current (2024 papers cited), no issue.
- **Self-citation (SOFT):** Proportionate; the authors cite their own prior work (refs 16, 17, 19, 23) where it is directly relevant, not padded.
- **Citation hygiene (SOFT):** Ref 18 is cited as "Steiner, W. P. et al. A Structural Mechanism for Noncanonical GPCR Signal Transduction in the Hedgehog Pathway. bioRxiv (2024)" — this is a preprint used to support a claim about Grk2 phosphorylation of Smo. Since the published Walker et al. 2024 paper (ref 19) covers the same ground, the preprint citation is redundant; flag whether the preprint should be replaced by the published version or disambiguated.
- **Citation hygiene (SOFT):** Ref 23 (Liu et al., Nat Commun 2024) is cited for the DArl13b ciliary-targeting construct; this is the authors' own prior work and is appropriately cited.

## Questions

1. Which specific source supports the "cerebellar agenesis" phenotype in Git1-null mice? The cited Badea et al. 2021 abstract describes microcephaly and altered cortical layering; I could not verify cerebellar agenesis from that source.
2. In the rescue experiment (Fig. 6G–H), was Smo phosphorylation or PKA-C recruitment in the cilium measured in Git1-null cells expressing ciliary Grk2, or only Gli1 transcript? If only Gli1, this leaves the middle of the causal chain untested.
3. Is the Git1 biotinylation signal in Fig. 4B quantifiable above background in the no-Shh condition, and does the modest increase after Shh reach significance across replicates? The claim that Git1 is "in proximity to Smo" rests on this signal.