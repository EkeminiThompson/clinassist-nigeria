# Manuscript reproducibility and submission status

**Updated:** 2026-11-14  
**Repository:** EkeminiThompson/clinassist-nigeria

## Verified against committed source code

- Both manuscripts include the author-supplied ORCID, corresponding email and affiliations: Nnamdi Azikiwe University and VergelAI.
- The baseline Table 1 gradient-boosting estimator is `GradientBoostingClassifier`; the repeated-split shift study uses `HistGradientBoostingClassifier`. They are separate experiments.
- The executable shift protocol is present at `ml/experiments/run_shift_study.py`. It defines all seven scenarios, feature transformations, scenario-specific seeds, model constructors, calibration procedure and generated raw/summary outputs. See `docs/experiment_protocol.md`.
- CORAL implementation is present at `ml/domain_adaptation/coral.py`. Its source-to-target mapping is `(X_s - mean_s) @ C_s^(-1/2) @ C_t^(1/2) + mean_t`, with covariance regularisation epsilon (10^{-5}). It fits from source and target feature matrices only; target labels are not accepted by the adapter.
- The explanation-stability and subgroup-audit scripts are present. The subgroup audit consumes patient-level predictions from the shift study and uses paired bootstrap resampling.
- The baseline estimator settings and shift-study estimator settings are documented from their respective source files.
- An MIT licence applies to repository software only; it does not relicense the Pima benchmark or third-party assets.

## Remaining evidence and author decisions

1. **Original run environment:** the repository CI workflow specifies Python 3.11, but that does not establish the environment used for the reported manuscript runs. The independent verification note separately records Python 3.12, scikit-learn 1.9.1 and XGBoost 3.4.1 for its clean rerun. Original-run OS, CPU, RAM and complete package lock remain unrecorded.
2. **Execution evidence for all reported tables:** the source scripts generate all seven scenario summaries and raw paired split-level outputs. The currently committed manuscript presents only the severe-combined scenario table. A successful, retained workflow artifact containing the exact table-producing run must be retrieved and checked before claiming that all seven scenario tables or the AUROC discrepancy have been reconciled. CI workflow configuration alone is not proof that a particular run succeeded.
3. **AUROC reconciliation:** the exploratory audit deltas (−0.0008, +0.0367, +0.0508) differ slightly from deltas recomputed from rounded Table 2 means (−0.0007, +0.0362, +0.0505). Recompute from unrounded paired split-level output and use one authoritative calculation. Do not infer it from rounded means.
4. **Hyperparameter search:** no tuning/search routine is present in the reviewed experiment scripts. The author should confirm whether any separate tuning was performed; do not imply optimisation or tuning in the manuscript without records.
5. **Hypothesis testing:** subgroup paired-bootstrap intervals are exploratory. They are not evidence that prespecified confirmatory hypothesis tests were conducted.
6. **Ethics and governance:** obtain and accurately report any institutional/venue ethics determination required for secondary analysis of the public benchmark. No approval or exemption is asserted here.
7. **Supervisor review, author order, contributions and competing interests:** require author/institutional confirmation.
8. **References and journal style:** verify every reference against its original source and apply the target journal's current citation and bibliography requirements.
9. **Target-journal checklist:** complete the applicable TRIPOD+AI reporting checklist and any journal-specific submission forms.
10. **Data terms and archive:** cite the actual OpenML/UCI dataset source and applicable terms used for the experiment. A versioned Zenodo archive with a DOI is recommended after the final code/data manifest has been checked.

## Methodological limitation retained

The code applies covariate and missingness transformations to raw held-out test features before the preprocessing pipeline replaces zero values with missing values, imputes and scales. This means a raw zero can be changed by a shift before zero-to-missing conversion. The manuscript should retain this ordering as a limitation unless the protocol is intentionally changed and all affected experiments are rerun.

## Scientific boundary

The current experiments use only the public Pima Indians Diabetes benchmark (768 records). The work is a controlled computational methodology study, not Nigerian hospital data, multi-hospital external validation, a fairness certification, clinical utility evidence or a deployment evaluation.