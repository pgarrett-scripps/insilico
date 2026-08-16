# Ethics & Compliance Reviewer

SCORE: 6/10

## Strengths

1. The use of TurboID proximity labeling is well-suited to the goal of capturing transient interactions that standard immunoprecipitation approaches would miss.
2. The study design includes a thoughtful time-resolved analysis of Smo-associated proteins during distinct phases of Hedgehog signaling activation (resting, SAG-stimulated, and cyclopamine-treated states).
3. The authors validated their key finding—that Git1 regulates ciliary Grk2 translocation—using both gain- and loss-of-function approaches, strengthening the causal claim.

## Weaknesses

**1. The claim that Git1 controls Grk2 translocation into the cilium is not convincingly supported by the data presented.**

The manuscript shows that Git1 knockout reduces Hh signaling (Fig. 6H) and that expressing cilium-targeted Grk2 (Grk2-V5-DArl13b) partially rescues this defect. However, the key mechanistic claim—that Git1 regulates Grk2 entry into the cilium—is not directly demonstrated. Figure 5G-I appears to show ciliary Grk2 staining in Git1-null versus wild-type cells, but the figure is not described in sufficient detail to assess quantification, statistical power, or whether the effect is specific to Grk2 versus overall ciliary transport. The manuscript never directly shows that Git1 loss reduces Grk2 localization at the ciliary base or within the cilium itself. Without directly testing whether Grk2 fails to enter the cilium in Git1-null cells, the core mechanistic claim is incomplete. If Grk2 still enters the cilium but Smo phosphorylation is reduced, the mechanism would instead be that Git1 regulates Grk2 kinase activity rather than its localization, which would represent a fundamentally different conclusion.

**2. The functional relevance of Git1 interaction with Smo is not adequately tested with the rescue experiment, as the ciliary-localized Grk2 construct (Grk2-V5-DArl13b) does not reach endogenous levels or spatial regulation.**

**2. The claim that "active" Smo recruits PKA-C to the cilium relies on a single small-molecule inhibitor (cyclopamine) and does not establish physiological relevance of PKA-C ciliary translocation, since PKA-C is not shown to be required for Smo phosphorylation in this system.** The authors suggest that even if Smo accumulates in the cilium without activation, PKA-C is not recruited, implying specificity. However, they do not test whether artificially tethering PKA to the cilium could bypass the need for Git1-mediated Grk2 entry, which would distinguish whether Git1's role is in Grk2 trafficking or in assembling a signaling complex at the cilium.

**2. The evidence for Git1 as a Smo interactor is indirect.** The pulldown shown in Figure 4B indicates increased Git1 association after SAG stimulation, but this is not confirmed by Co-IP (which they state failed). A key alternative — that Git1 interacts with Grk2, which itself associates with Smo only in the activated state — is not excluded. The authors do show Git1-Grk2 Co-IP (Fig. 5D), but Smo is not demonstrated in that complex. Without direct evidence that Smo and Git1 are in a proximity (<20 nm) rather than merely in the same ciliary compartment (the labeling radius of TurboID is reported as being on the order of 10-20 nm), the claim that Smo and Git1 directly interact is overstated. A domain-level mapping or an additional orthogonal method (e.g., in situ proximity ligation) would strengthen this.

**3. The manuscript does not fully characterize the signaling consequences of Git1 loss.** The authors show that Git1 knockdown reduces Gli1 expression, but do not examine whether this is a direct consequence of reduced Smo phosphorylation or an indirect effect through changes in ciliary composition/stability. Given that GIT1 is a scaffolding protein with many partners (e.g., Paxillin, βPIX), off-target effects on broader cell signaling are possible. The paper would be strengthened by a Git1 rescue experiment in the knockdown background and by quantifying Smo phosphorylation directly (e.g., phospho-specific antibody or phospho-Smo stoichiometry), rather than relying solely on Gli1 readout.

**4. The manuscript does not address whether Git1's previously characterized functions — such as its role in GPCR desensitization or centrosomal organization — contribute to the observed phenotype.** GIT1 is a multifunctional protein; the effects on Hh signaling could be indirect through general defects in ciliary trafficking or cell division rather than reflecting a specific function in Grk2-mediated Smo phosphorylation.

**5. The statistical analysis is minimal; key comparisons (e.g., Gli1 levels, ciliary Smo-P) are presented without error bars or replicate numbers in several figures.**

**6. Git1 has known roles in receptor endocytosis generally (Claing et al., 2000), yet the authors do not discuss whether the effect on Hh signaling might occur through altered Smo internalization rather than ciliary Grk2 recruitment.**

**7. The finding that cyclopamine treatment does not recruit PKA to the cilium (Fig. 3) is interesting, but the conclusion drawn — that Smo activation is required for PKA-C ciliary localization — assumes the effect is Smo-specific rather than a general Smo-independent effect of cyclopamine.**

**8. The rescue experiment with Grk2-Arl13b (Fig. 6G-H) increases Gli1 levels but does not restore them fully to wild-type levels. The partial rescue suggests that Git1 may have additional Smo-independent roles in Hh signaling that are not discussed.**

**9. The manuscript would benefit from a positive control showing that the Grk2-V5-DArl13b fusion retains kinase activity.**

## Questions

1. Does the Smo phosphorylation defect in Git1-null cells reflect only reduced Grk2 ciliary entry, or could Git1 loss also affect Grk2 catalytic activity or substrate accessibility within the cilium?
2. Is Grk2-V5-DArl13b expression in Git1-null cells sufficient to restore Smo phosphorylation at the endogenous level, or is full-length Grk2 re-expression also required?