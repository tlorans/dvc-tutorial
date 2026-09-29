[Home](../README.md) › Route 1

# Route 1: Save file versions, no git

**For you if** you want to keep versions of files without learning git or DVC. You write a few
lines of Python.

**Before you start:** do steps 1 to 4 of [Setup](setup.md). About 15 minutes.

**Time for this page:** about 30 minutes.

## Step 1 – How it works

This route uses **pins**, a free, open-source Python package. It needs no git, no DVC, no server
and no web interface.

Two words are enough:

- A **pin** is a named dataset, such as `client-portfolio`. It can be any file, like an Excel
  workbook, or a table saved from Python.
- A **board** is the place where pins are stored: here, a folder in your team's S3 bucket.

Every time you save a pin, pins keeps it as a **new version**, with the date, a fingerprint of the
content, and a title and details you add. Old versions are never overwritten, so you can always
get them back.

## Step 2 – Set up (once per person)

**1. Your storage keys.** Store them under the `team` profile, as in [Setup, step 4](setup.md#step-4--store-your-storage-keys).
Ask your team lead which bucket and folder the team uses.

**2. A folder for your scripts, with pins installed:**

```powershell
mkdir C:\projects\my-data
cd C:\projects\my-data
uv init --bare
uv add pins s3fs
```

You run your scripts with `uv run python <script>.py`, and uv makes sure pins is there. If you
already have a Python project, just run `uv add pins s3fs` inside it.

## Step 3 – Connect to the board

Save these lines as `connect.py` in your folder. Every script then starts with
`from connect import board`, and everyone on the team uses the same file.

```python
# connect.py
import os

import pins

os.environ["AWS_PROFILE"] = "team"
board = pins.board_s3("your-company-bucket/team-inputs", versioned=True)
```

## Step 4 – Every day: four things you'll do

```python
from connect import board

# 1. Get the latest version: gives back the path of a local copy
path = board.pin_download("client-portfolio")

# 2. Save a new version, with a title and some details
board.pin_upload("C:/data/client-portfolio.xlsx", name="client-portfolio",
                 title="Client portfolio, September 2026",
                 metadata={"month": "2026-09", "source": "Client X"})

# 3. See the history: version ID, date and fingerprint of every saved version
print(board.pin_versions("client-portfolio"))

# 4. Get an old version, by its version ID from step 3
path_august = board.pin_download("client-portfolio", version="<version-id>")
```

Put the lines you need in a script, for example `save_portfolio.py`, and run it:

```powershell
uv run python save_portfolio.py
```

They also work in a Jupyter notebook, or in VS Code's interactive window.

## Good to know

- **`pin_download` gives back the path of a local copy**, kept in a cache folder. Open it, read it
  with pandas, or copy it elsewhere, but don't edit it in place: save changes as a new version with
  `pin_upload`.
- **Saving a table from pandas?** Save the data frame directly with `board.pin_write(df, name="...", type="parquet")`
  and read it back with `board.pin_read("...")`. No file needed in between.
- **Versions add up over time.** `board.pin_versions_prune("<name>", n=24)` keeps only the last 24.
  Agree as a team before anyone runs it.

## When to move to DVC instead

pins is enough for many teams. Move to [Route 2](route-2-save-files-with-dvc.md) (DVC) when:

- colleagues who don't write Python need to save and get files too,
- you want each version tied to a commit, reviewed in a pull request, like the rest of your work,
- or the work grows into calculations that should rerun when data changes. Then go to
  [Route 3](route-3-1-how-dvc-works.md).

pins is actively developed, so check its current documentation for the exact function options
before you rely on them.

## You've finished

- Keep the [cheat sheet](cheat-sheet.md) at hand: this route fits in four lines.
- If something goes wrong, see [When something goes wrong](troubleshooting.md).

---

