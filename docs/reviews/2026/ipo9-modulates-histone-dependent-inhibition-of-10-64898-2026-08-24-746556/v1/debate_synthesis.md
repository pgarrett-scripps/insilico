# Area Chair Synthesis

## Issue 1: Causal necessity of IPO9 for SR-218's cellular phenotype

**Evidence cited:** Fig. 3b–c (IPO9 knockdown phenocopies SR-218's effect on phospho-STING); Fig. 2c–h and Extended Data Fig. 4a–g (target-engagement SAR tracking phenotypic SAR); scientific_validity's explicit note that no experiment tests whether SR-218 retains activity in IPO9-depleted cells.

**Strongest case for concern (skeptic):** The manuscript infers, but never directly tests, that IPO9 is the operative target for SR-218's cellular activity. The single decisive experiment — an epistasis/rescue test dosing SR-218 in IPO9-knockdown vs. wild-type cells — is absent. This gap is compounded by data_analysis's finding that the existing knockdown phenotype is itself statistically fragile (SR-717 condition p=0.0951 and p=0.0741 for the two knockdown lines; borderline significance even in the dsDNA condition), while the text describes this as a clean "phenocopy."

**Strongest case for the paper (advocate):** The target-binding chemistry (SR-432 labeling, competition by active/inactive analogs, cross-competition by structurally unrelated ligand dbk-032A) is uncontested and rigorous. The in vitro biochemical reversal of H2A-H2B-mediated (not NCP-mediated) cGAS inhibition by IPO9 (Fig. 3d) is a clean, internally-controlled result independent of the cellular-necessity question.

**Conceded:** Advocate conceded the epistasis gap is real and that causal necessity in cells is inferred, not demonstrated. Both sides agree the in vitro target-engagement and biochemical-reversal findings stand independently of this gap.

**Status:** Unresolved but explicitly bounded. The debate converged on separating what is directly shown (IPO9 binds SR-218; IPO9 reverses H2A-H2B inhibition in vitro) from what is inferred (IPO9 is the operative cellular target of SR-218's phenotype). Not fatal to the narrower biochemical claims, but the title/abstract-level framing ("IPO9 modulates histone-dependent inhibition of cGAS" as a cellular fact) outruns this evidence. Fixable by a dose-response rescue/epistasis experiment.

## Issue 2: Undistinguished mechanisms of IPO9-mediated release (displacement vs. sequestration vs. DNA competition)

**Evidence cited:** BLI transient signal increase (Extended Data Fig. 5f–g) interpreted as possible tripartite complex; cryo-EM structure at 4.3 Å with authors' own statement that resolution "precludes definitive conclusions... at an amino acid level"; Discussion's explicit acknowledgment of three non-mutually-exclusive mechanisms.

**Strongest case for concern (skeptic):** Three separate reports (contribution_context, reporting_reproducibility, scientific_validity) independently flag that no single experiment distinguishes direct displacement, indirect sequestration of free H2A-H2B, or sequestration from DNA — this is a repeated observation across reports sharing the same underlying model, not independent corroboration, but it is also a substantive point the authors themselves concede.

**Strongest case for the paper (advocate):** This ambiguity is an authorial admission, not a reviewer-discovered flaw, and per venue norms should be credited as candor rather than penalized as a new weakness. The structural hypothesis (H18-19 loop displacing the acidic patch) is explicitly flagged as resolution-limited rather than asserted as fact.

**Conceded:** Advocate conceded the mechanistic ambiguity is genuine and undistinguished by any presented experiment.

**Status:** Unresolved, not fatal — treated by both sides as a scoped limitation appropriately flagged by the authors, requiring further biophysical work (soluble-phase BLI, SEC/AUC, sequential titration, as specified across reports) but not undermining the core biochemical finding that IPO9 antagonizes H2A-H2B-mediated inhibition in some manner.

## Issue 3: Ethics/compliance gaps — IACUC and IRB documentation

**Evidence cited:** Ethics report identifies two HARD gaps: no IACUC approval number for Trex1−/− mouse work; no IRB approval or consent statement for human PBMCs (sourced as a gift from the Teijaro Lab).

**Debate treatment:** Skeptic raised these as non-negotiable but trivially fixable compliance omissions, outside the scientific-validity discussion. Advocate agreed these are documentation lapses correctable by adding protocol numbers, not evidence of improper conduct, and that the venue's model is to publish the finding alongside the flagged gap rather than withhold it.

**Status:** Unresolved as a documentation matter, explicitly separated by both debaters from the scientific merit assessment. Not treated as fatal by either side, but both agree it must be stated plainly in any published record. No reviewer or debater disputed the ethics report's characterization.

## Duplicate/clustered criticisms (same underlying point, multiple reports)

- **Stoichiometry/resolution limits of cryo-EM (4.3 Å, sidechain assignment, 2:2 vs. 2:1 population):** Raised independently by contribution_context, data_analysis, reporting_reproducibility, and scientific_validity. This is one underlying concern about resolution-limited mechanistic inference, repeated across reports sharing a common model — not four independent confirmations.
- **BLI transient-signal interpretation (tripartite complex vs. artifact):** Raised by contribution_context, reporting_reproducibility, and scientific_validity as the same unresolved ambiguity about mechanism (see Issue 2).
- **In vivo Trex1−/− n=2 experiments / indirect pharmacodynamic marker:** Raised by data_analysis and scientific_validity; not engaged in the debate at all.

## Concerns raised in reports but not engaged in the debate

- **Physiological relevance/stoichiometry:** Cellular concentrations of IPO9 and free H2A-H2B are unreported (contribution_context); mentioned once by skeptic as a "panel blind spot" but never substantively debated.
- **Statistical/methodological transparency gaps:** Proteomics FDR/filtering thresholds unspecified (reporting_reproducibility); malachite green assay substrate concentrations not stated (data_analysis, reporting_reproducibility); BLI kon/koff and Kd values not reported; RT-qPCR pseudo-replication risk. None discussed in debate.
- **Missing citation:** Cho et al. 2024 (MRE11-mediated cGAS release) not discussed by authors (contribution_context) — not raised in debate.
- **SR-218 metabolic stability and its implications for in vivo target engagement** (contribution_context, scientific_validity) — not raised in debate.
- **Funding disclosure (SOFT gap)** — noted by ethics report, not discussed in debate.
- **Probe/reagent characterization gaps:** SR-432 synthesis/NMR/MS data absent; nucleosome core particle validation absent (reporting_reproducibility) — not raised in debate.

These silences should not be read as resolution; they reflect topics the debate did not reach rather than points settled in the paper's favor.