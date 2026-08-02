# Ethics & Compliance Reviewer

## Summary
This manuscript presents a computational study comparing different scoring rules for training machine-learned weather forecast models. No human subjects, animals, clinical interventions, dual-use biosafety risks, or secondary/sensitive data are involved. The work is purely computational, using publicly available ERA5 reanalysis data and open-source frameworks. Funding sources are disclosed (Gauss Centre for Supercomputing, EuroHPC Joint Undertaking). No competing interests statement is provided, but the authors are from ECMWF and appear to be developing the Anemoi framework they use; this relationship should be explicitly declared. No IRB, ethics committee, or animal-welfare approvals are needed. Code and data availability are not explicitly addressed, which is a soft transparency issue for reproducibility but not a compliance barrier. Overall, no hard ethical or compliance violations are evident.

## Strengths
- Funding sources are clearly acknowledged: Gauss Centre for Supercomputing and EuroHPC Joint Undertaking are named with specific computing resources (JUPITER supercomputer at JSC).
- The work uses only publicly available data (ERA5 reanalysis, 1979–2020) with no privacy, consent, or human-subjects concerns.
- The study is purely computational and methodological, with no clinical, animal, or dual-use biosafety triggers.
- Authors acknowledge contributors to the Anemoi framework, showing transparency about collaborative development.

## Weaknesses
- No explicit declaration of competing interests or conflicts of interest is provided. The authors appear to be affiliated with ECMWF and are developing/using the Anemoi framework (https://github.com/ecmwf/anemoi-core), which is central to the experiments; this relationship should be declared as present or absent.
- Code and data availability are not addressed. While ERA5 is public, the trained models, custom scoring-rule implementations, and experimental configurations are not stated to be deposited or made available, limiting reproducibility and transparency.

## Questions
- Do the authors have any competing interests, financial or otherwise, related to the Anemoi framework, ECMWF, or the scoring-rule implementations tested? Please provide an explicit declaration.
- Will the trained models, code for the custom scoring rules, and experimental configurations be made available (e.g., on GitHub, Zenodo, or a supplementary repository)? If not, what are the barriers?
- The manuscript states 'All scores are implemented in the Anemoi framework' — are these implementations already public in the Anemoi repository, or are they new contributions that will be released?