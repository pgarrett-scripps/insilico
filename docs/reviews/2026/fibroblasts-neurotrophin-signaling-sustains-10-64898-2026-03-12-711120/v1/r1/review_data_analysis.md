# Statistics & Data-Analysis Reviewer

SCORE: 3
CONFIDENCE: 4

## Summary

This manuscript presents spatial transcriptomic evidence that neurotrophin signaling via NOTCH3-mediated induction sustains pathological vascular maturation in RA synovia despite immunosuppressive therapy, and demonstrates that FDA-approved TRK inhibitors can reverse this in tissue explants. The core biological claims are plausible and supported by coherent mechanistic data, but the quantitative evidence for the central finding—that vascular maturation *persists* despite treatment—rests on a denominator problem that conflates vascular expansion with treatment failure, and several key effect sizes lack the precision needed to support the therapeutic claims.

## Strengths

1. Spatial transcriptomics applied to paired pre/post-treatment biopsies (n=22 RA patients) is a rigorous design that avoids pseudo-replication and captures tissue architecture lost in dissociated single-cell studies.

2. Mechanistic pathway is traced from endothelial NOTCH3 through fibroblast NGF induction to mural cell differentiation, with orthogonal validation (RNAscope, immunohistochemistry, RNA-seq, functional assays) supporting each step.

3. Functional experiments (collagen gel contraction, organoid tube formation, explant treatment) demonstrate that neurotrophins are sufficient to induce mural cell phenotypes and that TRK inhibitors reverse maturation markers in human tissue.

## Weaknesses: Load-bearing claims

**Claim 1: Vascular maturation persists despite immunosuppressive treatment.** Figure 1G reports increased capillary EC density (p=0.00036 post-treatment vs. pre-treatment; p=0.0042 vs. healthy), increased pericytes (p=1.6e-05 vs. pre-treatment; p=0.029 vs. healthy), and increased VSMCs (p=0.0031 vs. pre-treatment; p=0.029 vs. healthy). However, vascular cell density is calculated as "proportion of vascular cells as a function of total surface area" (Methods). This denominator is the *total* synovial cellularity, which is expected to *decrease* with immunosuppression as immune infiltrates are depleted. A reduction in immune cells without change in absolute mural cell numbers would mechanically increase the proportion of vascular cells, producing the reported pattern without any increase in vascular maturation itself. The manuscript does not report absolute mural cell counts per unit tissue area, only proportions. Figure 1H reports "absolute cell proportion changes" but this is still a proportion (cells of type X / total cells), not an absolute count. To distinguish treatment-resistant vascular maturation from immune depletion-driven proportional shifts, the authors must report mural cell density normalized to tissue area alone, not to total cellularity. This is the central claim and it is not yet established.

**Claim 2: Neurotrophin signaling is necessary and sufficient for mural cell differentiation in RA.** Fibroblasts stimulated with NGF, BDNF, or NT3 show induction of mural markers (Fig. 4A–C), and knockdown of NGFR/NTRK1/2/3 reduces these markers (Fig. S4, S6). However, the effect sizes are modest: NGF induces RGS5 1.3-fold (p=0.0006), NT3 induces MYH11 2.9-fold (p=0.0001), and BDNF induces both. The collagen gel contraction assay (Fig. 4F) shows NT3 induces 21% contraction (p=0.002) and BDNF 16% (p=0.01), but NGF has "no significant effect." If NGF is the primary NOTCH3-induced neurotrophin (Fig. 5C–E), and NGF does not induce contractility, the functional significance of the NGF→NGFR→TRKA axis for VSMC maturation is unclear. The authors argue NGFR potentiates low-dose NGF sensitivity (Fig. 5G–H), but NGFR overexpression is a non-physiological condition. In intact RA tissue, whether endogenous NGFR levels are sufficient to sensitize fibroblasts to physiological NGF concentrations remains undemonstrated. The necessity claim (knockdowns) is stronger than the sufficiency claim (exogenous ligand at high doses).

