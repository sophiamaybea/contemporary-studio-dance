from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np


@dataclass(frozen=True)
class DynamicWeights:
    musical_fit: float = 0.15
    momentum_continuity: float = 0.18
    weight_logic: float = 0.16
    asymmetry: float = 0.09
    limb_lag: float = 0.08
    suspension: float = 0.08
    gesture_propagation: float = 0.10
    dynamic_contrast: float = 0.08
    interestingness: float = 0.08


def cosine_continuity(previous: np.ndarray, current: np.ndarray) -> float:
    a = np.asarray(previous, dtype=float).reshape(-1)
    b = np.asarray(current, dtype=float).reshape(-1)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom < 1e-8:
        return 0.0
    return float(np.clip(np.dot(a, b) / denom, -1.0, 1.0))


def asymmetry(left: np.ndarray, right_mirrored: np.ndarray) -> float:
    left = np.asarray(left, dtype=float)
    right = np.asarray(right_mirrored, dtype=float)
    numerator = np.linalg.norm(left - right)
    denominator = np.linalg.norm(left) + np.linalg.norm(right) + 1e-8
    return float(np.clip(numerator / denominator, 0.0, 1.0))


def optimal_lag(driver: np.ndarray, follower: np.ndarray, max_lag: int) -> tuple[int, float]:
    a = np.asarray(driver, dtype=float)
    b = np.asarray(follower, dtype=float)
    a = (a - a.mean()) / (a.std() + 1e-8)
    b = (b - b.mean()) / (b.std() + 1e-8)

    best_lag, best_corr = 0, -1.0
    for lag in range(max_lag + 1):
        aa = a[: len(a) - lag] if lag else a
        bb = b[lag:] if lag else b
        if len(aa) < 3:
            continue
        corr = float(np.mean(aa * bb))
        if corr > best_corr:
            best_lag, best_corr = lag, corr
    return best_lag, best_corr


def interestingness(novelty: float, coherence: float) -> float:
    """Reward motion that is both new and stylistically coherent."""
    novelty = float(np.clip(novelty, 0.0, 1.0))
    coherence = float(np.clip(coherence, 0.0, 1.0))
    return float(np.sqrt(novelty * coherence))


def weighted_objective(
    metrics: Mapping[str, float],
    penalties: Mapping[str, float] | None = None,
    weights: DynamicWeights | None = None,
) -> float:
    weights = weights or DynamicWeights()
    total = 0.0
    weight_sum = 0.0

    for name, weight in vars(weights).items():
        value = float(np.clip(metrics.get(name, 0.0), 0.0, 1.0))
        total += weight * value
        weight_sum += weight

    score = total / max(weight_sum, 1e-8)
    if penalties:
        score -= sum(max(0.0, float(v)) for v in penalties.values())

    return float(np.clip(score, 0.0, 1.0))


def curve_loss(
    candidate: np.ndarray,
    target: np.ndarray,
    discontinuity_weight: float = 0.15,
) -> float:
    candidate = np.asarray(candidate, dtype=float)
    target = np.asarray(target, dtype=float)

    if candidate.shape != target.shape:
        raise ValueError("candidate and target must have identical shapes")

    fit = float(np.mean(np.square(candidate - target)))

    if len(candidate) < 2:
        return fit

    velocity = np.diff(candidate, axis=0)
    discontinuity = float(np.mean(np.square(np.diff(velocity, axis=0)))) if len(velocity) > 1 else 0.0

    return fit + discontinuity_weight * discontinuity
