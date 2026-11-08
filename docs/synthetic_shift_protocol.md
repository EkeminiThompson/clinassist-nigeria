# Reproducible synthetic-shift study

Run only after placing a verified, licensed public Pima CSV at `ml/datasets/diabetes_dataset.csv`:

```bash
PYTHONPATH=. python -m ml.experiments.run_shift_study --repeats 5 --missing-rate 0.10
```

The experiment performs repeated stratified source/held-out splits and compares source-only models with CORAL using *unlabelled held-out target covariates*. Target labels are used only after prediction for evaluation. Preprocessing is fitted on source training data only. The shifted cohort is created by a deterministic covariate perturbation and random feature masking; it is a synthetic stress test, not a hospital cohort, external validation, or simulated Nigerian clinical population.

Outputs are written to `ml/artifacts/experiments/`: per-repeat metrics, grouped mean/standard deviation, and a JSON provenance manifest. The script intentionally does not publish headline performance claims. Report uncertainty intervals and all seeds when interpreting results. This is an initial controlled protocol, not proof of domain adaptation benefit.
