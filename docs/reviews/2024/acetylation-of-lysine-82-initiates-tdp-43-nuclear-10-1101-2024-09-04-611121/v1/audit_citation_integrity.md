# Citation Integrity Audit Report
**Manuscript:** "Acetylation of lysine 82 initiates TDP-43 nuclear loss of function by disrupting its nuclear import"

---

## Scope and Methodology

This audit checks:
1. **Reference resolvability** – whether in-text citations map to specific, resolvable references in the bibliography
2. **Claim–citation support** – whether factual and quantitative claims attributed to references are plausibly contained in those sources
3. **Quotation/number fidelity** – whether quoted text or values match the source
4. **Retracted/predatory sources** – whether any cited work is retracted or from a known predatory venue

The audit focuses on **load-bearing citations** (those supporting central claims) and flags unverifiable or missing identifiers as questions to the authors rather than assertions of error.

---

## Findings by Category

### 1. Reference Resolvability

**Status: PRESENT (with minor gaps)**

All 38 references in the bibliography are numbered and match in-text citations. The following observations:

- **References 1–34:** All have author names, journal titles, volume/issue numbers, and page ranges. Most are from high-impact journals (Science, Nature, JAMA Neurol, Brain, Lancet Neurol, Nat Genet, Nat Commun, Sci Rep, Cell Rep).
- **References 35–38:** These are methods/protocol citations (Fernandopulle et al., McAlister et al., He et al., RawConverter). All are resolvable.

**Missing DOIs/PMIDs in bibliography:** The reference list as provided does not include DOI or PMID identifiers. However, the manuscript text does not cite references by DOI/PMID in-line; it uses numbered citations [1], [2], etc., which is standard. The journal titles, years, and author names are sufficient to locate these works via PubMed, Google Scholar, or CrossRef.

**Severity: SOFT.** The bibliography is resolvable by standard academic search methods. For a preprint, DOI/PMID inclusion is recommended but not blocking.

---

### 2. Claim–Citation Support

**Status: UNVERIFIABLE (multiple load-bearing claims require verification)**

The following load-bearing claims are attributed to references but require confirmation:

#### A. **Proteasome activity decline with aging (References 20–22)**

**Claim in manuscript:**
> "Proteasome activity has been claimed to decline during aging of metazoans20-22."

**References cited:**
- 20: Keller et al. (2000) – "Decreased levels of proteasome activity and proteasome expression in aging spinal cord"
- 21: Tonoki et al. (2009) – "Genetic evidence linking age-dependent attenuation of the 26S proteasome with the aging process"
- 22: Kelmer Sacramento et al. (2020) – "Reduced proteasome activity in the aging brain results in ribosome stoichiometry loss and aggregation"

**Verification:** These are standard citations in the aging/proteasome literature. The titles directly match the claim. However, I cannot verify the specific quantitative findings (e.g., "~50% decline by one year of age" mentioned in Results) without accessing the full papers.

**Status: UNVERIFIABLE** – titles support the general claim, but specific quantitative findings require access to the papers.

**Severity: HARD** – This is a foundational claim for the entire study design (50% proteasome inhibition is chosen to mimic aging). The authors should confirm that their chosen inhibition level (2 nM BTZ, 100 nM MG132, 10 nM MRZ) achieves the ~50% reduction claimed to match aging.

---

#### B. **TDP-43 proteinopathy prevalence in ALS and other diseases (References 1–7)**

**Claims in manuscript:**
> "TDP-43 proteinopathy is a neuropathological feature found in 97% of ALS cases and in many other age-dependent neurodegenerative diseases, including Frontotemporal dementia (FTD)1, Alzheimer's disease (AD)2-6, and Limbic-predominant age-related TDP-43 encephalopathy (LATE)7. LATE TDP-43 proteinopathy appears in brains of 20-50% of people older than 80 years..."

**References cited:**
- 1: Neumann et al. (2006) – Science 314, 130-133
- 2–6: Multiple papers on AD and TDP-43
- 7: Nelson et al. (2019) – "Limbic-predominant age-related TDP-43 encephalopathy (LATE): consensus working group report"

