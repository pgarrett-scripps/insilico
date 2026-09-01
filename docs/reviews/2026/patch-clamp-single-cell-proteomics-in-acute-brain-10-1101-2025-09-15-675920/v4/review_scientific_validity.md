# Scientific Validity & Claims Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents a framework for interpreting patch-clamp electrophysiology combined with single-cell mass spectrometry proteomics (patch-SCP) in acute brain slices, with emphasis on how soma retrieval quality shapes proteomic recovery. The work is methodologically honest and addresses a real technical problem—the decoupling of electrophysiological measurements from proteome recovery during neuron extraction. However, the central claims rest on a very small sample (n=3 for gigaseal-preserved retrievals, n=12 total), and the evidence for the load-bearing conclusions does not exclude plausible alternatives. The framework itself is conceptually sound but the empirical support for its predictive utility is limited. The paper makes useful negative findings (in situ recordings do not predict proteomic yield) but the positive claims about what *does* predict yield are underdetermined by the data.

## Strengths

1. The authors explicitly acknowledge and systematically examine a source of variability (soma retrieval mechanics) that prior patch-SCP work has either ignored or excluded by selection criteria, and they provide video evidence of retrieval outcomes.

2. The decision to analyze all retrieval attempts rather than only high-quality samples is methodologically principled and generates honest negative results (e.g., Figure 5: in situ capacitance does not correlate with protein yield when gigaseal is lost).

3. The framework mapping patch-clamp outcomes to interpretive contexts (Figure 1) is conceptually clear and the authors are candid about compartmental bias and the limits of soma-only sampling.

## Load-Bearing Weaknesses

**Claim 1: Soma capacitance measured during gigaseal-preserved retrieval predicts proteome yield.**

Evidence: Figure 3D shows correlation between log-transformed capacitance and protein identifications (F=1577, p<0.05, adjusted R²=0.998, n=3). 

