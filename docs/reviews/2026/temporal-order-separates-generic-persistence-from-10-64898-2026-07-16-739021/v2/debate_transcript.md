# Debate Transcript

## Advocate — round 1

The manuscript delivers a genuine methodological advance: an exact analytical order-null that isolates sequence-dependent persistence from static polarity and step content, enabling exact decomposition identities (Eqs. 8–12) that close to machine precision. This is not merely a shuffled-step null — it provides a computationally efficient, permutation-free reference that makes the biological comparison explicit ("how much a cell moves, whether it continues moving persistently, and whether that persistence remains aligned with an environmental cue" — Abstract). The framework is demonstrated across three biologically distinct perturbations (matrix: MYO10–collagen; geometry: haptotaxis; metabolism: PFKL), revealing insights conventional metrics miss: the MYO10–collagen buffering interaction is carried ~70% by temporal order (Fig. 3B,E); wide geometry redistributes order from gradient to lateral axis without increasing total order (Table 4, intrinsic lateral order +0.2176, 95% HI 0.1274–0.3171); PFKL-N702T impairs cue-aligned runs (FMI −0.278, run −0.666 steps) while generic serial order meets a locked non-inferiority margin (Table 5). Statistical rigor is exceptional: hierarchical bootstrap with simultaneous bands, lag-invariant cohorts, leave-one-FOV-out, exact closure checks, and locked robustness plans (HC3, propensity matching, overlap weighting).

Reviewers correctly flag three limitations that require revision, not rejection: (1) Low biological replication (n=3 repeats for MYO10, zero replicate labels for PFKL) — the manuscript already acknowledges these boundaries explicitly (Discussion: "inference remains limited to this specific experimental batch\); "track-level intervals cannot replace replicate-level inference\)). Revision should add a prominent "Limitations" paragraph and qualify language from "reproducible" to "repeat-consistent in this dataset." (2) Analytical order-null assumes exchangeability — add a stationarity discussion in Results/Methods referencing the early-vs-late test (Appendix 1–Fig. 5) and note that non-stationarity would inflate sequence-excess. (3) Non-inferiority margin justification — add a sentence explaining the 0.10-SD choice (e.g., based on observed SD of cue-FMI in WT).

