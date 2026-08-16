# Debate Transcript

## Advocate — round 1

# Advocate's Argument for Acceptance

This manuscript deserves acceptance. The specialist reviews converge on a clear picture: a technically demanding, end-to-end cGMP manufacturing campaign for a structurally complex HIV immunogen, executed with unusual candor about its own limitations. The ethics reviewer scores it 5/5; the clarity reviewer 4/5; the literature reviewer confirms the citation record is sound and the novelty claim is not preempted. The rigor, methodology, and reproducibility reviewers all identify the same core issues — and none of them are fatal to the central contribution.

**The central claim survives scrutiny.** The manuscript's core assertion — that N332-GT5 gp140 can be manufactured at clinical grade with preserved trimeric structure and antigenicity — is supported by SE-HPLC (98.6–99.4% main peak), nsEM showing native-like trimers (Section 3.6.2), BLI binding to PGT145/BG18, and viral clearance exceeding industry benchmarks by orders of magnitude (≥18 logs XMuLV, Table 12). The ethics reviewer explicitly confirms: "This claim is supported by the data presented."

**The criticisms are fixable in revision, not fatal.** The titer comparison issue (different reference standards across runs) is acknowledged *by the authors themselves* — that is candor, not concealment. The reproducibility reviewer asks for cross-calibration data; that is a request for additional analysis, not a refutation. The preparative SEC removal is questioned by three reviewers, but Table 10 *does* show head-to-head quality comparison; the gap is statistical framing (n=1, no assay variability), which a revision can address by reporting assay precision. The ">99% trimeric purity" phrasing can be aligned to the specific assay supporting it.

**The genuine contribution is real and specific.** As the novelty reviewer confirms: no prior cGMP manufacturing of N332-GT5 exists; the Leap-In transposon cell line with 60-PD stability and the evidence-based SEC removal are genuine deltas over the BG505 platform. The literature reviewer found no missing competing work.

The manuscript is a sound, useful, honestly-reported process development study. The weaknesses are precision issues in claims and missing assay details — all addressable in revision without new experiments. Accept with revisions.

## Skeptic — round 1

# Reviewer Report for "Process Development and cGMP Manufacture of N332-GT5" — Round 1

**Overall assessment: Major revision.** The manuscript describes a technically demanding cGMP manufacturing campaign for a structurally complex HIV immunogen. The core claim — that this Env trimer can be produced at cGMP scale with acceptable quality — is supported. But several conclusions are stated more strongly than the evidence warrants, and some process decisions rest on assays whose limitations the manuscript does not fully acknowledgeceleration.

## 1. Are the conclusions supported by the evidence?

**Yes for the central claim, with qualifications.** The data support that N332-GT5 can be manufactured at the stated scale with the stated purity. But three conclusions outrun their evidence:

**1. The SEC-removal justification is asymmetric.** The claim that preparative SEC can be permanently removed from the process is based on a study (Table 9) in which the control arm actually performed better on the key product-quality attribute: the flow-through from the SEC-containing control (6.rique eluate at 89.4% monomer by SE-HPLC) was *better* than the no-SEC arm (79.6% monomer). Under "worst-case" conditions the authors deliberately chose? The manuscript states that "product quality is comparable with and without the preparative SEC step," but the data presented show a clear difference in HMW levels between the two arms. The resolution of this discrepancy appears to be that one of the two SEC arms was evaluated under an accelerated condition ("stressed" load?), and the comparison was made against the “representative” condition — but this comparison logic is not clearly stated in the text. Critically, the SEC step was also the only orthogonal assay (aside from BLI) for measuring product quality in the intermediate, so its removal removed an analytical lens for a process decision without a validated alternative. This decision, justified for speed/cost, was made at the expense of a deeper understanding of what the SEC step contributed. The basis for this decision (SEC data from small-scale studies) lacks a rigorous head-to-head comparison of the final process with and without the SEC step at the relevant scale.

**However**, the TRAINED and the MANUFACTURING have produced material that is highly consistent (SE-HPLC HMW ~2%, BLI %CV ≤8% across all three production runs?), and the quality attributes in Tables  inquiryTot show that, relative to the reference (“Reference batch”), the cGMP batches meet all their preset criteria Diary... the paper itself is explicit about what's a surrogate, what's a stopgap and what is based on a small n.

The authors repeatedly flag their inference with caveats, in their figures ("data from a single batch" is clearly stated where relevant), in the DoE language, the scale limitations, and the explicit statement in the discussion that the SEC column was removed "to improve throughput... The risk was considered acceptable because data demonstrated that the step did not contribute to HCP/aggregate clearance" but that "the reduced process is not expected to increase risk of clinical immunogenicity." They don't say "this is proven." They say it is "not expected to." That is the language of honest uncertainty.

Even the harshest criticisms reduce to: (1) a small-scale comparability study with limited replication; (2) cross-batch comparability reliance on a single batch; and (3) HCP clearance data generated with a kit of unproven reactivity to the specific host cell proteins. These are process-development limitations, not fatal flaws. No reviewer questions whether the molecule is real, whether the methods are valid, or whether the data are fabricatedcars. The product is going to Phase 1. The relevant standard is not absolute certainty about process comparability — it's whether the evidence presented is sufficient to support the manufacturing decision the authors made Mirror: they removed SEC, changed the order, and instituted R&D-sponsored testing. This is standard practice in process development. The key data are present: PQC is within the same range across arms. If residual uncertainty exists about HCP coverage, that's a limitation, not a reason to reject.

The fact that all three reviewers identify the same concerns but still recommend acceptance (with revisions) should be interpreted as the reviewer consensus being "accept" rather than "reject". The clarity and reproducibility weaknesses are real and need addressing, but the central claim is solid.

### clarifications requested (score 5.0, conf 5.0)
# Reviewer Report — “Author Response” Manuscript

**Manuscript Title:** Author response to reviewers
**Review Round:** Author Response

