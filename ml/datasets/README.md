# Benchmark dataset setup

The Pima Indians Diabetes CSV is intentionally not committed in this repository. Obtain the permitted public dataset from its authoritative source, verify its provenance and license, and place the CSV at `ml/datasets/diabetes_dataset.csv` with the expected columns: `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`, `Outcome`.

The prediction service cannot train its baseline until this file is supplied. The repository does not generate synthetic patient records or silently substitute another dataset. In CI, inference tests are skipped when the benchmark CSV is absent; all other unit and import checks still run.
