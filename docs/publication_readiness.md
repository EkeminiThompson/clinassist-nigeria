# Publication readiness — ClinAssist Nigeria

**Package date:** 2026-11-14  
**Primary manuscript:** papers/01_calibration_domain_adaptation_diabetes.md  
**Supplementary:** papers/02_explanation_stability_subgroup_audit.md  

## Completed

- Added an evidence-based reproducibility checklist response at `docs/reproducibility_checklist_response.md`; clarified that no new dataset was introduced and distinguished source-dataset access status from a licence grant.
- Added `DATA-LICENSE.md` to separate the MIT software licence, the existing benchmark's source terms and author-generated experiment outputs.
- Added exact paired sign-flip tests for AUROC, Brier and ECE (63 comparisons) and archived the results. With five overlapping split pairs, the minimum two-sided p-value is 0.0625; no comparison is statistically significant at 0.05. The manuscript now reports this limitation explicitly.
- Expanded the manuscript's rationale for the benchmark, classifier families, CORAL, scenario design, metrics, TreeSHAP and subgroup audit. Fixed hyperparameter settings are documented as protocol choices, not optimised values.

1. Full methods, results tables, and discussion for the public-benchmark calibration and domain-adaptation study.
2. Supplementary TreeSHAP stability and subgroup audit report with audit counts.
3. Independent clean-environment experiment rerun (2026-11-13): baseline five-fold metrics match the archived manuscript table; CORAL reduces ECE under controlled age and BMI shifts.
4. Dataset provenance documentation (Pima / OpenML only; no Nigerian hospital claim).
5. Full seven-scenario experiment execution verified in successful CI run #156 (run ID `43558361142`): 210 split/model/scenario/adaptation rows, 42 summary rows, 1,050 paired differences and 40,320 held-out prediction rows. Appendix B reports all 21 model-by-scenario paired comparisons. Raw outputs are committed under `ml/artifacts/experiments/` by research CI run #164.

## Scope of the scientific claim

- Methodological evaluation of discrimination, calibration, selective prediction, and explanation stability under controlled shift on a public diabetes benchmark.
- Scenario- and model-dependent behaviour of unsupervised CORAL.
- No claim of Nigerian multi-hospital external validation, clinical utility, or deployment readiness.

## Remaining author / journal steps

- Retain successful CI run #160 (run ID `43571392655`), output commit `79438a8927669a2d18924200619e1fd8c98b069a`, and the artifact checksum recorded in `docs/manuscript_reproducibility_status.md`.
- Original-run hardware, operating system and complete package lock remain unavailable; the current CI runner is pinned and logs hardware details but does not reconstruct historical runs.
- Confirm whether any separate hyperparameter search was performed.
- Confirm the Associate Editor assignment before using the author-supplied name Dr. Joshua Babatunde Agbogun in correspondence.
- Zenodo software archive DOI supplied: [10.5281/zenodo.24215668](https://doi.org/10.5281/zenodo.24215668); GitHub release `v0.1.0` is published. Confirm the Zenodo landing-page metadata and archived files before manuscript submission.
- Review the exact shift equations, random seeds and CORAL mapping in `docs/experiment_protocol.md` against the final manuscript.

## Author / journal steps (outside the repository)

- Final reference list and citation style for the target venue. ACM author-year BibLaTeX setup is documented in `docs/submission_metadata.md`; use it only if the selected ACM venue requires author-year references.
- Author contribution and competing-interest statements.
- Institutional review / ethics determination as required by the venue (computational benchmark using public data).
- TRIPOD+AI checklist completion for prediction-model reporting.
- Supervisory co-author review if applicable.

## Neuroscience companion project

See `EkeminiThompson/movement-awareness-computational-neuroscience`. Protocol and validation framework are specified; version-pinned OpenNeuro download, trial-count reconciliation, and participant-held-out experiments are the remaining empirical steps for that package.
