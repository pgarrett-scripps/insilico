# Rigor & Overclaiming Reviewer

## Summary
This manuscript presents a rigorous activity-based chemoproteomic profiling of the T. cruzi epimastigote serinome, identifying 37 enriched serine hydrolases with 63% coverage of in silico predictions. The whole-cell FP-ABPP approach is well-justified and executed, and the integration with bioinformatics is thorough. However, the interpretation of the uncaptured 37% as biologically informative rather than a technical limitation is overstated, and the conservation analysis lacks direct figure support. Minor revisions to temper conclusions and clarify data presentation would strengthen the paper.

## Strengths
- The whole-cell ABPP strategy effectively overcomes lysate agglutination issues and captures active enzymes in their native state.
- The integration of in silico curation with experimental ABPP data provides a comprehensive and validated serinome map.
- The identification of known virulence factors among the enriched SHs validates the approach and highlights therapeutic targets.

## Weaknesses
- The claim that the uncaptured 37% of predicted SHs is "biologically informative in itself" (Discussion) overinterprets negative data; alternative explanations like probe inaccessibility, low expression, or technical false negatives are not experimentally excluded, and the authors present no direct evidence for stage-specific expression or zymogen status in this study.
- The conservation analysis across trypanosomatids (Discussion) references Figure 4 for the two T. cruzi-specific proteins, but Figure 4 shows only Pfam domain architectures, not conservation data; this mismatch makes the claim unverifiable from the presented figures.
- The "first activity-based chemoproteomic map" claim (Title, Abstract, Conclusions) relies on "to our knowledge" without a systematic literature search citation; while likely true, absolute novelty claims should be hedged or supported by a database search statement.
- Probe 1 (alkyl-FP) showed poor enrichment (only 3 SHs) but is included in the probe panel description without explanation of its distinct behavior.
- The GO and PPI analyses use the CL Brener strain proteome as background due to STRING database limitations, introducing potential strain-specific bias that is acknowledged but not quantified.
- The lysate-based labelling failure is described in text but not shown in any figure, making it difficult to assess the severity of the agglutination issue.
- The manuscript states that "Benjamini–Hochberg-adjusted values were computed but not used for thresholding, to avoid discarding genuine low-abundance hydrolases", which increases false discovery risk; this choice should be justified with a sensitivity analysis.
- The rhomboid protease C4B63_34g300 is highlighted as notable, but its activity and substrate specificity are not experimentally validated beyond probe labelling.

## Questions
- Can the authors provide the conservation data (presence/absence across T. brucei and Leishmania) in a supplementary table or figure to support the claims in the Discussion?
- Was the lysate agglutination issue tested with different lysis buffers or conditions, or was whole-cell labelling adopted after a single failed attempt?
- For the two proteins absent from both T. brucei and Leishmania (C4B63_57g112 and C4B63_25g256), are there any functional data or expression evidence in T. cruzi life stages?