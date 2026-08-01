# Related-Work & Citations Reviewer

## Summary
The manuscript's citation record is generally accurate for foundational TB drug resistance literature, but there are significant gaps in recent computational and machine-learning work directly relevant to the study's novelty claims. The claim that this is "the first study with systematic sorting and comprehensive in silico analysis" requires either stronger justification (by comparing to Portelli et al. 2018 and recent WGS-based tools) or reframing. One specific attribution (pncA essentiality) requires verification. These issues are substantial enough to warrant major revision before acceptance, as they affect the positioning of the work and its contribution to the field.

## Strengths
- Foundational citations present: Key seminal papers establishing the role of katG [19], rpoB [21], pncA [22], and embB [24–25] in first-line drug resistance are cited.
- Compensatory mechanism literature acknowledged: References [36–37, 48–49] on ahpC and rpoA/rpoC compensatory mutations are included, supporting the discussion of fitness costs.
- WHO reports cited appropriately: Global TB burden and epidemiology data from WHO Global TB Reports [2, 11] are used to contextualize the problem.
- Methodological tools documented: Bioinformatics tools (MODELLER, ConSurf, SIFT, PROVEAN, PolyPhen-2, I-MUTANT 3.0, mCSM, AutoDock) are cited with appropriate references [51–82].
- Citation hygiene sound: All references appear to be real and resolvable; no obvious fabricated or garbled citations detected.

## Weaknesses
- Missing directly competing computational work on TB drug resistance prediction (2015–2025): The manuscript claims novelty as "the first study with systematic sorting and comprehensive in silico analysis of 821 non-synonymous mutations" yet does not cite or compare against recent machine-learning and structural prediction pipelines for TB drug resistance, including multiple 2023–2025 studies on genomic resistance screening and WGS-based prediction tools.
- Claim about pncA essentiality not fully supported: The statement that "pncA is not considered essential for Mycobacterium tuberculosis growth and development [14]" cites Baddam et al. (2018), but the abstract does not explicitly address pncA essentiality, requiring verification of this attribution.
- Incomplete attribution of compensatory mutation findings: The discussion of fitness trade-offs relies on categorical ranking (lethal/moderate/mild/neutral) without citing empirical fitness measurements from the literature, and does not adequately ground the thresholds in quantitative fitness data.
- Portelli et al. (2018) [8] underutilized: This appears to be one of the few prior in silico studies of TB drug resistance mutations but is cited only in passing and not discussed in the related work section or compared methodologically.
- Recent WGS and machine-learning literature underrepresented: The manuscript does not cite or discuss advances in whole-genome sequencing for TB drug resistance prediction (2020–2025), machine-learning models for genotype-to-phenotype prediction, or reference-graph approaches, which are directly relevant to the computational methodology.
- BCG vaccine efficacy claim needs stronger source: The claim about BCG protection in babies versus adults cites McShane (2014), a commentary, rather than a primary systematic review or meta-analysis.
- Missing recent epidemiological context: The manuscript cites WHO 2020 and 2021 reports but does not cite the 2024 or 2025 WHO Global TB Reports, which would provide the most current burden estimates.
- Fitness cost literature incomplete: While Gagneux et al. [31] and Andersson & Hughes [32] are cited, the manuscript does not engage with more recent work on fitness landscapes and epistasis in TB drug resistance.

## Questions
- Can you confirm that reference [14] (Baddam et al. 2018) explicitly supports the statement that pncA is "not considered essential for Mycobacterium tuberculosis growth and development"? If not, please cite the primary source for this claim.
- How does your systematic in silico analysis of 821 mutations differ methodologically from Portelli et al. (2018) [8]? Why are recent machine-learning and WGS-based resistance prediction tools (2020–2025) not cited or compared?
- Your ranking system (lethal/moderate/mild/neutral) integrates predictions from multiple bioinformatics tools, but does not cite quantitative fitness measurements from the literature. How were the thresholds for each category determined, and should this be grounded in empirical fitness data?
- You cite Sherman et al. [49] and Comas et al. [48] for compensatory mechanisms, but these papers are from 1996 and 2012. Are there more recent studies (2015–2025) on compensatory mutations in TB that should be cited to strengthen this discussion?
- Reference [6] for BCG vaccine efficacy is a commentary. Would a primary meta-analysis be more appropriate to support the claim about differential protection in children versus adults?
- You note that mutation frequencies vary across WHO regions but attribute this to "prolonged exposure, weather conditions, and poor diagnostic testing." Are there recent epidemiological or genomic studies on regional TB lineage diversity and transmission that could explain these patterns better than the current discussion?