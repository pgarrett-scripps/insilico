# Citation Integrity Auditor

## Summary
I have examined the manuscript "LATTICE: Graph Self-Supervised Learning for Multimodal Spatial Omics Integration" for citation integrity. The manuscript contains 20 references in its bibliography. I detected triggers for three categories: (1) Reference resolvability, (2) Claim–citation support, and (3) Self-citation/citation inflation. I found several issues requiring attention, including unverifiable references for key methodological comparisons, potential self-citation concerns, and references that could not be verified through available tools.

## Categories checked
- Reference resolvability
- Claim–citation support
- Self-citation / citation inflation

**HARD gaps (blocking): 0** · SOFT gaps: 0 · unverifiable: 6

## Unverifiable (raise as questions)
- **[Reference resolvability] GraphST paper (Yahui Long et al., Nature Communications 2023)** — The manuscript makes specific claims about GraphST's methodology and performance (Table 2 comparison), but I could not verify the existence of this exact reference through available search tools. The searches for 'GraphST' and the specific title did not return the expected Nature Communications paper.
- **[Reference resolvability] STAGATE paper (Kangning Dong and Shihua Zhang, Nature Communications 2022)** — The specific title 'Deciphering spatial domains from spatially resolved transcriptomics with an adaptive graph attention auto-encoder' could not be verified through available search tools.
- **[Reference resolvability] SpaGCN paper (Jian Hu et al., Nature Methods 2021)** — The specific title 'Spagcn: Integrating gene expression, spatial location and histology to identify spatial domains and spatially variable genes by graph convolutional network' could not be verified through PubMed search.
- **[Reference resolvability] SIMO paper (Penghui Yang et al., Nature Communications 2025)** — The specific title 'Spatial integration of multi-omics single-cell data with simo' could not be verified through PubMed search.
- **[Reference resolvability] MaxFuse paper (Bokai Zhu and Zongming Ma, Nature Biotechnology 2024)** — The specific title 'Maxfuse enables data integration across weakly linked spatial and single-cell modalities' could not be verified through PubMed search.
- **[Claim–citation support] Methodological comparisons in Table 2** — Table 2 presents quantitative comparisons between LATTICE and methods from references [3], [5], [6], [7], and [9]. Without being able to verify these references exist as cited, I cannot confirm whether the performance claims attributed to these methods are accurate or supported by the cited works.

## Documented (for the record)
- **[Self-citation / citation inflation] SARSIM paper (Dwarampudi et al., bioRxiv 2026)** — This is a self-citation (first author Dwarampudi matches manuscript first author). The reference was verified through PubMed search (PMID: 41993479), confirming it exists on bioRxiv. However, it represents the authors' own prior work.
- **[Reference resolvability] Spatial transcriptomics foundational paper (Ståhl et al., Science 2016)** — Standard foundational reference, likely correct
- **[Reference resolvability] CUT&Tag paper (Kaya-Okur et al., Nature Communications 2019)** — Standard method reference
- **[Reference resolvability] Technical references [10]-[20] (PyTorch, PyTorch Geometric, etc.)** — Standard software and methodological references