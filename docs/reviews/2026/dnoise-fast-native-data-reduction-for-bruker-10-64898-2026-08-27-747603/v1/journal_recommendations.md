# Venue Recommendations

## as_is

**Journal of Proteome Research**

This manuscript is ready for submission to JPR now. The work is methodologically sound, the benchmark is rigorous, and the tool is immediately useful to the timsTOF user base. JPR's scope explicitly covers software tools, data processing methods, and instrument-specific workflows in proteomics — dnoise fits squarely in that remit. The paper's modest scope (one instrument, one benchmark, one acquisition mode pair) and honest limitations are assets rather than liabilities in a methods journal; JPR readers expect exactly this kind of focused validation. The editor's "minor" verdict and the panel's unanimous 4/5 scoring (with no fatal issues identified) indicate acceptance-ready work. Acceptance odds: **high (75–85%)**.

*Rationale:* JPR has published comparable timsTOF processing tools (e.g., the MaxQuant ion-mobility extensions, IonQuant papers). The manuscript's depth of validation, open code, and public data align with JPR's standards. The required revisions are all reporting and scoping clarifications, not methodological fixes — exactly what a minor verdict signals.

---

## after_revision

**Molecular & Cellular Proteomics**

After addressing the editor's required revisions — particularly items 1–4 (parameter sweep disclosure, confidence intervals in main text, scope qualification, and native-compatibility closure) — this becomes a strong fit for MCP. The journal explicitly covers computational methods, data reduction, and instrument-specific workflows. The revision will tighten the claims and surface the evidence more transparently, which is precisely what MCP's broad readership (computational and experimental proteomists) needs to evaluate whether the tool applies to their own data. The public data, code, and reproducibility will be a strong signal. Acceptance odds after revision: **moderate-to-high (65–75%)**.

*Rationale:* MCP is more selective than JPR but values methodological rigor and honest scoping. The required revisions strengthen both. The main risk is that MCP may view the contribution as incremental (a denoising tool for one vendor's format), but the panel's verdict and the tool's immediate utility to a large user base mitigate that. The revision will make it clear that this is not a claim of universal applicability, which is appropriate.

**Analytical Chemistry** (or **ACS Analytical Chemistry**)

If the authors want a broader audience beyond proteomics specialists, AC is a realistic target after revision. The paper's focus on data reduction, signal-to-noise filtering, and instrument-specific optimization fits AC's scope. The Rust implementation and the performance benchmarking (runtime, memory) will appeal to the computational chemistry and analytical methods readership. The required revisions (especially items 1, 3, and 10) will make the methodology and reproducibility transparent to a non-proteomics audience. Acceptance odds after revision: **moderate (55–70%)**.

*Rationale:* AC is more instrument-agnostic than JPR or MCP, so the timsTOF specificity is less of a barrier. However, the paper will need to emphasize the general principle (mobility-coherent filtering for ion-mobility data) more than it currently does. The revision list includes items that support this (parameter sweep, decision rules, absolute numbers). The risk is that AC may view the work as too specialized; the upside is that a successful publication there reaches analytical chemists who use timsTOF but do not read JPR.

---

## alternative

**bioRxiv** (or **medRxiv** if clinical proteomics context applies)

If the target venues above prove unexpectedly selective, posting to bioRxiv is a low-risk fallback. The manuscript is already preprint-ready: data, code, and reproducibility are all public, and the editor's verdict is "minor." A bioRxiv posting will immediately reach the timsTOF user community and will accumulate citations from users who adopt dnoise. Many proteomics labs check bioRxiv for tools before formal publication. The required revisions can be incorporated into a revised preprint without journal gatekeeping. This is a realistic and respectable outcome for a tool paper.

*Rationale:* Tool papers often have longer publication timelines in traditional journals. bioRxiv allows immediate dissemination while the authors pursue formal publication. Given the work's utility and the panel's positive verdict, a bioRxiv listing will not diminish the paper's impact in the proteomics community.

**Proteomics** (Wiley)

A narrower alternative if JPR or MCP reject. *Proteomics* is explicitly focused on methods and tools for proteomics workflows and has a lower acceptance bar than JPR. The paper fits comfortably in scope. Acceptance odds: **moderate (60–70%)** without revision, **high (75–85%)** after revision.

*Rationale:* *Proteomics* is a solid specialty journal with a dedicated readership in the timsTOF community. It is a realistic fallback if the higher-tier venues are competitive.

---

## Notes on the revision path

The editor's decision letter is unusually detailed and constructive. Items 1–4 are **critical for any journal submission** and will be required by JPR and MCP alike; the others are important for transparency but less likely to be blocking. The authors should prioritize:

1. **Parameter sweep disclosure** (item 1) — this is the most substantive revision and will take the most care, but the data exist.
2. **Confidence intervals and consistency** (item 2) — straightforward; Tables S10/S11 are already computed.
3. **Scope qualification** (item 3) — a few sentences in the Abstract and Conclusions; high-impact, low-effort.
4. **Native compatibility** (item 4) — either a quick reader test or a restatement; the restatement is acceptable and faster.

Items 5–12 are tabulations, clarifications, and citation fixes — all low-effort once the above are done.

**Realistic timeline:** The required revisions can be completed in 2–3 weeks. The optional reader test (item 4a) would add 1–2 days if the authors have access to AlphaTims or OpenTIMS; the restatement (item 4b) takes an hour.