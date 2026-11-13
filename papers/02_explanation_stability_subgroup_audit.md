# Explanation Stability and Subgroup Audit under Controlled Distribution Shift for Tabular Diabetes Risk Models

**Author:** Ekemini Thompson  
**Status:** Supplementary technical report to the calibration and domain-adaptation manuscript  
**Study type:** Exploratory sensitivity and subgroup audit on a public benchmark

## Abstract

Post-hoc explanation methods such as TreeSHAP provide feature-attribution summaries for individual predictions. Explanation stability under input perturbation is distinct from explanation validity. This report quantifies local TreeSHAP rank stability under standardised perturbations and reports an age- and body-mass-index-stratified audit with paired within-split bootstrap intervals for source-only versus CORAL predictions on the public Pima Indians Diabetes benchmark under controlled synthetic shift. Mean rank-biased overlap for random forest ranged from 0.994 to 0.963 across increasing noise levels; for XGBoost the range was 0.971 to 0.952. The subgroup audit produced 1,638 metric rows and 819 paired comparisons, of which 609 yielded usable intervals. Under combined severe shift, paired bootstrap intervals showed lower Brier scores for CORAL in all 15 model-by-seed comparisons.

**Keywords:** TreeSHAP; explanation stability; rank-biased overlap; subgroup analysis; paired bootstrap; domain adaptation.

## 1. Explanation stability

TreeSHAP explanations were computed for random forest and XGBoost on 100 held-out examples (seed 42). Standardised Gaussian perturbations were applied at noise standard deviations 0.01, 0.05 and 0.10. Feature rankings were compared using rank-biased overlap (RBO) with persistence parameter 0.9.

| Model | Noise SD 0.01 | Noise SD 0.05 | Noise SD 0.10 |
|-------|--------------:|--------------:|--------------:|
| Random forest (RBO) | 0.994 | 0.974 | 0.963 |
| XGBoost (RBO) | 0.971 | 0.965 | 0.952 |

*Table 1. Mean rank-biased overlap of TreeSHAP feature rankings (100 cases).*

## 2. Subgroup statistical audit

Age strata: <30, 30–49, ≥50 years. BMI strata: <18.5, 18.5–24.9, 25–29.9, ≥30. Zero BMI values excluded. Eligibility: ≥20 observations and ≥5 events per outcome class. Paired bootstrap (1,000 replicates) with identical patient indices for source-only and CORAL.

| Quantity | Count |
|---|---:|
| Subgroup metric rows | 1,638 |
| Paired-bootstrap comparisons | 819 |
| Usable intervals (≥90% valid draws) | 609 |
| Sparse comparisons suppressed | 210 |
| Model×seed cells with CORAL Brier gain (severe combined) | 15 / 15 |
| Model×seed cells with AUROC interval excluding 0 | 6 / 15 |
| Model×seed cells with AUPRC interval excluding 0 | 5 / 15 |

*Table 2. Subgroup audit summary counts.*

## 3. Discussion

Local TreeSHAP rankings were highly stable under modest perturbation. Calibration gains from CORAL under severe controlled shift were consistent across the model-by-seed grid. Stratified precision is limited by cell size on this benchmark; the eligibility rule and suppression log define a reusable protocol for larger cohorts.

## 4. Data and code availability

`EkeminiThompson/clinassist-nigeria`. Independent verification: `docs/independent_verification.md`.
