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
| Exact experiment protocol | [`docs/experiment_protocol.md`](docs/experiment_protocol.md) |

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
python -m ml.datasets.download_pima
python -m ml.experiments.run_baselines
python -m ml.experiments.run_shift_study --repeats 5
python -m ml.experiments.run_explanation_stability --seed 42 --n-explain 100
python -m ml.experiments.run_subgroup_statistical_audit --bootstrap 1000 --seed 2026
```

Outputs are written to `ml/artifacts/experiments/`. The shift study writes the raw split-level metrics, patient-level predictions, summary table, paired differences and JSON manifest used by the subgroup audit. The subgroup audit must be run after the shift study.

## Software stack

FastAPI backend, React frontend (PWA path), experiment pipeline under `ml/`. See backend and frontend READMEs for local development.

## Citation

**Software archive:** Thompson, E. (2026). *ClinAssist Nigeria: Calibration, Domain Adaptation and Explanation Stability Benchmark* (v0.1.0). Zenodo. https://doi.org/10.5281/zenodo.24215668

**Manuscript:** Thompson, E. Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions. Research manuscript, `EkeminiThompson/clinassist-nigeria` (2026).


## Repeated-shift experiment outputs

The seven-scenario, five-seed shift-study outputs are stored under `ml/artifacts/experiments/` after the reproducibility CI commit. See `docs/experiment_protocol.md` for the verified run record and `papers/01_calibration_domain_adaptation_diabetes.md` Appendix B for the paired scenario comparison.

## Submission and archiving metadata

See [submission metadata and template instructions](docs/submission_metadata.md) for the computing-environment statement, Associate Editor confirmation note, ACM author-year BibLaTeX setup, and optional Zenodo deposit preparation.
