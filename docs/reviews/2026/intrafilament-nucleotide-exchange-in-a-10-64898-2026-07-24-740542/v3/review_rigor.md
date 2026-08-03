# Rigor & Overclaiming Reviewer

## Summary
The manuscript provides compelling evidence for intrafilament nucleotide exchange in MreB filaments, a novel mechanism distinct from actin. The combination of in vitro reconstitution, high-resolution imaging, mutagenesis, modeling, and in vivo validation is strong. However, the in vivo CCCP experiment cannot fully disentangle ATP depletion from membrane potential effects, and the claim that ATPase activity is dispensable for morphogenesis conflicts with cited literature reporting mild defects. These issues warrant minor revision.

## Strengths
- The multi-modal approach (HS-AFM, TIRF, biochemistry, modeling) provides robust, cross-validated evidence for symmetric elongation and intrafilament nucleotide exchange.
- The use of ATPase mutants (E136A, D158A) as mechanistic tools is well-executed and reveals distinct nucleotide-binding phenotypes that align with the model.
- The stochastic Monte-Carlo model quantitatively recapitulates complex polymerization/depolymerization kinetics using experimentally derived parameters.

## Weaknesses
- The in vivo CCCP experiment (Fig 4J) attributes MreB delocalization solely to ATP depletion, but CCCP also collapses the proton motive force and membrane potential, which independently affect MreB localization (Strahl & Hamoen, 2010). The resistance of E136A could reflect its locked ATP-state rather than proof that ATP hydrolysis is dispensable for morphogenesis; the cited references (7,29,32,33) actually report mild morphological defects for these mutants, contradicting the statement that E136A displays "normal rod-shape, consistent with normal MreB function." This overclaim should be qualified or reconciled.
- The claim that this is "the first report of nucleotide cycling within a biological polymer" (main text) is a strong novelty assertion that may not hold given nucleotide exchange in other cytoskeletal systems (e.g., tubulin GTP exchange in microtubules, though not within intact polymers). The authors should verify this claim against the literature or soften the language to "to our knowledge" with appropriate citations.
- The TFLime FRAP experiment (Fig 3E) is acknowledged to suffer from irreversible photochemical trapping, undermining the conclusion that monomers do not turnover within filaments. While the ATP* incorporation assay (Fig 3H) provides stronger evidence for nucleotide exchange, the subunit turnover question remains open. The authors should either remove the definitive statement about no monomer turnover or provide an orthogonal assay (e.g., photoactivatable tags).
- The HS-AFM elongation rate (14.4 ± 10.16 nm/s, n=7) is based on very few, short tracks due to tip-induced mobility, making it a rough estimate; the text should reflect this uncertainty.
- The critical concentration (Cc ≈ 0.003 µM) derived from TIRF is exceptionally low and relies on a linear fit at low concentrations where few filaments were tracked; the confidence interval should be reported.
- The Monte Carlo model assumes identical dynamics at both ends and nucleotide-state-independent exchange rates; the justification for these simplifications should be discussed.
- The liposome binding assay (Fig 1E,F) uses Coomassie staining which may not be quantitative for low protein amounts; fluorescence-based quantification would strengthen the CL-dependence claim.
- The statement "ATP binding triggers MreB polymerization" (Abstract) implies causation, but the data show ATP is required; the trigger could be membrane binding coupled to ATP binding, which the data also support.

## Questions
- Can the authors rule out that CCCP-induced delocalization is due to membrane potential collapse rather than ATP depletion, e.g., by using an ATP synthase inhibitor that doesn't affect membrane potential?
- What is the estimated confidence interval for the critical concentration (0.003 µM) given the low-concentration TIRF data?
- Does the Monte Carlo model fit any parameters to the disassembly data, or are all rates fixed from independent experiments?
- Have the authors tested whether other anionic lipids (e.g., phosphatidylserine) can substitute for cardiolipin in supporting MreB polymerization?