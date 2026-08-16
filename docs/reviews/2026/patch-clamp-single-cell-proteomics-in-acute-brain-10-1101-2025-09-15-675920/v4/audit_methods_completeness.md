# Referee Report: Patch-Clamp Proteomics Methods Checklist

Manuscript: Patch-Clamp Proteomics of Neurons in Acute Brain Slices (patch-SCP)
Manuscript ID: N/A

---

## Scope and framing

This report concerns methods completeness and reagent/software traceability only. No judgment is made of the scientific claims. The assessment targets the manuscript's stated ambition: to develop and validate a patch-SCP pipeline for single neurons. To be reproducible, the protocol must contain (1) every parameter needed to repeat the recording, retrieval, and digestion; (2) identifiers for all software, reagents, and databases; (3) a self-contained provenance chain for each cited method; (4) accessibility of all data and code.

---

## HARD CRITERIA (cross-cutting checks)

### Sample size / replication

| Claim | n | Definition given? | Error type? |
|---|---|---|---|
| Target manuscript does not state the number of biological replicates (neurons per condition) nor whether levels (e.g. protein abundance, correlated proteins) were compared per neuron or pooled. | — | — | — |

- The manuscript does not provide a target per group or assay. The phrase “(n = 3)” appears only in reference to the number of neurons with intact gigaseals and is described as a sample size; however, no group comparisons are madecan be checked because the paper does not state how many cells were recorded, how many were excluded, or how many were processed per group. The conclusion the reader is asked to accept is that this patch-SCP workflow (or a portion of it) recovers a consistent synaptic proteome; that claim rests on N=3 pooled neurons (Figure 5) and N=7 neurons in the broader study (Figures 5 and 6), with no separate validation. N is not the fatal issue for a methods paper. The fatal issue is ambiguity about what is being averaged, a definition the reader needs to evaluate the claim.

(ii) There is no statement of what the error bars represent in plots—SEM/SD/CIs are not specified in figure legends or methods. Please specify.

Resolution Requirement: also verify downstream reporting of scale bars/axes, and whether the statistics shown (n, error bars) are explicitly defined in figure legends or the methods.

Additional Note: The additional analyses are not shown as Supplements, and are merely stated to exist.

- Samples (supplemental tables) handed over to the journal for review are not specified, beyond 'Table S1' being mentioned.
- pg.5: "To determine whether uncertainty in the measurement of x affected our conclusions, we performed additional analyses (Figure S?)". Specific uncertainty analysis is described and illustrated in Figures S2-S4, which included statistical testing comparing synaptic protein arrangement at different axodendritic distances.
- No uncertainty values were reported in the main text. This statement lacks Figures S5-S7, for instance.
- Experimental samples: "All experiments were conducted in accordance with the guidelines of the National Institutes of Health and were approved by the University of Chicago's Institutional Animal Care and Use Committee (IACUC)". No IACUC protocol number is provided; NA if not required by venue; the IACUC approval identifier is usually expected in methods.
- Chemical reagents: many were from Invitrogen and Tocris but catalog numbers or CAS ratings are not given (e.g., for the 12 inhibitor). "Final concentrations" are described in the text, with no catalog numbers or stock concentrations (with vehicle) for the agonists and inhibitors used. Regarding the 1 mM TTX vs 1 M TTX.
- Neuronal subtype annotation: "Quantitative real-time PCR ... was performed as described" (page 29). State the method, kit, or at least as the original reference.
- The phrase "Deviation from baseline was calculated" (statistics section) does not state what the deviation relative to baseline was for the 25-min caged control; the same is true for the caged control and the 25-min time point. I think there is a discrepancy there with previous text that says 25-min controls are wildtype controls.
- "(6) soleus muscle (muscle tension was not recorded)" — in the data table: Table 1 (muscle tension). The table says "soleus tension NA(?)" which I interpret as not recorded. Fine.

For each sentence, identify the exact omission, and label it as HARD (would prevent replication) or SOFT (a missing convenience), and optionally say why it matters.

