# Reporting & Reproducibility Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript reports the discovery of SR-218, a small-molecule inhibitor of cGAS-STING signaling, and identifies IPO9 as its cellular target through chemical proteomics. The authors then characterize IPO9's role in releasing cGAS from H2A-H2B dimer-mediated inhibition using biochemical assays and cryo-EM. The work is well-executed across multiple complementary methods, with detailed protocols and data availability statements. Reproducibility is strong overall, though a few procedural details and statistical reporting gaps require clarification.

## Strengths

1. Comprehensive data availability: atomic coordinates and cryo-EM density maps are deposited (PDB 13ME, EMDB EMD-77152); recombinant proteins are explicitly sourced or generated with clear purification protocols; cell lines are named with ATCC/vendor identifiers (THP-1 Dual, THP-1 Lucia ISG from Invivogen).

2. Multi-method validation of target engagement: rhodamine labeling, BLI, and cryo-EM all converge on IPO9 as the SR-218 target, with orthogonal competition by inactive analogs (SR-363, SR-278) and an independent IPO9 binder (dbk-032A) strengthening specificity claims.

3. Explicit reporting of stochastic and design choices: UV crosslinking parameters (365 nm, 20 min), cryo-EM tilt angle (30°), symmetry assumptions (C2 applied post-symmetry expansion), and negative results (IPO9 does not reverse NCP-mediated inhibition) are all stated.

## Weaknesses: Load-bearing claims

**Claim 1: SR-218 inhibits cGAS-STING signaling by engaging IPO9, not by direct cGAS inhibition.**

The evidence is that SR-218 is inactive in a recombinant cGAS enzyme assay (Fig. 1h) and does not directly bind cGAS (Extended Data Fig. 4f), yet inhibits pathway activation in cells. This rules out direct catalytic inhibition but does not exclude off-target effects that secondarily suppress cGAS. The chemical proteomics screen (Fig. 2b) identifies IPO9 as a top hit, and rhodamine competition confirms SR-218 binds IPO9 in cells and in vitro. However, the proteomics filtering criteria are not fully specified: the text states "proteins were prioritized if they were selectively competed in the presence of SR-218, so that log2[Fold Change, SR-218+SR-432/SR-432] was less than −1," but does not report how many candidates passed this threshold, whether multiple peptides per protein were required before prioritization, or the false-discovery rate. The volcano plot (Fig. 2b) shows IPO9 as a clear outlier, but without the full candidate list and filtering statistics, alternative explanations—such as IPO9 being a high-abundance protein that happens to be competed—cannot be fully excluded. To resolve this: report the complete list of candidates passing the log2 < −1 threshold, the number of unique peptides per candidate, and the q-value or FDR for IPO9 relative to the distribution.

**Claim 2: IPO9 releases cGAS from H2A-H2B-mediated inhibition by directly displacing the histone dimer from cGAS.**

The biochemical evidence is that IPO9 rescues cGAMP production in the presence of free H2A-H2B (Fig. 3d) and disrupts cGAS:H2A-H2B binding in BLI (Fig. 3f, EC50 = 110 nM). The cryo-EM structure of cGAS:H2A-H2B (4.3 Å resolution) shows H2A-H2B bound at site B, blocking DNA binding, and structural comparison suggests IPO9's H18-19 loop could displace cGAS from the acidic patch. However, the BLI experiment shows a transient increase in signal immediately after IPO9 addition (Extended Data Fig. 5f, g), which the authors interpret as a "potential transient tripartite interaction" but do not quantify or characterize further. This is consistent with direct displacement but also consistent with IPO9 binding H2A-H2B while cGAS remains bound, followed by slow dissociation. The authors acknowledge three non-mutually exclusive mechanisms (direct displacement, indirect sequestration of H2A-H2B, or sequestration from DNA) but do not experimentally distinguish them. The cryo-EM resolution (4.3 Å) precludes sidechain modeling, so the proposed H18-19 loop–acidic patch interaction is inferred from lower-resolution density and prior IPO9:H2A-H2B crystal structures, not directly observed here. To resolve this: (1) quantify the kinetics of the transient BLI signal increase (association rate, amplitude, and decay) and compare to a control where IPO9 is added to cGAS alone; (2) perform a competition BLI experiment where IPO9 is pre-incubated with H2A-H2B before addition to cGAS:DNA, to test whether IPO9 sequesters H2A-H2B away from cGAS; (3) report the local resolution of the cryo-EM map at the H2A-H2B acidic patch and IPO9 H18-19 loop contact region to assess confidence in the proposed interaction.

