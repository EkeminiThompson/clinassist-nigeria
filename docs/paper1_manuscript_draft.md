# Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions

**Manuscript status:** Working draft for supervisor review; not submission-ready.  
**Study type:** Secondary analysis of a public historical benchmark with controlled distribution-shift experiments.  
**Proposed institutional affiliation:** Nnamdi Azikiwe University, Awka, Nigeria.  
**Academic supervisor:** Prof. V. E. Ejiofor (supervisory role to be confirmed in the manuscript metadata; authorship requires agreement on substantive contributions).  
**Corresponding author details, final author order and CRediT contributions:** To be confirmed by the research team.

## Abstract

### Background
Clinical prediction models can lose discrimination and calibration when the distribution of predictors changes between model development and evaluation. Unsupervised domain adaptation is one proposed response, but its benefits may depend on the model and the type and severity of distribution shift. Reporting discrimination alone may conceal substantial changes in probability calibration.

### Objective
To compare baseline diabetes-classification models and evaluate how CORrelation ALignment (CORAL) affects discrimination, calibration and selective prediction under controlled covariate-shift and missingness scenarios, while examining the local stability of tree-based SHAP explanations.

### Methods
We used the public OpenML Pima Indians Diabetes dataset (data ID 37; 768 records; eight predictors; 500 negative and 268 positive labels) as a methodological benchmark. The cohort is historical and comprises adult women of Pima heritage; it is not a Nigerian clinical cohort. Five-fold benchmark evaluation compared logistic regression, random forest, gradient boosting, XGBoost and radial-basis-function support vector machines. A repeated controlled-shift experiment compared source-only training with CORAL for logistic regression, random forest and histogram gradient boosting across seven scenarios and five stratified 75:25 splits (seeds 42–46). CORAL used target covariates but not target labels. Outcomes included AUROC, area under the precision-recall curve (AUPRC), Brier score, expected calibration error (ECE), calibration intercept and slope, and selective-prediction metrics. TreeSHAP rank stability was evaluated on 100 cases at three standardized perturbation magnitudes.

### Results
In the five-fold benchmark, logistic regression achieved AUROC 0.835, AUPRC 0.707, Brier score 0.157 and ECE 0.036. No complex model showed a clear discrimination advantage. Under severe controlled covariate shift, CORAL improved mean AUROC for random forest by 0.037 and histogram gradient boosting by 0.044, while logistic-regression AUROC was essentially unchanged. Under combined severe covariate shift and MAR-like missingness, AUROC changes were +0.036, +0.051 and -0.001, respectively. CORAL substantially reduced Brier score and ECE in these severe scenarios, but produced small, inconsistent or adverse changes in reference and missingness-only scenarios. TreeSHAP rank-biased overlap ranged from 0.952 to 0.994 across tested perturbations. The subgroup and paired-bootstrap audit was cancelled in the latest completed workflow; subgroup estimates and confidence intervals are therefore not available.

### Conclusion
In this historical benchmark, CORAL's effect was model- and scenario-dependent. Improvements under selected severe controlled covariate shifts did not generalise to reference or missingness-only conditions. These findings are methodological and exploratory; they do not establish Nigerian clinical validity, fairness, clinical utility or generalisability. The subgroup audit, final calibration visualisations and independent review remain necessary before submission.

**Keywords:** diabetes classification; calibration; domain adaptation; CORAL; distribution shift; missing data; selective prediction; SHAP; Pima Indians Diabetes.

---

## 1. Introduction

Machine-learning models for diabetes classification are often evaluated on a single dataset or through internal resampling. Such evaluations do not establish that a model will retain its performance when predictor distributions, clinical measurement practices or patient populations change. In clinical settings, changes in case mix, measurement systems and missing-data processes can affect both discrimination and the reliability of predicted probabilities. A model may preserve ranking performance while becoming poorly calibrated, or it may improve one metric while deteriorating on another.

