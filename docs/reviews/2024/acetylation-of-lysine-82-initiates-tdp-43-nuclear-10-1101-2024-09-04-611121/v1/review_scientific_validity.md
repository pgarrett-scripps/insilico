# Scientific Validity & Claims Reviewer

SCORE: 4
CONFIDENCE: 4

## Summary

This study identifies lysine 82 acetylation within TDP-43's classical nuclear localization signal (cNLS) as a mechanism driving nuclear loss of function in ALS. The core claims are well-supported by a coherent experimental progression: reduced proteasome activity triggers K82 acetylation, which abolishes importin-α1 binding and nuclear import, and K82 acetylation is detected in sporadic ALS motor cortex. The work is mechanistically sound and the evidence is largely convincing, though one load-bearing claim requires clarification and the translational scope remains narrower than the framing suggests.

## Strengths

1. The quantitative mass spectrometry survey (TMT proteomics) directly demonstrates that TDP-43 is the most sensitive nuclear protein to proteasome inhibition, establishing specificity rather than assuming it.

2. The K82 mutagenesis panel (K82R, K82-K95, K82-K97, etc.) systematically maps the functional architecture of the bipartite NLS and shows K82 is necessary but not sufficient, a nuanced finding that rules out oversimplified models.

3. The acetylation-specific antibodies against K82 are validated by ELISA and applied to human postmortem tissue, providing orthogonal evidence that the modification occurs in disease and is not merely an in vitro artifact.

## Weaknesses: Load-bearing claims

**Claim 1: Acetylation at K82 is sufficient to abolish TDP-43 nuclear import.**

The evidence is the K82Q acetylation-mimicking mutation, which "eliminated its nuclear import and binding to importin-α1" (Fig. 3C–E, Results section). However, K82Q is a lysine-to-glutamine substitution, which mimics acetylation structurally but does not replicate the actual post-translational modification. The authors do show that synthetic peptides with *actual* acetylation at K82 fail to bind importin-α1 (Fig. 3F), but this is a 33-residue peptide in vitro, not full-length TDP-43 in cells. The gap is whether the K82Q mutation faithfully recapitulates the effect of genuine acetylation on the full-length protein in its native context—particularly whether other lysines in the NLS might be acetylated simultaneously in vivo, or whether the charge-reversal model (glutamine vs. acetyl-lysine) is equivalent. The peptide-binding assay (Fig. 3F) bridges this partially but does not test full-length protein dynamics. *What would settle this:* co-expression of TDP-43-K82Q with a histone acetyltransferase or deacetylase inhibitor to show that blocking deacetylation phenocopies K82Q, or direct measurement of nuclear import kinetics for acetylated vs. unacetylated full-length TDP-43 in a cell-free import assay.

**Claim 2: Reduced proteasome activity drives TDP-43 mislocalization through K82 acetylation (and ubiquitination/phosphorylation of K79, K84, S91, S92).**

The evidence chain is: (i) proteasome inhibition causes TDP-43 cytoplasmic accumulation (Fig. 1); (ii) mass spectrometry identifies acetylation/ubiquitination at K79, K82, K84 and phosphorylation at S91, S92 in proteasome-inhibited cells (Fig. 3A–B); (iii) K82Q mimics this and blocks import (Fig. 3C–E). The missing link is causality: the authors show that these modifications *occur* when proteasome activity is reduced, but do not directly show that *blocking* these modifications (e.g., by preventing acetylation or ubiquitination) rescues nuclear import under proteasome inhibition. The K82Q experiment shows that acetylation is *sufficient* to cause mislocalization, but the proteasome-inhibition experiment does not prove it is *necessary*. An alternative explanation is that proteasome inhibition causes mislocalization through a different mechanism (e.g., sequestration of importin-α1 by other ubiquitinated substrates, or direct proteasome-dependent turnover of importin machinery), and the acetylation is a secondary consequence or bystander. *What would settle this:* expression of a TDP-43 variant with K79R/K82R/K84R/S91A/S92A (or acetylation-resistant lysines) in proteasome-inhibited neurons, with quantification of whether nuclear import is restored compared to wild-type TDP-43 under the same inhibition.

