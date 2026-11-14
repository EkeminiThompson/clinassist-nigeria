# Executable experiment protocol

**Repository:** `EkeminiThompson/clinassist-nigeria`  
**Source of truth:** executable Python files listed below.  
**Scientific scope:** controlled experiments on OpenML Pima Indians Diabetes (768 rows); no Nigerian hospital cohort or external clinical validation.

## Reproduction sequence

Run from the repository root in an environment compatible with `backend/requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
export PYTHONPATH="$PWD"
python -m ml.datasets.download_pima
python -m ml.experiments.run_baselines
python -m ml.experiments.run_shift_study --repeats 5
python -m ml.experiments.run_explanation_stability --seed 42 --n-explain 100
python -m ml.experiments.run_subgroup_statistical_audit --bootstrap 1000 --seed 2026
```

The subgroup audit depends on the patient-level prediction CSV produced by the shift study. The raw dataset is retrieved at runtime and is not committed to Git.

## Dataset and preprocessing

- Retrieval: OpenML dataset ID 37; expected 768 rows, eight predictors and class counts 500 negative / 268 positive.
- Canonical features: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction and Age.
- Outcome: binary 0/1.
- In Glucose, BloodPressure, SkinThickness, Insulin and BMI, raw zeros are converted to missing values.
- Median imputation and standardisation are fitted on source-training data only in each shift-study split.
- In the shift study, perturbations are applied to raw held-out test features before zero-to-missing conversion. Therefore, a zero can be shifted to a nonzero value and will not then be treated as missing. This is a protocol limitation and is not silently corrected here.

## Repeated-split domain adaptation study

**Implementation:** `ml/experiments/run_shift_study.py`

- Split seeds: 42, 43, 44, 45 and 46 for the five-repeat manuscript protocol.
- Split: stratified 75:25 source train / held-out target test using `train_test_split`; 576 / 192 rows.
- Source preprocessor: fitted once per split on source-training features.
- Three classifiers:
  - Logistic regression: `max_iter=1500`, `class_weight="balanced"`, split-specific random state.
  - Random forest: `n_estimators=250`, `max_depth=6`, `min_samples_leaf=3`, `class_weight="balanced"`, `n_jobs=-1`, split-specific random state.
  - Histogram gradient boosting: `max_iter=150`, `learning_rate=0.06`, `max_leaf_nodes=15`, `l2_regularization=1.0`, split-specific random state.
- Probability calibration: sigmoid `CalibratedClassifierCV`, three-fold CV, fitted using source-training labels only.
- Arms: source-only and CORAL. CORAL is fitted using source-training features and the transformed target-test features; target labels are used only for final evaluation.
- Scenario RNG seed: `split_seed + 1000 * scenario_index`, with scenario indices assigned by the insertion order below.

### Scenario definitions and transformations

| Scenario | Covariate severity | Missing rate | Mechanism |
|---|---:|---:|---|
| reference | 0 | 0 | none |
| covariate_mild | 0.5 | 0 | none |
| covariate_severe | 1.5 | 0 | none |
| mcar_10 | 0 | 0.10 | MCAR |
| mar_like_10 | 0 | 0.10 | glucose-dependent MAR-like |
| combined_mild | 0.5 | 0.10 | MCAR |
| combined_severe | 1.5 | 0.20 | glucose-dependent MAR-like |

For severity (s), the code shifts only three columns of the raw held-out matrix:

[
Glucose'=Glucose(1+0.15s)+5s
]

[
BMI'=BMI(1+0.10s)+1.5s
]

[
Age'=Age(1+0.05s)+2s
]

MCAR independently masks each cell with probability (m). The MAR-like mechanism standardises shifted glucose within the held-out matrix, computes (q_i=\operatorname{clip}(2m/(1+e^{-z_i}),0,1)), and independently masks SkinThickness and Insulin for each row with probability (q_i). It is a controlled glucose-dependent missingness mechanism, not a claim about a clinically observed missingness process.

The script writes:
- `synthetic_shift_runs.csv`: unrounded split/model/scenario/arm metrics.
- `synthetic_shift_predictions.csv`: held-out patient-row labels and probabilities for paired audit.
- `synthetic_shift_summary.csv`: mean and standard deviation by model, scenario and arm, rounded to five decimals.
- `synthetic_shift_paired_differences.csv`: CORAL minus source-only paired differences for each metric and split.
- `synthetic_shift_study.json`: run manifest and complete row-level metric objects.

The split-level outputs, not rounded summary tables, are the source for reconciling paired metric differences.

## CORAL implementation

**Implementation:** `ml/domain_adaptation/coral.py`

For source and target feature matrices, the code calculates sample covariance matrices and adds (epsilon I), with (epsilon=10^{-5}). It maps source rows as:

[
X_{s\rightarrow t}=(X_s-\mu_s)C_s^{-1/2}C_t^{1/2}+\mu_t
]

The adapter fits on source and target feature matrices only. No target labels are accepted by its fit method. The implementation rejects non-finite inputs, so missing values must be imputed before CORAL.

## Baseline and explanation experiments

