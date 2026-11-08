# Concept note: Nigerian multi-site external validation of ClinAssist diabetes prediction

**Working title:** External Validation and Unsupervised Domain Adaptation of Diabetes Prediction Models Across Nigerian Secondary and Tertiary Hospitals

**Status:** Draft for discussion with a Nigerian clinical principal investigator. This is not an approved study protocol and does not request patient records before ethics and institutional approvals.

## Background and rationale

Clinical prediction models trained on non-Nigerian datasets may be miscalibrated when transported to Nigerian hospitals because of differences in patient populations, disease prevalence, measurement methods, referral patterns, missingness and clinical workflows. The current ClinAssist research prototype uses the historical Pima Indians Diabetes benchmark and has no verified Nigerian external validation. A genuine multi-site study is required before any claim of local clinical validity can be made.

## Aim

To evaluate the transportability, calibration, subgroup performance and explanation stability of diabetes prediction models across independent Nigerian hospital cohorts, and to determine whether unsupervised domain adaptation improves performance without unacceptable negative transfer.

## Proposed objectives

1. Establish a retrospective, provenance-verified cohort at a development site and at least one independent external-validation site.
2. Compare a prespecified source-only baseline with local recalibration and unsupervised CORAL adaptation using target covariates only.
3. Quantify discrimination, calibration, clinical operating characteristics and selective prediction under temporal and site shift.
4. Evaluate subgroup performance by clinically justified demographic and clinical strata, subject to adequate sample and event counts.
5. Assess missingness patterns, laboratory/measurement differences, explanation stability and the effect of adaptation on each site.
6. Produce a reproducible, privacy-preserving validation report and a clinical safety case before considering any deployment.

## Study design

A retrospective, multi-site observational model-validation study, with a prespecified temporal split at the development site and a site-held-out external test cohort. Patient-level identifiers must be deduplicated across visits and sites. The final protocol, sample-size calculation, analysis plan and subgroup definitions will be co-developed with the clinical PI, statistician and participating HRECs before data extraction.

## Candidate cohort and data elements

The clinical team will define eligibility, index date, follow-up window and outcome ascertainment using the hospitals' adopted diagnostic guidance. The proposed minimum predictor compatibility set is age, pregnancy history where clinically relevant, glucose, blood pressure, skinfold thickness, insulin, BMI and diabetes pedigree/family-history information. Additional locally available variables—such as HbA1c, fasting glucose, sex, medication history, hypertension and comorbidities—should be recorded where permitted, but the model's input set must be frozen before external evaluation.

Required metadata include site code, calendar period, measurement units, assay/device method, care setting, missingness indicators and outcome source. Missing outcomes must not be labelled as negative. The PI and HREC must approve the use of retrospective records and determine consent or waiver requirements.

## Analysis overview

- Freeze model code, preprocessing and thresholds before the external labels are unblinded.
- Report AUROC and AUPRC alongside prevalence; sensitivity, specificity, PPV and NPV at prespecified thresholds; Brier score, calibration intercept/slope and calibration plots.
- Compare source-only, local recalibration and unsupervised adaptation; use target covariates only for adaptation and reserve target labels for final evaluation.
- Report negative transfer and site-specific outcomes explicitly.
- Use patient-clustered bootstrap intervals and site/temporal holdouts; do not treat repeated random splits as independent cohorts.
- Conduct subgroup analyses only where event counts support stable estimates; disclose sparse strata and avoid unsupported fairness claims.
- Report all deviations from the prespecified protocol and all null or harmful findings.

## Ethics, privacy and data security

No data will be extracted, transferred or analysed until the participating institution(s) provide written permission, the relevant registered HREC(s) issue approval, the lawful basis and consent/waiver are documented, a DPIA is completed with the DPO, and a data-use/sharing agreement is executed. Direct identifiers and re-identification keys remain at the source hospital. Analysis will occur in an institution-approved secure environment; no patient-level data will be committed to GitHub or transferred to public cloud workspaces.

## Initial Nigerian institutional pathway

Federal Medical Centre Bida is the proposed first development-site approach because its official Centre for Health & Allied Researches (CHAR) describes a multidisciplinary research collaboration structure. The published CHAR contact is Dr A. O. Adekanye, Director, CHAR FMC Bida (08033840426). FMC Bida's Internal Medicine department lists an Endocrinology unit, its specialty schedule lists a Gastro-Endocrine Clinic on Thursdays (8:00 am–12:00 noon), and its Family Medicine service lists an NCD clinic on Tuesdays (8:00 am–2:00 pm). The official consultants directory lists Dr Olajide Olayode O. under Internal Medicine (olajideolayode@gmail.com; o.olajide@fmcbida.org; 07031084451), but does not identify an endocrinology subspecialty; ask CHAR to route the enquiry to the appropriate endocrine consultant rather than presuming he is the PI. The NHREC public directory lists an FMC Bida HREC contact (Sunday Erinle; 08030664239; surubomi@gmail.com); verify current committee contacts and review route with the hospital before submission.

Potential independent validation sites to approach after the development-site PI is secured include NAUTH Nnewi and UNTH Enugu. Their current HREC contacts are listed in the NHREC registered-committee directory, but those HREC contacts are not substitutes for a clinical PI or hospital data custodian. UITH may also be considered only after the previously identified Pima-duplicate Mendeley deposit is excluded and a genuine site cohort is independently verified.

The FMoH Health Partners' Projects & Data Mapping Platform is a parallel route for identifying partner-held datasets. A project-specific approved research-user account is required; no diabetes cohort is assumed available.

## Requested collaboration

We seek a named clinical PI/co-investigator, access to the hospital research office and HREC process, a data custodian, and a feasibility discussion about a de-identified retrospective cohort. The first meeting should determine whether the cohort, variables, outcome definitions, ethics route and data governance requirements are feasible. No commitment to release data is assumed.

## Expected outputs

1. Approved protocol and statistical analysis plan.
2. Data dictionary, cohort-flow and data-quality report.
3. Site-held-out external-validation results with calibration and subgroup uncertainty.
4. Reproducible code and synthetic/public benchmark artefacts without patient-level records.
5. Clinical safety and governance report describing whether the model should remain research-only.

**Contact/PI details:** To be completed by the institutional research lead before submission.
