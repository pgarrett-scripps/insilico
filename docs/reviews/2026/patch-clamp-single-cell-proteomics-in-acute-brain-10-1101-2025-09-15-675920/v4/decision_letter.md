# Decision Letter

VERDICT: major

## Summary of Evaluation

Five of eight panelists score this manuscript 2–3/5 in the dimensions that matter most here (methodology, rigor, data analysis), and the central objection is concordant rather than idiosyncratic: the paper's headline claims run ahead of the evidence presented. Three reviewers recommend rejection; two recommend minor revisions; one recommends acceptance. I am converting the strongest critical signal into a *major revision* rather than a rejection because the weakness is calibrational and framing, not structural — the underlying design is a legitimate proof-of-concept, the conceptual framework is genuinely novel, and the gap between what was measured and what is claimed can be closed without abandoning the work.

What survives scrutiny: the framework itself, the indiscriminate "shotgun" collection strategy, the honest inclusion of torn and no-gigaseal retrievals as internal comparators, and the integrity of the data deposition (MassIVE/PXD, Zenodo videos). The novelty audit confirms the gigaseal-preserved-retrieval-with-capacitance approach is not preempted. These are real contributions, and the ethics/reproducibility auditors found no HARD compliance failures.

What does not survive as written:

1. **The central correlation (capacitance vs. protein identifications) is an n = 3 point inference.** F = 1577, adjusted R² = 0.998 on three points is a descriptive alignment, not evidence of a relationship. The rigor, methodology, and data-analysis reviewers correctly label the "links soma size to proteome yield" formulation as unsupported. This claim must be downgraded to an explicitly hypothesis-generating observation — or, if the authors prefer to keep it as a finding, they need the dataset to support it.

2. **The spike-integrity → synaptic-enrichment claim is confounded by the authors' own variable.** Neuron #6 (worst spiking) was also the smallest neuron by capacitance, which the authors themselves show tracks yield. The claim that spiking preservation *per se* drives synaptic protein recovery is not isolable from soma size in the present data. The abstract's wording outruns the test.

3. **The design's most defensible claims are "risk of the obvious."** That torn cells yield fewer proteins than intact ones is trivially true. The more interesting claims — that in situ electrophysiology cannot predict recovery, and that protein counts alone are unreliable quality metrics — are plausible but supported by null results at n = 6 and descriptive PCA, neither of which can distinguish "no effect" from "underpowered."

4. **Reproducibility is partial.** Data are deposited, but the custom scripts' GitHub link resolves to a user profile rather than a named repository; DIA-NN parameters, the SynGO pipeline parameters, reduction/alkylation steps, and the LC gradient composition are all underspecified. This is a HARD closure gap for a methods paper whose entire contribution is procedural.

5. **Citation hygiene.** Ref [31] (Guo et al., saxitoxin synthesis) appears in the methods block but bears no relationship to the claim it supports — a soft citation-integrity flag that must be corrected. Ref [8] "cytoplasm-limited" and ref [9] "hyperlink association" attributions should be confirmed against the source full texts.

The verdict distribution (3 reject / 2 major) in the panel cluster reflects reviewers' irritation that the headline claims do not survive. My judgment is that the design is sound for a proof-of-concept, the field genuinely lacks a retrieval-quality framework for patch-SCP, and the repairs are achievable in revision. That is the definition of `major`, not `reject` — the fix is reframing to match the evidence, closing reproducible gaps, and cleaning the citations.

## Required Revisions

1. **Recalibrate the capacitance–yield claim.** Remove "links soma size to proteome yield" and equivalent statements from the abstract, results, and conclusions. Report the three individual data points (capacitance and protein counts) with confidence intervals on the slope, and present this explicitly as a hypothesis-generating observation from n = 3, not a demonstrated relationship. State in plain terms that the correlation cannot be distinguished from a near-perfect fit expected at this sample size. If the authors wish to retain it as a relationship, the alternative: report the regression on the entirety of the gigaseal-preserved cohort (i.e., new data).

2. **Resolve the spike-integrity / soma-size confound in the text.** Neuron #6 had both the worst spiking and the smallest capacitance. Either (a) acknowledge explicitly that the reduced synaptic enrichment could be a size effect rather than a retrieval effect and temper the claim accordingly, or (b) add quantitative spike-integrity metrics (mean amplitude, spike count during depolarization) for neurons #4, #6, and #7 and show that the relationship to SynGO enrichment persists independent of capacitance. Do the same for the Figure 7 ion-channel comparisons — normalize channel recovery to total identifications, since the claim "gigaseal neurons recovered broader diversity" is contradicted by the authors' own text for several cases.

3. **Reproducibility closure (HARD for a methods paper).**
   - Provide a named GitHub repository (or Zenodo DOI) with a commit hash for the analysis scripts, keyed to figures, and specify the SynGO run (version, minimum gene-set size, background, BH/FDR method, per-sample input).
   - Report full DIA-NN settings: precursor FDR, mass tolerance, MBR precision, quantification mode; the exact UniProt release (not just "2024").
   - Specify: reduction/alkylation steps (or state none), digestion buffer (beyond 0.02% DDM), quench details, exact LC mobile phase composition (%B at the gradient shape) and column temp.
   - Electrophysiology: report the liquid-junction potential correction (or its absence), sampling rate and filter, series resistance/access resistance criteria, and the holding/step parameters for the current-clamp protocol. Report the number of animals, number of slices per animal, and per-animal neuron counts, and whether retrieval categories were assigned blind to the MS results.

4. **Operationalize the "torn"/"gigaseal-lost" categories.** Define a priori the criteria separating torn from gigaseal-lost from preserved (e.g., visible membrane breakage, suction artifact, loss of capacitive transient). The current post-hoc visual assignment cannot be reproduced and is not blinded.

5. **Citation hygiene.** Remove or relocate and justify ref [31]. Confirm the attributions to refs [8] and [9] against the primary texts, and note where NeuroExpress (ref [15]) is publicly accessible (or provide version and export settings if not).

6. **Fix internal inconsistencies.** (a) The abstract's "thousands of proteins" should be the actual range across samples (1,400–2,300) or qualified by the torn-neuron outliers. (b) Replace "demonstrate" with "hypothesis-generating" in the Conclusions where the results only support the weaker form. (c) State the denominator — the total number of patch attempts and how many yielded no detectable proteome at all.

## Minor Suggestions

- The "shotgun" label, while evocative, risks colliding with "shotgun proteomics"; consider defining "indiscriminate collection" terminology at first use.
- Test the framework's claims against a threshold-exclusion comparator in discussion (the authors note the value of this strategy over cutoffs but do not directly compare).
- Address the contamination alternative in the synapse-dense mPFC (adherent tissue fragment confounding), and the 25–50% soma-loss estimate should be shown as calculation (capacitance before/after? imaging?).
- Add the foundational SCP sample-preparation citations (nanoPOTS, SCOPE2, isobaric-carrier approaches) for context of the DDM-based digestion with which DIA builds.

These demands are substantial but entirely achievable in the text and deposited materials. The revisions must fix the evidence claims that are currently structural caulk. If the authors are able, additional gigaseal-preserved neighborhoods or a post-hoc sensitivity analysis (refreshing the correlation with the removal of each point) would strengthen the most contentious claim without further animal work.