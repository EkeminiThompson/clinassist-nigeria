# Research benchmark results review

**Workflow:** GitHub Actions run 42463107060  
**Commit evaluated:** 91c94c9fcd3f753001dee8d5dfd3ce7f461cf700  
**Artifact:** `clinassist-research-results` (artifact ID 13610682436; SHA-256 `0f64456dcbe83becc83c38611d4d364faa3bdb10fb06663b53e0d9969332aa9c`)  
**Data:** OpenML 37 / Pima Indians Diabetes; 768 records, 8 predictors, 500 negative and 268 positive.  
**Interpretation:** Methodological benchmark only. This is not Nigerian hospital data or external clinical validation.

## 1. Execution status

The workflow completed successfully for backend, frontend and the research job. The benchmark download, 5-repeat synthetic-shift experiment and TreeSHAP stability experiment executed and their outputs were uploaded. A subsequent code review found that the subgroup audit script in this evaluated commit was a no-op (imports/helper only); therefore **no subgroup analysis or paired subgroup bootstrap was actually produced by this run**. A complete implementation and CI output assertions were added in a later commit and require a new green run before subgroup results can be accepted.

## 2. Five-fold public-benchmark comparison

| Model | AUROC | AUPRC | Brier | ECE | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.835 | 0.707 | 0.157 | 0.036 | 0.571 | 0.880 |
| Random forest | 0.834 | 0.698 | 0.157 | 0.040 | 0.563 | 0.864 |
| Gradient boosting | 0.827 | 0.693 | 0.168 | 0.084 | 0.627 | 0.826 |
| XGBoost | 0.825 | 0.692 | 0.164 | 0.064 | 0.616 | 0.836 |
| RBF SVM | 0.821 | 0.697 | 0.164 | 0.055 | 0.541 | 0.868 |

The Pima benchmark does not show a compelling discrimination advantage for the more complex tree/boosting models over logistic regression. Logistic regression has the strongest AUROC/AUPRC and lowest Brier/ECE in this run. These are benchmark estimates only; no confidence intervals or independent Nigerian test cohort are represented in this table.

## 3. Synthetic shift experiment

Design: three models (logistic regression, random forest, histogram gradient boosting), seven controlled shift/missingness scenarios, two adaptation arms (source-only and CORAL), five random seeds (42–46), 75/25 stratified splits. Total: 210 model/scenario/arm evaluations. Target labels were not used to fit CORAL; target covariates were used for CORAL alignment. Scenarios are synthetic perturbations of Pima test rows, not real hospital/site shifts.

### Mean results by selected scenario

| Scenario | Model | AUROC source → CORAL | AUPRC source → CORAL | Brier source → CORAL | ECE source → CORAL |
|---|---|---:|---:|---:|---:|
| Reference | Logistic regression | 0.845 → 0.843 | 0.730 → 0.725 | 0.153 → 0.153 | 0.065 → 0.074 |
| Reference | Random forest | 0.850 → 0.848 | 0.723 → 0.732 | 0.151 → 0.152 | 0.083 → 0.074 |
| Reference | Hist. gradient boosting | 0.832 → 0.834 | 0.707 → 0.714 | 0.160 → 0.160 | 0.077 → 0.070 |
| Severe covariate | Logistic regression | 0.839 → 0.839 | 0.726 → 0.721 | 0.245 → 0.154 | 0.290 → 0.067 |
| Severe covariate | Random forest | 0.808 → 0.845 | 0.641 → 0.726 | 0.216 → 0.154 | 0.208 → 0.073 |
| Severe covariate | Hist. gradient boosting | 0.776 → 0.820 | 0.620 → 0.691 | 0.223 → 0.165 | 0.204 → 0.082 |
| MCAR 10% | Logistic regression | 0.826 → 0.827 | 0.702 → 0.702 | 0.163 → 0.162 | 0.073 → 0.075 |
| MCAR 10% | Random forest | 0.838 → 0.834 | 0.711 → 0.705 | 0.157 → 0.158 | 0.078 → 0.083 |
| MCAR 10% | Hist. gradient boosting | 0.814 → 0.813 | 0.682 → 0.667 | 0.167 → 0.167 | 0.082 → 0.079 |
| MAR-like 10% | Logistic regression | 0.845 → 0.843 | 0.730 → 0.722 | 0.153 → 0.154 | 0.069 → 0.074 |
| MAR-like 10% | Random forest | 0.850 → 0.848 | 0.726 → 0.737 | 0.151 → 0.152 | 0.079 → 0.078 |
| MAR-like 10% | Hist. gradient boosting | 0.833 → 0.833 | 0.708 → 0.715 | 0.160 → 0.161 | 0.075 → 0.068 |

