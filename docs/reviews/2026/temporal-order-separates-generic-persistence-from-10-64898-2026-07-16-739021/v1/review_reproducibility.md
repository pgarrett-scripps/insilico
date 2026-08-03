# Reproducibility Reviewer

## Summary
The manuscript makes strong computational claims but fails to provide the code, computational environment, or explicit results-to-artifact mapping needed for independent reproduction. Data are well-deposited with DOIs, but the analysis workflow exists only as a promised 'peer-review package' and future software repository, with no versioned public code archive, container, or lockfile. Procedural detail is extensive but cannot be executed without the missing software artifacts.

## Strengths
- All primary datasets are deposited with working DOIs (Zenodo, Dryad, CORA) and clearly referenced.
- Methods section provides exceptional procedural detail: exact equations, bootstrap seeds, cohort definitions, matching parameters, and frozen analysis plans.
- Hierarchical bootstrap, simultaneous bands, lag-invariant cohorts, and analytical nulls are fully specified with numerical tolerances.

## Weaknesses
- No custom analysis code is available at a resolvable, versioned location (GitHub commit, Zenodo DOI, or similar). The 'peer-review package' is described as accompanying the appeal but not publicly deposited; the software repository is promised 'before publication' — both are unavailable now, making the workflow non-rerunnable. [HARD]
- No computational environment is captured: no conda environment file, Docker/Singularity container, requirements.txt, or pinned Python/package versions. The manuscript notes SLURM on Hummel-2 with H100 GPU but provides no environment specification. [HARD]
- No explicit mapping from figures/tables to the scripts and intermediate outputs that produce them. The 'figure-rendering code' is claimed in the peer-review package but that package is not publicly accessible. [HARD]
- The generative model fitting (linear active-memory and angular hidden-state) uses custom optimization objectives, parameter transforms, and simulation procedures that are described in prose but not embodied in inspectable, runnable code. [HARD]
- Track reconstruction depends on a 'Unique_ID' column in the MYO10-collagen data; the manuscript does not state whether this column is present in the public Zenodo deposit or was constructed by the authors, creating ambiguity about the exact input to the workflow. [SOFT]

## Questions
- Is the 'peer-review package' (workflow, tests, rendering code) currently deposited in a public archive with a DOI? If not, when and where will it be deposited?
- Can the authors provide a conda lockfile, Dockerfile, or equivalent environment capture for the Python/SLURM workflow?
- Will the command-line workflow be released at a versioned public URL (GitHub + Zenodo) with a commit hash referenced in the final manuscript?
- For the MYO10-collagen data: is the 'Unique_ID' column present in the Zenodo deposit (doi:10.5281/zenodo.11282716), or was it constructed during reanalysis? If constructed, what is the exact rule?