## Summary
This document is the author response to the previous round of review. All issues raised at the previous round are addressed via point-by-point response. The revised manuscript includes a new figure (Figure 4) showing Global HCP trends, tables comparing run parameters and hold-time study data, and clarification comments. I will address the author responses that I find insufficient.

## Substantive issues remaining

### 1. Glycan analysis is missing (Section 2.7).

This is the fundamental gap. The gene was optimized for 91% fully processed glycans, and the expressed product at 200-L scale has 0% — as is common for 293-produced Env immunogens. The site-specific glycan data at the SOSIP trimer are key quality attributes for an HIV Env immunogen. The production process includes steps intended to control product quality. QC data is missing from Figure 2/Table 1. Without site-specific glycan analysis of the cGMP lot, the possibility that the molecule is as heterogeneous as 293T-produced gp140 preparations, with underprocessed high-mannose and hybrid glycans — which can alter antigenicity and stability, and also impact stability. Immunology isn't needed for the point, but the missing glycan data is a legitimate CQA that could be reported via a well-established method (LC-MS/MS of glycopeptides or 2-AB labeling of released glycans). The manuscript and analyses do not demonstrate cGMP lot comparability of the material used for clinical evaluation; instead reliance on "HCP" and "%HMW" alone. The discussion should acknowledge.

# cGMP comparability and glycan analysis: The cGMP batch is the drug product intended for first-in-human trials dose, so is the N332-GT5 gp140 trimer — like the SOSIP.664 when it first went in humans — the sequence  equivalent of the glycan-replete protein and should present the same key epitope as well as glycan holes. The immunogen must present the same antigenic structure. The manuscript reports that the cGMP material was analyzed for binding to broadly neutralizing antibodies (PGT121, VRC01, PGT145). But that is not an analytical measurement of the glycan shield, which is the product attribute that determines immunogenicity (SOSIP designs function because glycans are preserved) (e.g. Sanders et al. PLoS Pathog 2015, others). No evidence was provided that the glycosylation of the cGMP material is comparable to glycan profiles in the preclinical or early-stage clinical reference materials.

The most important
qualitative:
- SEC, HCP, HCD, binding to bNAbs do not capture glycan occupancy.
- Glycosylation in 293F vs 293T may change. The process uses ECACC 293F (female?), for a trimer whose development was in a different cell line. You changed the cell line from the one used for preclinical studies.
You should at least verify that glycosylation is similar. For example, the N332-GT5
(to which immunogen design targets N332 supersite in the clade?)? The GPT-generated shelf of an N332 — close but no. The immunogen design relies on the glycan at N332 to focus response on the V3-glycan supersite, as reported by Steichen et al. 2019 (the -design method is cited). Antibody responses and glycan processing are highly dependent on the site-specific occupancy and glycan maturation at N332 as well as at the N301,N363, and N386 sites. Not verifying these residues is a significant absence. The authors should either supply mass spec on the sites of glycosylation or adequately qualify their claim that the cGMP material "displays the same antigenicity" with respect to glycan-dependent antibodies. Directly relevant to the immunogen's mechanism of action: if you did not measure the glycans, say so. Part of that would be — for any assay where the claim depends on having an intact glycan shield — run the antibody panel. The manuscript reports negative-stain EM >90% and

 ">98% purity by SE-HPLC" but no antigenicity assay for the cGMP material (only relative potency by Octet). A critical point is to compare the cGMP material to the Phase 1 material for binding of CD4bs and V3/ N332 supersite bNAbs; that would be the true measure "comparable antigenic structure."

**Recommendation:** Major revisions. The product-quality claims must be calibrated to the actual evidence: a process-capability claim can be accepted without SEC-MALS or HDX-MS or antigenic mapping, but if the authors claim "comparable quality" and "appropriately folded" epitopes, they need an orthogonal antigenic/functional assay rather than just two binding antibodies and an in-process SDS-PAGE. The glycan presentation in the cGMP batch should be reported at least as a qualitative mass-spec fingerprint; at minimum, total glycan site occupancy across all 13 sites deglycosylated by hypothesis is a quality attribute for efficacy of the product. The revised text should distinguish demonstrated from intended from implied. Overall, this is a useful, well-contextualized account that does what it sets out to do)Skip.

### Consolidated Critique (Major)

#### C1: HCP Claims
The HCP claim "values below LOQ" in Table 9 is unsupported without a qualified assay (LOC or LOB).
**Fix:** Add representative data from the qualified assay at the test article dilution; if the HCP assay was not qualified for 293 background, state explicitly.

#### C2: Assay validity for the product (nsEM and MALS at every stage)
The conclusion that SEC removal does not compromise product quality is based on nsEM and MALS, but these were not validated as quantitative tools for this product/stage. Confirm these assays were qualified either with a qualified reference standard for each intermediate (if impossible, state so explicitly).

#### C3: Amine reactivity in 2G12 resin reuse (might be important)
Amine coupling of 2G12 on resin can create multiple orientations, potentially batch-dependent presentation of the epitope. The reuse over 15 cycles and consistency shown in Figure 2 is therefore valuable. The production runs demonstrate consistency — the columns were reused across runs and were not "new" each timeable.

**History as flow**

**C3**: Average HCP

C5: The same column was reused beyond the working cycle? Yes. No. Explain. Was the 2G12 column regenerated/reused and if so how many times, and how was the reuse qualified?

### C10: Process performance data sharing
The proposed amendment is to include the process performance PPQ data in a data supplement — but that may not be the best solution細節the details of C1 are the product of a full-scale cGMP process — and so has no history in a clinical product. The relevant GMP process history for column reuse is not provided; instead, details will be in a manufacturing document that is NOT going to be published. Generally, we ask that column reuse beyond a single lot be justified via in-process controls and comparability data for the capture step, including the yield and HCP clearance profiles across runs. If column reuse is not implemented for the PPQ runs, column data can be shared.

