# Citation Integrity Audit — "Using Alternative Proteases and Tandem Mass Tags"

## Scope and method

I checked the categories whose triggers appear in the manuscript: **reference resolvability**, **claim–citation support**, **quotation/number fidelity**, **self-citation/citation inflation**, and **retracted/predatory sources**. I verified resolvability of the load-bearing references via PubMed where the search budget allowed, and assessed claim–citation support from the manuscript text. Where a reference's contents could not be confirmed from the manuscript or the tools, I marked the finding **unverifiable** rather than asserting it is wrong.

The reference list as parsed contains 73 entries (with some duplication in the parse, e.g., refs 1 and 7 are the same Sidoli et al. work; refs 41 and 44 are the same Bao et al. work; ref 43 is a partial/merged entry). Several entries lack DOIs in the parse (e.g., refs 3, 4, 5, 6, 13, 14, 15, 16, 21, 22, 31, 32, 35, 36, 38, 39, 40, 42, 45–59, 60–73), but per the task instructions, a missing DOI in the parse is a gap in the parse unless the entry as printed also lacks it — I did not treat parse gaps as evidence of a missing identifier.

---

## Category 1: Reference resolvability

### Verified resolvable (present)

The following load-bearing references were confirmed to exist via PubMed:

| Ref | Work | Status |
|-----|------|--------|
| 2 | Garcia et al., *Nat. Protoc.* 2007 (PMID 17446892) | **present** |
| 1/7 | Sidoli et al., *J. Vis. Exp.* 2016 (PMID 27286567) | **present** |
| 9 | Meert et al., *Proteomics* 2016 (PMID 27139031) | **present** |
| 10 | Ryzhaya et al., *Anal. Chem.* 2025 (PMID 40505065) | **present** |
| 12 | Meert et al., *Proteomics* 2015 (PMID 26010583) | **present** |
| 19 | Weyh et al., *Nat. Chem.* 2024 (PMID 38531969) | **present** |
| 20 | Vai et al., *Mol. Cell. Proteomics* 2025 (PMID 41038282) | **present** |

### Unverifiable from available tools (question to authors)

- **Ref 18** (Zhang et al., *Nat. Chem. Biol.* 2011, "Identification of Lysine Succinylation as a New Post-Translational Modification") — this is a well-known paper and the citation is specific and plausible, but I could not confirm it via the search tools within budget. **Status: unverifiable** (not flagged as wrong). It is load-bearing for the claim that succinylation is a recognized histone PTM, but the claim is general and the citation is specific and standard, so this is a low-risk question rather than a HARD finding.
- **Ref 43** (Tan et al., *Cell Metab.* 2014, "Lysine Glutarylation Is a Protein Posttranslational Modification Regulated by SIRT5") — the parse shows this entry merged/truncated with the following entries. The citation is specific and standard, but I could not independently confirm it within budget. **Status: unverifiable** (question to authors).
- **Ref 16** (Adoni et al., *J. Proteome Res.* 2026, recombinant chymotrypsin analogue) — cited for the properties of r-Chymotrypsin. The citation is specific and plausible, but I could not confirm it within budget. **Status: unverifiable** (question to authors).

### No "(data not shown)", "(unpublished)", or "(in preparation)" citations found

I scanned the manuscript text for these triggers. None appear as load-bearing citations. **Status: not in play.**

---

## Category 2: Claim–citation support

### Findings

