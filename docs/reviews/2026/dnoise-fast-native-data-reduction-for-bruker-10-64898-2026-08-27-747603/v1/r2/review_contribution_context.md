# Contribution & Prior-Work Reviewer

SCORE: 4
CONFIDENCE: 4

## Overall Assessment

dnoise presents a real and useful contribution: a native-format data reduction tool for Bruker timsTOF that removes uninformative points while preserving analytical results. The work is well-executed, thoroughly benchmarked, and addresses a genuine operational pain point in high-throughput proteomics. The novelty claim—that no open-source tool previously wrote reduced data back to native .d format—appears sound based on the literature record, though the contribution is primarily engineering rather than methodological. The manuscript is honest about limitations and the benchmark, while narrow, is rigorous within its scope.

## Strengths

1. The manuscript directly addresses a practical bottleneck (storage and transfer of dense timsTOF data) with a tool that produces native-compatible output, enabling immediate downstream use without format conversion.

2. The benchmark design is disciplined: a defined three-species mixture with known ratios, replicated across two acquisition modes and gradient lengths, with quantification validated against expected biological ratios rather than summary statistics alone.

3. The authors transparently report the confound (on-instrument MS1 denoising enabled only for ddaPASEF, not diaPASEF) and acknowledge that the 15-minute ddaPASEF results are not fully out-of-sample, rather than obscuring these limitations.

## Weaknesses: Load-Bearing Claims

**Claim 1: No prior open-source tool writes reduced data to native Bruker .d format.**

The manuscript states (lines 50–67): "To our knowledge, no open-source tool removes points and writes the result as a new native-compatible Bruker .d directory." The evidence is a literature survey showing that existing approaches either convert to mzML (lines 50–52), apply general compression (lines 53–54), operate on other ion-mobility platforms (line 55, PNNL PreProcessor), or export to MGF/feature lists (line 56, Wilding-McBride et al.). The reference list confirms Wilding-McBride et al. (ref. 14, PLoS One 2022) exists and is correctly characterized as exporting MGF or feature lists rather than native .d. The PNNL PreProcessor (ref. 7, J. Proteome Res. 2022) is cited as supporting other platforms but not Bruker .d. I found no contradicting published or preprint work in my search; the claim appears accurate. However, the claim is narrow: it is about *writing* native format, not about denoising itself. The novelty is primarily in the engineering choice to preserve native format compatibility, not in the filtering algorithms (streak filter, halo filter, geometric gates), which are conceptually straightforward. This is a real but incremental contribution.

**Claim 2: Default MS1-only denoising preserves label-free quantification accuracy and identification counts.**

The evidence is quantitative: ddaPASEF PSM, peptide, and protein-group counts are identical (Figure 2, line 186), and LFQ accuracy (observed vs. expected log₂ ratios) remains within the confidence intervals of the original arm across all species and condition pairs (Figure 3, lines 189–191). For diaPASEF, precursor and protein-group counts change by 0.2–2.2% and 0.2–1.6% respectively (lines 191–193), and median protein-level CV and LFQ accuracy are unchanged (lines 193–195). The mechanism is clear: MS1 filtering does not alter the MS/MS spectra used for identification in ddaPASEF, and in diaPASEF the fragment-based MaxLFQ quantification is unaffected by MS1 point removal. This claim is well-supported. The control experiment (Section 3.4, lines 260–285) comparing the streak filter to a matched-intensity threshold strengthens confidence: the streak filter outperforms the threshold on weak peptides (Figure S5) and preserves more searchable signal when extended to fragment frames. The alternative explanation—that the results reflect only the confound that MS1 filtering leaves MS/MS untouched—is explicitly acknowledged and is the correct interpretation for ddaPASEF. For diaPASEF, the small changes in precursor and protein counts are consistent with the claim but not definitive proof that quantification is preserved; the direct MS1-area check (Table S12) showing regulated-species ratios moving toward expected values is reassuring but indirect. The claim holds, but the evidence for diaPASEF is weaker than for ddaPASEF.

**Claim 3: The tool is fast enough for routine post-acquisition use.**

The evidence is runtime and memory measurements across all 72 benchmark files (Figure 6, Table S16): default MS1-only processing took 7.4–39.0 seconds, and MS1+MS/MS took 10.2–68.7 seconds, all shorter than the shortest gradient (5 minutes, 300 seconds). Peak working-set memory was 4.56 GB maximum. The claim is supported by the data. However, "routine post-acquisition use" assumes the tool will be run on a workstation with 20 threads and sufficient RAM; the manuscript does not address whether this is realistic for all laboratories or whether the tool scales to larger files or lower-resource environments. The benchmark is on a single instrument type (timsTOF Ultra 2) and a single sample type (three-species digest). Generalization is not claimed but should be noted.

## Weaknesses: Sweep

1. The parameter selection (min_feature_length=5, max_internal_gap=2) was optimized on the 15-minute ddaPASEF data (lines 91–109), making those results not fully out-of-sample; the authors acknowledge this but do not report sensitivity to parameter choice on the other three acquisition arms, leaving uncertainty about whether the defaults are robust across conditions.

2. The optional MS/MS denoising trades 7–12% of peptide identifications for 70–74% frame-binary reduction (Figure 2, lines 221–258), and the authors correctly note this is not analytically neutral, but the paper does not provide guidance on when this tradeoff is acceptable or how to choose parameters for different use cases.

3. The halo filter (removing points below 15% of local off-column maximum intensity) is presented as a small trim (Table S4) but is not validated independently; it could preferentially remove weak co-eluting ions, and no control experiment isolates its effect on quantification.

4. The benchmark uses a single three-species mixture at 50 ng load; validation on single-cell, sparse, or very low-input data is explicitly flagged as necessary (lines 318–329) but not provided, limiting the scope of the claim.

5. The manuscript does not compare dnoise to the PNNL PreProcessor on ion-mobility data from other platforms (e.g., Waters Vion, Agilent IM-QTOF) to establish whether the filtering strategy is platform-agnostic or timsTOF-specific.

6. The centroiding options (watershed and box, Section 3.5, lines 286–307) are presented as optional high-reduction operating points but are not integrated into the main narrative; their relationship to the default configuration and when they should be used is unclear.

## Questions

1. Table S1 lists "default" parameters, but were these parameters tuned on any subset of the benchmark data, and if so, which arms were excluded from the final evaluation to ensure out-of-sample validation?

2. Figure 5 shows feature-level intensity agreement across replicates, but does the alignment hold within each individual run, or only in aggregate across runs, and does this distinction affect the claim that quantification is preserved?

3. The manuscript states (line 73) that the halo filter "can be disabled because a sufficiently weak co-eluting ion could meet the same criteria"—does disabling it change the results, and if so, by how much?

---

## Context on Prior Work

The literature search confirmed the key citations: Wilding-McBride et al. (2022, PLoS One) on spectral simplification, the PNNL PreProcessor (Bilbao et al., 2022, J. Proteome Res.) on other ion-mobility platforms, and the MSFragger/IonQuant work (Yu et al., 2020, Mol. Cell. Proteomics) on timsTOF quantification. The Houthuijs et al. (2026, Anal. Chem.) reference on detector oscillation artifacts was confirmed in PubMed. No contradicting or directly competing native-format reduction tool was found in the literature or preprint record. The contribution is real: dnoise fills a gap in the toolchain by writing native .d output, which is genuinely useful for laboratories that want to reduce storage without format conversion. The novelty is primarily in the engineering choice and the validation on timsTOF, not in the filtering algorithms themselves.