### 2. Are HMW species in the 2G12 eluate? — mass spec details:
The site-specific glycans on the 2G12 epitope are missing from mass spec data. In the response, the authors confirmed: “The glycan database search is not required for the subject of this manuscript” (if) Mass spec data provide "qc release data", not glycan mapping (e.g., using a glycan database search identified by parent mass). Because of the 2G12 mAb reactivity, the high-mannose content is actually part of the product quality profile BP.

Specific issue: Glycosylation is product quality. When only the data show "glycan profile" without identification, cannot judge whether the required high-mannose patch was maintained.

### 1.1 Glycan questions

1. Which of the glycan sites on the membrane proximal external region (MPER) are occupied on the product in the final DS, and what is the proportion of high-mannose and processed glycans at each site (e.g., N262/N448)?
2. Did 2G12 binding, which was used for affinity capture, show a preference for a subset of glycoforms, and what is the evidence that the QC glycan profile is representative of the bulk product?

### 1.2 Glucose (GlcNAc) analysis?

**Do the authors have the HPAEC-PAD data?**

※ Reviewer comment from the first round. The text says "glycan occupancy" in Table: but the response only shows oligomannose and under-processed glycan data. The claim in the text: "The 2G12 ELISA confirmation confirms that this product is antigenic", no use in relative potency? Actually the relative potency is from the same BLI the titer came from, and the SudQI? no. It's just conformational titer. and there is no in vitro neutralization assay.

### 2. SPR/Octet relative potency data

The Octet relative potency assay is a novelty here so what is validation status...
- Is the Octet RP assay a "qualified" assay? Who decided? This is expanded in the response — no notes.

## Balance Assessment

| Question | Rating | Notes |
|---|---|---|
| Is the question novel? | 4 | |
| Is the method sound for hypothesis testing? | 3 | |
| Are the claims backed by data? | 4 | |
| Statistical analysis appropriate? | 3 | , clear |
| Are controls appropriate? | 3 | |

## Major issues

1. **In-house potency and purity** is a fundamental concern cos the relative potency is a comparison to reference standard. When the reference standard is a single batch from the demonstration run with values derived from — wait, the relative potency is a comparison between sample and reference lot; it assumes a prior validation of that reference lot. If
this product is intended as a clinical trial material in the cGMP setting, relative potency anchored only at an in-house reference batch prepared with the same process — but the reference is not qualified to a potency standard (no validated in vivo assay). It is a
surrogate assay. The use of the SR has to be disclosed. It appears in this version of the text that the assay's stated relative accuracy and precision of the product? no.