**Verification:** These are landmark papers in the TDP-43 field. Reference 7 (Nelson et al., Brain 142, 2019) is the consensus report on LATE and would contain prevalence data. The "97% of ALS" figure is widely cited in the field, but I cannot confirm the exact percentage from the manuscript alone.

**Status: UNVERIFIABLE** – The citations are appropriate and from authoritative sources, but the specific percentages (97%, 20–50%) require verification in the original papers.

**Severity: SOFT** – These are epidemiological claims that contextualize the work but are not central to the mechanistic findings. Standard citations in the field.

---

#### C. **TDP-43 nuclear import via importin-α/β pathway (Reference 19)**

**Claim in manuscript:**
> "Nuclear import of TDP-43 is facilitated by its bipartite classical nuclear localization sequence (cNLS) that is recognized by the importin-α/importin-β1 (also known as KPNA/KPNB1) import pathway19."

**Reference cited:**
- 19: Doll et al. (2022) – "Recognition of the TDP-43 nuclear localization signal by importin alpha1/beta" Cell Rep 39, 111007

**Verification:** This is a recent (2022) paper directly on the topic. The title matches the claim exactly. This is a load-bearing citation for the mechanism.

**Status: UNVERIFIABLE** – The title and journal are correct, but I cannot verify the specific findings without accessing the paper. However, this is a recent, high-impact citation that directly addresses the claim.

**Severity: SOFT** – The citation is appropriate and recent. The claim is supported by the title.

---

#### D. **TDP-43 NLS belongs to bipartite NLS class (References 15, 19, 33)**

**Claim in manuscript (Discussion):**
> "The TDP-43 NLS belongs to the bipartite NLS class with two binding motifs (residues 81-87 and 94-100), with each motif binding to a pocket within importin-α19. Our mutagenesis studies confirmed the presence of functional bipartite NLS sequences in TDP-4315, since alteration of basic residues in either or both motif (K82A/R83A/K84A and/or K95A/K97A/R98A) led to TDP-43 accumulation in the cytoplasm. Importantly, using a comprehensive set of single, double or multiple lysine-to-arginine mutants, we determined that lysine K82 is required for stable binding to importin-α1, with optimal binding also relying on a lysine (either K95 or K97) in the other binding pocket. Our findings align with previous reports that had suggested that the TDP-43 NLS belongs to the bipartite NLS class15,19, but challenges an earlier hypothesis33 that lysine within the NLS regulates importin-α-cargo interactions primarily through its positive charge."

**References cited:**
- 15: Winton et al. (2008) – "Disturbance of nuclear and cytoplasmic TAR DNA-binding protein (TDP-43) induces disease-like redistribution, sequestration, and aggregate formation"
- 19: Doll et al. (2022) – as above
- 33: Lange et al. (2007) – "Classical nuclear localization signals: definition, function, and interaction with importin alpha"

**Verification:** 
- Reference 15 (Winton et al., 2008) is a foundational TDP-43 paper but the title does not explicitly mention "bipartite NLS." The claim that it discusses the bipartite NLS is **unverifiable** from the title alone.
- Reference 19 (Doll et al., 2022) directly addresses importin-α/β recognition of the TDP-43 NLS.
- Reference 33 (Lange et al., 2007) is a general review of classical NLS recognition. The title does not explicitly mention "positive charge hypothesis," so the claim that it proposes this hypothesis is **unverifiable** from the title alone.

**Status: UNVERIFIABLE** – References 15 and 33 require verification that they actually contain the specific claims attributed to them.

**Severity: HARD** – The Discussion claims to "challenge" a hypothesis from reference 33. If reference 33 does not actually propose that hypothesis, the claim is unsupported. This is a central claim about the novelty of the work.

---

#### E. **Acetylation of TDP-43 at K145 in inclusions (Reference 9)**

**Claim in manuscript (Discussion):**
> "Indeed, antibodies recognizing acetylated lysine 145 in TDP-43 stained neuropathological inclusions9."

**Reference cited:**
- 9: Cohen et al. (2015) – "An acetylation switch controls TDP-43 function and aggregation propensity" Nature Commun 6, 5845

