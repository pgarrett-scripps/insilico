# Debate Transcript

## Advocate — round 1

The manuscript makes a substantial contribution by establishing a principled, model-based framework for personalized stimulation targeting that directly addresses a fundamental question in network neuroscience: whether pathology hubs are the optimal intervention sites. The central finding—that discriminant-aligned sites differ from pathology-deviation sites—is robustly demonstrated through systematic in-silico experiments comparing multiple targeting strategies. While the reviewers raise valid concerns about interpretation and validation, the core methodological advance remains: the authors show that within their identifiable generative model, selecting targets based on their effect on the disease discriminant (LDA-resonant) yields dramatically better reclassification than targeting the most-deviant model parameters (ΔW), regardless of whether both are tested as resonant drives (Fig. 5A shows resonant drive at ΔW site saturates at ~57% while LDA-resonant reaches 100%). This dissociation is not merely a category error—it's a demonstration that different selection criteria produce different therapeutic outcomes within the same intervention modality. The framework's value lies in providing a computable prescription for personalized targeting that could be tested in more biophysical models, moving beyond descriptive correlations to causal, counterfactual testing.

**Key points:**
- The manuscript provides a novel methodological framework for personalized stimulation targeting using identifiable generative models.
- The dissociation between discriminant-aligned and pathology-deviation targeting is robustly demonstrated through systematic comparison of resonant drives.
- The approach enables causal, counterfactual testing of network interventions that observational data cannot provide.
- The findings challenge conventional assumptions about targeting pathology hubs and offer testable hypotheses for translational research.

## Skeptic — round 1

The advocate's defense misses the fatal flaw: the manuscript's central claim compares apples to oranges. As the rigor reviewer notes, the "pathology" intervention is a theoretical read-out interpolation (ΔW correction), while the "therapy" intervention is a physical resonant drive. When properly comparing resonant drives at both site types (as shown in Fig. 5A), the ΔW site reaches ~57% reclassification while the LDA-resonant site reaches 100%. This difference, while substantial, doesn't establish that "optimal stimulation sites are not the most affected"—it only shows that among stimulation strategies, discriminant-aligned targeting works better. The manuscript's framing implies a biological dissociation, but as the methodology reviewer notes, ΔW is a model-fitting residual, not an independent pathology measure. The subcortical "pathology" sites are where the model is least constrained, so their ranking may reflect fitting uncertainty rather than disease concentration.

Furthermore, the 100% "reversion" is achieved at supra-physiological amplitudes that induce massive network-wide perturbation (distance ~0.7 from baseline FC), essentially overwriting the system rather than therapeutically modulating it. The leave-one-out analysis in Fig. S9 still shows alarmingly high "net cure" rates (~100% for personalized targets), suggesting potential overfitting despite cross-validation. This is FATAL to the clinical interpretation, though potentially fixable with more honest reporting that this is model-internal overwrite, not biological restoration.

**Key points:**
- Core claim suffers from category error comparing different intervention types
- 100% reclassification achieved through supra-physiological overwrite, not therapeutic modulation
- ΔW pathology measure is model-fitting residual, not independent biological marker
- High cure rates in leave-one-out analysis suggest potential overfitting issues