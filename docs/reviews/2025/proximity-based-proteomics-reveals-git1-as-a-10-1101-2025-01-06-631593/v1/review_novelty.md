# Novelty & Contribution Reviewer

The second search returned the key prior work. The 2011 paper (Chen et al., "Sonic Hedgehog Dependent Phosphorylation by CK1α and GRK2 Is Required for Ciliary Accumulation and Activation of Smoothened") is directly relevant — it established that GRK2 phosphorylates Smo. The 2024 paper is the authors' own Walker et al. work. The 2025/2026 papers on Smo-PKA at cilia are also relevant context. None of these preempt the specific Git1 finding.

Let me note the key point: the 2011 Chen et al. paper already established GRK2 phosphorylation of Smo and its role in ciliary accumulation/activation. The authors' own Walker 2024 paper established Grk2 in the cilium initiates Smo-PKA signaling. The novel contribution here is Git1 as the regulator of Grk2's ciliary translocation. That specific claim appears novel.

I have enough to write the review. Let me be honest about the search limitations (the arXiv fallback returned noise, bioRxiv returned nothing for the specific queries, but the Semantic Scholar search did surface the relevant prior literature).

Now writing the review.

SCORE: 4
CONFIDENCE: 3

My verdict: the Git1 finding is genuinely novel — no prior work links Git1 to Hedgehog signaling. The Smo-TurboID interactome resource appears novel. The main novelty concerns are positioning: (1) the "ciliary Grk2 is the primary site" claim is a refinement of the authors' own prior Walker 2024 work rather than a new discovery, and (2) the resource's incremental value over existing ciliary proteomics (Mick 2015, May 2021) needs sharper framing. These are SOFT issues, not HARD — the core Git1 claim survives the search.

Let me write the full review.

SCORE: 4
CONFIDENCE: 3

# Novelty & Contribution Review

## Verdict

The central novelty claim — that Git1 is a previously unknown regulator of Smo signaling, acting by controlling Grk2's translocation into the primary cilium — survives my searches. I found no published or preprint work linking Git1 to Hedgehog signaling, ciliary Grk2 transport, or Smo phosphorylation. The Smo-TurboID time-resolved interactome likewise appears to be a new resource. The contribution is real and the core claim is not preempted. My concerns are about positioning and the altitude of two secondary claims, not about whether the work is new.

## Load-bearing claims

**1. Git1 is a new regulator of Smo signaling via Grk2 ciliary transport.** This is the claim the paper rests on, and it holds up. The nearest prior work is Chen et al. 2011 (Sonic Hedgehog Dependent Phosphorylation by CK1α and GRK2 Is Required for Ciliary Accumulation and Activation of Smoothened), which established that GRK2 phosphorylates Smo, and the authors' own Walker et al. 2024 (GRK2 kinases in the primary cilium initiate SMOOTHENED-PKA signaling), which established Grk2's ciliary role and the Smo-PKA interaction. Neither identifies a mechanism for Grk2's ciliary entry, which is exactly the gap Git1 fills. The searches returned no Git1-Hedgehog connection in any prior work. The claim is novel. One caveat on the authors' own framing: the manuscript says Git1-null mice show "microcephaly-like phenotypes... consistent with impaired Hh signaling transduction" — this is presented as supporting evidence, but it is an inference from phenotype, not a prior demonstration of a Git1-Hh link, and should not be read as independent corroboration.

**2. The ciliary shaft, not the basal body, is the primary site of Grk2-mediated Smo phosphorylation.** This is framed as a conclusion of the paper ("pinpoint the cilium as the primary site"), but it is a refinement of the authors' own Walker et al. 2024 finding rather than a new discovery. The evidence here — Git1 loss abolishes ciliary Grk2 while leaving basal-body Grk2 intact, and ciliary-targeted Grk2 rescues signaling — is a legitimate and useful sharpening of the prior claim, but the novelty is incremental. The paper should state explicitly that this is an extension of their own prior work, not a first demonstration that Grk2 acts in the cilium. As written, the abstract's "pinpoint the cilium as the primary site" risks overstating the delta over Walker 2024.

**3. The Smo-TurboID time-resolved proteomic dataset is a novel resource.** This is a real contribution — I found no prior Smo-specific TurboID interactome. But the resource's incremental value over existing ciliary proximity-labeling proteomics (Mick et al. 2015; May et al. 2021, both cited by the authors) is not sharply stated. The paper claims the dataset "provides a unique resource," but does not say what it captures that the prior ciliary proteomes do not — beyond the obvious Smo-specificity. The claim is true but under-argued; a sentence on what the Smo-anchored view adds over whole-cilium proteomics would sharpen it.

## Sweep

- The "known Smo interactors recapitulated" claim (Fig. 2D-E) is a validation of the method, not a novelty claim; it is fine as framed but should not be double-counted as a contribution.
- The claim that Git1 interacts with both Smo and Grk2 (Fig. 4B, 5B) is asserted from proximity/Co-IP data; whether this is a direct or indirect interaction is a rigor question, not mine, but the novelty framing ("Git1 brings the two molecules together") leans on a mechanism the data only partially support.
- The differentiation from the authors' own prior Liu et al. 2024 TurboID-in-cilia work is not stated; a one-line head-to-head would help readers place the two resources.
- The Git1-null mouse phenotype link (microcephaly, cerebellar agenesis, Badea et al.) is cited as consistent with impaired Hh signaling, but the manuscript does not test Git1-null mice directly — the GNP data are knockdown, not knockout; the in vivo claim is extrapolation and should be flagged as such.
- The "new Smo-associated proteins" list (450/576 candidates) is presented as a resource, but only Git1 is characterized; the paper should be explicit that the rest are unvalidated candidates, not confirmed interactors.

## Questions

- Does the Smo-TurboID dataset capture any interaction that the prior whole-cilium proteomes (Mick 2015, May 2021) do not, beyond Smo-specificity — and can you state that delta in one sentence?
- Is the "ciliary shaft is the primary site" claim presented as new relative to Walker et al. 2024, or as a refinement of it? The abstract should make this explicit.

## Note on search limitations

My novelty searches (find_related_work, search_preprints) returned mostly irrelevant results for the biology-specific queries — the arXiv fallback surfaced physics/engineering papers, and bioRxiv returned nothing for the Git1-Hedgehog and Smo-TurboID queries. The one productive search (Semantic Scholar) surfaced the relevant prior literature (Chen 2011, Walker 2024, and the 2025/2026 Smo-PKA-at-cilia papers). On the basis of that productive search and the absence of any Git1-Hedgehog hit, I judge the core novelty claim to survive; but my confidence is tempered by the noisy search environment, and I would flag that a dedicated literature check on Git1's role in Hh signaling is warranted before publication.

## Overall

The Git1 finding is genuinely new and the Smo-TurboID resource is a real contribution; the paper's core novelty claim survives my searches. The main issues are positioning: the ciliary-site claim is an extension of the authors' own prior work and should be framed as such, and the resource's delta over existing ciliary proteomics is asserted rather than argued. These are SOFT issues, not HARD — nothing here preempts the central claim.