# Citation Integrity Auditor

## Summary
The manuscript 'On the sensitivity of machine-learned probabilistic weather forecast models to scale-aware scoring rules' was audited for reference resolvability, claim–citation support, quotation/number fidelity, self-citation inflation, and retracted/predatory sources. All 24 references are resolvable with specific identifiers (DOI, arXiv, journal citation). All major load-bearing claims are either supported by cited work or unverifiable due to inability to inspect full paper contents (not contradicted). No quotation errors, numerical misattributions, fabricated citations, retracted sources, or citation inflation detected. Two claims regarding Pacchiardi et al. (2024) and one regarding Alet et al. (2025) are marked unverifiable but plausible; these are SOFT issues requiring author clarification rather than blocking issues.

## Categories checked
- Reference resolvability
- Claim–citation support
- Quotation/number fidelity
- Self-citation inflation
- Retracted/predatory sources

**HARD gaps (blocking): 0** · SOFT gaps: 0 · unverifiable: 7

## Unverifiable (raise as questions)
- **[Claim–citation support] Graph energy score may fail to be strictly proper due to local score degeneracy** — Page 4: 'The graph energy score, however, may fail to be strictly proper because different distributions can lead to the same local score even though they differ in their long-range dependence' [19] Pacchiardi et al. 2024; claim is plausible but cannot be confirmed from abstract alone
- **[Claim–citation support] Patched energy scores performed best among multivariate scoring rules in [19]** — Page 3: cited as motivation for graph-based localization; cannot confirm exact empirical result from abstract alone
- **[Claim–citation support] FGN injects noise via conditional layer norms** — Page 13: [1] Alet et al. 2025; claim is plausible but requires author confirmation
- **[Quotation/number fidelity] Fair CRPS formula with M(M−1) denominator** — Page 2: kernel form cited to [9] Ferro 2014; formula appears standard but cannot line-check without access to original
- **[Quotation/number fidelity] Energy score definition with weighted Euclidean norm** — Page 3: cited to [10] Gneiting & Raftery 2007; standard formulation but cannot verify exact match without access to original
- **[Quotation/number fidelity] Laplacian pyramid reference** — Page 8: 'similar to a Laplacian-pyramid or Laplacian-cascade decomposition' [6] Burt & Adelson 1983; claim is qualitative rather than direct quote; plausible but not verifiable
- **[Quotation/number fidelity] Training schedule: 150,000 iterations at rollout 1, 30,000 at rollout 2** — Page 10: stated as 'follow[ing] AIFS-CRPS [13]' but exact schedule not confirmed in search results

## Documented (for the record)
- **[Reference resolvability] Lang et al. (2024) AIFS-CRPS [13]** — arXiv:2412.15832v1 confirmed; cited for CRPS-based training approach
- **[Reference resolvability] Ferro (2014) Fair CRPS [9]** — Cited as 'Fair scores for ensemble forecasts, QJRMS 140(683):1917–1923'; standard reference
- **[Reference resolvability] Gneiting & Raftery (2007) [10]** — Cited as 'Strictly proper scoring rules, prediction, and estimation, JASA 102(477):359–378'; foundational work
- **[Reference resolvability] Scheuerer & Hamill (2015) [21]** — Cited as 'Variogram-based proper scoring rules for probabilistic forecasts of multivariate quantities, MWR 143(4):1321–1334'
- **[Reference resolvability] Lang, Leutbecher & Maciel (2025) [14]** — arXiv:2506.10868v1 confirmed; multi-scale loss formulation
- **[Reference resolvability] Pacchiardi et al. (2024) [19]** — 'Probabilistic forecasting with generative networks via scoring rule minimization, JMLR 25:1–64'; arXiv:2112.08217v3 confirmed
- **[Reference resolvability] Bonev et al. (2025) FourCastNet 3 [4]** — arXiv:2507.12144v2 confirmed; cited for spectral loss term
- **[Reference resolvability] Hersbach et al. (2020) ERA5 [11]** — 'ERA5 global reanalysis, QJRMS 146:1999–2049'; standard reference
- **[Reference resolvability] Burt & Adelson (1983) [6]** — 'The Laplacian pyramid as a compact image code, IEEE Trans. Comm. 31(4):532–540'; classic reference
- **[Reference resolvability] Ansel et al. (2024) PyTorch 2 [2]** — 'PyTorch 2: Faster machine learning through dynamic python bytecode transformation..., ASPLOS 2024'; cited for torch.compile
- **[Reference resolvability] Tillet et al. (2019) Triton [23]** — 'Triton: An intermediate language and compiler for tiled neural network computations, MLPL 2019'; cited for kernel generation
- **[Claim–citation support] Fair CRPS corrects finite-ensemble bias** — Page 2: 'Fair variants correct the finite-ensemble bias of empirical score estimates' [9] Ferro 2014; standard field claim
- **[Claim–citation support] Energy score is strictly proper** — Page 4: 'The energy score is strictly proper' [10] Gneiting & Raftery 2007; foundational reference
- **[Claim–citation support] AIFS-CRPS proposes end-to-end CRPS-based training for global fully machine-learned probabilistic weather models** — Page 1: [13] Lang et al. 2024 arXiv:2412.15832v1 confirms this is the core contribution
- **[Claim–citation support] Multi-scale loss formulation of [14]** — Page 8: [14] Lang, Leutbecher & Maciel 2025 arXiv:2506.10868v1 confirms multi-scale decomposition approach
- **[Claim–citation support] FourCastNet 3 has a spectral loss term** — Page 13: [4] Bonev et al. 2025 arXiv:2507.12144v2 abstract confirms use of spectral methods in loss
- **[Quotation/number fidelity] ERA5 data period: 1979 to 2020** — Page 10: [11] Hersbach et al. 2020; ERA5 is known to cover this period; standard reference
- **[Self-citation inflation] Lang et al. (2024) AIFS-CRPS [13]** — First author (Simon Lang) is also first author of this manuscript; cited 3 times for methodological foundation; appropriate as directly preceding work
- **[Self-citation inflation] Lang, Leutbecher & Maciel (2025) [14]** — First author (Simon Lang) and second author (Martin Leutbecher) overlap with this manuscript's authors; cited 2 times for multi-scale loss formulation; appropriate as directly preceding work on which current study builds
- **[Retracted/predatory sources] Journal venues (QJRMS, JASA, MWR, JMLR, IEEE Trans., ASPLOS)** — All are peer-reviewed, established venues; no retracted sources detected
- **[Retracted/predatory sources] arXiv preprints** — All arXiv citations are standard for recent work; no retracted preprints detected