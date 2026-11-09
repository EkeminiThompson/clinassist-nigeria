# Novelty Statement — ClinAssist Nigeria

**Document status:** Formal research novelty assessment  
**Date:** 2026-11-09  
**Scope:** Methodological contribution under current data constraints (public Pima benchmark + controlled synthetic shift). No claim of Nigerian multi-hospital external validation.

---

## 1. What is *not* novel (explicit exclusions)

The following are **not** claimed as original contributions:

- Application of CORAL, logistic regression, random forest, XGBoost, or SHAP in isolation.
- Construction of a diabetes prediction web application or offline PWA by itself.
- Any performance number obtained on the public Pima Indians Diabetes dataset presented as Nigerian hospital or African multi-site performance.
- Claims of clinical validation, prospective utility, or fairness for Nigerian patients.
- Invention of a new deep domain-adaptation architecture.

These exclusions are deliberate. Over-claiming any of the above would be scientifically false.

---

## 2. Primary research gap addressed

Most evaluations of unsupervised domain adaptation (including CORAL) on tabular clinical or biomedical data report **discrimination** (AUROC / accuracy / F1). Far fewer jointly report:

1. **Calibration** (Brier, ECE, calibration intercept/slope) under the same controlled shifts,
2. **Selective prediction / risk-coverage** behaviour after adaptation,
3. **Explanation stability** (local TreeSHAP rank consistency) under perturbation,
4. Explicit documentation of **negative or null transfer** (when adaptation harms or does nothing),
5. A leakage-safe, fully reproducible protocol that separates *controlled synthetic shift* from *genuine external validation*.

Literature confirms CORAL is established for covariance alignment. Calibration under distribution shift is an active concern in clinical ML, but the joint, model-stratified, scenario-stratified evaluation of CORAL’s effect on *both* discrimination *and* calibration, together with selective metrics and explanation stability, on a small tabular clinical benchmark with fully transparent negative results, remains under-documented.

---

## 3. Defensible novel contributions

### Contribution A — Joint discrimination–calibration–selective evaluation of unsupervised adaptation under controlled shift (primary)

A prespecified, repeated-split experimental protocol that compares source-only training versus CORAL across multiple model classes (logistic regression, random forest, histogram gradient boosting) and a grid of covariate-shift and missingness scenarios, reporting:

- AUROC, AUPRC
- Brier score, ECE, calibration intercept/slope
- Selective (entropy-ranked) metrics at fixed coverage
- Paired within-split bootstrap intervals for adaptation deltas

**Key empirical finding (already obtained):** CORAL’s benefit is **model- and scenario-dependent**. Under severe controlled covariate shift (and combined severe shift + MAR-like missingness) it improves AUROC for tree ensembles and substantially reduces Brier/ECE; under reference and missingness-only scenarios the effect is negligible or occasionally adverse. This pattern of *conditional* benefit, including explicit negative/null results, is itself a contribution to realistic assessment of unsupervised adaptation.

### Contribution B — Local explanation stability under controlled perturbation

Quantification of TreeSHAP feature-rank stability (rank-biased overlap) under standardised input perturbations at multiple noise levels, for the same models used in the adaptation study. This treats explanation stability as a sensitivity analysis, not as causal or clinical validation.

### Contribution C — Auditable separation of synthetic shift from external validation

An explicit research and software architecture that:

- Treats the public Pima dataset strictly as a methodological benchmark,
- Documents the provenance failure of the Mendeley “UITH/Offa” deposit,
- Reserves a clean data interface for future authorised multi-site Nigerian cohorts,
- Prevents synthetic-shift results from being misread as Nigerian external validation.

This governance contribution is unusual in applied clinical ML repositories and is required for scientific integrity given the data history of the project.

### Contribution D — Integrated research software system (secondary, systems contribution)

A working, offline-capable clinical decision-support stack (FastAPI + auth/RBAC + sync + React/Ant Design PWA) that embeds the above evaluation components, uncertainty reporting, and clinical disclaimers. The systems contribution is secondary to the methodological one and is positioned as infrastructure for future prospective evaluation, not as evidence of current clinical validity.

---

## 4. Positioning relative to closest prior work

| Prior theme | Typical focus | Differentiation of this work |
|-------------|---------------|------------------------------|
| CORAL / Deep CORAL applications | Accuracy or F1 under domain shift | Joint calibration + selective metrics + explicit negative transfer |
| Clinical calibration literature | Post-hoc calibration or single-domain ECE | Calibration *under controlled adaptation* |
| Selective classification / conformal | Safety under i.i.d. or known shifts | Selective metrics reported *after* unsupervised adaptation |
| SHAP stability studies | Perturbation sensitivity of attributions | Linked to the same models and shift protocol used for adaptation |
| Offline African health software | Engineering / usability | Coupled to a rigorous, provenance-aware ML evaluation pipeline |

No single prior study is known to combine all four elements (A–D) under the same transparent data and governance constraints.

---

## 5. What would strengthen novelty further (future work)

True multi-site Nigerian hospital data with site identifiers and ethics approval would convert Contribution A from a controlled-benchmark result into an external-validation result. Until that data exist, the novelty remains methodological and must be stated as such.

Additional strengtheners:
- Formal statistical comparison of calibration slopes under adaptation,
- Comparison against alternative adaptation methods (e.g., importance weighting, simple fine-tuning with limited labels),
- Prospective clinician-facing evaluation of the selective-prediction interface.

---

## 6. One-sentence claim suitable for abstract / contribution list

> We provide a reproducible, model- and scenario-stratified evaluation showing that unsupervised CORAL adaptation improves discrimination and calibration only under selected severe controlled covariate shifts on a public diabetes benchmark, while remaining neutral or harmful under milder or missingness-only conditions, accompanied by explanation-stability analysis and an offline-capable decision-support system designed for future authorised multi-site evaluation.

This claim is fully supported by the experiments and documentation already in the repository. It does not require Nigerian hospital data to be true, and it does not overstate clinical readiness.

---

## 7. Recommendation for paper framing

**Recommended primary framing:** Methodological study of calibration and domain adaptation under controlled distribution shift, using a public clinical benchmark, with transparent negative results and software infrastructure for future external validation.

**Avoid:** Any language that implies Nigerian multi-hospital validation, clinical deployment readiness, or universal superiority of CORAL.

**Emphasise:** Conditional benefit, joint metric reporting, explanation sensitivity, and data-governance discipline.

---

*This statement is the authoritative novelty assessment for ClinAssist Nigeria as of 2026-11-09.*
