# Reproducibility Reviewer

## Summary
The manuscript is largely reproducible: the cytosol isolation, infection, ELISA, Western blot, and MS acquisition procedures are specified in unusual detail, and the raw MS data is deposited at MassIVE with reviewer credentials and a resolvable URL. The main gaps are the absence of deposited code for the downstream proteomics analysis and an internal inconsistency about histone H3 in the proteomics results. Both are addressable but require revision.

## Strengths
- MS acquisition and search parameters are specified in unusual detail (PASEF settings, ion mobility range, collision energy ramp, precursor thresholds, FDR criteria), making the acquisition reproducible.
- Raw MS data is deposited at MassIVE (PXD069795) with reviewer credentials and a resolvable URL.
- The cytosol isolation procedure is specified end-to-end (digitonin concentration, buffer composition, times, speeds, filtration, MWCO), with the organelle-purity check (LAMP-2 absence) described.

## Weaknesses
- No code for the downstream proteomics analysis (HARD). The normalization (NSAF log2, scaling, correlation-slope normalization), missForest imputation, PCA, and heatmap are described in prose with citations, but no R script is deposited at a resolvable, versioned location. The prose is detailed enough that reconstruction is feasible, but the exact implementation — particularly the "normalization by correlation slope" (ref 30) and the imputation rule — would require inference. Depositing the analysis script would remove this ambiguity.
- Internal inconsistency about histone H3. The text states H3 "was regularly present in WT- but not DSLO-infected cytosol (Supp. Table 1)," then says the Western blot showing H3 in both WT- and ΔSLO-infected cytosol is "consistent with our findings in our proteomics analysis." These statements contradict each other. The load-bearing claim (histones in both infected types) rests on the Western blot, but the Supp. Table 1 entry needs reconciliation — a replicator needs to know which result is correct.
- No random seed stated for missForest imputation; the imputation is stochastic, so the quantitative comparisons in Fig. 3A cannot be reproduced exactly (the presence/absence claims don't depend on it).
- The imputation rule "values below the least expressed protein were imputed for proteins consistently absent in a sample type" doesn't quantify "consistently absent" (absent in all replicates? a majority?), which affects which proteins are imputed.
- No environment capture (lockfile, container) for the R analysis; package versions are cited for missForest and heatmaply but not for the base R environment or other dependencies.

## Questions
- Will the R analysis script be deposited at a resolvable, versioned location, with package versions?
- Was a random seed used for missForest imputation, or was imputation averaged over multiple seeds?