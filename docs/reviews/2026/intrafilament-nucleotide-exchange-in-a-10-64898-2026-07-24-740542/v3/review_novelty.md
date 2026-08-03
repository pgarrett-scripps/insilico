# Novelty & Contribution Reviewer

## Summary
The manuscript reports a genuine novelty: nucleotide exchange within intact MreB filaments, a behavior not seen in eukaryotic actin or other characterized cytoskeletal polymers. The evidence from TIRF, HS-AFM, and ATPase mutants supports this claim. The contribution is significant for understanding bacterial cytoskeletal dynamics and evolutionary divergence of actin homologs.

## Strengths
- Direct visualization of bidirectional filament growth and intrafilament nucleotide exchange using complementary high-resolution methods (TIRF, HS-AFM).
- Clean genetic dissection with ATPase mutants (E136A, D158A) showing hydrolysis is uncoupled from polymerization but required for ADP-induced disassembly.
- Integration of in vitro reconstitution, stochastic modeling, and in vivo validation (CCCP experiments) into a coherent mechanistic framework.

## Weaknesses
- The claim that intrafilament nucleotide exchange defines a 'new class of biological polymer behavior' is not benchmarked against other prokaryotic actin-like proteins (e.g., ParM, MamK, AlfA) where nucleotide dynamics in filaments may have been studied but not framed as exchange; a literature search reveals ParM filament nucleotide exchange was proposed in Garner et al. 2004 (Science) and later works, though the mechanism may differ. The manuscript should explicitly differentiate its finding from these precedents or acknowledge them.
- The critical concentration (Cc ≈ 0.003 µM) derived from TIRF elongation rates is exceptionally low and not independently validated (e.g., by sedimentation); the plateau in elongation rate above 0.06 µM MreB is attributed to 2D diffusion limitation, but alternative explanations (e.g., filament end capping, cooperativity) are not ruled out.
- The in vivo CCCP experiment depletes ATP globally, causing pleiotropic effects; the specific attribution to intrafilament nucleotide exchange vs. general membrane potential collapse or other ATP-dependent processes is not controlled (e.g., by expressing a non-hydrolyzable ATP analog or using an ATP-depletion system with faster kinetics).

## Questions
- Has intrafilament nucleotide exchange been reported for other bacterial actins (ParM, MamK, AlfA, CetZ) in any form, and if so, how does MreB's mechanism differ?
- Can the authors provide a direct measurement (e.g., by fluorescence correlation spectroscopy or single-molecule tracking) of the 2D diffusion coefficient of membrane-bound MreB subunits to support the diffusion-limitation model for the elongation plateau?
- Does the Monte Carlo model predict the observed acceleration of WT disassembly after buffer wash (Fig. 4C) without invoking cooperative effects, and are the fitted parameters (k_hyd, k_Pir, k_+n, k_-n) uniquely constrained by the data?