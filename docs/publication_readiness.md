# Publication readiness — ClinAssist Nigeria

**Package date:** 2026-11-13  
**Primary manuscript:** papers/01_calibration_domain_adaptation_diabetes.md  
**Supplementary:** papers/02_explanation_stability_subgroup_audit.md  

## Completed

1. Full methods, results tables, and discussion for the public-benchmark calibration and domain-adaptation study.
2. Supplementary TreeSHAP stability and subgroup audit report with audit counts.
3. Independent clean-environment experiment rerun (2026-11-13): baseline five-fold metrics match the archived manuscript table; CORAL reduces ECE under controlled age and BMI shifts.
4. Dataset provenance documentation (Pima / OpenML only; no Nigerian hospital claim).
5. Reproducible experiment pipeline under `ml/experiments/` with CI artifact history.

## Scope of the scientific claim

- Methodological evaluation of discrimination, calibration, selective prediction, and explanation stability under controlled shift on a public diabetes benchmark.
- Scenario- and model-dependent behaviour of unsupervised CORAL.
- No claim of Nigerian multi-hospital external validation, clinical utility, or deployment readiness.

## Author / journal steps (outside the repository)

- Final reference list and citation style for the target venue.
- Author contribution and competing-interest statements.
- Institutional review / ethics determination as required by the venue (computational benchmark using public data).
- TRIPOD+AI checklist completion for prediction-model reporting.
- Supervisory co-author review if applicable.

## Neuroscience companion project

See `EkeminiThompson/movement-awareness-computational-neuroscience`. Protocol and validation framework are specified; version-pinned OpenNeuro download, trial-count reconciliation, and participant-held-out experiments are the remaining empirical steps for that package.
