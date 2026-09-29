[Home](../README.md) › Route 3 › Page 1 of 4

# Route 3: Run pipelines — 1. How DVC works

**For you if** you run calculations on data, such as risk models, ratings or scenario analysis,
and you want results you can rebuild exactly, months later.

Route 3 has four pages:

1. **How DVC works** (this page, 10 minutes)
2. [Practice project](route-3-2-practice-project.md) (1 hour)
3. [DVC in your own project](route-3-3-your-own-project.md) (1 hour)
4. [Good habits](route-3-4-good-habits.md) (5 minutes)

**Before you start:** do steps 1 to 6 of [Setup](setup.md). New to git? Also read
[Git and uv basics](git-and-uv-basics.md).

**Used DVC before?** Skim this page and go to the [practice project](route-3-2-practice-project.md).

## The five ideas behind DVC

You only need five ideas to understand DVC.

**1. Git keeps the small files, storage keeps the big ones.**
Code, settings and small summary files live in git. Big data files live in separate storage.
In this tutorial it's Amazon S3, but DVC also works with Azure Blob Storage, Google Cloud Storage,
a network drive and more.

**2. A fingerprint for every file.**
DVC reads each data file and computes a short code from its content, called a *hash*
(DVC uses the MD5 method). It looks like `6645fac464949232a02816779c89ca59`. If even one byte of
the file changes, the hash changes completely. So the hash identifies one exact version of the data.

**3. The recipe: `dvc.yaml`.**
A list of steps, called *stages*. For each stage it says which command to run, what the stage
reads (its *dependencies*), which settings it uses (its *params*) and what it produces (its *outputs*).

**4. The receipt: `dvc.lock`.**
After a run, DVC writes down the hash of every dependency and output. This file is small, so it
lives in git. Checking out an old git commit gives you the old receipt, and the receipt tells DVC
exactly which data to fetch.

**5. Cache and remote.**
On your computer, DVC keeps a copy of each data version in a hidden folder called the *cache*
(`.dvc/cache`). The *remote* is the shared storage (S3) where everyone pushes and pulls these copies.

Here is how the pieces fit:

```mermaid
flowchart LR
    subgraph GIT["git (small text files)"]
        Y[dvc.yaml<br/>the recipe]
        L[dvc.lock<br/>the receipt]
        C[code + settings]
    end
    subgraph PC["your computer"]
        D[data files]
        K[.dvc/cache]
    end
    subgraph S3["remote storage (S3)"]
        R[all data versions]
    end
    L -->|hashes point to| K
    K <-->|dvc push / dvc pull| R
    K -->|dvc checkout| D
```

And here is what happens when you ask DVC to run the pipeline (`dvc repro`):

```mermaid
flowchart LR
    A[Read dvc.yaml] --> B[Hash every dependency<br/>and setting]
    B --> C{Same as<br/>dvc.lock?}
    C -- yes --> S[Skip the stage]
    C -- no --> R[Run the stage]
    R --> W[Write new hashes<br/>to dvc.lock]
```

That second picture is the whole trick. DVC reruns a stage only when something it reads has
changed, and it knows what changed because it compares hashes.

---

[Next: Practice project](route-3-2-practice-project.md) →
