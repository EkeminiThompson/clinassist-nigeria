# Supplementary Technical Report: TreeSHAP Sensitivity and Sparse Subgroup Auditing in the Pima Diabetes Benchmark

**Author:** Ekemini Thompson  
**Affiliation:** Nnamdi Azikiwe University, Awka, Nigeria  
**Status:** Supplementary technical report accompanying the primary ClinAssist benchmark manuscript; not a separate original research submission  
**Study type:** Exploratory computational audit

## Abstract

**Background:** Predictive performance alone does not establish that model explanations are stable or that subgroup estimates are sufficiently supported by data. Small benchmark datasets make these questions sensitive to perturbation size, subgroup event counts and resampling validity.

**Objective:** To provide reproducible methodological detail for two ancillary analyses reported in the primary ClinAssist benchmark manuscript: local TreeSHAP feature-ranking sensitivity under controlled input perturbations, and paired-bootstrap subgroup auditing with prespecified sparse-stratum suppression.

**Methods:** Analyses used OpenML dataset 37, the Pima Indians Diabetes benchmark. The explanation experiment trained random forest and XGBoost models on one stratified 75:25 split (seed 42), computed TreeSHAP attributions for up to 100 held-out observations, perturbed standardised features with Gaussian noise at standard deviations 0.01, 0.05 and 0.10, and compared feature rankings using rank-biased overlap (RBO; persistence 0.9). The subgroup audit considered age bands (<30, 30–49, 50+) and BMI bands (<18.5, 18.5–24.9, 25–29.9, ≥30). Source-only and CORAL predictions were paired by original row identifier. One thousand paired patient-row bootstrap draws were requested; comparisons were retained only when subgroup size, class-count and bootstrap-validity criteria were met.

**Results:** Mean RBO for random forest was 0.9944, 0.9743 and 0.9630 at noise standard deviations 0.01, 0.05 and 0.10. Corresponding XGBoost values were 0.9711, 0.9652 and 0.9522. The subgroup audit generated 1,638 metric rows and 819 paired-bootstrap comparisons. Of these, 609 met prespecified eligibility and validity criteria; 210 sparse comparisons were suppressed. Among retained comparisons, 595 had 1,000 valid draws, 12 had 999 and two had 998.

**Conclusion:** In this single-split benchmark experiment, local feature-ranking agreement declined as perturbation magnitude increased. The subgroup workflow operationalised paired resampling and suppression of sparse comparisons. These are exploratory methodological observations, not evidence of causal explanation validity, fairness or subgroup performance in Nigerian patients.

**Keywords:** diabetes prediction; explainable AI; TreeSHAP; rank-biased overlap; subgroup audit; paired bootstrap; sparse data.

## 1. Introduction

Clinical prediction studies often report discrimination and calibration without examining how sensitive model explanations are to small input changes or whether subgroup estimates are supported by adequate numbers of outcome events. These questions are important in small datasets, where a few observations can materially change subgroup metrics and feature-attribution rankings may respond to perturbations.

This supplementary report expands the methods and audit-coverage details for two ancillary analyses already summarised in the primary ClinAssist benchmark manuscript. It is provided to improve transparency and reproducibility, not to claim a separate independent study. The first examines local TreeSHAP feature-ranking agreement under specified Gaussian perturbations. The second describes a paired subgroup bootstrap workflow that suppresses comparisons failing prespecified sample and resampling criteria.

The data are the historical Pima Indians Diabetes benchmark, not a Nigerian clinical cohort. Stable feature rankings are not treated as causal explanations, and subgroup metrics are not treated as proof of fairness.

## 2. Methods

### 2.1 Dataset and scope

The analyses used OpenML dataset 37, comprising 768 records and eight predictors. The dataset represents adult women of Pima heritage. Findings are benchmark-specific and are not estimates of performance in Nigerian hospitals.

### 2.2 Local explanation stability

Random forest and XGBoost models were trained using one stratified 75:25 split with random seed 42. TreeSHAP attributions were computed for up to 100 held-out examples, using a source-training background sample of up to 100 observations. Standardised feature vectors were perturbed with independent Gaussian noise at standard deviations 0.01, 0.05 and 0.10. Original and perturbed feature rankings were compared using rank-biased overlap with persistence parameter 0.9.

This design evaluates local ranking sensitivity under the specified perturbation procedure. It does not test explanation faithfulness, causality, clinician interpretability or stability across hospitals. The experiment uses a single split and should be interpreted accordingly.

### 2.3 Exploratory subgroup audit

