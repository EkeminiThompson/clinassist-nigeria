# Research Gap and Novelty Assessment
**ClinAssist Nigeria**  
**Last updated:** 2026-11-08

## 1. Primary Research Question (Refined)

Given the current data reality (no verified multi-hospital Nigerian diabetes cohort with site identifiers is accessible), the research focuses on:

> Can a confidence-aware, missingness-robust domain-adaptation and selective-prediction framework improve the reliability and interpretability of diabetes risk models under controlled distribution shift, while remaining deployable offline in resource-constrained clinical environments?

This is a methodological + systems contribution that is directly transferable to future authentic multi-site Nigerian data.

## 2. Literature Gaps (2020–Nov 2026)

| Gap | Evidence from Literature | Relevance |
|-----|--------------------------|-----------|
| Uncertainty-aware selective prediction under distribution shift for tabular clinical diabetes models | Conformal prediction and selective classification exist, but limited joint evaluation with domain adaptation on small clinical tabular data | High |
| Explanation stability (SHAP consistency) across domain-adapted models | Most XAI work evaluates single models; stability under shift is under-studied | High |
| Missingness-aware domain adaptation for small clinical datasets | DAMS and MNAR methods exist; few practical pipelines for n < 1000 with clinical constraints | Medium-High |
| Offline-first clinical decision support that embeds the above ML components | Offline PWAs exist for African health settings; rarely coupled with rigorous adaptation + uncertainty research | High for systems contribution |
| Evaluations explicitly designed for Nigerian / African teaching-hospital constraints (small n, intermittent connectivity, limited labels) | Most domain-adaptation work uses large US/European EHR | High |

## 3. What Is Not Claimed as Novel

- Using SHAP, XGBoost, or basic domain adaptation techniques in isolation.
- Building a diabetes prediction web application.
- Offline PWA engineering by itself.
- Any performance numbers derived from the re-packaged Pima data presented as Nigerian hospital results.

## 4. Defensible Contribution

A complete, reproducible research software framework that:

1. Implements and comparatively evaluates domain-adaptation methods suitable for small tabular clinical data.
2. Integrates calibrated uncertainty quantification and selective prediction (abstention when uncertainty or shift is high).
3. Quantifies explanation stability under controlled shift.
4. Provides missing-data robustness experiments.
5. Delivers a production-oriented, offline-capable clinical interface designed for Nigerian teaching-hospital infrastructure constraints.
6. Maintains strict provenance, experiment tracking, and data-governance standards so that the same pipeline can be applied to future authenticated multi-site African cohorts without modification of the scientific claims.

## 5. Success Criteria for the Research

- Reproducible experimental results with confidence intervals.
- Clear ablation of each component (adaptation, uncertainty, missingness handling).
- Honest reporting of limitations imposed by current data.
- Working software that can accept new hospital cohorts via a documented interface.
- Documentation and model cards sufficient for independent verification and future clinical evaluation studies.

---
*This assessment will be updated if verified multi-site Nigerian data become available.*
