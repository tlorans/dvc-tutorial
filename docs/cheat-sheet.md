[Home](../README.md) › Cheat sheet

# Cheat sheet

*The commands of every route, on one page.*

## Route 1: Save file versions, no git

| Task | Code |
|---|---|
| Get the latest version | `board.pin_download("<name>")` |
| Save a new version | `board.pin_upload("<file>", name="<name>", title="<message>")` |
| See the history | `board.pin_versions("<name>")` |
| Get an old version | `board.pin_download("<name>", version="<version-id>")` |

## Route 2: Save file versions with DVC

| Task | Command |
|---|---|
| Get the latest versions | `git pull`, then `uv run dvc pull` |
| Save a new version | `.\save-data.ps1 <file> "<message>"` |
| See the history of a file | `git log --oneline -- <file>.dvc` |
| Get an old version as a new file | `uv run dvc get . <file> --rev <id> -o <new name>` |

## Route 3: Run pipelines

| Task | Command |
|---|---|
| Start DVC in a git repository | `dvc init` |
| Version a data file | `dvc add <file>`, then `git add <file>.dvc` and commit |
| Add a pipeline stage | `dvc stage add -n <name> -d <dep> -p <params> -o <out> -M <metric> <command>` |
| Run what changed | `dvc repro` |
| What is out of date | `dvc status` |
| Draw the pipeline | `dvc dag` |
| Compare settings / results | `dvc params diff`, `dvc metrics diff [branch]` |
| Send / get data | `dvc push`, `dvc pull` |
| Make data match the current commit | `dvc checkout` |
| Download one file at one version | `dvc get <repo> <path> --rev <tag or commit>` |

### Setting up storage

| Task | Command |
|---|---|
| Add a remote (default) | `dvc remote add -d <name> s3://<bucket>/<folder>` |
| Add a remote (not default) | `dvc remote add <name> s3://<bucket>/<folder>` |
| Set its region | `dvc remote modify <name> region <region>` |
| Use your AWS profile, outside git | `dvc remote modify --local <name> profile <profile>` |

### With the wrapper (several pipelines in one repository)

| Task | Command |
|---|---|
| Latest results | `uv run tools/run.py <pipeline> pull` |
| What is out of date | `uv run tools/run.py <pipeline> status` |
| What would rerun | `uv run tools/run.py <pipeline> dry` |
| Run | `uv run tools/run.py <pipeline> repro` |
| Share results | `uv run tools/run.py <pipeline> push` |
| Old release in its own folder | `git worktree add ..\<folder> <tag>`, then `pull` there |

---

