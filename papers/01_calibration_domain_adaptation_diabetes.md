# Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions

**Working paper — methodological benchmark study**  
**Author:** Ekemini Thompson  
**Status:** Not peer-reviewed. No clinical validation claimed.

## Abstract

Clinical prediction models can lose discrimination and calibration when predictor distributions change between development and evaluation. Unsupervised domain adaptation is one proposed response, but benefits may depend on model class and shift severity. We used the public OpenML Pima Indians Diabetes dataset (n=768) as a methodological benchmark — not a Nigerian clinical cohort — to compare logistic regression, random forest, gradient boosting, XGBoost and RBF SVM under five-fold cross-validation, and to evaluate CORrelation ALignment (CORAL) under a prespecified grid of controlled covariate and missingness shifts. Logistic regression achieved AUROC 0.835, AUPRC 0.707, Brier 0.157 and ECE 0.036. Under severe controlled covariate shift, CORAL improved mean AUROC for random forest (+0.037) and histogram gradient boosting (+0.044) and substantially reduced Brier score and ECE; under reference and missingness-only scenarios effects were negligible or adverse. TreeSHAP rank-biased overlap remained high (0.952–0.994) under modest input perturbation. These findings are methodological and exploratory; they do not establish Nigerian clinical validity, fairness or generalisability.

**Keywords:** diabetes classification; calibration; domain adaptation; CORAL; distribution shift; selective prediction; SHAP; Pima Indians Diabetes.

## 1. Introduction

Machine-learning models for diabetes classification are often evaluated on a single dataset or through internal resampling. Such evaluations do not establish that a model will retain performance when predictor distributions, measurement practices or patient populations change. Domain adaptation methods such as CORrelation ALignment (CORAL) align second-order feature statistics without requiring target labels. Their computational simplicity is attractive for tabular settings, but adaptation is not guaranteed to improve downstream performance and can produce negative transfer. Calibration is a distinct property from discrimination: a model may preserve ranking while becoming poorly calibrated.

This study addresses four questions: (1) how common classifiers compare in discrimination and calibration on the selected public benchmark; (2) whether CORAL changes discrimination and calibration under controlled covariate and missingness perturbations; (3) whether effects are consistent across model classes; and (4) how stable local TreeSHAP feature rankings are under standardised input perturbations. The contribution is a reproducible, model- and scenario-stratified evaluation with explicit reporting of negative or negligible adaptation effects. No claim is made of Nigerian multi-hospital external validation.

## 2. Methods (summary)

**Data.** OpenML dataset 37 (Pima Indians Diabetes), 768 observations, eight predictors, 500/268 outcome balance. The dataset is a historical cohort of adult women of Pima heritage; it is not a Nigerian cohort. A Mendeley deposit labelled as UITH/General Hospital Offa was excluded after provenance review found it reproduces Pima values without site identifiers.

**Preprocessing.** Physiological zeros treated as missing; median imputation and scaling fitted within training partitions only.

**Benchmark.** Stratified five-fold CV for logistic regression, random forest, gradient boosting, XGBoost and RBF SVM.

**Shift study.** Five stratified 75:25 splits (seeds 42–46); seven scenarios (reference, mild/severe covariate, MCAR 10%, MAR-like 10%, combined mild, combined severe). CORAL fitted on source features and target covariates only (no target labels).

**Outcomes.** AUROC, AUPRC, Brier, ECE, calibration intercept/slope, selective metrics at 80% coverage. Explanation stability: TreeSHAP rank-biased overlap (p=0.9) at noise SD 0.01, 0.05, 0.10 on 100 cases.

## 3. Results

### 3.1 Five-fold benchmark

| Model | AUROC | AUPRC | Brier | ECE | Sens. | Spec. |
|-------|------:|------:|------:|----:|------:|------:|
| Logistic regression | 0.835 | 0.707 | 0.157 | 0.036 | 0.571 | 0.880 |
| Random forest | 0.834 | 0.698 | 0.157 | 0.040 | 0.563 | 0.864 |
| Gradient boosting | 0.827 | 0.693 | 0.168 | 0.084 | 0.627 | 0.826 |
| XGBoost | 0.825 | 0.692 | 0.164 | 0.064 | 0.616 | 0.836 |
| RBF SVM | 0.821 | 0.697 | 0.164 | 0.055 | 0.541 | 0.868 |

*Table 1. Stratified five-fold cross-validation on the public Pima benchmark.*

### 3.2 Controlled domain-adaptation experiment

Under severe controlled covariate shift, CORAL improved AUROC for random forest (+0.037) and histogram gradient boosting (+0.044); logistic regression was essentially unchanged. Under combined severe covariate shift and MAR-like missingness at 20%, corresponding AUROC changes were +0.036 and +0.051. Calibration deterioration under severe scenarios was pronounced in source-only models; CORAL reduced Brier score and ECE substantially in those settings. Under reference and missingness-only scenarios, adaptation effects were small, inconsistent or adverse.

| Scenario | LogReg ΔAUROC | RF ΔAUROC | HistGB ΔAUROC |
|----------|--------------:|----------:|--------------:|
| Reference | −0.0019 | −0.0021 | +0.0019 |
| Covariate mild | −0.0011 | +0.0021 | +0.0050 |
| Covariate severe | −0.0004 | +0.0373 | +0.0437 |
| MCAR-like 10% | +0.0011 | −0.0033 | −0.0006 |
| MAR-like 10% | −0.0019 | −0.0018 | +0.0007 |
| Combined mild | +0.0026 | +0.0057 | +0.0112 |
| Combined severe | −0.0007 | +0.0362 | +0.0505 |

*Table 2. Mean paired CORAL-minus-source-only AUROC differences across five stratified split seeds.*

| Model | Adaptation | Brier | ECE |
|-------|------------|------:|----:|
| Logistic regression | Source-only | 0.245 | 0.290 |
| Logistic regression | CORAL | 0.155 | 0.064 |
| Random forest | Source-only | 0.221 | 0.217 |
| Random forest | CORAL | 0.154 | 0.077 |
| Hist. grad. boosting | Source-only | 0.227 | 0.209 |
| Hist. grad. boosting | CORAL | 0.164 | 0.075 |

*Table 3. Calibration under combined severe controlled shift (mean across seeds).*

### 3.3 Explanation stability

Mean rank-biased overlap for random forest was 0.994 (noise SD 0.01), 0.974 (0.05) and 0.963 (0.10). For XGBoost: 0.971, 0.965 and 0.952. Stability declined with perturbation magnitude. Stability is not evidence of causal validity.

## 4. Discussion and limitations

CORAL’s effect is model- and scenario-dependent. Improvements under selected severe controlled covariate shifts did not generalise to reference or missingness-only conditions. Reporting discrimination alone would have obscured substantial calibration changes.

**Limitations:** (1) public historical benchmark only — not Nigerian multi-hospital data; (2) controlled synthetic shifts do not recreate institutional heterogeneity; (3) five split seeds are descriptive, not independent cohorts; (4) TreeSHAP stability is a sensitivity analysis, not clinical validation of explanations; (5) no prospective clinical evaluation.

## 5. Data and code availability

Analysis code, experiment manifests and provenance documentation: private repository `EkeminiThompson/clinassist-nigeria`. Public Pima data retrieved from OpenML with recorded checksum. No identifiable patient data are redistributed.

---
*Disclaimer: Methodological research only. Does not constitute clinical advice. No Nigerian hospital validation is claimed.*
