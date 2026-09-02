# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This is a well-executed chemical biology study that identifies IPO9 as a regulator of cGAS-STING signaling through a phenotypic screening campaign and validates the mechanism with biochemistry, structural biology, and cell-based assays. The core claims—that SR-218 inhibits cGAS-STING signaling by engaging IPO9, and that IPO9 disrupts H2A-H2B-mediated inhibition of cGAS—are supported by appropriate evidence. The cryo-EM structure of cGAS:H2A-H2B provides structural context for the mechanism. The work is technically sound and makes a genuine contribution to understanding cGAS regulation. One significant limitation is that the mechanism of IPO9-mediated release of cGAS from H2A-H2B remains incompletely resolved, with multiple non-exclusive mechanisms proposed but not definitively distinguished.

## Strengths

1. The target identification pipeline is rigorous: photoactivatable probe design, quantitative proteomics with competition, and orthogonal validation across recombinant protein, overexpressed protein, and endogenous knockdown systems all converge on IPO9 with strong SAR correlation.

2. The biochemical evidence cleanly separates H2A-H2B dimer inhibition (reversed by IPO9) from nucleosome core particle inhibition (not reversed by IPO9), establishing a functionally distinct regulatory axis.

3. The cryo-EM structure of cGAS:H2A-H2B at 4.3 Å resolution, combined with structural comparison to IPO9:H2A-H2B and cGAS:NCP complexes, provides a coherent model for how H2A-H2B blocks DNA binding sites while allowing cGAS dimerization.

## Load-bearing Claim 1: SR-218 inhibits cGAS-STING signaling by engaging IPO9

**Evidence:** Photoactivatable probe SR-432 labels IPO9 in cells and recombinant protein; labeling is competed by SR-218 but not by inactive analogs SR-363 and SR-278 (Fig. 2c–h). SAR for target engagement correlates with phenotypic activity across a series of analogs (Fig. 2g–h). IPO9 knockdown phenocopies SR-218 inhibition of STING phosphorylation (Fig. 3a–c).

**Alternative explanation:** SR-218 could inhibit cGAS-STING signaling through a different mechanism, with IPO9 engagement being a secondary or off-target effect. The correlation between SAR for IPO9 binding and pathway inhibition is strong, but does not prove causation—SR-218 could bind both IPO9 and another target, with only one driving the phenotype.

**What would settle it:** The critical test is whether IPO9 knockdown fully rescues the phenotype of SR-218 treatment in a dose-response experiment. Figure 3b–c shows that IPO9 knockdown reduces phospho-STING to similar levels as SR-218 treatment, but does not directly show whether SR-218 retains activity in IPO9-depleted cells. A rescue experiment—treating IPO9-knockdown cells with SR-218 and asking whether the compound still inhibits STING phosphorylation—would definitively establish whether IPO9 is the relevant target. The authors should report whether SR-218 remains active in IPO9 sh1 and sh2 knockdown cells, or whether knockdown occludes further inhibition by the compound.

---

## Load-bearing Claim 2: IPO9 releases cGAS from H2A-H2B-mediated inhibition by directly disrupting the cGAS:H2A-H2B interaction

**Evidence:** In malachite green assays, free H2A-H2B inhibits cGAS activity; IPO9 addition rescues cGAMP production (Fig. 3d). IPO9 does not rescue nucleosome core particle-mediated inhibition (Fig. 3d). Biolayer interferometry shows IPO9 causes concentration-dependent loss of signal in a cGAS:H2A-H2B complex (Fig. 3f, EC50 = 110 nM). Structural comparison of cGAS:H2A-H2B with IPO9:H2A-H2B suggests the H18-19 loop of IPO9 could displace cGAS from the histone acidic patch (Fig. 4d).

**Alternative explanation:** IPO9 could release cGAS from H2A-H2B inhibition indirectly, by sequestering free H2A-H2B away from cGAS (preventing re-binding) rather than actively displacing bound H2A-H2B. The BLI experiment (Fig. 3e–f) measures loss of signal when IPO9 is added to a pre-formed cGAS:H2A-H2B complex, which is consistent with displacement, but the authors acknowledge (Discussion) that "IPO9 may selectively target monomeric cGAS or disrupt dimeric cGAS" and that "we cannot exclude the possibility that multiple mechanisms contribute to the overall net impact of IPO9 on cGAS activation in cells." The transient increase in BLI signal immediately after IPO9 addition (Extended Data Fig. 5f–g) is interpreted as a tripartite interaction, but could also reflect non-specific binding or instrumental artifact.

**What would settle it:** A direct binding assay measuring the kinetics of H2A-H2B dissociation from cGAS in the presence and absence of IPO9 would distinguish active displacement from sequestration. Alternatively, a competition assay in which IPO9 is added to pre-formed cGAS:H2A-H2B and then H2A-H2B is titrated back in would show whether IPO9 prevents re-binding (sequestration) or actively removes bound H2A-H2B (displacement). The authors should report the dissociation rate constant (koff) for H2A-H2B from cGAS ± IPO9, measured by surface plasmon resonance or stopped-flow kinetics, to establish whether IPO9 accelerates dissociation.

