# Submission metadata and final template instructions

**Repository:** `EkeminiThompson/clinassist-nigeria`

## Associate Editor field

**Author-supplied name:** Dr. Joshua Babatunde Agbogun  
**Institutional profile supplied by author:** Federal University Lokoja, https://fulokoja.edu.ng/staff.php?i=1845&sn=joshua-agbogun

Use this name in the Associate Editor field only if the journal's submission record or editorial office confirms that he is the assigned handling editor for this manuscript. The institutional profile is not, by itself, evidence of an editorial appointment or assignment. Do not place an unconfirmed editor name in the manuscript's author metadata or imply that he has agreed to handle the paper.

Suggested cover-letter salutation once confirmed: `Dear Dr. Agbogun,`

## Computing hardware statement

The research CI workflow is pinned to GitHub-hosted `ubuntu-24.04` (x86-64), with Python 3.11. GitHub documents standard public-repository `ubuntu-24.04` runners as 4 vCPUs and 16 GB RAM. The CI workflow logs the actual CPU model, OS release, kernel and memory for each run.

This describes the CI reproduction environment only. The CPU, RAM and OS for the original reported experiment and the 2026-11-13 independent verification run were not recorded. Do not retrospectively assign CI specifications to those runs. If a later CI run supplies the results used in the final tables, cite that run ID and report the captured hardware from its log.

## ACM author-year bibliography using BibLaTeX

For an ACM venue that explicitly requires author-year references, use the ACM-supported BibLaTeX `acmauthoryear` style. In the `acmart` document class, disable natbib integration, remove any `\citestyle{acmauthoryear}` command, load BibLaTeX with the ACM data model, add the .bib resource, and print the bibliography:

```latex
\documentclass[manuscript,natbib=false]{acmart}

\RequirePackage[
  datamodel=acmdatamodel,
  style=acmauthoryear
]{biblatex}

\addbibresource{references.bib}

\begin{document}

% manuscript content

\printbibliography
\end{document}
```

Do not combine this BibLaTeX setup with the BibTeX commands `\bibliographystyle{ACM-Reference-Format}` or `\bibliography{references}`. Confirm that the target ACM journal or conference actually requires author-year style; most ACM venues default to numeric citations. The final template and journal instructions take precedence.

## Zenodo deposit (optional; not yet deposited)

The repository now includes `CITATION.cff` and `.zenodo.json` as deposit metadata preparation. No Zenodo record or DOI exists yet. To create one, enable the public GitHub repository in Zenodo, create a versioned GitHub release after the final code and experiment artifacts have been checked, and wait for Zenodo to archive the release and issue its DOI. Add the DOI to the manuscript, README and citation metadata only after Zenodo returns it.

The repository's MIT licence covers code only. Dataset and third-party asset rights remain governed by their own terms. Do not upload restricted clinical data or unlicensed third-party datasets to Zenodo.