- **Ref 2 (Garcia et al., 2007)** is cited for the foundational propionylation workflow ("introducing a workflow that includes a chemical derivatization step to propionylate ε-amino groups of lysine and peptide N-termini"). This is the canonical description of that method and the claim is consistent with the reference. **Status: present** (plausibly supported).
- **Ref 10 (Ryzhaya et al., 2025)** is cited for the claim that "Arg-C Ultra... can be combined with peptide-level derivatization using trimethylacetic anhydride (TMA) to reduce histone sample preparation time to ~3-4 hours." This is a specific, checkable claim. The reference exists (PMID 40505065) and its title is consistent with a histone-preparation methods paper, but I could not inspect the full text to confirm the specific TMA/3–4 h claim. **Status: unverifiable** (question to authors — please confirm the TMA and ~3–4 h details are in ref 10).
- **Ref 20 (Vai et al., 2025)** is cited for the claim that HiP-Frag "identified 60 previously unreported modifications on core histones and 13 on linker histones across multiple cell lines and tissue samples." This is a specific quantitative claim. The reference exists (PMID 41038282) and its title matches an unrestricted PTM-search methods paper, but I could not inspect the full text to confirm the exact numbers 60 and 13. **Status: unverifiable** (question to authors — please confirm the 60/13 figures match ref 20).
- **Ref 9 and 12 (Meert et al., 2015, 2016)** are cited for the claim that propionylation "can be highly variable, with both under- and over-propionylation affecting downstream quantification." Both references exist and their titles directly concern propionylation pitfalls/overpropionylation, consistent with the claim. **Status: present** (plausibly supported).
- **Ref 18 (Zhang et al., 2011)** is cited for the claim that "succinylation as a histone PTM is thought to occur less frequently than acetylation and methylation." This is a general contextual claim; the reference is the canonical succinylation-identification paper. I could not confirm the specific "less frequently" framing within budget. **Status: unverifiable** (question to authors).
- **Ref 19 (Weyh et al., 2024)** is cited for the claim that "dysregulation of these modifications has been implicated in cancer, protein-protein and DNA-protein interactions, and defective DNA repair." The reference exists (PMID 38531969) and its topic (functional roles of succinylation/glutarylation) is consistent, but I could not inspect full text to confirm the specific disease/repair claims. **Status: unverifiable** (question to authors).
- **Ref 42 (Stransky et al., 2026, *Aging Cell*)** is cited for the claim that "an increase in global histone succinylation is associated with longevity." This is a specific claim attributed to a 2026 paper. I could not confirm this reference within budget. **Status: unverifiable** (question to authors — please confirm the reference exists and supports the longevity claim; note the 2026 date makes it a very recent citation).
- **Ref 48 (Li et al., *Cell Discov.* 2023)** is cited for the claim that "HDACs may play a more prominent role than sirtuins" in histone desuccinylation. This is a specific claim; I could not confirm the reference within budget. **Status: unverifiable** (question to authors).

### No central claim found resting on a clearly misattributed or unsupported citation

The manuscript's central claims (Arg-C Ultra efficiency, TMT charge-compensation for acidic acylations, dual-protease coverage) are supported by the manuscript's own experimental data (Figures 2–8), not by external citations. The external citations support contextual/methodological framing. **Status: no HARD claim–citation finding.**

---

## Category 3: Quotation/number fidelity

No direct quotations are used in the manuscript. Specific numbers attributed to sources are the Vai et al. 60/13 figures (ref 20) and the Ryzhaya et al. ~3–4 h figure (ref 10), both flagged above as **unverifiable** pending full-text confirmation. No other quoted statistics or values are attributed to sources in a way I could check. **Status: no confirmed discrepancies; two unverifiable numeric claims (see above).**

---

## Category 4: Self-citation / citation inflation

- The reference list includes multiple entries from the Yates lab (refs 1/7 Sidoli et al., 23 Diedrich et al., 66 MacCoss et al., 71–73 ProteomeXchange/PRIDE consortium papers). Refs 71–73 are data-repository citations appropriate to the deposited dataset (PXD073683) and are germane. Ref 23 (Diedrich et al., stepped collision energy) is directly germane to the TMT stepped-NCE method used. Refs 1/7 and 66 are methodological and germane.
- I found no conspicuous, non-germane self-citation or padding. The self-citations present are all topically relevant to the methods used. **Status: no finding (SOFT category, no trigger confirmed).**

---

## Category 5: Retracted / predatory sources

I identified no cited work as retracted or from a known predatory venue. All references I could verify are from established journals (*Nat. Protoc.*, *Anal. Chem.*, *Proteomics*, *Mol. Cell. Proteomics*, *Nat. Chem.*, *J. Vis. Exp.*). **Status: no finding.**

---

## Summary of findings

| # | Category | Finding | Severity | Status |
|---|----------|---------|----------|--------|
| 1 | Resolvability | Refs 1/2/7/9/10/12/19/20 confirmed resolvable via PubMed | — | present |
| 2 | Resolvability | Refs 16, 18, 43 could not be confirmed within budget | — | unverifiable (question) |
| 3 | Claim–citation | Ref 10 TMA/~3–4 h claim not confirmable from full text | SOFT | unverifiable (question) |
| 4 | Claim–citation | Ref 20 "60 core / 13 linker" figures not confirmable from full text | SOFT | unverifiable (question) |
| 5 | Claim–citation | Refs 9/12 propionylation-variability claim consistent with source titles | — | present |
| 6 | Claim–citation | Refs 18, 19, 42, 48 contextual claims not confirmable within budget | SOFT | unverifiable (question) |
| 7 | Number fidelity | No direct quotations; two numeric claims (refs 10, 20) unverifiable | SOFT | unverifiable (question) |
| 8 | Self-citation | No conspicuous non-germane self-citation found | — | no finding |
| 9 | Retracted/predatory | None identified | — | no finding |

**No HARD findings.** All flagged items are SOFT or unverifiable questions to the authors. The most useful follow-ups for the authors are to confirm (a) the specific TMA/3–4 h claim in ref 10, (b) the 60/13 figures in ref 20, and (c) that refs 42 and 48 exist and support the stated longevity and HDAC-desuccinylation claims respectively.