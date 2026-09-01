# Contribution & Prior-Work Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a solid, well-executed manufacturing and process-development manuscript that documents the translation of a rationally designed HIV vaccine candidate into clinical-grade material. The work is competent and thorough, with genuine practical value for the field, but the contribution is fundamentally incremental: it applies established bioprocess platforms and purification strategies to a new immunogen, with no methodological innovations or surprising findings that would elevate it beyond competent execution. The manuscript is appropriately scoped for a specialized bioprocess venue but sits in the middle range for a general audience—useful documentation of a necessary step, not a conceptual advance.

## Strengths

1. Comprehensive end-to-end documentation from cell line development through cGMP manufacturing, with transparent reporting of intermediate hold-time stability, robustness studies, and viral clearance data that will be valuable for practitioners scaling similar glycoproteins.

2. Rigorous viral clearance demonstration (≥18.14 log reduction for XMuLV, ≥11.70 for MMV) with orthogonal unit operations and quantified model virus studies, exceeding industry benchmarks and providing confidence in safety margins.

3. Detailed characterization of site-specific glycosylation using complementary mass spectrometry methods (DeGlyPHER and LC-MS glycoproteomics) with explicit reporting of occupancy variation between analytical approaches, supporting reproducibility claims.

## Weaknesses: Load-Bearing Claims

**1. Novelty of the manufacturing platform itself.** The manuscript claims to establish "a scalable, reproducible manufacturing paradigm for structurally complex HIV-1 envelope immunogens" (Abstract, Conclusions). However, the core platform is not new: the authors explicitly state (Section 3.3, first paragraph) that "The downstream purification process for N332-GT5 gp140 (Figure 3) was developed based on the process established for BG505 SOSIP.664 (Dey et al., 2018)." The upstream process uses standard CHO cell culture with Leap-In transposon integration (a commercial technology from ATUM), Ambr®250 optimization (routine in bioprocess development), and scale-up to single-use bioreactors (industry standard). The purification employs 2G12 affinity capture, Protein A chromatography, mixed-mode polishing (Capto adhere), and viral filtration—all established unit operations. The manuscript does not claim to have invented any of these; rather, it demonstrates their application to N332-GT5. This is competent execution of known methods, not a new platform. The distinction matters: a "paradigm" would imply a novel strategy or principle; what is demonstrated is successful application of existing strategies to a new molecule. The evidence does not support the stronger claim.

**2. Claim that this work "advances the field toward rational vaccine design based on germline-targeting principles" (Abstract).** The germline-targeting design of N332-GT5 itself is not the contribution of this manuscript—that work is attributed to Steichen et al. (2019, 2024) and is documented in the preclinical immunogenicity studies (Steichen et al., 2024, cited as demonstrating priming of BG18-class precursor B cells in macaques). This manuscript's role is to manufacture the designed immunogen for clinical use. The advance in germline-targeting vaccine design was made by the immunogen design work, not by the manufacturing work. The manufacturing contribution is enabling that design to reach the clinic, which is valuable but distinct from advancing the design principle itself. Attributing the design advance to the manufacturing work conflates two separate contributions and overstates what this manuscript establishes.

**3. Claim of "genetic stability through 60 population doublings" (Abstract).** Section 3.1.2 states that "Sixty population doubling (PD) long serial passage cultures were maintained in 24 deep well plates" and that "Productivity, transgene copy numbers, and N332 and furin mRNA identities were used as stability indicators." However, the manuscript does not report the actual results of these stability studies—no data are shown for transgene copy number, mRNA sequence integrity, or productivity across the 60 PD. Figure 1 labels this as part of the workflow but provides no quantitative evidence. Section 2.3.8 describes the protocol but not the outcome. The abstract claims stability "through 60 population doublings" as a key result, but the evidence for this claim is not presented in the results section. This is a gap between claim and evidence: the study was performed, but the data supporting the conclusion are absent from the manuscript.

## Weaknesses: Sweep

- The manuscript states that preparative SEC was removed from the process due to "supply constraints" (Section 3.3.2) and that a small-scale study showed comparable results without it, but does not report whether this change was validated at cGMP scale or whether the final cGMP batch was manufactured with or without SEC—the text is ambiguous on this critical point.

- Reference [3] (Bale et al., 2025, "Accelerated cGMP production of near-native HIV-1 Env trimers following electroporation transfection") is cited as a parallel cGMP production run but was not retrievable in preprint searches, making independent verification of the claimed comparison impossible.

- The manuscript does not compare the final N332-GT5 product quality metrics (% trimer, HCP, DNA, endotoxin) to the BG505 SOSIP.664 cGMP batch (Dey et al., 2018) or other published Env trimer cGMP runs, leaving unclear whether the achieved purity and safety margins are state-of-the-art or routine for this class of molecule.

- Intermediate hold-time stability (Section 3.3.3, Figure 15) is based on a single pilot-scale demonstration run; robustness of these hold times across multiple manufacturing batches or cell banks is not demonstrated.

- The glycosylation analysis (Figures 17–18) shows discordance between the two MS methods at several sites (e.g., N185e, N611, N625 show 50–90% occupancy by DeGlyPHER but appear unoccupied in LC-MS), yet the manuscript does not resolve which method is more reliable or whether this variation affects product potency.

- Negative-stain EM (Section 3.6.2) confirms native-like trimer morphology but does not quantify the percentage of particles in the final drug substance that are trimeric versus aggregated or misfolded, only that "no other oligomeric states were observed"—a qualitative rather than quantitative claim.

- The manuscript does not discuss whether the >99% trimer purity achieved is sufficient for the immunogenicity goals of HVTN144 or whether higher purity would be expected to improve clinical outcomes.

## Questions

- Section 3.1.2 reports "Productivity, transgene copy numbers, and N332 and furin mRNA identities were used as stability indicators" for the 60 PD study—please provide the actual data (copy number, mRNA sequence confirmation, and productivity values) for PD0, PD60+Gln, and PD60-Gln to support the stability claim in the abstract.

- Was the final cGMP batch manufactured with or without the preparative SEC step, and if without, was this decision validated in a full-scale robustness study or only in the small-scale comparison shown in Table 10?

- For the glycosylation sites where DeGlyPHER and LC-MS methods disagree (N185e, N611, N625), which method is considered the reference standard, and does the discordance affect the relative potency assay or other quality attributes?