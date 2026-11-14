# Computational reproducibility checklist response

**Manuscript:** *Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions*  
**Repository:** https://github.com/EkeminiThompson/clinassist-nigeria  
**Status:** Evidence-based author response, updated 2026-11-14.

This response distinguishes a true “not applicable” from an unmet or only partly evidenced item. Do not change a response to “yes” solely to improve the checklist score.

## Dataset reporting

| Item | Response | Evidence / explanation |
|---|---|---|
| (1) Newly introduced datasets publicly available with long-term access and research-use licence | NA | No new dataset was collected or introduced. The study uses the existing Pima Indians Diabetes benchmark (OpenML ID 37). |
| (2) Newly introduced dataset licensed for reproducibility | NA | No newly introduced dataset. |
| (3) Newly introduced dataset licensed for general research | NA | No newly introduced dataset. |
| (4) Public/literature datasets appropriately cited | Yes | Cite the original Pima dataset paper (Smith et al., 1988) and OpenML (Vanschoren et al., 2013; Feurer et al., 2021). The manuscript and provenance record identify OpenML dataset 37. |
| (5) Existing literature datasets publicly available | Yes | OpenML dataset 37, version 1 is publicly accessible. The source CSV is retrieved at runtime and is not committed. |
| (6) New or non-public datasets described in detail | NA | No new or non-public dataset is analysed. The public benchmark's dimensions, features, outcome counts, source population and preprocessing are described in the manuscript and provenance file. |
| (7) Preprocessing, augmentation and splitting described | Yes | Zero-to-missing handling, training-only imputation/scaling, stratified 75:25 splits, seeds, shift transformations and CORAL fit boundaries are specified in the manuscript and docs/experiment_protocol.md. |

**Dataset licence qualification:** OpenML's dataset 37 record reports the access label “Public”, not a CC or SPDX licence. Public access is not itself a licence grant. The repository therefore does not invent a CC0/CC BY licence for the original Pima source. Its source attribution and terms must be observed. The repository's DATA-LICENSE.md separately licenses author-generated experiment outputs under CC BY 4.0 to the extent of author-held rights, without purporting to relicense source labels or the source dataset.

## Design choices and computational experiments

| Item | Response | Evidence / explanation |
|---|---|---|
| Motivation for design choices beyond metrics | Yes (revised) | The manuscript now explains the methodological role and limits of the public benchmark, why the three complementary classifiers were selected, why calibration is evaluated, why CORAL is used as a label-free second-order alignment comparator, why controlled covariate/missingness scenarios are used, and why repeated paired splits are used. |
| Computational experiments included | Yes | Baseline cross-validation, repeated controlled-shift experiment, TreeSHAP perturbation experiment and exploratory subgroup audit. |
| (1) Source code available and documented | Yes | Research code and reproduction sequence are in the public repository. |
| (2) Code licence for reproducibility | Yes | MIT licence. |
| (3) Code licence for research use | Yes | MIT licence. |
| (4) Raw, unaggregated experimental outputs available | Yes | These outputs are committed and retrievable at PR head `48cff833f43299a62aaa77a83cd64deb308f3897`: baseline five-fold out-of-fold predictions (`baseline_cv_predictions.csv`), split-level shift metrics and held-out predictions, paired differences and run manifest, per-example TreeSHAP RBO values (`explanation_stability_raw.csv`), subgroup metric rows (`subgroup_metrics.csv`), replicate-level paired-bootstrap deltas (`subgroup_bootstrap_draws.csv.gz`), and summary tables. The raw TreeSHAP file (19,470 bytes) and compressed subgroup draws (17,320,709 bytes) are present in the branch tree. The CI run that generated and committed these outputs passed research-benchmarks, backend and frontend on parent commit `d9cd22f6717f491c5e1e919c405e5ce3c1e810aa`; the subsequent output-archive commit is the current PR head. A follow-on workflow run for that bot-authored head is marked `action_required` and has not executed jobs. |
| (5) Unaggregated output licence for reproducibility | Yes, with source-data caveat | Author-generated result files are CC BY 4.0 to the extent of author-held rights. Source labels remain subject to the original dataset's terms. |
| (6) Unaggregated output licence for research | Yes, with source-data caveat | Same as item (5); see DATA-LICENSE.md. |
| (7) Random-number generation and seeds | Yes | NumPy default_rng, split seeds 42–46, scenario seed rule seed + 1000 × scenario_index, model random states and bootstrap seed are documented in code and protocol. |
| (8) Execution environment and hardware | Partially | The actual CI environment and workflow are described and hardware is logged by the workflow. The author's local MacBook is separately reported. The exact original-run CPU cache, complete package lock and historical run-to-machine mapping are not retained; do not claim those details are known. |
| (9) Metrics clearly explained and motivated | Yes (revised) | AUROC/AUPRC assess ranking; Brier/ECE and calibration intercept/slope assess probability quality; risk–coverage and selective metrics assess abstention behaviour; RBO assesses ranking stability of local explanations. The manuscript now explains these complementary dimensions. |
| (10) Number of algorithm runs reported | Yes | Five split seeds × seven scenarios × three classifiers × two adaptation arms = 210 shift-study cells; five-fold baseline CV; explanation study uses 100 held-out examples in one split; subgroup bootstrap requests 1,000 replicates. |
| (11) No silent cherry-picking | Yes | All seven prespecified scenarios and all 210 shift-study cells are retained; the committed outputs preserve raw run rows and paired differences. |
| (12) Variation/distributional information | Yes | Mean and SD across five paired splits; paired bootstrap intervals in the exploratory subgroup audit; unrounded split-level outputs retained. |
| (13) Hyperparameter settings and rationale | Yes (revised) | The fixed estimator settings, calibration method, CORAL regularisation and perturbation parameters are documented, with methodological rationale. These are fixed protocol settings, not a claim of optimised hyperparameters. |
| (14) Number/range of hyperparameter settings explored and optimisation effort | No / not documented | The committed experiment code contains no hyperparameter-search routine or search log. The record now states that no systematic search is evidenced and does not invent a search range or optimisation effort. The author must confirm whether any separate manual or external tuning occurred before submission. |
| (15) Statistical hypothesis tests | Partially | An exact two-sided paired sign-flip test was added for five split-level differences in each model-by-scenario contrast for AUROC, Brier and ECE (63 tests), with Holm adjustment within each metric family. The smallest attainable unadjusted p-value is 0.0625 because n=5; no comparison reached 0.05 and all Holm-adjusted p-values are 1.00. The five train/test splits overlap, so these are exploratory sensitivity tests, not confirmatory population-level inference. The manuscript explicitly reports the limitation rather than claiming statistical significance. |

## Important author confirmations before submission

1. Confirm that no separate hyperparameter search or manual tuning was performed outside the committed repository. If tuning did occur, provide the candidate values, search method, selection criterion and compute effort so it can be reported accurately.
2. Confirm the target journal's required interpretation of the OpenML/UCI dataset terms and whether the editor accepts “Public” access status with original-source attribution in the absence of a dataset-specific SPDX/Creative Commons declaration.
3. Keep items (8), (14) and (15) qualified as above unless additional contemporaneous evidence or a larger, appropriately designed experiment is produced.

## Files supporting this response

- papers/01_calibration_domain_adaptation_diabetes.md
- docs/experiment_protocol.md
- docs/dataset_provenance.md
- ml/analysis/paired_sign_flip_tests.py
- ml/artifacts/experiments/paired_sign_flip_tests.csv
- DATA-LICENSE.md
- LICENSE
