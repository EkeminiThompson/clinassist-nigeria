# Research benchmark results review

**Latest completed workflow:** GitHub Actions run [42464788999](https://github.com/EkeminiThompson/clinassist-nigeria/actions/runs/42464788999)  
**Commit evaluated by that run:** `bd648d4e927da13bf3008cb6d53f9b3e2528f82f`  
**Artifact:** `clinassist-research-results` (ID `13613280079`; ZIP SHA-256 `9af01326e273b5ddbd14f9a2ed6a6efdc6bf7b3c3d27dc24add7afb004387ea7`)  
**Current PR branch head when this review was updated:** see [PR #1](https://github.com/EkeminiThompson/clinassist-nigeria/pull/1).  
**Dataset:** OpenML data ID 37, version 1; 768 records, eight predictors, 500 negative and 268 positive.  
**Interpretation:** Pima methodological benchmark only. It is not Nigerian hospital data, external validation, clinical validation, or evidence of Nigerian population generalisability.

## 1. Execution and artifact audit

Backend and frontend CI passed in the completed run. Benchmark retrieval, five-repeat controlled shift experiment and TreeSHAP explanation-stability experiment completed. The artifact contains:

- `baseline_cv_results.json`
- `domain_adaptation_results.json`
- `explanation_stability.csv`
- `synthetic_shift_paired_differences.csv`
- `synthetic_shift_predictions.csv`
- `synthetic_shift_runs.csv`
- `synthetic_shift_study.json`
- `synthetic_shift_summary.csv`
- `pima_manifest.json`

**The subgroup audit did not complete.** The workflow was cancelled during that step. Neither `subgroup_metrics.csv` nor `subgroup_paired_bootstrap.csv` exists in this artifact. No subgroup metric or subgroup confidence interval is reported here.

The subgroup audit implementation has since been replaced with a vectorised paired-bootstrap implementation, stricter prediction/label pairing checks, tie-aware AUPRC computation, explicit sparse-stratum suppression and stronger artifact assertions. Those changes are on the PR branch after the commit evaluated by run 42464788999. They remain unverified by a fresh successful GitHub Actions run.

## 2. Benchmark provenance

The manifest records:

- OpenML dataset ID 37, version 1 (`diabetes`)
- 768 observations and eight predictors
- 500 negative and 268 positive outcome labels
- CSV SHA-256: `c980e5e01dc1c554a358102b773f34b29599d0051ec5cf5b56ad1c6fcb3a23b0`

The dataset represents adult women of Pima heritage in the historical Arizona cohort. It must be described as a public methodological benchmark only. The Mendeley UITH/General Hospital Offa-labelled release was found to reproduce the Pima values/schema and lacks independent site identifiers; it is not independent Nigerian validation.

## 3. Five-fold baseline comparison

| Model | AUROC | AUPRC | Brier | ECE | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.835 | 0.707 | 0.157 | 0.036 | 0.571 | 0.880 |
| Random forest | 0.834 | 0.698 | 0.157 | 0.040 | 0.563 | 0.864 |
| Gradient boosting | 0.827 | 0.693 | 0.168 | 0.084 | 0.627 | 0.826 |
| XGBoost | 0.825 | 0.692 | 0.164 | 0.064 | 0.616 | 0.836 |
| RBF SVM | 0.821 | 0.697 | 0.164 | 0.055 | 0.541 | 0.868 |

The five-fold baseline does not show a compelling discrimination advantage for the more complex tree/boosting estimators over logistic regression. Logistic regression had the highest AUROC/AUPRC and lowest Brier/ECE in this run. These results are specific to this dataset and evaluation pipeline.

## 4. Repeated controlled distribution-shift experiment

Design: three models (logistic regression, random forest, histogram gradient boosting), seven scenarios, two arms (source-only and CORAL), five seeds (42–46), and stratified 75/25 source/held-out splits. This produced 210 model/scenario/arm evaluations. Preprocessing and sigmoid calibration were fitted on source training data. CORAL used held-out target covariates without target labels. The held-out labels were used for evaluation only.

The shifts are controlled perturbations of Pima held-out rows. The glucose/BMI/age perturbations and MCAR-/MAR-like missingness are stylised stress tests, not observed hospital or site shifts.

### Paired mean changes in discrimination

The table gives the mean CORAL-minus-source-only difference across five split seeds. Standard deviations across seeds describe split variability; they are not independent patient-level confidence intervals.

| Scenario | Logistic regression AUROC Δ | Random forest AUROC Δ | Hist. gradient boosting AUROC Δ |
|---|---:|---:|---:|
| Reference | -0.0019 | -0.0021 | +0.0019 |
| Severe covariate shift | -0.0004 | +0.0373 | +0.0437 |
| MCAR-like 10% | +0.0011 | -0.0033 | -0.0006 |
| MAR-like 10% | -0.0019 | -0.0018 | +0.0007 |
| Combined severe shift + MAR-like 20% | -0.0007 | +0.0362 | +0.0505 |

### Selected combined-severe results

| Model | Arm | AUROC | AUPRC | Brier | ECE |
|---|---|---:|---:|---:|---:|
| Logistic regression | Source-only | 0.8391 | 0.7273 | 0.2450 | 0.2900 |
| Logistic regression | CORAL | 0.8384 | 0.7206 | 0.1547 | 0.0643 |
| Random forest | Source-only | 0.8069 | 0.6433 | 0.2210 | 0.2172 |
| Random forest | CORAL | 0.8431 | 0.7258 | 0.1540 | 0.0765 |
| Hist. gradient boosting | Source-only | 0.7718 | 0.6141 | 0.2269 | 0.2094 |
| Hist. gradient boosting | CORAL | 0.8223 | 0.6950 | 0.1638 | 0.0754 |

Under severe covariate shift, CORAL improved mean AUROC for random forest (+0.0373) and histogram gradient boosting (+0.0437), while logistic-regression AUROC was effectively unchanged. Under combined severe covariate shift and MAR-like missingness, the corresponding AUROC changes were +0.0362, +0.0505 and -0.0007. Brier score and ECE improved in these severe simulated scenarios.

The results do **not** show that CORAL is generally beneficial. In reference conditions and missingness-only scenarios, discrimination changes were small, inconsistent or adverse depending on the model and metric. Under reference conditions, logistic regression and random forest AUROC declined slightly with CORAL. Under MCAR-like missingness, random-forest AUPRC declined by 0.0052 and histogram-gradient-boosting AUPRC by 0.0149. Under MAR-like missingness, results were mixed across models and metrics.

The defensible interpretation is conditional: CORAL may help selected tree-based models under the specific severe covariate perturbations used in this experiment, but it is not a universal remedy for missingness or distribution shift. Five seeds are insufficient for confirmatory inference.

## 5. TreeSHAP explanation stability

Rank-biased overlap (RBO) for 100 explained cases, seed 42:

| Model | Noise SD 0.01 | Noise SD 0.05 | Noise SD 0.10 |
|---|---:|---:|---:|
| Random forest | 0.994 | 0.974 | 0.963 |
| XGBoost | 0.971 | 0.965 | 0.952 |

Feature-rank stability declined as perturbation magnitude increased. This is a local sensitivity experiment on Pima data, with one seed. It does not establish explanation correctness, causal validity, clinician usefulness or cross-hospital stability.

## 6. Subgroup and paired-bootstrap audit — outstanding

The intended audit reports overall, age (<30, 30–49, 50+) and BMI (<18.5, 18.5–24.9, 25–29.9, >=30) strata. Zero BMI is excluded from BMI grouping. Strata with fewer than 20 observations or fewer than five events in either class must retain denominator information but suppress unstable discrimination estimates. The paired bootstrap resamples the same held-out patient rows for source-only and CORAL predictions within each seed/model/scenario.

**No subgroup results can yet be reported.** The latest completed artifact has no subgroup CSVs. The updated implementation must pass a fresh run and the uploaded files must be checked for:
- non-empty rows and required columns;
- correct subgroup denominators and event counts;
- paired source-only/CORAL rows and identical labels;
- at least 900 valid draws from each requested 1,000-replicate bootstrap where the stratum is eligible;
- finite, ordered percentile confidence limits;
- explicit sparse-stratum status rather than unstable estimates.

These Pima age/BMI strata cannot support Nigerian fairness claims. The cohort is female-only and cannot assess sex differences.

## 7. Statistical and reporting limitations

1. Five repeated splits describe sensitivity to the chosen split seeds; overlapping participants mean these are not independent replications.
2. The controlled shift grid is stylised and cannot establish real-world site or temporal robustness.
3. No independent Nigerian cohort, prospective evaluation or clinical workflow assessment is available.
4. Calibration plots and uncertainty intervals for the main scenario-level metrics should accompany the final manuscript.
5. Subgroup analysis is pending; no subgroup fairness conclusion is supported.
6. The outcome is the historical Pima dataset label, not a validated Nigerian prospective diabetes-risk endpoint.
7. The study does not establish clinical utility or justify diagnosis, screening, triage or treatment decisions.

## 8. Reproducibility and manuscript status

The workflow artifact preserves baseline results, repeated split-level results, predictions, paired differences, summary metrics, TreeSHAP stability results and the dataset manifest. The manifest records the dataset version and SHA-256. The subgroup audit outputs are absent and must not be implied by the current artifact.

Before journal submission, add the successful subgroup audit artifact, calibration plots, final figures/tables, a complete literature synthesis, a TRIPOD+AI-aligned manuscript checklist, full author contribution statements and a target-journal-specific format check.

**Bottom line:** The completed experiments support a narrow methodological finding about model- and scenario-dependent CORAL behaviour under controlled shifts. They do not establish Nigerian clinical validity or generalisability. The corrected subgroup audit is the immediate reproducibility gate.