**Claim 3: K82 acetylation is an early initiator of TDP-43 proteinopathy in sporadic ALS.**

The evidence is that ac-TDP-43(K82) is detected in all six sALS motor cortices but not in four controls (Fig. 5B), and ac-TDP-43(K82) appears in both soluble and insoluble fractions while phosphorylated TDP-43 (pS409/410) is only in the insoluble fraction, suggesting acetylation precedes phosphorylation (Fig. 5C). This is correlational: the authors show acetylation is present in disease but do not establish that it *initiates* the cascade or that it is causally upstream of phosphorylation and aggregation. The small sample size (n=6 sALS, n=4 controls) and lack of quantitative correlation between ac-TDP-43(K82) levels and disease severity, proteinopathy burden, or clinical phenotype leave open whether acetylation is a driver, a marker, or a consequence of other pathology. The presence in both soluble and insoluble fractions is consistent with early involvement but does not prove it is the initiating event—phosphorylation could be initiated by a separate mechanism and acetylation could follow. *What would settle this:* quantitative correlation of ac-TDP-43(K82) signal intensity with phosphorylated TDP-43 levels and neuropathological staging across a larger cohort, or functional evidence (e.g., in a transgenic model) that preventing K82 acetylation delays or prevents TDP-43 aggregation and disease phenotypes.

## Weaknesses: Sweep

1. The proteasome inhibitor doses (2–10 nM BTZ, 100 nM MG132, 10 nM MRZ) achieve ~50% inhibition, but the physiological relevance of this specific threshold is not justified—aging and ALS show 20–60% declines (Fig. S1A), so the choice of 50% is somewhat arbitrary and sensitivity to dose is not explored.

2. The iPSC-derived cortical neurons are a valid model but are not motor neurons, and TDP-43 pathology in ALS is most prominent in motor cortex and spinal cord; generalization to the primary affected cell type is assumed but not tested.

3. The stathmin-2 splicing assay (Fig. 1G) confirms loss of TDP-43 nuclear function but is a single downstream target; whether K82 acetylation disrupts other known TDP-43 functions (e.g., RNA binding, splicing of other targets) is not addressed.

4. The FUS-PY-NLS rescue (Fig. 2E–I) shows that importin-β2-mediated import is resistant to proteasome inhibition, but does not test whether acetylation of K82 would also block PY-NLS-mediated import if acetylation sites were engineered into that sequence.

5. The three polyclonal antibodies against ac-TDP-43(K82) are validated by ELISA against synthetic peptides but not by mass spectrometry or independent orthogonal detection (e.g., immunofluorescence with orthogonal antibodies or Western blot with a second antibody source).

6. The human postmortem samples are fresh-frozen with short postmortem interval (<6 h), but no information is provided on disease duration, age at onset, genotype, or clinical subtype, limiting interpretation of whether acetylation correlates with disease stage or phenotype.

7. The claim that acetylation is "sufficient to initiate TDP-43 nuclear loss of function" (Abstract) is supported for K82 but the title emphasizes K82 alone while the Results show K79 and K84 also contribute (albeit less); the framing could be more precise about which lysine is the primary driver.

8. No data are provided on the acetyltransferases or deacetylases responsible for K82 acetylation, limiting mechanistic insight into how proteasome inhibition triggers acetylation or how this pathway might be therapeutically targeted.

## Questions

1. In Fig. 3F, does the peptide-binding assay control for non-specific binding by testing whether acetylation at K79 or K84 alone (without K82 acetylation) also abolishes importin-α1 binding, or is the selectivity of K82 inferred only from the cellular K82Q data?

2. Figure 5B shows variable ac-TDP-43(K82) signal across sALS samples; is this variation correlated with phosphorylated TDP-43 levels, disease duration, or clinical severity, or is it purely categorical (present vs. absent)?

3. In the proteasome-inhibition experiments, is the kinetics of acetylation (when it first appears relative to mislocalization) measured, or is only the 24 hr timepoint shown?