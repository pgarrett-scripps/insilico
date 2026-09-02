# Desk Screen Report: RIPUP Manuscript

## Summary
This is a methodological paper describing RIPUP (Rapid Identification of histone PTMs in Underivatized Peptides), a streamlined multi-protease mass spectrometry workflow for histone post-translational modification analysis. The authors systematically compare Arg-C Ultra and recombinant Chymotrypsin against the conventional Trypsin + propionylation approach, with and without TMT labeling, and demonstrate enhanced detection of negatively charged acylations (succinylation, glutarylation) using TMT.

## Scope Assessment

**In scope for In Silico?** Yes. This is original methodological research with empirical validation. The claims are checkable from the manuscript and deposited data (ProteomeXchange PXD073683, GitHub code provided). It addresses a real technical problem in epigenetics proteomics and offers practical solutions.

## Threshold Issues

### 1. Completeness of submission
✓ **Pass.** Full methods, results, figures, supplementary tables, data deposition, and code availability are provided. The manuscript is complete and intelligible.

### 2. Fundamental soundness
✓ **Pass.** The experimental design is appropriate for the question. The authors:
- Test multiple conditions systematically (10 distinct protease/derivatization combinations)
- Include technical replicates (n=4 for HEK293T, n=5 for rat hippocampus)
- Apply rigorous FDR control (1% at PSM and peptide levels)
- Use appropriate statistical methods (limma with Benjamini-Hochberg correction)
- Provide orthogonal validation (two proteases, two labeling strategies)
- Acknowledge limitations (single cell line for main comparisons, sequence coverage gaps)

The mechanistic explanation for TMT's advantage (tertiary amine charge compensation for acidic acylations) is plausible and supported by the data pattern.

### 3. Evidence-claim alignment
**Mostly sound, with one notable caveat:**

**Strong claims well-supported:**
- Arg-C Ultra outperforms Trypsin in digestion efficiency and peptide yield
- TMT labeling achieves ~92-99% efficiency vs. 29-71% for propionylation
- TMT preferentially detects succinylation (58 sites) and glutarylation (31 sites)
- Dual-protease approach provides complementary coverage (H2A, H1 variants)
- RIPUP achieves 231 PTM sites in rat hippocampus within 3 hours

**Claim requiring scrutiny:**
- The claim that succinylation/glutarylation represent a "dark epigenome" *largely undetected by propionylation-based methods* is well-demonstrated empirically here, but the authors acknowledge (appropriately) that this reflects a mechanistic limitation of propionylation, not necessarily that these sites were previously unknown in the field. The novelty is in the detection method, not necessarily in the biological discovery. This is stated clearly enough that it does not constitute overstatement.

### 4. Reproducibility and transparency
✓ **Pass.** 
- Raw MS data deposited (ProteomeXchange)
- Custom R scripts on GitHub
- Detailed methods (main text + SI)
- Digestion parameters, search settings, and variable modifications fully specified
- Labeling efficiency metrics clearly defined and reported
- Quantitative analysis approach (histone-level normalization, kNN imputation, limma) is transparent

### 5. Novelty and contribution
✓ **Adequate.** This is methodological work, not a breakthrough discovery. The contribution is:
- **Systematic comparison** of alternative proteases (Arg-C Ultra, r-Chymotrypsin) vs. standard Trypsin—this comparison has not been done comprehensively for histone PTMs
- **TMT as a derivatization agent** for histone PTMs—while TMT has been used in other contexts, its systematic evaluation against propionylation for histone analysis is novel
- **Mechanistic insight** into why TMT rescues acidic acylation detection
- **Practical workflow** (RIPUP) that reduces preparation time from ~6+ hours to ~3 hours

This is incremental but solid methodological progress. The field will benefit from knowing that TMT enables detection of a PTM class previously suppressed by propionylation.

### 6. Clarity and honesty
✓ **Pass.** The authors:
- Clearly state limitations (single cell line, sequence coverage gaps, computational constraints)
- Acknowledge that their propionylation protocol uses ammonium-containing buffers that reduce efficiency relative to optimized approaches
- Distinguish between what they demonstrate (method advantage) and what would require further validation (biological prevalence of succinylation/glutarylation)
- Provide cost analysis and practical considerations

## Potential Reviewer Concerns (not desk-reject issues)

1. **Limited biological validation:** The NAM experiment is a proof-of-concept in vitro model. Validation in additional cell types or tissues would strengthen claims about general applicability.

2. **r-Chymotrypsin availability:** The paper notes r-Chymotrypsin is available only under "Early Access" from Promega. This may limit immediate adoption, though it does not invalidate the method.

3. **Succinylation/glutarylation interpretation:** The authors detect these sites but do not provide independent validation (e.g., synthetic peptides, targeted MS/MS). However, they acknowledge this and note that pragmatic validation (as used in HiP-Frag) is appropriate for PTM discovery at this scale.

4. **Generalizability:** Comparisons focus on HEK293T cells. The hippocampal proof-of-concept is encouraging but limited (n=5 animals, one tissue type).

These are appropriate topics for reviewer discussion but do not constitute threshold problems.

## Fit for In Silico

The manuscript is **in scope**: it presents original methodological research with checkable claims, deposited data, and transparent reporting. It is not a clinical trial, diagnostic guidance, or work with inaccessible evidence. The central claims can be evaluated from the manuscript and supplementary materials.

The work is **above the venue's bar**: it is technically sound, clearly reported, and makes a useful contribution to an established field. It is not groundbreaking, but that is not required.

---

## DESK DECISION: proceed

**Rationale:** This is a well-executed methodological study with complete data, transparent reporting, and sound experimental design. The claims are appropriately scaled to the evidence. While the work is incremental rather than transformative, it addresses a real technical problem in histone PTM analysis and provides practical solutions with mechanistic insight. It merits full peer review.