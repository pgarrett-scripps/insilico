# Methodology Reviewer

## Summary
The manuscript presents a compelling body of evidence for intrafilament nucleotide exchange in MreB, a novel mechanism diverging from eukaryotic actin. However, the central claim rests critically on FRAP experiments where the negative control (TFLime-labeled filaments) is compromised by acknowledged irreversible photochemical trapping, leaving subunit exchange as an unruled-out alternative explanation for ATP* signal recovery. The capping experiment and preformed-filament ATP* incorporation provide valuable orthogonal support but do not fully close this gap. Other claims (ATP hydrolysis dispensable for polymerization, ADP-induced depolymerization, symmetric elongation) are well-supported by mutagenesis, buffer-exchange, and dual-color imaging designs.

## Strengths
- The combination of HS-AFM, TIRF, and mutagenesis with two distinct ATPase-deficient mutants (E136A, D158A) provides robust, multi-angle evidence that ATP hydrolysis is not required for polymerization but occurs post-assembly.
- The buffer-exchange experiments (nucleotide-free vs. ADP) coupled with the E136A-capping experiment elegantly dissect the roles of Pi release, nucleotide exchange, and filament-end stability in disassembly dynamics.
- The Monte-Carlo model integrates measured kinetic parameters and correctly predicts the distinct disassembly behaviors of WT, E136A, and D158A filaments under different nucleotide conditions, strengthening mechanistic interpretation.

## Weaknesses
- The primary evidence for intrafilament nucleotide exchange (Fig. 3F, ATP* FRAP recovery) lacks a valid negative control for subunit exchange: the authors acknowledge that photobleaching may irreversibly trap TFLime on pFAST, so the absence of TFLime FRAP (Fig. 3E) cannot distinguish between stable subunits and trapped fluorogen. Subunit exchange (annealing/fragmentation, observed in Fig. 1L-P) could produce the same ATP* recovery signal, and the design does not rule this out.
- The capping experiment (Fig. 4G-H) uses E136A subunits labeled with both ATP* and TFCoral added to preformed WT-TFCoral filaments. Because E136A caps are added only at t0 and filament ends are dynamic, incomplete or asymmetric capping could allow ADP to access WT subunits from an uncapped end, producing breakage near caps without requiring intrafilament exchange. The experiment does not verify cap completeness or symmetry.
- The symmetric elongation claim relies on dual-color TIRF with ATP* (Fig. 2F), which the authors note reduces polymerization rates two-fold and may cause steric conflicts, and on photobleaching with an artificial orientation assignment that amplifies stochastic asymmetry (Fig. 2G). While the conclusion is likely correct, the methods introduce systematic biases that are not fully quantified.

## Questions
- Could the ATP* FRAP recovery (Fig. 3F) be explained by subunit exchange (end-to-end annealing/fragmentation visible in Fig. 1L-P) rather than nucleotide exchange within intact subunits? What experiment would distinguish these?
- In the capping experiment (Fig. 4G-H), how was the completeness and symmetry of E136A capping at both filament ends verified? Could uncapped ends explain breakage in WT segments?
- The fluorescence anisotropy data show MreB nucleotide binding rates ~300-fold slower than actin (Table 1), attributed to partial unfolding without nucleotide. Was the nucleotide-free state of purified MreB confirmed structurally (e.g., CD, DSF) to support this interpretation?