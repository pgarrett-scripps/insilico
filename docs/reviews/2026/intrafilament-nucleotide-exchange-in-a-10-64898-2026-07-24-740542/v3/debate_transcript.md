# Debate Transcript

## Advocate — round 1

This manuscript reports a genuine mechanistic discovery: intrafilament nucleotide exchange in MreB filaments, a behavior fundamentally distinct from eukaryotic actin and defining a new class of cytoskeletal polymer dynamics. The evidence is multi-layered and mutually reinforcing. TIRF and HS-AFM directly visualize symmetric, ATP-driven elongation on cardiolipin-containing membranes (Figs 1I-K, 2E-G). Two ATPase mutants (E136A, D158A) with distinct nucleotide-binding phenotypes (Fig 3B, Table 1) polymerize indistinguishably from WT (Fig 3C-D), proving hydrolysis is uncoupled from assembly. The critical FRAP ambiguity (Fig 3F) is resolved by the orthogonal pure-ATP* incorporation assay (Fig 3H-I), which shows homogeneous nucleotide binding along preformed filaments — impossible via end-wise addition alone. The capping experiment (Fig 4G-H) and Monte Carlo model (Fig 4D, S8-S10) further validate that intrafilament exchange tunes stability: ATP rejuvenates, ADP triggers catastrophic disassembly. In vivo CCCP data (Fig 4J) align with this mechanism.

Most reviewer concerns are presentational or analytical, not fatal. Pseudo-replication (data_analysis) reflects how n is reported, not data quality; mixed-effects re-analysis and explicit replicate counts will fix this. The FRAP negative-control caveat (methodology) is acknowledged in-text and superseded by Fig 3H-I. The CCCP confound (rigor) is mitigated by the in vitro reconstitution establishing causality. The novelty claim (literature) should be qualified to "to our knowledge" with a ParM/MamK literature search — a simple revision. Data/code deposition (reproducibility) is a journal requirement, not a scientific flaw.

The core advance — nucleotide cycling within intact filaments as a stability rheostat — is robust, quantitatively grounded, and evolutionarily significant. Accept with revisions addressing statistics, clarity, and deposition.

**Key points:**
- Intrafilament nucleotide exchange is a novel, quantitatively documented biopolymer behavior
- Orthogonal methods (TIRF, HS-AFM, mutants, modeling, in vivo) converge on the same mechanism
- FRAP ambiguity resolved by pure-ATP* incorporation assay (Fig 3H-I) and capping experiment (Fig 4G-H)
- Pseudo-replication and statistical gaps are analytical/presentation issues fixable in revision
- CCCP confound mitigated by in vitro reconstitution establishing direct causality
- Novelty claim requires qualification and literature search — minor revision
- Data/code deposition is a compliance matter, not a scientific deficiency

## Skeptic — round 1

The central claim — intrafilament nucleotide exchange defining a new polymer class — rests on two load-bearing assays that cannot distinguish nucleotide exchange from subunit exchange, and all quantitative comparisons are statistically invalid due to pseudo-replication.

1. **FATAL: FRAP assay (Fig 3F) lacks a valid negative control for subunit exchange.** The authors acknowledge TFLime photobleaching may irreversibly trap fluorogen (Fig 3E), so absent TFLime recovery cannot rule out subunit turnover. Annealing/fragmentation (Fig 1L-P) could produce identical ATP* recovery. The advocate cites Fig 3H-I (pure ATP* incorporation on preformed filaments) as orthogonal proof, but the method for forming D158A filaments for this assay is undescribed (Clarity Q: "how were D158A filaments formed and visualized initially if they're not visible with ATP*?" — unanswered). Without knowing how preformed D158A filaments were generated, Fig 3H-I cannot validate the FRAP interpretation.

2. **FATAL: Pervasive pseudo-replication invalidates every quantitative claim.** Data_analysis reviewer documents that all key comparisons (symmetrical elongation n=13 filaments/unknown SLBs; mutant elongation rates n=318/68/39 filaments from 2 experiments; ATP* incorporation n=19/12/17; ADP depolymerization n=60–408) treat filaments as independent replicates despite originating from 1–2 SLB preparations. No statistical tests, p-values, or mixed-effects models are reported. The advocate calls this "analytical/presentation issues fixable in revision," but with n=1–2 true replicates, the data may simply lack power to support the claimed effect sizes — this is not a presentation fix.

3. **FATAL: Capping experiment (Fig 4G-H) does not verify cap completeness/symmetry.** Methodology reviewer notes incomplete/asymmetric E136A capping could allow ADP access to WT subunits from an uncapped end, producing breakage near caps without intrafilament exchange. The advocate's claim that this "validates" the mechanism assumes perfect capping, which was not demonstrated.

Conceded: The advocate correctly notes that in vitro reconstitution establishes ATP-driven polymerization and hydrolysis-uncoupled assembly (Figs 1–3C-D), and that the Monte Carlo model integrates measured parameters. However, the novel mechanistic conclusion — nucleotide cycling *within intact filaments* as a stability rheostat — remains unsupported by the critical assays above. The CCCP confound (Rigor) and novelty overclaim (Literature) are additional weaknesses but secondary to these fatal gaps.

Verdict: Reject. The core discovery cannot be accepted on evidence that conflates nucleotide exchange with subunit exchange and lacks statistical rigor.

