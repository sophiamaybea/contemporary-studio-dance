from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .kinematics import analyse_pose_sequence, indices_from_names


def analyse_npz(path: str | Path, fps: float | None = None) -> dict:
    """Analyse a pose file.

    Expected NPZ fields:
      - positions: [frames, joints, 3]
      - joint_names: [joints]
      - fps: scalar (optional when fps arg is supplied)
    """
    source = Path(path)
    data = np.load(source, allow_pickle=False)

    if "positions" not in data or "joint_names" not in data:
        raise ValueError("NPZ must contain 'positions' and 'joint_names'.")

    actual_fps = fps
    if actual_fps is None:
        if "fps" not in data:
            raise ValueError("Provide fps or include an 'fps' field in the NPZ.")
        actual_fps = float(np.asarray(data["fps"]).reshape(-1)[0])

    positions = np.asarray(data["positions"], dtype=float)
    joint_names = [str(x) for x in np.asarray(data["joint_names"]).tolist()]
    skel = indices_from_names(joint_names)

    metrics = analyse_pose_sequence(positions, float(actual_fps), skel)
    return {
        "source_file": source.name,
        "metrics": metrics,
    }


def write_analysis(
    source: str | Path,
    output: str | Path,
    fps: float | None = None,
) -> Path:
    report = analyse_npz(source, fps=fps)
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return target