Domain adaptation attempts to reduce differences between source and target distributions. CORrelation ALignment (CORAL) is an unsupervised approach that aligns second-order feature statistics without requiring target labels [1,2]. Its computational simplicity makes it attractive for tabular settings, but adaptation is not guaranteed to improve downstream performance. In particular, aligning covariate distributions may be ineffective when the target shift is not primarily a covariance shift, and can produce negative transfer when the adaptation transformation is poorly matched to the task.

A further concern is calibration. A model's probability estimates are relevant to threshold selection and risk communication; discrimination metrics alone do not show whether predicted probabilities agree with observed outcome frequencies. Brier score, calibration-in-the-large, calibration slope and calibration plots provide complementary views of probability performance. Expected calibration error (ECE) is also reported here, with the limitation that its value depends on binning choices. Precision-recall performance is reported alongside AUROC because the benchmark outcome is not evenly distributed [3].

Post-hoc explanation methods such as SHAP provide feature-attribution summaries for individual predictions [4]. However, explanation stability under small input perturbations is distinct from explanation validity: a stable attribution can still be misleading or non-causal. We therefore treat explanation stability as a sensitivity analysis, not as evidence that model explanations are clinically correct.

This study addresses four questions:

1. How do common classification models compare in discrimination and calibration on the selected public diabetes benchmark?
2. Does CORAL change discrimination and calibration relative to source-only training under a prespecified grid of controlled covariate and missingness perturbations?
3. Are the effects of CORAL consistent across model classes and shift scenarios, or is negative transfer observed?
4. How stable are local TreeSHAP feature rankings under small standardized input perturbations?

The contribution is a reproducible, model- and scenario-stratified evaluation of calibration and domain-adaptation behaviour under controlled perturbations, with explicit reporting of negative or negligible adaptation effects. The work does not claim to develop a clinically validated Nigerian diabetes model. It provides a methodological baseline for a separate future study using appropriately authorised Nigerian hospital data.

## 2. Related work

CORAL aligns source and target feature covariance structures as an unsupervised adaptation operation [1,2]. Its appeal is that target labels are not required; however, this does not mean that adaptation is free from assumptions. The target covariates must be available at the appropriate prediction time, and the shift must be sufficiently represented by the alignment operation. This study evaluates CORAL as a comparator rather than assuming that it is universally beneficial.

Probability calibration is a distinct model-performance property. Work on post-hoc calibration has demonstrated that classifier scores may not correspond to empirical event probabilities [5]. For clinical prediction models, calibration-in-the-large and calibration slope should be considered alongside discrimination and calibration plots. Evaluation guidance also emphasises assessment in new, relevant populations and settings before generalisability or implementation is claimed [6,7].

SHAP provides a unified framework for additive feature attribution [4]. The present study does not treat attribution stability as causal explanation or clinician-facing validation. It quantifies only the consistency of feature rankings under a specified perturbation procedure.

The reporting framework for prediction models using regression or machine-learning methods is now addressed by TRIPOD+AI [8]. PROBAST+AI provides a complementary framework for evaluating study quality, risk of bias and applicability [9]. These frameworks will guide the final manuscript audit; neither guideline substitutes for a suitable external validation dataset.

## 3. Methods

### 3.1 Study design and data source

This is a secondary methodological analysis of OpenML dataset 37, version 1, commonly referred to as the Pima Indians Diabetes dataset. The verified retrieval manifest records 768 observations, eight predictors, 500 negative and 268 positive outcome labels, and a CSV SHA-256 of `c980e5e01dc1c554a358102b773f34b29599d0051ec5cf5b56ad1c6fcb3a23b0`.

The dataset represents adult women of Pima heritage in a historical population near Phoenix, Arizona, USA [10]. Predictors are pregnancies, glucose, blood pressure, skin thickness, insulin, body mass index, diabetes pedigree function and age. The target is the dataset's recorded binary diabetes outcome. The analysis does not establish a prospective Nigerian risk-prediction endpoint.

