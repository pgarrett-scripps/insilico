# Citation Integrity Auditor

## Summary
The manuscript contains 25 references with triggers detected for three categories: reference resolvability, claim-citation support, and self-citation/citation inflation. No triggers were found for quotation/number fidelity or retracted/predatory sources. Foundational references [9] and [10] and data source [11] require verification of resolvability. Three specific claim-citation relationships require verification that cited papers support the claims made about them. All cited works appear to exist based on available evidence, though some could not be fully verified. Self-citations appear appropriate and relevant.

## Categories checked
- Reference resolvability
- Claim–Citation Support
- Self-citation / Citation Inflation

**HARD gaps (blocking): 0** · SOFT gaps: 0 · unverifiable: 6

## Unverifiable (raise as questions)
- **[Reference resolvability] Reference [9] 'Fair scores for ensemble forecasts' (Ferro, 2014)** — cited for foundational scoring rule definitions but search tools did not return this specific paper
- **[Reference resolvability] Reference [10] 'Strictly proper scoring rules, prediction, and estimation' (Gneiting and Raftery, 2007)** — cited for foundational scoring rule definitions but search tools did not return this specific paper
- **[Reference resolvability] Reference [11] 'The ERA5 global reanalysis' (Hersbach et al., 2020)** — cited as the data source ('Training uses ERA5 reanalysis data [[11](#ref-11)] from 1979 to 2020') but search did not retrieve this specific paper
- **[Claim–Citation Support] Claim that reference [19] reports 'patched energy scores performed best'** — 'In the weather forecasting experiments of [[19](#ref-19)], patched energy scores performed best among the multivariate scoring rules they considered' - cannot confirm from manuscript excerpt whether reference [19] specifically reports this
- **[Claim–Citation Support] Claim that reference [13] defines 'almost fair variant'** — 'Following [[13](#ref-13)], an almost fair variant can be defined as a convex combination of the standard and fair scores' - cannot verify from manuscript excerpt whether reference [13] actually defines this variant
- **[Claim–Citation Support] Claim that references [15] and [18] describe applications of CRPS-based training to limited-area and stretched-grid modeling** — 'The approach is also being applied for regional and high-resolution forecasting, including limited-area [[15](#ref-15)] and stretched-grid modelling [[18](#ref-18)]' - cannot verify whether these references specifically describe these applications

## Documented (for the record)
- **[Reference resolvability] Reference [13] 'AIFS-CRPS: Ensemble forecasting using a model trained with a loss function based on the continuous ranked probability score' (Lang et al., 2024)** — cited multiple times as foundational to the current work (e.g., 'follow AIFS-CRPS [[13](#ref-13)] in terms of architecture and general training configuration')
- **[Reference resolvability] Reference [19] 'Probabilistic forecasting with generative networks via scoring rule minimization' (Pacchiardi et al., 2024)** — cited for motivation ('This kind of localization is intended to make the score more sensitive to local multivariate relationships than a purely global energy score. In the weather forecasting experiments of [[19](#ref-19)], patched energy scores performed best among the multivariate scoring rules they considered')
- **[Reference resolvability] Reference [4] 'Fourcastnet 3: A geometric approach to probabilistic machine-learning weather forecasting at scale' (Bonev et al., 2025)** — cited for context ('an approach that has since also been used in recent global models such as FGN [[1](#ref-1)], FourCastNet 3 [[4](#ref-4)]')
- **[Self-citation / Citation Inflation] Self-citations by author Simon Lang in references [13], [14], and [18]** — References [13], [14], and [18] all include author 'Simon Lang' (first author of current manuscript). Reference [13] is foundational, reference [14] introduces multi-scale loss formulation, reference [18] cited for context on high-resolution forecasting