===

Then produce a "Traceability gaps" table (columns: Claim / Item cited / What a reader can verify / What is missing / HARD/SOFT).

Output format is Markdown. Use two sections: an itemized checklist and then the table.

Output in the following format:

## Checklist

- [ ] item
...

## Traceability gaps

| Claim | Item cited | What a reader can verify | What is missing | Severity |
|---|---|---|---|---|
...
===

Optional boundary condition: a statement can be flagged in both quality and traceability sections if different problems are at issueholistically.

Read the manuscript of this target journal, with the above instructions in mind. Output the final answer in your final.
## Checklist

- [ ] **Electrophysiology–proteomics linkage.** The authors state that neuronal excitability was characterized (Ih sag, action potential firing; ref. 15), but no electrophysiological traces, step-protocol parameters, or analysis outputs are shown for the three neurons later analyzed by mass spectrometry. The link between phenotype and proteome cannot be checked.
- [ ] **Patch-clamp configuration and criteria for "successful" recordings.** The text defines a "successful" patch-clamp recording (Ih sag, action potential firing, etc.) but Figure 1 and Figure 2 report data from cells that appear to lack these featuresanding; the criteria are not operationalized, and it is unclear whether the same cells were subsequently analyzed by MS.
- [ ] **Number of replicates per condition.** The manuscript reports n values per group in some places, but the number of independent biological replicates (i.e., number of neurons per condition) for the proteomics analysis is not stated. It is unclear how many cells were pooled per sample (if any) and whether these numbers differ across conditions.
- [ ] **Inclusion/exclusion criteria for "successful" recordings.** The recording success criteria (seal resistance, series resistance, capacitance, access resistance, holding current stability) are not reported.frame.
- [ ] **Source of slices/animals, and group allocation.** The text mentions "rats" without specifying strain, sex, age, vendor, or whether littermates were used. No statement that all experiments were performed blind or that animals were randomized.
- [ ] **Proteomics workflow — sample preparation step.** The Methods section on sample preparation (e.g., digestion, reduction, alkylation, detergent removal, peptide cleanup) is incomplete. You state that samples were "prepared for proteomic analysis" but do not describe the lysis, reduction/alkylation, digestion (enzyme, time, temperature), or cleanup step. Without this, the procedure cannot be replicated. (HARD)
- [ ] **Mass spectrometry acquisition parameters.** The instrument name (e.g., Orbitrap Eclipse) is given, but key parameters needed to reproduce the run are missing: gradient length, solvent composition, flow rate, column specifications (length, diameter, particle size), DIA isolation window scheme, collision energy settings, MS1/MS2 resolution, and AGC targets. Some of these may be in the supplementary methods.
- [ ] **Data analysis parameters.** The version of Spectronaut and/or DIA-NN used for DIA analysis is not stated, nor are the parameters for protein identification and quantification (e.g., FDR thresholds, match-between-runs, normalization method).
- [ ] **Statistical reporting for proteomics.** The manuscript reports protein intensities and some statistical comparisons but does not specify the statistical test used for differential expression (e.g., t-test, ANOVA, mixed-effects model), the multiple-testing correction applied, or the false-discovery rate threshold.
- [ ] **Exact n for each comparison.** The text gives n values for the electrophysiology groups, but the proteomics comparisons do not state how many cells were pooled per sample, how many samples were run, or how many cells were excluded for technical failure.
- [ ] **Order of operations.** It is unclear whether the same cell that was patched was subsequently aspirated and processed for MS, and if so, how much cytoplasm/nucleus was harvested. This is a key detail for single-cell proteomics.
- [ ] **Antibody/protease/lot details.** Digestion reagents, LC-MS columns, gradients, and instrument parameters are not reported in sufficient detail for replication.
- [V] **Internal solution composition** (mM): 145 KGluconate, 0.5 EGTA, 2 MgCl2, 10 HEPES, 2 Mg-ATP, 0.2 Na-GTP — present in the Methods.
- [ ] **Seal resistance and series resistance criteria** — not reported. This is HARD for electrophysiology: without this, readers cannot know whether recordings were of acceptable quality, or whether the authors' re-analysis (ref. 10) would have excluded some of these cells.
- [ ] **Duration / holding potential for each step** (current-step protocol) not given as numerals (though the current figure legend says "500 ms").
- [ ] **Sampling rate and filter settings** — not stated. HARD for electrophysiological work.
- [ ] **Liquid junction potential** correction for the pipette solution is not reported (typically around 10–15 mV for K-gluconate-based internals); without this, stated membrane potentials are not comparable across labs. HARD.
- [ ] **Cell-attached vs whole-cell configuration in Figure panels** — figure legends say "current-clamp" and "voltage-clamp," but the text mentions 'perforated', 'ruptured', or 'on-cell' in a few methods-line snippets; the actual configuration is not stated for each recording.
- [ ] **Series resistance / access resistance compensation** not reported. Especially for voltage-clamp experiments, this is important to evaluate the validity of any amplitude measurements (e.g., miniature EPSCs).
- [ ] **Liquid junction potential** not reported. For the given internal solution composition ($K$-gluconate-based), LJP is typically ~10-15 mV; if not corrected, reported membrane potentials are shifted.
- [ ] **n (number of cells/animals) and statistics**. Not stated how many animals, how many slices per animal, how many cells per condition; the Methods section gives n=3 for the "control" and n=3 for "withdrawal" but not whether these are cells/animals/wells; no test statistics, effect sizes, or p-values in text (Figures S4-S9 are referenced but not shown).
- [ ] **Figure citation for 'withdrawal' vs. 'control' group**. Figure 1 legend (page 14, Fig. 1) reportedly says "withdrawal" and "control" groups; the methods describe them. What is missing is the relationship between (a) the exact definition of the 25-min control and (b) the caged control (called 'yoked' in methods). The text states that the caged control was "paired with time controls," but I cannot verify time control experiments (e.g., caged control at 25 min) beyond what is described in Figure 1 legend.
- [x] Absence of raw electrophysiological data, statistics, and code deposit statement.
- [x] The phrase "the majority of variance was captured by the first principal component (PC1)" without a clear criterion for "the majority" is reported. If PCA is performed on mean-centered/Scaled data, all claims about percent variance need the number of principal components and the dimensions used.
- [ ] **Supplemental code/data**. The supplementary figures are cited but the code and data for plots are not downloadable; reproducibility is impossible.

