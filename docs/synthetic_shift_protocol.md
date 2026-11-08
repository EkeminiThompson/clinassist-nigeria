# Factorial controlled synthetic-shift study

Run after fetching and verifying the local benchmark CSV:

```bash
PYTHONPATH=. python -m ml.experiments.run_shift_study --repeats 5
```

The protocol compares source-only training with CORAL across an unshifted reference, mild/severe covariate shifts, MCAR-like missingness, glucose-dependent MAR-like missingness, and combined scenarios. Preprocessing and sigmoid calibration are fitted on source-training data only. CORAL sees only held-out target covariates; held-out labels are used only after prediction for evaluation.

Outputs include per-split metrics, mean/standard-deviation summaries and paired CORAL-minus-source-only differences. Repeated-split variability is not a patient-level confidence interval. The benchmark is historical Pima data, not a Nigerian cohort; synthetic stress tests are not external validation. Negative transfer must be reported.