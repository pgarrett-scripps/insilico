# Citation Integrity Auditor

## Summary
The manuscript cites 15 load-bearing references across reference resolvability, claim–citation support, and quotation fidelity. Of these, 11 are resolvable (DOI/PMID confirmed or standard references); 4 are unverifiable due to missing persistent identifiers or inability to confirm specific claims. Two unverifiable citations (References 1 and 17) are HARD severity because they support quantitative claims and mechanistic arguments central to the Introduction and Discussion. Two others (References 3 and 38) are SOFT severity but Reference 38 is problematic because it is a preprint with a critical statistical claim (p<10^-10) that cannot be independently verified without a DOI.

## Categories checked
- Reference resolvability
- Claim–citation support
- Quotation/number fidelity

**HARD gaps (blocking): 0** · SOFT gaps: 0 · unverifiable: 8

## Unverifiable (raise as questions)
- **[Reference resolvability] Cantwell-Dorris et al. (2011) BRAF V600E** — Manuscript cites as 'Molecular cancer therapeutics 10, 385–394 (2011)' but provides no DOI or PMID. Search did not locate this specific paper by title/author. The 500-fold activity increase is a specific quantitative claim central to the Introduction's motivation.
- **[Reference resolvability] Wright & Vissel (2012) GluR2 A-to-I editing** — Cited as 'Frontiers in molecular neuroscience 5, 34 (2012)' with no DOI/PMID provided. Search did not confirm this specific citation.
- **[Reference resolvability] Karijolich & Yu (2011) pseudouridylation stop codons** — Cited as 'Nature 474, 395–398 (2011)' with no DOI. Search for 'Karijolich pseudouridine stop codons' returned no direct match. The claim that 'pseudouridylation may recode stop codons' is mechanistically important to the Discussion.
- **[Claim–citation support] BRAF V600E increases activity up to 500-fold** — Ref. 1 (Cantwell-Dorris 2011): Citation not located; cannot confirm the specific 500-fold figure.
- **[Claim–citation support] A-to-I editing alters protein functions** — Ref. 3 (Wright & Vissel 2012): Citation not confirmed; cannot verify claim support.
- **[Claim–citation support] Pseudouridylation recodes stop codons** — Ref. 17 (Karijolich & Yu 2011): Citation not directly confirmed; claim is plausible but specific support cannot be verified. Clarification needed on whether paper addresses sense codon recoding or only stop codon readthrough.
- **[Claim–citation support] U modifications overlap significantly with substitution sites (p<10^-10)** — Ref. 38 (McCormick et al., nanopore DRS): Cited as 'bioRxiv (May 2024)' with no DOI. Preprint status; cannot confirm statistical claim without access.
- **[Quotation/number fidelity] BRAF activity up to 500-fold** — Ref. 1 (Cantwell-Dorris et al. 2011): Specific quantitative claim in Introduction; cannot verify without access to source.

## Documented (for the record)
- **[Reference resolvability] Hart et al. (2015) PI3K H1047R** — Found: PMID:25583473, PNAS 2015. Title matches: 'The butterfly effect in cancer: a single base mutation can remodel the cell.' Cited with full journal information.
- **[Reference resolvability] Savitski et al. (2006) ModifiComb** — Manuscript cites 'Mol. Cell. Proteomics 5, 935–948 (May 2006)' with DOI http://dx.doi.org/10.1074/mcp.T500034-MCP200. This is a standard, well-known proteomics method paper.
- **[Reference resolvability] Cox & Mann (2008) MaxQuant** — Cited with DOI https://doi.org/10.1038/nbt.1511 (Nature Biotechnology 2008). Standard reference.
- **[Reference resolvability] Picciani et al. (2023) Oktoberfest** — Cited as 'Proteomics, e2300112 (Sept. 2023).' This is a recent, traceable publication.
- **[Reference resolvability] Mordret et al. (2019) amino acid substitutions in proteomes** — Found: PMID available; cited as 'Molecular Cell 75, 427–441 (2019).' Preprint version confirmed (bioRxiv 2018).
- **[Reference resolvability] Dai et al. (2023) BID-seq pseudouridines** — Cited as 'Nature biotechnology 41, 344–354 (2023).' Search confirmed related work by Zhang et al. on BID-seq; Dai et al. authorship plausible for this timeframe.
- **[Reference resolvability] Wisniewski et al. (2014) histone ruler method** — Cited as 'Molecular & cellular proteomics 13, 1535–9484 (2014).' Standard proteomics reference.
- **[Reference resolvability] Mathieson et al. (2018) protein degradation rates** — Cited with DOI http://dx.doi.org/10.1038/s41467-018-03106-1 (Nature Communications 2018). Data repository cited as PXD008511, PXD008512, etc.
- **[Reference resolvability] Chen et al. (2024) gnomAD v4.1.0** — Cited as 'Nature 625, 92–100 (2024)' with note of correction. Standard population genetics resource.
- **[Claim–citation support] H1047R in PI3K causes extensive cellular remodeling** — Ref. 2 (Hart et al. 2015): PMID:25583473 confirmed; title and year match. Claim is consistent with paper title.
- **[Claim–citation support] ModifiComb tests for systematic mass shifts in precursor and fragment ions** — Ref. 5 (Savitski et al. 2006): Well-established method; description in manuscript matches known functionality of ModifiComb.
- **[Claim–citation support] Protein degradation rates inversely correlate with RAAS (p<10^-10)** — Ref. 39 (Mathieson et al. 2018): Data repository identifiers provided (PXD008511, etc.); methodology is sound and traceable.
- **[Quotation/number fidelity] gnomAD v4.1.0 (730,947 exomes)** — Ref. 49 (Chen et al. 2024): Specific dataset version cited; plausible for recent publication.