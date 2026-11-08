# ClinAssist Nigeria

**Research title:** An Explainable, Uncertainty-Aware and Offline-Capable Domain Adaptation Framework for Multi-Hospital Clinical Decision Support in Resource-Constrained Healthcare Settings.

**Repository:** private – EkeminiThompson/clinassist-nigeria  
**Status:** Active research & engineering (Phase 2–3)

## Important Data Statement

The Mendeley deposit previously considered as “UITH + General Hospital Offa” was independently inspected and found to be a re-packaging of the public **Pima Indians Diabetes** dataset. It contains no hospital identifiers and cannot support true cross-hospital domain-adaptation claims for Nigerian sites.

The original ESUTH research dataset associated with earlier work remains inaccessible.

**Current modelling therefore uses the public Pima dataset strictly as a methodological benchmark.** All results are labelled accordingly. The software architecture and experimental pipeline are designed so that verified multi-site Nigerian cohorts can be plugged in when they become available.

See `docs/dataset_provenance.md` and `docs/research_gap.md` for the full record.

## Research Objectives

1. Develop and evaluate domain-adaptation methods suitable for small tabular clinical datasets under distribution shift.
2. Integrate calibrated uncertainty quantification and selective prediction (abstention when uncertainty is high).
3. Quantify explanation stability (SHAP) under controlled shift.
4. Investigate missing-data robustness.
5. Deliver an offline-capable clinical decision support interface suitable for Nigerian teaching-hospital infrastructure constraints.

## Architecture (high-level)

```
clinassist-nigeria/
├── backend/          # FastAPI, Pydantic, SQLAlchemy, ML inference layer
├── frontend/         # React + TypeScript + Ant Design + PWA
├── ml/
│   ├── preprocessing/
│   ├── domain_adaptation/   # CORAL and related methods
│   ├── uncertainty/         # Bootstrap & selective prediction
│   ├── explainability/
│   ├── evaluation/
│   ├── experiments/         # Reproducible experiment scripts
│   └── artifacts/           # Versioned experiment outputs (no patient data)
├── docs/             # Research methodology, governance, model cards
└── tests/
```

## Quick Start (development)

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (once scaffolded)
cd frontend
npm install
npm run dev
```

## Reproducible Baseline Experiments

```bash
cd ml
python -m experiments.run_baselines
```

Results are written to `ml/artifacts/experiments/` with full data-source provenance.

## Ethics & Intended Use

- The system is intended to **support** qualified healthcare professionals.
- It does **not** provide autonomous diagnosis or treatment recommendations.
- No identifiable patient data are stored in the repository.
- All experimental claims are restricted to the exact data and protocol used.

---

*Principal investigator / lead engineer: Ekemini Thompson*  
*This is a living research repository. Claims evolve only with evidence.*
