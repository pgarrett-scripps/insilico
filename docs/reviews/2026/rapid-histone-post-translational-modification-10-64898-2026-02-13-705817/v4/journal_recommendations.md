# Venue Guidance for RIPUP Manuscript

## as_is
**In Silico** (the target venue)

This manuscript is *in scope* for In Silico as submitted. It presents original empirical and methodological work with deposited data (PXD073683), code (GitHub), and sufficient procedural detail for inspection. The central claims are evaluable from the manuscript and materials. The editor's verdict of "major" does not disqualify submission to In Silico — the journal explicitly publishes work with identified limitations and unresolved confounds, provided they are stated plainly. The charge-compensation mechanism is currently asserted rather than proven, and the quantitative analysis conflates cleavage-state redistribution with PTM abundance, but neither gap prevents readers from judging the evidence themselves.

**Submission strategy:** Post to bioRxiv or similar preprint server first (if not already done), then submit to In Silico with a cover letter acknowledging the editor's major-revision points and indicating which you will address before publication. In Silico's model-based review process and public-record format actually reward candour about unresolved confounds — the panel's convergence on a score of 4 reflects confidence that the work is sound despite those gaps. Addressing even 3–4 of the 12 required revisions (especially #1, #3, #6, #8) before submission would substantially strengthen your position.

---

## after_revision

**Journal of Proteome Research** (ACS)

Once the collision-energy confound is resolved (Required Revision #1) and the quantitative analysis is reframed to separate cleavage-state effects from PTM abundance (Required Revision #3), this becomes a strong fit for JPR. The journal publishes methods papers with systematic benchmarking, and the dual-protease strategy plus TMT-labeling comparison are exactly the kind of practical workflow optimization JPR's audience (analytical and bioanalytical proteomics labs) needs. The 89 acidic-acylation sites do not require synthetic validation at JPR if the computational filtering is rigorous (which it is, via HiP-Frag), but the mechanistic claim about charge compensation must be either supported by matched-energy data or explicitly reframed as a hypothesis. Acceptance odds post-revision: **60–70%** (solid methods contribution, but the confound resolution will determine whether the headline claim survives intact).

**Molecular & Cellular Proteomics (MCP)**

MCP is the natural home for this work if you can address the protease-vs-labeling confound (Required Revision #5) and provide the dual-protease complementarity quantification (Required Revision #6). The journal has published recent work on histone PTM discovery (Vai et al. 2025, which you cite) and actively seeks methods that expand the PTM landscape. The "dark epigenome" framing is exactly MCP's scope, and the tissue application (rat hippocampus) adds biological relevance. The quantitative NAM experiment, once decoupled from cleavage-state redistribution, would be a strong secondary contribution. Acceptance odds post-revision: **65–75%** (the field recognizes the need for this comparison, and MCP values comprehensive benchmarking).

**Analytical Chemistry** (ACS)

If your primary contribution is the TMT-labeling chemistry and its mechanistic advantage for acidic acylations, this is a strong fit for Anal. Chem., especially once the collision-energy confound is resolved. The journal publishes analytical method development and validation, and the charge-compensation hypothesis (if properly qualified) is a genuine chemical insight. The benchmarking across ten conditions and three proteases is exactly the kind of systematic parameter exploration Anal. Chem. readers expect. Acceptance odds post-revision: **55–65%** (depends heavily on whether you can isolate the chemical mechanism from the acquisition-method effect; if you can, this rises to 70%).

---

## alternative

**bioRxiv / medRxiv preprint servers**

If revision is not feasible or if you wish to establish priority before addressing the major revisions, post to bioRxiv. The manuscript is complete, the data are deposited, and the limitations are already acknowledged. A preprint with a clear statement of the unresolved confounds (charge compensation, cleavage-state redistribution) will be useful to the community and will not prevent later journal submission. Many labs will cite and use the RIPUP protocol from the preprint alone. Consider adding a "Known Limitations" section to the preprint version that flags the two confounds explicitly.

**Proteomics** (Wiley)

A fallback if JPR or MCP desk-reject on scope grounds (unlikely, but possible if they view the work as incremental to Ryzhaya et al. 2025). Proteomics publishes methods papers with lower selectivity than JPR/MCP and would accept the manuscript with the major revisions addressed. Acceptance odds: **70–80%** post-revision, but this is a step down in venue prestige and audience reach.

**Methods in Molecular Biology / Springer Protocols**

If you wish to position RIPUP as a practical protocol for labs adopting Arg-C Ultra and TMT, a methods chapter or protocol paper in this series would be appropriate and would reach a different audience (bench researchers, not primarily methods developers). This is a lower-impact outlet but guarantees publication and high practical utility. Not recommended as a primary venue, but worth considering as a complementary publication once the journal paper is placed.

---

## Notes on Revision Priority

The editor's 12 required revisions are not equally load-bearing. **Focus first on these three:**

1. **Required Revision #1** (collision-energy confound): This is the make-or-break issue. If you can acquire matched-energy data or reframe the charge-compensation claim as a hypothesis, the "dark epigenome" finding becomes publishable as an observation with a mechanistic hypothesis, which is defensible. If you cannot, the claim must be substantially softened, and the paper's headline impact is reduced.

2. **Required Revision #3** (missed-cleavage confound in NAM quantitation): Stratifying the 112 Arg-C Ultra peptidoforms and repeating the contrasts on zero-missed-cleavage peptides is a bounded reanalysis that will either confirm or weaken the quantitative claim. If the sirtuin-target sites survive the restriction, you have a strong secondary contribution. If they don't, you must scale back the quantitative-performance claim.

3. **Required Revision #6** (dual-protease complementarity): Quantifying unique-to-Arg-C, unique-r-Chymotrypsin, and shared PTM sites is essential for justifying the dual-protease design. This is straightforward to do and will strengthen the paper substantially.

Revisions #4, #5, #8, #9 are transparency and consistency issues that do not change the science but are necessary for publication at a top venue.

---

## Bottom Line

**Current verdict:** This is a sound, useful methods paper with two unresolved confounds that prevent the strongest claims from being fully supported. It is *in scope* for In Silico as-is, but will be more competitive at JPR, MCP, or Anal. Chem. once the confounds are addressed.

**Realistic path:** Address Required Revisions #1, #3, and #6 (the science-bearing ones), then submit to MCP or JPR. Acceptance odds rise from ~50% (as-is) to ~65–70% post-revision. If revision is not feasible, post to bioRxiv and submit to In Silico; the public-record format of In Silico's reviews will actually serve you well by making the confounds and their resolution (or non-resolution) permanently visible to readers.