The problem: This correlation is based on only three neurons, all from the same brain region and cell type, retrieved by the same experimenter on the same day. The extraordinarily high R² (0.998) with n=3 is a red flag for overfitting rather than a generalizable relationship. The authors do not report whether these three neurons were pre-selected for successful gigaseal preservation (which would introduce selection bias) or were consecutive attempts. Critically, capacitance is proportional to soma surface area, and protein yield is expected to scale with soma size for purely physical reasons—this is not a novel finding and does not establish that *retrieval quality* (the paper's central claim) predicts proteome recovery. A torn neuron with a large soma would also yield many proteins if enough material remains. The correlation does not distinguish between "gigaseal preservation preserves material" and "larger somas yield more protein regardless of retrieval method." To settle this, the authors would need to compare protein yield in gigaseal-preserved vs. gigaseal-lost retrievals *within the same size range* of neurons, or to show that the relationship between capacitance and protein yield differs systematically between preserved and lost gigaseals.

**Claim 2: Preservation of neuronal spiking during retrieval is associated with broader synaptic enrichment.**

Evidence: Figure 4 shows that neuron #4 (stable spiking) had the most enriched synaptic biological process terms, while neuron #6 (single spike, compromised) lacked significant synaptic enrichment despite detecting ion channels.

The problem: This is a post-hoc observation on n=3 neurons with gigaseals, ordered by spike quality. The authors interpret spike integrity as a proxy for "physical disruption" and thus material loss, but spike amplitude and frequency are also sensitive to electrophysiological state (temperature, oxygen, time under recording, dialysis of the cytoplasm during whole-cell access). A neuron with reduced spiking may have been recorded longer, dialyzed more, or experienced more metabolic stress—any of which could alter the proteome independent of physical retrieval damage. Neuron #7 showed reduced spike amplitude but clustered with neuron #4 in synaptic enrichment (Figure 4C), contradicting the claim that spike integrity predicts synaptic recovery. The authors note this ("neuron #7 showed the fewest unique BP terms" despite good synaptic overlap) but do not resolve it. To distinguish retrieval-induced material loss from electrophysiological state effects, the authors would need to measure spike properties in neurons retrieved under identical conditions but with different gigaseal outcomes, or to show that spike degradation correlates with specific protein losses (e.g., axonal or presynaptic markers) rather than global proteome shrinkage.

**Claim 3: The framework enables interpretation of how retrieval quality shapes proteomic measurements in semi-intact circuits.**

Evidence: Figure 6 PCA and SynGO analysis show that neurons cluster by retrieval outcome and synaptic enrichment, and the authors argue this allows "benchmarking retrieval integrity."

The problem: The framework is descriptive, not predictive. The authors show that torn neurons cluster apart (expected) and that neuron #6 clusters with failed gigaseals despite having a gigaseal (Figure 6A), but they do not demonstrate that the framework can prospectively identify compromised retrievals or guide decisions about sample inclusion. Neuron #1 (no gigaseal) yielded an unusually large proteome and clustered with successful recordings (Figure 6A), yet the authors cannot explain why. The framework does not predict which neurons will have good synaptic enrichment from retrieval outcome alone—neuron #7 and #4 had similar outcomes but different GO profiles. The authors acknowledge this ("categorical patch-clamp outcome alone does not reliably predict the biological content of single-neuron proteomes," Results section) but then claim the framework enables interpretation. These are in tension: if outcome does not predict content, the framework's utility for prospective sample selection is unclear. The framework works post-hoc to contextualize results but does not provide actionable guidance for future experiments. To support the claim, the authors would need to show that the framework correctly predicts (in a held-out or new dataset) which samples will have good synaptic enrichment, or to reframe the contribution as a post-hoc interpretive tool rather than a predictive framework.

## Sweep

1. The claim that "capacitance during gigaseal-preserved retrieval correlated with protein identifications" (Abstract) is stated as a key result, but the correlation is driven by soma size, not retrieval quality per se, and the n=3 sample size does not support generalization.

2. The authors state they "did not impose selection or exclusion criteria" (Methods) but do not report whether the three gigaseal-preserved neurons were consecutive attempts or selected post-hoc, which would affect interpretation of the correlation in Figure 3D.

3. Figure 5 shows that in situ capacitance does not predict protein yield when gigaseal is lost (n=6), but the authors do not test whether *retrieval-time* capacitance (measured during relocation, as in Figure 3C) predicts yield in the larger dataset, which would directly test the framework's core claim.

4. The paper claims neurons were collected "indiscriminately" but neuron #11 and #12 are labeled as "torn" and used as negative controls; it is unclear whether these were identified as torn before or after MS analysis, and whether they were included in the correlation analyses.

5. The detection of ion channels (Figure 7) varies widely (4–27 subunits) across retrieval outcomes, but the authors do not report whether this variation correlates with spike integrity or synaptic enrichment, which would test whether retrieval quality predicts recovery of functional protein classes.

6. The authors use DIA-MS, which is more sensitive than prior patch-SCP work using DDA, but do not compare their ion channel and GPCR recovery rates to published patch-SCP studies to establish whether the framework improves detection of low-abundance transmembrane proteins.

7. The paper does not report the time elapsed between retrieval and MS analysis, which could affect proteome composition and would be relevant to interpreting variability across samples.

8. SynGO analysis uses a Q-value threshold of <0.05 without multiple-testing correction across the full set of GO terms tested, which may inflate false positives in the enrichment claims.

## Questions

- Figure 3D: Were the three gigaseal-preserved neurons selected prospectively (consecutive attempts) or identified post-hoc as successful retrievals? If post-hoc, does the correlation hold for all attempted gigaseal retrievals, including failed ones?

- Figure 4C: Neuron #7 shows reduced spike amplitude but overlaps with neuron #4 in synaptic BP enrichment. How does this fit the claim that spike integrity predicts synaptic recovery, and what explains the discrepancy?

- Methods: What is the operational definition of a "torn" neuron (Figure 5B), and was this assessment made blind to MS results? Were torn neurons included in any of the correlation analyses?

- Figure 7: Does the number of detected ion channel subunits correlate with spike integrity or synaptic enrichment (Figure 4C)? If not, what explains the variation in transmembrane protein recovery?