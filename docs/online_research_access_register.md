# Online research and Nigerian data-access register

**Review date: 8 November 2026**  
**Purpose:** Record publicly discoverable data sources, institutional access routes, and named research/ethics contacts for the ClinAssist diabetes-model external-validation study. This register is not evidence of permission to access patient data.

## 1. Data sources and suitability

| Source | What the public record says | Suitability for ClinAssist | Current action |
|---|---|---|---|
| OpenML 37 / Pima Indians Diabetes | 768 historical records; 8 predictors; 500 negative and 268 positive labels | Methodological benchmark only. Historical adult women of Pima heritage; not Nigerian and not hospital external validation | Already retrieved and used in CI experiments |
| Mendeley DOI 10.17632/n2fd27pkg9.1, labelled UITH + General Hospital Offa | Landing page claims 800 Nigerian hospital patients, 768 complete records, and the classic eight Pima predictors | Repository provenance audit found the 768-row release identical to the Pima benchmark in values/schema/class counts and no site IDs. Reject as Nigerian validation pending credible source documentation | Do not use as independent Nigerian cohort |
| Mendeley DOI 10.17632/ksdk5m939c.1, 1,500 records | Landing page lists age, gender, BMI, systolic BP, glucose, HbA1c, family history, hypertension and diabetes status; 820 positive / 680 negative | No named hospitals, collection dates, site identifiers, sampling frame, ethics reference, consent/waiver or data-use permission established by public metadata. Not explicitly identified as Nigerian. The same contributor group is associated with the UITH/Offa-labelled deposit, increasing the need for independent provenance verification | Contact authors for provenance packet; do not train/evaluate as Nigerian data until verified |
| Mendeley DOI 10.17632/hyy9ctvyfd.1 | 158 Lagos tertiary-hospital respondents; oral-health seeking behaviour and glycaemic-control measures among people already living with T2DM | Potentially useful for a separate diabetes-management/complication question, not a diagnostic case/non-case cohort. Secondary-use permission and variable-level data dictionary still need review | Not suitable for current diagnostic external validation |
| Nigeria DHS 2023–24 microdata | National household survey; project-specific dataset access request; recent published analysis uses screening, self-reported diagnosis and treatment indicators in adults aged 15–49 | Useful for population context, care-cascade analysis and subgroup hypotheses. Not a hospital diagnostic cohort and not a replacement for measured diagnostic biomarkers / site-held-out clinical validation | Request access for contextual epidemiology only if needed |
| FMoH Health Partners' Projects & Data Mapping Platform (HPPDM/PDM) | FMoH DHPRS platform inventories health projects, datasets and stakeholders. Dataset download requires a registered data-user account and legitimate research purpose | Best national discovery route for partner-held datasets; no qualifying diabetes cohort has yet been confirmed | Register an institutional research account; search dataset inventory and contact DHPRS about diabetes/NCD datasets |
| CIHP Clinical Data Repository (CDR) | Public site describes a clinical data repository covering 150+ health facilities and requires account access | Potential multi-facility access route; diabetes fields, sites, cohort dates, data controller, ethics status and access eligibility remain unverified | Request institutional collaboration and data dictionary; do not assume diabetes cohort availability |
| Sule Lamido University HIS Clinical Data Repository (HISCDR) | Public site describes a secure clinical data repository developed with collaborators and TETFund support | Potential research infrastructure lead; no public evidence yet of a suitable diabetes cohort or external researcher access | Ask project leadership for site list, diabetes variables, ethics framework and access conditions |
| DataLens Africa African Patient EHR Dataset | Public page describes a 1M+ episode Nigeria/Ghana dataset but labels it synthetic (seed-labelled), commercial licence, access on request | Synthetic data cannot serve as authentic Nigerian patient external validation | Do not use as clinical external validation; possibly consider only for software stress testing if licence permits |
| Turkey EHR diabetes dataset, Zenodo 10.5281/zenodo.19084146 | Public description claims retrospective records from 30 Istanbul healthcare centres, with ethics approval; research-only | Could be a non-Nigerian external transportability comparator if raw files, documentation and licence are verified. It does not establish Nigerian validity | Secondary optional comparator; first verify downloadable contents and usage rights |

## 2. Official Nigerian access routes