Reproducibility gaps (no public code/environment) are fixable: the authors commit to depositing a versioned workflow with environment capture before publication; this should be a condition of acceptance. Missing citations (Fraley 2015, Paul 2016) must be added with a clear distinction: the analytical order-null provides exact expectation and decomposition closure, not just Monte Carlo shuffling. Terminology harmonization ("sequence excess" vs "sequence-dependent persistence\); "stationary" vs "nonlinear" angular model) is trivial.

The core contribution — a transportable, exact framework separating motility, generic persistence, and cue commitment — is novel, rigorous, and biologically useful. The limitations are transparently stated and addressable in revision. Accept with revisions.

**Key points:**
- Analytical order-null is a novel methodological advance: exact, permutation-free, enables algebraic decomposition closure (Eqs. 8–12).
- Framework cleanly separates three biological questions across three distinct perturbation types (matrix, geometry, metabolism).
- Biological insights not accessible to conventional metrics: MYO10–collagen interaction carried by temporal order (~70%); geometry redistributes order axis without increasing total; PFKL-N702T spares generic persistence while impairing cue alignment.
- Statistical rigor exceeds field standards: hierarchical bootstrap, simultaneous bands, lag-invariant cohorts, leave-one-FOV-out, locked robustness plans.
- Limitations (low replication, stationarity assumption, arbitrary non-inferiority margin, missing code/citations) are transparently acknowledged and fixable in revision — not fatal flaws.
- Reproducibility commitment (versioned workflow + environment) should be condition of acceptance.

## Skeptic — round 1

The advocate concedes the replication crisis but calls it 'fixable by qualification.' It is not. The MYO10–collagen discovery claim — that a buffering interaction is 'carried mainly by the order of directions' (~70% sequence-excess, Fig. 3B,E) — rests on n=3 biological repeats with one (R3) 'disproportionately large and phenotypically distinct' (Methods). Hierarchical bootstrap with n=3 yields ≤27 unique resamples; simultaneous bands and leave-one-FOV-out cannot manufacture between-repeat variance. The PFKL conclusion — 'PFKL filamentation supports cue-aligned commitment without reducing generic serial order' (Abstract) — is explicitly track-level only because 'biological-replicate identity was lost' (Table 5, Discussion). Track-level non-inferiority (0.10-SD margin, arbitrary) cannot support a biological generalization about PFKL function. These are not textual fixes; they are missing experimental units. The paper presents them as supported findings (Abstract: 'reproducible MYO10–collagen interaction'; 'PFKL-N702T produced fewer up-gradient steps') rather than hypothesis-generating observations.

FATAL: Biological replication insufficient for population-level claims in both primary datasets. No revision can create missing replicates.

FATAL: Analytical order-null assumes step exchangeability (Eq. 8). If 14-h movies have non-stationary speed/direction trends (untested; early-vs-late test in Appendix only checks interaction strengthening, not stationarity), permutation destroys trends and inflates sequence-excess. The ~70% figure could be artifact. The advocate's 'add stationarity discussion' does not fix an unvalidated null.

FIXABLE but severe: Non-inferiority margin (0.10 SD) unjustified in main text; reproducibility artifacts absent (no code/environment/versioned workflow); missing citations (Fraley 2015, Paul 2016) overstate novelty.

Concede: Method is mathematically novel (exact order-null, algebraic closure) and framework is conceptually valuable. But biological claims exceed evidence. Reject or require new data.

**Key points:**
- MYO10–collagen n=3 repeats (one anomalous) cannot support 'reproducible' interaction or simultaneous bands
- PFKL track-level inference (zero replicate labels) cannot support biological conclusion about PFKL function
- Analytical order-null stationarity assumption untested; may inflate sequence-excess (~70% claim)
- Non-inferiority margin arbitrary; reproducibility artifacts missing; novelty overstated vs. Fraley 2015/Paul 2016
- Method mathematically sound but biological claims exceed evidence — fatal for acceptance

## Advocate — round 2

The skeptic conflates two distinct contributions: (1) a novel, exact analytical framework that separates motility, generic persistence, and cue commitment — demonstrated across three perturbation types — and (2) the specific biological conclusions in each dataset. The manuscript explicitly qualifies both: the MYO10–collagen interaction is 'repeat-consistent in this dataset' (Discussion) and 'inference remains limited to this specific experimental batch'; the PFKL conclusion is 'explicitly track-level' because 'biological-replicate labels were lost' (Discussion, Table 5). These are not overclaims but transparent boundary statements.

The analytical order-null (Eqs. 8–12) is a genuine methodological advance: exact, permutation-free, with algebraic closure to machine precision — unlike Monte Carlo shuffling in Fraley 2015 or Paul 2016. The framework's transportability is shown by distinguishing sustained (HUVEC), short-lived (MDA-MB-231), and sign-reversing (MDCK) regimes in independent archives (Fig. 6A–C, Table 7) — a conceptual demonstration, not a controlled comparison.

Conceded: stationarity assumption deserves explicit discussion (early-vs-late test in Appendix 1–Fig. 5 only checks interaction strengthening); non-inferiority margin needs justification; reproducibility artifacts must be deposited. These are revision requirements, not fatal flaws. The core contribution — a documented, exact workflow that calculates sequence-dependent persistence, axis-resolved order, and cue-directed runs from standard x–y tables — is novel, rigorous, and immediately usable. Accept with revisions: add Limitations paragraph, stationarity caveat, margin rationale, citations (Fraley 2015, Paul 2016), and deposit versioned code/environment.

**Key points:**
- Analytical order-null is a novel methodological advance: exact expectation, algebraic closure, permutation-free — distinct from Fraley 2015/Paul 2016 Monte Carlo shuffling.
- Framework cleanly separates three biological questions across matrix, geometry, and metabolic perturbations — demonstrated, not just claimed.
- Biological conclusions are explicitly qualified: MYO10–collagen 'repeat-consistent in this dataset'; PFKL 'track-level only, cannot replace replicate-level inference'.
- Cross-system validation shows transportability (sustained/short-lived/sign-reversing regimes), not controlled taxonomy.
- Limitations (n=3 repeats, track-level PFKL, stationarity assumption, arbitrary margin, missing code/citations) are acknowledged and fixable in revision — not fatal to the methodological contribution.

## Skeptic — round 2

The advocate concedes every limitation I raised but reclassifies them as 'revision requirements.' This is the core disagreement: qualification cannot rescue biological claims built on n=3 repeats (one anomalous) and zero replicate labels. The Abstract states 'reproducible MYO10–collagen interaction' and 'PFKL-N702T produced fewer up-gradient steps' — unqualified population claims. The Discussion's 'repeat-consistent in this dataset' and 'track-level only' are post-hoc hedges that contradict the Abstract. A method paper demonstrating utility on fatally underpowered data does not demonstrate utility; it demonstrates the method can produce seemingly precise estimates from insufficient replication.

FATAL: MYO10–collagen n=3 repeats (R3 'disproportionately large and phenotypically distinct' per Methods) cannot support simultaneous bands, leave-one-FOV-out, or '70% sequence-excess' (Fig 3B,E). Hierarchical bootstrap with n=3 yields ≤27 unique resamples — the precision is illusory.

FATAL: PFKL conclusion ('PFKL filamentation supports cue-aligned commitment without reducing generic serial order', Abstract) is explicitly track-level only (Table 5, Discussion) because biological-replicate labels were lost. Track-level non-inferiority (arbitrary 0.10-SD margin) cannot support a biological mechanism claim.

FATAL: Analytical order-null (Eq 8) assumes step exchangeability. Fourteen-hour movies likely have non-stationary speed/direction trends; permutation destroys trends and inflates sequence-excess. The early-vs-late test (Appendix 1–Fig 5) checks interaction strengthening, not stationarity. The ~70% figure may be artifact.

FIXABLE but severe: Non-inferiority margin unjustified; reproducibility artifacts absent (no code/environment/versioned workflow per Reproducibility reviewer HARD findings); novelty overstated vs Fraley 2015/Paul 2016 (analytical vs Monte Carlo is computational, not conceptual).

Conceded: Mathematical framework is novel (exact order-null, algebraic closure); statistical safeguards exceed field standards; cross-system transportability shown descriptively.

Verdict: Biological claims exceed evidence in ways revision cannot fix. Reject.

**Key points:**
- MYO10–collagen n=3 repeats (one anomalous) cannot support 'reproducible' interaction or 70% sequence-excess claim
- PFKL track-level inference (zero replicate labels) cannot support biological conclusion about PFKL function
- Analytical order-null stationarity assumption untested; may inflate sequence-excess (~70% claim)
- Non-inferiority margin arbitrary; reproducibility artifacts missing; novelty overstated vs Fraley 2015/Paul 2016
- Method mathematically sound but biological claims exceed evidence — fatal for acceptance