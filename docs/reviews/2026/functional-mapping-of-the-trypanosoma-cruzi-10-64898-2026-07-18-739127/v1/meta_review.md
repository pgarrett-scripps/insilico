# Meta-Review

**Draft recommendation:** major

## Synthesis
The panel agrees this is the first activity-based chemoproteomic profiling of the T. cruzi serinome — a genuine, field-defining contribution verified by the Novelty reviewer (4/5, conf 5). The live-cell FP-ABPP workflow overcomes T. cruzi lysate agglutination (Methodology, Rigor reviewers), the in silico curation with AlphaFold catalytic-geometry validation is rigorous (Data Analysis reviewer), limma's empirical Bayes moderation is appropriate for n=3 (Data Analysis), and MS data (PXD080813) plus analysis code (Zenodo) are deposited (Reproducibility). The 35 enriched SHs with conserved/partially conserved catalytic triads (~63% of 56 curated candidates) include validated virulence factors (OPB, Tc80, CPB1, PLA1, rhomboid), delivering a prioritized, probe-accessible set for inhibitor discovery.

Two load-bearing issues split the panel and must be resolved before the central claims can stand:

1. **No competition ABPP to validate active-site engagement.** The Methodology reviewer (3/5, conf 4) calls this a 'critical design flaw' that 'undermines the central claim of activity-based profiling,' noting probe specificity ranges only 10–43% (Fig. 3 legend), meaning 57–90% of enriched proteins are non-SHs. The Advocate argues AlphaFold-validated catalytic geometry provides orthogonal evidence of active-site competence and the Leishmania precedent (ref 17) was accepted without per-probe competition. The Skeptic counters that structural prediction ≠ experimental on-target engagement in live cells, and each system requires its own validation. The Rigor reviewer (4/5, conf 4) does not flag this as fatal but notes the rhomboid protease's activity is 'not experimentally validated beyond probe labelling.'

2. **Uncontrolled false discovery rate across 7 probes.** The Data Analysis reviewer (4/5, conf 4) states the 37-protein list derives from 'uncorrected p<0.05 thresholds across 7 probes and ~56 candidate SHs, yielding an uncontrolled family-wise error rate' and the authors 'present the resulting list as a "prioritized set" and "reference resource" without estimating the false discovery proportion.' The Advocate notes BH-adjusted values exist in supplements and a sensitivity analysis can be added from the deposited R scripts. The Skeptic replies this dodges the direct question: 'What is the estimated false discovery rate among the 37 reported SHs?'

Additional issues requiring resolution (all fixable in revision):
- Experimental strain unspecified (Methodology: 63% coverage claim 'invalid comparison' if strains differ)
- Cross-strain GO/PPI analysis (Dm28c→CL Brener) with unquantified mapping bias (Rigor, Novelty)
- Missing dedicated Methods section with LC-MS/MS parameters, click chemistry protocol, lysis buffer, LFQ pipeline (Reproducibility: 3/5, conf 4)
- Clarity defects: abstract denominator ambiguity (35/37 vs 35/56), Table 2 lists two non-enriched proteins as 'enriched', Figure 4 vs Supp Fig S3 cross-reference error, probe structures unannotated in Fig 2 (Clarity: 3/5, conf 4)
- Reference 69 carries future publication date (Literature: 4/5, conf 4)

The confidence-weighted average (3.79) and verdict distribution (1 accept, 4 minor, 3 major) support Major Revision. The Skeptic's 'reject' stance requires new wet-lab experiments (competition ABPP); the Advocate and most reviewers treat this as a limitation to acknowledge with a concrete follow-up plan, plus computational FDR analysis on existing data. Given In Silico's standard — 'A modest claim that is fully supported is better work than an important claim that is not' — the manuscript must either (a) provide competition ABPP for a representative subset of high-priority hits, or (b) explicitly reframe the 37-protein list as 'probe-enriched candidates with structural support for catalytic competence' rather than 'activity-validated targets,' and supply the FDR sensitivity analysis the Data Analysis reviewer requested. The other issues are textual/presentational or supplementary-data gaps.

## Decisive Factors
1. Methodology reviewer (conf 4) explicitly states competition ABPP omission 'undermines the central claim of activity-based profiling' — this is the strongest single critique and comes from a domain specialist.
2. Data Analysis reviewer (conf 4) states the 37-protein list has 'uncontrolled family-wise error rate' and 'a reader cannot distinguish likely true positives from false positives' — directly contradicting the 'prioritized set' and 'reference resource' framing.
3. No reviewer recommended rejection; three gave 'major revision' and the confidence-weighted mean (3.79) sits squarely in major-revision territory.
4. The Advocate's point that FDR sensitivity analysis can be computed from deposited R scripts (Zenodo) means one load-bearing issue is resolvable without new experiments.
5. Competition ABPP for a subset (e.g., OPB, Tc80, CPB1, PLA1, rhomboid) is a concrete, bounded experiment that would directly address the Methodology reviewer's fatal flaw; requiring it as a revision condition is proportionate for a 'first-in-organism' resource paper.
6. Strain identity, orthologue table, Methods section, and clarity fixes are all textual/supplementary and non-negotiable for reproducibility.
7. In Silico's standard ('modest claim fully supported > important claim not supported') means the paper must either substantiate the activity-based claim experimentally or modulate the claim to match the evidence (probe enrichment + structural validation). The revision must choose one path explicitly.
8. The Ethics (5/5) and Novelty (4/5, conf 5) reviews are clean — the contribution is real and the gap is genuine; the revision must secure the evidence chain without discarding the resource value.

Therefore: Major Revision with mandatory requirements (competition ABPP subset OR explicit claim modulation + FDR sensitivity analysis; strain identity; orthologue table; complete Methods; all clarity fixes). The recommendation diverges from the confidence-weighted average only in being explicit about the competition ABPP / claim-modulation fork, which the numerical signal implies but does not articulate.

If the authors cannot provide competition ABPP data in revision, they must rewrite the abstract, title, and conclusions to describe a 'chemoproteomic survey of probe-enriched serine hydrolase candidates with in silico catalytic validation' rather than an 'activity-based chemoproteomic map' — and the Data Analysis reviewer's FDR analysis must be included to let readers gauge list reliability. This fork is the decisive factor.