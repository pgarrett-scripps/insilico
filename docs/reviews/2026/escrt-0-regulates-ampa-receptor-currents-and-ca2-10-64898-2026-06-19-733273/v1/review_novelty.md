# Novelty & Contribution Reviewer

## Summary
The manuscript reports that the ESCRT-0 subunit Hrs localizes to the postsynaptic density, is bidirectionally regulated by neuronal activity, and modulates AMPA receptor function and CaMKII signaling. The contribution is real and incremental — each of the main findings extends a line of prior work the authors themselves have published — but the manuscript does not cleanly distinguish what is new relative to those earlier papers, and the central mechanistic claim (that Hrs sorts AMPARs for degradation at the PSD) is inferred rather than directly tested. The framing could be sharpened, and some results (the phosphoproteomics in particular) rest on thin statistical support.

## Weaknesses
- The fractionation data show Hrs in the PSD2 fraction, though PSD2 is prepared with 0.5% Triton X-100, which can co-purify endosomal membranes that resist detergent extraction.
- The phosphoproteomics of 924 quantified phosphopeptides, 16 pass an uncorrected p < 0.05 threshold; none would survive Benjamini–Hochberg correction at 5% FDR (expected false positives: ~46 at p < 0.05), and adjusted p-values are not reported.
- The manuscript does not show co-immunoprecipitation of Hrs with GluA1, nor test whether Hrs depletion alters GluA1 ubiquitination, nor whether the AMPAR kinetic changes depend on the Hrs ubiquitin-interacting motif (UIM).
- The AMPA/NMDA ratio is measured at 100 ms post-stimulation where the AMPAR current has largely decayed, so the ratio is dominated by NMDAR amplitude rather than reflecting the relative contributions of the two receptors to the synaptic response.
- The CaMKII data show a striking dissociation — reduced pCaMKII alongside increased total CaMKII — but the proposed explanation (impaired proteasomal turnover) is untested; an alternative is reduced neuronal activity with compensatory transcriptional response.
- The conclusion that Hrs overexpression effects are due to enhanced PKC activity is correlative; the authors do not measure PKC activity directly or show that the pGluA1-S831 increase is blocked by a PKC inhibitor.
- The Nedd4-1 colocalization experiment uses overexpressed GFP-Nedd4-1 and does not demonstrate that endogenous Nedd4-1 recruits Hrs to ubiquitinated AMPARs.
- There is no mention of STAM1, the other component of ESCRT-0; some effects could be due to unpartnered STAM1 rather than loss of ESCRT-0 function.

## Questions
- What are the FDR-adjusted p-values for the phosphopeptides in Figure 4?
- Does the AMPA/NMDA ratio difference hold with peak-to-peak (AMPAR peak / NMDAR peak) measurement rather than the 100 ms time point?
- Can the rise-time difference in Figure 3I be explained by a shift in AMPAR subunit composition (e.g., GluA1:GluA2 ratio or TARP association) rather than altered surface abundance?
- Is the increase in total CaMKII in Hrs-KO cortex (Fig. 5) due to increased transcription, increased protein stability, or both — and does it occur in the postsynaptic density fraction or only in the total lysate?
- Does Hrs co-immunoprecipitate with GluA1 under basal or activity-stimulated conditions?