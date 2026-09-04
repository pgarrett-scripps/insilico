# Decision Letter

VERDICT: major

**Publication readiness:** 61/100

## Readiness Breakdown
- Scientific validity: 21/35
- Methods and evidence: 15/25
- Reproducibility and reporting: 11/20
- Clarity and completeness: 14/20

## Contribution Profile
- Novelty: moderate
- Significance: high
- Usefulness: high

## Score and Decision

The core observation — that mural cell coverage and arterial/capillary vascular structures persist and apparently expand in RA synovium after six months of csDMARD or TNFi therapy, and that a NOTCH3→NGF→NGFR/TRK axis can drive fibroblasts toward mural-cell marker programs — is interesting, internally consistent across five methodologically independent approaches, and translationally actionable. The ethics and compliance record is clean. What lowers readiness is not the plausibility of the model but three specific places where the stated conclusions run ahead of the evidence presented, each of which requires reanalysis or an additional control rather than rewording alone: (i) the headline "persistence despite treatment" claim is expressed in normalized units whose denominator plausibly changes with treatment, and the absolute-count analysis that would settle it is not shown; (ii) the explant TRK-inhibitor result — the basis for the therapeutic framing — reports a ~50% reduction in PECAM1⁺ structures with no viability or apoptosis control, so tissue toxicity is not excluded; (iii) the word "differentiation" in the title and throughout describes marker convergence and modest contractility, not fate. Reproducibility is further limited by absent sample sizes, no data or code deposition, an undocumented bulk RNA-seq pipeline that underpins the 461-gene signature, and three concrete citation errors.

None of these is fatal. The denominator issue is answerable by reanalysing data the authors already hold; the viability control is a single short experiment on material and models they have running; the differentiation language can be scaled to the evidence or supported with a trajectory analysis of existing data. Because at least one required item (absolute-density reanalysis) has an outcome that could change a conclusion, and one (explant viability) requires new data, this is a major revision rather than a long minor one. I would expect a revised version to be a strong paper.

## Summary of Evaluation

The panel converged on a shared view: the mechanistic pathway is well traced and the spatial dataset is valuable, but the two most quotable claims — treatment-resistant vascular maturation and drug-reversible maturation — each rest on a readout with an unexcluded alternative explanation.

On the denominator question, the advocate's defense in the debate is genuinely useful and I have weighed it: the reported pattern is selective (capillary/arteriolar ECs, pericytes and VSMCs rise; venular and lymphatic ECs do not), and a uniform shrinkage of the denominator would be expected to inflate all subtypes sharing it. That argument narrows the concern but does not close it, because immune infiltrate is not distributed uniformly with respect to vascular beds in RA synovium, and the manuscript never reports vascular cell counts per unit tissue area in absolute terms. The Methods also describe the density metric ambiguously ("proportion of vascular cells as a function of total surface area"), and the relationship between Fig. 1G and Fig. 1H denominators is not stated. This is straightforwardly resolvable from data in hand.

On the TRK-inhibitor explants, the advocate offered no counter-evidence on toxicity, and I agree with the skeptic that a 50–54% loss of PECAM1⁺ structures in 3-day explants is as consistent with reduced tissue viability as with de-maturation. The mechanistic conclusion survives either way; the translational framing does not.

On fibroblast origin, the advocate conceded the limitation and I accept the narrower claim as supported. The fix is either textual (recast as "neurotrophin signaling induces mural-cell programs in synovial fibroblasts") or evidentiary (trajectory/lineage analysis).

Several items raised in the reports were never contested in debate and I treat them as live: NOTCH3 as the primary rather than a sufficient NGF inducer; the overexpression-only basis for NGFR–TRKA potentiation given low endogenous NTRK1; absent multiple-comparison correction across ~18 comparisons in Fig. 1G; unreported CRISPR knockout validation; and the claim that vascular expansion occurred "regardless of whether patients reached clinical remission," which is asserted in the text with no supporting panel.

The compliance audits identified three HARD citation problems that must be corrected — most seriously, reference 16 (Domenga et al. 2004) is cited as "our previous study," which misattributes the authors' own prior findings. Methods completeness gaps are extensive but almost all text-and-file fixes; I have folded the load-bearing ones (bulk RNA-seq pipeline, data/code deposition, custom panel composition, oligo sequences, n reporting) into required revisions and routed the rest to suggestions.

