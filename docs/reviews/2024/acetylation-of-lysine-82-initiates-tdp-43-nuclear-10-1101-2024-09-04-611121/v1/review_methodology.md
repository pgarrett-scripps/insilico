# Methodology Reviewer

SCORE: 3
CONFIDENCE: 4

**Summary**

This manuscript reports a mechanistic pathway linking reduced proteasome activity to TDP-43 nuclear depletion and cytoplasmic accumulation, with lysine 82 acetylation identified as the critical post-translational modification disrupting the TDP-43–importin-α1 interaction. The design is generally sound, with appropriate use of multiple proteasome inhibitors, quantitative mass spectrometry, and mutagenesis to isolate the role of specific lysines. However, several load-bearing claims rest on designs that do not fully exclude alternative explanations, particularly regarding the specificity of the proteasome-inhibition effect, the causal role of acetylation versus other PTMs, and the interpretation of the sALS patient data.

**Strengths**

- The use of multiple orthogonal approaches (immunoblotting, live-cell imaging, mass spectrometry, peptide-binding assays) strengthens the central claim that proteasome inhibition disrupts TDP-43 nuclear import.
- The mutagenesis strategy systematically isolates lysine 82 as necessary and sufficient for the import disruption, with careful controls (e.g., 6KR vs. 14KR variants).
- The peptide-binding assay provides direct mechanistic evidence that K82 acetylation abolishes importin-α1 binding, complementing the in vivo findings.

**Weaknesses (load-bearing)**

1. **The claim that reduced proteasome activity *causes* TDP-43 mislocalization is not fully isolated from other effects of the inhibitors.** The manuscript uses three proteasome inhibitors (BTZ, MG132, MRZ) at doses that achieve ~50% inhibition, but these compounds are known to have additional effects (e.g., on non-proteasomal enzymes, cell signaling, or RNA processing). The control for this is the observation that FUS localization is unaffected, but FUS uses a different import pathway (importin-β2), so this does not rule out a general effect on importin-α1–mediated import. A stronger control would be to test another cNLS-dependent protein (e.g., a second importin-α1 cargo) under identical conditions. Without this, the claim that TDP-43 is uniquely sensitive to proteasome inhibition could reflect a broader disruption of the importin-α1 pathway rather than a TDP-43-specific mechanism.

2. **The causal role of acetylation at K82 is inferred from mimicking mutations (K82Q) and peptide-binding assays, but the direct evidence that acetylation occurs *in vivo* and drives the effect is incomplete.** The mass spectrometry identifies acetylation, ubiquitination, and phosphorylation at multiple lysines/serines within the cNLS after proteasome inhibition, but the manuscript does not quantify the relative abundance of each PTM or demonstrate that K82 acetylation is the dominant driver. The K82Q mimic abolishes import, but ubiquitination at K82 (also detected) could equally explain the effect, and the peptide-binding assay only tests acetylation. To distinguish, the authors would need to compare the binding of peptides with K82 acetylation versus K82 ubiquitination (or a ubiquitination mimic) to importin-α1. As written, the conclusion that acetylation specifically initiates the proteinopathy is not uniquely supported by the data.

3. **The sALS patient data are correlative and do not establish acetylation as an initiator.** The immunoblot shows increased K82 acetylation in all six sALS motor cortices versus controls, but this is a postmortem snapshot. The claim that acetylation "initiates" the proteinopathy requires temporal evidence (e.g., acetylation preceding phosphorylation or aggregation), which the manuscript attempts to support by showing acetylation in the NP-40-soluble fraction while phosphorylation is only in the insoluble fraction. However, this is a single case (#121) and the soluble/insoluble distinction is not validated as a reliable temporal marker. A stronger design would include multiple cases with graded proteinopathy severity and demonstrate that acetylation appears in cases with minimal or no phosphorylation/aggregation. Without this, the initiation claim outruns the evidence.

**Sweep (minor weaknesses)**

- The live-cell imaging of TDP-43-Clover relies on a fluorescent tag that may alter import kinetics; a control with untagged TDP-43 under identical conditions would strengthen the claim that the observed mislocalization is not an artefact of the tag.
- The siRNA-mediated depletion of endogenous TDP-43 (48 hr) followed by lentiviral expression of variants (72 hr) is a reasonable approach, but the manuscript does not report the efficiency of siRNA depletion or the residual endogenous TDP-43 level, which could confound the nuclear-localization measurements.
- The dose-response for proteasome inhibitors is shown for activity and viability, but the manuscript does not report a dose-response for TDP-43 mislocalization itself; a single dose (2 nM BTZ) is used for most experiments, leaving open whether the effect is dose-dependent or threshold-triggered.
- The claim that TDP-43 is "the protein whose nuclear localization is most sensitive" rests on a volcano plot of 5202 proteins, but the manuscript does not report the variance or confidence intervals for the TDP-43 measurement specifically; a single replicate per condition (as implied by the TMT design) may overstate the fold-change.
- The co-IP experiments for TDP-43–importin-α1 binding are qualitative (immunoblot only); a quantitative binding assay (e.g., ELISA or pull-down with molar ratios) would strengthen the claim that binding is "completely disrupted" versus merely reduced.

**Questions**

1. What is the relative abundance of K82 acetylation versus K82 ubiquitination in the mass spectrometry data, and does a ubiquitination-mimicking mutation (e.g., K82E) also abolish importin-α1 binding?
2. Can the authors provide a control experiment showing that another importin-α1–dependent protein (e.g., a second cNLS cargo) is *not* mislocalized under the same proteasome-inhibition conditions, to rule out a pathway-wide effect?
3. In the sALS cohort, is there a correlation between the degree of K82 acetylation and the extent of phosphorylated TDP-43 or cytoplasmic aggregation across all six cases, or is the association only qualitative?