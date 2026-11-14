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

For each seed 42–46, `train_test_split` generated a stratified 75:25 partition (576 source-training and 192 held-out target rows). The split seed was the integer seed itself. Repeated random splits describe split-to-split variability; they are not independent external validations.

### 2.4 Classifiers and probability calibration

The shift study used (i) logistic regression with `max_iter=1500`, `class_weight="balanced"`; (ii) random forest with 250 trees, maximum depth 6, minimum leaf size 3, balanced class weights and all available CPU workers; and (iii) scikit-learn histogram gradient boosting with 150 iterations, learning rate 0.06, at most 15 leaf nodes and L2 regularisation 1.0. Estimator random states were set to the corresponding split seed. Each estimator was wrapped in sigmoid probability calibration using three-fold cross-validation on source-training data (`CalibratedClassifierCV`, `cv=3`). The preprocessor was fitted only on source-training features in each split. These settings describe the shift-study models, not the separate baseline comparison in Table 1.

The baseline experiment used scikit-learn's `GradientBoostingClassifier`, not `HistGradientBoostingClassifier`. Its five-fold out-of-fold comparison used logistic regression (`max_iter=1000`), random forest (200 trees, maximum depth 6), gradient boosting (150 estimators, maximum depth 3), XGBoost (150 estimators, depth 3, learning rate 0.1, row and column subsampling 0.8) and RBF SVM with probability estimates. The baseline split generator was shuffled stratified five-fold cross-validation with seed 42. These pooled out-of-fold baseline metrics must not be directly compared with the repeated-split, calibrated shift-study results. Exact settings are recorded in the executable experiment scripts.

### 2.5 Prespecified shift scenarios and parameters

The seven target-domain conditions comprise an unshifted reference condition, mild covariate shift, severe covariate shift, 10% missing-completely-at-random (MCAR), 10% glucose-dependent missing-at-random (MAR), combined mild shift, and combined severe shift. Covariate transformations are applied to raw held-out values before the zero-to-missing preprocessing step; consequently, some recorded zeros can become non-zero in shifted scenarios and will not subsequently be recoded as missing. This ordering is retained as a methodological limitation. Covariate-shift severity is 0.5 (mild) or 1.5 (severe). The combined mild condition applies severity 0.5 with 10% MCAR missingness; the combined severe condition applies severity 1.5 with 20% glucose-dependent MAR missingness. The single-mechanism missingness conditions use 10% missingness. The severe-combined result tables in this manuscript therefore refer to 20%, not 10%, missingness.

The executable protocol applies these transformations to raw held-out features before zero-to-missing conversion, imputation and scaling. For severity `s` (0.5 or 1.5), glucose is transformed as `G' = G(1 + 0.15s) + 5s`, BMI as `B' = B(1 + 0.10s) + 1.5s`, and age as `A' = A(1 + 0.05s) + 2s`; other features are not directly shifted. For each split seed `r` (42–46), scenario index `j` (zero-based, in the order listed above) uses missingness RNG seed `r + 1000j`. MCAR independently masks every feature cell with probability 0.10. The MAR-like mechanism standardises shifted glucose within the held-out set to `z`, computes row probability `q_i = clip(2m/(1 + exp(-z_i)), 0, 1)`, where `m` is the configured missing rate, and independently masks skin thickness and insulin for each row using `q_i`. The combined severe condition therefore uses `m = 0.20`. The reference condition has no transformation or missingness. The exact implementation is in `ml/experiments/run_shift_study.py`; these are controlled perturbations, not observed population shifts.

### 2.6 Domain adaptation

The source-only arm fits the model using source-training data. In the CORAL arm, the target feature matrix is used without target labels to align source and target means and covariance structure. This is transductive unsupervised adaptation: target covariates are available during adaptation, but target outcomes are reserved for evaluation.

For source matrix $X_s$ and target matrix $X_t$, let $\mu_s$ and $\mu_t$ denote feature means and let $C_s$ and $C_t$ denote regularised covariance matrices, with $C=\operatorname{Cov}(X)+\epsilon I$ and $\epsilon=10^{-5}$. The source-to-target transformation is:

$
X_{s\rightarrow t}=(X_s-\mu_s)C_s^{-1/2}C_t^{1/2}+\mu_t.
$

The implementation uses the row-vector mapping `(X_s - mean_s) @ C_s^(-1/2) @ C_t^(1/2) + mean_t`, where the inverse square root is applied first and the target covariance square root second. The covariance matrices are regularised with epsilon (10^{-5}). The adapter's `fit(source_X, target_X)` interface accepts feature matrices only; target labels are not used to estimate either alignment statistic.



### 2.7 Performance metrics

AUROC, AUPRC, Brier score, ten-bin ECE, calibration intercept and slope, selective metrics at 80% entropy-based coverage.

### 2.8 Explanation stability