## Required Revisions

1. **Resolve the normalization question for Fig. 1G–H with a reanalysis of the existing Xenium data.** Report, for each vascular subtype, (a) absolute cell counts per unit tissue area (cells/mm²) with the segmented tissue area stated per biopsy, and (b) at least one denominator-independent metric — e.g. pericyte:capillary-EC and VSMC:arteriolar-EC ratios, or mural cell counts per vessel cross-section. State explicitly and separately what denominator each panel of Fig. 1G and Fig. 1H uses. Also report total cell counts and immune-lineage counts per biopsy pre- and post-treatment so readers can judge denominator drift directly. If absolute vascular counts do not increase post-treatment, the claim must be restated as "vascular maturation is not reduced by treatment" rather than "increases."

2. **Add a viability/cell-death control to the TRK-inhibitor explant experiments (Fig. 6).** Report cleaved caspase-3 (or TUNEL) and an independent viability readout (LDH release or ATP) in vehicle- versus larotrectinib- and entrectinib-treated explants at the concentrations used, alongside a non-vascular structural control (e.g. lining-layer integrity, total DAPI⁺ nuclei per section). Report PECAM1⁺ cell number separately from PECAM1⁺ area. If endothelial loss cannot be distinguished from de-maturation, the abstract and Discussion must not describe the effect as "reversal of vascular maturation" without that qualification.

3. **Scale the "differentiation" claim to the evidence, or supply fate evidence.** Either (a) revise the title, abstract, Fig. 7 model and Results text to state that neurotrophin signaling induces mural-cell marker and contractile programs in synovial fibroblasts, explicitly listing recruitment, proliferation of pre-existing mural cells, and EndMT as unexcluded alternatives for the in vivo mural expansion; or (b) provide fate evidence — e.g. a trajectory/RNA-velocity or fibroblast-marker co-expression analysis in the existing Xenium data showing intermediate fibroblast/mural states, or lineage labelling in explants. Note that aSMA alone (Fig. 4K, Fig. 6) does not distinguish VSMCs from activated fibroblasts; state this.

4. **Report sample sizes and design for every quantitative panel.** For each figure and supplementary figure: n per condition, whether n denotes independent donors/cultures or technical replicates, and for explant and tissue experiments whether the design is paired (same donor across arms) or unpaired. Overlay raw data points on all bar plots. Report effect sizes with 95% confidence intervals alongside p-values for the headline numbers (aSMA reduction, PECAM1 reduction, contraction assay, all fold-changes quoted in the text).

5. **Apply and report multiple-comparison correction for the spatial comparisons.** Fig. 1G–H involves ~18 pairwise tests across six vascular subtypes and three groups. Report adjusted p-values (FDR or Bonferroni) and state the correction family. Report the significance threshold in Methods.

6. **Support or remove the remission-independence claim.** The statement that increased vascular density "occurred in RA patients regardless of whether or not patients reached criteria for clinical remission (DAS28-ESR < 2.6)" is currently unsupported by any panel. Provide the stratified analysis (with n per stratum, and acknowledgement that these strata are underpowered) or delete the claim.

7. **Constrain the NGFR–TRKA potentiation and NOTCH3-initiation claims to what was tested.** For NGFR: either add the knockdown counterpart — endogenous NGFR knockdown in DLL4-stimulated fibroblasts followed by pY-TRKA and RGS5/ABCC9 readout at ≤10 ng/mL NGF — or state in Results and Discussion that the potentiation mechanism is demonstrated only under CMV-driven overexpression and that endogenous NGFR has not been shown to be rate-limiting. For NOTCH3: report NGF mRNA and secreted protein in NOTCH3-KO versus wild-type fibroblasts *without* endothelial co-culture, so that "NOTCH3 is the key initiator" is distinguished from "NOTCH3 is sufficient to induce NGF"; alternatively temper to the latter and note that endothelial and other stromal NGF sources are not excluded.

8. **Document the bulk RNA-seq pipeline that generates the 461-gene NGF/NGFR signature.** State platform, library kit, read configuration, sequencing depth, number of replicates per arm, reference genome and build, alignment and quantification tools with versions, differential-expression tool, and the FDR/log-fold-change thresholds used to select the 461 genes. Provide the gene list as a supplementary table. Without these, Fig. 5J–M cannot be evaluated or reproduced.