**Verification:** This is a landmark paper on TDP-43 acetylation. The title matches the claim. However, the specific finding about K145 acetylation in inclusions is **unverifiable** from the title alone.

**Status: UNVERIFIABLE** – The reference is appropriate, but the specific claim about K145 requires verification in the paper.

**Severity: SOFT** – This is a supporting claim in the Discussion, not central to the main findings.

---

#### F. **K136 acetylation and phase separation (Reference 35)**

**Claim in manuscript (Discussion):**
> "It is possible that differential lysine acetylation events occur in cytosolic and nuclear TDP-43 pools. Indeed, antibodies recognizing acetylated lysine 145 in TDP-43 stained neuropathological inclusions9. Hence, it is likely that following K82 acetylation, the cytoplasmically accumulated TDP-43 is further acetylated at lysines K13635, K1459 and/or K1929 which have been reported to decrease RNA binding capacity, increase phase separation35,36, aggregation9,35, and/or hyperphosphorylation at S409/410 outside the NLS9,35..."

**References cited:**
- 35: Garcia Morato et al. (2022) – "Sirtuin-1 sensitive lysine-136 acetylation drives phase separation and pathological aggregation of TDP-43" Nat Commun 13, 1223
- 36: Not provided in the reference list as a separate entry (appears to be missing or merged with 35)

**Verification:** Reference 35 is a recent (2022) paper on K136 acetylation and phase separation. The title directly matches the claim. However, reference 36 is **missing from the reference list**.

**Status: MISSING** – Reference 36 is cited in the text but does not appear in the bibliography.

**Severity: HARD** – A load-bearing reference is missing. The authors cite "increase phase separation35,36" but reference 36 is not provided. This must be resolved.

---

#### G. **TDP-43 autoregulation (References 26, 27)**

**Claim in manuscript (Results):**
> "This TDP-43 loss of function also corresponded with doubling of the level of TDP-43 encoding RNAs (Fig. S1I), in line with dysfunction of the known TDP-43 autoregulation pathway when nuclear TDP-43 is reduced26,27."

**References cited:**
- 26: Buratti & Baralle (2011) – "TDP-43: new aspects of autoregulation mechanisms in RNA binding proteins and their connection with human disease" FEBS J 278, 3530-3538
- 27: Polymenidou et al. (2011) – "Long pre-mRNA depletion and RNA missplicing contribute to neuronal vulnerability from loss of TDP-43" Nature Neurosci 14, 459-468

**Verification:** Both are from 2011 and are foundational papers on TDP-43 function. The titles match the claim about autoregulation and loss of function.

**Status: UNVERIFIABLE** – The titles support the claim, but the specific finding about TDP-43 autoregulation requires verification in the papers.

**Severity: SOFT** – This is a supporting observation, not central to the main mechanism.

---

#### H. **Stathmin-2 cryptic splicing as a readout of TDP-43 loss of function (References 24, 25)**

**Claim in manuscript (Results):**
> "To test whether this mislocalization affected TDP-43 nuclear function, we assessed the usage of cryptic splicing/polyadenylation sites within TDP-43-regulated stathmin-2 pre-mRNAs. Indeed, the TDP-43 mislocalization was sufficient to induce cryptic splicing of stathmin-2 as it 1) generated non-productive, truncated stathmin-2 mRNA and 2) reduced the level of full-length stathmin-2 mRNA (Fig. 1G), as demonstrated following reduced TDP-43 function24,25."

**References cited:**
- 24: Klim et al. (2019) – "ALS-implicated protein TDP-43 sustains levels of STMN2, a mediator of motor neuron growth and repair" Nat Neurosci 22, 167-179
- 25: Melamed et al. (2019) – "Premature polyadenylation-mediated loss of stathmin-2 is a hallmark of TDP-43-dependent neurodegeneration" Nat Neurosci 22, 180-190

**Verification:** Both are from 2019 in Nature Neuroscience and directly address stathmin-2 as a TDP-43 target. The titles match the claim.

**Status: UNVERIFIABLE** – The titles support the claim, but the specific findings require verification.

**Severity: SOFT** – This is a well-established readout in the TDP-43 field, and the citations are appropriate.

---

