"""Run DVC for one pipeline, always in the right folder, with the right file and remote.

Usage (from the repository root):

    uv run tools/run.py <pipeline> <action>

    uv run tools/run.py corporate status
    uv run tools/run.py project_finance repro

Actions: status, dry, repro, pull, push.

Why a wrapper? When a repository holds several pipelines, a bare `dvc repro` at the root runs all
of them, and a bare `dvc push` can send one pipeline's data to another pipeline's storage. This
script always picks exactly one pipeline, its own dvc.yaml and its own remote.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# One entry per pipeline folder under pipelines/. The remote has the same name as the pipeline.
PIPELINES = ["corporate", "project_finance"]

ACTIONS = {
    "status": ["status"],
    "dry": ["repro", "--dry"],
    "repro": ["repro"],
    "pull": ["pull", "--remote", "{pipeline}"],
    "push": ["push", "--remote", "{pipeline}"],
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in PIPELINES or sys.argv[2] not in ACTIONS:
        print(__doc__)
        print("Pipelines:", ", ".join(PIPELINES))
        return 2

    pipeline, action = sys.argv[1], sys.argv[2]
    folder = ROOT / "pipelines" / pipeline
    command = ["dvc", *[part.format(pipeline=pipeline) for part in ACTIONS[action]], "dvc.yaml"]

    print(f"[{pipeline}] {' '.join(command)}")
    return subprocess.call(command, cwd=folder)


if __name__ == "__main__":
    sys.exit(main())