**Claim 3: TRK inhibitors reverse pathological vascular maturation in RA.** Larotrectinib and entrectinib reduce aSMA staining by 36–40% (p=0.044, 0.034) and PECAM1+ vascular structures by 50–54% (p=0.04, 0.031) in synovial explants (Fig. 6E–F). However, these are short-term ex vivo experiments (3 days, Fig. 4G). The explants are cultured in EGM2 media, which contains growth factors that may not reflect the in vivo RA microenvironment. No dose-response curve is shown; only one concentration of each inhibitor is tested. The reduction in PECAM1+ structures could reflect endothelial cell death or reduced viability rather than reversal of maturation per se. Figure S9B shows no cytotoxicity at <100 µM, but the concentrations used in Fig. 6 are not stated. The claim that TRK inhibitors "reverse" maturation is supported only by reduction in markers; whether this represents dedifferentiation, cell death, or reduced proliferation is not distinguished. A time-course and dose-response, alongside viability assays at the concentrations used, would be needed to support therapeutic claims.

## Weaknesses: Sweep

1. **Multiple comparisons:** Figure 1G reports 8 vascular cell types × 3 groups (healthy, pre-treatment, post-treatment) = 24 comparisons without stated correction; the p-values reported (e.g., p=0.029) would not survive Bonferroni correction (threshold ~0.002), and no family-wise error control is disclosed.

2. **Sample size and pairing:** n=22 RA patients with paired pre/post biopsies is adequate for spatial transcriptomics, but the explant experiments (Figs. 4, 6) appear to use tissue from a subset of these patients or different cohorts; the number of independent tissue donors for each explant experiment is not stated, risking pseudo-replication if multiple explants from one patient are treated as independent replicates.

3. **Neurotrophin receptor expression:** NTRK1 (TRKA) is reported as "expressed, albeit at very low levels" (Fig. S2, text), yet the NGF→TRKA axis is central to the model; the absolute expression level and comparison to NTRK2/3 is not quantified, making it unclear whether TRKA is a physiologically relevant receptor or a minor off-target.

4. **NOTCH3 knockout validation:** NOTCH3 KO cells are generated by CRISPR-Cas9 (Methods) but no confirmation of knockout efficiency or off-target effects is shown; only the functional readout (NGF expression) is reported, not the genotype.

5. **Gene signature scoring:** The NGF/NGFR gene signature (Fig. 5K–M) is derived from bulk RNA-seq of NGFR-overexpressing fibroblasts treated with NGF, then projected onto spatial transcriptomics via UCell; this circular logic (training on NGFR-overexpression, then scoring NGFR-related genes in tissue) does not validate that the signature reflects endogenous neurotrophin signaling in vivo.

6. **Explant media:** EGM2 contains VEGF, FGF, and other growth factors; whether these confound the neurotrophin effect or whether the explant system recapitulates the RA microenvironment is not addressed.

7. **Statistical reporting:** Effect sizes (fold-change, % change) are reported but confidence intervals are absent; p-values are exact but often without test specification (e.g., Fig. 4A–C bar plots lack stated test, n, and error bar definition).

8. **Healthy donor controls:** Only 2 healthy donors are included in the spatial transcriptomics cohort (n=22 RA + 2 healthy); this is insufficient to establish a robust healthy baseline, and the comparison to healthy in Fig. 1G may be underpowered.

## Questions

1. **Figure 1G denominator:** Report mural cell density (cells per mm² tissue area) independent of total cellularity, to exclude the possibility that the post-treatment increase is a proportional artifact of immune depletion.

2. **Figure 6 concentrations and viability:** State the exact concentrations of larotrectinib and entrectinib used in Fig. 6C–F, and provide viability assays at those concentrations in the explant system (not just cultured fibroblasts in Fig. S9B).

3. **Explant sample size:** For Figs. 4 and 6, report the number of independent tissue donors and the number of explants per donor, with replication structure clearly stated to confirm independence.

4. **TRKA expression quantification:** Provide absolute transcript counts or relative expression levels (e.g., NTRK1 vs. NTRK2/3 in pericytes and VSMCs) to establish whether TRKA is a major or minor receptor in the tissue.

5. **NOTCH3 KO validation:** Show NOTCH3 genotype confirmation and off-target prediction for the guide RNA used in CRISPR experiments.