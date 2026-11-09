# Research Gap and Novelty Assessment
**ClinAssist Nigeria**  
**Last updated:** 2026-11-09

> **Authoritative novelty document:** see [`docs/novelty_statement.md`](novelty_statement.md). This file summarises the gap; the novelty statement is binding.

## 1. Primary research question (refined)

Under controlled covariate and missingness shift on a public clinical benchmark, when does unsupervised CORAL adaptation improve or harm discrimination, calibration and selective prediction relative to source-only training, and how stable are local TreeSHAP attributions under perturbation?

## 2. Core literature gap

Unsupervised domain adaptation (including CORAL) is frequently evaluated on discrimination alone. Joint reporting of:

- calibration (Brier, ECE, intercept/slope),
- selective / risk-coverage metrics after adaptation,
- explanation-rank stability,
- and explicit negative or null transfer,

under a leakage-safe, repeated-split protocol on small tabular clinical data remains under-documented.

## 3. What is not claimed

- Novelty of CORAL, SHAP, XGBoost or offline PWAs in isolation.
- Nigerian multi-hospital external validation (data unavailable).
- Clinical deployment readiness or causal feature interpretations.

## 4. Defensible contributions (summary)

**A (primary).** Model- and scenario-stratified evaluation showing CORAL improves discrimination and especially calibration only under selected severe controlled shifts; neutral or adverse under milder/missingness-only conditions.

**B.** TreeSHAP rank stability under controlled perturbation, linked to the same models.

**C.** Provenance-aware separation of synthetic shift from genuine external validation, including documentation of the Mendeley Pima re-packaging.

**D (secondary).** Offline-capable research software stack designed for future authorised multi-site evaluation.

## 5. One-sentence claim

We provide a reproducible, model- and scenario-stratified evaluation showing that unsupervised CORAL adaptation improves discrimination and calibration only under selected severe controlled covariate shifts on a public diabetes benchmark, while remaining neutral or harmful under milder or missingness-only conditions, accompanied by explanation-stability analysis and an offline-capable decision-support system designed for future authorised multi-site evaluation.

See `docs/novelty_statement.md` for full positioning, exclusions, and paper-framing recommendations.
