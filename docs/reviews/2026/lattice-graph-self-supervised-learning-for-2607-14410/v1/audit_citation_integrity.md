# Citation Integrity Auditor

## Summary
The manuscript LATTICE (arXiv:2607.14410v1) contains 20 numbered references across categories of reference resolvability, claim–citation support, and quotation fidelity. Of these, 16 references (80%) are fully resolvable to published works in mainstream journals and conferences; however, 4 references (20%) are unverifiable due to future dating or incomplete citation information. Most critically, reference [4] (SARSIM, Dwarampudi et al. 2026, bioRxiv) is a load-bearing dependency used to define modality blocks and evaluation constraints but lacks a DOI or preprint identifier and is dated 2026 (the manuscript's own date). Reference [17] (Space Ranger, 10x Genomics 2026) is similarly future-dated and used for RNA reference clustering. Reference [8] (SSpMosaic, Zhang et al. 2026) is incomplete and future-dated. Additionally, ReCAST is described as an internal engineering pipeline with no external publication. These gaps prevent independent verification of upstream preprocessing and evaluation methodology.

## Categories checked
- Reference resolvability
- Claim–citation support
- Quotation/number fidelity

**HARD gaps (blocking): 0** · SOFT gaps: 0 · unverifiable: 6

## Unverifiable (raise as questions)
- **[Reference resolvability] Dwarampudi et al. 2026 (SARSIM)** — Reference [4]: Dwarampudi et al. 2026, SARSIM, bioRxiv. Listed as 'bioRxiv, 2026' with no DOI or preprint identifier. This is a future-dated reference (manuscript dated July 2026, reference claims 2026 publication). This is a load-bearing dependency used to define M2–M3 modality blocks, upstream preprocessing, and evaluation constraints. Cannot verify existence or contents.
- **[Reference resolvability] Zhang et al. 2026 (SSpMosaic)** — Reference [8]: Zhang et al. 2026, SSpMosaic, *Cell Genomics* 6(4). Future-dated (2026). No article number or pages provided. Cannot verify.
- **[Reference resolvability] 10x Genomics 2026 (Space Ranger)** — Reference [17]: 10x Genomics 2026, Space Ranger. Future-dated (2026). URL provided but access date is 2026-05-06 (future). Cannot verify current availability.
- **[Claim–citation support] SARSIM integrates Visium with scMultiome to learn spatially coherent cell-to-spot mappings and project accessibility and motif activity into tissue space** — Claim attributed to reference [4] SARSIM. This is a central claim about upstream preprocessing. Reference [4] is dated 2026 (future) with no DOI. The manuscript states SARSIM is used to define M2–M3 modality blocks and provides 'overlap-gene constraints and clustering metadata during evaluation.' Cannot verify the method's actual contents or whether it performs as described.
- **[Claim–citation support] ReCAST performs preprocessing and harmonization** — ReCAST is described as 'an internal engineering pipeline' (Appendix F) with no external reference. Implementation details are in Appendix F but no published source is cited. Cannot independently verify.
- **[Claim–citation support] Masked reconstruction preserves modality-specific information** — Claim attributed to reference [12] Gutmann & Hyvärinen 2010 (NCE). The masked reconstruction objective (Eq. 6) is standard in self-supervised learning, but the specific citation to NCE is for the alignment loss, not reconstruction. The reconstruction approach is not explicitly attributed to a source.

## Documented (for the record)
- **[Reference resolvability] Ståhl et al. 2016 (Visium foundational paper)** — Reference [1]: Ståhl et al. 2016, *Science* 353(6294):78–82. Specific journal, volume, and pages provided; foundational Visium spatial transcriptomics paper.
- **[Reference resolvability] Kaya-Okur et al. 2019 (CUT&Tag)** — Reference [2]: Kaya-Okur et al. 2019, CUT&Tag, *Nature Communications* 10(1):1930. Specific journal, volume, and article number provided.
- **[Reference resolvability] Long et al. 2023 (GraphST)** — Reference [3]: Long et al. 2023, GraphST, *Nature Communications* 14(1):1155. Specific journal, volume, and article number provided.
- **[Reference resolvability] Dong & Zhang 2022 (STAGATE)** — Reference [5]: Dong & Zhang 2022, STAGATE, *Nature Communications* 13(1):1739. Specific journal, volume, and article number provided.
- **[Reference resolvability] Hu et al. 2021 (SpaGCN)** — Reference [6]: Hu et al. 2021, SpaGCN, *Nature Methods* 18(11):1342–1351. Specific journal, volume, and pages provided.
- **[Reference resolvability] Yang et al. 2025 (SIMO)** — Reference [7]: Yang et al. 2025, SIMO, *Nature Communications* 16(1):1265. Specific journal, volume, and article number provided.
- **[Reference resolvability] Zhu & Ma 2024 (MaxFuse)** — Reference [9]: Zhu & Ma 2024, MaxFuse, *Nature Biotechnology* 42(7):1036–1037. Specific journal, volume, and pages provided.
- **[Reference resolvability] Paszke et al. 2019 (PyTorch)** — Reference [10]: Paszke et al. 2019, PyTorch, *Advances in NeurIPS* 32. Standard reference to PyTorch library paper.
- **[Reference resolvability] Fey & Lenssen 2019 (PyTorch Geometric)** — Reference [11]: Fey & Lenssen 2019, PyTorch Geometric, arXiv:1903.02428. arXiv identifier provided.
- **[Reference resolvability] Gutmann & Hyvärinen 2010 (NCE)** — Reference [12]: Gutmann & Hyvärinen 2010, NCE, *AISTATS* pp. 297–304. Conference proceedings with page numbers.
- **[Reference resolvability] Loshchilov & Hutter 2017 (AdamW)** — Reference [13]: Loshchilov & Hutter 2017, AdamW, arXiv:1711.05101. arXiv identifier provided.
- **[Reference resolvability] 10x Genomics 2024 (Visium HD)** — Reference [14]: 10x Genomics 2024, Visium HD. URL provided; vendor documentation.
- **[Reference resolvability] 10x Genomics 2024 (Xenium)** — Reference [15]: 10x Genomics 2024, Xenium. URL provided; vendor documentation.
- **[Reference resolvability] Strehl & Ghosh 2002 (ARI/NMI)** — Reference [16]: Strehl & Ghosh 2002, ARI/NMI, *JMLR* 3(Dec):583–617. Specific journal, volume, and pages provided.
- **[Reference resolvability] Rousseeuw 1987 (Silhouette)** — Reference [18]: Rousseeuw 1987, Silhouette, *Computational & Applied Math* 20:53–65. Specific journal, volume, and pages provided.
- **[Reference resolvability] Traag, Waltman & Eck 2019 (Leiden)** — Reference [19]: Traag, Waltman & Eck 2019, Leiden, *Scientific Reports* 9(1):5233. Specific journal, volume, and article number provided.
- **[Reference resolvability] McInnes, Healy & Melville 2018 (UMAP)** — Reference [20]: McInnes, Healy & Melville 2018, UMAP, arXiv:1802.03426. arXiv identifier provided.
- **[Claim–citation support] Visium RNA captures broad transcriptional organization** — Claim attributed to reference [1] Ståhl et al. 2016. Foundational Visium paper; claim is standard characterization of the platform.
- **[Claim–citation support] Spatial ATAC and spatial CUT&Tag add section-level chromatin and histone-modification context** — Claim attributed to reference [2] Kaya-Okur et al. 2019. CUT&Tag paper describes histone modification profiling; spatial ATAC is standard assay.
- **[Claim–citation support] GraphST, STAGATE, and SpaGCN combine expression with spatial neighborhoods for domains and clustering** — Claim attributed to references [3], [5], [6]. All three are cited as spatial transcriptomics methods using graph-based clustering.
- **[Claim–citation support] Cross-modal alignment uses noise-contrastive estimation** — Claim attributed to reference [12] Gutmann & Hyvärinen 2010. NCE is correctly cited for the alignment loss (Eq. 8).
- **[Claim–citation support] Leiden clustering with resolution sweep** — Claim attributed to reference [19] Traag, Waltman & Eck 2019. Leiden is a standard clustering algorithm; reference is correct.
- **[Claim–citation support] Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI) for cluster comparison** — Claim attributed to reference [16] Strehl & Ghosh 2002. Standard reference for these metrics.
- **[Claim–citation support] UMAP for visualization** — Claim attributed to reference [20] McInnes et al. 2018. UMAP is correctly cited. Manuscript notes 'UMAP fallback to PCA if umap-learn is unavailable' (Appendix H).
- **[Quotation/number fidelity] Strehl & Ghosh 2002 ARI/NMI citation format and page numbers** — Reference [16]: Strehl & Ghosh 2002, Cluster ensembles—a knowledge reuse framework for combining multiple partitions, *Journal of Machine Learning Research*, 3(Dec):583–617. Citation format and page numbers match standard bibliographic records.
- **[Quotation/number fidelity] Traag, Waltman & Eck 2019 Leiden citation accuracy** — Reference [19]: Traag, Waltman & Eck 2019, From Louvain to Leiden: guaranteeing well-connected communities, *Scientific Reports*, 9(1):5233. Citation matches; search result confirms 5,153 citations.
- **[Quotation/number fidelity] McInnes, Healy & Melville 2018 UMAP arXiv identifier** — Reference [20]: McInnes, Healy & Melville 2018, UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction, arXiv:1802.03426. arXiv identifier is correct; search results confirm 12,947 citations.
- **[Quotation/number fidelity] Hyperparameter values (Appendix H)** — Specific values listed: k=6 for kNN, masking ratio ρ=0.15, temperature τ=0.1, loss weights λ₁=1.0, λ₂=0.5, λ₃=0.1. These are not attributed to external sources and appear to be author choices. No fidelity issues.