### Federal Ministry of Health HPPDM / Data Mapping Platform
- Platform: https://mapping.fmohconnect.gov.ng/
- Research-user registration: https://mapping.fmohconnect.gov.ng/auth/register
- Owner: Department of Health Planning, Research and Statistics (DHPRS), Federal Ministry of Health.
- Registration page states that dataset downloads require an approved PDM data-user account and legitimate research purpose.
- Ask for a catalogue search covering diabetes mellitus, NCDs, HbA1c, fasting/random glucose, outpatient clinics, tertiary hospitals and state-level facility data.
- Treat dataset descriptions as leads only; obtain site-specific custodian confirmation and ethics/DUA documentation.

### NHREC ethics guidance and e-portal
- NHREC registered HREC directory: https://nhrec.gov.ng/registered-ethics-committees/
- NHREC proposal guidance: https://nhrec.gov.ng/services/proposal-guidance/
- NHREC e-portal: https://healthresearchwebafrica.org.za/en/nigeria_nhrec/start
- NHREC contact page: https://nhrec.gov.ng/contact/
- The e-portal describes NHREC submissions for studies involving more than three Nigerian sites and Phase I trials; for a two-site retrospective study, confirm the correct review route with each site's registered HREC and NHREC before submission.
- NHREC guidance offers protocol templates/checklists and pre-submission consultation. Ask for current National Code, multi-site requirements, and whether any additional national review applies.

### Data protection
- Nigeria Data Protection Commission: https://ndpc.gov.ng/
- Nigeria Data Protection Act 2023: https://ndpc.gov.ng/ and official legal publication routes.
- Health data are sensitive personal data. The hospital data controller and DPO must determine lawful basis, DPIA requirements, controller/processor roles, pseudonymisation, retention, transfer and breach controls. This project must not treat public availability or de-identification as blanket permission for a new research purpose.

## 3. Prioritised hospital and collaborator route

### Priority 1 — Federal Medical Centre, Bida (Niger State)
This is the strongest first approach because it is in Niger State and has an established research centre.

**Centre for Health & Allied Researches (CHAR), FMC Bida**
- Official page: https://fmcbida.gov.ng/centre-for-health-allied-researches-char/
- Publicly listed contact: Dr A. O. Adekanye, Director, CHAR FMC Bida.
- Telephone published on official page: 08033840426.
- CHAR describes a multidisciplinary membership across consultants, resident doctors, nurses, health records, administration and laboratory staff, and states that it supports ethically approved research and collaborative research.
- Ask CHAR to identify a consultant physician/endocrinologist or diabetes-clinic lead as clinical PI/co-investigator, plus a records/laboratory custodian and the institutional research approval route.

**FMC Bida HREC**
- NHREC directory entry: contact listed as Sunday Erinle.
- Telephone: 08030664239.
- Email: surubomi@gmail.com.
- Verify contact details and current committee registration directly before sending sensitive protocol materials.

**Hospital context**
- Official FMC Bida overview: https://fmcbida.gov.ng/about-us/
- FMC Bida is a tertiary institution with a stated mandate covering patient care, training, research and community service.
- Its catchment area includes communities across Niger and neighbouring states. This makes it a plausible development-site partner, but not automatically an external-validation site.

### Priority 2 — Nnamdi Azikiwe University Teaching Hospital (NAUTH), Nnewi
- NHREC directory entry: contact listed as Chisolum Okafor.
- Telephone: 08033425656.
- Email: Chisolum2003@yahoo.co.uk.
- This is a candidate independent external-validation site only if a clinical PI, diabetes clinic, suitable retrospective cohort and institutional data governance pathway are confirmed.
- Do not assume an HREC contact is the clinical PI or data custodian.

### Priority 3 — University of Nigeria Teaching Hospital (UNTH), Enugu
- NHREC directory entry lists contact Mazi Oyinba Eze, email mazioyinba@gmail.com.
- Ask the hospital research office for the current HREC secretary/contact, diabetes clinic lead and data custodian; the NHREC public entry does not show a phone number.
- Candidate external site if the cohort and approvals are suitable.

### Additional possible external sites
- University of Ilorin Teaching Hospital (UITH): NHREC directory lists Ahmed Lanre, 081000189920, Lanreporter66@gmail.com. Important: do not treat the Mendeley UITH/Offa-labelled Pima duplicate as hospital evidence.
- University College Hospital (UCH), Ibadan: UI/UCH REC listing includes uiuchec@gmail.com. LUTH is another example of an institution requiring a local collaborator for non-LUTH researchers, but it is not the first choice for a Niger State-led study.