The dataset is used solely as a methodological benchmark. It is not a Nigerian cohort and does not support claims about Nigerian patients, Nigerian hospitals or population-level transportability. A Mendeley deposit labelled as UITH/General Hospital Offa data was excluded from independent Nigerian validation because repository provenance review found it to reproduce the Pima dataset values and schema without independent site identifiers.

### 3.2 Preprocessing and baseline models

The preprocessing pipeline treats zero values in glucose, blood pressure, skin thickness, insulin and BMI as missing placeholders, then imputes using the training data. Scaling is fitted on training partitions only. This prevents test-partition information from influencing preprocessing estimates.

The five-fold benchmark compared logistic regression, random forest, gradient boosting, XGBoost and radial-basis-function support vector machines. Reported metrics were AUROC, AUPRC, sensitivity, specificity, Brier score and ECE.

### 3.3 Controlled distribution-shift experiment

The repeated experiment compared source-only training with CORAL for logistic regression, random forest and histogram gradient boosting. Five stratified 75:25 source-training/held-out splits were generated using seeds 42–46. Each held-out partition was transformed into one of seven prespecified scenarios:

- Reference: no added perturbation.
- Mild covariate shift.
- Severe covariate shift.
- MCAR-like missingness at 10%.
- Glucose-dependent MAR-like missingness at 10%.
- Combined mild covariate shift and MCAR-like missingness at 10%.
- Combined severe covariate shift and MAR-like missingness at 20%.

The covariate perturbation altered glucose, BMI and age using fixed severity-dependent transformations. MCAR-like missingness was applied to cells at random. The MAR-like mechanism made missingness probabilities depend on glucose and applied missingness to selected laboratory variables. These mechanisms are controlled stress tests. They are not empirical estimates of missingness mechanisms or site differences in Nigerian hospitals.

For each split, preprocessing and sigmoid probability calibration were fitted using source-training data. In the CORAL arm, the adaptation transformation was estimated from source-training features and held-out target covariates. Target labels were not used to fit CORAL or the prediction models; held-out labels were used only for final evaluation. This is a transductive unsupervised-adaptation design because target covariates are available during adaptation.

### 3.4 Outcomes

Discrimination was assessed using AUROC and AUPRC. Calibration was assessed using Brier score, 10-bin ECE, calibration-in-the-large, and logistic calibration intercept and slope. Selective prediction used entropy-based ranking and evaluated risk-coverage behaviour and retained-set metrics at 80% coverage. All metrics are interpreted as benchmark outcomes, not clinical operating characteristics.

### 3.5 Explanation-stability experiment

TreeSHAP explanations were evaluated for random forest and XGBoost using 100 held-out examples and seed 42. Standardized input perturbations were applied at noise standard deviations 0.01, 0.05 and 0.10. Feature-rank consistency was summarised using rank-biased overlap with persistence parameter 0.9. This procedure assesses local sensitivity to the chosen perturbations only.

### 3.6 Subgroup analysis and paired bootstrap

The planned subgroup analysis stratifies observations by age (<30, 30–49 and 50+) and BMI (<18.5, 18.5–24.9, 25–29.9 and >=30). Zero BMI values are excluded from BMI strata. Strata with fewer than 20 observations or fewer than five events in either outcome class are to retain denominator information while suppressing unstable discrimination estimates.

For eligible strata, paired bootstrap resampling is performed at the held-out patient-row level within each seed/model/scenario. The same resampled patient indices are used for source-only and CORAL predictions. Percentile intervals are planned for paired AUROC, AUPRC and Brier-score differences using 1,000 requested replicates. These intervals are split-specific and must not be pooled as if repeated overlapping splits were independent cohorts.

**Status:** The subgroup audit did not complete in the latest verified workflow. Its output files are absent from that run's artifact. This section describes the prespecified analysis only; no subgroup findings are reported. The updated implementation has been committed to the PR branch but awaits a successful workflow run and artifact verification.

### 3.7 Statistical interpretation and reproducibility

The five split seeds provide descriptive information about sensitivity to partitioning. They do not constitute five independent patient cohorts. Mean differences and standard deviations across seeds are therefore descriptive. No inferential claim of a statistically significant adaptation benefit is made from these repeated splits.

