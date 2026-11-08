# Benchmark dataset setup

The raw benchmark is deliberately not committed to Git. To fetch OpenML dataset 37 and validate the expected Pima schema, sample count and class balance:

```bash
PYTHONPATH=. python -m ml.datasets.download_pima
```

The script writes `diabetes_dataset.csv` and `pima_manifest.json` locally. The manifest records OpenML dataset/version metadata, retrieval time, class counts and a SHA-256 checksum. Review the upstream dataset terms and retain the manifest with any experiment archive. If the upstream schema or counts change, the script stops rather than silently accepting a different dataset.

The Pima cohort comprises adult women of Pima heritage. It is a historical methodological benchmark only, not a representative Nigerian cohort or external validation dataset. Never describe synthetic shift experiments as Nigerian clinical validation.
