# Paper 1 subgroup audit: execution and results

**Workflow:** [GitHub Actions run 42472051266](https://github.com/EkeminiThompson/clinassist-nigeria/actions/runs/42472051266)  
**Evaluated commit:** `2d3abe3199288cda92fb679beb1c97a674a5d9c2`  
**Artifact:** `clinassist-research-results`, ID `13613489987`  
**Artifact SHA-256:** `f315ebe4d3e599b75281b534984d4a9bddf255375a99e0dd9f808efbcdae2e29`  
**Dataset:** OpenML 37, version 1; 768 historical Pima cohort records; methodological benchmark only.

## 1. CI execution

All three workflow jobs completed successfully:

- Backend: dependency installation, Alembic migration, test suite and application import passed.
- Frontend: dependency installation and production build passed.
- Research benchmarks: public dataset retrieval, repeated controlled-shift experiment, TreeSHAP stability experiment, subgroup audit and artifact upload passed.

The research job generated both `subgroup_metrics.csv` and `subgroup_paired_bootstrap.csv`.

## 2. Audit volume and validation

| Check | Result |
|---|---:|
| Subgroup metric rows | 1,638 |
| Paired-bootstrap comparison rows | 819 |
| Successful interval rows | 609 |
| Explicitly suppressed sparse rows | 210 |
| Unique comparison keys | 819 |
| Paired source-only/CORAL count mismatches | 0 |
| Paired source-only/CORAL event-count mismatches | 0 |
| Successful rows with 1,000 valid draws | 595 |
| Successful rows with 999 valid draws | 12 |
| Successful rows with 998 valid draws | 2 |

The audit requested 1,000 bootstrap draws per eligible comparison and required at least 900 valid draws. All 609 successful comparisons met that threshold. Successful intervals were finite and ordered for AUROC, AUPRC and Brier score. The paired source-only and CORAL arms contained identical held-out patient rows and labels.

The bootstrap resamples held-out patient rows with replacement and applies the same sampled indices to both prediction arms. Each interval is conditional on its split/model/scenario comparison. The five seeds have overlapping held-out participants and must not be treated as independent cohorts or pooled into a single confirmatory interval.

## 3. Sparse-stratum handling

Eligibility required at least 20 observations and at least five observations in each outcome class. Sparse strata retain their denominator/event counts but do not receive unstable discrimination or Brier estimates.

- Age strata: 315 comparison rows; 294 eligible intervals and 21 suppressed rows.
- BMI strata: 399 comparison rows; 210 eligible intervals and 189 suppressed rows.
- Overall group: 105 comparison rows; all 105 eligible.

The underweight BMI stratum (<18.5) contained only one participant when present. The 18.5–24.9 BMI stratum had only 0–3 events in held-out splits and was suppressed. The older-age stratum sometimes failed the minimum sample-size threshold. These data do not support reliable fairness or subgroup-parity claims.

## 4. Combined-severe scenario

For the overall group, the observed CORAL-minus-source-only AUROC differences averaged across five split-specific comparisons were:

| Model | Mean observed AUROC difference |
|---|---:|
| Logistic regression | -0.0008 |
| Random forest | +0.0367 |
| Histogram gradient boosting | +0.0508 |

Across the 15 model-by-seed comparisons in this scenario:

- AUROC percentile intervals excluded zero in 6/15 comparisons.
- AUPRC percentile intervals excluded zero in 5/15 comparisons.
- Brier-score intervals favoured CORAL (negative CORAL-minus-source-only difference) in 15/15 comparisons.

The results are conditional on the held-out split and are not multiplicity-adjusted. They should be described as exploratory, not as proof of a universal adaptation benefit.

For the age strata, 42 combined-severe intervals were available; 3/42 AUROC, 4/42 AUPRC and 20/42 Brier intervals excluded zero. For BMI strata, 30 intervals were available; 4/30 AUROC, 3/30 AUPRC and 21/30 Brier intervals excluded zero. These counts are descriptive only and do not constitute a fairness test.

## 5. Reproducibility and interpretation

The run validates that the corrected audit executes and that the required output schemas and minimum bootstrap checks pass. It does not validate the clinical relevance of the chosen age/BMI bins or the controlled shifts. The underlying cohort is historical and female-only; the subgroup analysis is not Nigerian demographic analysis, external validation, clinical validation or fairness certification.

## 6. Remaining work

1. Finalise calibration figures and explain the repeated-split aggregation used for descriptive plots.
2. Complete TRIPOD+AI and PROBAST+AI appraisals.
3. Obtain supervisor review and confirm author list, order and CRediT contributions.
4. Obtain the appropriate institutional ethics determination for secondary public-data analysis if required.
5. Select a journal that accepts methodological public-benchmark work and complete its formatting requirements.
6. Keep a future Nigerian hospital external-validation study separate, with authentic authorised clinical data and required ethics/data-governance approvals.
