[Home](../README.md) › Glossary

# Glossary

| Word | Meaning |
|---|---|
| **Board** | pins: the place where pins are stored, such as a folder in an S3 bucket. |
| **Cache** | The hidden folder (`.dvc/cache`) where DVC keeps a copy of each data version on your computer. |
| **Checkout** | `git checkout` moves code and pointers to a version; `dvc checkout` makes the data match. |
| **Commit** | A named snapshot of the project in git. |
| **Dependency (dep)** | A file or folder a stage reads. If it changes, the stage reruns. |
| **Frozen stage** | A stage `dvc repro` never runs. Useful for publishing. |
| **Hash (MD5)** | A short code computed from a file's content. It changes if one byte changes. |
| **Lock file (`dvc.lock`)** | The receipt: the hashes of every dependency and output of the last run. |
| **Metric** | A small results file kept in git (`cache: false`) so changes show in pull requests. |
| **Output (out)** | A file or folder a stage produces. DVC stores and versions it. |
| **Params** | Settings from a config file that a stage depends on, key by key. |
| **Pin** | pins: a named dataset, kept in versions on a board. |
| **Pipeline** | Stages linked by their dependencies and outputs, described in `dvc.yaml`. |
| **Pull / push** | Get data from / send data to the remote. |
| **Remote** | Shared storage for data versions, such as an S3 bucket. |
| **Repro** | "Reproduce": run every stage whose dependencies changed. |
| **Snapshot date** | A date in the config that pins which version of an external download a stage uses. |
| **Stage** | One step of a pipeline: a command with its dependencies and outputs. |
| **Tag** | A permanent name for a commit, such as a release: `corporate/2026.09`. |
| **Worktree** | A second folder showing another commit of the same git repository. |

---