**Claim 3: The cryo-EM structure demonstrates that free H2A-H2B dimers alone cannot prevent cGAS dimerization but block DNA binding sites.**

The structure shows a 2:2 cGAS:H2A-H2B stoichiometry with cGAS dimers assembled similarly to dsDNA-bound dimers, and H2A-H2B bound at site B (DNA-binding site), not site A. The authors state "there does not appear to be an interface between site A of cGAS and H2A-H2B, but in the context of the 2:2 stoichiometry, the histone dimers would sterically interfere with dsDNA binding at this site." This is a structural inference, not a direct measurement: steric interference is plausible but depends on the precise geometry of dsDNA binding, which is not modeled here. The authors also note that "cGAS has also been shown to dimerize in the absence of dsDNA, and thus we cannot definitively conclude that H2A-H2B binding induces dimerization." This candid statement undermines the claim that the structure reveals the mechanism of H2A-H2B-mediated inhibition, because the dimer assembly in the structure may be an artifact of the purification or crystallization conditions rather than the functional inhibitory state. To resolve this: perform size-exclusion chromatography or analytical ultracentrifugation on cGAS alone, cGAS + H2A-H2B, and cGAS + dsDNA to determine the oligomeric state in solution under assay conditions, and compare to the cryo-EM stoichiometry.

## Weaknesses: Sweep

1. **Statistical reporting gaps**: Fig. 1c, e, f report mean ± s.d. and ANOVA F-statistics but do not specify post-hoc tests or exact p-values for pairwise comparisons; Fig. 3d reports Tukey's test but does not state whether comparisons are one-tailed or two-tailed.

2. **Incomplete cell line authentication**: THP-1 cells are sourced from Invivogen but no passage number, mycoplasma testing, or STR profiling is reported; reproducibility across labs may be compromised if cell line drift occurs.

3. **Malachite green assay substrate concentrations**: Fig. 3d and Extended Data Fig. 5b use "concentrations corresponding to the approximate Km values of substrates" (50 µM ATP, 50 µM GTP) but Km values are not cited or measured here, making it unclear whether the assay is in the linear range or whether inhibition is substrate-dependent.

4. **Cryo-EM data processing ambiguity**: the text states "particles were classified through iterative rounds of 2D classification, ab-initio reconstruction and heterogeneous refinement" but does not specify the number of 2D classes, ab-initio models, or heterogeneous refinement classes, hindering reproduction of the workflow.

5. **BLI kinetic parameters not reported**: Fig. 3f reports EC50 for IPO9-induced dissociation but not kon, koff, or Kd, limiting mechanistic interpretation and comparison to other IPO9 interactions.

6. **Trex1−/− mouse experiment sample size**: Fig. 1g states "n=2 independent experiments, with at least n=4 mice per treatment group" but does not specify the exact n per group or whether data are pooled or reported separately by experiment.

7. **Photoactivatable probe synthesis and characterization**: SR-432 is described as a "diazirine alkyne" derivative but no synthetic scheme, NMR, or mass spectrometry data are provided; the probe's photochemical efficiency and labeling specificity are not quantified.

8. **Nucleosome core particle source and validation**: biotinylated mononucleosomes are purchased from Active Motif (31467) but no validation of histone composition, DNA length, or nucleosome positioning is reported.

## Questions

1. In the TMT proteomics experiment (Fig. 2b), how many total proteins were quantified, and how many passed the log2 < −1 competition threshold before IPO9 was prioritized?

2. For the BLI experiment in Fig. 3f, what is the kon and koff for IPO9-induced dissociation of the cGAS:H2A-H2B complex, and how does the EC50 (110 nM) compare to the Kd of IPO9:H2A-H2B binding reported in prior work?

3. In Extended Data Fig. 5f–g, can the authors quantify the amplitude and timescale of the transient BLI signal increase upon IPO9 addition, and provide a control where IPO9 is added to cGAS alone?

4. What is the local resolution of the cryo-EM map at the H2A-H2B acidic patch and the proposed IPO9 H18-19 loop contact region, and does it support sidechain-level modeling of the interaction?