### Interpretation: negative transfer is real and model/scenario-dependent

- Under the reference scenario, CORAL does not provide a consistent gain. For all three models the AUROC change is negligible (roughly -0.002 to +0.002), while some calibration metrics become slightly worse.
- Under 10% MCAR-like missingness, average CORAL AUROC/AUPRC changes are approximately -0.001/-0.007 across models; the Brier and ECE changes are also negligible or slightly adverse. Random forest AUROC fell in 4/5 seeds; random forest AUPRC fell in 3/5.
- Under 10% MAR-like missingness, average AUROC change is approximately -0.001 and average Brier worsens by about 0.001. CORAL is not a general missing-data remedy.
- Under severe covariate perturbation, CORAL materially improves random forest and histogram gradient boosting: mean AUROC changes +0.037 and +0.044 respectively. Logistic-regression AUROC is unchanged. Brier and ECE improve strongly across all three models.
- Under combined severe covariate shift and 20% MAR-like missingness, average AUROC changes are +0.036 (random forest), +0.051 (histogram gradient boosting) and -0.001 (logistic regression). AUPRC changes are +0.083, +0.081 and -0.007 respectively. CORAL also improves Brier/ECE in these simulated conditions.
- The above are descriptive means across only five seeds. Do not interpret them as statistically confirmed or as proof CORAL will help at a Nigerian hospital.

### Calibration interpretation

Severe synthetic covariate shift causes marked source-only calibration deterioration. For example, under severe covariate shift, logistic-regression Brier rises to 0.245 and ECE to 0.290 in source-only mode; CORAL gives 0.154 and 0.067. Calibration-in-the-large moves much closer to zero. Similar Brier/ECE improvement occurs for the tree models.

However, calibration improvements depend on model and scenario. Under reference and missingness-only conditions, CORAL sometimes worsens Brier/ECE. Calibration slope should be inspected alongside intercept and ECE; no universal CORAL benefit is established. A single ECE value is bin-dependent and must be accompanied by calibration plots and uncertainty estimates in the next analysis.

## 4. TreeSHAP explanation stability

Rank-biased overlap (RBO; 100 explained examples, seed 42):

| Model | Perturbation SD 0.01 | SD 0.05 | SD 0.10 |
|---|---:|---:|---:|
| Random forest | 0.994 | 0.974 | 0.963 |
| XGBoost | 0.971 | 0.965 | 0.952 |

Feature rankings are relatively stable under the tested perturbations, with lower stability as noise increases. This is a local perturbation test on Pima only, one random seed, and not evidence of explanation validity, causal relevance, clinician usefulness, or stability across Nigerian hospitals.

## 5. Statistical limitations and required next experiments

1. Five random seeds are too few for strong inferential claims. Increase repetitions and report paired uncertainty without treating overlapping repeated splits as independent patient cohorts.
2. The current synthetic test perturbations are stylised. Add clinically grounded shift ranges from Nigerian site data once authorised, and test label shift, prevalence shift, measurement-unit shifts and non-random missingness mechanisms.
3. Add calibration plots, bootstrap confidence intervals for absolute metrics, paired patient-level bootstrap for adaptation deltas, and prespecified clinically meaningful margins.
4. Complete subgroup analysis by age and BMI with event counts, sparse-cell suppression and paired bootstrap. The current Pima benchmark contains only women; it cannot evaluate sex fairness or Nigerian ethnicity/geography.
5. Add threshold decision analysis only after a clinically defined use case and operating threshold have been agreed with clinicians.
6. Validate across a genuine held-out Nigerian hospital and time period; synthetic shift cannot replace external validation.
7. Evaluate CORAL and any alternative adaptation only with target covariates available before the prediction point; keep target labels locked until final evaluation.

## 6. Reproducibility and provenance

The downloaded manifest records OpenML dataset ID 37, 768 rows, class counts 500/268, eight predictor names and SHA-256 `c980e5e01dc1c554a358102b773f34b29599d0051ec5cf5b56ad1c6fcb3a23b0`. No patient-level Nigerian data was included in the artifact.

**Bottom line:** The experiments support a narrow methodological observation: CORAL can reduce damage under the specific severe synthetic covariate shifts used here, but it offers little benefit and can produce negative transfer under reference and missingness-only scenarios. The Pima benchmark does not support Nigerian clinical claims. The next decisive step remains approved access to a real Nigerian hospital cohort.
