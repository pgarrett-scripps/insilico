# Statistics & Data-Analysis Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

This is a well-executed data-reduction tool paper with sound quantitative validation on a defined benchmark. The core claim—that dnoise removes 35–53% of MS1 frame data while preserving label-free quantification accuracy and identification counts—is supported by appropriate comparisons against unfiltered data across multiple acquisition modes and gradients. The statistical reporting is generally transparent about what was measured and how. The main limitation is that validation is narrow (one instrument, one sample type, controlled conditions), which the authors acknowledge; this constrains the generalizability claim but does not undermine the benchmark results themselves. The work is suitable for publication with minor clarifications on a few quantitative details.

## Strengths

1. **Reproducible parameter selection with disclosed bias**: The authors explicitly state that the streak-filter parameters were tuned on part of the benchmark (15-minute ddaPASEF) and acknowledge this is not fully out-of-sample, then validate on the remaining arms (5-minute and both diaPASEF modes), which is honest and methodologically sound.

2. **Paired feature-level validation**: Figure 5 reports Pearson *r* and aligned median absolute Δlog₂ on shared peptide/precursor intensities across replicate runs, a direct fidelity check that goes beyond summary ratios and strengthens the claim that quantification is preserved.

3. **Ablation and control comparisons**: Table S4 partitions the three filter stages, and Section 3.4 compares the streak filter against a matched-intensity threshold on the same removal target, isolating the structural advantage of mobility coherence over absolute intensity.

## Weaknesses: Load-Bearing Claims

**1. Label-free quantification accuracy claims rest on a narrow definition of "preserved."**

The authors report that "LFQ accuracy was preserved in both modes" (Abstract, Results). For ddaPASEF, they show that original and MS1-denoised arms returned identical PSM, peptide, and protein-group counts (line 186), so the claim is sound there: the database search reads only MS/MS, which is untouched. But for diaPASEF, the claim is more subtle. DIA-NN derives MaxLFQ quantities from fragment chromatograms (line 190), so MS1-only filtering does not directly alter the signal used for protein quantification. The authors then report that "median protein-level LFQ CV and LFQ accuracy (Figures 3 and 4) were unchanged at both gradients" (line 191). However, Figure 3 shows residual log₂ ratios (observed minus expected) for all condition pairs and species, and visual inspection suggests small movements in several cells—particularly the E. coli ratio at 5 minutes appears to shift downward in the MS1-denoised arm. The text states "the regulated-species ratios moved toward their expected values after denoising" (line 195), which is inconsistent with "unchanged." The percentile-bootstrap 95% CIs for paired original-versus-MS1 accuracy comparisons are cited as being in Tables S10 and S11 (line 162), but those tables are not provided in the manuscript excerpt. Without those intervals, I cannot verify whether the observed movements are within noise or systematic. **What is needed**: Report the 95% CIs from Tables S10 and S11 in the main text or supplement for at least the diaPASEF condition pairs where the largest movements occur, and clarify whether "preserved" means "statistically indistinguishable" or "moved toward expectation."

**2. Identification loss under MS/MS denoising is attributed to the streak filter's selectivity, but the mechanism is not fully isolated.**

In Section 3.4, the authors compare the streak filter with a matched-intensity threshold and report that the streak filter "preferentially retained searchable signal" (line 276). They show that under MS/MS denoising, the streak filter lost rank-1 decoy hits faster than target hits (decoy-to-target loss ratio 1.77–2.34), whereas the intensity threshold inverted this ratio (0.43–0.57). This is presented as evidence that the streak filter is better. However, the comparison is between two different filters applied to the same frames, not between the streak filter applied to different frame sets. The decoy-to-target ratio is a property of what each filter removes, but it does not directly prove that the streak filter's removals are more justified. A decoy hit that is removed might be removed because it is a false match *and* because it happens to be sparse in mobility, not because the filter correctly identified it as uninformative. The alternative explanation—that the intensity threshold simply removes weak signal more aggressively, and weak signal is enriched for false matches regardless of the filter's reasoning—is not excluded. **What is needed**: Report the distribution of mobility-streak lengths (number of consecutive occupied scans) for removed target hits versus removed decoy hits under the streak filter alone, to show whether removed decoys are actually sparser in mobility than removed targets, or whether the decoy enrichment is driven by intensity alone.