The subgroup audit considered age categories (<30, 30–49 and 50+) and BMI categories (<18.5, 18.5–24.9, 25–29.9 and ≥30). BMI values recorded as zero were excluded from BMI strata. Metric eligibility required at least 20 observations and at least five observations from each outcome class.

For each seed/model/scenario/stratum, source-only and CORAL predictions were paired using original dataset row identifiers. The bootstrap resampled patient rows with replacement while retaining paired adaptation arms within each draw. One thousand draws were requested. A comparison was accepted only if at least 90% of requested draws were valid. Comparisons failing the prespecified event or validity rules were suppressed.

### 2.4 Reproducibility

The analysis scripts and experiment definitions are maintained in the ClinAssist repository. The archived CI artifact records the outputs used for this report. This manuscript reports the completed exploratory outputs described above and does not claim independent re-execution beyond that archived run.

## 3. Results

### 3.1 TreeSHAP ranking stability

| Model | Gaussian noise SD 0.01 | SD 0.05 | SD 0.10 |
|---|---:|---:|---:|
| Random forest | 0.9944 | 0.9743 | 0.9630 |
| XGBoost | 0.9711 | 0.9652 | 0.9522 |

For both models, mean feature-ranking agreement declined as perturbation magnitude increased. Random forest had higher mean RBO than XGBoost at each tested noise level in this single-split experiment.

### 3.2 Subgroup audit

The audit produced 1,638 subgroup metric rows and 819 paired-bootstrap comparisons. A total of 609 comparisons met the prespecified minimum subgroup event counts and bootstrap validity criteria. The remaining 210 comparisons were suppressed as insufficiently supported. Of the retained comparisons, 595 had 1,000 valid bootstrap draws, 12 had 999 and two had 998.

The results reported here describe audit coverage and resampling validity. No claim is made about which age or BMI subgroup benefits most from CORAL because detailed stratum-level estimates and intervals are not independently reproduced in this manuscript.

## 4. Discussion

The explanation experiment indicates that local feature-ranking agreement was high under the smallest tested perturbation and decreased as noise increased. RBO depends on the selected models, background sample, feature scaling, perturbation distribution, number of explained observations and ranking metric. A high RBO does not establish that an attribution is causally correct or clinically meaningful.

The subgroup audit demonstrates an explicit safeguard for sparse strata. Suppressing 210 comparisons avoids presenting metrics or intervals from groups that did not meet the predefined support criteria. This is a reporting safeguard, not evidence that the remaining subgroup estimates are sufficiently powered for fairness conclusions.

Both analyses are constrained by the benchmark's small sample size and population composition. The explanation experiment used one split; subgroup analyses were exploratory; and neither analysis involved independent hospitals or Nigerian patient data. The paired bootstrap preserves within-row pairing between adaptation arms, but it does not convert the benchmark into an external validation cohort.

## 5. Conclusion

This supplementary report records the implementation details and coverage counts for the TreeSHAP sensitivity experiment and sparse subgroup audit. The single-split explanation analysis showed declining local feature-ranking agreement under larger Gaussian perturbations; the subgroup workflow suppressed comparisons that failed prespecified support or bootstrap-validity rules. These are ancillary methodological observations from the same Pima benchmark used in the primary manuscript. They do not establish causal explanations, fairness, clinical utility or Nigerian population validity, and they should not be submitted or presented as an independent second cohort study.

## Declarations

- **Ethics:** This work analyses a previously released public benchmark. The author should obtain and report the relevant institutional determination before journal submission; no exemption is asserted here.
- **Data:** OpenML dataset 37, https://www.openml.org/d/37.
- **Code:** https://github.com/EkeminiThompson/clinassist-nigeria.
- **Funding:** To be completed by the author.
- **Competing interests:** To be completed by the author.
- **Author contributions:** Ekemini Thompson: methodology, software, formal analysis and drafting; confirm before submission.

## References

1. Lundberg SM, Lee SI. A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems. 2017.
2. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378.
3. OpenML. Diabetes dataset, data ID 37. https://www.openml.org/d/37.
4. Sun B, Feng J, Saenko K. Correlation Alignment for Unsupervised Domain Adaptation. arXiv:1612.01939. https://arxiv.org/abs/1612.01939.

**Relationship to the primary manuscript:** This document is supplementary material for the ClinAssist calibration and domain-adaptation benchmark manuscript. Its TreeSHAP and subgroup-audit analyses are already summarised in that primary manuscript. Do not submit this report as a separate original research paper or duplicate the same results in another journal submission. If a journal requests supplementary methods or audit outputs, provide this document after checking its format and removing any overlap the editor considers unnecessary.