# Manuscript reproducibility and submission status

**Updated:** 2026-11-14  
**Repository:** EkeminiThompson/clinassist-nigeria

## Corrections made in this branch

- Added corresponding-author email and ORCID to both manuscript author blocks.
- Corrected the baseline Table 1 model label to `GradientBoostingClassifier`; the separate shift-study model remains described as histogram gradient boosting.
- Clarified that the severe combined scenario uses 20% glucose-dependent MAR missingness, while the single missingness scenarios use 10%; combined mild uses 10% MCAR and mild covariate severity 0.5.
- Clarified that CORAL is transductive unsupervised adaptation, uses unlabelled target covariates, and aligns both means and covariance structure.
- Added an MIT licence for repository software. This licence does not change the licence or terms governing the OpenML/Pima dataset or any third-party assets.

## Items deliberately not fabricated

The following cannot be closed from the current committed repository evidence:

1. **Second author affiliation:** the repository previously identified Nnamdi Azikiwe University only. No second institution or official department name was independently available in the project record. Add only after the author confirms its exact official wording.
2. **Hardware:** CPU, RAM and operating system for the reported runs are not recorded. Do not infer them from the current CI runner or a later verification machine.
3. **Hyperparameter search:** no tuning procedure is documented in the accessible experiment record. The author must confirm whether tuning was performed before the checklist can answer this.
4. **Hypothesis tests:** the subgroup paired-bootstrap intervals are exploratory. They do not establish that formal, prespecified hypothesis tests were run.
5. **Ethics determination, supervisor review and author order:** these are author/institutional decisions and remain pending until documented.
6. **ORCID and author metadata:** ORCID and corresponding email are supplied by the author and now included. No Associate Editor name should be invented; it is venue-assigned.
7. **Exact shift implementation:** the current public main branch did not expose the referenced `run_shift_study.py` or `domain_adaptation_results.json` at the paths checked. The manuscript records the verified scenario rates and severity values, but feature-wise shift equations and per-scenario seeds must be reconciled against the exact run script and output files before submission.
8. **CORAL implementation:** the manuscript includes the standard regularised mean-and-covariance alignment expression with epsilon 1e-5, based on the supplied study description. It must be compared line-by-line with the actual implementation before claiming exact code correspondence.
9. **Age/BMI subgroup shift results:** the independent verification report records AUROC/ECE for the age and BMI controlled shifts, but the source experiment script and complete result artifact were not found at the expected paths. These results are therefore not expanded into additional inferential claims.
10. **Six remaining scenario result tables:** only the severe combined scenario is fully tabulated in the current manuscript. The remaining scenario output CSVs are required to report all six other conditions.
11. **References and target-journal style:** references must be checked against the original sources and converted to the target journal's required bibliography system. Do not describe BibTeX as biblatex/acmauthoryear.
12. **Zero-to-missing order:** the recorded pipeline applies shift transformations to held-out raw feature values before zero-to-missing conversion. This can change originally zero values. Retain this as a stated limitation unless the experiment is corrected and rerun.

## Result reconciliation issue

The reported AUROC differences in the exploratory audit (−0.0008, +0.0367, +0.0508) do not exactly equal the differences calculated from the rounded Table 2 means (−0.0007, +0.0362, +0.0505). Recompute from unrounded paired split-level outputs and use one authoritative calculation before submission. Rounded table means are insufficient to resolve this.

## Data and code availability

The repository's MIT licence applies to the repository software. The Pima benchmark remains governed by its source terms; the dataset provenance record identifies the Mendeley repackage as CC BY 4.0 but the manuscript's OpenML retrieval should cite and state the actual source terms used. A Zenodo archive with a versioned DOI is still recommended for persistent release.
