# ClinAssist Nigeria

Research prototype for explainable, uncertainty-aware and offline-capable clinical decision support under resource constraints.

## Data integrity
The Mendeley deposit described as UITH + General Hospital Offa was found to repackage public Pima Indians Diabetes data without hospital identifiers. ESUTH research data remain inaccessible. The current model is a **public benchmark only**. Controlled synthetic shifts are not Nigerian external validation. See docs/dataset_provenance.md.

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
The prediction workspace exposes logistic regression, Random Forest and XGBoost. The benchmark CSV is fetched and checksum-manifested with `PYTHONPATH=. python -m ml.datasets.download_pima`.

## Research experiments
```bash
PYTHONPATH=. python -m ml.experiments.run_shift_study --repeats 5
PYTHONPATH=. python -m ml.experiments.run_explanation_stability --seed 42 --n-explain 100
```
Both are controlled public-benchmark studies, not external validation. Outputs go to `ml/artifacts/experiments/` and should be archived with the generated Pima manifest.

API docs: http://localhost:8000/api/docs

## Validation and ethics
No Nigerian hospital validation is claimed. Preprocessing is fitted on source training data only; target labels are not used for CORAL adaptation. SHAP is not causal. Clinical deployment requires ethics approval, local calibration, prospective workflow evaluation and independent external validation.