**Key points:**
- FRAP assay cannot distinguish intrafilament nucleotide exchange from subunit exchange (annealing/fragmentation)
- All quantitative comparisons use pseudo-replicates (filaments) from 1–2 independent SLB preparations with no statistical tests
- Capping experiment does not verify cap completeness, leaving alternative explanation for breakage
- D158A filament formation method for pure ATP* incorporation assay (Fig 3H-I) is undescribed
- In vitro reconstitution of polymerization/hydrolysis uncoupling is solid, but novel "nucleotide cycling within filaments" claim is not established

## Advocate — round 2

Conceded: the pseudo-replication issue (data_analysis) is serious — filament counts from 1–2 SLBs cannot support parametric inference without mixed-effects reanalysis and explicit biological replicate numbers. Conceded: the D158A filament formation method for Fig 3H-I is undescribed (Clarity Q unanswered); the text states preformed D158A filaments were exposed to pure ATP* but does not explain how they were polymerized/visualized initially given their invisibility under standard ATP* labeling. Conceded: the capping experiment (Fig 4G-H) lacks verification of cap completeness/symmetry.

However, the core claim — intrafilament nucleotide exchange — is directly demonstrated by Fig 3H-I: homogeneous ATP* incorporation along the *entire length* of preformed WT and D158A filaments. This cannot be explained by end-wise addition or annealing (which would label only ends), and it persists in D158A (hydrolysis-deficient), ruling out hydrolysis-coupled exchange. The Monte Carlo model (Fig 4D, S8-S10) quantitatively recapitulates WT/E136A/D158A disassembly kinetics using independently measured rates (Table 1), and predicts ATP rejuvenation/ADP catastrophe (Fig 4I) — a mechanistic coherence that subunit-exchange models cannot explain. In vitro reconstitution (Figs 1-3C-D) establishes ATP-driven, hydrolysis-uncoupled polymerization on cardiolipin membranes. The CCCP confound (rigor) is secondary to the in vitro causality.

All conceded gaps are fixable in revision: (1) report biological replicate counts, reanalyze with mixed-effects models; (2) describe D158A filament formation for Fig 3H-I (likely polymerized with ATP then washed); (3) add cap-verification control (e.g., dual-color end-tracking). The novelty claim requires qualification ("to our knowledge" + ParM/MamK search). Data/code deposition is a compliance step.

The discovery of nucleotide cycling within intact filaments as a stability rheostat — distinct from actin — remains robustly supported by convergent evidence. Accept with revisions addressing statistics, clarity, and controls.}

**Key points:**
- Concede pseudo-replication, D158A method gap, capping verification — all fixable in revision
- Fig 3H-I shows homogeneous ATP* incorporation along filament length — direct evidence of intrafilament exchange, not end-wise addition
- Monte Carlo model quantitatively predicts mutant disassembly kinetics and ATP/ADP switching using independent parameters
- In vitro reconstitution establishes ATP-driven, hydrolysis-uncoupled polymerization on cardiolipin membranes
- Core discovery — nucleotide cycling within intact filaments as stability rheostat — is robust and novel

## Skeptic — round 2

The advocate concedes three fatal gaps but argues the core claim survives on Fig 3H-I and the Monte Carlo model. It does not.

1. **FATAL: Fig 3H-I evidence chain is broken for D158A.** The text explicitly states: "D158A filaments were not visible" under standard ATP* labeling (line 228). The advocate speculates they were "likely polymerized with ATP then washed" — but this is not in the manuscript. If D158A filaments cannot be visualized during formation, there is no verification they are intact doublets (vs. aggregates) before ATP* exposure. The homogeneous ATP* signal could label non-filamentous protein. Without the formation method, Fig 3H-I cannot support intrafilament exchange for D158A, and the WT-only data are insufficient for the general mechanism.

2. **FATAL: Pseudo-replication is not a presentation fix.** The advocate calls it "fixable in revision," but with 1–2 true replicates (SLB preps), the data lack statistical power to detect the claimed effect sizes (e.g., >5-fold ADP acceleration, 2-fold D158A vs WT ATP* incorporation). Mixed-effects models cannot create power from n=1–2 biological replicates. The quantitative foundation for every kinetic parameter (Table 1, Fig 2E, 3D, 3I, 4B) is unsupported.

3. **FATAL: Monte Carlo model is circular.** The advocate claims it uses "independently measured rates," but Table 1 shows k_hyd, k_Pir, k_+n, k_-n, k_-e are from this study's fits or "ND" (not determined). The model fits the same disassembly curves it predicts (Fig 4C, S10) — no independent validation. Fig 4I's ATP/ADP switching prediction is a model output, not experimental confirmation.

4. **Conceded but unresolved:** Capping experiment lacks cap verification (Methodology reviewer); CCCP confound remains (Rigor reviewer); novelty claim unqualified (Literature reviewer).

The in vitro reconstitution of ATP-driven, hydrolysis-uncoupled polymerization (Figs 1–3C-D) is solid and novel. But the load-bearing claim — *intrafilament nucleotide exchange as a stability rheostat* — rests on a broken evidence chain (Fig 3H-I D158A gap), statistically invalid comparisons, and a circular model. These are not revision fixes; they require new experiments. Reject. 

**Key points:**
- Fig 3H-I D158A filament formation method absent → cannot verify intrafilament exchange for hydrolysis-deficient mutant
- n=1–2 biological replicates → no statistical power for any quantitative claim
- Monte Carlo parameters fitted to same data → circular validation
- Core mechanistic conclusion unsupported by current evidence

**Key points:**
- Fig 3H-I D158A filament formation method absent → cannot verify intrafilament exchange for hydrolysis-deficient mutant
- n=1–2 biological replicates → no statistical power for any quantitative claim
- Monte Carlo parameters fitted to same data → circular validation
- Core mechanistic conclusion unsupported by current evidence