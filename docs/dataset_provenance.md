# Dataset Provenance and Suitability Report
**ClinAssist Nigeria**  
**Date:** 2026-11-08  
**Status:** Phase 2 complete

## 1. Summary of Findings

| Dataset Candidate | Claimed Source | Actual Content | Hospital Identifiers | Usable for Cross-Hospital DA | Decision |
|-------------------|----------------|----------------|----------------------|------------------------------|----------|
| Mendeley DOI 10.17632/n2fd27pkg9.1 | UITH + General Hospital Offa, Nigeria (800 → 768 records) | Identical to public UCI Pima Indians Diabetes dataset | None | No | **Not usable as Nigerian multi-site data** |
| ESUTH research dataset (2023 paper) | Enugu State University Teaching Hospital | Inaccessible | Unknown | Pending access | Isolated environment reserved |
| Public Pima Indians Diabetes | UCI / National Institute of Diabetes and Digestive and Kidney Diseases | Classic 768 × 9 tabular clinical features | N/A | Benchmark only | **Historical benchmark only** |

## 2. Detailed Inspection – Mendeley Deposit

- File: `diabetes_dataset.csv` (23.3 KB)
- Shape: (768, 9)
- Columns: `Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome`
- Class balance: 268 positive / 500 negative
- Zero counts in physiological fields and summary statistics match the public Pima Indians Diabetes dataset exactly.
- No columns indicating hospital, site, centre, UITH, Offa, or any other stratification variable.
- Licence: CC BY 4.0
- Anonymisation claim is present; no identifiable fields observed.

**Conclusion:** The deposit is a re-packaged version of the well-known public Pima dataset. It cannot support claims of Nigerian multi-hospital domain adaptation.

## 3. Reproducible benchmark retrieval

The repository provides `ml.datasets.download_pima`, which fetches OpenML dataset ID 37, validates the eight expected feature aliases, 768 rows and 500/268 class counts, and writes a local SHA-256 provenance manifest. The CSV is not committed. The benchmark's source population is adult women of Pima heritage; it is not a Nigerian cohort.

## 4. Research Implications

True hospital-level domain adaptation experiments between Nigerian teaching hospitals cannot currently be performed with the available data.  

The project therefore proceeds as a **methodological and systems research contribution**:

1. Rigorous, reproducible experimental pipeline for domain adaptation, uncertainty quantification, missing-data robustness, and explanation stability.
2. Controlled distribution-shift experiments (synthetic and literature-based) on the public benchmark.
3. Fully engineered offline-capable clinical decision support software designed for resource-constrained Nigerian teaching hospital environments.
4. Clear data slots and interfaces ready for future authenticated multi-site Nigerian cohorts (including ESUTH when available).

All experimental results will be explicitly labelled with the data source used. No claim of external clinical validation or real multi-hospital Nigerian performance will be made until verified multi-site data are available.

## 5. Data Governance Rules (Enforced)

- Raw patient-level data are never committed to the public or private GitHub repository.
- Only de-identified, authorised, and properly licensed data may be used for model development.
- Synthetic data (when used) are clearly labelled and never presented as real clinical records.
- Model cards and experiment logs record exact data version, preprocessing, and random seeds.
- The system is intended to support qualified healthcare professionals; it does not diagnose or replace clinical judgment.

## 6. Next Data Actions

1. Continue monitoring for verified multi-site Nigerian diabetes cohorts with hospital identifiers and proper ethics documentation.
2. Maintain an isolated data environment for the original ESUTH research dataset pending access.
3. All current modelling uses only the public Pima dataset as a methodological benchmark.

---
*This document is part of the reproducible research record of ClinAssist Nigeria.*
