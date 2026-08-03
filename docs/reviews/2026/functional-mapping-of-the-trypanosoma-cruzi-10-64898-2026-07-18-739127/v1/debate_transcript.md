# Debate Transcript

## Advocate — round 1

This manuscript delivers the first activity-based chemoproteomic map of the T. cruzi serinome — a genuine, field-defining contribution that the Novelty reviewer confirms survives literature/preprint search. The core workflow (live-cell FP-ABPP + LFQ-MS + AlphaFold catalytic validation) is sound: the Methodology reviewer calls the in silico curation 'comprehensive' with 'AlphaFold structural validation of catalytic geometry'; the Data Analysis reviewer endorses the 'appropriate use of limma's empirical Bayes moderation for small-n (n=3) proteomics data' and 'rigorous in silico catalytic triad validation'; the Rigor reviewer agrees the 'whole-cell ABPP strategy effectively overcomes lysate agglutination issues and captures active enzymes in their native state.' The 35 enriched SHs with conserved/partially conserved catalytic triads (~63% of 56 curated candidates) include validated virulence factors (OPB, Tc80, CPB1, PLA1) and a catalytically supported rhomboid — a prioritized, probe-accessible set for inhibitor discovery as the WHO NTD roadmap demands.

Most criticisms are fixable in revision, not fatal: (1) Abstract denominator ambiguity (35/37 vs 35/56) and Table 2's two non-enriched entries — clarify text and move footnoted proteins to a separate table. (2) Figure 4 vs Supp Fig S3 cross-reference error — correct citation. (3) Missing Methods section — consolidate scattered parameters (probe concentrations, lysis buffer, LC-MS/MS settings) into a dedicated section. (4) Uncorrected p-values — add BH sensitivity analysis to contextualize FDR (authors already computed adjusted values). (5) Competition ABPP absence — acknowledge as limitation and propose for follow-up; the 10–43% probe specificity still enriches known active SHs. (6) Strain identity — specify Dm28c used for ABPP (in silico used Dm28c 2018). (7) CL Brener mapping bias — provide Dm28c→CL Brener orthologue table. (8) Reproducibility gaps — deposit full LC-MS/MS parameters, click chemistry protocol, and computational environment. (9) Ref 69 date — correct to preprint DOI.

Concede: the 63% framing needs nuance (stage-specificity vs technical limits), and lysate failure lacks quantitative comparison. But these don't invalidate the resource; they guide its interpretation. The manuscript meets the bar for a major chemoproteomic resource paper with revisions.

**Key points:**
- First-in-organism ABPP of T. cruzi serinome verified by Novelty reviewer
- Live-cell FP-ABPP overcomes T. cruzi lysate agglutination (Methodology, Rigor reviewers)
- 35 enriched SHs with conserved catalytic geometry (~63% of curated candidates) including known virulence factors
- Rigorous in silico curation with AlphaFold structural validation (Data Analysis reviewer)
- Appropriate limma statistics for n=3 with transparent FDR trade-off (Data Analysis reviewer)
- MS data (PXD080813) and code (Zenodo) deposited (Reproducibility reviewer)
- All major weaknesses are textual/presentational or addressable by supplementary analyses in revision
- No ethics concerns (Ethics reviewer)

## Skeptic — round 1

The advocate concedes presentational fixes but misses two load-bearing flaws that invalidate the paper's core claim of an 'activity-based chemoproteomic map' and 'prioritized set of probe-accessible, catalytically competent targets'.

1. **No competition ABPP — FATAL**. The Methodology reviewer states: 'No competition ABPP experiment… was performed to demonstrate that probe enrichment reflects active-site labelling rather than non-specific binding; with probe specificity of only 10–43%, this omission undermines the central claim of activity-based profiling.' The manuscript itself reports probe specificity as low as 10% (Fig. 3 legend: 'Probe specificity… ranged from 10% (probe 1) to 43% (probe 7)'). Without competition, the 37-protein list cannot be distinguished from non-specific binders — the entire 'activity-based' premise collapses. This cannot be fixed by revision; it requires new experiments.

2. **Uncontrolled false discovery rate — FATAL**. The Data Analysis reviewer notes the 37 SHs derive from 'uncorrected p<0.05 thresholds across 7 probes and ~56 candidate SHs, yielding an uncontrolled family-wise error rate' and the authors 'present the resulting list as a

**Key points:**
- No competition ABPP validates active-site labelling (probe specificity 10-43%)
- Uncontrolled FDR across 7 probes inflates false discoveries in 37-protein list
- Experimental strain unspecified — 63% coverage claim potentially invalid
- Cross-strain GO analysis (Dm28c→CL Brener) with unquantified bias
- Missing wet-lab protocols prevent reproducibility

## Advocate — round 2