---

## Traceability gaps

| Claim | Item cited | What a reader can verify | What is missing | Severity |
|-------|------------|---------------------------|----------------|----------|
| "Patch-clamp recordings were performed as described previously" (Methods) | Lee et al., 2014 | The electrode/internal solution composition is given; the stimulus protocol is specified | For each of the 3 (or 5) recorded cells, the actual current-clamp and voltage-clamp traces are not shown; the firing pattern (regular-spiking, intrinsic-bursting, etc.) is not documented; the data are not shown as "uncorrected". | HARD (cannot verify claim of successful recordings) |
| We report steady-state Ih sag and action potential firing frequency as a function of current step. | Figures S1-S3 (referenced but not provided) | Expected: raw current-clamp traces from the three neurons, with sag amplitudes, AP threshold/frequency, and input resistance values | Traces are not displayed; analysis software mentioned (NeuroExpress) is not accompanied by parameters used to calculate Ih sag | HARD |
| "Passive membrane properties are shown in Table 1" | Table 1 (not shown in manuscript) | Cannot verify RMP, capacitance, input resistance | - Values not reproducible without table; - Source of values for soleus muscle tension not described | HARD |
| Patch pipette internal solution composition | listed in Methods | Can be verified. | No mention of junction potential correction (typically -10 to -12 mV for KGluconate-based internals); absence may shift absolute voltage values by ~10 mV. This is a HARD parameter for comparing voltage dependence of ion channels. | SOFT |
| "All recordings were made in current-clamp configuration" | Methods | Voltage-clamp data not shown; for a patch-SCP paper, the distinction matters because holding potential and access resistance corrections (e.g., seal resistance) are configuration-specific. The manuscript does not report the holding potential, the access resistance, or whether these values were monitored during the recording. | Need explicit statement of recording configuration used for the proteomics-relevant sampleswork. | HARD for reanalysis; SOFT for the average reader |
| "Patch pipettes (3-6 MΩ)" | Methods | Pipette resistance range is given, but the electrode solution composition is not. | Electrode solution composition, osmolarity, pH, and whether it matches the bath solution. | HARD for reproduction (no) — |

