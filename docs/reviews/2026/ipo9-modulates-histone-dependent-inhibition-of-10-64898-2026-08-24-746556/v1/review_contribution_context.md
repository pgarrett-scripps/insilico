# Contribution & Prior-Work Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This manuscript reports the discovery of IPO9 as a previously unknown regulator of cGAS-STING signaling, identified through phenotypic screening and chemical proteomics. The work establishes that IPO9 modulates cGAS activity by disrupting inhibitory interactions between cGAS and free H2A-H2B histone dimers—a distinct mechanism from nucleosome-mediated inhibition. The contribution is real and substantive: IPO9's role in cGAS regulation is genuinely novel, the structural and biochemical evidence is solid, and the work opens a new regulatory axis. However, the novelty is somewhat narrower than framed, and key mechanistic claims rest on inferences that warrant explicit scrutiny.

## Strengths

1. The authors correctly identify and validate IPO9 as a bona fide target of SR-218 through orthogonal methods (competitive labeling, genetic knockdown, recombinant protein assays) with clear SAR correlation, establishing genuine target engagement.

2. The cryo-EM structure of cGAS:H2A-H2B at 4.3 Å provides direct structural evidence that free histone dimers block DNA binding sites on cGAS while permitting dimerization, distinguishing this inhibitory mode from nucleosome-mediated sequestration.

3. The manuscript appropriately acknowledges mechanistic uncertainty, explicitly stating that "multiple mechanisms" may contribute to IPO9-mediated cGAS release and that RanGTP involvement cannot be excluded.

## Weaknesses: Load-Bearing Claims

**Claim 1: IPO9 is a "previously unknown regulator of cGAS-STING signaling."**

The evidence supporting this claim is IPO9's ability to reverse H2A-H2B-mediated inhibition of cGAS in vitro (Fig. 3d) and the loss-of-function phenotype in cells (Fig. 3b,c). However, the manuscript does not establish that IPO9 *naturally* regulates cGAS in cells under physiological conditions. The in vitro rescue occurs at 500 nM IPO9 with an EC50 of 110 nM for H2A-H2B displacement (Fig. 3f), but neither the cellular concentration of IPO9 nor the abundance of free H2A-H2B dimers in the nucleus is reported. The cell-based knockdown experiments show that loss of IPO9 impairs dsDNA-dependent STING phosphorylation, but this could reflect a general defect in histone homeostasis or nucleosome assembly rather than a specific cGAS-regulatory function. The authors do not demonstrate that endogenous IPO9 and free H2A-H2B interact in cells, nor do they show that this interaction is rate-limiting for cGAS activation under any physiological stimulus. The claim would be stronger if the authors reported: (i) cellular IPO9 and free H2A-H2B concentrations; (ii) co-immunoprecipitation or proximity labeling data showing IPO9-H2A-H2B interaction in cells; or (iii) a condition (infection, DNA damage, etc.) where IPO9 knockdown specifically impairs cGAS activation relative to other innate pathways.

**Claim 2: IPO9 disrupts cGAS:H2A-H2B interaction by direct displacement via its H18-19 loop.**

