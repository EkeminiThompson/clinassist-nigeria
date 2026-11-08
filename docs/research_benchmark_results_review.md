# Research benchmark results review

**Latest completed workflow:** GitHub Actions run [42472051266](https://github.com/EkeminiThompson/clinassist-nigeria/actions/runs/42472051266)  
**Commit evaluated by that run:** `2d3abe3199288cda92fb679beb1c97a674a5d9c2`  
**Artifact:** `clinassist-research-results` (ID `13613489987`; ZIP SHA-256 `f315ebe4d3e599b75281b534984d4a9bddf255375a99e0dd9f808efbcdae2e29`)  
**Current PR branch head when this review was updated:** see [PR #1](https://github.com/EkeminiThompson/clinassist-nigeria/pull/1).  
**Dataset:** OpenML data ID 37, version 1; 768 records, eight predictors, 500 negative and 268 positive.  
**Interpretation:** Pima methodological benchmark only. It is not Nigerian hospital data, external validation, clinical validation, or evidence of Nigerian population generalisability.

## 1. Execution and artifact audit

Backend, frontend and research-benchmark jobs all passed in run 42472051266. Benchmark retrieval, five-repeat controlled-shift experiment, TreeSHAP explanation-stability experiment and the subgroup/paired-bootstrap audit all completed. The artifact contains:

- `baseline_cv_results.json`
- `domain_adaptation_results.json`
- `explanation_stability.csv`
- `synthetic_shift_paired_differences.csv`
- `synthetic_shift_predictions.csv`
- `synthetic_shift_runs.csv`
- `synthetic_shift_study.json`
- `synthetic_shift_summary.csv`
- `pima_manifest.json`

The artifact includes `subgroup_metrics.csv` (1,638 rows) and `subgroup_paired_bootstrap.csv` (819 rows). The workflow reported 609 successful interval comparisons and 210 explicitly suppressed sparse-stratum comparisons. The downloaded ZIP was independently inspected. All three CI jobs and the subgroup audit step completed successfully.

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

## 6. Subgroup and paired-bootstrap audit — completed

The intended audit reports overall, age (<30, 30–49, 50+) and BMI (<18.5, 18.5–24.9, 25–29.9, >=30) strata. Zero BMI is excluded from BMI grouping. Strata with fewer than 20 observations or fewer than five events in either class must retain denominator information but suppress unstable discrimination estimates. The paired bootstrap resamples the same held-out patient rows for source-only and CORAL predictions within each seed/model/scenario.

**Audit result:** The completed run produced 1,638 metric rows and 819 paired-bootstrap rows. The source-only and CORAL arms had exactly matching held-out patient counts and event counts in every paired comparison. All 819 comparison keys were unique. Among successful comparisons, 595 used 1,000 valid bootstrap replicates, 12 used 999 and two used 998; all exceed the 900-replicate threshold. All successful interval bounds were finite and ordered. Sparse rows were explicitly labelled `insufficient subgroup events` and contained no unstable metric estimates. The uploaded files were independently checked for:
- non-empty rows and required columns;
- valid denominators and event counts;
- identical source-only/CORAL patient rows and labels;
- at least 900 valid draws from each requested 1,000-replicate bootstrap where eligible;
- finite, ordered percentile confidence limits;
- explicit sparse-stratum status rather than unstable estimates.

Across the overall group in the combined-severe scenario, paired-bootstrap AUROC intervals excluded zero in 6/15 model-by-seed comparisons, AUPRC intervals in 5/15, and Brier intervals favoured CORAL in 15/15. In the age strata, 42 combined-severe intervals were available; AUROC/AUPRC/Brier intervals excluded zero in 3/42, 4/42 and 20/42 comparisons. In BMI strata, 30 intervals were available; the corresponding counts were 4/30, 3/30 and 21/30. These are exploratory within-split comparisons, not multiplicity-adjusted subgroup tests.

The underweight BMI stratum contained one participant when present. The 18.5–24.9 BMI stratum had 0–3 events in held-out splits and was suppressed. The older-age stratum sometimes fell below the minimum sample-size threshold. These Pima age/BMI strata cannot support Nigerian fairness claims. The cohort is female-only and cannot assess sex differences.

## 7. Statistical and reporting limitations

1. Five repeated splits describe sensitivity to the chosen split seeds; overlapping participants mean these are not independent replications.
2. The controlled shift grid is stylised and cannot establish real-world site or temporal robustness.
3. No independent Nigerian cohort, prospective evaluation or clinical workflow assessment is available.
4. Descriptive calibration curves have been generated from repeated held-out predictions; final uncertainty-aware calibration reporting remains necessary.
5. Subgroup estimates are sparse and exploratory; no subgroup fairness conclusion is supported.
6. The outcome is the historical Pima dataset label, not a validated Nigerian prospective diabetes-risk endpoint.
7. The study does not establish clinical utility or justify diagnosis, screening, triage or treatment decisions.

## 8. Reproducibility and manuscript status

The workflow artifact preserves baseline results, repeated split-level results, predictions, paired differences, summary metrics, TreeSHAP stability results, subgroup metrics, paired-bootstrap intervals and the dataset manifest. The manifest records the dataset version and SHA-256. Run 42472051266 passed backend, frontend and research-benchmark jobs on the current PR head.

Before journal submission, add final calibration plots, reconcile final figures/tables with the completed artifact, complete a literature synthesis, finish TRIPOD+AI and PROBAST+AI appraisals, obtain supervisor review, confirm authorship/contributions and declarations, and perform a target-journal-specific format check.

**Bottom line:** The completed experiments support a narrow methodological finding about model- and scenario-dependent CORAL behaviour under controlled shifts. The subgroup audit now runs successfully and its sparse-stratum limitations are documented. The work still does not establish Nigerian clinical validity or generalisability.