9. **Deposit data and code with accessions.** Add a data-availability statement giving repository accessions for (a) Xenium raw and processed count matrices for all 46 samples, (b) the bulk RNA-seq, and (c) a persistent link (GitHub/Zenodo with DOI) to the analysis code, including the Seurat/Harmony/UCell scripts. Also specify the QC thresholds applied (minimum transcripts and features per cell), Louvain resolution and neighbour-graph parameters (resolution 0.3 is stated; the rest are not), and the composition of the custom Xenium add-on panels — Tables S1–S3 are referenced but were not supplied with the manuscript.

10. **Correct the three citation errors identified in the compliance audit.** (a) Reference 16 (Domenga et al., *Genes Dev* 2004) is cited in the Introduction as "our previous study" — correct the attribution and cite the appropriate work. (b) Reference 27 is listed only as "Website" with a DOI; supply full bibliographic details for a citation that supports the MYOCD/MYOCO claim in Fig. 5J. (c) Reference 13 (Veale & Fearon, psoriatic arthritis) is cited for RA synovial vascular remodeling; either replace with an RA-specific source or state the cross-disease inference explicitly.

11. **Validate the genetic perturbations.** Report NOTCH3 CRISPR knockout efficiency (sequencing of the edited locus, plus protein or transcript loss) for the cells used in Fig. 5E, and provide siRNA and gRNA target sequences (or complete vendor assay IDs sufficient for reordering, which are partly present) in a supplementary table. Report knockdown efficiency for each siRNA in the same experiments in which it is used, not only in Fig. S6.

12. **Address overlapping prior work in the Discussion.** Neurotrophin involvement in vascular remodeling in inflammatory vasculopathy (e.g. giant cell arteritis) and BDNF-dependent pericyte homeostasis have been reported outside RA, and NOTCH3 control of pericyte phenotype has been described in other tissues. Cite and position the present contribution against this literature, stating clearly what is new here (the NOTCH3→neurotrophin coupling in synovium and the druggability in human RA tissue) versus what extends established vascular biology to a new context.

## Minor Suggestions

- Report explant baseline characterization: whether vascular structure, mural markers and neurotrophin receptor expression drift during the initial 3-day culture period before treatment, and whether explants derive from the same cohort profiled in Fig. 1.
- Add antibody dilutions, host species and clone/RRID for all primaries (α-SMA in particular has no vendor or catalogue number), secondary dilutions, and the identity of the NGF ELISA kit.
- State vehicle identity and final vehicle concentration in medium for every small-molecule inhibitor and agonist, plus the vendor for polybrene.
- Provide microscopy acquisition details (objective NA, detector, illumination and exposure/gain settings) for the EVOS M7000 and identify the confocal instrument used for Fig. S5A; state ImageJ and R versions, Cellpose model and diameter parameter, and the thresholding/ROI procedure used for "integrated aSMA staining density."
- Report mycoplasma testing for primary fibroblasts and HUVECs, and record passage number per experiment given known passage-dependent drift in fibroblast phenotype.
- Add cohort demographics (age, sex, disease duration, seropositivity, inclusion/exclusion criteria) and an explicit informed-consent statement alongside the existing IRB numbers.
- Cell segmentation and CRISPR guide design are delegated to a bioRxiv preprint (ref. 1) by the same group; summarise the essential parameters in this manuscript so it remains self-contained if that preprint changes.
- Consider a positive-comparator arm in explants (e.g. PDGFR-β or angiopoietin/Tie blockade) to indicate whether TRK inhibition is distinctive rather than one of several routes to reduced mural coverage; this would substantially strengthen the necessity argument but is not required for this revision.
- The Discussion proposes that low endothelial NOTCH ligand favours pericyte fate via NGF/TRKA while high ligand favours VSMC fate via TRKB/TRKC. This is an attractive model but is not tested; label it explicitly as a hypothesis.
- Add a sentence on anticipated tolerability considerations for systemic TRK inhibition in patients already on immunosuppression, since the Discussion advocates repurposing.
- Typographical fixes in figure text: "POOXL"/"KOR"/"CO34"/"POGFRB" in the Fig. 1 description appear to be OCR corruptions of PODXL, KDR, CD34 and PDGFRB; "MYOCO" is presumably MYOCD; "vascualrization" and "vasculature" misspellings; Fig. S1/S2 titles begin "5ingle-cell".