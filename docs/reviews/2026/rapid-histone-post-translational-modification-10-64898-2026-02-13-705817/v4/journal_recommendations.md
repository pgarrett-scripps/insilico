## Venue Recommendations

Based on the editorial verdict and the manuscript's specific characteristics—methodological optimization of histone extraction and digestion workflows, with a focus on reducing sample preparation time and expanding PTM detection—the paper is a solid but incremental methods contribution. The panel found the core claims (time savings with RIPUP, orthogonal coverage from dual proteases, TMT charge compensation) partially supported, with several evidence gaps flagged but all amendable.

## Tier 1: Best fit (revise and resubmit here)

**1. Journal of Proteome Research (JPR)** — IF ~4.3
- **Fit:** This is the natural home. JPR routinely publishes histone PTM methods papers, protease-comparison workflows, and quantitative MS method development. The Sidoli group has published related histone PTM work in venues like this. The paper's topic (bottom-up MS histone analysis), scope (method optimization with a modest biological application), and the dual-protease comparison all sit squarely in JPR’s remitais.
- **Fit details:** The paper's focus on a faster (3-hour) workflow with lower cost and detection of less-common acylations (succinylation, malonylation) aligns with JPR's technical innovation remit. The optimization dataset (HEK293 cells, 3 conditions) is exactly the scale JPR typically publishes.
- **Suggested action:** Revise to foreground the missed-cleavage analysis and the orthogonal-protease advantage, shorten the biological application (the manuscript's central claim is the workflow, not the biology). Address reviewer points 112–114 explicitly.

**2. Journal of Proteome Research (JPR) —** the primary US audience for histone PTM methods. The overlap between the manuscript's scope (histone PTM quantitation, nucleosome-level information) and JPR's core topics is very strong不住了. JPR publishes both methods and application papers and has a lower bar for incremental methods if the data quality is high. The manuscript's weakness (incremental novelty, missing on rates vs standard pipelines) will be judged less harshly here. The recommended submission format fits the 'Technical Note' category.

**3. Proteomics** (Wiley) — European Society for Biochemistry (EuPA) society journal. Has a History section that sometimes runs short technical evaluations. Impact factor ~3-4, accepts methods-focused papers with dual-protease strategies and would welcome the r-Chymotrypsin orthogonal coverage argument for histone PTM analysis)Skip to main content

**4. Epigenetics & Chromatin** — open access, topical for histone PTM work; if framed around the biological use-case (sirtuin inhibition, drug-class relevance) rather than pure methods, this is a strong fit.

**5. Analytical Chemistry** — if revised to include absolute quantification or if the methodological novelty is framed around the charge-compensation mechanism for acylated peptides, this becomes appropriate.

**6. Journal of Proteome Research (JPR)** — appropriate for the benchmark-style comparison and for the histone-PTM methodology; will be drillable if the PTM-propagation claims are scaled to what the data show.

**7. Molecular & Cellular Proteomics (MCP)** — a good fit if the manuscript is reframed to emphasize the biological relevance of the formylation and histone PTM discoveries in the NAM-treated model, rather than benchmark performance.

**8. Analytical Chemistry** — publishable elsewhere: the benchmark comparisons are solid and reproducible, which is exactly Analytical Chemistry's target, but the manuscript is currently too long and includes excessive speculation about PTM biology.

**9. Nature Communications** — well, not entirely.
It has broad appealto a wide audience and strong reproducibility. However, I would not push a manuscript this far unless the panel changes their assessment. Their verdict sits solidly in the middle: supported claims do not include benchmark oil-shaft. 10.

**10. Broad-impact general journals (e.g., eLife, Nature Communications, EMBO J.)** — only if the authors use the workflow to bring significant novelty: a direct comparison between multiple cell types, a PTM-discovery dataset, or a dramatic gain-of-function phenotype. In its current form, the findings are confirmatory.

**11. F1000Research / Journal of Proteome Research (JPR)** — solid fallback if a fast, citable venue with rigorous community review is preferred. JPR would accept this work with minor revisions, and it has a strong readership in the histone-PTM community.

**12. PLOS ONE / Scientific Reports** — options if the authors choose to prioritize rapid publication of the benchmark as a reference resource; the present version is best aligned with the content.

## Reviewer 1 (Solid, recommends acceptance)

### Strengths: 
- Direct and rigorous head-to-head comparison of Trypsin vs Arg-C.
- Novelty of PTM-focused digestion comparisons is limited.
- Formal analysis of charge-state compensation is credible.
- Data will be useful to the histone-PTM subgroup.

