# Venue Recommendations for dnoise Manuscript

## as_is
**In Silico** (the target venue)

This manuscript is ready for In Silico *as is*. The editor's verdict is "minor," and In Silico explicitly accepts work at this readiness level. The core contribution is sound, the evidence supports the central claims, and the reproducibility record (public code, public data, round-trip validation) meets the venue's standards for checkability. The required revisions are text-level clarifications and deposited scripts—not new experiments or reanalysis. The public review process is actually well-suited to this work: the required revisions are specific and fixable, and the authors' honest scoping of limitations (Section 3.7) will read well in a permanent, public review record. Submit with the 10 required revisions and 7 minor suggestions addressed.

---

## after_revision

**Journal of Proteome Research**

Once the required revisions are complete, this becomes a strong fit for JPR. The manuscript is a methodological contribution to a widely-used instrument platform (timsTOF), with rigorous benchmarking on a defined standard (Generation Beta), validation in both DDA and DIA modes, and open-source software release. JPR's audience includes method developers and practitioners who need exactly this kind of tool paper: honest about scope, transparent about tradeoffs (MS1-only vs. MS/MS filtering), and grounded in real acquisition modes. The revisions will tighten the claims to match the evidence, which is what JPR reviewers expect. Acceptance odds: moderate-to-good (60–70%), conditional on clean execution of the revisions.

**Molecular & Cellular Proteomics**

MCP is another strong fit post-revision. It publishes both methods and applications in proteomics, with a particular interest in ion-mobility and timsTOF work (several cited references are MCP papers). The benchmarking design (three-species mixture, replicated, two gradients, two modes) is the kind of disciplined validation MCP values. The software release and public data deposition align with MCP's reproducibility standards. The revisions will make the scope and limitations even clearer, which strengthens rather than weakens the submission. Acceptance odds: moderate (55–65%).

**Analytical Chemistry**

AC publishes analytical methods and instrumentation work. A denoising tool for a major commercial platform, validated on real samples with quantitative outcomes, fits AC's scope well. The manuscript's emphasis on data reduction (storage, transfer, archival) and the runtime/memory characterization appeal to AC's audience of method developers and facility managers. The revisions will make the claims more precise without changing the substance. Acceptance odds: moderate (50–60%).

---

## alternative

**bioRxiv** (preprint server)

If the authors want rapid dissemination before journal review, or if journal submission is delayed, deposit on bioRxiv with the required revisions applied. The work is solid enough to stand as a preprint, and the open-source software + public data mean readers can evaluate it independently. Many timsTOF users will find it via bioRxiv before it appears in a journal, and the tool's utility is not contingent on journal acceptance. This is a low-risk option that does not preclude later journal submission.

**Bioinformatics** (or **Briefings in Bioinformatics**)

If the authors want a faster, slightly lower-barrier journal path, Bioinformatics publishes software and computational methods in life sciences. The manuscript would need to be reframed slightly as a computational tool paper rather than a proteomics benchmarking study, but the core contribution fits. Acceptance odds are moderate (50–60%) because Bioinformatics is competitive, but the work is solid enough to have a real chance. This is a reasonable fallback if JPR or MCP reject.

**Proteomics** (Wiley journal)

A specialty journal with a narrower but highly engaged audience. Proteomics publishes methods, tools, and applications. The timsTOF focus and the honest scoping of limitations would appeal to the journal's readership. Acceptance odds are moderate-to-good (55–70%), but the journal is smaller and slower than JPR or MCP. Use as a fallback if the larger venues decline.

---

## Notes on Venue Strategy

- **Target sequence:** Submit to In Silico now (as is), then simultaneously or sequentially to JPR and MCP after revisions are complete. Both are realistic targets post-revision, and the 10 required fixes are straightforward.
- **Why not Nature Methods or similar?** The work is solid and useful, but it is a single-instrument, single-lab benchmarking study of a denoising tool for an existing platform. Nature Methods publishes broader methodological innovations; this is more specialized. The authors' honest scoping (Section 3.7) actually argues against overstating the scope to reach a top-tier venue.
- **Why In Silico is a good fit:** The public review process suits a tool paper. The required revisions will be visible to readers, and the authors' candor about limitations will be rewarded rather than penalized. The venue's emphasis on checkability (code, data, reproducibility) is exactly what this manuscript delivers.
- **Timing:** The Zenodo archive and GitHub repository are already in place. The analysis scripts need to be deposited (Required Revision 4), which is the main blocker for full reproducibility. Once that is done, the manuscript is ready for submission anywhere in the "after_revision" bucket.