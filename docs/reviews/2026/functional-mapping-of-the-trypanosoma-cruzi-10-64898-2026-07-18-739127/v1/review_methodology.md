# Methodology Reviewer

## Summary
The study presents a valuable first ABPP dataset for T. cruzi serine hydrolases but has three critical design flaws: (1) absence of competition ABPP to verify active-site labelling, (2) unspecified experimental strain preventing valid comparison with Dm28c in silico predictions, and (3) cross-strain GO enrichment using CL Brener background for Dm28c data. The probe panel characterization is incomplete without probe structure annotations and permeability validation. These issues require major revision to support the stated conclusions.

## Strengths
- Comprehensive in silico curation of the T. cruzi serinome with AlphaFold structural validation of catalytic geometry.
- Whole-cell ABPP approach successfully overcomes lysate agglutination issues inherent to T. cruzi.
- Integration of multiple genome assemblies captures gene family expansions missed by single assemblies.

## Weaknesses
- No competition ABPP experiment (e.g., pre-treatment with broad-spectrum FP inhibitor) was performed to demonstrate that probe enrichment reflects active-site labelling rather than non-specific binding; with probe specificity of only 10–43%, this omission undermines the central claim of activity-based profiling.
- The experimental T. cruzi strain used for ABPP is never stated, while in silico predictions used the Dm28c 2018 genome; if strains differ, the reported 63% capture rate (35/56 predicted SHs) is an invalid comparison, and even if identical, the 21 missing SHs are explained only by unsupported speculation.
- GO enrichment and PPI analyses used the CL Brener proteome as background because it is the only T. cruzi assembly in STRING, but the experimental data derive from Dm28c; extensive strain-specific gene family expansions (e.g., 17 copies of lipase C4B63_104g97) likely do not map 1:1 to CL Brener, biasing enrichment statistics and the conclusion that lipid metabolism is the dominant theme.
- Cell permeability of the FP-alkyne probes was assumed from Leishmania studies but not validated in T. cruzi, yet whole-cell labelling is the key enabling step.
- Lysate-based labelling failure is described without showing any data (no figure, no quantification), preventing assessment of whether whole-cell labelling was truly necessary or if lysis conditions were suboptimal.
- Figure 2 does not annotate which probe number (1–7) corresponds to which chemical structure, making it impossible to interpret probe-specific enrichment patterns in Figure 3a.
- Statistical thresholds (p < 0.05 unadjusted, log2FC > 1) were applied without multiple testing correction across seven probes and ~37 proteins; the authors acknowledge this but do not report how many proteins survive adjusted thresholds.
- Subcellular localization inferences rely on TrypTagDB data from T. brucei orthologues, not T. cruzi, and this cross-species extrapolation is not validated.
- Copy number variation in expanded families (e.g., 17 copies of C4B63_104g97) means LFQ-MS quantification likely represents summed abundance of multiple gene products, complicating interpretation of individual enzyme activity.

## Questions
- What T. cruzi strain was used for the ABPP experiments, and is it the same as the Dm28c strain used for in silico prediction?
- Can the authors provide competition ABPP data (e.g., pre-treatment with FP-biotin or PMSF) to confirm active-site dependent labelling for a subset of enriched proteins?
- Which specific probe structure corresponds to "probe 7" in Figure 3a, and what are the structural features distinguishing the seven probes tested?
- How many of the 37 enriched proteins pass a Benjamini–Hochberg adjusted p-value < 0.05 threshold across the probe panel?
- What are the non-SH proteins enriched by the probes (57–90% of enriched proteins), and do they represent known FP off-targets or non-specific binders?