The evidence is the cryo-EM structure showing minimal steric overlap between IPO9 and cGAS except at the H18-19 loop (Fig. 4d), combined with BLI data showing IPO9-dependent loss of cGAS:H2A-H2B binding signal (Fig. 3f). However, the BLI experiment measures binding kinetics on immobilized cGAS, not free cGAS in solution. The authors observe "a brief concentration-dependent increase in signal immediately after sensors were dipped in IPO9" (Extended Data Fig. 5f,g), which they interpret as a transient tripartite complex but could equally represent non-specific sensor effects or kinetic artifacts. Critically, the authors cannot distinguish between three mechanisms: (i) direct displacement of H2A-H2B from cGAS by IPO9 binding the histone acidic patch; (ii) indirect sequestration of free H2A-H2B away from cGAS; or (iii) sequestration of H2A-H2B from DNA (which they show IPO9 does, Extended Data Fig. 5d,h-i). The cryo-EM structure is at 4.3 Å resolution with preferred orientation requiring 30° tilt, precluding confident sidechain modeling. The authors state "resolution limits our ability to draw definitive conclusions about the interaction at an amino acid level" (Results section), yet they propose a specific mechanism involving the H18-19 loop. To distinguish these mechanisms, the authors should report: (i) BLI with soluble (not immobilized) cGAS; (ii) mutation of the IPO9 H18-19 loop and assessment of its ability to disrupt cGAS:H2A-H2B in vitro and rescue cGAS activity in cells; or (iii) direct measurement of ternary complex formation by size-exclusion chromatography or analytical ultracentrifugation.

**Claim 3: Free H2A-H2B dimers inhibit cGAS with similar potency to nucleosomes.**

The evidence is the malachite green assay showing comparable cGAMP inhibition by H2A-H2B and NCP at the concentrations tested (Fig. 3d). However, the assay uses 100 nM cGAS with 50 nM H2A-H2B or NCP—a 2:1 molar ratio that may not reflect physiological stoichiometry. The authors do not report the Kd values for cGAS:H2A-H2B or cGAS:NCP binding, making it impossible to assess whether the similar inhibition reflects similar affinity or simply saturation at the tested concentrations. The cryo-EM structure reveals a 2:2 cGAS:H2A-H2B stoichiometry, but the functional significance of this ratio is unclear. The authors should report: (i) dose-response curves for H2A-H2B and NCP inhibition of cGAS activity across a wider concentration range; (ii) Kd values from BLI or surface plasmon resonance; or (iii) quantification of free H2A-H2B dimer abundance in the nucleus relative to nucleosomes.

## Weaknesses: Sweep

- The manuscript does not cite or discuss Cho et al. (2024, Nature 625:585–592) on MRE11-mediated release of cGAS from nucleosomes, which describes an alternative mechanism for cGAS liberation during tumorigenesis and should be positioned relative to the IPO9 axis.

- SR-218 shows poor metabolic stability (Extended Data Fig. 3a) and the authors acknowledge this precludes steady-state dosing, limiting the compound's utility as a tool and raising questions about whether the in vivo Trex1−/− experiment (Fig. 1g) achieved sufficient target engagement.

- The claim that IPO9 "moonlights" beyond nucleocytoplasmic transport (Discussion) is speculative; the authors provide no evidence that IPO9's cGAS-regulatory function is independent of its canonical RanGTP-dependent cargo release mechanism.

- The manuscript does not address whether SR-218 or IPO9 inhibition affects nucleosome assembly or chromatin structure, which could confound interpretation of the cGAS-specific effects.

- The in vivo pharmacodynamic marker (cGAMP in heart tissue) is indirect; the authors do not measure cGAS activity, STING phosphorylation, or downstream interferon responses in the Trex1−/− mice.

- The cryo-EM reconstruction uses a 30° tilt dataset to overcome preferred orientation, which may introduce anisotropic resolution and bias in the final model; the angular distribution and local resolution are not reported in the main text.

- The authors state that IPO9 "may actively remove histone dimers from the cGAS:H2A-H2B complex by displacing the acidic patch interaction with its H18-19 loop" (Results) but then note this "could only occur in the context of monomeric cGAS" (Extended Data Fig. 6c), leaving the functional relevance of the 2:2 dimer structure unresolved.

## Questions

- What are the cellular concentrations of IPO9 and free H2A-H2B dimers, and do they support the in vitro EC50 values observed?

- Does mutation of the IPO9 H18-19 loop abolish its ability to disrupt cGAS:H2A-H2B binding in vitro and rescue cGAS activity in cells?

- What is the Kd for cGAS:H2A-H2B interaction, and how does it compare to cGAS:NCP?