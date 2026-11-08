# ClinAssist Nigeria

Research prototype for explainable, uncertainty-aware and offline-capable clinical decision support under resource constraints.

## Research paper

**Working manuscript:** [Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions](manuscript/paper1.md)

The manuscript reports a reproducible public-benchmark study using OpenML Pima Indians Diabetes dataset 37. It evaluates calibration, selective prediction, CORAL domain adaptation, controlled covariate/missingness shifts, local TreeSHAP stability and exploratory age/BMI subgroup diagnostics.

**Important:** this is a working manuscript, not a published or submitted paper. The dataset is a historical Pima cohort of adult women and is not Nigerian hospital data. Controlled target shifts are not external validation. No clinical deployment or patient-care use is authorised.

## Data integrity

The Mendeley deposit described as UITH + General Hospital Offa was found to repackage public Pima Indians Diabetes data without hospital identifiers. ESUTH research data remain inaccessible. The current model is a **public benchmark only**. Controlled shifts are not Nigerian external validation. See [docs/dataset_provenance.md](docs/dataset_provenance.md).

## Backend (Python 3.11 recommended)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export DATABASE_URL="sqlite:///./clinassist.db"
export PYTHONPATH="$PWD"
alembic upgrade head
uvicorn backend.app.main:app --reload
```

Create the first admin after migrations: set ADMIN_EMAIL, ADMIN_NAME and ADMIN_PASSWORD (12+ characters), then run `python -m backend.scripts.create_admin`.

## Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Research experiments

```bash
PYTHONPATH=. python -m ml.datasets.download_pima
PYTHONPATH=. python -m ml.experiments.run_shift_study --repeats 5
PYTHONPATH=. python -m ml.experiments.run_explanation_stability --seed 42 --n-explain 100
PYTHONPATH=. python -m ml.experiments.run_subgroup_statistical_audit --bootstrap 1000 --seed 2026
```

The shift study reports calibration, selective metrics and paired CORAL deltas; the explanation study measures local TreeSHAP rank stability; the audit reports descriptive age/BMI strata and paired within-split bootstrap intervals. Outputs go to `ml/artifacts/experiments/` and should be archived with the generated Pima manifest. GitHub Actions runs the experiments and uploads a `clinassist-research-results` artifact.

## Validation and ethics

No Nigerian hospital validation is claimed. Preprocessing is fitted on source training data only; target labels are not used for CORAL adaptation. CORAL uses unlabelled target covariates (transductive adaptation). SHAP is not causal. Clinical deployment requires ethics approval, local calibration, prospective workflow evaluation and independent external validation.
