# Rigor & Overclaiming Reviewer

SCORE: 2  
CONFIDENCE: 4  

**Overall take.** This is a method-development paper whose central interpretive claims — that gigaseal preservation during retrieval links soma size to proteome yield, and that retrieval integrity predicts synaptic protein recovery — are not supported by the evidence presented. The sample size (n=3 for the headline correlation, n=12 total) is far too small for the correlational and clustering claims, and the paper's own data contradict the strongest version of its framework. The indiscriminate-collection strategy is a reasonable exploratory choice, but the manuscript overinterprets what is essentially a proof-of-concept demonstration.

**Strengths.** The authors are transparent about including all retrieval outcomes rather than cherry-picking high-quality samples. The framework for categorizing retrieval quality (gigaseal preserved/lost/never formed) is conceptually useful and clearly presented. The decision to deposit videos and raw data is commendable for reproducibility.

**Weaknesses.**

**Load-bearing claim 1: "Protein identifications correlated with the log-transformed capacitance (F = 1577, p < 0.05, adjusted R² = 0.998, n = 3)"**  
This is the paper's central quantitative claim, and it rests on three data points. With n=3, any monotonic relationship will produce a near-perfect correlation; the adjusted R² of 0.998 is a statistical artifact of overfitting, not evidence of a real relationship. The p-value is meaningless at this sample size. The claim as worded — "linking soma size to proteome yield" — is HARD unsupported. What would settle it: the same correlation reported on a dataset of at least 10–15 gigaseal-preserved retrievals, with confidence intervals on the slope. As it stands, this is a hypothesis-generating observation, not a finding.

**Load-bearing claim 2: "Preservation of neuronal spiking during relocation tended to be associated with broader synaptic enrichment and recovery of transmembrane proteins."**  
This claim (from the abstract) is contradicted by the authors' own data. Neuron #7, which showed reduced spike amplitude (compromised spiking), had comparable SynGO enrichment to neuron #4 (the "ideal" retrieval). Neuron #6, with the worst spiking, had the fewest enriched terms — but it was also the smallest neuron by capacitance, so size and spiking integrity are confounded. The claim that spiking preservation *per se* drives synaptic enrichment is not isolable from soma size. Moreover, the PCA (Figure 6A) shows neuron #6 clustering with no-gigaseal neurons, but neuron #7 — with compromised spiking — does not cluster with the torn neurons. The data do not support the directional claim. SOFT at best; the abstract wording overstates what the results show.

**Load-bearing claim 3: "Retrieval loss decouples proteomic measurements from electrophysiology recordings."**  
This is the paper's most defensible claim, but it is also the most obvious. Of course a torn neuron yields fewer proteins than an intact one. The more interesting claim — that *in situ* recordings cannot predict proteome recovery even for intact retrievals — is supported by the lack of correlation in Figure 5C-D, but again n=6 with a null result is weak evidence. The claim as worded is SOFT: it is plausible and consistent with the data, but the sample size cannot distinguish "no relationship" from "relationship too weak to detect."

**Sweep.**

- The abstract claims "thousands of proteins" were detected, but the range across samples is 1,400–2,300; "thousands" is technically true but misleading for the lower end, and the torn neurons produced far fewer.
- The claim that "neurons with gigaseals generally retained broader sets of ion channel subunits" (Figure 7 legend) is contradicted by the authors' own text: "in some cases, more transmembrane proteins could be found among neurons that lost the whole-cell configuration during retrieval than neurons with continuous whole-cell access."
- The SynGO enrichment analysis is presented as evidence of "biological insight," but enrichment of synaptic terms in a soma retrieved from a synapse-dense region like mPFC could reflect contamination from adherent tissue rather than genuine compartment-specific recovery — the authors do not address this confound.
- The paper uses "tended to be associated" in the abstract but "demonstrate" in the conclusions for the same finding; the conclusions outrun the results.
- The claim that capacitance "reflects soma size" is standard electrophysiology, but the paper does not validate this against morphological measurements (e.g., imaging), which would be straightforward to do.
- The PCA clustering (Figure 6A) is presented as meaningful separation, but with n=12 and no statistical test of cluster separation, this is descriptive at best.
- The paper does not report how many neurons were attempted and failed to yield any proteome — the denominator for the 10/12 retrieval success rate is unclear.
- The framework's claim to be "a framework for interpreting patch-SCP outcomes" is reasonable, but the paper does not provide any validation that the framework improves interpretation over simply reporting protein counts — a comparison against a naive approach is missing.

**Questions.**

1. Can the authors report the capacitance–protein identification correlation on a larger cohort (n ≥ 10) of gigaseal-preserved retrievals, with confidence intervals?
2. How do the authors distinguish genuine synaptic protein recovery from contamination by adherent tissue in a synapse-dense region like mPFC?
3. What was the total number of patch attempts, and how many yielded no detectable proteome at all?