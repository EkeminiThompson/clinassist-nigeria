# ClinAssist Nigeria

Research prototype for explainable, uncertainty-aware and offline-capable clinical decision support under resource constraints.

## Data integrity
The Mendeley deposit described as UITH + General Hospital Offa was found to repackage public Pima Indians Diabetes data without hospital identifiers. ESUTH research data remain inaccessible. The current model is a **public benchmark only**. Controlled synthetic shifts are not Nigerian external validation. See docs/dataset_provenance.md.

## Features
- FastAPI with JWT authentication, roles and audit logging.
- SHAP where supported; coefficient fallback is explicitly labelled.
- Entropy-based uncertainty and abstention.
- React + Ant Design PWA and IndexedDB queue.
- Offline receipt sync metadata only; no offline inference.
- Research paper outline and security notes.

## Backend (Python 3.11 recommended)
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export PYTHONPATH="$PWD"
uvicorn backend.app.main:app --reload
```
Create first admin (same environment): set ADMIN_EMAIL, ADMIN_NAME and ADMIN_PASSWORD (12+ chars), then run `python -m backend.scripts.create_admin`.

## Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
API docs: http://localhost:8000/api/docs

## Validation and ethics
No Nigerian hospital validation is claimed. Preprocessing must be fitted inside training folds. SHAP is not causal. Clinical deployment requires ethics approval, local calibration, prospective workflow evaluation and independent external validation.