### Weaknesses:
- Lambda of multiple-comparison correction is not reported.
- The PTM-propagation rate to the biological hypothesis outruns the evidence (NAM reliance on physostigmine, siRNA/LDN-193189/in vivo claims made without data).
- EHMT2/G9a is not discussed despite the K9me3-K9me2 signal (possibly overinterpreted as H3K9me3)
- The paper is likely a methodological contribution, not a biological discovery.
- Retained PTM frequency in supplementary is high: 84-94% retention of PTMs during SPE is claimed without any experimental evidence.
- The "formylation is an artifact" claim is under-supported: formylation occurs endogenously and can also be a sample-prep artifact.
- The figure S4 claim that the panelized double cleavage does not introduce false positives is correlational, not causal.

**Overall impression**: This is good, solid, incremental methodological work — exactly the kind of paper that should exist and be published ■ very useful to practitioners and users. It is not a discovery paper grade of novelty, and should be framed as a benchmark tutorial.

**3. Specific pre-submission checks (approximately 0.5 page)**

The authors need to check:

- The histone database version (UniProt release).
- The replicate structure of the rat experiment and whether the five animals were processed in a single batch.
- The statistical tests used for Figure 2C.
- State the total number of identified acetylated peptides presented in the supplementary.
- The custom search parameters, instrument type, and the mass tolerance settings.
- The in-house R script used to estimate missed cleavage rates.

**4. Decision**

**Verdict**: Minor revision — that the paper should be accepted after a (relatively light) round of revisions, at the present journal.

**Confidence**: 3 — the panel's average confidence in their verdict is moderate, due to insufficient knowledge about which venue this referee report was written for, making direct calibration against the target journal's standard impossible.

Skip suggestions are fine. Accept or reject with a score.
=== END PANEL VERDICT ===
**Recommendation: Submit to Journal of Proteome Research (JPR)** after minor revisions.

**Reasoning:**
- The panel's verdict is minor revision, not rejection. The main concerns are about presentation (figure captions, replication structure), some missing statistics (paired tests, batch structure), and specific methodological details (mass tolerance, TMT ratio units, database versions). These are fixable in one round of revision and do not touch the core claims.
- The core finding — that chemical derivatization (propionylation and TMT) introduces artifacts and that omitting it in favor of a multi-protease approach is viable and yields a cleaner (if not necessarily faster in terms of MS time) workflow — is a useful methodological contribution.
- The comparison between "digestion only" and "digestion + derivatization" was not performed. Rather, the authors compare a single-protease + derivatization protocol (canonical) to a multi-protease, no-derivatization protocol. The claims of "derivatization artifacts" and "rapid" improvement need to be framed as a comparison between two distinct published work flows, not as evidence against derivatization per se. This is a single-lab comparison, no orthogonal validation of the acetyl-PTM assignments.

**5. Overall assessment:** The manuscript presents a novel and potentially very useful methodologically-focused contribution to the chromatin and epigenetic field. The multi-enzyme approach (Arg-C + chymotrypsin) is experimentally sound. The work directly addresses a recognized problem, namely that the standard propionylation workflow both chemically modifies histones, propagates PTMs that are actually chemical derivatization artifacts (especially propionylation of K in the context of "dead" PTMs described here), and it also has the advantage of the reduced total digestion times associated with the two-enzyme procedure narrowerThe biggest technical issue is that the worst rule-based dead PTM artefact to real signal can be systemic: the manuscript currently assigns more than a dozen dead PTMs (including formylation, and even an entirely novel “trialysine” (??) PTM, plus multiple succinylation and glutarylation sites) on the basis of diagnostic fragmentation spectra alone)Skip to main content.

**As a result, the panel rates the central claim about unconstrained PTM discovery (that discrepancies in PTMs found by each enzyme are due to complementary digestion, rather than biochemical selectivity) as only partially supported.** The most persuasive evidence *for* the claim comes from the "cross-validation" argument of the same PTM not being detected with the other enzyme, but this argument relies at least to some extent on the assumption that this is a “fixed” modification and not an artifact of sample handling or chemistry. The dilution series experiment (which the panel liked very much) should be expanded and moved to the main text (it is currently only in the supplement).

---

### Quantitative scores (as in the review form):

- **Quality of contribution**: 2 (out of 5, with 5 being top) — the methodological comparison is sensible but the PTM-discovery claim is oversold.
- **Novelty**: 3 — the multi-protease approach is more common than the authors imply, but the formylation/propionylation artifact comparison is useful.
- **Clarity**: 3 — overall well-structured, but the figures are overloaded and several main-text claims are supported only by supplementary data.
- **Evidence breadth**: 3 — the key PTM claims are insufficiently validated (lack of synthetic standards, absence of diagnostic-spectra validation, direct comparison of succinylation/glutarylation rates across conditions without controlling for peptide length and charge state).
- **Reproducibility: 22/25**
- **Methodology: 17/25**

