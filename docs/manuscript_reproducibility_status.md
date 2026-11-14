# Manuscript reproducibility and submission status

**Updated:** 2026-11-14  
**Repository:** EkeminiThompson/clinassist-nigeria

## Verified against committed source code

- Both manuscripts include the author-supplied ORCID, corresponding email and affiliations: Nnamdi Azikiwe University and VergelAI.
- The baseline Table 1 gradient-boosting estimator is `GradientBoostingClassifier`; the repeated-split shift study uses `HistGradientBoostingClassifier`. They are separate experiments.
- The executable shift protocol is present at `ml/experiments/run_shift_study.py`. It defines all seven scenarios, feature transformations, scenario-specific seeds, model constructors and calibration procedure. The successful CI run #156 (run ID `43558361142`, source commit `bc8611e42eac4832e5260804fb31bae1736fd17e`) completed all 210 split/model/scenario/adaptation cells and uploaded the run artifacts. The workflow committed the generated raw outputs to this PR branch in commit `6764354763d2fb3e0568e597942ecff628e110c3` after successful CI run #160 (run ID `43571392655`).
- CORAL implementation is present at `ml/domain_adaptation/coral.py`. Its source-to-target mapping is `(X_s - mean_s) @ C_s^(-1/2) @ C_t^(1/2) + mean_t`, with covariance regularisation epsilon (10^{-5}). It fits from source and target feature matrices only; target labels are not accepted by the adapter.
- The explanation-stability and subgroup-audit scripts are present. The subgroup audit consumes patient-level predictions from the shift study and uses paired bootstrap resampling.
- The baseline estimator settings and shift-study estimator settings are documented from their respective source files.
- An MIT licence applies to repository software only; it does not relicense the Pima benchmark or third-party assets.

## Remaining evidence and author decisions

1. **Original run environment:** the original reported run and 2026-11-13 independent verification run do not have retained CPU, RAM and OS details. The current research CI workflow is pinned to GitHub-hosted ubuntu-24.04 (x86-64), Python 3.11; for public repositories GitHub documents 4 vCPUs and 16 GB RAM. The workflow now logs the actual CPU model, memory and OS for each run. These CI specifications must not be retroactively attributed to historical runs. The independent verification note separately records Python 3.12, scikit-learn 1.9.1 and XGBoost 3.4.1 for its clean rerun.
2. **Execution evidence and scenario reporting:** verified by successful CI run #164 (run ID `43571713333`; source commit `9d31dfbb6105168abca0d62706f1f98dec01feec`; final output commit `79438a8927669a2d18924200619e1fd8c98b069a`). All seven prespecified scenarios ran across five seeds, three classifiers and two adaptation arms (210 run rows). The artifact contained 42 summary rows, 1,050 unrounded paired metric differences and 40,320 held-out prediction rows. Appendix B now reports all 21 model-by-scenario paired comparisons for AUROC, Brier and ECE. The raw JSON/CSV files are being committed with the reproducibility workflow; retain the CI artifact checksum `sha256:934d18546c3147797e3a48900b9956e2e8fd463965c651e1fe6a890ff258b222` as the provenance of run #156.
3. **AUROC reconciliation:** recomputed from unrounded paired split-level output. For severe combined shift, mean CORAL-minus-source-only AUROC differences are −0.0007 (logistic regression), +0.0362 (random forest) and +0.0505 (histogram gradient boosting). These agree with the paired run-level data; do not derive them from rounded arm means.
4. **Hyperparameter search:** no tuning/search routine is present in the reviewed experiment scripts. The author should confirm whether any separate tuning was performed; do not imply optimisation or tuning in the manuscript without records.
5. **Hypothesis testing:** subgroup paired-bootstrap intervals are exploratory. They are not evidence that prespecified confirmatory hypothesis tests were conducted.
6. **Ethics and governance:** obtain and accurately report any institutional/venue ethics determination required for secondary analysis of the public benchmark. No approval or exemption is asserted here.
7. **Supervisor review, author order, contributions and competing interests:** require author/institutional confirmation.
8. **References and journal style:** verify every reference against its original source and apply the target journal's current citation and bibliography requirements.
9. **Target-journal checklist:** complete the applicable TRIPOD+AI reporting checklist and any journal-specific submission forms.
10. **Data terms and archive:** cite the actual OpenML/UCI dataset source and applicable terms used for the experiment. Zenodo deposit is optional. Citation/deposit metadata are prepared in `CITATION.cff` and `.zenodo.json`; no deposit or DOI exists yet. Create a versioned release and archive only after final code and artifacts are checked. See `docs/submission_metadata.md`.

## Methodological limitation retained

The code applies covariate and missingness transformations to raw held-out test features before the preprocessing pipeline replaces zero values with missing values, imputes and scales. This means a raw zero can be changed by a shift before zero-to-missing conversion. The manuscript should retain this ordering as a limitation unless the protocol is intentionally changed and all affected experiments are rerun.

## Submission metadata requiring confirmation

- The author supplied the name Dr. Joshua Babatunde Agbogun for the Associate Editor field and provided a Federal University Lokoja profile. Confirm that he is the assigned handling editor with the journal before addressing the cover letter to him. Do not present his editorial role as independently verified. See `docs/submission_metadata.md`.
- ACM author-year BibLaTeX configuration and Zenodo deposit steps are documented in `docs/submission_metadata.md`.

## Scientific boundary

The current experiments use only the public Pima Indians Diabetes benchmark (768 records). The work is a controlled computational methodology study, not Nigerian hospital data, multi-hospital external validation, a fairness certification, clinical utility evidence or a deployment evaluation.