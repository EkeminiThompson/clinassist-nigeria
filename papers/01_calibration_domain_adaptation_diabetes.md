# Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions

**Author:** Ekemini Thompson  
**Affiliation:** Nnamdi Azikiwe University, Awka, Nigeria  
**Manuscript status:** Working research manuscript (version 0.1; not submitted or peer reviewed)  
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

Transportability introduces a second challenge. Differences in population characteristics, measurement practices, clinical workflows and data completeness can alter the feature distribution encountered after model development. Domain adaptation methods attempt to reduce some of these differences by using information from a target domain. Correlation Alignment (CORAL) is an unsupervised approach that aligns second-order feature statistics between source and target domains without using target labels (Sun et al., 2016). However, adaptation is not guaranteed to improve every model or every performance dimension. It can also create a misleading impression of clinical transfer if target-domain information is not described precisely.

A related issue is missingness. Routine clinical datasets can contain incomplete measurements, and the missingness process may differ between settings. Evaluating models under only complete-case or randomly missing data may understate the effect of more structured missingness. Finally, explanation methods such as SHAP can produce feature-attribution rankings, but their stability under small input perturbations should not be assumed.

This study uses the Pima Indians Diabetes dataset as a controlled methodological benchmark. The work does not treat the dataset as Nigerian data. The repository's provenance audit found that a Mendeley deposit previously described as UITH and General Hospital Offa data reproduces the public Pima dataset and contains no hospital identifiers; the ESUTH research dataset remains inaccessible. Consequently, a genuine Nigerian multi-hospital domain-adaptation experiment cannot be performed with the currently accessible data.

The study has four objectives:

1. Compare discrimination and calibration of several tabular classifiers on a reproducible public benchmark.
2. Stress-test model performance under prespecified covariate and missingness transformations.
3. Compare source-only modelling with unsupervised CORAL adaptation using target covariates but no target labels during adaptation.
4. Characterise selective-prediction behaviour and the local stability of tree-model explanations under controlled perturbation.

The contribution is an auditable, repeated-split evaluation pipeline that jointly reports discrimination, calibration, uncertainty-based coverage, explanation stability and exploratory subgroup diagnostics. CORAL, SHAP and diabetes classification are established techniques; this paper does not claim to invent them. The contribution is their controlled, reproducible assessment in this specific small-sample benchmark design.

## 2. Methods

### 2.1 Study design and data source

This was a retrospective computational benchmark study using OpenML dataset ID 37 (dataset name: diabetes; version 1), originally sourced from the UCI Pima Indians Diabetes Database. The dataset contains 768 records, eight predictors and a binary outcome. The class distribution was 500 outcome-negative and 268 outcome-positive records. The predictor variables were pregnancies, glucose, blood pressure, skin thickness, insulin, body mass index (BMI), diabetes pedigree function and age.

The original dataset concerns adult women of Pima heritage. It is not a Nigerian cohort, does not contain Nigerian hospital identifiers and cannot support estimates of performance in Nigerian patients. The data were retrieved through the repository's `ml.datasets.download_pima` workflow. The successful benchmark run generated a provenance manifest recording OpenML ID 37, dataset version, retrieval timestamp, schema, class counts and SHA-256 checksum. The dataset CSV is intentionally not committed to the repository; it is retrieved at experiment runtime.

### 2.2 Preprocessing

Five predictors—glucose, blood pressure, skin thickness, insulin and BMI—were treated as missing when recorded as zero because zero is physiologically implausible for these measurements in this dataset context. Pregnancies and diabetes pedigree function were not included in this zero-to-missing transformation.

The preprocessing sequence comprised:
1. replacing zero values in the five specified fields with missing values;
2. median imputation; and
3. standardisation.

The preprocessing pipeline was fitted on the source-training partition and then applied to the held-out target/test partition. The target labels were not used to fit preprocessing or the CORAL transformation. The same source-fitted preprocessing was applied before the adaptation step.

### 2.3 Repeated source/target splits