The workflow records per-split results, held-out predictions, paired adaptation differences, summary metrics, explanation-stability outputs and a dataset retrieval manifest. The final paper must include calibration plots and the completed subgroup artifact before submission.

## 4. Results

### 4.1 Baseline benchmark

Logistic regression achieved the highest baseline AUROC (0.835) and AUPRC (0.707), with Brier score 0.157 and ECE 0.036. Random forest was close (AUROC 0.834; AUPRC 0.698; Brier 0.157; ECE 0.040). Gradient boosting, XGBoost and RBF SVM did not exceed logistic regression on both discrimination and calibration. The baseline comparison therefore provides no evidence that model complexity alone improves benchmark performance.

### 4.2 Repeated controlled-shift experiment

Across five seeds, CORAL effects varied by model and scenario. Under the reference scenario, AUROC changes were -0.0019 for logistic regression, -0.0021 for random forest and +0.0019 for histogram gradient boosting.

Under severe covariate shift, AUROC changes were -0.0004, +0.0373 and +0.0437, respectively. Under MCAR-like 10% missingness, AUROC changes were +0.0011, -0.0033 and -0.0006. Under MAR-like 10% missingness, changes were -0.0019, -0.0018 and +0.0007.

Under combined severe covariate shift and MAR-like missingness at 20%, AUROC changes were -0.0007 for logistic regression, +0.0362 for random forest and +0.0505 for histogram gradient boosting. In the same combined scenario, AUPRC changes were -0.0067, +0.0825 and +0.0808, respectively.

Calibration deterioration under severe scenarios was pronounced in source-only models. In the combined severe scenario, source-only versus CORAL Brier scores were 0.2450 versus 0.1547 for logistic regression, 0.2210 versus 0.1540 for random forest, and 0.2269 versus 0.1638 for histogram gradient boosting. Corresponding ECE values were 0.2900 versus 0.0643, 0.2172 versus 0.0765, and 0.2094 versus 0.0754.

These changes are descriptive across five split seeds. They do not establish a universal or statistically confirmed benefit of CORAL. The results show that adaptation can improve selected metrics in specific severe controlled scenarios while having negligible or adverse effects in other conditions.

### 4.3 TreeSHAP explanation stability

Mean rank-biased overlap for random forest was 0.994 at noise SD 0.01, 0.974 at SD 0.05 and 0.963 at SD 0.10. For XGBoost, corresponding values were 0.971, 0.965 and 0.952. Stability declined as perturbation magnitude increased. The single-seed design and synthetic perturbation procedure limit interpretation.

### 4.4 Summary tables and figure legends

**Table 1. Five-fold benchmark performance**

| Model | AUROC | AUPRC | Brier | ECE | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|---:|
| Logistic regression | 0.835 | 0.707 | 0.157 | 0.036 | 0.571 | 0.880 |
| Random forest | 0.834 | 0.698 | 0.157 | 0.040 | 0.563 | 0.864 |
| Gradient boosting | 0.827 | 0.693 | 0.168 | 0.084 | 0.627 | 0.826 |
| XGBoost | 0.825 | 0.692 | 0.164 | 0.064 | 0.616 | 0.836 |
| RBF SVM | 0.821 | 0.697 | 0.164 | 0.055 | 0.541 | 0.868 |

**Table 2. Mean paired CORAL-minus-source-only AUROC differences across five split seeds**

| Scenario | Logistic regression | Random forest | Hist. gradient boosting |
|---|---:|---:|---:|
| Reference | -0.0019 | -0.0021 | +0.0019 |
| Covariate mild | -0.0011 | +0.0021 | +0.0050 |
| Covariate severe | -0.0004 | +0.0373 | +0.0437 |
| MCAR-like 10% | +0.0011 | -0.0033 | -0.0006 |
| MAR-like 10% | -0.0019 | -0.0018 | +0.0007 |
| Combined mild | +0.0026 | +0.0057 | +0.0112 |
| Combined severe | -0.0007 | +0.0362 | +0.0505 |

