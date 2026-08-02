# Journal Recommendations

## As-is (current quality)
_No headline venue is realistic at the current quality — see Alternative._

## After required revisions
- **Bioinformatics**
  - Fit: Spatial transcriptomics methods and multimodal omics integration are core topics; the journal publishes solid incremental computational work with major-revision expectations. Post-revision with matched-input baselines and statistical tests, the scope and rigor profile match well.
  - Realism: If matched-input baselines are completed and ethics/code disclosed, realistic odds are 50–60%; the major revision verdict reflects fixable issues, not fundamental unsuitability. Private cohort and single-disease focus are acceptable here if reproducible.
- **Genome Biology**
  - Fit: Broad computational biology journal that emphasizes methodological rigor and multimodal integration. The modality-ladder design and spatial-structure focus fit well. Would require matched-input baselines to separate method from input contribution.
  - Realism: Acceptance odds rise to 45–55% after revision if baselines show method contribution persists; higher bar than Bioinformatics for novelty, but solid engineering and honest negative results are valued. Data restrictions must be transparent.
- **NAR Genomics and Bioinformatics**
  - Fit: Methods-first genomics journal with focus on computational tools and reproducibility. Multimodal spatial integration and self-supervised representation learning align with scope. Rewards rigor and transparency over novelty.
  - Realism: 50–60% post-revision odds if code is deposited with DOI and matched-input baselines resolve the confound. Less emphasis on breakthrough than Genome Biology, making the incremental-but-solid framing defensible here.

## Alternative outlets
- **F1000Research**
  - Fit: Open-access overlay journal publishing versioned manuscripts with post-publication peer review. Suited for reproducibility-focused work with complex data-access restrictions. Would accept detailed disclosure of private-data governance and reuse by other teams via contact.
  - Realism: 60–70% odds; lower editorial bar than traditional journals and transparent versioning fits the paper's honest-reporting strengths. Not a prestige venue, but appropriate for methods papers with reproducible code and clear limitations.
- **GigaScience**
  - Fit: Data, software, and methods journal with explicit acceptance of projects with restricted-access cohorts and complex pipelines. Spatial omics integration and graph-based representation learning fit editorial scope well.
  - Realism: 55–65% post-revision; the journal explicitly values detailed implementation and code release over novelty. Private data is less of a barrier if governance and contact mechanisms are clear.
- **Frontiers in Bioinformatics**
  - Fit: Broad-scope open-access journal accepting incremental computational methods and validation work. Spatial transcriptomics is in-scope. Reviews are transparent and often constructive rather than gatekeeping.
  - Realism: 65–75% post-revision if major-revision items are addressed; lower selectivity than Genome Biology or Bioinformatics, but solid editorial oversight. Not a high-prestige venue but reliable home for reproducible, well-reported methods.

## Notes
The paper cannot be published as-is at any major venue: the matched-input confound (baselines on M1 only, LATTICE on M1–M5), undefined statistics (Table 2 ± values with no paired tests), and MUS metric introduced at the declining-metrics point without positive controls are load-bearing issues the editor identifies correctly. The ethics blocker (IRB/consent undisclosed) is a mandatory compliance gate. All required fixes are tractable—re-running baselines on M2/M5 features is new computation, but statistical tests, code deposition, and ethics disclosure are on data already in hand. If matched-input baselines cannot be completed, the abstract/introduction claims of superiority over existing methods must be rewritten as 'LATTICE plus richer inputs versus method on M1 alone', narrowing appeal to methods-first venues but increasing honesty. The paper is currently strongest as a preprint with public reviews (e.g., In Silico itself, or F1000Research) until those foundational issues are resolved.