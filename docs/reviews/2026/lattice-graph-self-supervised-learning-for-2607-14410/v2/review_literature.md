# Related-Work & Citations Reviewer

## Summary
The manuscript's related work section has serious citation hygiene issues and omits directly competing methods. While it appropriately cites foundational spatial transcriptomics papers, it fails to reference several recent multimodal spatial integration methods that directly compete with LATTICE's claims. The self-citation to SARSIM is appropriate given the methodological dependency, but the overall citation record undermines the novelty positioning.

## Strengths
- Properly cites foundational spatial transcriptomics methods (Ståhl et al. 2016) and key epigenomic techniques (CUT&Tag).
- Appropriately references the authors' own SARSIM framework for spatially anchored regulatory inference.
- Includes relevant graph neural network frameworks (PyTorch Geometric) and self-supervised learning foundations.

## Weaknesses
- Load-bearing claim 1: LATTICE is novel in combining graph self-supervision with multimodal spatial omics integration. The manuscript claims 'existing approaches often treat one aspect of the problem in isolation' and positions LATTICE as filling this gap. However, my search reveals multiple recent methods addressing multimodal spatial integration that are not cited: 'Multimodal spatial omics: From data acquisition to computational integration' (Isik et al., Patterns 2026), 'Riemannian metric learning for alignment of spatial multiomics' (Halmos et al., Bioinformatics 2026), and 'SpaMode: A Broadly Applicable Framework for Deciphering Spatial Multi-Omics Using Multimodal Mixture of Disentangled Experts' (Zheng et al., Advanced Science 2026). These directly compete with LATTICE's claimed novelty, and their omission constitutes a HARD citation defect that inflates the perceived contribution.
- Load-bearing claim 2: The comparison baseline is comprehensive. The manuscript compares against GraphST, STAGATE, SpaGCN, SIMO, and MaxFuse, but my searches could not verify the specific citations for GraphST and STAGATE in the reference list (though they may exist in the full manuscript). More importantly, it omits 'MOSAIK: Multi-Origin Spatial Transcriptomics Analysis and Integration Kit' (2025) and 'SAGE-FM: A lightweight and interpretable spatial transcriptomics foundation model' (2026), which represent directly competing graph-based approaches for spatial transcriptomics. This selective comparison creates a misleading impression of LATTICE's relative performance.
- No DOI or PubMed IDs are provided for most references, making verification difficult (SOFT hygiene issue).
- The related work section acknowledges competing methods but characterizes them as 'typically emphasizing RNA with limited multimodal side information' without providing citations to support this characterization.
- The manuscript would benefit from citing recent reviews like 'Spatial biology in cancer epigenetics' (Crespo-García et al., Molecular Oncology 2026) to situate the work in the broader field.
- The claim that 'Graph self-supervised learning is well developed for attributed graphs but is still used predominantly in single- or weakly multimodal settings' lacks specific citations to support this characterization of the field's limitations.

## Questions
- Please provide the full citations for GraphST and STAGATE that appear in the reference list but were truncated in the manuscript excerpt.
- Could you clarify why methods like MOSAIK (2025) and SAGE-FM (2026) were not included in the comparison, given their direct relevance to graph-based spatial transcriptomics analysis?