# Model card — ClinAssist baseline and research pipeline

## Status
Research prototype. Not approved for clinical use, diagnosis, screening decisions, triage, or treatment selection.

## Model task
The current API exposes a binary diabetes-outcome benchmark model trained on the public Pima Indians Diabetes dataset. The prediction probability is a model score on this benchmark, not an individual's calibrated clinical risk.

## Data provenance and population
The Pima dataset contains 768 records and eight input variables. It is not a Nigerian cohort and does not contain hospital/site identifiers. A separate deposit represented as Nigerian hospital data was identified as a repackaging of the same benchmark. It is excluded from claims of Nigerian validation. See `docs/dataset_provenance.md`.

## Intended users and use
The interface is an engineering and methodological research demonstrator for qualified research teams. It is not intended for use in patient care. Never enter identifiable patient information.

## Evaluation
The repository includes leakage-aware preprocessing, benchmark baselines, discrimination and calibration metrics, selective-prediction metrics, and a controlled synthetic covariate/missingness shift protocol comparing source-only and CORAL-adapted models. Synthetic stress tests are not external validation. Results are not asserted until run on a verified dataset and independently checked.

## Uncertainty and explanations
The current service uses binary entropy of a single predicted probability as a simple uncertainty score. It is not a calibrated confidence interval and does not quantify all sources of uncertainty. SHAP explains model behaviour, not causal effects; coefficient fallback is labelled separately. Attribution stability should be reported under the documented perturbation protocol.

## Limitations and risks
- No verified Nigerian multi-hospital cohort is currently available in the repository.
- Small historical benchmark; population and temporal representativeness are limited.
- No prospective evaluation, clinical workflow study, subgroup validation, or fairness assessment has been completed.
- Missingness and distribution shifts in the stress test are synthetic assumptions.
- Calibration on source data may not hold after distribution shift.
- Model outputs can be wrong and must not direct care.

## Required evidence before any clinical evaluation
Ethics approval; data-use agreements; provenance and site verification; independent external validation; subgroup performance and calibration; prospective workflow and human-factors evaluation; clinical safety review; security/privacy assessment; locally approved operating procedures; and monitoring with a defined rollback process.
