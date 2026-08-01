# Ethics & Compliance Reviewer

## Summary
The manuscript describes a single-cell top-down proteomics study of cardiomyocytes and presents appropriate ethics and compliance disclosures for animal research. Animal-use approval is clearly stated with institutional oversight named, and funding sources are disclosed. However, the manuscript is silent on whether data and code will be made available in a manner consistent with reproducibility standards, and the conflict-of-interest statement, while present, contains a potential ambiguity regarding the scope of disclosed interests. These are minor compliance gaps that do not rise to the level of blocking acceptance but warrant clarification.

## Strengths
- Animal research ethics approval is explicitly stated: 'All animal studies were approved by the Institutional Animal Care and Use Committee at Cedars-Sinai Medical Center and The Scripps Research Institute, and carried out in accordance with the National Institute of Health guidelines' (Methods, Animal studies section).
- Funding sources are comprehensively disclosed in the Acknowledgments, naming specific NIH grants and institutional awards (R00-HL141702, R01-HL177461, R21MH129776-01, R01 MH100175-05, R01 DK138430, and others).
- A conflict-of-interest statement is present: 'K.R.D. is involved in the commercialization of the software ProSight PD 4.5. The other authors declare no conflict of interest' (Notes section).
- The manuscript specifies mouse strain (C57BL/6J), age (8–12 weeks), and housing conditions, supporting reproducibility and welfare transparency.
- Humane endpoints are implicit in the use of anesthesia (Nembutal via intraperitoneal injection at 100 mg/kg) and standard Langendorff perfusion protocols for cardiomyocyte isolation, consistent with established animal-care practices.

## Weaknesses
- Data availability statement is vague: 'Raw spectrum data are available via figshare' is stated without a persistent identifier (DOI), accession number, or explicit link, making verification and access difficult for readers and reproducibility auditors.
- The scope of K.R.D.'s conflict of interest is incompletely disclosed: the statement notes involvement in 'commercialization of the software ProSight PD 4.5,' but does not clarify whether K.R.D. holds equity, receives royalties, or has other financial interests, nor does it state whether this relationship could influence the choice or interpretation of the software in the analysis.
- No explicit statement regarding code availability: the manuscript describes custom data-analysis workflows (ProSight PD 4.5, UniDec, Freestyle, TDValidator) but does not state whether analysis scripts, parameter files, or reproducible workflows will be shared, limiting transparency for computational reproducibility.
- The IACUC approval statement does not include a protocol number, which is standard for verification and traceability in animal-research compliance documentation.

## Questions
- Will the authors provide a persistent DOI or direct link to the figshare repository containing the raw spectrum data, and will the repository be made public upon publication?
- Can the authors clarify the nature and scope of K.R.D.'s financial or commercial interest in ProSight PD 4.5 (e.g., equity stake, royalty arrangement, consulting fee), and whether this relationship influenced the selection or interpretation of the software in this study?
- What is the IACUC protocol number for the animal studies conducted at Cedars-Sinai Medical Center and The Scripps Research Institute, and can it be provided for verification?
- Will the authors make available the analysis scripts, parameter files, or workflows used in ProSight PD 4.5, UniDec, and other custom computational tools to support reproducibility?
- The manuscript states that cells were 'shipped on dry-ice to The Scripps Research Institute and stored at -80°C until use' — were samples transferred under any material-transfer agreement (MTA) or institutional data-use agreement (DUA) that should be disclosed?