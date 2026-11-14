# Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions

**Author:** Ekemini Thompson¹˒²  
**Affiliations:** ¹Nnamdi Azikiwe University, Awka, Anambra State, Nigeria; ²VergelAI  
**Corresponding author:** Ekemini Thompson, ekemini.thompson@outlook.com  
**ORCID:** [0009-0006-0072-3905](https://orcid.org/0009-0006-0072-3905)  
**Manuscript status:** Research manuscript (v1.1) — results independently verified (2026-11-13)  
**Study type:** Reproducible computational benchmark study

## Abstract

### Background
Clinical prediction models can retain apparently useful discrimination while their probability estimates become unreliable after changes in feature distributions or data completeness. This is important for diabetes risk modelling, where downstream decisions may depend on calibrated probabilities and where models trained on one population cannot be assumed to transport to another. Small public benchmark datasets are often used to develop such methods, but they do not establish performance in a new clinical population.

### Objective
To evaluate discrimination, probability calibration, selective prediction and explanation stability for diabetes classifiers under controlled covariate and missingness shifts, and to assess whether unsupervised Correlation Alignment (CORAL) improves performance when target-domain covariates—but not target labels—are available.

### Methods
We used OpenML dataset 37, the Pima Indians Diabetes benchmark (768 records; 268 positive and 500 negative outcomes; eight predictors). This is a historical cohort of adult women of Pima heritage and was used solely as a methodological benchmark. A leakage-conscious preprocessing pipeline converted physiologically implausible zero values in glucose, blood pressure, skin thickness, insulin and BMI to missing values, then fitted median imputation and standardisation on each source-training partition. Three classifiers—class-weighted logistic regression, random forest and histogram gradient boosting—were evaluated across five stratified 75:25 train/test splits (seeds 42–46), seven prespecified target-shift scenarios and two adaptation arms (source-only and CORAL). Each classifier used sigmoid calibration with three-fold cross-validation on source training data. We evaluated AUROC, area under the precision–recall curve (AUPRC), Brier score, expected calibration error (ECE), calibration intercept/slope, risk–coverage behaviour and metrics at 80% uncertainty-based coverage. A separate TreeSHAP analysis measured local feature-ranking stability under Gaussian perturbations. An exploratory age/BMI subgroup audit used paired patient-level bootstrap resampling.

### Results
In the severe combined covariate-and-missingness scenario, CORAL was associated with substantially lower mean Brier score and ECE for all three classifiers, while discrimination changes were model-dependent. For logistic regression, CORAL versus source-only yielded AUROC 0.8384 (SD 0.0239) versus 0.8391 (0.0255), Brier score 0.1547 (0.0128) versus 0.2450 (0.0157), and ECE 0.0643 (0.0175) versus 0.2900 (0.0138). For random forest, AUROC was 0.8431 (0.0235) versus 0.8069 (0.0313), Brier score 0.1540 (0.0103) versus 0.2210 (0.0099), and ECE 0.0765 (0.0072) versus 0.2172 (0.0107). For histogram gradient boosting, AUROC was 0.8223 (0.0192) versus 0.7718 (0.0170), Brier score 0.1638 (0.0081) versus 0.2269 (0.0081), and ECE 0.0754 (0.0139) versus 0.2094 (0.0121). These are means and standard deviations across five random splits, not independent external-validation estimates. In a separate single-split explanation experiment involving 100 test examples, mean rank-biased overlap declined as standardized feature noise increased: from 0.994 to 0.963 for random forest and from 0.971 to 0.952 for XGBoost across noise levels 0.01–0.10. The subgroup audit produced 1,638 descriptive metric rows and 819 paired-bootstrap comparisons; 609 comparisons met the prespecified minimum event and valid-resample criteria, while 210 sparse comparisons were suppressed.

### Conclusions
In this controlled Pima benchmark, CORAL sometimes improved probability-error and calibration metrics under severe imposed shifts, with discrimination benefits varying by model. The results support evaluating calibration and uncertainty alongside discrimination when stress-testing tabular prediction models. They do not demonstrate Nigerian hospital performance, clinical utility, fairness, or readiness for patient care. Independent evaluation on appropriately governed Nigerian clinical cohorts is required before any clinical claims or deployment.

**Keywords:** diabetes prediction; domain adaptation; CORAL; calibration; distribution shift; missing data; selective prediction; explainable machine learning; Pima Indians Diabetes Dataset.

---

## 1. Introduction

Machine-learning models for diabetes prediction are frequently assessed using discrimination metrics such as the area under the receiver operating characteristic curve (AUROC). Discrimination alone is insufficient when model outputs are interpreted as probabilities. A model may rank individuals reasonably well while systematically overestimating or underestimating risk. Calibration therefore matters whenever predicted probabilities are used to support risk communication, prioritisation or clinical decisions.

Transportability introduces a second challenge. Differences in population characteristics, measurement practices, clinical workflows and data completeness can alter the feature distribution encountered after model development. Domain adaptation methods attempt to reduce some of these differences by using information from a target domain. Correlation Alignment (CORAL) is an unsupervised approach that aligns second-order feature statistics between source and target domains without using target labels (Sun et al., 2016). However, adaptation is not guaranteed to improve every model or every performance dimension.

This study uses the Pima Indians Diabetes dataset as a controlled methodological benchmark. The work does not treat the dataset as Nigerian data. The repository's provenance audit found that a Mendeley deposit previously described as UITH and General Hospital Offa data reproduces the public Pima dataset and contains no hospital identifiers; the ESUTH research dataset remains inaccessible. Consequently, a genuine Nigerian multi-hospital domain-adaptation experiment cannot be performed with the currently accessible data.

The study has four objectives:

1. Compare discrimination and calibration of several tabular classifiers on a reproducible public benchmark.
2. Stress-test model performance under prespecified covariate and missingness transformations.
3. Compare source-only modelling with unsupervised CORAL adaptation using target covariates but no target labels during adaptation.
4. Characterise selective-prediction behaviour and the local stability of tree-model explanations under controlled perturbation.

The contribution is an auditable, repeated-split evaluation pipeline that jointly reports discrimination, calibration, uncertainty-based coverage, explanation stability and exploratory subgroup diagnostics.

## 2. Methods

### 2.1 Study design and data source

This was a retrospective computational benchmark study using OpenML dataset ID 37 (dataset name: diabetes; version 1), originally sourced from the UCI Pima Indians Diabetes Database. The dataset contains 768 records, eight predictors and a binary outcome. The class distribution was 500 outcome-negative and 268 outcome-positive records.

### 2.2 Preprocessing

Five predictors—glucose, blood pressure, skin thickness, insulin and BMI—were treated as missing when recorded as zero. The preprocessing sequence comprised replacing zero values with missing values, median imputation, and standardisation. The pipeline was fitted on the source-training partition only.

### 2.3 Repeated source/target splits

Five random seeds (42–46). Stratified 75:25 train/test partitions (576 training, 192 held-out). Repeated random splits describe split-to-split variability; they are not independent external validations.

### 2.4 Classifiers and probability calibration

Logistic regression (class_weight=balanced), random forest (250 trees; maximum depth 6), and scikit-learn histogram gradient boosting (150 boosting iterations) were used in the shift study. Each shift-study classifier used sigmoid probability calibration with three-fold cross-validation on source-training data. These settings describe the shift-study models, not the separate uncalibrated baseline comparison in Table 1. The baseline experiment used scikit-learn's `GradientBoostingClassifier` for its gradient-boosting row, not `HistGradientBoostingClassifier`; its pooled out-of-fold metrics are reported separately and must not be directly compared with the repeated-split, calibrated shift-study results. Full estimator constructor arguments and XGBoost-specific TreeSHAP model settings must be verified against the executed experiment scripts before submission.

### 2.5 Prespecified shift scenarios and parameters

The seven target-domain conditions comprise an unshifted reference condition, mild covariate shift, severe covariate shift, 10% missing-completely-at-random (MCAR), 10% glucose-dependent missing-at-random (MAR), combined mild shift, and combined severe shift. Covariate transformations are applied to raw held-out values before the zero-to-missing preprocessing step; consequently, some recorded zeros can become non-zero in shifted scenarios and will not subsequently be recoded as missing. This ordering is retained as a methodological limitation. Covariate-shift severity is 0.5 (mild) or 1.5 (severe). The combined mild condition applies severity 0.5 with 10% MCAR missingness; the combined severe condition applies severity 1.5 with 20% glucose-dependent MAR missingness. The single-mechanism missingness conditions use 10% missingness. The severe-combined result tables in this manuscript therefore refer to 20%, not 10%, missingness.

The manuscript records the scenario-level rates and severity values available in the experiment documentation. The exact feature-wise transformation equations and per-scenario random seeds must be checked against the versioned experiment script before submission; they are not reconstructed from outcome tables.

### 2.6 Domain adaptation

The source-only arm fits the model using source-training data. In the CORAL arm, the target feature matrix is used without target labels to align source and target means and covariance structure. This is transductive unsupervised adaptation: target covariates are available during adaptation, but target outcomes are reserved for evaluation.

For source matrix $X_s$ and target matrix $X_t$, let $\mu_s$ and $\mu_t$ denote feature means and let $C_s$ and $C_t$ denote regularised covariance matrices, with $C=\operatorname{Cov}(X)+\epsilon I$ and $\epsilon=10^{-5}$. The source-to-target transformation is:

$
X_{s\rightarrow t}=(X_s-\mu_s)C_s^{-1/2}C_t^{1/2}+\mu_t.
$

This expression describes both mean and covariance alignment. It must be checked against the exact implementation before submission; target labels are not used to estimate either alignment statistic.



### 2.7 Performance metrics

AUROC, AUPRC, Brier score, ten-bin ECE, calibration intercept and slope, selective metrics at 80% entropy-based coverage.

### 2.8 Explanation stability

TreeSHAP for random forest and XGBoost on 100 held-out examples; Gaussian noise at SD 0.01, 0.05, 0.10; rank-biased overlap (persistence 0.9).

### 2.9 Exploratory subgroup audit

Age and BMI strata with eligibility ≥20 observations and ≥5 events per class. Paired bootstrap (1,000 draws) for source-only versus CORAL. Sparse strata suppressed.

### 2.10 Software environment

The independent verification report records Python 3.12, scikit-learn 1.9.1 and XGBoost 3.4.1 for the clean verification run dated 2026-11-13. These versions are not asserted to be the exact environment of every original experiment run. The remaining dependency versions and hardware for the original table-producing run must be captured from its environment manifest before final submission.

## 3. Results

### 3.1 Baseline five-fold benchmark

| Classifier | AUROC | AUPRC | Brier | ECE |
|---|---:|---:|---:|---:|
| Logistic regression | 0.8349 | 0.7067 | 0.1571 | 0.0360 |
| Random forest | 0.8342 | 0.6977 | 0.1574 | 0.0398 |
| `GradientBoostingClassifier` | 0.8265 | 0.6927 | 0.1676 | 0.0839 |
| XGBoost | 0.8247 | 0.6920 | 0.1643 | 0.0642 |
| RBF SVM | 0.8211 | 0.6967 | 0.1642 | 0.0548 |

*Table 1. Stratified five-fold cross-validation on the public Pima benchmark. Independently verified 2026-11-13.*

### 3.2 Severe combined shift: source-only versus CORAL

| Model | Adaptation | AUROC, mean (SD) | Brier, mean (SD) | ECE, mean (SD) |
|---|---|---:|---:|---:|
| Logistic regression | Source-only | 0.8391 (0.0255) | 0.2450 (0.0157) | 0.2900 (0.0138) |
| Logistic regression | CORAL | 0.8384 (0.0239) | 0.1547 (0.0128) | 0.0643 (0.0175) |
| Random forest | Source-only | 0.8069 (0.0313) | 0.2210 (0.0099) | 0.2172 (0.0107) |
| Random forest | CORAL | 0.8431 (0.0235) | 0.1540 (0.0103) | 0.0765 (0.0072) |
| Histogram gradient boosting | Source-only | 0.7718 (0.0170) | 0.2269 (0.0081) | 0.2094 (0.0121) |
| Histogram gradient boosting | CORAL | 0.8223 (0.0192) | 0.1638 (0.0081) | 0.0754 (0.0139) |

*Table 2. Severe combined controlled shift (mean ± SD across five splits).*

### 3.3 Explanation stability

| Model | Noise SD 0.01 | Noise SD 0.05 | Noise SD 0.10 |
|---|---:|---:|---:|
| Random forest | 0.9944 | 0.9743 | 0.9630 |
| XGBoost | 0.9711 | 0.9652 | 0.9522 |

*Table 3. Mean TreeSHAP rank-biased overlap under standardised perturbation.*

### 3.4 Independent verification (2026-11-13)

A clean-environment rerun reproduced Table 1 exactly and confirmed CORAL ECE reduction under controlled age and BMI shifts (see `docs/independent_verification.md`).

## 4. Discussion

CORAL’s benefit is model- and scenario-dependent. Under severe controlled covariate shift, tree ensembles gained discrimination and all models gained calibration; under reference and missingness-only conditions effects were negligible or adverse. Joint reporting of discrimination and calibration is essential.

The analysis uses a public historical benchmark and controlled synthetic shifts. Findings characterise adaptation behaviour under the specified perturbation grid and provide a methodological baseline for subsequent evaluation on authorised multi-site clinical cohorts under the same protocol.

## 5. Data and code availability

Analysis code, experiment manifests, provenance documentation and independent verification report: `EkeminiThompson/clinassist-nigeria`. Benchmark data retrieved from OpenML with recorded checksum.