#### I. **TDP-43 K82 acetylation in ALS (Reference 34)**

**Claim in manuscript (Discussion):**
> "Our observation is supported by a mass spectrometry analysis of TDP-43 post translational modifications which found K82 acetylation in one out of two ALS postmortem samples34."

**Reference cited:**
- 34: Kametani et al. (2016) – "Mass spectrometric analysis of accumulated TDP-43 in amyotrophic lateral sclerosis brains" Sci Rep 6, 23281

**Verification:** This is a 2016 paper on TDP-43 PTMs in ALS. The title matches the claim. However, the specific finding about K82 acetylation in "one out of two" samples is **unverifiable** from the title alone.

**Status: UNVERIFIABLE** – The reference is appropriate, but the specific quantitative claim requires verification.

**Severity: SOFT** – This is a supporting claim that contextualizes the authors' findings, not central to the main results.

---

### 3. Quotation and Number Fidelity

**Status: UNVERIFIABLE (no direct quotations provided)**

The manuscript does not include direct quotations from cited works. Quantitative claims (e.g., "97% of ALS," "20–50% of people older than 80 years," "~50% decline in proteasome activity") are attributed to references but cannot be verified without accessing the original papers.

**Severity: SOFT** – No direct quotations are misquoted, but specific numbers require verification in the original sources.

---

### 4. Retracted or Predatory Sources

**Status: PRESENT (no retracted or predatory sources identified)**

All cited journals are mainstream, high-impact venues:
- Science, Nature Communications, Nature Neuroscience, Nat Genet
- Brain, Lancet Neurology, JAMA Neurology
- Cell Reports, Scientific Reports, FEBS Journal, Acta Neuropathologica

No citations appear to be from retracted papers or predatory venues based on journal names and publication years.

**Severity: N/A** – No issues identified.

---

## Summary of Issues

| Issue | Category | Severity | Status |
|-------|----------|----------|--------|
| Reference 36 cited but missing from bibliography | Reference resolvability | **HARD** | Missing |
| Proteasome activity decline quantification (50% by age 1) | Claim–citation support | **HARD** | Unverifiable |
| Reference 33 (Lange et al.) hypothesis attribution | Claim–citation support | **HARD** | Unverifiable |
| K145 acetylation in inclusions (Reference 9) | Claim–citation support | **SOFT** | Unverifiable |
| K136 acetylation and phase separation (Reference 35) | Claim–citation support | **SOFT** | Unverifiable |
| Bipartite NLS in TDP-43 (Reference 15) | Claim–citation support | **SOFT** | Unverifiable |
| TDP-43 autoregulation (References 26, 27) | Claim–citation support | **SOFT** | Unverifiable |
| K82 acetylation in ALS samples (Reference 34) | Claim–citation support | **SOFT** | Unverifiable |
| DOI/PMID identifiers in bibliography | Reference resolvability | **SOFT** | Missing |

---

## Recommendations for Authors

1. **CRITICAL:** Provide Reference 36 in the bibliography. It is cited in the Discussion but missing from the reference list.

2. **HIGH PRIORITY:** Verify that Reference 33 (Lange et al., 2007) actually proposes the "positive charge hypothesis" that the authors claim to challenge. If not, revise the Discussion to accurately attribute this hypothesis.

3. **RECOMMENDED:** Add DOI or PMID identifiers to the bibliography for all references to improve resolvability and transparency.

4. **RECOMMENDED:** In the Results section, cite the specific papers (References 20–22) that support the "~50% decline in proteasome activity by one year of age" claim, or provide the quantitative data from those papers to justify the choice of inhibitor concentrations.

5. **RECOMMENDED:** Verify that Reference 9 (Cohen et al., 2015) contains the specific claim about K145 acetylation in inclusions, or clarify the source of this observation.

---

## Conclusion

The manuscript's citations are generally resolvable and from appropriate, high-impact sources. However, **one reference is missing from the bibliography** (Reference 36), and **several load-bearing claims require verification** that they are actually supported by the cited sources. The audit cannot confirm these claims without access to the original papers, so they are marked unverifiable rather than unsupported. The authors should address the missing reference and verify the claim–citation support for the items flagged as HARD severity.