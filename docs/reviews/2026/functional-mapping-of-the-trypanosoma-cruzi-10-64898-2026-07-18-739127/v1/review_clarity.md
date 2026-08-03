# Clarity & Presentation Reviewer

## Summary
The manuscript reports a valuable chemoproteomic resource but has several HARD clarity defects that impede a reader's ability to verify the central quantitative claims. The abstract's denominator for the 63% coverage statistic is ambiguous (35/37 vs 35/56), Table 2 lists two proteins as 'enriched' that a footnote admits were not detected by chemoproteomics, and the conservation analysis references Figure 4 (domain architectures) instead of the correct Supplementary Figure S3. These issues must be resolved before the evidence can be cleanly evaluated.

## Strengths
- The experimental workflow (live-cell ABPP with FP-alkyne probes, click chemistry, LFQ-MS) is described with sufficient procedural detail to be reproducible.
- Quantitative claims consistently report actual values (fold-change ranges, copy numbers, p-values, percentages) rather than vague qualifiers.
- The integration of in silico curation (catalytic triad geometry scoring with AlphaFold pLDDT thresholds) with experimental enrichment is logically structured and well motivated.

## Weaknesses
- The abstract states '37 enriched SH-like proteins, including 35 with conserved... catalytic triad/dyad features. The 35 SHs represent approximately 63% of the 56 predicted SHs' — a reader cannot tell whether the 35 is a subset of the 37 or of the 56 without reading the Discussion; the two denominators are conflated in a single paragraph.
- Table 2 is titled 'Serine hydrolases identified in T. cruzi' and the text says '37 non-redundant enriched SH-like proteins', but two entries (C4B63_10g142*, C4B63_25g255*) carry a footnote stating they 'were not detected by chemoproteomics assay'; listing non-enriched proteins in a table of enriched proteins without visual distinction or a separate category is misleading.
- The conservation summary ('29 present in both... two proteins absent from both') cites Figure 4, but Figure 4 shows Pfam domain architectures; the conservation data appear in Supplementary Figure S3, so the cross-reference is wrong.
- Figure 2's legend labels probe classes by color (alkyl/benzyl/aryl) but does not map the numbered structures (1–7) to those classes, forcing the reader to infer which probe is 'alkyl probe 1' or 'Probe 7' from the text.
- The manuscript lacks a dedicated Methods section; critical parameters (probe concentrations, incubation times, lysis buffer composition, LC-MS/MS settings, limma design matrix) are scattered across Results, figure legends, and Supplementary Data, making it unnecessarily hard to reconstruct the full protocol.
- Supplementary Data numbering is inconsistent: 'Supplementary Data 1', 'Supplementary Data 2-3', 'Supplementary Data 4', 'Supplementary Data 5', and 'Supplementary Data S4' are all used; a reader cannot reliably locate the referenced files.
- In Table 2, copy-number annotations for the same gene differ between assemblies (e.g., CPB1 shows '(12) (11)') but the text cites only '12 copies' without explaining the discrepancy or which assembly is authoritative.

## Questions
- Which 35 of the 37 proteins in Table 2 have conserved/partially conserved catalytic triads, and which two do not? (The footnote marks two as undetected, but the catalytic-status mapping is not shown.)
- Should C4B63_10g142* and C4B63_25g255* be excluded from the '37 enriched' count and the 63% coverage calculation?
- What are the exact probe concentrations, incubation times, and lysis conditions used for the whole-cell labelling? (Only 'optimisation of lysis conditions' is mentioned.)
- In Figure 3a, what does each column represent — individual probes or probe classes? The heatmap has 7 columns but the text describes a 'panel' of probes; the mapping is not explicit.