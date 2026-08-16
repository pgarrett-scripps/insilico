# Debate Transcript

## Advocate — round 1

# Advocate's Opening Statement

This manuscript deserves acceptance. The core claim — that Git1 regulates Smo signaling by controlling Grk2 translocation into the cilium — is novel, mechanistically coherent, and supported by convergent evidence across multiple orthogonal assays.

**The central finding is genuinely new.** As the novelty reviewer confirms: "The central novelty claim — that Git1 is a previously unknown regulator of Smo signaling, acting by controlling Grk2's translocation into the primary cilium — survives my searches." No prior work links Git1 to Hedgehog signaling. The Smo-TurboID time-resolved interactome is likewise a new resource.

**The causal chain is tested at both ends.** The rigor reviewer correctly notes the rescue experiment (Fig. 6G–H) is "a strong causal test that directly supports the proposed mechanism." The methodology reviewer agrees: "The ciliary-targeted Grk2 rescue experiment is a well-designed test." While the middle links (Grk2 entry → Smo phosphorylation → PKA inhibition) are inferred from correlation, the authors themselves acknowledge this gap and the inference is reasonable given the convergent data: Git1 loss reduces ciliary Grk2 (Fig. 5E), reduces pSmo (Fig. 4E), and reduces PKA-C recruitment (Fig. 4I).

**The "primary site" claim is defensible with re-hedging.** The rigor reviewer's HARD objection — that basal-body phosphorylation followed by Smo transport is not excluded — is fair, but the fix is linguistic, not experimental. The data show ciliary Grk2 is *sufficient* for signaling; the claim should be softened to "Grk2 entry into the cilium is required for Smo phosphorylation." This does not undermine the paper's contribution.

**The reproducibility gaps are fixable in revision.** The proteomics pipeline needs deposited code and raw data — a legitimate HARD issue — but the authors already provide Table S1–S5 and describe the pipeline in prose. Depositing the R script and PRIDE accession is a mechanical fix, not a scientific one.

**The statistical concerns are addressable.** Pseudo-replication in microscopy quantifications (n=90 cells from 3 replicates) is a real issue, but the fix — reporting per-replicate means — is standard practice and does not require new experiments.

This is sound, novel, and buildable work. Accept with revision.

## Skeptic — round 1

The advocate's case rests on the claim that the manuscript's flaws are "fixable in revision" and that the core biology is sound. I disagree on the most load-bearing point: the central mechanistic claim is not merely under-hedged — it is materially untested at its midpoint.

**The causal chain is tested at its two ends, but the middle is inferred, not demonstrated.** The advocate concedes this, calling it "a reasonable inference." It is not. The manuscript claims Git1 controls Grk2 *translocation into the cilium* (Abstract, Fig. 5E). But the Grk2 localization data come from lentivirally overexpressed Grk2-V5, and the WT ciliary increase is only 1.2-fold — near the detection floor. As the methodology reviewer notes: "the absence of signal in Git1-null cilia could reflect a sensitivity floor rather than a true absence of translocation." The authors never show that Grk2-V5 is functional (can rescue Smo phosphorylation in a Grk2-null background), nor do they report its expression level relative to endogenous Grk2. Without that positive control, "no translocation" versus "below detection" is unresolved. This is a FATAL gap in the central claim as stated — not a wording fix.

**The "primary site" claim is not a linguistic issue.** The rigor reviewer's objection is substantive: the data show ciliary Grk2 is *sufficient* for signaling, not that it is the *physiological* site. The Git1-null phenotype is equally consistent with Git1 acting at the basal body to enable phosphorylation *en route* to the cilium. The advocate's proposed re-hedging ("Grk2 entry is required") is an admission that the paper's headline claim outruns its evidence.

**The proteomics resource is not yet a resource.** The reproducibility reviewer identifies a HARD failure: no raw data deposit, no accession, no executable analysis code. The advocate calls this "mechanical." It is not — the TMT normalization pipeline is described in prose that a competent reader cannot reproduce (the clarity reviewer could not determine whether TMM was per-channel or per-replicate). A resource that cannot be inspected is not a resource.

**The panel's collective blind spot:** every reviewer focused on the Git1 biology, but none independently verified that the pSmo antibody signal is phosphorylation-specific in Git1-null cells. The methodology reviewer flagged this; no one resolved it. If the pSmo signal reflects Smo conformation rather than phosphorylation, the entire downstream chain collapses.

The manuscript is promising, but the central claim — Git1 controls Grk2 *entry into the cilium* — is not established by the evidence presented. That is FATAL as written, though fixable with the Grk2-V5 functional control and per-replicate statistics.