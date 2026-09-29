[Home](../README.md) › Route 3 › Page 2 of 4

# Route 3: Run pipelines — 2. Practice project

> **Good at git?** Steps 1, 2 and 5 are routine for you: skim them.
>
> **Used DVC before?** Skim everything, but do [Step 8](#step-8--change-a-setting-and-watch-what-reruns)
> and the [exercises](#exercises): they show behaviour people often get wrong.
>
> **New to git?** Do every step, in order. Type the commands yourself rather than copying them.

We will build a small version of what a real risk pipeline does: take market prices, compute a
portfolio's risk, and run a carbon-price stress test on company profits. Everything runs on your
laptop with made-up data, so you can't break anything.

## Step 1 – Copy the practice project and install DVC

Copy the [`practice-project`](../practice-project/) folder of this repository to `C:\dvc-practice`,
outside the company repositories and outside OneDrive.

**In VS Code:** open `C:\dvc-practice` with *File → Open Folder*, then *Terminal → New Terminal*,
and skip the `cd` line below. After `uv venv`, select the `.venv` interpreter as in
[Setup, step 7](setup.md#step-7--optional-use-vs-code).

Then, in PowerShell:

```powershell
cd C:\dvc-practice
uv venv                              # creates a private Python environment in .venv
.venv\Scripts\activate               # turns it on for this terminal
uv pip install -r requirements.txt   # installs DVC, pandas, numpy, pyyaml
dvc --version                        # should print 3.x
```

You should see `(dvc-practice)` or `(.venv)` at the start of your terminal line. That means the
environment is active. If you close the terminal, run the `activate` line again.

If activation fails with "running scripts is disabled on this system", see [Setup, step 6](setup.md#step-6--allow-powershell-to-run-scripts).

## Step 2 – Start git and DVC

```powershell
git init                                           # start a git history in this folder
dvc init                                           # add DVC to it (creates the .dvc folder)
python -c "open('.gitignore','w').write('.venv/\n')"   # tell git to ignore the environment
git add .
git commit -m "Start practice project with DVC"
git branch -M main                                 # name the main line of work "main"
```

`dvc init` created a hidden `.dvc` folder. It holds DVC's settings (`.dvc/config`) and, later,
the cache.

## Step 3 – Put the first version of the data under DVC

Create the input data. In real life this would be a download from a data provider.

```powershell
python make_data.py
```

This writes `data/prices.csv` (250 trading days for five companies) and `data/companies.csv`
(their emissions and profits). Now hand them to DVC:

```powershell
dvc add data/prices.csv data/companies.csv
```

DVC did three things:

1. It computed the hash of each file and copied the files into `.dvc/cache`.
2. It created a small "pointer" file next to each one: `data/prices.csv.dvc` and `data/companies.csv.dvc`.
3. It added the real data files to `data/.gitignore`, so git will never try to store them.

Open `data/prices.csv.dvc` in any text editor. It looks like this:

```yaml
outs:
- md5: 6645fac464949232a02816779c89ca59
  size: 13262
  hash: md5
  path: prices.csv
```

That hash *is* this version of the data, and you should see exactly the same one: the practice
scripts write identical files on every computer. Save the pointers in git:

```powershell
git add data/prices.csv.dvc data/companies.csv.dvc data/.gitignore
git commit -m "Add input data, version 1"
```

> **The key idea:** git now stores a 5-line pointer, not the data. The data itself stays in the
> DVC cache, and later in the remote.

## Step 4 – Set up shared storage and push

In a real project the remote is usually cloud storage, such as an S3 bucket. For practice we use a plain folder next to the
project, so no credentials are needed:

```powershell
dvc remote add -d practice ../dvc-practice-storage   # -d makes it the default remote
git add .dvc/config
git commit -m "Configure practice storage"
dvc push                                             # copies the cache to the remote
```

Look inside `../dvc-practice-storage`: you'll see folders with hash-like names. That's where DVC
keeps every version. In a real project, the same line in `.dvc/config` points to cloud storage, for
example `url = s3://your-company-bucket/dvc-store`. [DVC in your own project](route-3-3-your-own-project.md) shows how to set that up.

## Step 5 – A new data version, and travelling back in time

The data provider sends a refresh with 20 more trading days, including a market sell-off:

```powershell
python make_data.py --update
dvc status
```

`dvc status` tells you that `data/prices.csv` has changed. `data/companies.csv` hasn't: the script
rewrote it with the same content, and DVC compares content, not dates. Record the new version:

```powershell
dvc add data/prices.csv
git add data/prices.csv.dvc
git commit -m "Refresh prices: 20 more trading days"
dvc push
git log --oneline
```

Now go back to version 1 of the prices, without touching anything else:

```powershell
git checkout HEAD~1 -- data/prices.csv.dvc   # the pointer from one commit ago
dvc checkout data/prices.csv.dvc             # make the data match the pointer
python -c "import pandas as pd; print(len(pd.read_csv('data/prices.csv')), 'days')"
```

It prints `250 days`. Come back to the latest version:

```powershell
git checkout HEAD -- data/prices.csv.dvc
dvc checkout data/prices.csv.dvc
python -c "import pandas as pd; print(len(pd.read_csv('data/prices.csv')), 'days')"
```

It prints `270 days`.

> **Remember the pair:** `git checkout` moves the pointers, `dvc checkout` moves the data to match.
> Every time you switch commits or branches, run `dvc checkout` afterwards.

## Step 6 – Your first pipeline stage

So far DVC only stores data. Now let it run calculations too. The first stage turns prices into
daily returns:

```powershell
dvc stage add -n returns `
  -d returns.py -d data/prices.csv `
  -o data/returns.csv `
  python returns.py
```

In PowerShell, a backtick `` ` `` at the very end of a line means "the command continues on the
next line". You can also type it all on one line without the backticks.

Each option means:

| Option | Meaning |
|---|---|
| `-n returns` | the stage's name |
| `-d returns.py -d data/prices.csv` | its dependencies: if either changes, the stage reruns |
| `-o data/returns.csv` | its output: DVC stores and versions it |
| `python returns.py` | the command to run |

This wrote a file called `dvc.yaml`, the recipe. Run it:

```powershell
dvc repro
```

DVC runs the stage and writes `dvc.lock`, the receipt. Open both files and compare: `dvc.yaml`
says *what should happen*, `dvc.lock` records *what did happen*, with hashes.

```powershell
git add dvc.yaml dvc.lock data/.gitignore
git commit -m "Add returns stage"
```

## Step 7 – A pipeline with settings and metrics

Add the two other stages. They read their settings from `params.yaml`, and each writes a small
metrics file:

```powershell
dvc stage add -n risk `
  -d risk.py -d data/returns.csv `
  -p risk `
  -o data/portfolio_returns.csv `
  -M metrics/risk.json `
  python risk.py

dvc stage add -n climate_stress `
  -d climate_stress.py -d data/companies.csv `
  -p scenario `
  -o data/stressed.csv `
  -M metrics/stress.json `
  python climate_stress.py
```

Two new options:

| Option | Meaning |
|---|---|
| `-p risk` | depends on the `risk` section of `params.yaml` only, not the whole file |
| `-M metrics/risk.json` | a metrics file that is **kept in git**, not in the cache, so every change is visible in a pull request |

Your `dvc.yaml` now looks like this. Real projects use exactly the same shape, just with more stages:

```yaml
stages:
  returns:
    cmd: python returns.py
    deps:
    - data/prices.csv
    - returns.py
    outs:
    - data/returns.csv
  risk:
    cmd: python risk.py
    deps:
    - data/returns.csv
    - risk.py
    params:
    - risk
    outs:
    - data/portfolio_returns.csv
    metrics:
    - metrics/risk.json:
        cache: false
  climate_stress:
    cmd: python climate_stress.py
    deps:
    - climate_stress.py
    - data/companies.csv
    params:
    - scenario
    outs:
    - data/stressed.csv
    metrics:
    - metrics/stress.json:
        cache: false
```

Run it and look at the results:

```powershell
dvc repro          # returns is skipped (nothing changed); risk and climate_stress run
dvc dag            # draws the pipeline in the terminal
dvc metrics show   # prints both metrics files as a table
```

You should see a 1-day Value at Risk of 2.177% and, in the stress test, Echo Airlines losing
40.3% of its profit at a carbon price of 85 €/t.

Save everything, including the metrics:

```powershell
git add dvc.yaml dvc.lock metrics data/.gitignore
git commit -m "Add risk and climate stress stages"
dvc push
```

## Step 8 – Change a setting and watch what reruns

This is where DVC saves time. Open `params.yaml` and change the carbon price from `85` to `150`.
Then:

```powershell
dvc status
```

DVC reports that only `climate_stress` is out of date, because only its params section changed.
Run it:

```powershell
dvc repro
```

Only `climate_stress` runs. `returns` and `risk` are skipped. Now compare with the last commit:

```powershell
dvc params diff
dvc metrics diff
```

`dvc metrics diff` prints something like:

```
Path                 Metric                  HEAD    workspace    Change
metrics/stress.json  average_profit_hit_pct  22.9    40.5         17.6
metrics/stress.json  carbon_price_eur        85      150          65
metrics/stress.json  worst_profit_hit_pct    40.3    71.1         30.8
```

In one command you see which setting changed and what it did to the results. Keep it:

```powershell
git add params.yaml dvc.lock metrics
git commit -m "Stress test at 150 EUR/t"
dvc push
```

## Step 9 – Try an idea on a branch

Someone suggests a "greener" portfolio. Try it without disturbing the main line of work:

```powershell
git switch -c greener-portfolio
```

In `params.yaml`, change the weights to: Alpine Steel `0.10`, Blue Wind `0.40`,
Coastal Cement `0.10`, Delta Retail `0.25`, Echo Airlines `0.15`. Then:

```powershell
dvc repro                   # only risk reruns
dvc metrics diff main       # compare with the main branch
```

You'll see the annual volatility fall from 16.2% to 15.0%, but the 1-day VaR rise from 2.18% to
2.30%. Lower volatility, but a worse bad day. That's exactly the kind of finding you want recorded.
If the team likes it, commit and merge the branch. If not, throw it away:

```powershell
git restore .               # undo the uncommitted edits
git switch main
dvc checkout                # data back to main's version
git branch -D greener-portfolio
```

## Step 10 – Be your own colleague

A colleague needs your results. They clone the project and pull the data. Nothing is recomputed:

```powershell
cd C:\
git clone dvc-practice dvc-practice-colleague
cd dvc-practice-colleague
uv venv
.venv\Scripts\activate
uv pip install -r requirements.txt
dvc pull                             # fetches every file the receipt names
dvc status                           # "Data and pipelines are up to date."
```

The colleague now has exactly your data, byte for byte. This is how teams share
results: one person runs the pipeline and pushes, everyone else pulls.

## Exercises

Try each one before opening the answer.

<details>
<summary><b>1.</b> You change <code>confidence</code> in <code>params.yaml</code> from 0.99 to 0.95. Which stages rerun?</summary>

Only `risk`, because only it depends on the `risk` section. The 1-day VaR drops, since a 95% VaR
looks at a less extreme day than a 99% VaR.
</details>

<details>
<summary><b>2.</b> You add a comment line to <code>returns.py</code>. Which stages rerun?</summary>

`returns` reruns, because its code changed. But `risk` is **skipped**: `returns.py` produced exactly
the same `data/returns.csv` as before, so its hash is unchanged. DVC follows content, not
timestamps. This surprises many people, and it is one of DVC's biggest time savers.
</details>

<details>
<summary><b>3.</b> You need the version-1 prices as a separate file, without changing your workspace. How?</summary>

Find the commit with `git log --oneline` (the one named "Add input data, version 1"), then:

```powershell
dvc get . data/prices.csv --rev <commit-id> -o prices_v1.csv
```

`dvc get` downloads one file at one version. It also works with a GitHub URL instead of `.`,
which is useful for people who don't want to clone a whole repository.
</details>

<details>
<summary><b>4.</b> A colleague runs <code>dvc pull</code> and gets "missing cache" errors. What happened?</summary>

You committed the receipt (`dvc.lock` or a `.dvc` file) but forgot `dvc push`. The receipt points
to data that isn't on the remote yet. Run `dvc push` and ask them to pull again.
</details>

<details>
<summary><b>5.</b> Someone edits <code>data/returns.csv</code> by hand. What does <code>dvc status</code> say, and how do you fix it?</summary>

It reports that the output of `returns` was modified. Never keep hand edits to outputs.
`dvc checkout data/returns.csv` restores the recorded version, or `dvc repro --force returns`
recomputes it.
</details>

---

← [Previous: How DVC works](route-3-1-how-dvc-works.md) · [Next: DVC in your own project](route-3-3-your-own-project.md) →