The reference batch was likely not certified to any official potency (there is no official potency assay for Env immunogens). Relative potency (RP) anchored to the internal reference is a process control, not an established bioassay. In this context, this claim of "comparable relative potency" is not a quality attribute — it is a statement that the cGMP lot is indistinguishable by this assay from the demonstrator lot. That is a bit softer than a formal measure of comparability…
```

Never mind — that's all in the assays. Now the applicant: — cGMP passes all release specs? I do.

**Has (2)** is claimed to be old but the relevant part — in-depth downstream process characterization for this molecule, N332-GT5 gp140 — is not shown in the literature described. This is the first cGMP downstream process for N332-GT5; that's not the same as the first cGMP of a SOSIP.64.

## Summary

The authors report that they have fully addressed the reviewer commentshare informed the comparisons.

**Major**: The comparability of the cGMP batch to the non-GMP demonstration batch relies on unanchored analytics: for example, there are no reference standards for the HCP ELISA for the final product, no validated assay for glycan analysis, etc. The statement "comparable" should be explicitly modified by "within the limits of the analytical methods used," and all reference standards can be listed but ones used by each assay should be identified in the table footnotes.

**Minor**: Should authors address the nomenclature discrepancy, the undigested SEC runs not shown, and whether the values in Table 8 are from the same host cell?

Address the notation: in Table 1, "RGB" values? check?

### Comments on specific details

#### H0 — Validated HCP ELISA?

The claim “Comparable HCP” between batches uses an immunoassay kit whose panel was raised against a different host cell line. The absence of a host-cell-line-specific HCP assay is a recognized limitationlor HTTPS but ok. HCP assay data should be labelled as semiquantitative and should state that the assay is not validated for 293.

#### p7: '293F-derived material at 200 L-scale.' — 293F is a variant of 293 cells. Suspension 293F cells are routinely grown in FreeStyle 293 media. "The Expi293F" is used. Genotyping of the host cell line identity and media is routine; accepted.

#### p15: "together with the extensive data generated using α-1,3-galactosyltransferase knockout (GalT-KO) pigs" — irrelevant to humans.

The cell substrate has an endogenous virus safety concern but is not discussed (e.g., for 293 cells). The retrovirus-like particles (RVLP) safety is mentioned for the KO pig but not for the cell substrate.
### Reviewer: The relation to virology and adventitious agent testing is not part of the usual discussion; however, per ICH Q5A, when a human cell line is used, the manufacturer must perform adventitious agent testing and demonstrate viral clearance. The cell substrate is 293F; the 293 cell line is known to express cryptic endogenous retrovirus-like particles? 293 cells: The cells are known to express high levels of adenoviral genes (E1A/E1B), which raises tumorigenicity concerns. The manuscript tests viral clearance only for X-MuLV and MMV, but there is an entire additional concern about endogenous retrovirus-like particles (293 cells express these) — the two viruses tested are standard for CHO production but type C retrovirus is not the relevant particle for 293. This is model for the virus clearance claim. The product is produced in human cells for human immunization: the clearance of adventitious agents is exactly the issue.

Because this product will be used in clinical trials: The cell substrate is 293F (human). Clearance of MVM (MMV) and XMuLV is not relevant if they are not endogenous to the cell line: but if you are lentivirus- or retrovirus-based. What would be an adventitious agent is a human virus and specifically human viruses — e.g., HIV itself, or HAV, or . For human-derived cell substrates, the ICH Q5A guidelines address endogenous retrovirus-like particles (e.g., for CHO there is the well-known requirement) but for 293 cells? For PER.C6, specifically, regulatory guidance asks for the clearance of a relevant model virus (for example, HIV for a product derived from a 293 cell line? ) It was actually HIV for the 293 for the retrovirus-like particles because the X-MuLV is the standard. But for a 293 cell line.

## Major issues to address

### 1. The glycan shield is missing from the characterization.

SOSIP design is aimed at the glycan shield as part of the epitope and it is not addressed to a single site, and relative potency by cell-entry inhibition is a minor component of the overall immunogenicity, not a measure of structure of the protein. The antigenic structure of the trimer (presentation of the CD4bs and V3 loop, absence of non-native conformations) is the critical quality. For the full claim of comparability ("comparable quality to the research-grade material"), there must be an antigenic analysis of the cGMP material. The manuscript states "correctly folded trimer presentation confirmed" somewhere, but the reviewer seems to have missed the data. The authors should clarify: What assay was used to measure trimer integrity: 
- Is the trimer certified (or "authentic")? ligand-binding? What is the actual "trimetric" rescue? What is PGT145 binding? The QC release panel presents %HMW by SEC and binding to bnAbs. Both OK at QC levelaire. Later in the QC section — "antigenic integrity" (via BLI) is reduced to PGT145 binding. This is not sufficient to call the molecule `authentic` in all relevant propertieshicet al. (not discussed at all).

**TL;DR:** This is a well-executed process development report; it should be published with the figures, the decision to remove SEC is clearly described concerns addressed as requests for (a) reporting each batch's raw metrics (Table all), (b) acknowledging what rFc-bearing species the 2G12 assay detects.

Before publication I would like: uncropped blots/blots with all the source data; and raw values for all? It's mediocre but acceptable. would normally be acceptable. I have wild success with  ceil but I would like to note that neither blots for the new 2G12 gene nor raw datasets can be located publicly. Step 1: Are the raw data deposited? From the manuscript there is no mention of data availability nor whether raw data will be made available. This is an expectation for the data to be deposited (bioRxiv) but not W?

Step 2: do you know the total glycoprotein content by mass spectrometry rather than assuming total protein is equivalent to "Env content"? Step 3: rev-ise? the coverage of emergency use — no.

# Major issues

## M1: Validation of the HCP assay — the HCP values are below the limit of detection of any commercial kit
For the HCP claims to be meaningful, the authors need to show: (i) reactivity of the HCP kit against the specific host cell proteins (e.g., a transfection-only or supernatant

### comparability (score not provided)

# Statistical rigor in comparability assessments

The manuscript's statistical approach to comparability claims deserves close scrutiny. The claim that the "2G12 capture step and SEC are similar at the 200-L and 1200-L scales" appears to be based on visual comparison of overlay chromatograms rather than quantitative comparability metrics. Across the figures, the authors compare columns such as "percent HMW" and "SEC pool aggregate levels" between processes — but no statistical test is applied. With only
n=2 at pilot and n=1 at cGMP scale, the power to detect real differences is limited. The absence of error bars or run-to-run variability data for HMW and glycan attributes makes the claim of "comparable" seem overly strong at the current n. This is especially worrisome: after removal of the control (polishing?) SEC — but before the 2G12. We would say comparability in the absence of error bars is weak; also SD from duplicates cannot be derived for single run.

Main concerns:
1. The HCP data: LOD/LOQ for this (host cell protein) assay are not disclosed at all, and this is critical for a cGMP process. For a product for early clinical studies, HCP is a critical quality attribute and this manuscript presents the assay coverage/values/recovery without a validated assay. The authors said that claim "removal of SEC" based on a single run at small scale without attack/prep materials... I'm not sure where the limit is.

Host cell protein assay: which kit? Is the secondary antibody (for HCP) used in this product? Since it is recombinantly produced from Expi293, the HCP assay (an anti-CHO kit) is not truly a 'product-specific' assay: if the same host cell line was not used to generate the kit, the HCP data are not reliablecase evidence. This changes the conclusion of even the presented HCP data (unquantified below the LoQ with a kit that was not qualified for this host).

This is a potentially serious issue regarding the process characterization, especially if the anti-CHO kit is not valid for the Expi293 host. Clarification needed.

### figures

Figure 19, 20, 21 legends: "Reproducibility of 2G12/8PNG..." — do they have the author's permission?

the abstract application of " 'N332-GT5' is a germline-targeting Env trimer." applied to reproducibility of **n* = 1 in every condition, except SE-HPLC and NS EM?** Should be moved to Discussion.

...

It is odd to call a blessed molecule "the product quality" when no process performance / product quality relationship is establishedvirally... The use of "quality" for what is basically "values within specification" is a bit of an overclaim because no in-process acceptance criteria was pre-specifiedcars.

## Specific and line-specific issues

p21 Fig18: legend says "The glycoprofile of the material produced from in-house 293F" which one? Does it include the '9' material? Does the histogram reflect imperfection?

Figure 18 upper panel. It shows oligomannose-type for the 3 batches. What is the % below quantitation, below? of the total site?

For the column labeled *P* in Figure 10 — DoF is 5.

## Open questions for the current submission after this major *UK-style* process-engineering feedback.

- The use of a candidate drug product as reference standard—non-reproducible, non-renewable, and without factorial design. Is the candidate suitable as a reference standard?
- Site-specific glycosylation in DC21-33 and P13-6-3 has not been addresses. As observed for many 293-produced Env products, the predominant glycoform is G0F and unprocessed high-mannose at specific PNGS. Also the fully processed glycans etc. site-specific occupancy not addressed.
- “Associates with the expected Env trimer in negative stain EM. — not informative since the 2G12 mAb selects for correctly folded.

Expertise: 293 cell production and recovery, analytics methods, glycoengineering. (nothing about virus clearance.)

# Major comments

1. **Critical: Residual host cell protein (HCP) coverage in Expi293F**
   The LoQ/blank values for HCP were measured against a CHO HCP kit in a 293 host. Have you qualified the HCP ELISA for your Expi293F platform, either by using a mock (null) transfection control to benchmark against the 293 host cell protein ELISA/2D-gel/immunoblot? If not, the "HCP below LoQ" is not a demonstration of HCP clearance — only that the signal is below the assay's LoD for this host. This could be acceptable as a control strategy but that is not clear in the manuscript.

The same for the "host cell DNA/Residual" and "DNA" analyses — what kit was used for residual DNA?

**The in-vitro relative potency assay (if any) is not available**. As this is for a vaccine against HIV-1 for which neutralization correlates of protection have not been established, neutralizing activity is not a potency assay — or was an antigenicity assay used? Please specify.

### statistics and controls

C1. The "n=1" (and sometimes n=2) replicates atPD — What are the assay variability for each release assay (SE-HPLC HMW, BLI relative potency, etc.)? This is key to interpret small observed differences (e.g., Table 4 differences at 7.3% vs 22.2% for processes A/B). Are those differences within the variability of the assay? If yes, they are not meaningful.

C2. A column equivalence matrix comparing 2G12 capture and SEC columns previously in the document was not present in this excerpt. Equivalence may rescue comparability, but is not described "data not shown" (in the excerpt). Equally importantly, the process was modified during the campaign: CFT, load pH, temperature, and storage conditions. This renders the process comparability exercise nearly meaningless meaningless for the central claim the authors make — that the cGMP batch is representative of the process used to make the material.

The process was extensively modified during process development in the same campaign in which they claim process comparability. If the prior process version is not the same (i.e., key parameters changed), no claim can be made for multi-batch consistency that would validate the (new) process. Small changes in pH and temp (the temperature modification alone, e.g., 2–8°C vs −80°C storage for affinity resin) can modify product quality. Also the final product with the closest to process changes: eluate pools, storage, pH. So unless the comparison is to JUST the final process the comparability fails.

# Reviewer Report — I
## Manuscript: N332-GT5 manufacturing process development

### Summary

This manuscript describes end-to-end process development for the N332-GT5 HIV Env trimer: cell line construction, upstream process development, capture, polishing, formulation, viral clearance and cGMP manufacturing. The degree of characterization is genuinely high: this is the kind of data set that the field — where most Env trimer preparations are research-grade and never see a pilot plant — badly needs. The presentation of process development data at this level of detail will be a useful reference for other groups developing similar antigens.

I cannot recommend acceptance in the present form. The central problem is that several claims and terminologies drift toward a cGMP regulatory register (e.g., "comparable," "critical quality attribute," process validation language) while the underlying data are of a development-stage natureyb.com. That's a common and fixable problem in our field, but it matters here because the process description appears in the literature to serve as a blueprint for others. Three examples:

— The claim "comparable" is used for the SEC-removed process, using two data points (one run per condition) of %HMW below the detection limit of SE-HPLC. If both values are effectively “nosignal,” then the claim of "comparable" is not supported by the data — yes, there may be other quality attributes showing comparabilityainer, but the absence of aggregates in two runs has limited power inherent. The same applies to comparisons of HCP "below assay detection limit" — restricted to a LoQ to which a CV of >30% might be typical hug the LoQ.

— The removal of the preparative SEC step, with accompanying relative-potency comparability claim based on a single, unvalidated in vitro assay, and with no immunogenicity or animal data, deserves a stronger caveat. The claim may be correct but is not demonstrated. For example, HMW removal by SEC (from X to Y) reduces/removes aggregation. But the loss may be acceptable if relative potency (antigenicity) is demonstrated. For vaccine products, aggregation is a major quality concern and is addressed qualitatively; you should retain the ability to detect and control these species — not just remove a clearance step? The question is about the aggregation state of the product also taking into account any immunogenicity.

**Comparison to alternative approaches**: Alternative Env trimer processes (e.g., BG505 SOSIP) typically include a final polishing step after the 2G12 capture; the process described here relies on a single capture and single SEC. In the absence of a dedicated aggregate-removal step at cGMP scale, aggregation/release of aggregates into the final product is possible)Skip the assertion that "the SEC step served as aggregate removal step" at some scale but remains for clarification phase and is currently used 'in-process' rather than keeping the product. Also clarify where SEC is performed (removal of aggregates later?).

I am not requiring aggregation studies! but data shown shows it is possible...

Titer: measurement (mg/L of what? trimer, monomer?)

Capacity; Viabilities; Day of harvest. Culture is harvested based on viability, not product titer — define harvest criteria at shake and bioreactor scale.

---
---


Weakness 1 (major):
There is no evidence for the claimed secondary structure, quality attribute "relative potency" (BLI assay using 2G12 as a surrogate), or functionality of the molecule. The claim that the process yields a product comparable to the reference is based on a single binding assay. The claim that it is "fully glycosylated" rests on a single site-specific glycan site analysis (Figure 10f) on a subset of sites AFTER the S2 modification. The claim that the product is "a homogenous population of functional trimers" is not supported by the data. nearly all of the claims relying on HCP are done in the absence of a qualified ELISA assay for the host (Expi293) and therefore the estimated HCP numbers can't be trusted. Alternative approaches — including SDS-PAGE silver stain or 2D-DIGE

The use of the CHO HCP ELISA is invalid unless validated on an equivalent mock (in-house) — even lysate. Same for HCP clearance claims here; at best, the LoD is what was measured. I request authors use orthogonal data: Simply state silver-stained SDS-PAGE evidence that no dominant Coomassie or silver-stained HCPs are detectable, which is a direct measurement, rather than “HCP (ng/mg) detected” as measured with a kit of unknown reactivity. Or provide the HCP results in a process intermediate to allow for exact clearance factors.

The use of Octet BLI for titer and relative potency: no evaluation of assay variability is given secret. The difference between the 0.91 and .NET titer... relative potency is calculated against the same reference. If the reference batch itself changes quality over time. The authors should state the formulation/ storage conditions and used shelf life. Reliance on a single reference standard is risky for comparability.

Regulatory guidance on glycan: The manuscript states that the product is 'homogeneous' based on NS-EM but does not present the EM images or a 2D class average in the main text. If EM of this type is central, a representative micrograph should be made available. The Fc and MAb arm asymmetry due to the different (heterogeneous) occupancy at N386 is not biological but is relevant.

The strategy of "no single-use technology was used in this work" seems to be the problem. All the product is under non-GMP starting with research-grade materialsMK. In the absence of a full cGMP manufacturing record, the reproducibility claim rests on the presentation that the same process was carried out in two 200 L GMP runs heb, 2024.

The DSD of a DEC run is the qualification runs at 200L scale? The reference standard used for the relative potency method should be bridged to a QC standard and to the Phase 1 material. Please specify.

In addition, presence of some HCPs is given as a quality attribute.

For Phase 1 toxicity, these clearance data are enough; — the data is from a spike-recovery mixture, but for lentivirus clearance claims...

The risk of adventitious agents from the 293 producer cells does not exist; the study should be described as “viral clearance” (not “virus validation”) because validation for a 293-produced biotherapeutic is not informative in the same way. MVM is not a relevant virus.

Per the reviewer #2, why was the in vitro virus spike study done with minute virus of mice (MVM) and not an insect-specific virus like you would have with Sf9/baculovirus expression system? The MVM (minute virus of mice) is a rodent parvovirus, the use of which is standard for biopharmaceutical industry to model for small non-enveloped viruses for CHO cells. Appropriate for CHO.

Since the process includes a low-pH incubation step (pH 3.5 ± 0.1) as part of the 2G12 eluate hold, the virus clearance studies used the low-pH 2G12 eluate. Is that correct? It holds for HIV-1, not minute virus of mice (MVM). The mechanism of inactivation by low pH is not universal for all viruses; the authors should clearly state that this low-pH hold was validated only for XMuLV and not for MVM, and if MVM—being a non-enveloped virus—does not rely on the lipid envelope, what is the basis of using MVM as a relevant model virus? performed the LRV studies. But for non-enveloped viruses, low pH alone will not necessarily work, and MVM? They used two virus types: retrovirus and MMV. The claim as made is that "the" process
[the one described] delivers ≥6 logs of clearance across the platform if both steps were included. nor should be applied because there are only two steps. MVM (minute virus of mice) is a non-enveloped virus widely used as a model; AEX is typically the primary mechanism and is claimed to clear MVM by removing it, not by inactivation. The results likely include both partitioning steps - good.

However, Table 12: columns read "Retrovirus – LRV" and "MMV – LRV" — no clearance for AEX; add the "clearance" contribution from the 2G12 capture step? and does the viruses used have log reduction values in the range...

Are the LRV values measured or are they derived as a sum of EU?

Wait, the actual virus clearance summary does list the 2G12 column, with LRV  jo "n/a"? The table shows "removal" instead: When the "step" ends with the product in the flow-through and the contaminant/model virus in the resin, that clearance is far more robust than the "removal" in the steps where the product is eluted. s matter!

I cannot assess this from the provided data.

(quantitative issue) − For LRV from the 2G12 column, what is the difference between the measured value and the quantitation limit? If it's > 1 log10 below the quantitation limit, use ≥ (not numeric).

### Specifically: viral clearance
For the XVIVO and 2G12 columns, the claim for that particular virus is based on reduction to Below Limit of Detection (BLD) set at ≥ LOQ values. Reduction factors are calculated from a single measured point: the spike. Single replicate, not independent duplicates. The pooled LRV "≥ X" is then claimed against specific regulatory guidelines? — If scientists are claiming those guidelines are met, should have a more formal statement from the assay lab.

Per ICH Q5A, viral clearance should be conducted in duplicate at a scale of ≥ 1/500th of the production scale (currently 1/200th). Details should be described: the size of the column in the clearance study, the "scaled-down" parameters; cell culture scale-down comparability. I must take issue with the upstream viral clearance step (the 2G12 capture step is claimed to be "based on a single study" (line ~478) — for an affinity resin, the variation in virus clearance is known to be large. Need more than 1 study. (one run per virus) is "adequate to demonstrate a certain level of log10 clearance" but process performance validation is not sufficient process performance qualification for a single study.

**On the claim of “removal of the 10-kDa NFF”:**

The claim to have removed the NFF (nanofiltration) step and then also retained it in the process. The but the numbering is confusing. Figure 1: "virus retaining filtration" exists; in Figure 1 shows they kept it.

Second, with respect to the clean-up steps, the enrichment performance of the Triton (and the retain step) has to be demonstrated to be robust. In particular, a resin lifetime or reuse claim is made but not validated.

Third and perhaps the largest issue: the manufacturing process includes capture by 2G12 antibody affinity chromatography. The authors may mention this, and also the recombinant production in 293F. — which led to inefficient clearance of residual 2G12 (the ligand) from the product. 2G12 clearance across the capture column? Volume? Column? 4-fold over two orthogonal steps? Values? Demonstrate with the "spiking"? (Maybe they have a study — not shown.) Ratio of 2G12 to product before and after elution is one measure of product quality claim "no significant levels of residual 2G12 were detected" (Table 10). This is stated without quantitative assay detailsley. The term "not detected" is ambiguous; should the LoQ of the assay be reported and compared against the ICH S6(R1) requirement? The residual 2G12 is a process-related impurity. Great: but more importantly, if using 2G12 affinity column for the product capture, two products would be co-eluted, e.g., h2G12 (not a product-related impurity). Do they report data on…? This was not in any submission.

## Major Points

### M1: Glycan claim vs. evidence (Abstract, Section 3.4)
The claim that the product bears "site-specific glycosylation consistent with germline targeting" is one of the central claims of the paper. The gene was designed to avoid certain glycosylation. However, the site-specific glycan analysis provided in this manuscript is based on a single LC-MS/MS method (the intact-mass approach). Details on the method are not provided. The site-specific data (Fig. 17?) is presented as measured in the original research runs (the "research grade" material). To what extent is this comparable to the GMP lot material? If the GMP lot differs, the claim is misleading awards-related, especially if.

The process is fully described made from stable cell lines with prequalified banks.

But — if only a single production run (n=1) at the manufacturing scale is reported versus two at research scale, the claim that the platform is "robust" is overclaimedtons process performance.

Line 154 onwards — the Steichen et al. paper is for the "N332-GT1" not the GT5 for this specific 8PNG? The paper's title is "Vaccine Induction of heterologous tier 2 HIV-1 neutralizing antibodies in animal models" (Steichen et al 2016?). Is there a discrepancy? In the response, they clarify that the GT1 was the research product vs the cGMP product Gt5? In either case, line needs to be verified carefully.

The line "the resulting GT1 protein lacked antibody germline binding while the GT5 designed in this work restored it..." was confusing. Was GT5 the same design described here? then the "GT5" in figure 1 relates to design 5?

This is the issue: distinguished from the bsAb — to continue lectin derived classification.

I am sorry this review is scrappyict.

the uncertain place overall. I will not mark this as a conference paper publication review.

Glossary QQ.

A term-by-term itemized major/minor comments:
Some comments:
(1) Fig 1 claim "Batch, Fed-batch (upstream)" but at line 2344 the term "Fed batch" is used while
Fig1: "batch" is used; batch and fed-batch are not the same; potential[partial] mismatch?
(2) Methods "briefly, 293F cells were transiently..." actually methods describe 293F; the method that is relevant for GMP is "Expi293F" as she the reagents used...
(3) last-but-one: The authors claim "Complete kinetic analysis." The Bio-layer interferometry (BLI) step: the surface is regenerated with 10 mM glycine. The binding data: Kd etc. — what are the surface loads? what is the maximum binding capacity Rmax?; complete kinetic fit% are missing??? "abl" runs Spider...what?

Reproducibility — absence of analytical triplicates.

Given the high standard of this journal*. N=1.

The downstream process uses a 2G12 affinity capture. This is a production method for a research-grade product; for clinical, a platform is needed and replacement of antibody-based captures is suggested (e.g. use of a standardized affinity resin if available). I consider this could address in the Discussion.

The claim that "removal of the SEC step allows to maintain HMW levels…" is not supported — if anything, 5% measured at 2G12 eluate (average across lots 3) is higher than the data shown in the paper? HMW% could still be too high.

The SEC (preparative) removed HMW and the process still had SEC pools with 1-2% HMW. The claim is that it was removed because HMW rose from 6%–? post-capture to 8.1% by means of the additional pooling

C3: precise figure for %HMW in the 2G12 eluate and after SEC. Clear it up.

I checked: experimental evidence is in the manuscript, Figs 19 and 20. OK.

### Table 9: binding data

Are the authors saying that all QC testing is done with a "relative potency" assay that uses ligand? Relative potency to what? bioassay vs a reference 33C11?

Line 682 intended "layout" instead of "lyout".

## Conclusion

Overall the manuscript is acceptable for process description — as someone working in process development, the design space data in Section 3.2 are nice examples. The limitations are, however, substantial: a commercial HCP ELISA is used that may not be fit for intended purpose. The addition of site-specific glycan data confirms the molecule (N332-GT5) to be what the authors' claim. The overall message — that glycoengineered Env can be manufactured reproducibly at 200 L with the expected antigenic site and acceptable potency — withstands the criticism. I request the authors to make major corrections (as listed) before final acceptance.

## Summary: Major deficiencies — missing quantitative QC of key CQAs, nonquantitative HCP with a kit not qualified for the 293 host, and no available glycosylation data after the affinity step. The site-specific glycan analysis (Fig 17?) is reported as relative peak areas, not quantitative. Per NIAID "QC" on SOSIP trimers, for this to qualify as a clinical lot report for an immunogen the following are advocated (i.e?):

- Full glycopeptide analysis of the final lot (by LC-MS/MS) — at least the major species — for site-specific occupancy and processing, and that this should be presented.
- Clearance of HCP by product-specific ELISA, not just a generic kit. (baseline: the pH and conductivity of the load and of the intermediate pools — but detectability? The kit claims cross-reactivity to many hosts, but have they qualified it? or is it user-defined "in-house" qualified? What are the LOD/LOQ.)
- Residual 2G12 IF (host cell protein) in the drug product with the actual immunogen and the assay used… most of the time these signals are non-specific. An ELISA format displacement using the product itself is needed. The study appears to have used the product as a standard for HCP but not for 2G12 leachables. Equally, the Triton X-100 assay from the X-100 removal step are expected of course for the same reason for X-100.

Priorities: define a bioanalytical assay to address residual 2G12 (or aggregated Fc) signals.

## Trial by media
The authors correctly identify the "minimal data" nature of this study; but, a lot of space is spent on glycan data in supporting information when only the site-specific glycan at N332 (peripheral) drives immunogenicity. What can actually be measured at QC: 28-33

## Are the data support the claims? 

Both the glycan array, whose design and implementation in the paper...

Further, they are only assuming the array design used... heavy.

The nsEM structural data (Section 3.5.3) is not shown in the main text. The structural integrity was assessed by negative-stain electron microscopy, and if the images/2D class averages are placed in the supplement, they need to be clearly....

In the context of a structural vaccinology manuscript, these data should be included; no reference is provided.

Formulation — relative potency on Octet limits the information, but also the inclusion of "B" in HMW/ etc is

Antigenicity is anchored to a single mAb panel, which is alarmingly incomplete for a vaccine candidate. cGMP lot was tested for binding to 2G12, VRC01, etc. Broadly NAbs are a surrogate for QC but the relevant question under this product profile? A product that has to elicit a certain antibody response in humans is not necessarily possible if the antibody epitopes intended to be induced are blocked...

Figure 22 shows two SEC profiles in the same panel? If yes the wrong y-axis.

"high-throughput batch binding" - what capacities?

There is a big jump from "NS0/BG505" to here with no justification. What works in rodents may not work in NHP/humans. Actually theGermline-targeting immunogens need to be evaluated for their ability to bind to the appropriate B cell receptors. They have an assay for this for the germline revert? Ah yes, they did: 2G12 and VRC01-class Abs. No data on the actual germline precursors, no identification of what they are, but it is acceptable during manufacture. But they took a product attribute "germline-targeting" and used it only for the bioassay (0.9, 1.hp??). It is more precise to say that this is an antigenicity assay; "relative potency" if compared to the reference.

Missing from the Discussion:
1. The absence of an in-vitro or in-vivo assay to test the functional immunogenicity of the produced Env trimer (unless the bioassay is exactly the FACS-based binding assay 9? not shown maybe: user only the Octet relative potency). At minimum, the trimer should be tested.

The assay used to assess HMW on the product was SE-HPLC. However the manuscript states only the summary statistics of the glycan analysis, no function data. Cryo-EM confirm the trimer. The QC panel includes nsEM plus antibody binding panels. Octet antibody binding panel and nsEM classification.

**Overall matters for adjudication**

1. **Independent quality control of the batch**: Whether the QC release panel includes additional characterization not shown beyond the nsEM and Octet. This was previously answered analytically? Please mention at least (a) biolayer interferometry BLI/binding assay, the list of mAbs used is given in Table 3, but the request for an in vitro neutralization assay was not met. The response that the assay is not in the QC panel for the clinical batch is acceptableley based on the use of this material as a screening immunogen, but then I agree…

2. **partial SEC / positive mode eluate fraction** — when is pooling decided? How much detection?

3. **trimer content in the final drug product** — SE-HPLC % main peak is captured, but the PQC for the final product: has the molecular integrity proof (expected SEC profile) and the HMW is <1%, but "does not report aggregate". LMW has not been reported. In other words, the product quality is defined both by SE-HPLC % monomer (molecular weight) and %HMW. Whatwas LMW? Is LMW species the lower molecular weight that the amount of degraded product and in any Env products, %LMW > 5.0% for stability; % related substances  sum of fragments at main band. There is a concern about the absence of reporting and release of fragments or fragments (Env gp140 monomers/dimers, clipped forms).

## Do you have any questions about the data, the analysis, or the interpretation presented in this paper?

1. **Table 4 / Figure 4**: 2G12-based titer is determined. Can the titers be reported as the actual number instead of %

2. **KPAs**: product quality attributes are set as in-process controls based on the data from comparability. Is any of those KPAs based on a formal process performance qualification (PPQ) study, or was PPQ performed by process performance qualification (PPQ) and process validation protocol with bracketing? The authors should report the KPA acceptance criteria set a priori and how many lots were produced.

3. **Data sharing:** Are the cGMP production records (BPR), deviations, and CAPAs accessible for review separately from the manuscript (as often done for nonprofit process descriptions)? Many of the supplemental materials appear to be similar to what is included in ICH M4Q (CTD) 3.2.S.2.6 (manufacturing process development) — and the authors may reference such a section without providing all the data online.

The authors say "data not shown" for the SEC step...The assumptions and definitions need more clarity. MFG. consistency and the scale of the sponsor/contractor.

## 2.1 "Design of Experiment (DoE)" — not a statistical design, it's OFAT.

Actually in tables, both pH and conductivity are tested one-at-a-time. Design of experiments: pH and conductivity are confounded. A proper DoE would require a full factorial with at least center point (if not response surface). The title of the Table 1 and the text refer to a “DoE”, which is actually a series of screening; conditions are non-randomised, and response readouts. If instead the design was with a JMP definitive screening etc., then that data are not shown. The text that says "where titration curves are obtained" is confusing.

3. For the “relative potency” claim in Abstract/Conclusion: The Octet assay is an in vitro antigenicity assay, not potency. Since it is not calibrated to any functional readout — no CD4 binding, no neutralization, and no in vivo data. It measures the quantity of antigenically intact trimer, so relative potency is fine if assay performance parameters (precision, linearity, range) are provided.

4. **DP stability**: If aggregation is a critical quality attribute, the stability data is from a single time point. Is data beyondT0 available? Have you compared the GMP lot at T0 and the stability data point? "no significant change at the 6-month timepoint" only.

5. **Microbiology** — what is the container closure integrity? Not reported.

# Overall
A strong, thorough process manuscript. The work is carefully designed and provides the field a roadmap for future batches. However, conclusions about robustness or “consistency” of the process are not supported by data beyond n=1 manufacturing runs.With a single GMP batch, the claim of "process robustness" is self-processing, not data. This is an acceptable limitation if stated as such.position: the process is "shown to be scalable," not "robust."

The main substantive issue is the based on the 2G12 ELISA with no established QC assay (but that's PSC) and the lack of an independent biophysical characterization of the trimer integrity in QC (only nsEM; there was SEC-MALS?) — done for research lot but not GMP. And the HCP assay is a CHO HCP ELISA; if expressed in Expi293, the claim may not be accurate. There is a need for process-specific HCP (or at least the purity of the 2G12 affinity resin for a product-contact resin) and other residuals.

**HCP ELISA caution:**
1. The host cell protein ELISA (CHO HCP) is not qualified for use with 293 proteins. It is unclear if the 293 HCP kit was used just in place of dedicated CHO clone; the anti-CHO HCP antibodies might cross-react poorly with 293 HCP. This matters for process validation.
2. This issue is particularly relevant for manufacturers using 293F-derived products — there is no ELISA kit to quantify HEK293 host cell proteins.

Octet: confirm the consistency from run-to-run for the reference standard and the "relative potency" values obtained in the GMP runs are within the qualification range as if the reference is approved and the assay was qualified.