TreeSHAP for random forest (250 trees, depth 6, minimum leaf size 3) and XGBoost (180 estimators, depth 3, learning rate 0.04, subsample and column subsample 0.8, L2 penalty 2) on up to 100 held-out examples from the seed-42 split. Standardised Gaussian noise was added at SD 0.01, 0.05 and 0.10 using a NumPy generator initialised with seed 42; feature rankings were compared with rank-biased overlap (persistence 0.9).

### 2.9 Exploratory subgroup audit

Age and BMI strata with eligibility ≥20 observations and ≥5 events per class. Paired bootstrap (1,000 draws) for source-only versus CORAL. Sparse strata suppressed.

### 2.10 Software environment

The author's reported local development workstation is a 13-inch MacBook Pro (Mid-2012; model identifier `MacBookPro9,2`) with an Intel Core i5 processor at 2.5 GHz, one physical processor package, two CPU cores and 8 GB RAM. The operating-system information returned by `sw_vers` was ProductName `Mac OS X`, ProductVersion `10.15.8`, BuildVersion `19H2026`. These specifications describe the author's workstation as reported; they are not evidence that every experiment or the final table-producing run was executed on this machine. The independent verification report records Python 3.12, scikit-learn 1.9.1 and XGBoost 3.4.1 for the clean verification run dated 2026-11-13. The separate research CI environment is described in Appendix A. Exact historical run-to-machine mapping and the remaining dependency versions for the original table-producing run were not retained.

### 2.11 Statistical analysis

The primary paired contrast was CORAL minus source-only within each identical split, model and shift scenario. For AUROC, Brier score and ECE, two-sided exact sign-flip permutation tests were applied to the five split-level paired differences for each of the 21 model-by-scenario contrasts (63 tests). The test enumerates all 32 sign assignments and uses the absolute mean paired difference as the test statistic. Holm adjustment was applied separately within each metric family of 21 comparisons. The analysis unit is the repeated split, not the patient. Because the five train/test partitions overlap, the split-level contrasts are dependent; the tests are therefore exploratory sensitivity analyses and do not support population-level or clinical inference. With only five pairs, the smallest attainable two-sided exact p-value is 0.0625. No contrast can reach the conventional 0.05 threshold, even before multiplicity adjustment. The complete results are in `ml/artifacts/experiments/paired_sign_flip_tests.csv`; the executable analysis is `ml/analysis/paired_sign_flip_tests.py`.

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

### 3.5 Exploratory paired sign-flip tests

Exact two-sided sign-flip tests were conducted on the five paired split-level CORAL-minus-source-only differences for AUROC, Brier score and ECE across all 21 model-by-scenario comparisons. The smallest unadjusted p-value was 0.0625, the minimum attainable with five pairs and 32 sign assignments. Holm-adjusted p-values were 1.000 across the reported metric families. No comparison met a two-sided 0.05 threshold. The large and directionally consistent Brier/ECE differences in some imposed-shift conditions should therefore be interpreted as descriptive effects in this small, repeated-split benchmark, not as statistically established improvements. The split overlap and low number of pairs further limit inferential strength. Full test statistics are archived in `ml/artifacts/experiments/paired_sign_flip_tests.csv`.

## 4. Discussion

CORAL’s benefit is model- and scenario-dependent. Under severe controlled covariate shift, tree ensembles gained discrimination and all models gained calibration; under reference and missingness-only conditions effects were negligible or adverse. Joint reporting of discrimination and calibration is essential.

The analysis uses a public historical benchmark and controlled synthetic shifts. Findings characterise adaptation behaviour under the specified perturbation grid and provide a methodological baseline for subsequent evaluation on authorised multi-site clinical cohorts under the same protocol.

## 5. Data and code availability

Analysis code, experiment manifests, raw run-level metrics, held-out prediction outputs, paired differences, exact sign-flip test results, provenance documentation and independent verification report are available in `EkeminiThompson/clinassist-nigeria`. The original benchmark is an existing public dataset retrieved as OpenML dataset 37 (version 1); it is not a newly introduced dataset and the source CSV is not redistributed in the repository. OpenML records the dataset access status as “Public”; this metadata is not an SPDX or Creative Commons licence grant. The original dataset attribution and use conditions must therefore be followed, and no new licence is asserted for the source dataset. The author-generated experiment summaries and analysis outputs are released under CC BY 4.0 to the extent of rights held by the author; source-dataset rights and conditions remain unaffected. See `DATA-LICENSE.md` and `docs/dataset_provenance.md`.




## Appendix A. Computing environment

The author's reported local workstation is a 13-inch MacBook Pro (Mid-2012; `MacBookPro9,2`): Intel Core i5 at 2.5 GHz, two CPU cores, 8 GB RAM, Mac OS X 10.15.8 (build 19H2026). This is a user-reported machine specification and is not, by itself, proof that the historical result-producing experiments were run on this workstation.

The repository's reproducibility workflow runs the research-benchmark job on a GitHub-hosted `ubuntu-24.04` x86-64 runner. For public repositories, GitHub documents the standard runner configuration as 4 vCPUs and 16 GB RAM. The workflow records the actual CPU model, logical CPU count, memory and operating-system release in the run log for each execution. The Python environment for this workflow is Python 3.11, as configured in `.github/workflows/ci.yml`.

