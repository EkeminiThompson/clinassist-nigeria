# Model card — ClinAssist baseline and research pipeline

## Status
Research prototype. Not approved for clinical use, diagnosis, screening decisions, triage or treatment selection.

## Model task and selectable estimators
The API currently exposes three benchmark estimators: logistic regression, random forest and XGBoost. All are trained on the public Pima Indians Diabetes dataset. The returned score is not an individual's calibrated clinical risk. The service currently uses binary entropy of a single model score as a simple uncertainty indicator; it is not a calibrated confidence interval.

## Data provenance and population
The benchmark has 768 observations and eight input variables. It represents adult women of Pima heritage and is not a Nigerian cohort. The purported UITH/General Hospital Offa deposit was found to repackage the same public benchmark and lacks site identifiers. It is excluded from Nigerian validation claims. See `docs/dataset_provenance.md` and the OpenML dataset 37 retrieval manifest.

## Intended users and use
The interface is an engineering and methodological research demonstrator for qualified research teams. It is not intended for use in patient care. Never enter identifiable patient information.

## Explanations
Logistic regression uses SHAP when available, with an explicitly labelled coefficient fallback. Random Forest and XGBoost use TreeSHAP on the probability scale. If TreeSHAP cannot be computed for a tree model, the service fails the explanation request rather than mislabelling a global feature importance as a local explanation. SHAP explains model behaviour, not causal effects.

## Evaluation
The repository includes leakage-aware preprocessing, source-only baseline comparisons, CORAL adaptation using held-out target covariates only, controlled synthetic covariate/missingness shifts, calibration metrics, selective prediction and local TreeSHAP stability experiments. No result is asserted until experiments are run against the verified local benchmark and their artifacts reviewed.

## Limitations and risks
- No verified Nigerian multi-hospital cohort is available in the repository.
- Small historical benchmark; population and temporal representativeness are limited.
- No prospective evaluation, clinical workflow study, subgroup validation or fairness assessment has been completed.
- Synthetic shifts do not recreate all clinical or institutional heterogeneity.
- Source calibration may not remain valid after distribution shift.
- Model outputs can be wrong and must not direct care.

## Required evidence before any clinical evaluation
Ethics approval; data-use agreements; provenance and site verification; independent external validation; subgroup performance and calibration; prospective workflow and human-factors evaluation; clinical safety review; security/privacy assessment; locally approved operating procedures; and monitoring with a defined rollback process.
