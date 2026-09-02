# Area Chair Brief for Editor-in-Chief

## Manuscript overview
RIPUP is a methods paper combining Arg-C Ultra and r-Chymotrypsin digestion with TMT labeling for histone PTM analysis, benchmarked against Trypsin+propionylation. Headline claims: (1) faster (~3h) workflow with comparable/superior PTM coverage; (2) TMT's tertiary amine "rescues" detection of acidic acylations (succinylation, glutarylation) via charge compensation; (3) proof-of-concept application to rat hippocampal tissue (231 PTM sites). All five specialist reports converged at score 4 (ethics at 5, no compliance issues raised or debated).

## Issue 1: Collision-energy confound in the charge-compensation mechanism (central to debate)

**Evidence cited:** Methods state fixed 30% NCE for non-TMT samples vs. stepped 30/40/50% NCE for TMT samples. The succinylation/glutarylation "dark epigenome" claim (58/31 sites, Abstract) rests on this TMT-vs-propionylation comparison.

**Convergence note:** This point was raised independently by data_analysis, reporting_reproducibility, and scientific_validity reviewers using different textual entry points (Methods parameters, mechanism narrative, missing unlabeled-vs-labeled comparison respectively). The skeptic argued this is genuine corroboration rather than model-multiplicity noise, since each reviewer located different supporting evidence for the same structural problem. This is a defensible reading, though the AC notes all three reviewers likely share the same underlying model and the convergence should be weighted as strong but not fully independent confirmation.

**Advocate's case:** Stepped NCE for TMT is standard practice (cited prior work, ref 23), not an ad hoc oversight; the empirical outcome (differential site counts) stands regardless of which mechanism is correct; the manuscript already frames the tertiary-amine explanation as inference, not fact.

**Skeptic's case:** The confound is stated in the authors' own Methods, not inferred by reviewers; it directly undermines the ability to attribute the effect to charge compensation rather than more thorough fragmentation; zero orthogonal or synthetic-peptide validation is offered anywhere to break the tie.

**Concessions:** Advocate conceded the confound is real and unresolved for isolating *mechanism*. Skeptic conceded the digestion-efficiency advantage of Arg-C Ultra (Figure 2C) is measured independently of this issue, and that the authors are candid about *other* limitations.

**Status: Unresolved, load-bearing but not fatal to the paper as a whole.** The confound is real and acknowledged by both sides; it specifically undermines the mechanistic explanation for the abstract's flagship discovery, not the descriptive outcome (TMT-labeled samples detect more succinylation/glutarylation sites). Resolution requires either matched-energy control experiments or explicit softening of causal language in the Abstract/Discussion. The skeptic noted a buildable-but-unperformed check (comparing unlabeled vs. propionylated samples, both at fixed NCE, from Figure 5A/5B data already in the manuscript) that could partially isolate energy from labeling — this remains an open, low-cost recommendation for revision.

## Issue 2: Internal inconsistency between Abstract and Results on Arg-C Ultra+TMT vs. Trypsin+Prop

**Evidence cited:** Abstract states Arg-C Ultra+TMT "exceeds Trypsin-based approaches" in total PTM detection; Results state TMT-labeled samples achieved "comparable PTM numbers to conventional 'Trypsin + Prop' methods (~120 PTMs)" (flagged independently by scientific_validity reviewer, raised by skeptic in debate).

**Advocate's case:** Reads as imprecise Abstract wording summarizing a multi-condition comparison, not a fabricated number since the Results text is clear a few paragraphs later; resolvable by editorial revision.

**Skeptic's case:** This is a plain textual contradiction in the paper's central quantitative claim, not an interpretive dispute.

**Concession:** Advocate conceded this is a real inconsistency worth fixing.

**Status: Resolved as fixable, not fatal.** Both sides agree this is a wording/consistency problem requiring the authors to reconcile Abstract and Results language, not a deeper evidentiary failure.

## Issue 3: Arg-C Ultra vs. Trypsin comparison confounded by labeling chemistry (raised in reports, not engaged in debate)

The contribution_context reviewer noted that Arg-C Ultra is only ever compared to Trypsin when paired with different labeling strategies (TMT vs. propionylation), and that the one same-label comparison available (Arg-C Ultra+Prop: 254 peptides vs. Trypsin+Prop: 179) shows only a modest advantage — undermining the strength of the protease-superiority claim independent of the labeling confound. **This did not come up in the debate and stands unaddressed.**

## Issue 4: Missed-cleavage redistribution confounding the NAM quantitative experiment (raised in reports, not engaged in debate)

Both data_analysis and reporting_reproducibility reviewers raised that NAM treatment induces dose-dependent missed-cleavage redistribution, meaning fold-changes in the quantitative peptidoform analysis (Figure 7) may reflect cleavage-efficiency shifts rather than true PTM occupancy changes. Reviewers proposed a concrete check (restrict to zero-missed-cleavage peptidoforms, or stratify significant peptidoforms by modified/unmodified status). **This is a substantive, independently-raised concern across two reports that never entered the debate** and should not be read as resolved.

## Issue 5: Lack of orthogonal/synthetic validation for succinylation and glutarylation sites (raised in reports, touched on but not resolved in debate)

Multiple reviewers (contribution_context, data_analysis, reporting_reproducibility, scientific_validity) independently flagged that the 58 succinylation and 31 glutarylation sites — the paper's headline novel finding — rest entirely on computational assignment with no synthetic peptide or orthogonal-method validation. The debate touched this only in the context of the NCE confound; the standalone absence of validation was not separately debated but is repeatedly noted across reports and compounds the NCE issue rather than being resolved by it.

## Concerns from reports not engaged in debate at all

- Formylation presented as a possible finding but not experimentally distinguished from known sample-prep artifact (contribution_context, reporting_reproducibility).
- Rat hippocampal proof-of-concept (231 sites) lacks per-animal reproducibility breakdown and any comparison to prior literature or orthogonal method (multiple reviewers).
- Propionylation efficiency benchmark may be unfairly low due to buffer choice (ammonium bicarbonate vs. optimized TEAB-based protocols) (multiple reviewers).
- Cost analysis excludes instrument/researcher time and r-Chymotrypsin's uncertain "Early Access" pricing (contribution_context, scientific_validity).
- Dual-protease "complementary coverage" claim not quantified (unique vs. shared PTM sites per protease) (contribution_context, scientific_validity).