**Baseline:** `ml/experiments/run_baselines.py`. Five-fold shuffled stratified CV, seed 42, out-of-fold probabilities. Models are logistic regression (`max_iter=1000`), random forest (200 trees, depth 6), GradientBoostingClassifier (150 estimators, depth 3), XGBoost (150 estimators, depth 3, learning rate 0.1, subsample/column subsample 0.8) and RBF SVM with probability estimates. These are separate from the calibrated shift-study estimators.

**Explanation stability:** `ml/experiments/run_explanation_stability.py`. Seed-42 stratified 75:25 split; random forest (250 trees, depth 6, minimum leaf 3) and XGBoost (180 estimators, depth 3, learning rate 0.04, subsample/column subsample 0.8, L2 penalty 2); up to 100 held-out examples; Gaussian perturbation SD 0.01, 0.05 and 0.10; rank-biased overlap persistence 0.9.

## Subgroup audit

**Implementation:** `ml/experiments/run_subgroup_statistical_audit.py`

The audit consumes `synthetic_shift_predictions.csv`, verifies each held-out label against its original Pima row index, checks paired source-only/CORAL patient rows, and computes descriptive metrics for overall, age and BMI strata. Eligibility requires at least 20 observations and at least five observations in each outcome class. Paired bootstrap resamples the same patient indices for both adaptation arms, requests 1,000 draws, and retains a comparison only when at least 90% of requested replicates are valid. This is exploratory subgroup analysis, not fairness certification or confirmatory hypothesis testing.

## Evidence limitations

The CI workflow configures these commands and artifact upload. A workflow definition does not prove that a particular run completed successfully. For manuscript submission, retain the successful run ID, commit SHA, artifact bundle and exact unrounded CSVs used to produce every reported table. Record the actual run environment (Python and package versions, OS, CPU and RAM) separately. Do not infer the historical experiment environment from the current CI runner or a later clean verification run.


## Verified execution record

- Successful GitHub Actions run: **#164**, run ID `43571713333`.
- Source commit: `9d31dfbb6105168abca0d62706f1f98dec01feec`.
- All seven scenarios completed for seeds 42–46, three models and two adaptation arms: 210 run-level rows.
- Summary: 42 model/scenario/adaptation rows.
- Paired differences: 1,050 rows across ten metrics.
- Held-out predictions: 40,320 rows.
- Workflow artifact: `clinassist-research-results`, 1,103,250 bytes compressed; SHA-256 `de58d936100cd1ae67c3e2404f57295132feeeb50713881d56f4bdd20427c572`.
- The workflow committed the five shift-study result files and Pima provenance manifest in Git at commit `79438a8927669a2d18924200619e1fd8c98b069a`; the Actions artifact remains an additional 90-day copy.
- No benchmark source CSV is committed. The manifest records OpenML dataset ID 37, 768 rows, class counts and the retrieved CSV checksum.


**Bitwise reproducibility note:** a subsequent fixed-seed rerun showed sub-micro floating-point variation in some unrounded calibration and paired-difference fields. The rounded scenario summaries and Appendix B paired comparisons remained unchanged to four decimal places. The committed output snapshot is the successful run #164; later CI runs retain artifacts but do not automatically rewrite this reviewed snapshot.

## Statistical comparison added for the frozen five-split output

The analysis script ml/analysis/paired_sign_flip_tests.py reads the committed split-level paired differences and enumerates all 2^5=32 sign assignments for each two-sided exact sign-flip test. It analyses AUROC, Brier and ECE for each of the 21 model-by-scenario comparisons (63 tests total), then applies Holm adjustment within each metric family. The generated table is ml/artifacts/experiments/paired_sign_flip_tests.csv.

With five pairs, the minimum attainable two-sided p-value is 0.0625. No result reaches 0.05; Holm-adjusted values are 1.00. The five train/test splits overlap, so this is an exploratory sensitivity analysis at split level, not confirmatory population inference. Do not describe any result as statistically significant. A larger, independently designed evaluation would be needed for confirmatory inference.

## Licensing boundary

The original benchmark is OpenML dataset 37, version 1. The OpenML record labels it Public but does not supply a specific CC or SPDX licence identifier. The source CSV is not redistributed here; users must retain original dataset attribution and follow the source terms. The author's generated analysis outputs are CC BY 4.0 to the extent of author-held rights, while source labels retain their original rights and terms. Software remains MIT-licensed. See DATA-LICENSE.md.


## Unaggregated explanation and subgroup outputs

The TreeSHAP stability script writes `explanation_stability_raw.csv`, one RBO value per explained held-out example, model and perturbation level, in addition to the model/noise summary table. The subgroup audit writes `subgroup_bootstrap_draws.csv.gz`, retaining each valid paired bootstrap replicate's AUROC, AUPRC and Brier deltas together with subgroup, split, model and scenario identifiers. `subgroup_metrics.csv` retains group-level metric rows and `subgroup_paired_bootstrap.csv` retains interval summaries and validity counts. The raw draw file records valid draws; the bootstrap seed (2026 by default), requested replicate count and minimum-valid rule are recorded in the executable protocol. The raw output files are committed by research CI.
