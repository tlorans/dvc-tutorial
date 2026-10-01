# Templates

Files from [DVC in your own project](../docs/3-your-own-project.md), ready
to copy into your own repository. They belong to the invented example project *greenfin-risk*:
rename the pipelines, commands and settings to match yours.

| File | Copy it to | What it is |
|---|---|---|
| `dvc.yaml` | `pipelines\<pipeline>\dvc.yaml` | A full example pipeline: download → prepare → cash flow → valuation → ratings → report → publish |
| `config.yaml` | `pipelines\<pipeline>\config.yaml` | The settings the pipeline depends on, key by key |
| `run.py` | `tools\run.py` | A wrapper that runs DVC for one pipeline at a time (for repositories with several pipelines) |
| `dvc-check.yml` | `.github\workflows\dvc-check.yml` | A GitHub Actions check that pulls the data and fails if a `dvc.lock` is out of date |
| `gitignore.txt` | add the lines to `.gitignore` | Keeps environments and credentials out of git |
| `gitattributes.txt` | add the lines to `.gitattributes` | Stops git on Windows from changing metrics files, so a fresh clone matches `dvc.lock` |
