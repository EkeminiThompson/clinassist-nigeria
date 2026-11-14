# ClinAssist Nigeria

**Explainable, uncertainty-aware clinical prediction research under distribution shift.**

Publication package for a reproducible computational benchmark study of discrimination, calibration, selective prediction and explanation stability under controlled covariate and missingness shift, with unsupervised CORAL domain adaptation.

| Resource | Location |
|---|---|
| Software licence | [`LICENSE`](LICENSE) — MIT for repository code |
| Manuscript reproducibility status | [`docs/manuscript_reproducibility_status.md`](docs/manuscript_reproducibility_status.md) |
| Primary manuscript | [`papers/01_calibration_domain_adaptation_diabetes.md`](papers/01_calibration_domain_adaptation_diabetes.md) |
| Supplementary audit | [`papers/02_explanation_stability_subgroup_audit.md`](papers/02_explanation_stability_subgroup_audit.md) |
| Independent verification | [`docs/independent_verification.md`](docs/independent_verification.md) |
| Publication readiness | [`docs/publication_readiness.md`](docs/publication_readiness.md) |
| Dataset provenance | [`docs/dataset_provenance.md`](docs/dataset_provenance.md) |

## Key results (independently verified 2026-11-13)

- Five-fold baseline: logistic regression AUROC 0.835, Brier 0.157, ECE 0.036.
- Under severe controlled shift, CORAL substantially reduces Brier score and ECE for logistic regression, random forest and histogram gradient boosting; discrimination gains are model-dependent.
- TreeSHAP rank-biased overlap remains high (0.95–0.99) under modest input noise.

**Data scope:** public OpenML / Pima Indians Diabetes benchmark only. Not Nigerian hospital data. Not clinical validation.

## Reproduce experiments

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
export PYTHONPATH="$PWD"
python -m ml.datasets.download_pima   # if present
python -m ml.experiments.run_baselines
python -m ml.experiments.run_domain_adaptation
```

Outputs: `ml/artifacts/experiments/`.

## Software stack

FastAPI backend, React frontend (PWA path), experiment pipeline under `ml/`. See backend and frontend READMEs for local development.

## Citation

Thompson, E. Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions. Research manuscript, `EkeminiThompson/clinassist-nigeria` (2026).