The main controlled-shift experiment used five random seeds (42, 43, 44, 45 and 46). For each seed, the dataset was split using a stratified 75:25 train/test partition, giving 576 training records and 192 held-out records. The same split was used for all models, scenarios and adaptation arms within a seed, enabling paired comparisons. Repeated random splits are used to describe split-to-split variability; they are not independent cohorts or independent external validations.

### 2.4 Classifiers and probability calibration

Three classifiers were evaluated:

- **Logistic regression:** maximum 1,500 iterations and balanced class weights.
- **Random forest:** 250 trees, maximum depth 6, minimum leaf size 3 and balanced class weights.
- **Histogram gradient boosting:** 150 boosting iterations, learning rate 0.06, maximum 15 leaf nodes and L2 regularisation of 1.0.

Each classifier was wrapped in sigmoid probability calibration using three-fold cross-validation on the source-training data. Calibration was therefore learned without target labels. The prediction threshold for threshold-dependent classification metrics was 0.5 unless otherwise stated by the metric implementation.

### 2.5 Controlled target-domain scenarios

Seven scenarios were applied to the held-out feature matrix. The target labels remained unchanged and were used only after prediction for evaluation.

| Scenario | Covariate transformation | Missingness |
|---|---|---|
| Reference | None | None |
| Mild covariate shift | Severity 0.5 | None |
| Severe covariate shift | Severity 1.5 | None |
| MCAR-like 10% | None | Independent cell-wise masking at rate 0.10 |
| MAR-like 10% | None | Glucose-dependent masking of skin-thickness and insulin fields |
| Combined mild | Severity 0.5 | MCAR-like masking at 0.10 |
| Combined severe | Severity 1.5 | MAR-like masking at 0.20 |

