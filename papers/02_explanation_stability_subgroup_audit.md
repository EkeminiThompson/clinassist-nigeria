# Explanation Stability and Subgroup Audit under Controlled Distribution Shift for Tabular Diabetes Risk Models

**Companion working paper**  
**Author:** Ekemini Thompson  
**Status:** Exploratory sensitivity analysis on a public benchmark. No clinical validation claimed.

## Abstract

Post-hoc explanation methods such as TreeSHAP provide feature-attribution summaries for individual predictions, but explanation stability under input perturbation is distinct from explanation validity. This companion paper reports (1) local TreeSHAP rank stability under standardised perturbations and (2) an exploratory age- and BMI-stratified audit with paired within-split bootstrap intervals for source-only versus CORAL predictions. All analyses use the public Pima Indians Diabetes benchmark under controlled synthetic shift. No Nigerian clinical validity or fairness claim is made. Subgroup analyses are exploratory; sparse strata are explicitly suppressed.

## 1. Explanation stability protocol

TreeSHAP explanations were computed for random forest and XGBoost on 100 held-out examples (seed 42). Standardised Gaussian perturbations were applied independently to each feature at noise standard deviations 0.01, 0.05 and 0.10. Feature rankings were compared using rank-biased overlap (RBO) with persistence parameter 0.9.

| Model | Noise SD 0.01 | Noise SD 0.05 | Noise SD 0.10 |
|-------|--------------:|--------------:|--------------:|
| Random forest (RBO) | 0.994 | 0.974 | 0.963 |
| XGBoost (RBO) | 0.971 | 0.965 | 0.952 |

*Table 1. Mean rank-biased overlap of TreeSHAP feature rankings under standardised input perturbation (100 cases).*

## 2. Subgroup statistical audit

**Planned strata:** age (<30, 30–49, ≥50) and BMI (<18.5, 18.5–24.9, 25–29.9, ≥30). Zero BMI values excluded from BMI strata. Eligibility: ≥20 observations and ≥5 events per outcome class; sparse strata retain denominators but do not receive unstable discrimination estimates. Paired bootstrap (1,000 replicates) used identical patient indices for source-only and CORAL within each seed/model/scenario.

**Execution status:** completed in GitHub Actions (1,638 metric rows; 819 paired comparisons; 609 usable intervals; 210 sparse comparisons suppressed).

Overall paired bootstrap intervals under combined severe shift showed lower Brier scores for CORAL in all 15 model-by-seed comparisons. AUROC and AUPRC intervals excluded zero in 6/15 and 5/15 comparisons respectively. Age- and BMI-stratified results were substantially less precise and frequently suppressed.

## 3. Interpretation constraints

Explanation stability does not imply clinical validity of feature attributions. Subgroup analyses on a small public benchmark cannot establish fairness, equity or transportability to Nigerian teaching hospitals. The audit is reported for transparency and to pre-specify analysis choices before any future multi-site data become available.

---
*Companion to the calibration and domain-adaptation working paper. No clinical validation claimed.*
