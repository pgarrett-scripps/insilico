# Related-Work & Citations Reviewer

## Summary
The manuscript presents LATTICE with a generally well-structured related-work section that appropriately positions the work against foundational spatial transcriptomics and multimodal integration methods. However, there are critical reproducibility and citation hygiene issues that require resolution before publication. Most significantly, the pipeline depends on two insufficiently documented components: SARSIM [4], cited as a future-dated preprint (2026) with no verifiable identifier, and ReCAST, described as an internal engineering pipeline without published reference or detailed methodology. Additionally, multiple references contain future access dates (2026), masked reconstruction lacks proper foundational citations, and cross-modal alignment is attributed only to a generic 2010 NCE paper rather than modern multimodal contrastive learning work. Recent directly relevant papers on multimodal spatial omics (2025–2026) appear to be missing from the literature review. While the paper's methodological contribution is sound and baseline comparisons are transparent, these citation and reproducibility issues must be resolved.

## Strengths
- Clear positioning against baselines (GraphST, STAGATE, SpaGCN, SIMO, MaxFuse) with explicit quantitative comparisons in Table 2, demonstrating transparency and fairness in evaluation.
- Appropriate scope acknowledgment that existing spatial methods emphasize RNA with limited multimodal information, and that single-cell spatial integration methods yield maps or fused views rather than unified spot-level encoders.
- Honest modular framing acknowledging that LATTICE is compatible with alternative upstream pipelines beyond SARSIM and ReCAST, showing awareness of dependencies.
- Self-supervised learning grounding through references to contrastive learning (NCE [12]) is appropriate for the domain.

## Weaknesses
- SARSIM [4] is cited as a preprint with a future date (2026) and no verifiable arXiv or bioRxiv identifier, yet it is load-bearing for generating projected scMultiome RNA and ATAC blocks (M2–M3) that are critical to the pipeline, raising severe reproducibility concerns.
- ReCAST is described as an internal engineering pipeline with no external reference or published paper, yet it generates spatial ATAC and spatial CUT&Tag blocks (M4–M5) that are essential inputs to LATTICE, making reproduction impossible without detailed methodology.
- Masked reconstruction objective in Section 3.3 lacks citation to foundational masked autoencoder work (e.g., He et al. MAE or BERT-style masking), despite being a core component of the self-supervised learning framework.
- Cross-modal alignment objective cites only NCE [12] from 2010, which is a generic contrastive principle rather than a specific multimodal alignment method; modern contrastive learning work (CLIP, SimCLR, MoCo) is not cited.
- Multiple references contain future access dates (2026-05-06) for references [14], [15], and [17], which is impossible and indicates placeholder or erroneous entries.
- Reference [4] (SARSIM) lacks a DOI or arXiv ID and uses a future year (2026), making it unverifiable as a real preprint.
- Recent multimodal spatial omics papers from 2025–2026 (arXiv:2601.12381, arXiv:2508.00969, arXiv:2511.11730) do not appear to be cited, suggesting incomplete literature coverage of directly competing work.
- Table 2 baseline comparisons do not specify which modality levels (M1–M5) were used for each baseline or whether baseline-specific hyperparameter tuning was performed, making fairness of comparison unclear.
- Theoretical analysis in Appendix I presents informal lemmas and theorems without formal statements or citations to standard results in spectral graph theory, conflating novel and established results.

## Questions
- Can you provide the actual arXiv or bioRxiv identifier for SARSIM [4]? If it is unpublished work by your group, will you commit to releasing it alongside LATTICE or provide sufficient methodological detail in the appendix for readers to reproduce the projected scMultiome block generation?
- Will the ReCAST pipeline be released as open-source code? If not, can you provide a detailed methods section in the appendix describing the harmonization and quality-control steps used to generate the spatial ATAC and spatial CUT&Tag blocks?
- For Table 2, can you provide a supplementary table showing which modality levels (M1–M5) were used for each baseline method and whether any baseline-specific hyperparameter tuning was performed?
- Which prior work on masked autoencoders or masked language models inspired your masked reconstruction objective in Section 3.3? Please cite the specific foundational paper(s).
- Beyond NCE [12], are there specific prior works on cross-modal contrastive learning or multimodal alignment (e.g., CLIP, SimCLR, MoCo) that informed your cross-modal alignment objective?
- Have you reviewed the recent papers on multimodal spatial omics published in 2025–2026 (e.g., arXiv:2601.12381, arXiv:2508.00969, arXiv:2511.11730)? If so, how does LATTICE compare to or differ from these approaches?
- Can you correct the future access dates in references [14], [15], and [17], and provide the correct preprint identifier and publication year for reference [4]?
- For the theoretical analysis in Appendix I, can you either cite the standard results in spectral graph theory (e.g., Chung's book or recent GNN surveys) or move the informal sketches to a discussion section rather than presenting them as formal lemmas?