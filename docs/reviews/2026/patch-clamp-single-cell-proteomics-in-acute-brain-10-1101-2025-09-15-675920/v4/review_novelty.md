# Novelty & Contribution Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript presents a framework for patch-clamp single-cell proteomics (patch-SCP) in acute brain slices, with the central methodological contribution being the preservation of the gigaseal during soma retrieval. The authors demonstrate that capacitance measured during retrieval correlates with protein identifications, that spike integrity during relocation is associated with synaptic protein enrichment, and that torn/aspirated neurons produce poor proteomes. They propose a "shotgun" strategy of indiscriminate collection to benchmark retrieval quality. The novelty claim is modest and largely methodological: maintaining whole-cell access during retrieval to link electrophysiological properties to proteomic yield.

## Strengths

1. The framework of categorizing retrieval outcomes (gigaseal preserved/lost/never formed) and analyzing all samples indiscriminately is a genuinely useful methodological contribution that addresses a real gap in patch-SCP practice.
2. The correlation between capacitance during retrieval and protein identifications is a concrete, testable finding that could serve as a quality-control metric for future patch-SCP studies.
3. The authors are candid about limitations, including the small sample size (n=3 for gigaseal-preserved retrievals) and the incomplete recovery of membrane proteins.

## Load-Bearing Weaknesses

**1. The central claim — that gigaseal preservation during retrieval provides a quantitative bridge between electrophysiology and proteomics — rests on an n=3 correlation.** The capacitance-protein identification correlation (F=1577, p<0.05, adjusted R²=0.998, n=3) is striking but statistically fragile. With three data points, a single outlier drives the entire fit. The authors acknowledge the small sample size but do not address the specific fragility of a three-point regression. The claim that "soma size, which is proportional to capacitance, plays a more direct role in protein recovery than RM" is asserted from this n=3. What would distinguish the authors' account from a null hypothesis where any passive property (or simply retrieval ease, which correlates with soma size) predicts yield? A larger cohort, or at minimum a statement of the confidence interval on the slope, would be needed. I could not verify the regression from the text alone; the figure is referenced but the underlying data are not tabulated.

**2. The claim that "preservation of active properties during retrieval is associated with recovery of synaptic proteins" is based on a single qualitative comparison.** Neuron #6 (compromised spiking) lacked synaptic signaling enrichment while neurons #4 and #7 (better spiking) showed it. But neuron #6 was also the smallest neuron by capacitance, and the authors themselves show that size correlates with yield. The alternative explanation — that the synaptic enrichment difference reflects soma size, not spike integrity — is not excluded. The authors do not attempt to separate these confounded variables. A head-to-head comparison of two neurons matched for capacitance but differing in spike preservation would distinguish these accounts; the current data cannot.

**3. The "shotgun" indiscriminate-collection strategy is presented as a deliberate framework, but its value is asserted rather than demonstrated.** The authors show that torn neurons cluster separately in PCA and that protein counts alone are unreliable indicators of sample quality. However, the claim that this approach "enables systematic evaluation of retrieval quality" is not tested against any alternative — e.g., a threshold-based exclusion strategy. The utility of the framework rests on the claim that proteome-centric analysis reveals retrieval problems that protein-count cutoffs would miss, but no comparison to such a cutoff-based approach is offered. The PCA separation of torn neurons is suggestive but the authors do not show that the separation is robust or that it would generalize beyond this dataset.

## Sweep

- The novelty claim is appropriately modest — the authors do not claim "first" for patch-SCP itself (which exists in prior work from Choi et al. 2022 and Lee et al. 2024), but the specific contribution of gigaseal-preserved retrieval with capacitance-yield correlation is not preempted by anything I found in related-work or preprint searches.
- The claim that "in situ recordings are not a prerequisite for achieving a large number of protein identifications" is interesting but under-analyzed — the authors do not explore whether the no-gigaseal retrievals differ systematically in composition from gigaseal-preserved ones beyond the PCA plot.
- The detection of ion channels (SCN2A, GABRA1, CACNA2D1) across samples is a useful capability demonstration, but the authors do not quantify recovery rates relative to expected expression, which would strengthen the claim that the workflow is adequate for neurophysiologically relevant proteins.
- The framework's generalizability to other brain regions or neuronal subtypes is asserted but not argued — the authors note that mPFC L2/3 pyramidal neurons were chosen for large soma, which may limit applicability to smaller or more fragile neurons.
- The distinction between "gigaseal lost during retrieval" and "no gigaseal" categories is clear, but the authors do not report whether the timing of gigaseal loss (early vs. late in retrieval) affects outcomes, which would be a natural extension of their framework.
- The claim that "retrieval mechanics, rather than in situ electrophysiology alone, limit whether proteins associated with excitability and synaptic function are recovered" is well-supported by the torn-neuron data but would be stronger with a quantitative statement of how much material is typically lost during retrieval (the authors estimate 25-50% but do not show how this was derived).

## Questions

1. For the capacitance-protein identification correlation (n=3), what are the individual data points and the 95% confidence interval on the slope? A three-point regression with R²=0.998 is sensitive to a single point; the raw values would allow assessment of robustness.

2. Can the authors separate the effects of soma size from spike integrity on synaptic enrichment? Specifically, is there a neuron in their dataset (or could one be added) with large capacitance but compromised spiking that would test whether the synaptic enrichment difference in neuron #6 is attributable to size or to retrieval damage?

3. How was the 25-50% soma loss estimate derived? The text references Figure 3C but does not explain the calculation.

## Novelty Assessment (auditable)

I searched for prior work on patch-clamp single-cell proteomics with gigaseal preservation during retrieval. Related-work searches for "patch-clamp single-cell proteomics acute brain slice," "patch-SCP soma retrieval gigaseal," and "single neuron proteomics electrophysiology retrieval" returned the expected prior work (Choi et al. 2022, Lee et al. 2024, Ghatak et al. 2024) but nothing reporting gigaseal-preserved retrieval with capacitance-yield correlation. Preprint searches (bioRxiv) for "patch-clamp proteomics single neuron" and "patch-SCP retrieval" similarly returned no preempting work. The specific contribution — using gigaseal preservation during retrieval as a quantitative bridge between electrophysiology and proteomic yield — appears novel. The framework's positioning against the "all-or-nothing" exclusion strategy used in prior patch-SCP studies is a genuine delta, though the authors could sharpen this by explicitly naming the prior studies that used threshold-based exclusion and stating what their approach does that those do not.