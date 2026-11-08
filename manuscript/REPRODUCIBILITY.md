# Manuscript verification and reproducibility notes

## Source artifacts

This manuscript was drafted against the ClinAssist repository at merge commit:

`4fcd3518be5f4973bb2e8229d912375f98971f5c`

The GitHub Actions run `42491430183` completed backend, frontend and research-benchmark jobs successfully. Its `clinassist-research-results` artifact (artifact ID `13621936755`) was retrieved on 8 November 2026. The artifact contains:

- `baseline_cv_results.json`
- `domain_adaptation_results.json`
- `pima_manifest.json`
- `explanation_stability.csv`
- `subgroup_metrics.csv`
- `subgroup_paired_bootstrap.csv`
- `synthetic_shift_paired_differences.csv`
- `synthetic_shift_predictions.csv`
- `synthetic_shift_runs.csv`
- `synthetic_shift_study.json`
- `synthetic_shift_summary.csv`

## Results reported in the manuscript

The manuscript uses the exact values in the archived five-seed summary for the severe combined scenario. Mean and SD are copied from `synthetic_shift_summary.csv`; they are not presented as independent patient-level confidence intervals.

The separate baseline values are copied from `baseline_cv_results.json`. They are explicitly separated from the repeated 75:25 shift study because they are a different evaluation artifact.

The explanation stability values are copied from `explanation_stability.csv`.

The subgroup counts are copied from the archived subgroup CSVs and prior CI validation: 1,638 descriptive metric rows; 819 paired-bootstrap comparisons; 609 successful comparisons; 210 suppressed comparisons; among successful comparisons, 595/12/2 had 1,000/999/998 valid bootstrap draws. The manuscript deliberately does not state subgroup-specific differences because those detailed estimates have not been independently re-analysed for manuscript reporting.

## Methodological caveats

- Five repeated random splits (seeds 42–46) have overlapping records across test partitions. Their SDs describe split variability and are not independent cohort-level uncertainty estimates.
- CORAL is transductive in this experiment because it uses the unlabelled target/test feature matrix to estimate alignment.
- The controlled target shifts are artificial transformations of Pima test covariates. They are not real hospital shifts.
- The MAR-like missingness mechanism depends on observed glucose and masks skin-thickness and insulin; it is not a validated Nigerian clinical missingness process.
- Selective prediction uses predictive entropy and retains approximately 80% of observations. This is not a clinically validated abstention policy.
- The TreeSHAP stability experiment uses one split and Gaussian perturbations. It does not establish causal interpretability.
- The public Pima dataset is not Nigerian clinical data. No Nigerian external validation, prospective evaluation or clinical deployment is claimed.

## Required before journal submission

1. Re-run the experiments from a clean checkout and compare checksums/outputs.
2. Independently recalculate every table and resolve any discrepancy.
3. Include full results for all scenarios and supplementary outputs.
4. Add justified uncertainty intervals for repeated-split summaries.
5. Complete TRIPOD+AI reporting and a risk-of-bias/applicability assessment.
6. Confirm ethics determination, author affiliation, funding, conflicts and contributions.
7. Verify all bibliographic details and obtain the original dataset citation.
8. Confirm whether the repository can be made public and archived.
9. Obtain institutional/supervisory review.

This is a working manuscript, not a submitted or published article.
