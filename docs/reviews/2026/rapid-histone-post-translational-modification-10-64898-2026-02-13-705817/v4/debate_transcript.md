# Debate Transcript

## Advocate — round 1

**Advocate’s Opening Statement**

This manuscript earns acceptance because it delivers a practical, field-ready advance with a mechanistically grounded discovery, and its weaknesses are precisely the kind that revision—not rejection—can resolve.

**The core contribution is real and defensible.** The systematic 10-condition comparison (Figure 1) is exactly the benchmarking the histone PTM field needs. The dual-protease RIPUP workflow demonstrably achieves complementary coverage: r-Chymotrypsin uniquely captures H2A.Z (72% proteotypic coverage vs. <6% for Arg-C/Trypsin) and linker histone H1 variants (Figure 2D, SI Figure S1). This is the most defensible claim in the paper, and it is fully supported by the data.

**The TMT charge-compensation finding is genuinely novel.** The mechanistic hypothesis—that TMT’s tertiary amine sequesters a mobile proton, enhancing b-ion series and rescuing ionization of acidic acylations—is plausible and testable. The detection of 58 succinylation and 31 glutarylation sites in HEK293T histones (Figure 5B) is a striking observation that warrants the “dark epigenome” framing, *provided* the authors add the matched comparison the reviewers request. This is a revision-level fix, not a fatal flaw.

**The NAM experiment, while confounded, is honestly handled.** The authors explicitly identify the missed-cleavage redistribution problem and choose peptidoform-level analysis over the artifactually biased peptide-family approach. This is exactly the design thinking that should be standard. The 112 significant peptidoforms claim is statistically valid as stated; the biological interpretation can be requalified in revision.

**The reviewers’ demands are all addressable.** The protease confound in the TMT comparison (Clarity, Methodology, Rigor) is settled by adding Arg-C Ultra + Prop counts side-by-side. The NCE confound (Data Analysis) is settled by running TMT samples at fixed 30% NCE. The biological-replicate question (Data Analysis) is settled by one explicit sentence in Methods. The missing limma specification (Reproducibility) is settled by a commit hash and design matrix.

This is a sound, useful paper whose claims modestly outrun its evidence in two places—both fixable with targeted additions. Accept with minor revision.

## Skeptic — round 1

# Skeptic's Rebuttal — Round 1

The advocate's case rests on the premise that the manuscript's weaknesses are "precisely the kind that revision—not rejection—can resolve." I agree that *some* are. But two are not merely fixable gaps in presentation; they are confounds that undermine the paper's two headline claims, and the advocate has not engaged with the strongest form of either objection.

**The TMT "dark epigenome" claim is confounded by the protease comparison, not just the missing denominator.** The advocate says the fix is "adding Arg-C Ultra + Prop counts side-by-side." But the methodology reviewer identified a deeper problem: the manuscript compares TMT-labeled Arg-C Ultra against *Trypsin* + Prop — differing in *two* variables. The paper's own numbers show "Arg-C Ultra + Prop" yields 254 fully cleaved peptides, closer to the TMT number (416) than to Trypsin (179). The protease, not the label, may be driving the improvement. The succinylation/glutarylation counts for the propionylated Arg-C Ultra condition are never reported. Without that matched comparison, the charge-compensation mechanism is inferred, not demonstrated. This is not a missing table — it is an untested alternative hypothesis.

**The NAM experiment's "112 significant peptidoforms" may rest on pseudo-replication.** The data-analysis reviewer flagged that the three "replicates" appear to be aliquots from a single split culture ("divided into 3 x 5 mL aliquots"). If so, the effective n is 1, and the entire limma analysis collapses. The advocate calls this "settled by one explicit sentence in Methods" — but a sentence cannot retroactively create biological replication that did not occur. This is potentially fatal, not cosmetic.

**The "quantitative accuracy" claim in the abstract is unsupported by any validation experiment.** No spike-in, no known-ratio control, no orthogonal method comparison. The rigor reviewer correctly identifies this as HARD. The advocate did not address it.

**Collective blind spot:** No reviewer tested whether the stepped NCE (30/40/50) used for TMT samples — versus fixed 30% for unlabeled — alone explains the enhanced b-ion coverage and succinylation detection. This is the cheapest control in the paper and it is absent.

The workflow is useful. The claims outrun it.