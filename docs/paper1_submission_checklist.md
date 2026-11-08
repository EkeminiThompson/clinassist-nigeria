# Paper 1 submission-readiness checklist

**Working title:** Evaluating Calibration, Model Robustness and Domain Adaptation in Diabetes Prediction Across Changing Data Distributions  
**Institutional context:** Nnamdi Azikiwe University, Awka, Nigeria  
**Proposed academic supervisor:** Prof. V. E. Ejiofor  
**Status:** Internal working draft; not ready for journal submission.

| Component | Status | Evidence / next action |
|---|---|---|
| Title | Drafted | Retains the agreed title without naming synthetic data in the title. The methods must still describe controlled synthetic perturbations transparently. |
| Abstract | Drafted | Update after subgroup audit and final figures. |
| Research question | Drafted | Focuses on calibration, model-specific CORAL effects and negative transfer under controlled shifts. |
| Related work | Partial | Core references added; complete a reproducible literature search and compare directly with recent domain-adaptation and clinical calibration studies. |
| Dataset provenance | Documented | OpenML 37 v1, 768 rows, eight predictors, 500/268 labels, SHA-256 recorded. Reconfirm source terms and appropriate institutional determination before submission. |
| Nigerian data claim | Correctly excluded | Pima is methodological only. The UITH/Offa-labelled Pima-identical deposit is not independent Nigerian validation. |
| Methods | Drafted | Confirm all hyperparameters, preprocessing, calibration folds, shift formulae and random seeds against the final code release. |
| Baseline results | Verified in run 42464788999 artifact | Five-fold comparison table included. |
| Repeated shift results | Verified in run 42464788999 artifact | 210 evaluations, five seeds; results and paired differences included. |
| TreeSHAP stability | Verified in run 42464788999 artifact | 100 explanations, one seed; RBO table included. |
| Subgroup metrics | Blocked | Latest artifact has no `subgroup_metrics.csv`. Complete the updated audit and inspect denominators and event counts. |
| Paired-bootstrap intervals | Blocked | Latest artifact has no `subgroup_paired_bootstrap.csv`. Complete the updated 1,000-replicate paired bootstrap and verify intervals. |
| Calibration plots | Not prepared | Produce calibration curves with appropriate uncertainty for baseline and selected shift scenarios; include intercept/slope interpretation. |
| Figures | Provisional | Five chart files generated from verified artifact values. Final journal styling and repository/supplementary inclusion remain pending. |
| Tables | Drafted | Baseline, paired AUROC deltas and combined-severe calibration tables included. Reconcile after final audit. |
| Discussion | Drafted | Revisit after subgroup results and calibration figures are final. |
| Limitations | Drafted | Explicitly states no Nigerian cohort, no prospective validation, five overlapping split seeds and no clinical utility evaluation. |
| Reproducibility | Partial | Scripts, protocol and artifact exist. A fresh green workflow on the latest commit and immutable release are required. |
| TRIPOD+AI | Pending | Complete the 27-item reporting checklist and abstract checklist; report missing items rather than imply compliance. |
| PROBAST+AI | Pending | Conduct a structured self-appraisal of model-development and evaluation risk of bias/applicability. |
| Ethics statement | Pending determination | No ethics approval or exemption is claimed. Ask the NAU research ethics process whether a determination is required for this secondary public-dataset analysis. |
| Data availability | Drafted | Link exact OpenML version and repository manifest in final version. |
| Code availability | Drafted | Tag a final release after CI and artifact review. |
| Author list/order | Pending | Confirm contributions and consent. Supervisory status alone does not establish authorship. |
| CRediT contributions | Pending | Obtain each author's agreement to specific roles. |
| Funding/conflicts/acknowledgements | Pending | Obtain declarations from all authors; do not assume no funding or conflicts. |
| Journal selection | Pending | Shortlist journals that accept methodological public-benchmark studies; check external-validation expectations, scope, APCs and reporting policies. |
| Cover letter and submission files | Not started | Prepare only after supervisor approval and final statistical audit. |

## Mandatory release gates

1. Run the CI workflow on the current PR head and obtain green backend, frontend and research jobs.
2. Confirm the two subgroup CSVs exist, are non-empty and pass schema, pairing, denominator, event-count and interval checks.
3. Reconcile the manuscript and benchmark review with the successful run's artifact.
4. Add final calibration figures and verify every plotted value against the artifact.
5. Complete TRIPOD+AI and PROBAST+AI review.
6. Obtain supervisor review and agree author order, contributions and declarations.
7. Select a journal and format the manuscript to its current requirements.

## Separate future Nigerian hospital study

Do not combine the current Paper 1 benchmark findings with a Nigerian hospital external-validation claim. A separate study requires authentic clinical data, hospital and institutional permissions, a data-use agreement, appropriate HREC/ethics review and data-protection safeguards before any patient records are accessed.
