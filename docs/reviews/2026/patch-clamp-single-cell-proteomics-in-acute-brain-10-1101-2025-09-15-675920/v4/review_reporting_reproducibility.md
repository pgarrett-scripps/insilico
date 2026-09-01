# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall assessment

This manuscript presents a methodologically sound framework for interpreting patch-clamp single-cell proteomics in acute brain slices, with explicit attention to how soma retrieval mechanics influence proteomic recovery. The work is well-documented, the authors are transparent about limitations, and the core finding—that retrieval integrity rather than in situ electrophysiology alone predicts proteome quality—is supported by the data presented. Reproducibility is strong across most dimensions, though a few procedural details and data-processing decisions require clarification. The contribution is incremental but honest and useful for the field.

## Strengths

1. The authors release raw mass spectrometry data (ProteomeXchange PXD068359), search results, and analysis code on GitHub, enabling independent verification of the proteomics pipeline and downstream GO enrichment.

2. All patch-clamp recordings are documented with video evidence (Zenodo DOI provided), allowing readers to inspect retrieval quality directly rather than relying on categorical labels alone.

3. The framework explicitly maps electrophysiological outcomes to interpretive constraints rather than discarding partial retrievals, which is methodologically honest and maximizes signal from labor-intensive manual recordings.

## Load-bearing weaknesses

**Claim 1: Soma capacitance measured during retrieval predicts protein identifications.**

The correlation reported (Figure 3D: F=1577, p<0.05, adjusted R²=0.998, n=3) rests on only three neurons with gigaseal preservation. This sample size is acknowledged as exploratory, but the extremely high R² (0.998) with n=3 raises a red flag: with only three points, even a perfect linear fit is expected by chance if measurement error is small. The authors do not report the residual standard error, confidence intervals on the slope, or whether the fit remains significant if one neuron is removed (leave-one-out cross-validation). The claim that "capacitance plays a more direct role in protein recovery than RM" depends entirely on this correlation; without robustness checks, it is unclear whether the relationship is real or an artifact of the tiny sample. What would settle this: report 95% CIs on the slope and intercept, and show the fit with one neuron removed.

**Claim 2: Preservation of neuronal spiking during relocation is associated with broader synaptic enrichment.**

Figure 4 shows that neuron #4 (stable spiking) has more enriched synaptic biological process (BP) terms than neuron #6 (single spike), and neuron #6 lacks significant enrichment for synaptic signaling despite detecting ion channels. However, neuron #6 is also the smallest (lowest capacitance), and the authors themselves establish that size predicts protein recovery (Claim 1). The association between spike integrity and synaptic enrichment is therefore confounded by soma size: a smaller soma yields fewer proteins overall, which reduces the chance of detecting rare synaptic terms, independent of retrieval damage. The authors do not stratify by size or use a statistical model that accounts for it. The claim would be stronger if the same enrichment pattern held when comparing neurons of similar size but different spike integrity, or if enrichment were normalized by total protein count. What would settle this: report SynGO enrichment for neurons #4 and #7 (both large, similar spike integrity) versus #6 (small, poor spikes), or show that the number of enriched terms correlates with spike quality after controlling for capacitance.

**Claim 3: Retrieval loss decouples in situ electrophysiology from proteome recovery.**

Figure 5A-D shows that in situ capacitance and RM do not correlate with protein identifications across all neurons (n=6, p>0.05). However, this comparison mixes neurons with different retrieval outcomes (gigaseal preserved, lost, or never formed). The authors argue this demonstrates that "mechanical retrieval can introduce sample loss," but the result is also consistent with a simpler explanation: in situ recordings simply do not predict proteome yield because the two measure different things (soma size in situ vs. material recovered post-retrieval). The authors do not show that capacitance measured *during* retrieval (when the gigaseal is preserved) fails to predict protein recovery; they show that capacitance measured *before* retrieval does not. This is a weaker claim than stated. The decoupling narrative would be stronger if the authors demonstrated that neurons with stable in situ recordings but poor retrieval mechanics (e.g., torn during withdrawal) yield smaller proteomes than those with poor in situ recordings but intact retrieval. What would settle this: stratify Figure 5C-D by retrieval outcome (gigaseal preserved vs. lost vs. torn) and show whether the lack of correlation holds within each stratum.

## Sweep

1. DIA-NN v1.8.1 was used with "match-between-runs" enabled and 1% FDR filtering; the manuscript does not state whether the FDR was applied globally across all samples or per-sample, which affects reproducibility of the protein group counts reported in Figure 3F.

2. The UniProt Mus musculus reference proteome was used to search rat (Rattus norvegicus) samples; the authors do not justify this choice or report how many peptides map ambiguously between species, which could inflate or deflate protein identifications.

3. SynGO enrichment was performed with "stringent" GSEA filtering (Methods), but the specific parameters (e.g., minimum gene set size, permutation count) are not provided, preventing independent replication of the GO heatmaps in Figures 4C and 6B.

4. The three neurons with gigaseal preservation (Figure 3) are not identified by their neuron numbers in the figure legend, making it unclear which of the 12 total neurons they are and whether they are a representative subset.

5. Neuron #1 is noted as yielding an "unusually large proteome" and being located near the slice surface (Video S4), but no quantitative comparison of location (distance from surface) to proteome size is provided, leaving this observation anecdotal.

6. The manuscript states that "25–50% of the soma could be lost over the course of collection" (Results) but provides no calculation or data supporting this range; the basis for this estimate should be made explicit.

7. Videos S1–S3 are referenced as evidence of retrieval quality, but the manuscript does not specify the frame rate, duration, or criteria used to classify retrievals as "stable," "compromised," or "torn" from video inspection alone.

8. The internal solution for patch pipettes includes 2 Mg-ATP and 0.2 Na-GTP, but the manuscript does not state whether these were replenished during long recordings or whether ATP depletion could have affected the passive membrane properties measured during retrieval.

## Questions

- Figure 3D: Are the three gigaseal-preserved neurons a pre-specified subset, or were they selected post hoc from a larger attempt pool? If post hoc, what was the selection criterion?
- Methods: Was the UniProt Mus musculus database chosen because rat sequences are not available, or for another reason? How many peptides map to both species?
- Figure 5: Why are neurons #11 and #12 (torn) included in the correlation analysis in panels C–D if they are described as negative controls? Should they be excluded from the regression?