**Table 3. Calibration metrics under combined severe controlled shift**

| Model | Adaptation | Brier | ECE |
|---|---|---:|---:|
| Logistic regression | Source-only | 0.2450 | 0.2900 |
| Logistic regression | CORAL | 0.1547 | 0.0643 |
| Random forest | Source-only | 0.2210 | 0.2172 |
| Random forest | CORAL | 0.1540 | 0.0765 |
| Hist. gradient boosting | Source-only | 0.2269 | 0.2094 |
| Hist. gradient boosting | CORAL | 0.1638 | 0.0754 |

**Figure 1.** Five-fold baseline discrimination (AUROC and AUPRC) across the five benchmark classifiers.

**Figure 2.** Mean paired AUROC difference (CORAL minus source-only) across the seven controlled shift scenarios and three model classes. Positive values favour CORAL; negative values indicate negative transfer.

**Figure 3.** Brier score for source-only and CORAL models under combined severe covariate shift and MAR-like missingness. Lower values indicate better probabilistic accuracy.

**Figure 4.** ECE for source-only and CORAL models under combined severe controlled shift. Lower values indicate smaller average calibration error; ECE remains bin-dependent.

**Figure 5.** Mean TreeSHAP feature-rank RBO across three standardized perturbation magnitudes. Values are from 100 explained examples and one random seed.

### 4.5 Subgroup results

No subgroup results are available from the latest completed workflow. The subgroup and paired-bootstrap audit was cancelled before producing the required CSV outputs. Results must be added only after a successful rerun and review of subgroup denominators, event counts, paired resampling and confidence intervals.

## 5. Discussion

The primary finding is that CORAL's effect is conditional on both model class and shift scenario. Under severe covariate perturbations, random forest and histogram gradient boosting showed improved discrimination, and all three models showed improved calibration metrics. However, logistic-regression discrimination remained effectively unchanged. Under reference and missingness-only scenarios, adaptation effects were small, inconsistent or adverse.

This pattern argues against treating unsupervised covariance alignment as a generic robustness layer. The method aligns feature covariance structures; if the target change is not well represented by that structure, or if missingness alters information in a way not corrected by alignment, performance gains should not be expected. The negative or negligible results are therefore important and should remain visible in the manuscript.

Calibration results also demonstrate why discrimination alone is insufficient. In the severe controlled scenarios, source-only models experienced substantial increases in Brier score and ECE, while CORAL reduced these measures. This is a benchmark observation under the specified transformations, not proof that CORAL will recalibrate a model in a clinical deployment. ECE is bin-dependent, and calibration plots with uncertainty should accompany final reporting.

The baseline comparison does not justify preferring complex models solely on the basis of model class. Logistic regression performed at least as well as the more complex estimators on the reported baseline discrimination and calibration metrics. This finding supports retaining simple baselines in clinical prediction research.

The TreeSHAP results indicate relatively high local feature-rank stability under the tested perturbations, with a decline as noise increased. Stability should not be equated with correctness, causal relevance, fairness or clinician interpretability. Future work should examine explanation validity and clinical usefulness with domain experts and independently sampled clinical data.

## 6. Limitations

First, the dataset is small, historical and demographically narrow. It consists of adult women of Pima heritage and is not representative evidence for Nigerian clinical populations. Second, the controlled shifts are stylised transformations, not observed changes between hospitals, regions, time periods or laboratory systems. Third, only five random split seeds were used; repeated splits overlap in participants and do not provide independent cohort replication. Fourth, subgroup analysis is not yet complete. Fifth, the explanation-stability experiment uses one seed and a limited perturbation design. Sixth, no calibration plots, prospective workflow assessment, decision-curve analysis or independent Nigerian external validation are currently available. Finally, the paper evaluates recorded benchmark outcome classification and must not imply prospective clinical risk prediction or clinical deployment readiness.

## 7. Conclusion

