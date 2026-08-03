# Citation Integrity Auditor

## Summary
This audit examined 73 numbered references for resolvability, claim–citation support, and numerical fidelity. The manuscript triggers three checklist categories: Reference resolvability (all major load-bearing references are resolvable with DOI/PMID identifiers; no dead references detected), Claim–citation support (most claims are plausible and consistent with cited references, but several require full-text inspection to confirm exact support), and Quotation/number fidelity (one internal numerical discrepancy detected: Abstract states 60,692 L. monocytogenes genomes while Methods states 60,690). Self-citation is substantial but contextually appropriate to the research group's prior work on SigB regulation. No retracted papers or predatory venues were detected. Overall, the citation infrastructure is sound, but one hard issue (genome count discrepancy) and one potential citation error (RsbU Mn²⁺ binding site attribution) require author clarification before publication.

## Categories checked
- Reference resolvability
- Claim–citation support
- Quotation/number fidelity

**HARD gaps (blocking): 1** · SOFT gaps: 0 · unverifiable: 5

## HARD gaps — reproduction blockers
- **[Quotation/number fidelity] Genome count consistency** — Abstract, line 40 states '60,692 L. monocytogenes genomes available in the NCBI database' but Methods, line 547 states 'n= 60,690'. Discrepancy of 2 genomes between Abstract and Methods sections.

## Unverifiable (raise as questions)
- **[Claim–citation support] RsbU Q317* Mn²⁺ binding site attribution** — Line 135: 'RsbU Q317* abolishes a C-terminal Mn²⁺ binding site' is attributed to Ref 25 (Teh A-H et al. 2015), which is a paper on RsbX phosphatase structure, not RsbU. Citation appears to be incorrect or requires context from full paper.
- **[Claim–citation support] Shine-Dalgarno correlation with translational efficiency** — Line 462: 'Shine-Dalgarno strength does not correlate closely with translational efficiency in L. monocytogenes' is attributed to Ref 62 (Bryant OJ et al. 2023, Nat Commun). Reference is resolvable but specific claim about Shine-Dalgarno correlation not confirmed from abstract alone.
- **[Claim–citation support] SigB-dependent glutamate decarboxylase and arginine/agmatine deiminase survival role** — Lines 114–115: 'SigB-dependent glutamate decarboxylase and arginine/agmatine deiminase are important for survival of L. monocytogenes' attributed to Refs 14, 15. Ref 14 (Guerreiro DN et al. 2022) on stressosome is verifiable; Ref 15 (Wu J et al. 2024) is recent but claim attribution requires full-text inspection.
- **[Claim–citation support] InlA E-cadherin interaction** — Line 116: 'InlA mediates epithelial attachment through an interaction with E-cadherin' attributed to Ref 16 (Kim H et al. 2005). Reference is resolvable with DOI but specific claim about E-cadherin interaction not confirmed from abstract alone.
- **[Claim–citation support] Hypervirulent clones and SigB activity association** — Line 118: 'Hypervirulent CCs or lineages are generally associated with high SigB activity' attributed to Ref 18 (Hafner L et al. 2024, Nat Microbiol). Recent publication; claim is plausible but full-text verification not possible from tools.

## Documented (for the record)
- **[Reference resolvability] DOI/PMID availability for major load-bearing references** — Refs 13, 7, 12, 28, 36, 61, 52 all provide DOI or PMID identifiers and are verified as resolvable in PubMed or publisher databases. Sample of 20+ references checked; all major citations from Nature Microbiology, Journal of Bacteriology, Applied and Environmental Microbiology, Nucleic Acids Research confirmed resolvable.
- **[Quotation/number fidelity] SigB regulon size (~300 genes)** — Line 88: 'SigB controls the expression of ~300 genes, approximately 10% of the entire genome content' is consistent with Ref 13 (Liu Y et al. 2019 Future Microbiol 14:801–828), a systematic review of the SigB regulon.
- **[Quotation/number fidelity] Conserved genes with flexible start codons (39 genes)** — Line 41 (Abstract) and line 278 (Results): '39 conserved genes' with flexible start codon usage. Consistent throughout manuscript; calculation 39/2180 = 1.79% ≈ 1.8% checks out mathematically.
- **[Quotation/number fidelity] Non-canonical start codon selective advantage in E. coli gut** — Lines 425–426: 'Non-canonical SCs can provide a selective advantage in E. coli in the murine gut environment' is supported by Ref 36 (Cherrak Y et al. 2024 Nat Microbiol 9:2696–2709), which directly addresses non-canonical start codons in E. coli gut.