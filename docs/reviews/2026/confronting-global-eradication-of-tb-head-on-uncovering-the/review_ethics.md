# Ethics & Compliance Reviewer

## Summary
This computational bioinformatics study of TB drug-resistance mutations does not involve human subjects, animal research, clinical trials, or dual-use pathogen work, and thus triggers no HARD ethics requirements. The authors collected published mutation data from 149 peer-reviewed studies covering 31,073 clinical isolates; this is secondary-use aggregation of already-published, de-identified epidemiological data. No IRB approval is needed for retrospective analysis of published literature. However, the manuscript is silent on funding sources and competing interests, which are cross-cutting HARD disclosures required by most journals. The authors should also clarify data and code availability, and acknowledge any AI-tool use in manuscript preparation.

## Strengths
- Work is purely computational analysis of published, de-identified mutation data, placing it outside the scope of human-subjects, animal, or clinical-trial ethics oversight.
- Data source is transparent: 149 published studies explicitly listed in Supplementary Table S1, enabling traceability and verification of secondary-use aggregation.
- No identifiable patient data, genetic sequences linked to individuals, or sensitive clinical information is presented; all data are population-level mutation frequencies and structural predictions.

## Weaknesses
- No funding sources disclosed. The manuscript does not state whether the work was supported by grants, institutional funds, or other sources, violating standard cross-cutting HARD disclosure requirements.
- No competing interests or conflicts of interest statement. The manuscript does not include an explicit declaration of competing interests or a statement that none exist, which is a HARD requirement at most peer-reviewed venues.
- No statement on data and code availability. The manuscript does not specify whether the mutation atlas (Supplementary Table S3), structural models, docking results, or analysis code are publicly available, or under what terms; this is a SOFT transparency issue for reproducibility.
- No acknowledgement of AI-tool use. Given the extensive bioinformatics analysis and the 2026 publication date, the manuscript does not disclose whether any generative AI or large-language models were used in analysis, visualization, or manuscript preparation, which is increasingly expected.

## Questions
- What funding sources supported this research? Please provide grant numbers, funder names, and any relevant funding disclosures.
- Do the authors have any competing interests, financial or otherwise, that should be disclosed? If none, please include an explicit 'Competing Interests: None declared' statement.
- Will the mutation atlas (Supplementary Table S3), structural models, docking scores, and analysis code be made publicly available? If so, under what license and via which repository? If not, what are the access restrictions?
- Were any generative AI tools, large-language models, or automated writing assistants used in the preparation of this manuscript? If so, please disclose the tool name, version, and the specific tasks for which it was used.
- The manuscript cites 149 published studies as the data source. Are the individual study identifiers (PubMed IDs, DOIs) and the extracted mutation counts per study provided in Supplementary Table S1 in a format that allows independent verification and reuse?