**Contact caution:** The NHREC directory is an official public listing, but contact details can change. Verify them on the institution's current website or through its switchboard before sharing the protocol. Do not email patient records or identifiable information.

## 4. Recommended collaboration design

Preferred route:
1. FMC Bida as the development/clinical partner, with a local consultant physician as PI and CHAR facilitating introductions.
2. NAUTH Nnewi or UNTH Enugu as the independent external-validation site. Select only after the site confirms adequate cohort size, compatible outcome ascertainment, data quality and willingness to participate.
3. If only one site agrees, conduct a properly separated temporal validation at that site and describe it honestly as temporal validation—not multi-hospital external validation.
4. A third site is optional and may trigger NHREC-level multi-site review; confirm the exact review requirement before submission.

Do not request raw patient files at the first contact. First request a feasibility discussion, an aggregate cohort feasibility estimate, data dictionary availability and the institution's formal application process. Aggregate counts should themselves be shared only through an institution-authorised process.

## 5. Data requirements to take into the feasibility meeting

- Adult cohort definition, index date, care setting and calendar range.
- Diabetes outcome definition and adjudication source (e.g. documented diagnosis, laboratory criterion, clinician-confirmed diagnosis); missing outcome is not a negative label.
- Predictors available before or at the intended prediction time: age, sex, BMI, blood pressure, glucose/HbA1c and relevant clinical history.
- Laboratory units, assay/device methods, timing relative to index date, reference ranges and quality-control practices.
- Site, calendar period and care setting fields retained in pseudonymised analytical data for transportability analysis.
- Missingness, exclusions, duplicates, repeat visits, medication status and referral pathway.
- Adequate positive and negative outcome counts for planned analyses; a statistician should calculate sample size and precision before extraction.
- Direct identifiers and re-identification keys remain at source; only approved pseudonymised extracts enter the controlled analysis environment.

## 6. Ethics and privacy sequence

1. Secure institutional clinical PI/co-investigator and data custodian.
2. Complete protocol, scientific rationale, statistical analysis plan, sample-size justification, data dictionary, cohort flow, consent documents or waiver request, and participant-risk assessment.
3. Obtain written permission from each hospital and its relevant registered HREC before extraction or transfer.
4. Confirm whether NHREC review is additionally required for the number/sites and study type.
5. Complete DPIA with the hospital DPO; document lawful basis, purpose limitation, data minimisation, access controls, retention, breach response and any cross-border processing.
6. Sign data-use/sharing agreements with publication rights, controller/processor roles, permitted purpose and secure transfer/storage terms.
7. Extract data inside the institution-approved environment; never place patient-level data in GitHub, ChatGPT, public notebooks or public cloud storage.
8. Freeze protocol, model, thresholds and adaptation rules before external labels are used for final evaluation.

## 7. Immediate enquiries

**FMC Bida CHAR:** Request a 30-minute feasibility meeting and an introduction to a consultant physician/diabetes clinic lead. Ask whether the hospital has an ethically approvable retrospective adult diabetes cohort with glucose/HbA1c, age, BMI, BP and documented diagnosis.

**HPPDM/DHPRS:** Register as an institutional research user and request a catalogue search for diabetes/NCD datasets and data custodians.

**NAUTH / UNTH:** Ask research offices for a clinical co-investigator and confirm whether they can serve as an independent validation site. No patient records should be requested until approvals are established.

**Dataset authors:** Ask the 1,500-record Mendeley dataset authors for hospital/site names, data collection dates, source protocol, ethics committee and approval number, consent/waiver, data dictionary, data-use rights and a signed provenance statement. Compare the actual data file against known public datasets before accepting it.

## 8. Decision rule

A source is accepted as authentic Nigerian clinical validation data only after the project has: (a) named source institution(s), (b) verified data-custodian provenance, (c) ethics approval/waiver and institutional permission, (d) lawful secondary-use rights and DUA, (e) site/time metadata, (f) a documented cohort/outcome/data dictionary, and (g) independent checks against copied or synthetic datasets. A dataset title, Nigerian author affiliation, repository licence or public download link is insufficient.