On the OpenML Pima methodological benchmark, logistic regression provided the strongest baseline combination of discrimination and calibration among the evaluated models. CORAL improved selected tree-based model results under severe controlled covariate perturbations, but had little consistent benefit under reference or missingness-only scenarios. These findings support model- and scenario-specific evaluation rather than assuming that domain adaptation is universally beneficial. They do not establish Nigerian clinical validity, fairness or clinical utility. The corrected subgroup audit, final calibration visualisations, supervisor review and journal-specific reporting audit remain outstanding.

## Declarations to complete before submission

### Ethics approval and consent
This analysis used a public historical benchmark and did not recruit participants or access Nigerian patient records. No institutional ethics approval or exemption determination is claimed in this draft. The researcher should obtain the appropriate determination from the university research ethics process before submission if required by institutional or journal policy.

### Data availability
The benchmark is available through OpenML dataset ID 37. The retrieval manifest and SHA-256 are recorded in the repository. The manuscript should link to the exact dataset version and repository release used for the final analysis.

### Code availability
The analysis code and experiment protocols are maintained in the ClinAssist Nigeria repository: https://github.com/EkeminiThompson/clinassist-nigeria. A tagged, immutable release should be created after the final successful benchmark and subgroup workflow.

### Funding
To be completed. Do not state that the work had no funding until this has been confirmed by all authors.

### Conflicts of interest
To be completed by all authors.

### Author contributions
To be completed using the CRediT taxonomy after contributors agree on roles. Academic supervision alone does not automatically establish authorship; each listed author must meet the target journal's authorship criteria.

### Acknowledgements
To be completed with permission. Do not imply institutional endorsement or hospital participation.

### Target journal
Not yet selected. The final journal should accept methodological prediction-model evaluations using public benchmark data and controlled perturbation experiments. Confirm its policy on external validation, data provenance, reporting checklists, word limits, open data and article processing charges before formatting.

## References

1. Sun B, Feng J, Saenko K. Return of Frustratingly Easy Domain Adaptation. *Proceedings of the AAAI Conference on Artificial Intelligence*. 2016;30(1). doi:10.1609/aaai.v30i1.10306.
2. Sun B, Saenko K. Deep CORAL: Correlation Alignment for Deep Domain Adaptation. In: *Computer Vision – ECCV 2016 Workshops*. 2016:443–450. doi:10.1007/978-3-319-49409-8_35.
3. Saito T, Rehmsmeier M. The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE*. 2015;10(3):e0118432. doi:10.1371/journal.pone.0118432.
4. Lundberg SM, Lee SI. A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*. 2017;30:4765–4774.
5. Guo C, Pleiss G, Sun Y, Weinberger KQ. On calibration of modern neural networks. In: *Proceedings of the 34th International Conference on Machine Learning*. PMLR. 2017;70:1321–1330.
6. Collins GS, Dhiman P, Ma J, Schlussel MM, Archer L, Van Calster B, et al. Evaluation of clinical prediction models (part 1): from development to external validation. *BMJ*. 2024;384:e074819. doi:10.1136/bmj-2023-074819.
7. Collins GS, Dhiman P, Andaur Navarro C, Ma J, Hooft L, Reitsma JB, et al. Evaluation of clinical prediction models (part 2): how to undertake an external validation study. *BMJ*. 2024;384:e074820. doi:10.1136/bmj-2023-074820.
8. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*. 2024;385:e078378. doi:10.1136/bmj-2023-078378.
9. Moons KGM, Damen JA, Kaul T, Hooft L, Andaur Navarro C, Dhiman P, et al. PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods. *BMJ*. 2025;388:e082505. doi:10.1136/bmj-2024-082505.
10. Smith JW, Everhart JE, Dickson WC, Knowler WC, Johannes RS. Using the ADAP learning algorithm to forecast the onset of diabetes mellitus. In: *Proceedings of the Symposium on Computer Applications and Medical Care*. IEEE Computer Society Press; 1988:261–265.
11. OpenML. Diabetes (Pima Indians Diabetes Database), data ID 37, version 1. https://www.openml.org/d/37.
