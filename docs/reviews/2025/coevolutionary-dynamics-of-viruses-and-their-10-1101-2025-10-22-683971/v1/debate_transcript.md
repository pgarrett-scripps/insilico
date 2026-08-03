# Debate Transcript

## Advocate — round 1

This manuscript deserves acceptance because it delivers a genuinely new theoretical synthesis: extending Alfaro et al.'s phenotype-diffusion framework to virus-DIP systems by adding phenotype-dependent interference (Eqs 1-3), de novo DIP generation, and a zero-sum resource constraint. Reviewers across methodology, novelty, and data-analysis panels agree the model is mathematically sound, reproducible (public code, explicit parameters), and robust to structural choices—alternative kernels (Fig S5) and 3D extensions (Fig S4) preserve qualitative chase dynamics. The LHS sensitivity analysis (n=10,000) mapping four regimes (Fig 5) is a substantive, systematic contribution that most reviewers rate positively even while wanting confidence intervals.

The most serious criticism—that Fig 6's match to DePolo et al. is only qualitative, with linear-scale rather than orders-of-magnitude resistance shifts—is real, but it is a revision-scope problem, not a fatal flaw. The authors already disclose this discrepancy explicitly (lines 443-450) and propose a specific, testable mechanism (corkscrew trajectories in higher dimensions) rather than hiding the gap. Similarly, the biology-to-parameter mapping gap and the α-tautology concern (rigor reviewer) can be addressed by rewording claims from 'predicts' to 'demonstrates conditions under which,' and by adding a worked mapping example—both are text-and-framing fixes, not redesigns.

What cannot be dismissed as merely fixable is the core achievement: this is the first model to mechanistically unite von Magnus oscillations and Red Queen chase dynamics in one framework, generating falsifiable, parameter-specific predictions (e.g., washout rate effects) that invite direct experimental test.

**Key points:**
- Genuine methodological extension of Alfaro et al. framework with biologically motivated new terms (interference kernel, de novo generation)
- Sensitivity analysis (10,000 LHS samples) and robustness checks (kernels, dimensions) are substantive, reviewer-acknowledged strengths
- Quantitative mismatch to DePolo et al. data is transparently disclosed by authors and represents a revision-fixable framing issue, not a structural flaw
- Reproducibility is strong: public code, explicit parameters, stated extinction thresholds
- Model generates falsifiable, testable predictions (e.g., washout rate vs chase prevalence) that advance the field beyond qualitative intuition

## Skeptic — round 1

The advocate frames the DePolo mismatch as a disclosed, fixable framing issue. That undersells it. Four independent reviewers (rigor, methodology, novelty, literature) converge on the same structural problem: the model's *only* real empirical anchor produces resistance changes on a linear scale where experiments show orders-of-magnitude shifts (lines 443-445), and the paper's proposed fix—a 'corkscrew trajectory' in higher dimensions—is admitted to be speculative and untested (S4 shows only that 3D perturbations don't collapse, not that they recover the missing magnitude). You cannot call this 'transparently disclosed and revision-fixable' when the disclosure is a hand-wave, not a remedy; fixing it requires new modeling work, not rewording. This is FIXABLE only if the authors actually build and test the higher-dimensional extension—not by changing 'reproduce' to 'qualitatively resemble' in the abstract.

Compounding this, the methodology reviewer notes the paper never shows the continuous-diffusion machinery is *necessary*: no comparison against a discrete-mutation or simple fixed-trait predator-prey null model is offered, despite von Magnus oscillations being explicable by simpler means (ref 5-10 predate any phenotype-space formalism). Without that comparison, the paper's central methodological claim—that strong-mutation continuous diffusion is required to explain the phenomena—is asserted, not demonstrated. That is FIXABLE in principle (run the comparison) but as submitted it's an unaddressed gap, not a stylistic one.

I concede reproducibility and mathematical self-consistency are solid, and the sensitivity analysis is a genuine strength. But the paper's motivating empirical claim currently rests on an admittedly failed quantitative test.

**Key points:**
- The DePolo validation (Fig 6) fails quantitatively by orders of magnitude, and the proposed fix (higher-dimensional 'corkscrew') is speculative, not demonstrated—this needs new modeling, not rewording
- No comparison against simpler null models (discrete adaptive dynamics, fixed-trait predator-prey) establishes that continuous phenotype diffusion is necessary rather than merely sufficient
- Concede: mathematical soundness, public code, and the LHS sensitivity analysis are genuine strengths not in dispute
- The advocate's 'framing fix' characterization understates the work required to actually validate the model's central empirical claim