For non-zero covariate severity (s), glucose was transformed as (G'=G(1+0.15s)+5s), BMI as (BMI'=BMI(1+0.10s)+1.5s), and age as (Age'=Age(1+0.05s)+2s). The MCAR-like scenario independently masked cells across the feature matrix. The MAR-like scenario made the probability of missing skin-thickness and insulin values depend on standardised glucose. These are controlled perturbations, not observed hospital effects or empirically estimated Nigerian missingness mechanisms.

### 2.6 Domain adaptation

The source-only arm fitted the calibrated classifier to the preprocessed source-training data. The CORAL arm first estimated a linear transformation from the source-training features and the unlabelled, perturbed target/test covariates. It aligned the source and target means and covariance structure, transformed the source-training features, and fitted the calibrated classifier to the transformed source data.

The target feature matrix was available to CORAL during adaptation, but target outcomes were not. This is a transductive unsupervised adaptation design: it assumes access to an unlabelled batch of target covariates at adaptation time. It does not represent a strictly inductive setting in which each future patient is predicted without access to other target observations.

### 2.7 Performance metrics

Discrimination was assessed using AUROC and AUPRC. Calibration was assessed using the Brier score, ten-bin expected calibration error (ECE), calibration-in-the-large intercept, and joint calibration intercept and slope. Lower Brier score and ECE indicate better probability agreement under their respective definitions; ideal calibration-in-the-large and joint intercept are zero, and ideal calibration slope is one.

Prediction uncertainty was quantified using binary predictive entropy. The selective-prediction analysis retained the 80% of observations with the lowest entropy (with the implementation retaining the ceiling of the requested fraction). Discrimination and calibration metrics were recomputed on this retained subset. The area under the risk–coverage curve (AURC) summarised error accumulation as coverage increased. This is a model-evaluation construct, not a clinically validated abstention policy.

### 2.8 Explanation stability

A separate experiment trained random forest and XGBoost models on one stratified 75:25 split (seed 42). TreeSHAP feature attributions were computed for up to 100 held-out examples using a source-training background sample of up to 100 observations. Standardised feature vectors were perturbed with independent Gaussian noise at standard deviations 0.01, 0.05 and 0.10. Feature rankings from perturbed and unperturbed inputs were compared using rank-biased overlap (RBO; persistence parameter 0.9). This experiment measures local ranking stability to the specified input perturbations; it is not a test of causal explanation, clinical validity or explanation stability across hospitals.

### 2.9 Exploratory subgroup audit

An exploratory audit described performance across age bands (<30, 30–49 and 50+) and BMI bands (<18.5, 18.5–24.9, 25–29.9 and ≥30). BMI values recorded as zero were excluded from BMI strata. A stratum was eligible for AUROC, AUPRC and Brier calculations only when it contained at least 20 observations and at least five observations from each outcome class.

For each seed/model/scenario/stratum, source-only and CORAL predictions were paired by original dataset row. The bootstrap resampled patient rows with replacement and preserved the paired arms within each draw. One thousand bootstrap draws were requested; a comparison was accepted only when at least 90% were valid. Sparse strata were explicitly suppressed rather than assigned unstable performance estimates. These analyses are exploratory and do not establish fairness or subgroup validity in a Nigerian population.

### 2.10 Reproducibility and reporting

The experiment scripts, preprocessing, model definitions, metrics and data-retrieval workflow are version-controlled. The CI workflow retrieved the benchmark, executed the repeated-shift experiment, explanation-stability experiment and subgroup audit, checked output schemas and validity conditions, and uploaded the resulting artifact. The manuscript is informed by the archived CI artifact generated on 8 November 2026. Reporting is structured with reference to TRIPOD+AI recommendations for transparent reporting of prediction-model studies (Collins et al., 2024).

## 3. Results

### 3.1 Dataset and baseline benchmark

The retrieved dataset contained 768 records: 500 outcome-negative and 268 outcome-positive. The primary repeated-shift experiment generated 5 seeds × 7 scenarios × 3 classifiers × 2 adaptation arms = 210 model/scenario/arm evaluations. Each evaluation used 576 source-training and 192 held-out records.

A separate five-fold baseline benchmark artifact reported the following overall results. These values are presented as a separate baseline analysis and should not be conflated with the repeated 75:25 shift experiment.

| Classifier | AUROC | AUPRC | Brier | ECE |
|---|---:|---:|---:|---:|
| Logistic regression | 0.8349 | 0.7067 | 0.1571 | 0.0360 |
| Random forest | 0.8342 | 0.6977 | 0.1574 | 0.0398 |
| Gradient boosting | 0.8265 | 0.6927 | 0.1676 | 0.0839 |
| XGBoost | 0.8247 | 0.6920 | 0.1643 | 0.0642 |
| RBF support vector machine | 0.8211 | 0.6967 | 0.1642 | 0.0548 |

Logistic regression had the highest AUROC and AUPRC and the lowest Brier score and ECE in this baseline artifact. These are benchmark estimates only.

### 3.2 Severe combined shift: source-only versus CORAL

Table 2 reports the archived mean and standard deviation across the five random splits for the severe combined scenario (severity 1.5 plus 20% glucose-dependent MAR-like missingness). CORAL was associated with lower Brier score and ECE for all three classifiers. Discrimination gains were observed for random forest and histogram gradient boosting, whereas logistic-regression AUROC was essentially unchanged.

| Model | Adaptation | AUROC, mean (SD) | AUPRC, mean (SD) | Brier, mean (SD) | ECE, mean (SD) |
|---|---|---:|---:|---:|---:|
| Logistic regression | Source-only | 0.8391 (0.0255) | 0.7273 (0.0537) | 0.2450 (0.0157) | 0.2900 (0.0138) |
| Logistic regression | CORAL | 0.8384 (0.0239) | 0.7206 (0.0485) | 0.1547 (0.0128) | 0.0643 (0.0175) |
| Random forest | Source-only | 0.8069 (0.0313) | 0.6433 (0.0435) | 0.2210 (0.0099) | 0.2172 (0.0107) |
| Random forest | CORAL | 0.8431 (0.0235) | 0.7258 (0.0477) | 0.1540 (0.0103) | 0.0765 (0.0072) |
| Histogram gradient boosting | Source-only | 0.7718 (0.0170) | 0.6142 (0.0405) | 0.2269 (0.0081) | 0.2094 (0.0121) |
| Histogram gradient boosting | CORAL | 0.8223 (0.0192) | 0.6950 (0.0530) | 0.1638 (0.0081) | 0.0754 (0.0139) |

The pattern indicates that calibration and probability error may respond differently from ranking discrimination under the imposed transformations. It also shows that adaptation effects depend on classifier choice. These descriptive repeated-split summaries do not establish statistical significance or expected benefit in an external clinical population.

### 3.3 Explanation stability

The separate local TreeSHAP stability experiment evaluated 100 held-out examples per model. Mean RBO values were:

| Model | Noise SD 0.01 | Noise SD 0.05 | Noise SD 0.10 |
|---|---:|---:|---:|
| Random forest | 0.9944 | 0.9743 | 0.9630 |
| XGBoost | 0.9711 | 0.9652 | 0.9522 |

Feature-ranking agreement declined as perturbation magnitude increased for both models. Random forest showed higher mean agreement than XGBoost at each tested noise level in this single-split experiment. The result is conditional on the chosen sample, preprocessing, background data, perturbation distribution and ranking metric.

### 3.4 Subgroup audit and paired bootstrap

The audit produced 1,638 subgroup metric rows and 819 paired-bootstrap comparisons. Of the comparisons, 609 met the prespecified minimum subgroup size/class counts and bootstrap validity criterion; 210 were labelled “insufficient subgroup events” and had their paired intervals suppressed. Among the successful comparisons, the archived audit reported 595 with 1,000 valid draws, 12 with 999 and two with 998. The workflow verified that source-only and CORAL arms shared identical held-out row identifiers and labels.

The present manuscript does not make claims about which age or BMI subgroup benefited most because the detailed stratum-level estimates and intervals have not been independently re-analysed for the manuscript. Suppression of sparse strata is an intentional safeguard against overinterpretation.

### 3.5 Selective prediction

The repeated-shift artifact includes entropy-based selective metrics at approximately 80% coverage and risk–coverage summaries. The selective results are reported as secondary model diagnostics, not as evidence that abstention improves clinical outcomes. No clinician-defined referral threshold or prospective workflow evaluation was performed.

## 4. Discussion

This study evaluated how discrimination, calibration, uncertainty-based coverage and local explanation rankings behaved under controlled transformations of a small public diabetes benchmark. The principal finding in the severe combined scenario was that CORAL was associated with lower Brier score and ECE across all three evaluated classifiers, while AUROC changes varied by model. This reinforces the practical point that discrimination and calibration should be reported together rather than treated as interchangeable indicators of model reliability.

The classifier-specific pattern is important. Logistic-regression AUROC changed little in the severe combined scenario, despite a large difference in Brier score and ECE between adaptation arms. Random forest and histogram gradient boosting showed both improved discrimination and improved probability-error metrics in the same scenario. These observations are consistent with CORAL changing the feature geometry presented to each classifier, with consequences that depend on the classifier's decision function. They do not imply that CORAL will improve calibration in every dataset or shift.

The experiment deliberately separates target covariate access from target label access. CORAL used the unlabelled target/test feature matrix to estimate its alignment transformation; target labels were held back until evaluation. This is a legitimate unsupervised adaptation setting, but it is transductive. In a real deployment, the availability, representativeness and governance of an unlabelled target batch would need to be established. A single patient's covariates would not necessarily provide a reliable estimate of the target distribution.

The missingness scenarios also require careful interpretation. MCAR-like masking was imposed independently across cells, while the MAR-like process made missingness in skin-thickness and insulin fields depend on glucose. These are transparent stress tests, not empirically observed mechanisms. They omit more complex processes such as missing-not-at-random measurement driven by unobserved values, clinician ordering behaviour or site-specific workflow. They also do not reproduce the full range of measurement shifts that occur between hospitals.

The explanation experiment found high average local feature-ranking agreement under modest standardised perturbations, with a gradual decline as perturbation magnitude increased. This should be interpreted narrowly. Stable rankings under small Gaussian perturbations do not show that SHAP values are causal, clinically meaningful or stable across populations. Attribution stability is one property of an explanation pipeline, not a substitute for clinician assessment or external validation.

The subgroup audit demonstrates the value of predefining minimum sample and event thresholds. Rather than reporting unstable estimates for sparse strata, the pipeline suppressed 210 comparisons. Even for eligible strata, the Pima benchmark's limited sample size and narrow source population make the estimates exploratory. They should not be described as evidence of fairness in Nigerian populations.

### 4.1 Relationship to prior work

CORAL and its extensions are established unsupervised domain-adaptation methods (Sun et al., 2016). The present study does not claim methodological novelty for covariance alignment itself. Recent diabetes prediction work has also evaluated calibration, leakage control, subgroup stability and decision-aware modelling on Pima and larger public datasets. For example, Ismael and Rasul (2026) reported a leakage-controlled risk-aware framework on Pima and CDC Diabetes Health Indicators data. Other recent work has examined few-shot transfer between Bangladesh, Iraq and Pima cohorts. The distinction sought here is a focused repeated-split stress-test of source-only versus unlabelled-covariate CORAL across explicitly specified covariate and missingness perturbations, accompanied by entropy-based selective diagnostics, local explanation stability and a paired subgroup audit.

The distinction is not sufficient to claim a definitive new domain-adaptation algorithm. The manuscript should be positioned as a reproducible benchmark/evaluation study. A stronger journal submission would benefit from additional independent datasets, more extensive comparisons with alternative adaptation methods, uncertainty intervals for repeated-split summaries, and a complete reporting checklist.

### 4.2 Implications for Nigerian clinical AI research

The project began with an interest in clinical decision support for resource-constrained Nigerian hospitals. The data provenance audit changed what can be claimed. A dataset described as originating from UITH and General Hospital Offa was found to reproduce the public Pima records without hospital identifiers. The ESUTH research dataset was not accessible. The current results therefore cannot be represented as Nigerian hospital findings.

The value of this work for Nigerian clinical research is methodological preparation: transparent provenance, leakage-conscious preprocessing, calibrated probabilities, unsupervised adaptation, missingness stress tests, explicit suppression of sparse subgroup estimates and reproducible CI execution. When authorised Nigerian cohorts become available, the same pipeline can be evaluated with actual site identifiers and clinically appropriate governance. That future work will require independent external validation rather than a relabelling of the present benchmark.

### 4.3 Strengths

Strengths include a reproducible benchmark retrieval workflow with a checksum manifest; training-only preprocessing; explicit separation of target covariates and target labels; paired source-only/CORAL evaluations using common held-out rows; five repeated splits; multiple complementary performance dimensions; and explicit suppression of sparse subgroup estimates. The research code and CI workflow preserve the experiment definitions and generated artifacts.

### 4.4 Limitations

Several limitations constrain interpretation:

1. **Population and sample size:** the Pima dataset contains 768 historical records from adult women of Pima heritage. It is not representative of Nigeria or of all people with diabetes risk.
2. **No external validation:** the target domains were generated by controlled transformations of held-out benchmark covariates. They are not independent hospitals, geographic populations or real-world time periods.
3. **Transductive adaptation:** CORAL uses the unlabelled target/test feature matrix. Performance may differ when target covariates arrive sequentially or in smaller batches.
4. **Limited model and adaptation comparison:** the main experiment compares three classifiers and one CORAL implementation with source-only training. It does not exhaust alternative adaptation or recalibration methods.
5. **Repeated-split uncertainty:** means and standard deviations across five overlapping random splits describe split variability, not independent patient-level confidence intervals. The manuscript does not infer statistical significance from these summaries.
6. **Missingness realism:** MCAR-like and glucose-dependent MAR-like mechanisms are controlled perturbations and do not cover all clinical missingness processes.
7. **Subgroup power:** several strata were too sparse for reliable estimates and were suppressed. The remaining subgroup analyses are exploratory.
8. **Explanation scope:** TreeSHAP stability was tested in one split under Gaussian feature perturbations and does not establish causal or clinical explanation validity.
9. **Clinical utility:** no decision-curve analysis, prospective workflow study, clinician evaluation or patient-outcome study is reported here. The software prototype is not a clinically validated medical device.

## 5. Conclusion

On the Pima benchmark under a severe combined, artificially imposed covariate-and-missingness shift, CORAL was associated with lower Brier score and ECE for logistic regression, random forest and histogram gradient boosting. Discrimination gains varied by classifier. Local TreeSHAP rankings were relatively stable under the tested perturbations but became less concordant as perturbation magnitude increased. The subgroup audit suppressed sparse comparisons rather than reporting unreliable estimates.

These results support multidimensional stress-testing of clinical prediction models, including calibration and uncertainty, rather than relying on AUROC alone. They do not establish clinical effectiveness, fairness, Nigerian external validity or readiness for patient care. The next scientifically necessary step is independent validation using appropriately authorised, genuinely Nigerian clinical data with site provenance, followed by prospective clinical evaluation.

## Declarations

- **Ethics approval:** This analysis used a previously released public benchmark and involved no new recruitment or intervention. The author should obtain and report the relevant institutional determination on whether formal ethics review is required before journal submission; no exemption is asserted here.
- **Consent to participate:** No new participants were recruited. Dataset-level consent and governance are as described by the original data custodians.
- **Data availability:** OpenML dataset 37 is available at https://www.openml.org/d/37. The dataset is downloaded at runtime; the repository records a retrieval manifest and checksum. No patient-level Nigerian dataset is included.
- **Code availability:** ClinAssist research code and experiment definitions are maintained at https://github.com/EkeminiThompson/clinassist-nigeria. The repository is currently private; access and public release should be confirmed before journal submission.
- **Funding:** To be completed by the author.
- **Competing interests:** To be completed by the author.
- **Author contributions:** Ekemini Thompson: conceptualisation, methodology, software, formal analysis, investigation and manuscript drafting. Confirm and amend before submission.
- **Acknowledgements:** To be completed by the author. Do not add a supervisor or collaborator as an author without their substantive contribution and approval.

## References

1. Smith JW, Everhart JE, Dickson WC, Knowler WC, Johannes RS. Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. In: *Proceedings of the Symposium on Computer Applications and Medical Care*. 1988;261–265.
2. Sun B, Feng J, Saenko K. Correlation Alignment for Unsupervised Domain Adaptation. In: *Domain Adaptation in Computer Vision Applications*. 2017. arXiv:1612.01939. https://arxiv.org/abs/1612.01939.
3. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378.
4. Ismael DA, Rasul A. A leakage-free and risk-aware machine learning framework for reliable diabetes prediction. *AIMS Bioengineering*. 2026;13(4):483–503. https://doi.org/10.3934/bioeng.2026023.
5. OpenML. Diabetes dataset, data ID 37, version 1. https://www.openml.org/d/37.
6. Sigillito V. Pima Indians Diabetes Database. UCI Machine Learning Repository. Original source attributed to the National Institute of Diabetes and Digestive and Kidney Diseases.

---

## Submission-readiness checklist

- [ ] Independently rerun all experiments from a clean environment and compare outputs with the archived CI artifact.
- [ ] Recalculate and independently verify all tables, particularly the severe-combined-shift table and subgroup bootstrap summaries.
- [ ] Add full results for all seven scenarios and all three classifiers to supplementary material.
- [ ] Add uncertainty intervals for repeated-split summary estimates using a method justified for repeated, overlapping splits.
- [ ] Complete a TRIPOD+AI checklist and review risk of bias and applicability.
- [ ] Verify all references and add the full citation required by the OpenML/UCI dataset.
- [ ] Confirm author affiliation, contributions, funding, competing interests and ethics determination.
- [ ] Decide whether to make the repository public and archive a tagged release.
- [ ] Obtain supervisory and institutional review before submission.
- [ ] Select a journal only after the additional validation and reporting checks are complete.

**Do not describe this manuscript as published or submitted until an actual journal submission has been made and acknowledged.**
