# Novelty & Contribution Reviewer

## Summary
The manuscript introduces a genuinely novel analytical framework that decomposes cell migration trajectories into motility, generic serial-order persistence, and cue-aligned commitment using an exact order-null reference. The method is mathematically sound, the reanalyses of public datasets yield new biological insights not accessible to conventional metrics, and the limitations are transparently acknowledged. This is a significant methodological contribution with demonstrated biological utility.

## Strengths
- The analytical order-null (exact expectation under uniform permutation preserving step content, static polarity, and endpoint) is a novel and elegant alternative to Monte Carlo shuffling, enabling exact decomposition identities that close to machine precision.
- The framework cleanly separates three biologically distinct questions — how much a cell moves, whether it persists generically, and whether that persistence aligns with a cue — and demonstrates this separation across matrix, geometric, and metabolic perturbations.
- The workflow is fully documented, reproducible, and accepts standard x-y tracking tables, with audit files for identifier reuse, missing frames, and unit inconsistencies.

## Weaknesses
- The discovery MYO10–collagen experiment has only three biological repeats (R1–R3), with R3 noted as disproportionately large and phenotypically distinct; while hierarchical bootstrap and leave-one-FOV-out analyses mitigate this, the highest-level replication remains minimal and the operational independence of repeats could not be verified beyond public metadata.
- The PFKL chemotaxis reanalysis lacks biological-replicate labels in the deposited tracking tables, forcing track-level inference; the five perturbation series come from a single source study and are correctly framed as concordant mechanistic comparisons rather than independent replications, but this limits generalizability.
- Cross-system comparisons (HUVEC, MDA-MB-231, MDCK) confound cell type, species, substrate, imaging, and tracking differences; the authors correctly treat these as descriptive demonstrations of transportability rather than controlled comparisons, but the framing occasionally blurs this distinction.

## Questions
- For the MYO10–collagen analysis: could the trajectory reconstruction using Unique_ID be independently validated against a subset of raw images to confirm that the corrected identities correspond to biologically distinct cells?
- For the PFKL non-inferiority test: was the 0.10-SD margin justified a priori (e.g., by a minimal biologically relevant effect size from prior literature), or was it chosen post hoc based on the observed variability?
- In the generative model falsification: the linear active-memory model was fitted only to one- and two-step transitions; would fitting to the full lag-resolved VACF or sequence-excess curve (even if overparameterized) change the conclusion that stationary local models cannot reproduce the long-lag hierarchy?