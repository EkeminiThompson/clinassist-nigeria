# Explanation stability protocol

Run after retrieving the verified benchmark CSV:

```bash
PYTHONPATH=. python -m ml.experiments.run_explanation_stability --seed 42 --n-explain 100
```

The script trains Random Forest and XGBoost on a stratified source-training partition, fits preprocessing only on that partition, and explains held-out benchmark rows. It perturbs the standardized held-out feature vectors at fixed noise standard deviations (0.01, 0.05, 0.10) and computes pairwise local feature-rank stability with rank-biased overlap (p=0.9). Results are written to `ml/artifacts/experiments/explanation_stability.csv`.

This is a controlled explanation-sensitivity analysis, not clinical robustness validation. A stable explanation can still be wrong, incomplete or non-causal. Report model, background sample, seed, perturbation scale and sample count. Do not compare raw attribution magnitudes across models without checking output scales and explanation semantics.