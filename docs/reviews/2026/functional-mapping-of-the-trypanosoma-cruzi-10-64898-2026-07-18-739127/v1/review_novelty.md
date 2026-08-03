# Novelty & Contribution Reviewer

## Summary
This manuscript reports the first activity-based chemoproteomic profiling of the Trypanosoma cruzi serinome, identifying 37 active serine hydrolases in epimastigotes via live-cell fluorophosphonate-ABPP coupled with genome-informed curation. The novelty claim — that T. cruzi SHs have not previously been profiled directly by ABPP — is verified against the literature and preprints; the closest prior work applies the same probe panel to Leishmania (Isern et al., 2025). The contribution is substantial for Chagas disease research, delivering a prioritized, probe-accessible set of catalytically competent SHs with functional annotations linking them to lipid metabolism and virulence.

## Strengths
- The 'first-in-organism' ABPP claim is accurate and survives a dedicated literature/preprint search; the work fills a genuine gap in T. cruzi chemical biology.
- Integration of live-cell labelling (circumventing lysate agglutination), multi-assembly genome curation, AlphaFold catalytic-site validation, and orthogonal GO/PPI analysis yields a robust, multi-layered resource.
- The dataset explicitly prioritizes 35 enzymes with conserved catalytic geometry (~63% of curated candidates), including known virulence factors (OPB, Tc80, CPB1, PLA1) and previously uncharacterized hydrolases, enabling immediate downstream inhibitor discovery.

## Weaknesses
- The manuscript frames the 63% capture rate as 'substantial coverage' without clarifying whether the missing 37% reflects stage-specific expression (epimastigote vs. amastigote/trypomastigote), zymogen latency, or probe inaccessibility — a distinction that directly affects target prioritization for the clinically relevant intracellular stages. The Discussion acknowledges this but does not propose a concrete strategy to resolve it, leaving the most therapeutically relevant question unaddressed.
- Probe selectivity is assessed only by the number of SHs enriched per probe; no competitive ABPP or dose-response data are shown to confirm on-target engagement or to differentiate probe-specific vs. pan-FP reactivity, which weakens the chemical-biology utility of the probe panel for future structure-guided ligand discovery.
- The GO/PPI analyses map Dm28c hits to the CL Brener reference proteome in STRING; the manuscript does not quantify how many enriched proteins lack CL Brener orthologues or how mapping ambiguity might bias the lipid-metabolism enrichment conclusion.

## Questions
- Can the authors provide a table or supplementary list explicitly mapping each of the 37 enriched Dm28c proteins to its CL Brener orthologue (or noting absence), so readers can assess the STRING mapping fidelity?
- Are there plans or existing data for competitive ABPP (e.g., FP-alkyne vs. broad-spectrum FP-biotin competition) to validate on-target labelling for the highest-priority hits (OPB, Tc80, CPB1, PLA1, rhomboid)?
- Will the authors deposit the AlphaFold-predicted structures with catalytic-distance measurements (pLDDT, interatomic distances) for all 56 curated candidates in a public repository to enable community re-use?