**Important distinction:** the MacBook specifications describe the author's local workstation; the Ubuntu specifications describe the CI reproduction environment. Neither should be attributed to a historical run unless its execution log or contemporaneous environment record confirms that machine. The original table-producing run's exact hardware-to-run mapping was not retained.


## Appendix B. Complete seven-scenario paired comparison

The complete repeated-split outputs are committed under `ml/artifacts/experiments/`. The table below reports the mean (SD) across five paired split-level differences, calculated as CORAL minus source-only from the unrounded run-level metrics. Negative Brier and ECE differences indicate lower error; positive AUROC differences indicate improved discrimination. These are descriptive paired differences on the public Pima benchmark under controlled transformations, not external validation.

| Shift scenario | Model | ΔAUROC, mean (SD) | ΔBrier, mean (SD) | ΔECE, mean (SD) |
|---|---|---:|---:|---:|
| reference | Histogram gradient boosting | +0.0019 (0.0097) | −0.0005 (0.0040) | −0.0067 (0.0178) |
| reference | Logistic regression | −0.0019 (0.0060) | +0.0005 (0.0024) | +0.0081 (0.0102) |
| reference | Random forest | −0.0021 (0.0048) | +0.0009 (0.0020) | −0.0089 (0.0209) |
| covariate_mild | Histogram gradient boosting | +0.0050 (0.0110) | −0.0056 (0.0052) | −0.0071 (0.0304) |
| covariate_mild | Logistic regression | −0.0011 (0.0061) | −0.0084 (0.0023) | −0.0405 (0.0162) |
| covariate_mild | Random forest | +0.0021 (0.0110) | −0.0057 (0.0050) | −0.0177 (0.0166) |
| covariate_severe | Histogram gradient boosting | +0.0437 (0.0147) | −0.0585 (0.0052) | −0.1216 (0.0194) |
| covariate_severe | Logistic regression | −0.0004 (0.0071) | −0.0907 (0.0076) | −0.2232 (0.0214) |
| covariate_severe | Random forest | +0.0373 (0.0264) | −0.0619 (0.0079) | −0.1354 (0.0296) |
| mcar_10 | Histogram gradient boosting | −0.0006 (0.0097) | +0.0004 (0.0043) | −0.0022 (0.0352) |
| mcar_10 | Logistic regression | +0.0011 (0.0071) | −0.0010 (0.0030) | +0.0012 (0.0097) |
| mcar_10 | Random forest | −0.0033 (0.0036) | +0.0010 (0.0015) | +0.0049 (0.0208) |
| mar_like_10 | Histogram gradient boosting | +0.0007 (0.0081) | +0.0013 (0.0021) | −0.0076 (0.0301) |
| mar_like_10 | Logistic regression | −0.0019 (0.0066) | +0.0009 (0.0027) | +0.0045 (0.0093) |
| mar_like_10 | Random forest | −0.0018 (0.0037) | +0.0011 (0.0016) | −0.0013 (0.0176) |
| combined_mild | Histogram gradient boosting | +0.0112 (0.0202) | −0.0088 (0.0080) | −0.0029 (0.0181) |
| combined_mild | Logistic regression | +0.0026 (0.0077) | −0.0071 (0.0021) | −0.0308 (0.0106) |
| combined_mild | Random forest | +0.0057 (0.0100) | −0.0064 (0.0043) | −0.0179 (0.0128) |
| combined_severe | Histogram gradient boosting | +0.0505 (0.0174) | −0.0631 (0.0044) | −0.1341 (0.0083) |
| combined_severe | Logistic regression | −0.0007 (0.0085) | −0.0903 (0.0074) | −0.2257 (0.0265) |
| combined_severe | Random forest | +0.0362 (0.0281) | −0.0670 (0.0089) | −0.1407 (0.0134) |

The table contains all 21 model-by-scenario comparisons. The committed files retain all 210 split/model/scenario/adaptation metric rows, 1,050 paired metric differences and 40,320 held-out prediction rows. The rounded summary CSV contains 42 model-by-scenario-by-adaptation rows. The full JSON manifest preserves the run-level metric values.

## References

Smith, J. W., Everhart, J. E., Dickson, W. C., Knowler, W. C., & Johannes, R. S. (1988). Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. *Proceedings of the Symposium on Computer Applications and Medical Care*, 261–265.

Vanschoren, J., van Rijn, J. N., Bischl, B., & Torgo, L. (2013). OpenML: Networked science in machine learning. *SIGKDD Explorations*, 15(2), 49–60. https://doi.org/10.1145/2641190.2641198

Feurer, M., van Rijn, J. N., Kadra, A., Gijsbers, P., Mallik, N., Ravi, S., Müller, A., Vanschoren, J., & Hutter, F. (2021). OpenML-Python: An extensible Python API for OpenML. *Journal of Machine Learning Research*, 22(100), 1–5.
