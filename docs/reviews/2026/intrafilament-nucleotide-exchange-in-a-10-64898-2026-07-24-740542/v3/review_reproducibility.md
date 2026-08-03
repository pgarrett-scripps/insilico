# Reproducibility Reviewer

## Summary
The manuscript's central claims — intrafilament nucleotide exchange in MreB filaments, ATP-hydrolysis-independent polymerization, and ADP-triggered depolymerization — rely on quantitative live imaging, mutagenesis, and a stochastic Monte Carlo model. However, none of the load-bearing datasets (TIRF/HS-AFM movies, FRAP curves, ATPase kinetics, in vivo time-lapses) or custom analysis code (Monte Carlo simulations, SOAX/TSOAX tracking scripts, FRAP quantification) are deposited; they are offered only 'on request' or 'upon publication'. This makes independent reproduction impossible at present. Procedural detail is strong for biochemistry but incomplete for computational steps (no environment capture, no random seeds, no versioned repository).

## Strengths
- Experimental design is thorough with orthogonal methods (TIRF, HS-AFM, TEM, QCM-D, anisotropy, in vivo) and well-characterized mutants.
- Methods section provides detailed protocols for protein purification, lipid preparation, and imaging buffer compositions, enabling wet-lab replication.
- Monte Carlo model parameters are explicitly listed in Figure 4D legend and Supplementary Information, allowing theoretical replication if code were available.

## Weaknesses
- Load-bearing empirical data (all TIRF/HS-AFM movies, FRAP recovery curves, ATPase time courses, in vivo CCCP time-lapses) are not deposited in a public repository; the manuscript states they 'will be deposited on Zenodo after publication and are available from the corresponding authors upon request', which does not meet reproducibility standards for primary evidence.
- Custom computational artifacts — the stochastic Monte Carlo simulation code, SOAX/TSOAX MATLAB scripts for filament tracking, FRAP analysis pipeline, and anisotropy fitting routines — are not versioned or archived; no repository, commit hash, or DOI is provided, and the environment (MATLAB/Igor Pro/PRISM versions, dependencies) is not captured.
- Several methods cite 'performed as previously described' (e.g., TEM, liposome preparation, HS-AFM cantilever fabrication) without confirming that the cited references contain the exact protocol used; critical parameters such as HS-AFM scan force, TIRF laser power/exposure, and SOAX/TSOAX threshold settings are omitted.
- Monte Carlo simulations lack random seed reporting or a statement on seed averaging, making stochastic results non-reproducible even if code were shared.
- FRAP experiments use TFLime with a caveat that high-intensity bleaching may irreversibly trap the fluorogen (Fig 3E), yet this potential artifact is not controlled for with an alternative probe or lower-power validation; the conclusion of 'no monomer turnover' rests on this single assay.

## Questions
- Will the authors deposit all raw imaging data (TIRF/HS-AFM movies, FRAP stacks, in vivo time-lapses) and processed datasets with persistent DOIs prior to publication?
- Will the Monte Carlo simulation code, SOAX/TSOAX tracking scripts, and FRAP/anisotropy analysis pipelines be placed in a versioned public repository (e.g., GitHub + Zenodo) with a documented computational environment?
- Can the authors provide the exact SOAX/TSOAX parameter files (thresholds, smoothing, linking criteria) used for filament detection and tracking in Figures 1, 2, 3, 4?
- For the 'performed as previously described' methods, can the authors confirm that the cited references contain the identical protocol, or supply a protocols.io entry with the exact steps used here?