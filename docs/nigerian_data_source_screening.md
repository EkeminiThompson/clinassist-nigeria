# Nigerian diabetes data-source screening log

**Last reviewed: 2026-11-08. No candidate below is currently accepted as authentic, ethically approved external-validation data.**

| Candidate | Publicly stated information | Verification status | Decision |
|---|---|---|---|
| Mendeley DOI 10.17632/n2fd27pkg9.1, labelled UITH + General Hospital Offa | Claims 800 patients, 768 retained, and eight classic Pima predictors | Repository-level inspection found the released 768-row file identical in schema, row count, class balance and values to the public Pima benchmark; no site identifiers | Reject as Nigerian external validation |
| Mendeley DOI 10.17632/ksdk5m939c.1 | Public description claims 1,500 type-2 diabetes records and nine demographic/clinical fields | Public landing-page description does not establish named recruiting hospitals, patient-level provenance, site labels, diagnostic adjudication, ethics approval, consent/waiver, or data-use permission | Unverified lead only; do not train/evaluate until authors supply documentary provenance and ethics evidence |
| Mendeley DOI 10.17632/hyy9ctvyfd.1 | 158 Lagos tertiary-hospital survey respondents on oral-health seeking behaviour and glycaemic control | Different research question and outcome; not a diabetes diagnostic cohort. Download/secondary-use permissions and variable-level suitability still require review | Not suitable for current diagnostic external validation |
| Federal Ministry of Health Health Partners' Projects & Data Mapping Platform | Research-data user registration and access for legitimate research | Access requires approved account; no specific eligible diabetes dataset confirmed | Explore as a formal institutional route, not as available data |
| Clinical Data Repository (CDR), CIHP | Public site describes a repository spanning 150+ facilities | Login/access restricted; dataset availability, governance, provenance and permission for this project unverified | Explore only through a formal institutional partnership and data agreement |
| ESUTH dataset referenced in prior repository provenance work | A 2023 study was identified | Dataset not accessible to the project; cohort definition, site metadata and permissions not verified | Pending direct author/institutional enquiry |


| Nigeria DHS 2023–24 microdata | National household survey with project-specific access requests; published 2026 analysis uses blood-sugar screening, self-reported diagnosis and treatment indicators among adults aged 15–49 | Useful for population care-cascade context, not a measured-biomarker hospital diagnostic cohort or site-held-out model validation | Request only for contextual epidemiology |
| FMoH HPPDM/PDM platform | Official FMoH DHPRS inventory of projects, datasets and stakeholders; approved research-user registration required for downloads | Formal discovery route; no specific qualifying diabetes dataset confirmed | Register and search NCD/diabetes inventory |
| CIHP Clinical Data Repository | Public site describes a repository spanning 150+ facilities; access requires account | Facility coverage and diabetes variables, provenance, ethics and access conditions not independently verified | Institutional enquiry only |
| Sule Lamido University HISCDR | Public page describes a TETFund-supported clinical data repository | Potential data infrastructure; no diabetes cohort or external access conditions confirmed | Enquiry only |
| DataLens Africa African Patient EHR Dataset | Public page describes Nigeria/Ghana episodes but labels the dataset synthetic/seed-labelled and commercial | Not authentic patient-level external validation | Exclude from clinical validation |
| Zenodo 10.5281/zenodo.19084146 (Turkey EHR diabetes) | Public description claims retrospective data from 30 Istanbul healthcare centres and ethics approval | Possible non-Nigerian transportability comparator; not Nigerian validation; raw file/rights need verification | Optional comparator after file and licence review |

## Verification checklist for any proposed dataset

Before accepting a dataset, obtain and archive in the institution's controlled records:
- Named source hospital(s), departments, collection dates, sampling frame and cohort flow.
- Signed statement from the data custodian or PI confirming the records are genuine observations from those sites and not synthetic, copied, resampled or relabelled benchmark data.
- Original study protocol, ethics committee name, approval/reference number, approval date, approved consent/waiver and evidence that secondary AI use is covered.
- Data-use agreement, licence, controller/processor roles, permitted purposes, retention, transfer and publication conditions.
- Site identifiers or a documented site-level partition key for external validation.
- Outcome definition, measurement units, missingness, exclusion rules, duplicate handling, patient-level de-duplication and codebook.
- Independent provenance checks against the known Pima benchmark and other publicly circulating datasets.

A public repository licence is not proof that the underlying human-subjects collection had valid ethics approval or that a new research purpose is covered. Do not infer Nigerian provenance from a dataset title, author affiliation, or institution named in a description.
