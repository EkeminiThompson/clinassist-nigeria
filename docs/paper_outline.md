# Manuscript outline

## Working title
An Explainable, Uncertainty-Aware and Offline-Capable Domain Adaptation Framework for Clinical Decision Support Under Resource Constraints

## Research questions
1. Under controlled covariate and missingness shift, when does CORAL adaptation improve or harm discrimination and calibration versus source-only baselines?
2. Does uncertainty-based selective prediction improve retained-case performance at prespecified coverage, and what is the coverage trade-off?
3. How stable are local feature attributions under perturbation and domain shift?
4. What reliability constraints arise when clinical workflows tolerate intermittent connectivity?

## Contributions
- Auditable evaluation protocol separating genuine external validation from synthetic shift.
- Leakage-safe source-only versus CORAL comparisons.
- Joint discrimination, calibration and risk-coverage reporting.
- SHAP explanation stability measured through rank-biased overlap.
- Offline-first client with no offline inference and explicit sync boundaries.

## Data provenance
The purported UITH/General Hospital Offa deposit is repackaged Pima data without hospital identifiers; ESUTH data remain inaccessible. Results must be called public benchmark and controlled synthetic shift, never Nigerian multi-hospital validation. Future cohorts require ethics approval, site provenance and prespecified external validation.

## Methods
Use repeated stratified/nested CV with preprocessing fitted within folds; logistic regression, random forest and gradient-boosted baselines; CORAL with unlabelled target covariates; prespecified covariate and MCAR/MAR-like missingness shifts; calibration curves, Brier and ECE; risk-coverage/AURC; SHAP and explanation-ranking stability; offline persistence/reconnect/duplicate-delivery tests.

## Analysis and reporting
Report repeated-seed means and uncertainty intervals, paired effect sizes and confidence intervals. Do not treat folds as independent patients. Include negative results and ablations. Prespecify primary outcomes and shift severity.

## Limitations and ethics
No Nigerian multi-hospital validation currently exists. Synthetic shifts do not recreate all clinical or institutional heterogeneity. This prototype is not for clinical use. Prospective work requires ethics review, local leadership, secure governance and independent validation.