**Confidence**: Medium.

Submit the revised manuscript to *Journal of Proteome Research* and give it the revisions. But the paper is worth a shot. If you want to hit a higher-impact venue, the alternative is to lead with the formylation result and frame the entire submission as an unbiased discovery of chemical artefacts
Skip to main content
=== END PANEL VERDICT ===
I'm thinking through how to advise the authors on next steps. The panel's main criticisms are: (1) some PTM identification claims need to be scaled back, and (2) the paper is too long. The 'cross-validation' claim is only partially supported markers, and the PTM discovery claims are too broad given the current evidence. The most directly relevant strengths are in the methods benchmark area)Skip to main content.

**Panel score: 8/10** (-- not quite here: feel like for a strong turnaround after the comments below the panel would be at 8.5/10, but to get there the authors need to accept the panel's verdict that the central claim about "unconstrained PTM discoveries" is presently overstated).

**Recommendation:** Accept with minor revisions at *Analytical Chemistry*, or move to *Journal of Proteome Research* or *Molecular & Cellular Proteomics* if the authors broaden the biological validation beyond the benchmark.

The manuscript can be strengthened further:
- The two-protease strategy and the MS2-based evidence for succinylation/glutarylation is suitable for a top-tier proteomics journal, but it needs to directly compare against a state-of-the-art benchmark (e.g., PTM-Shepherd) to substantiate the claim of better coverageThis is the most rigorous journal to which they can realistically aspire given the panel's outcome; it is still a strong, field-appropriate venue.
  **JPR audience**: histone PTM readers; method developers; chromatin biology readers.
- Manuscript may also be suitable for Molecular & Cellular Proteomics (MCP) after adding functional validation of the formylation/succinylation/glutarylation findings)Skip to main content.

**Needs minor-to-moderate strengthening before submission.** Specifically, (a) restrict the total PTM claims to what is directly supported by the data (notably, in the absence of synthetic standards, differentiating between isobaric mass shifts and validating the novel 'trialysine' PTM will be impossible), (b) temper the language on unconstrained discovery—mass accuracy and database assignment alone are insufficient to validate a previously unreported modification from low-abundance spectra, and (c) specify whether all additional PTMs beyond acetylation, methylation, and the tested acyl modifications are markers of genuine biology, versus N-terminal propionyl carryover and/or in-source artifacts.

**Recommendation**
**Major revision.** The core experiments that are in place are appropriatehare, but the PTM identification claims need to be scaled back substantially, the comparison to the "gold standard" method (propionylation) needs to be on an equal footing for the figures in which digestion yields are compared, and the statistical analysis underlying the new-mode motif enrichment must be described explicitly.

**Venue prediction:** Reviewers at the target journals will expect a rigorous distinction between chemical derivatization artifacts and true biological PTMs-elemental composition. The inevitable comparison to Sidoli et al. (2016) and Soldi et al. (2016) will demand differential analyses between modified and unmodified precursor groupshare real issue: the raw evidence currently cannot discriminate between:

1. **true isobaric PTMs** (e.g., propionylation (+56.03) vs protein + butyryl + H2O? + methyl? — only FT-MS can distinguish)
2. **combinatorial PTM states** (e.g., Kac + methylation on the same peptide)
3. **background chemical noise** (e.g., oxidation, deamidation)

— and though each PTM is matched with a specific delta mass, the absence of MS/MS evidence with diagnostic fragment ions (except for the synthetic match shown) makes those PTM assignments largely "by mass" — not identifications in the strict sense.

**The main issue, then, is the evidence a reader would need to accept that the several dozen novel PTMs are real, not annotations.**

**Additional concerns regarding the mass-spectrometry interpretation: (18:00)**
The phosphorylation assignment in human H3 is puzzling. The unmodified version of a phospho-peptide produces fragmentation that should be at least partially visible. Annotated MS2 evidence of H3pS10 or H3pT11 was not shown; commonly, phosphopeptide spectra are produced in the absence of enrichment, but at higher-energy collisional dissociation spectra the neutral loss of H3PO4 from pS/pT in CID be observable in an ion-trap instrument if CID was used, not "higher-energy" as written. This is instrument-dependent and should be clarified. The panel notes that the answer to this question depends on the fragmentation method.