The skeptic's two 'FATAL' claims overstate the case for a first-in-organism chemoproteomic resource paper. (1) Competition ABPP: The manuscript reports 35/37 enriched proteins have conserved/partially conserved catalytic triads validated by AlphaFold geometry (distance <5Å, pLDDT≥80) — orthogonal structural evidence of active-site competence that the Data Analysis reviewer calls 'rigorous in silico catalytic triad validation.' FP-alkyne probes are a well-established SH chemotype; the 10–43% probe specificity reflects the proportion of *all* enriched proteins that are SHs, not the false-positive rate *among* SHs. The Leishmania FP-ABPP precedent (ref 17, same probe panel) was accepted without competition ABPP for every probe. This is a limitation to acknowledge, not a fatal flaw requiring new experiments for a resource paper. (2) Uncontrolled FDR: The authors transparently report using uncorrected p<0.05 'to avoid discarding genuine low-abundance hydrolases' and provide BH-adjusted values in supplements. The Data Analysis reviewer calls this 'defensible' and 'transparent.' A sensitivity analysis (how many survive BH correction) can be added in revision — the R scripts are on Zenodo. The 63% coverage (35/56 curated candidates) is a *lower bound* on active SHs; the missing 37% may reflect stage-specificity (epimastigote vs amastigote) as the Discussion notes, consistent with the authors' Leishmania work (ref 17). Strain identity: the in silico work uses Dm28c 2018; the ABPP almost certainly used the same lab strain (Dm28c epimastigotes) — a one-sentence clarification in Methods fixes this. Cross-strain GO bias: provide the Dm28c→CL Brener orthologue table (requested by Novelty reviewer) in revision. Reproducibility gaps: deposit LC-MS/MS parameters, click chemistry protocol, lysis buffer — the data and code are already public (PXD080813, Zenodo). These are all textual/presentational fixes or supplementary analyses, not new wet-lab experiments. The core contribution — first activity-based map of T. cruzi serinome, 35 catalytically validated SHs including OPB, Tc80, CPB1, PLA1, rhomboid — stands. Accept with revisions.

**Key points:**
- 35/37 enriched proteins have AlphaFold-validated catalytic geometry — orthogonal evidence of active-site competence
- FP-alkyne probes are established SH chemotype; Leishmania precedent (ref 17) accepted without per-probe competition ABPP
- Authors transparent about FDR trade-off; BH-adjusted values in supplements; sensitivity analysis can be added in revision
- Strain identity, orthologue mapping, missing protocols are all fixable by textual clarification or supplementary data deposition
- First-in-organism ABPP of T. cruzi serinome verified by Novelty reviewer; resource value for WHO NTD roadmap target discovery remains intact

## Skeptic — round 2

The advocate conflates structural prediction with experimental validation. AlphaFold-validated catalytic geometry (Data Analysis reviewer: 'rigorous in silico catalytic triad validation') proves *potential* activity, not *actual* probe engagement in live cells. The Methodology reviewer is unequivocal: 'No competition ABPP… was performed to demonstrate that probe enrichment reflects active-site labelling rather than non-specific binding; with probe specificity of only 10–43%, this omission undermines the central claim of activity-based profiling.' Probe specificity of 10–43% (Fig. 3 legend) means 57–90% of enriched proteins are non-SHs; without competition, the 37-protein list cannot be distinguished from non-specific binders that happen to possess catalytic triads. The Leishmania precedent (ref 17) does not excuse this — each system requires on-target validation.

Uncontrolled FDR is equally load-bearing. The Data Analysis reviewer states the 37 SHs derive from 'uncorrected p<0.05 thresholds across 7 probes and ~56 candidate SHs, yielding an uncontrolled family-wise error rate' and the authors 'present the resulting list as a "prioritized set" and "reference resource" without estimating the false discovery proportion.' The advocate's 'sensitivity analysis can be added in revision' dodges the reviewer's direct question: 'What is the estimated false discovery rate among the 37 reported SHs…?' If FDR is high, the 'prioritized set' claim collapses.

Strain identity remains unspecified in the manuscript — the advocate's 'almost certainly' is insufficient for a 63% coverage claim (Methodology reviewer: 'if strains differ, the reported 63% capture rate… is an invalid comparison'). Cross-strain GO bias (Dm28c→CL Brener) is acknowledged but unquantified (Rigor reviewer), risking artifactual 'lipid metabolism' enrichment.

Concede: AlphaFold curation is rigorous, limma use appropriate, MS data/code deposited, first-in-organism claim verified, ethics clean.

Verdict: The central 'activity-based chemoproteomic map' claim lacks experimental substantiation (no competition ABPP) and statistical rigor (uncontrolled FDR). These are FATAL without new experiments. Reject or require major revision with competition ABPP and FDR analysis.

**Key points:**
- No competition ABPP validates active-site labelling (probe specificity 10-43%) — Methodology reviewer: 'undermines the central claim'
- Uncontrolled FDR across 7 probes inflates false discoveries in 37-protein list — Data Analysis reviewer: 'uncontrolled family-wise error rate'
- Experimental strain unspecified — 63% coverage claim potentially invalid
- Cross-strain GO analysis (Dm28c→CL Brener) with unquantified bias
- AlphaFold validation ≠ experimental on-target engagement
- Leishmania precedent does not substitute for T. cruzi competition ABPP