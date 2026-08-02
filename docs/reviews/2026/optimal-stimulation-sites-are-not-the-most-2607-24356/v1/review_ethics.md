# Ethics & Compliance Reviewer

## Summary
This is a secondary analysis of publicly available, de-identified fMRI data from the Alzheimer's Disease Neuroimaging Initiative (ADNI). The ethics and compliance posture is sound: the authors explicitly state IRB approval was obtained by ADNI at all participating sites, informed consent was documented at enrollment, the data are de-identified and publicly available, no new human subjects were enrolled, and funding sources are disclosed. The work is plainly exempt from new ethics review as a secondary computational analysis. No conflicts of interest are declared, which is appropriate given the institutional affiliations and funding sources listed. Data and code availability statements are clear and consistent with the ADNI Data Use Agreement. The manuscript meets the compliance bar for In Silico.

## Strengths
- IRB approval explicitly stated: 'The ADNI study was approved by the institutional review boards of all participating sites' (Ethics section).
- Informed consent documented: 'all participants (or their authorised representatives) provided written informed consent at enrollment' (Ethics section).
- De-identification confirmed: data are described as 'de-identified' and sourced from a public repository (ADNI database).
- Secondary-use data governance clear: authors note 'in accordance with [the ADNI Data Use Agreement], the raw and derived imaging data are not redistributed here,' showing awareness of data-use restrictions.
- Funding sources disclosed: Italian Ministry of University and Research grant (PNC0000001, Spoke 3) and ADNI funding (NIH U01 AG024904, DOD W81XWH-12-2-0012) are listed in Acknowledgments.
- No conflicts of interest declared, appropriate for the institutional context.
- Code and data availability statement is explicit and consistent with consent/DUA limits: code is openly available on GitHub; raw/derived data are available through ADNI upon registration and DUA acceptance.
- No vulnerable-population protections needed: the cohort comprises cognitively unimpaired controls and AD patients; no children, prisoners, or other protected groups are involved.
- Authorship integrity: author list is clear, affiliations are stated, and no evidence of ghost or gift authorship appears.

## Weaknesses
- SOFT: The Ethics section could explicitly state that this work is a secondary analysis and therefore exempt from new IRB review, to preempt any ambiguity about whether new approval was sought or required. The current phrasing ('This work is a secondary analysis of de-identified, publicly available human imaging data obtained from ADNI') is correct but does not explicitly invoke exemption language.
- SOFT: The manuscript does not acknowledge the use of any AI tools or large language models in analysis, manuscript preparation, or figure generation. Given the computational nature and the date (2026), a statement on AI use (if any) would strengthen transparency, even if none was used.

## Questions
- Was this work reviewed and approved as exempt by the authors' institutional IRB, or did it proceed without new review on the grounds that it is secondary analysis of de-identified public data? An explicit statement of the exemption determination would clarify the compliance pathway.
- Were any AI tools, machine-learning models, or large language models used in the analysis pipeline, figure generation, or manuscript preparation? A brief disclosure would be consistent with emerging transparency norms.
- The ADNI Data Use Agreement restricts redistribution of raw and derived data. Does the authors' GitHub repository contain any derived imaging data (e.g., preprocessed BOLD time series, FC matrices, or model outputs), or only analysis code and non-data outputs? If derived data are posted, is that consistent with the DUA?
- Table S1 lists cohort sizes for each analysis. Are all cohort definitions and exclusion criteria (e.g., the '>100-volume filter' mentioned for the tangent-space SVM benchmark) documented in the Methods or Supplementary Materials, to support reproducibility and audit of data governance?