# Related-Work & Citations Reviewer

## Summary
The manuscript's citation record is generally sound and appropriate for a rapidly evolving field. The authors accurately attribute claims to prior work, cite foundational scoring-rule literature correctly, and maintain reasonable self-citation proportions. The reference list includes both established work (Gneiting & Raftery 2007, Ferro 2014, Scheuerer & Hamill 2015) and recent developments (2025-2026 preprints), which is appropriate. However, one specific empirical claim about [19] (Pacchiardi et al.) could not be independently verified due to search limitations, and the manuscript could be more explicit about the relationship between this work and the closely related [14] by the same authors on multi-scale losses. No hard citation defects were identified, but minor clarifications would strengthen the related-work narrative.

## Strengths
- Foundational scoring-rule literature is correctly cited and attributed (Gneiting & Raftery 2007, Ferro 2014, Scheuerer & Hamill 2015).
- Self-citation is proportionate (2 of 24 references) and not used to inflate novelty.
- Recent competing work in machine-learned weather forecasting is cited (FGN, FourCastNet 3, Huracan, etc.), showing awareness of the state of the field.
- References appear real and resolvable; no obvious fabrications or garbled citations detected.
- The mix of journal articles and preprints is appropriate for a fast-moving field (2025-2026 work is current).

## Weaknesses
- The specific empirical claim that 'patched energy scores performed best' in [19] (Pacchiardi et al. 2024) is not independently verified in this review due to search tool limitations. The authors should confirm this claim is accurately attributed.
- The relationship between this work and [14] (Lang & Leutbecher 2025, 'A multi-scale loss formulation...') is not clearly delineated. Both are by overlapping author groups and both address scale-aware losses. The manuscript should explicitly state whether [14] is concurrent work, prior work, or a companion paper, and how this work extends or differs from it.
- The manuscript does not cite or discuss diffusion-based ensemble forecasting approaches (e.g., continuous ensemble weather forecasting with diffusion models, 2024), which are emerging alternatives to CRPS-based training. While not mandatory, a brief acknowledgment of this alternative direction would contextualize the contribution.

## Questions
- Can the authors confirm that the claim on page 3 — 'In the weather forecasting experiments of [19], patched energy scores performed best among the multivariate scoring rules they considered' — is accurately represented from Pacchiardi et al. (2024)? Please cite the specific section or figure.
- What is the publication status and relationship of [14] (Lang, Leutbecher, Maciel 2025) to the present work? Is it concurrent, prior, or a companion paper? How does the multi-scale formulation in [14] differ from the scale-aware approaches tested here?
- The manuscript mentions that 'the now operational version of the AIFS ensemble uses the scale aware loss formulation introduced in [14]' (Discussion, page 26). Does this mean [14] has already been operationalized, or is this planned? This affects how to position the novelty of the present study.