# Reproducibility Reviewer

SCORE: 3  
CONFIDENCE: 4

**Summary**  
This manuscript presents a time-resolved TurboID proximity-labeling proteomics study of Smoothened (Smo) in NIH3T3 cells, identifying Git1 as a novel regulator of Grk2-mediated Smo phosphorylation in the primary cilium. The authors provide a compelling biological narrative supported by multiple orthogonal assays (immunofluorescence, Western blot, CRISPR knockout, primary neuron culture). The proteomics dataset is a potentially valuable community resource, but the manuscript currently lacks the full reproducibility infrastructure needed for an independent group to rerun the analysis end-to-end.

**Strengths**  
1. The time-resolved experimental design (15 min, 1 h, 4 h Shh stimulation) is well-conceived for capturing transient Smo interactions.  
2. The authors validated their Smo-TurboID cell line against multiple criteria (no self-activation, physiological expression, normal cilia) before proceeding.  
3. The functional follow-up on Git1 is thorough, including rescue experiments with ciliary-targeted Grk2.

**Weaknesses (load-bearing)**  

**1. Mass spectrometry raw data and search results are not deposited.** The central claim of the paper — that Git1 is a Smo-associated protein identified by proximity labeling — rests entirely on the proteomics dataset. The manuscript states that data will be available “upon publication” but provides no accession number, repository link, or supplementary file. For a paper whose primary contribution is a proteomic resource, this is a HARD reproducibility failure. An independent group cannot verify the Git1 peptide evidence, the TMT reporter ion intensities, or the normalization steps without the raw files (e.g., .raw/.d files) and the search output (e.g., .xml or .tsv from IP2/ProLuCID). The authors must deposit raw data (e.g., PRIDE/ProteomeXchange) and processed tables (Table S1–S5) with a working accession before this can be considered reproducible.

**2. The normalization and differential-expression pipeline is described in prose but not executable.** The methods state that “sample loading and trimmed mean of M values (TMM) normalization were performed” and that “Empirical Bayes moderation” was applied via the `eBayes` package in R. However, no code, R script, or analysis notebook is provided. The exact order of operations (global scaling → TMM → eBayes), the specific TMM parameters (e.g., trim fraction), and the contrast definitions (e.g., how “no Shh + biotin” vs. “no Shh − biotin” was modeled) are not fully specified. An independent group could not reproduce the volcano plots, heatmaps, or the 1.5-fold/p<0.05 thresholding without this code. This is a HARD gap: the analysis is load-bearing for every downstream conclusion.

**3. The biotin-labeling time course and Shh treatment windows are not fully reconciled.** The proteomics workflow (Fig. 2A) shows 15 min biotin labeling at the end of Shh treatment, but the text states “15 min, 1 h, and 4 h” Shh stimulation with biotin added for the final 15 min. The 15-min Shh time point therefore has biotin added simultaneously with Shh (0–15 min), which is a different condition from the others (where biotin is added after Shh has already acted). This is not inherently wrong, but the manuscript does not state this explicitly, and it affects interpretation of the “early” interactors. The authors should clarify whether biotin was added at t=0 for the 15-min condition or at t=0–15 min after Shh pre-incubation. This is a SOFT issue if clarified, but as written it is ambiguous enough to affect replication.

**Sweep (one sentence each)**  

- The manuscript does not state the version of the UniProt mouse proteome (UP000000589) used for the search, nor the version of ProLuCID, DTASelect2, or Census2 — all are required for exact reproduction.  
- The TMT 6-plex channel-to-condition mapping (126–131) is described in Fig. S2A but not in the methods; a replicator must infer which channel corresponds to which condition.  
- The Git1 shRNA sequences are not provided; only “shRNA against Git1” is mentioned, with no target sequence or validated clone identifier.  
- The lentiviral expression constructs (FUGW backbone) are described but no Addgene/plasmid accession is given for the Git1-YFP or Grk2-V5-DArl13b constructs.  
- The “selected cell colony” for Smo-TurboID is described as one of 50 screened, but the screening criteria (e.g., exact Smo expression fold-change threshold) are not quantified.  
- The statistical test for the proteomics (eBayes) is stated, but the multiple-comparison correction method (e.g., BH-FDR) is not named.  
- The mass spectrometry instrument model (e.g., Orbitrap Fusion, Q-Exactive) is not stated, only “nano-LC” and “mass spectrometer” — this affects feasibility of replication on similar hardware.  
- The paper does not state whether the three biological replicates were processed in the same TMT batch or across batches; batch effects are not discussed.

**Questions**  

1. Can the authors provide a ProteomeXchange/PRIDE accession for the raw mass spectrometry files and the IP2 search output, active at the time of review?  
2. Will the R code for normalization and differential expression be deposited (e.g., GitHub with a release tag or Zenodo DOI), including the exact TMM parameters and eBayes contrasts?  
3. For the 15-min Shh time point, was biotin added simultaneously with Shh, or after 15 min of Shh pre-incubation? Please state this explicitly in the methods.  
4. What is the target sequence of the Git1 shRNA used in both NIH3T3 and GNP experiments?