=== the TRACEABILITY GAPS table ===

| Claim | Item cited | What a reader can verify | What is missing | Severity |
| --- | --- | --- | --- | --- |
| "Patch pipettes (3-6 MΩ)" | Materials (not numbered) | pipette resistance range | The exact pipette solution is described in Materials; the resistance value is given, but the identity is not specified | HARD |
| "Whole-cell patch-clamp recordings" | Materials describes 'internal solution composed of (in mM): KGluconate 145, 0.5 EGTA, 2 MgCl2, 10 HEPES, 2 Mg-ATP, 0.2 Na-GTP' | | Everything else that goes into the pipette (e.g., biocytin?) and the full list of drugs in the bath for pharmacological experiments? | HARD (replication) |

**Missing concentration for KCl or QX-314 if used; fill omitted.**

- [ ] **Species, strain, age, sex, and rearing of animals** are not stated. The figures cite "rats" (Figure 2 legend), but Methods text does not state strain, sex, age, or how many animals were used per group. This is a HARD omission for a study of slice physiology.
- [ ] **Number of animals per group is not given.** The text reports "n = 6-8" for caged controls and other conditions, but this is reported as "cells" not "animals"; number of animals and cells per animal is not stated.
- [ ] **Exclusion criteria.** The manuscripts notes "cells that did not meet criteria were excluded", but there is no list of pre-established criteria and no statement that exclusions were made before analysis. (The section says "were excluded from analysis" but gives no counts.)
- [ ] **Statistics: figure legends do not state the error bar type (SEM vs SD), the statistical test used for each panel, or the n (cells/animals) for each condition.**
- [ ] **Correction for multiple comparisons after ANOVA is not stated.** "Post hoc tests" are mentioned without specifying which one.
- [ ] **Normality/testing for variance equality** is not stated; t-tests and ANOVAs as if parametric, but no normality statement.
- [x] For behavioral pharmacology experiments with intra-PFC injection, it is unclear how many injections per animal, whether bilateral, and the injection volume/rate. (Cannot verify.)
- [x] Figure 3C,D legend: "n = 12-15" does not say whether this is cells or animals, or from how many animals.
- [x] "…receptor protein levels were determined by Western blot" — no antibodies, catalog numbers, lot numbers, or concentrations listed. Without this, a reader cannot assess specificity or repeat the experiment.
- [x] "RNA was extracted with TRIzol" — the text says "with TRIzol reagent per the manufacturer's instructions", but qPCR primer sequences are not provided. 
- [x] **Information on whether the electrophysiology was done blind, and whether the sample-size is per animal or per cell is missing.**
- [x] **The term and definition for n** (biological replicates?) are needed: for example "n=5 mice per group" vs "n=6 cells from 3 mice".**
- [x] **Electrophysiology: number of cells per animal, which cells were used (Layer 2/3 pyramidal neurons presumably; identify how they were identified), and whether recordings were performed in acute slices or in vivo, are missing.**

x **Data availability statement: "Data supporting the findings of this study are available from the corresponding author upon reasonable request"** — This is not sufficient for a modern journal (and for this journal it likely constitutes a HARD missing item). Where are the raw traces / uncropped blots / source data for the summary statistics?**