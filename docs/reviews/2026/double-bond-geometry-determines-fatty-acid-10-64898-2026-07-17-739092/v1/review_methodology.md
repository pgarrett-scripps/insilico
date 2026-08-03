# Methodology Reviewer

## Summary
The manuscript makes a compelling conceptual advance but the methodology does not fully support its causal claims. The SCD mechanism for petroselaidic acid relies on indirect pharmacological/genetic evidence without direct biochemical validation. The phospholipid remodeling data are correlative; no experiment tests whether blocking specific remodeling events (diPUFA formation, sn-1 incorporation, arachidonate enrichment) abolishes ferroptosis sensitization. The primary screen uses only two cell lines and one inducer (RSL3), limiting generalizability of the hit identification.

## Strengths
- The FALCON screen design with dose-response and AUC quantification is rigorous and identifies unexpected trans-fatty acid hits.
- Complementary loss- and gain-of-function SCD experiments (inhibitor + inducible overexpression) strongly implicate SCD in petroselaidic acid metabolism.
- Multi-modal validation (multiple ferroptosis inducers, inhibitors, cell lines, and orthogonal lipid peroxidation assays) strengthens the core phenotype.

## Weaknesses
- The claim that SCD directly desaturates petroselaidic acid to a trans/cis-18:2 PUFA lacks direct biochemical evidence: no in vitro assay with purified SCD and petroselaidyl-CoA, and GC-FID identifies only a 'trans 18:2' peak without structural confirmation (e.g., MS/MS or NMR) that it is 6E,9Z-18:2. SCD inhibition globally depletes MUFAs and independently promotes ferroptosis, confounding the rescue interpretation.
- Phospholipid remodeling is presented as the mechanistic convergence point but remains correlative. No genetic or pharmacological perturbation of the specific remodeling pathways (e.g., ACSL4, LPCAT3, MBOAT1/2 for sn-1 incorporation or diPUFA generation) tests whether these changes are necessary for the ferroptosis sensitization by either trans fatty acid.
- The primary FALCON screen tests only two cancer cell lines (H460, U-2 OS) with a single GPX4 inhibitor (RSL3) at one timepoint. Hits are not validated in the screen against non-ferroptotic death or in non-cancer models, risking false positives from cell-line-specific metabolism or off-target toxicity at 1 mM fatty acid.
- Metabolic tracing uses endpoint GC-FID at limited timepoints without isotope tracing or flux analysis, so the relative contributions of direct incorporation vs. elongation/desaturation vs. remodeling cannot be quantified. The claim that linoleic acid does not convert to arachidonic acid in 24h is based on a single timepoint in one cell line.
- Targeted oxidized phospholipid analysis is restricted to PC species with available synthetic standards, omitting PE, PI, and other classes known to be ferroptosis-relevant. The authors acknowledge this limitation but the conclusion that linoelaidic acid generates 'unique oxidation products' is overstated given the narrow analytical window.

## Questions
- Was the 'trans 18:2' metabolite from petroselaidic acid structurally confirmed as 6E,9Z-18:2 (linopetroselaidic acid) by MS/MS or NMR, or is the assignment based solely on SCD's known Δ9 regioselectivity?
- In the SCD inhibition rescue (Fig 3D), SCD inhibitor alone increases RSL3 killing (Suppl Fig S4G,H). The combination of SCD inhibitor + petroselaidic acid returns death to BSA control levels — is this interpreted as petroselaidic acid's effect being blocked, or as two opposing effects canceling? How was this distinction made?
- For the lipidomics (Fig 6), were the sn-1/sn-2 assignments inferred from acyl chain composition or determined by positional analysis (e.g., phospholipase digestion)?