# Methods Completeness & Reagent Traceability Auditor

## Summary
The manuscript is a computational reanalysis of public cell migration tracking datasets. Its methods are entirely computational: trajectory reconstruction, temporal-order analysis (sequence excess, order-null), and generative modeling (linear active-memory model, angular hidden-state model). No wet-lab experiments are performed; cell lines, chemicals, and imaging protocols are referenced from original studies. The audit therefore focuses on the computational methods and cross-cutting reproducibility items.

## Categories checked
- Computational/ML/modeling
- Cross-cutting

**HARD gaps (blocking): 5** · SOFT gaps: 0 · unverifiable: 0

## HARD gaps — reproduction blockers
- **[Computational/ML/modeling] Training procedure (optimizer/schedule/early-stopping)** — Manuscript states: 'Sixteen FOV-bootstrap models were optimized simultaneously. The objective was residual-transition loss plus 0.5 times the flow-transition loss and a small quadratic raw-parameter penalty.' No optimizer (e.g., Adam, SGD), learning rate, number of epochs, or early-stopping criteria are specified for the generative model fitting (Eqs 17-26).
- **[Computational/ML/modeling] Library versions** — Manuscript mentions 'software versions' are written to the result archive but does not list key library versions (e.g., Python, NumPy, SciPy, PyTorch/TensorFlow, pandas) in the text.
- **[Computational/ML/modeling] Code availability (persistent identifier)** — Manuscript states: 'A DOI-minted public software and results repository will be deposited before publication.' No current DOI or persistent link is provided for the custom analysis workflow; only an accompanying peer-review package is referenced.
- **[Computational/ML/modeling] Hyperparameters (complete)** — Some hyperparameters are given (Student-t ν=5, penalty weight 0.5, tanh/softplus transforms, partial-autocorrelation parameterization), but optimizer hyperparameters (learning rate, batch size, etc.) are absent.
- **[Cross-cutting] Software, tool, and instrument versions** — Manuscript does not report versions of Python, key analysis libraries, or computational tools used in the main text. It only notes that versions are recorded in the workflow archive.

## Documented (for the record)
- **[Cross-cutting] Sample size n with replicate definition** — Manuscript provides trajectory counts (e.g., 48,134), FOV counts (117), biological repeats (3), and clearly distinguishes hierarchical levels (track → FOV → repeat) for each dataset.
- **[Cross-cutting] Named statistical test and error bar definition** — Manuscript specifies hierarchical bootstrap, simultaneous confidence bands (max-t), HC3 robust intervals, propensity matching, overlap weighting, and non-inferiority testing. Error bars are described as standard errors across repeats, hierarchical 95% intervals, and simultaneous 95% bands.
- **[Cross-cutting] Data availability statement** — DOIs provided for all datasets: MYO10-collagen (10.5281/zenodo.11282716), TrackMate archives (10.5281/zenodo.4959169), haptotaxis (10.34810/data2489), PFKL chemotaxis (10.5061/dryad.6m905qgfp).
- **[Cross-cutting] Code availability** — Manuscript states code is in the accompanying peer-review package and a DOI-minted repository will be deposited before publication. Availability is declared but not yet persistently identified.