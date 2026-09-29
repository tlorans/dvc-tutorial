# Templates

Files from [DVC in your own project](../docs/route-3-3-your-own-project.md), ready
to copy into your own repository. They belong to the invented example project *greenfin-risk*:
rename the pipelines, commands and settings to match yours.

| File | Copy it to | What it is |
|---|---|---|
| `dvc.yaml` | `pipelines\<pipeline>\dvc.yaml` | A full example pipeline: download → prepare → cash flow → valuation → ratings → report → publish |
| `config.yaml` | `pipelines\<pipeline>\config.yaml` | The settings the pipeline depends on, key by key |
| `run.py` | `tools\run.py` | A wrapper that runs DVC for one pipeline at a time (for repositories with several pipelines) |
| `dvc-check.yml` | `.github\workflows\dvc-check.yml` | A GitHub Actions check that pulls the data and fails if a `dvc.lock` is out of date |
| `save-data.ps1` | the root of a data-only repository | Saves a new version of a data file in one command ([Route 2, step 4](../docs/route-2-save-files-with-dvc.md#step-4--every-day-four-things-youll-do)) |
| `gitignore.txt` | add the lines to `.gitignore` | Keeps environments and credentials out of git |
