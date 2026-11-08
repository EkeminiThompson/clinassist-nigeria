# Clinical governance, ethics and Nigerian data-access plan

**Status: planning document only. No Nigerian patient dataset, institutional permission, ethics approval, or data-use agreement has been obtained.**

## 1. Current evidence boundary

The executable benchmark is OpenML dataset 37 / Pima Indians Diabetes: 768 historical records from a non-Nigerian cohort. It is suitable only for software and methodological benchmarking. It cannot support claims about Nigerian prevalence, clinical performance, fairness across Nigerian populations, or inter-hospital transportability. The repository's provenance review found that a Mendeley deposit labelled as UITH/General Hospital Offa data reproduces the Pima dataset and has no hospital identifiers; it is explicitly excluded as Nigerian external validation.

## 2. Required approvals before any hospital data access

1. Identify a Nigerian principal investigator and clinical co-investigator at each participating site. Obtain written institutional sponsorship and a named data custodian.
2. Submit a complete protocol to the relevant institution's registered Health Research Ethics Committee (HREC). Obtain written approval before recruitment, extraction, transfer, or analysis. Determine whether NHREC-level review or additional regulatory permissions apply to the specific study.
3. Obtain a signed data-use/sharing agreement, controller/processor responsibilities, permitted purpose, retention period, breach process, publication rights, and cross-site transfer terms.
4. Complete a Data Protection Impact Assessment with the institution's Data Protection Officer and confirm the lawful basis under the Nigeria Data Protection Act. Do not assume that de-identification alone removes governance obligations.
5. Obtain consent or a formally documented ethics-approved waiver, as applicable. For retrospective records, the HREC must decide whether waiver criteria are met.
6. Restrict access to an institution-approved secure environment. No patient-level records, row-level extracts, screenshots, or derived identifiable data may be uploaded to GitHub, ChatGPT, public cloud notebooks, or this repository.
7. Maintain a data dictionary, extraction query, provenance record, codebook, data-quality report, and signed approvals in the institution's controlled records system.

## 3. Minimum external-validation data specification

For diabetes risk modelling, the site should supply a documented cohort definition, outcome definition and ascertainment window, index date, eligible adult population, and the predictors that are genuinely available at the intended point of care. Candidate fields include age, pregnancy status/history where clinically justified, glucose/HbA1c, BMI, blood pressure, relevant laboratory values, comorbidities, medication context, and missingness indicators. The clinical team must define units, reference ranges, measurement timing, diagnostic criteria, and exclusions.

Each site should create a random study identifier and retain the re-identification key locally. Prefer site-specific pseudonymous IDs and date offsets where feasible. Site, calendar period, device/laboratory method, and care setting must be retained in a controlled analytical dataset because they are necessary to evaluate transportability; direct identifiers must not enter the modelling extract.

Do not pool incompatible diagnostic definitions or treat a missing test as a negative outcome. Record how labels were established and whether adjudication was blinded to model outputs.

## 4. Prespecified validation design

- Development and tuning must be separated from external evaluation.
- Use a temporal holdout and at least one genuinely independent hospital holdout; do not randomly mix patients from the same site across train and test.
- Prevent patient-level leakage across visits and repeated records.
- Report AUROC, AUPRC with outcome prevalence, sensitivity, specificity, PPV/NPV at clinically selected thresholds, Brier score, calibration intercept/slope and calibration plots.
- Report subgroup metrics only where sample sizes and event counts support meaningful estimation. Prespecify age, sex, pregnancy status if applicable, site, and clinically justified strata; report uncertainty and suppress small cells.
- Evaluate missingness mechanisms, measurement differences, prevalence shift, calibration drift, and negative transfer. Compare source-only, recalibration, and adaptation without target-label leakage.
- Use patient-clustered bootstrap confidence intervals and site-level uncertainty where the number of sites permits. With very few sites, state that site-level generalisation is uncertain.
- Publish a protocol and statistical analysis plan before accessing the held-out labels. Report all planned analyses, including null and harmful adaptation results.

## 5. Governance and deployment gates

No clinical deployment until all gates are signed off:
- HREC approval, institutional permissions, data-use agreement, DPIA and DPO review.
- Clinical safety case, intended-use statement, contraindications, escalation pathway, human oversight and override process.
- External and temporal validation with prespecified acceptance criteria, subgroup safety review and local calibration.
- Independent security assessment, penetration test, access-control review, incident response, backup/restore test, vulnerability management and audit-log retention policy.
- Usability and workflow evaluation with clinicians; training, monitoring, model-change control, rollback and post-deployment surveillance plan.
- Regulatory review to determine whether the intended function and claims trigger medical-device or other applicable requirements.

## 6. Candidate institutional routes to explore

The NHREC public register lists institutional HRECs including University of Nigeria Teaching Hospital (Enugu), Nnamdi Azikiwe (Nnewi), ESUT-related institutions where confirmed by the institution, Federal Medical Centre Bida, Jos University Teaching Hospital, and others. This register is a starting point for verifying the appropriate committee and current registration status, not evidence that any site has agreed to participate.

For a non-LUTH researcher, LUTH's HREC guidance explicitly asks for an institutional collaborator or institutional co-supervisor. The same practical principle should be followed elsewhere: approach a clinical department and research office through a named institutional collaborator rather than requesting raw patient data informally.

## 7. Data leads screened (not approved datasets)\n\nA separate screening log records the candidate Mendeley deposits and the FMOH/CIHP data-access routes. The UITH/Offa-labelled 768-row release is excluded because repository inspection found it to be the Pima benchmark. A separate 1,500-record Mendeley diabetes dataset is an unverified lead: its public description does not establish named hospitals, site labels, ethics approval or secondary-use rights. The FMOH Health Partners' Projects & Data Mapping Platform requires an approved research-user account; no eligible patient-level diabetes cohort has yet been confirmed. These leads must pass the verification checklist in `docs/nigerian_data_source_screening.md` before use.\n\n## 8. Immediate partner-engagement sequence

1. Secure a clinical PI and statistician/epidemiologist.
2. Send a two-page concept note and request a feasibility meeting with the hospital research office/HREC secretariat.
3. Co-design the protocol, cohort definition, data dictionary, and sample-size calculation with the site.
4. Submit ethics and governance documents.
5. Sign the data-use agreement and DPIA; agree secure enclave and access controls.
6. Only after written approvals, receive the minimum necessary pseudonymised extract into the institution-approved environment.

**No data request or transfer should be represented as approved until written institutional and ethics documentation exists.**
