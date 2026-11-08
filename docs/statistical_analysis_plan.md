# Statistical analysis plan

## Scope and data boundary
The available dataset is the historical Pima Indians Diabetes benchmark (768 observations, eight predictors), not a Nigerian cohort. This protocol evaluates methodological behaviour under explicitly controlled synthetic shifts. No result is external clinical validation or evidence of transportability to Nigerian patients.

## Research questions and hypotheses
- **RQ1 / H1:** Does unsupervised CORAL adaptation change discrimination and calibration relative to source-only training under prespecified covariate and missingness shifts? No direction of benefit is assumed; negative transfer is a primary result to report.
- **RQ2 / H2:** Does entropy-ranked selective prediction reduce empirical error among retained cases at fixed 80% coverage, and what is the accompanying coverage-risk trade-off?
- **RQ3 / H3:** How sensitive are local TreeSHAP feature rankings to small, controlled perturbations of standardized input features?
- **RQ4:** Can the software provide auditable, metadata-only offline receipt handling without storing clinical payloads in the queue?

## Experimental design
Use repeated stratified 75/25 source/held-out splits with fixed, published seeds. Fit preprocessing on source-training rows only. Create target stress-test covariates after splitting; never use held-out labels to fit preprocessing, CORAL, calibration or model parameters. CORAL may use held-out target covariates as an explicitly transductive, unsupervised adaptation input. Held-out labels are used only for final evaluation.

The shift grid includes an unshifted reference, mild/severe covariate shifts, MCAR-like missingness, glucose-dependent MAR-like missingness in selected laboratory fields, and combined scenarios. These are simplified stress tests, not claims about real hospital missingness processes.

Compare logistic regression, random forest and histogram gradient boosting. Calibrate probability outputs using sigmoid calibration with source-training folds only. Report the calibration method and limitations under target shift.

## Outcomes
- Primary discrimination: area under the precision-recall curve (AUPRC), interpreted alongside prevalence.
- Secondary discrimination: AUROC, sensitivity, specificity, precision and F1 at the prespecified 0.5 threshold.
- Calibration: Brier score, 10-bin expected calibration error (ECE), calibration-in-the-large intercept, and joint logistic calibration intercept/slope (ideal intercept 0, slope 1). Calibration plots should accompany the numeric metrics in a publication-ready analysis.
- Selective prediction: risk-coverage curve, area under the risk-coverage curve (AURC), and retained-set metrics at 80% target coverage.
- Explainability: local feature-rank stability using rank-biased overlap (p=0.9) at standardized perturbation SD 0.01, 0.05 and 0.10.\n- Exploratory subgroup analysis: age (<30, 30–49, 50+) and BMI (<18.5, 18.5–24.9, 25–29.9, >=30) strata, reporting sample count, event count, prevalence, discrimination and calibration. Invalid zero BMI values are excluded from BMI strata. The Pima benchmark contains only women of Pima heritage; sex/race subgroup fairness cannot be assessed.
- Systems: authentication/RBAC tests, migration tests, sync idempotency and rejection of clinical payload fields.

## Statistical reporting
Report each split's metrics and held-out predictions, mean and standard deviation across repeated splits, and paired CORAL-minus-source-only differences by split. A paired patient bootstrap within each held-out split supplies exploratory 95% intervals for AUROC, AUPRC and Brier deltas. These split-specific intervals must not be pooled as if repeated overlapping splits were independent; the summary envelope is descriptive only. These repeated-split summaries describe split variability; they are not independent patient-level confidence intervals. Do not apply naive significance tests treating repeated splits as independent cohorts. A confirmatory external study must prespecify site-level or temporal holdouts and use patient-level resampling that respects clustering.

## Ablations
1. Source-only versus CORAL.
2. No shift versus covariate-only, missingness-only and combined shifts.
3. MCAR-like versus glucose-dependent MAR-like missingness.
4. Discrimination/calibration with and without selective abstention.
5. Logistic regression versus tree ensembles.
6. TreeSHAP ranking stability across perturbation magnitudes.

## Reproducibility
Record dataset version and SHA-256 manifest, feature schema, preprocessing configuration, split seeds, model hyperparameters, calibration folds, scenario definitions, software versions, raw per-split predictions and metrics. Do not publish aggregate headline results without corresponding run artifacts.

## Decision rules
Subgroup metrics with small event counts are unstable and must not be used to rank groups or claim fairness. Report denominators and event counts, suppress sparse strata in any public release, and obtain external cohort-specific subgroup validation.\n\nNo single metric determines success. A method that improves AUROC while materially worsening calibration, AUPRC or retained-case safety is not declared superior. CORAL negative transfer must be reported. Thresholds must not be tuned on held-out target labels.

## Future authentic validation
A future Nigerian multi-site study requires verified site provenance, data-use agreements, ethics approval, prespecified site-held-out evaluation, local calibration, subgroup analyses, missingness characterization and prospective workflow/human-factors evaluation. Until then, no Nigerian clinical validity claim is permitted.