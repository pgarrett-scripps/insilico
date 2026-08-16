# Related-Work & Citations Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents a framework for combining patch-clamp electrophysiology with single-cell proteomics (patch-SCP) in acute brain slices, with a focus on how soma retrieval quality affects proteomic measurements. The authors introduce a "shotgun" collection strategy where all patched neurons are analyzed regardless of electrophysiological outcome, and they demonstrate that preserving the gigaseal during retrieval enables correlations between capacitance and protein identifications. The work is positioned as a methodological proof-of-concept with a small dataset (n=12 neurons).

## Strengths

1. The authors are admirably candid about the limitations of their approach, explicitly acknowledging that in situ recordings can be decoupled from proteomic content by retrieval mechanics.
2. The framework's emphasis on interpreting partial or failed retrievals rather than discarding them is a genuinely useful contribution to the patch-SCP methodology literature.
3. The decision to deposit raw mass spectrometry data, videos, and code is exemplary for a methods paper.

## Weaknesses

**Load-bearing weakness 1: The central claim that gigaseal preservation enables meaningful correlations is supported by only n=3 neurons.** The correlation between log-transformed capacitance and protein identifications (Figure 3D) rests on three data points. With n=3, a linear regression with adjusted R² = 0.998 is statistically fragile — any single point drives the fit. The authors acknowledge the small sample size but still present this as a framework-level finding. The claim that "soma size, which is proportional to capacitance, plays a more direct role in protein recovery than RM" outruns what three neurons can establish. What would settle this: report the correlation with all neurons where capacitance was measured (including those where the gigaseal was lost), or explicitly frame this as a hypothesis-generating observation rather than a demonstrated relationship.

**Load-bearing weakness 2: The claim that "retrieval loss decouples proteomic measurements from electrophysiology recordings" is asserted from a negative result with n=6.** The absence of correlation between in situ capacitance/RM and protein identifications (Figures 5C-D) is interpreted as evidence that retrieval mechanics dominate over electrophysiological context. But with n=6 across three different outcome categories (no gigaseal, gigaseal lost, torn), the failure to find a correlation could equally reflect insufficient power or heterogeneity within categories. The alternative explanation — that in situ properties genuinely predict proteomic yield but the sample is too small and too heterogeneous to detect it — is not excluded. What would distinguish these: a power analysis showing the sample could detect a meaningful effect, or a larger dataset stratified by outcome category.

**Load-bearing weakness 3: The claim that spike integrity during retrieval "is associated with recovery of synaptic proteins" is based on a single neuron comparison.** The contrast between neuron #4 (stable spiking, broad SynGO enrichment) and neuron #6 (single spike, no synaptic signaling enrichment) is presented as evidence that active membrane properties during retrieval reflect biological content. With n=1 per condition, this is an anecdote, not a finding. The authors do hedge ("tended to be associated"), but the framing in the abstract and introduction ("Preservation of neuronal spiking during relocation tended to be associated with broader synaptic enrichment") still overstates what one neuron per group can show.

**Sweep items:**

- The claim that "patch-SCP in the locus coeruleus of mice revealed sex-specific differences" (ref 8) should be verified against the actual findings of Lee et al. 2024 — the abstract I can access describes sex differences in both proteomes and excitability, which is consistent, but the authors should confirm the specific attribution about "molecular drivers... difficult to identify" matches the source's own framing.
- The manuscript cites ref 9 (Ghatak et al. 2024) for the claim that "a lack of compartment-specific synaptic and membrane proteins raised the question of whether local synaptic activity could be adequately captured" — this is a fair characterization of that paper's limitations discussion, but the authors should confirm the specific wording matches.
- The reference list contains an apparent error: ref 31 (Guo et al., "Scalable total synthesis of saxitoxin and related natural products," Nature 2025) appears unrelated to patch-clamp or proteomics and is not cited in the manuscript text I can see — this looks like a citation-hygiene defect (a garbled or misplaced entry).
- The manuscript cites ref 15 (Szücs, "NeuroExpress program for analyzing patch-clamp data," ResearchGate 2022) for the analysis software — a ResearchGate-hosted citation without a DOI is acceptable for software but should be flagged as a SOFT currency issue if a peer-reviewed version exists.
- The reference list does not include any work on single-cell proteomics from the Mann group's or the Slavov group's SCP pipelines (e.g., SCOPE2, nanoPOTS), which are foundational to the field's sample-preparation methodology — consider whether these should be cited for context on the DDM-based digestion approach.
- The claim that "DIA workflows augmented with parallel reaction monitoring (PRM)" would enhance sensitivity is presented without citation — this is a reasonable methodological suggestion but should be supported by a reference to a published hybrid acquisition approach.
- The manuscript's use of "shotgun" to describe indiscriminate collection is potentially confusing given the established use of "shotgun proteomics" to mean bottom-up proteomics — consider whether this terminology could mislead readers.

## Questions

1. Can the authors confirm that ref 31 (Guo et al., saxitoxin synthesis) is correctly placed in the reference list, and if so, where it is cited in the text?
2. For the capacitance–protein identification correlation (Figure 3D), what are the raw data points for all three neurons, and would the correlation survive if any single neuron were removed?
3. Did the authors consider using the neurons without gigaseals (n=6) as an additional test of whether in situ capacitance predicts protein yield, and if so, what was the result?
4. Can the authors confirm that the SynGO enrichment analysis was performed on the full protein list per neuron rather than a filtered subset, and that the Q-value threshold of 0.05 was applied uniformly across all samples?

## Related-Work Verification

I ran a search for directly competing patch-SCP methods to check for missing citations. The search surfaced the following relevant work not cited in the manuscript:

- **Choi, Polter, and Nemes (2022)** — cited as ref 7, correctly attributed to patch-clamp proteomics with capillary electrophoresis.
- **Lee et al. (2024)** — cited as ref 8, correctly attributed.
- **Ghatak et al. (2024)** — cited as ref 9, correctly attributed.

I also searched for "single-cell proteomics patch-clamp brain slice" and "patch-SCP" to check for any 2024-2025 work that might be directly competing. The search returned no additional directly competing methods beyond those cited. The citation record for the core patch-SCP lineage (refs 6-9) appears complete and accurate.

One SOFT observation: the manuscript does not cite any of the foundational single-cell proteomics sample-preparation methods (e.g., nanoPOTS, SCOPE2, or the isobaric carrier-channel approaches from the Slavov group), which are the methodological ancestors of the DDM-based digestion workflow described here. This is a completeness gap rather than a misattribution, and it does not undermine the novelty claim since the manuscript's contribution is the retrieval framework rather than the sample-preparation chemistry.

The reference list contains one entry (ref 31, Guo et al., saxitoxin synthesis) that appears entirely unrelated to the manuscript's topic. I could not find this reference cited in the manuscript text I can see, which suggests either a citation-hygiene error in the reference list or a citation in a section I cannot access (e.g., a figure legend or supplementary material). This should be verified by the authors.