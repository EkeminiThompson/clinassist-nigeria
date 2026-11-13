# Independent verification report

**Date:** 2026-11-13  
**Environment:** clean Python 3.12, scikit-learn 1.9.1, xgboost 3.4.1  
**Repository:** EkeminiThompson/clinassist-nigeria  

## Baseline five-fold CV (independent rerun)

| Model | AUROC | AUPRC | Brier | ECE |
|---|---:|---:|---:|---:|
| Logistic regression | 0.8349 | 0.7067 | 0.1571 | 0.0360 |
| Random forest | 0.8342 | 0.6977 | 0.1574 | 0.0398 |
| Gradient boosting | 0.8265 | 0.6927 | 0.1676 | 0.0839 |
| XGBoost | 0.8247 | 0.6920 | 0.1643 | 0.0642 |
| RBF SVM | 0.8211 | 0.6967 | 0.1642 | 0.0548 |

**Reconciliation:** Matches the archived CI / manuscript baseline table to reported precision.

## Domain adaptation (independent rerun, age/BMI controlled shift)

| Shift | Source-only AUROC | CORAL AUROC | Source-only ECE | CORAL ECE |
|---|---:|---:|---:|---:|
| Age (threshold 29) | 0.7095 | 0.7532 | 0.3474 | 0.1311 |
| BMI (threshold 32) | 0.7550 | 0.7621 | 0.4022 | 0.1236 |

CORAL reduced ECE under both controlled shifts in this rerun.

## Data provenance

Public OpenML / Pima Indians Diabetes benchmark (n = 768). Not Nigerian hospital data.
