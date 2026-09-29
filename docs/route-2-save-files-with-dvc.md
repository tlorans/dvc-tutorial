[Home](../README.md) › Route 2

# Route 2: Save file versions with DVC

**For you if** you want to keep versions of files and don't mind a little git. No coding needed:
a script does most of the work.

**Before you start:** do steps 1 to 6 of [Setup](setup.md). New to git? Also read
[Git and uv basics](git-and-uv-basics.md).

**Time for this page:** about 30 minutes.

> **Want no git at all, and happy to write a few lines of Python?** [Route 1](route-1-save-files-no-git.md) is simpler for you.

## Step 1 – How it works

The simplest tool for this is **DVC without a pipeline**, called "data only" in this tutorial.

DVC stores your files in shared storage, here an S3 bucket, and git stores a tiny note for each
file saying which version is current. Every time you save a new version, the note changes, so
git's history becomes the history of your files.

Why DVC and not something else:

- **Four everyday tasks cover all you do**, and a small script turns saving into one command.
- **It uses the storage you already have.** No server to install.
- **Every version is kept and named**, with who saved it, when, and a message saying why.
- **It's the same tool as the pipelines route**, so if your work grows into calculations, you already know it.

## Step 2 – Set up the repository (once per team)

> **New to git?** Ask a colleague who is good at git to do this step for you, then go to [step 3](#step-3--your-own-setup-once-per-person).
>
> **Good at git?** This step is for you. You do it once, for the whole team.

Create a small repository just for the data, for example `team-inputs`, with one folder per kind
of file:

```
C:\projects\team-inputs\
├── inputs\
│   ├── client-portfolio.xlsx
│   └── sector-mapping.xlsx
├── save-data.ps1
└── pyproject.toml
```

Create an empty repository on GitHub, then add DVC and connect the storage. Ask your cloud
administrator for an S3 bucket, or a folder in one, with read/write access for the team:

```powershell
cd C:\projects
git clone <repository-url> team-inputs
cd team-inputs
uv init --bare
uv add "dvc[s3]"
uv run dvc init
uv run dvc remote add -d storage s3://your-company-bucket/team-inputs
python -c "open('.gitignore','w').write('.venv/\n.env\n')"   # keep these out of git
git add .
git commit -m "Set up DVC for team inputs"
git push
```

Copy [`templates/save-data.ps1`](../templates/save-data.ps1) into the repository and commit it too.
Then put the first files in `inputs\` and save each one with the script, as shown in [step 4](#step-4--every-day-four-things-youll-do).

## Step 3 – Your own setup (once per person)

You need your storage keys stored under a profile first ([Setup, step 4](setup.md#step-4--store-your-storage-keys)).
Then get the repository and the files:

```powershell
cd C:\projects
git clone <repository-url> team-inputs
cd team-inputs
uv sync
uv run dvc remote modify --local storage profile team
uv run dvc pull
```

The `remote modify --local` line tells DVC to use your `team` profile. `--local` keeps this in a
settings file that git ignores, so each person uses their own keys.

## Step 4 – Every day: four things you'll do

**1. Get the latest versions.** Close Excel first, then:

```powershell
git pull
uv run dvc pull
```

**In VS Code:** click **Sync Changes** in Source Control, then run **DVC: Pull** from the Command Palette.

**2. Save a new version.** Put the new file in place of the old one, **with the same name**.
Don't rename it: the history keeps the old versions for you. Then:

```powershell
.\save-data.ps1 inputs\client-portfolio.xlsx "Client portfolio, September 2026"
```

The script stops at the first problem, so nothing is ever half-saved. If PowerShell refuses to
run it, see [Setup, step 6](setup.md#step-6--allow-powershell-to-run-scripts). If you copied it from a downloaded zip
file, run `Unblock-File .\save-data.ps1` once.

**In VS Code:** run the script in VS Code's terminal. Afterwards, the Source Control panel should
show no changes left: that's a quick check that everything was saved and pushed.

> **Good at git?** The script just runs these five commands, which you can also type yourself:
>
> ```powershell
> uv run dvc add inputs\client-portfolio.xlsx
> git add inputs\client-portfolio.xlsx.dvc inputs\.gitignore
> git commit -m "Client portfolio, September 2026"
> uv run dvc push
> git push
> ```

**3. See the history of a file.**

```powershell
git log --oneline -- inputs\client-portfolio.xlsx.dvc
```

**In VS Code:** select `client-portfolio.xlsx.dvc` in the Explorer and look at the Timeline view.

Each line is one saved version, with its ID and your message:

```
a41c9e2 Client portfolio, September 2026
7d0b513 Client portfolio, August 2026
c9e8f07 Client portfolio, July 2026
```

**4. Get an old version, as a separate file.** Take the ID from the history:

```powershell
uv run dvc get . inputs/client-portfolio.xlsx --rev 7d0b513 -o client-portfolio-august.xlsx
```

Your current files are not touched. You get a new file, `client-portfolio-august.xlsx`, with
exactly what was saved in August.

That's all: these four tasks are everything this route needs.

## You've finished

- Keep the [cheat sheet](cheat-sheet.md) at hand: this route fits in four lines.
- If something goes wrong, see [When something goes wrong](troubleshooting.md).
- If your work grows into calculations, continue with [Route 3](route-3-1-how-dvc-works.md). You
  already know half of it.

---