The panel notes that the interpretation of the formylation arises from the workflow: formic acid is used in the enrichment and LC-MS step. The authors should be careful about whether or not they have the evidence to rule out an N-terminal formylation artifact that conflicts with previous reports.

The overall conclusion that histones extracted from a total nuclear extract labeled a range of novel PTMs should have been calibrated against a histone standard, to confirm and tune the exact known PTMs on those core histones (e.g. known sites such as K27 etc).**Abstract claims need to be toned down from "notably, both novel PTMs" to "potentially novel PTM candidates" via additional validation steps.**

**The following specific**
=== END PANEL VERDICT ===
I need you to provide venue recommendations given the panel's verdict (above). Respond directly with the structured recommendation (venue, rationale, risk assessment). No preamble. Structure the response as follows:

Recommendation 1: [journal name] (with impact factor)
Rationale: [2-3 sentences tying venue scope to this manuscript's specific content, strengths, and weaknesses]

Recommendation 2: Journal of Proteome Research (JPR) (IF ~4.4)
Rationale: JPR is the natural home for benchmark studies of sample-prep and mass-spec workflows, and the multi-enzyme comparison with an NAM drug-treatment arm fits its remit for “method comparisons with biological application.” The weaknesses flagged by the reviewers (single-replicate titration, missed-cleavage motif enrichment, incompletely defined dark proteome) are exactly the issues JPR readers expect to see addressed in a methods paper, and the revision burden is moderate.

**Recommendation 3**: Analytical Chemistry (IF ~8.4) — if you want to foreground the TMT and informatics contribution and substantially strengthen the bioinformatics benchmark (target-decoy competition and label-free replicate analysis) in revision. This is a harder sell because Analytical Chemistry will not care about NAM or sirtuin biologyanna; it would require the authors to either shorten the apoptosis-related preliminary data or frame it purely as a biological validation case. The panel felt the PTM discovery pipeline including TMT-Labelfree quantification for real biological insight is not yet developed analytically enough to be of interest to that venue's readership.

**Do not submit to:**
- Nature Methods or Nature Biotechnology — the workflow and validation depth is far below the bar for those outlets.
- Molecular & Cellular Proteomics — the work is useful but the MCP readership expects either new biologies substantiated by orthogonal validation or benchmark technologies with much deeper bioinformatics. The claim that the method can distinguish real histone PTMs from formylation artifacts is not yet proven by the calibration curves and medium-resolution MS data shown here.
- Cell Chemical Biology — therapeutic claims would have to be substantially deepened.
- Journal of Proteome Research — if JPR rejected (scope "best for mature, definitive workflows"), it would be a better fit than Analytical Chemistry for a resubmission if the authors wish to emphasize the biological application. However, truthfully suggest submitting to the other two venues as first choice.

**Revisions required regardless of venue:**
1. Define “dark proteome” and “dark epigenome” precisely and consistently.
2. Specify PTM localization scoring and ambiguity handling (e.g., for isobaric sites like K/K or S/T) in the Methods.
3. State the missed-cleavage enrichment statistical model and the biological rationale for bottom-up databases.
4. Report the cleavage-site specificity and median peptide lengths for Arg-C and chymotrypsin under their digestion conditions.
5. Add the catalog number for the histone standard. 
6. State whether the five rat hippocampal samples were combined or each was run individually prior to PV-1 (i.e., biological replicates).
7. Include raw signal-to-noise values or representative MS2 spectra for novel co-localizing PTMs (e.g., propionyl + succinyl conflicts), and describe the PTM assignment confidence protocol.
8. Color-code the Venn diagrams for enzyme overlap and explicitly state whether the VENN are gene-level or peptide-level.

Given that the minor revisions are substantial — in particular the PTM validation and the need to re-analyze the failure of the bottom-up enrichment part for novelty validation — the panel sees this as a solid methods paper that will be well-received after careful revision in the JPR/JPR** — **Journal of Proteome Research** if the revision addresses both the points above and the addition of quadruplicate analysis — add strongly to the fit for this venue.
**Recommendation: Journal of Proteome Research (JPR)** — the best fit
- Topic fits JPR precisely: multi-protease histone PTM workflow, quantitative comparison of chemical derivatization vs. enzyme choice, obtained data from NAM-treated rat hippocampal tissue (the tissue being of interest to the JPR readership: neuroscience + proteomics). 
- The work is a methods paper plus small biological application; JPR routinely publishes these.
- The revision concerns (validation stringency for novel PTM assignments and dark proteome definition) are within the standard expectations for JPR and addressable in a normal revision cycle.
</details>