---

## Load-bearing Claim 3: Free H2A-H2B dimers inhibit cGAS activity by blocking DNA binding sites, independent of nucleosome context

**Evidence:** Cryo-EM structure of cGAS:H2A-H2B at 2:2 stoichiometry shows H2A-H2B bound at DNA binding site B of cGAS, with steric interference at site A (Fig. 4b). Comparison to dsDNA-bound cGAS dimers shows nearly identical cGAS dimer assembly. Malachite green assay shows H2A-H2B inhibits cGAS activity to similar levels as full nucleosomes (Fig. 3d).

**Limitation (not a hard flaw, but a scope issue):** The cryo-EM structure is at 4.3 Å resolution with preferred orientation requiring a 30° tilt. The authors state "resolution limits our ability to draw definitive conclusions about the interaction at an amino acid level" (Results). The model was built by docking coordinates from PDB 7C0M (cGAS) and 7PII (H2A-H2B) into the map, which is standard practice but means the atomic details of the cGAS:H2A-H2B interface are not independently resolved at this resolution. The claim that H2A-H2B "blocks essential DNA binding sites" is supported by the overall domain positioning, but the specific residue contacts that mediate inhibition cannot be verified from the cryo-EM map alone. The biochemical data (malachite green assay showing inhibition) is independent and strong, so the claim is well-supported, but the structural detail is lower confidence.

**What would strengthen it:** A higher-resolution structure (3.5 Å or better) or complementary biochemical data (e.g., alanine scanning of acidic patch residues on H2A-H2B, or DNA-binding kinetics with H2A-H2B present) would provide atomic-level validation. The authors should report Kd values for cGAS:DNA binding ± H2A-H2B to quantify the inhibitory effect and confirm it is due to DNA site occlusion rather than allosteric inhibition.

---

## Sweep

1. **Cellular mechanism not fully resolved:** The authors show IPO9 knockdown phenocopies SR-218 in cells (Fig. 3b–c), but do not demonstrate that SR-218 requires IPO9 for its activity in cells—a rescue experiment with IPO9 overexpression in the presence of SR-218 would confirm IPO9 is the relevant target in the cellular context.

2. **RanGTP role unexplored:** The Discussion mentions that "RanGTP may influence the ability of IPO9 to disrupt the cGAS:H2A-H2B interaction" and notes IPO9's established role in cargo release, but no experiments test whether RanGTP modulates IPO9-mediated cGAS release, leaving a potential regulatory axis unexamined.

3. **Stoichiometry ambiguity:** The cryo-EM data show a 2:2 cGAS:H2A-H2B complex as the major class, but a 2:1 population was also observed during 3D classification (Extended Data Fig. 6a); the functional relevance of these different stoichiometries and their relative prevalence in cells is not addressed.

4. **In vivo pharmacodynamic is limited:** The Trex1−/− mouse experiment (Fig. 1g) measures cGAMP in heart tissue after four intraperitoneal injections of SR-218 (30 mg/kg), but does not report dose-response, tissue distribution, or whether the reduction in cGAMP correlates with rescue of disease phenotype (survival, inflammation markers).

5. **Metabolic stability caveat:** The authors note that the 5-aminoisoxazole ring system's poor metabolic stability "precluded identification of an analog that would enable steady-state drug levels necessary for constant target coverage" (Results), limiting the therapeutic potential of this series and raising questions about whether the in vivo effect is robust.

6. **IPO9 specificity within importin-β family:** While SR-432 does not label IPO5 or IPO11 (Extended Data Fig. 4d–e), the selectivity mechanism is not explained; if other importins share similar binding pockets, off-target effects on nucleocytoplasmic transport could confound the cellular phenotype.

7. **cGAS dimerization mechanism with H2A-H2B unclear:** The authors state "the mechanism of cGAS dimerization when complexed with H2A-H2B is unclear" and note that "H2A-H2B binding may simply fail to disrupt pre-existing apo-cGAS dimers" (Results), leaving open whether H2A-H2B actively promotes or merely permits cGAS dimerization.

8. **Extrachromosomal H2A-H2B context in vivo not tested:** The Discussion proposes a role for "extrachromosomal H2A-H2B as regulators of cGAS-STING pathway activation, independent of a chromatin context," but no experiments directly test whether free H2A-H2B dimers regulate cGAS in cells or tissues, or under what conditions they accumulate.

---

## Questions

- **Figure 3f:** Does IPO9 retain the ability to disrupt cGAS:H2A-H2B binding in the presence of RanGTP, and if so, does RanGTP modulate the EC50?

- **Figure 3d:** What are the Kd values for cGAS:H2A-H2B and cGAS:NCP binding, and do they differ in a way that explains why IPO9 rescues one but not the other?

- **Extended Data Fig. 6a:** What is the relative abundance of the 2:2 vs. 2:1 cGAS:H2A-H2B populations, and do they have different functional properties in the malachite green assay?

- **Figure 1g:** Is the reduction in cardiac cGAMP dose-dependent, and does it correlate with improved survival or reduced inflammatory markers in the Trex1−/− mice?