**3. The benchmark is explicitly narrow, but the generalization claim is not scaled to match.**

The authors state in Section 3.7 that "the replicated benchmark remains controlled and narrow: one timsTOF Ultra 2 instrument, one laboratory, one 50 ng three-species sample, two gradients, and two acquisition modes" and that "validation across laboratories, sample loads, and sparse acquisitions remains necessary." This is candid. However, the Abstract and main Results sections present the findings as if they apply to timsTOF broadly: "On a three-species benchmark spanning ddaPASEF and diaPASEF at 5- and 15-minute gradients, default MS1-only denoising reduced the frame binary by 35 to 53%." The range (35–53%) is correct for the tested conditions, but a reader might infer that any timsTOF user running ddaPASEF or diaPASEF at similar gradients will see similar reduction. The paper does not report whether reduction varies with sample complexity, ion abundance, or instrument state. The 50 ng load is described as "a standard test" (line 142), but no data are shown for lower loads (e.g., single-cell or low-input proteomics), where the streak filter's assumption of "enough consecutive mobility scans to form a recoverable run" (line 318) might fail. **What is needed**: Either restrict the main claims to "on this benchmark" or provide at least one additional sample type (e.g., a complex cell lysate, or a low-input sample) to show whether the 35–53% range holds outside the controlled mixture.

## Weaknesses: Sweep

- **Precision reporting**: The paper reports "median pooled protein CV across conditions A and B" (line 161) but does not state how many proteins contribute to that median or whether the distribution is symmetric; a box plot or percentile range would clarify whether the median is representative.

- **Multiple comparisons**: The benchmark includes 18 runs per gradient and acquisition mode (72 total), with condition pairs, species, and filter arms all compared; no multiple-comparison correction is applied or discussed, though the comparisons are largely descriptive rather than hypothesis-driven.

- **Quantified protein and peptide counts**: Figure 2 (right) shows counts "relative to the original arm," but the absolute numbers are not given in the figure; readers cannot judge whether a 1.6% change in protein-group counts (line 189) is a loss of 10 proteins or 100.

- **Runtime and memory**: Table S16 is cited but not provided in the excerpt; the text reports "7.4–39.0 seconds" (line 298) across 72 files, but the range is wide and no median or mean is given, making it hard to assess typical performance.

- **Halo filter validation**: The halo filter is described as "a small final trim" (line 181), but no ablation is provided showing its effect on accuracy or precision; if it is small, it should be easy to show.

- **Centroiding results**: Section 3.5 reports that the watershed centroider "gave up 1.3% of the proteins and 2.2% of the peptides" (line 310) but does not state the absolute counts or whether these losses are statistically meaningful given the benchmark size.

- **Decoy-hit interpretation**: The claim that "the spectra the streak filter withdraws are enriched for matches that were already wrong" (line 276) assumes that rank-1 decoy hits are uniformly false, but some may be true matches to contaminants or off-target sequences; the enrichment argument is sound, but the interpretation overstates certainty.

- **On-instrument denoising confound**: The text notes that "Bruker's on-instrument denoising was enabled for the ddaPASEF survey scans but not for the diaPASEF scans" (line 175), which explains the difference in reduction (53% vs. 40%) but also means the two modes are not directly comparable; this should be stated more prominently in the Results.

## Questions

- **Tables S10 and S11**: Are the 95% CIs for paired accuracy comparisons available, and do they overlap zero for the diaPASEF condition pairs where Figure 3 shows visible shifts?

- **Mobility-streak distribution of removed decoys**: Can you report the median number of consecutive occupied scans for removed target hits versus removed decoy hits under the streak filter, to show whether the decoy enrichment is driven by mobility sparsity or by intensity alone?

- **Generalization beyond the benchmark**: Do you have data from a second sample type (e.g., a complex cell lysate or low-input sample) showing whether the 35–53% reduction range holds, or is the claim restricted to three-species mixtures at 50 ng?