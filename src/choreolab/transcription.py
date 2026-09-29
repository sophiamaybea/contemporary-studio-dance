from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np


@dataclass(frozen=True)
class FidelityWeights:
    pose: float = 0.18
    velocity: float = 0.20
    acceleration: float = 0.18
    root_trajectory: float = 0.16
    contact: float = 0.12
    phase: float = 0.07
    facing: float = 0.05
    level: float = 0.04


def finite_difference(x: np.ndarray, fps: float, order: int = 1) -> np.ndarray:
    out = np.asarray(x, dtype=float)
    if fps <= 0:
        raise ValueError("fps must be positive")
    for _ in range(order):
        if len(out) < 2:
            return np.zeros_like(out)
        out = np.gradient(out, axis=0) * fps
    return out


def mse(a: np.ndarray, b: np.ndarray) -> float:
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    if aa.shape != bb.shape:
        raise ValueError("arrays must have identical shapes")
    return float(np.mean(np.square(aa - bb)))


def binary_contact_loss(a: np.ndarray, b: np.ndarray) -> float:
    aa = np.asarray(a).astype(bool)
    bb = np.asarray(b).astype(bool)
    if aa.shape != bb.shape:
        raise ValueError("contact arrays must have identical shapes")
    return float(np.mean(np.logical_xor(aa, bb)))


def repair_mask(confidence: np.ndarray, threshold: float = 0.55) -> np.ndarray:
    c = np.asarray(confidence, dtype=float)
    return c < threshold


def source_fidelity_losses(
    *,
    source_pose: np.ndarray,
    result_pose: np.ndarray,
    source_root: np.ndarray,
    result_root: np.ndarray,
    fps: float,
    source_contact: np.ndarray | None = None,
    result_contact: np.ndarray | None = None,
    source_phase: np.ndarray | None = None,
    result_phase: np.ndarray | None = None,
    source_facing: np.ndarray | None = None,
    result_facing: np.ndarray | None = None,
    source_level: np.ndarray | None = None,
    result_level: np.ndarray | None = None,
) -> dict[str, float]:
    losses: dict[str, float] = {}

    losses["pose"] = mse(source_pose, result_pose)
    losses["velocity"] = mse(
        finite_difference(source_pose, fps, 1),
        finite_difference(result_pose, fps, 1),
    )
    losses["acceleration"] = mse(
        finite_difference(source_pose, fps, 2),
        finite_difference(result_pose, fps, 2),
    )
    losses["root_trajectory"] = mse(source_root, result_root)

    if source_contact is not None and result_contact is not None:
        losses["contact"] = binary_contact_loss(source_contact, result_contact)
    if source_phase is not None and result_phase is not None:
        losses["phase"] = mse(source_phase, result_phase)
    if source_facing is not None and result_facing is not None:
        losses["facing"] = mse(source_facing, result_facing)
    if source_level is not None and result_level is not None:
        losses["level"] = mse(source_level, result_level)

    return losses


def weighted_fidelity_loss(
    losses: Mapping[str, float],
    weights: FidelityWeights | None = None,
) -> float:
    weights = weights or FidelityWeights()
    total = 0.0
    total_weight = 0.0

    for name, weight in vars(weights).items():
        if name not in losses:
            continue
        total += weight * float(losses[name])
        total_weight += weight

    return total / max(total_weight, 1e-8)
