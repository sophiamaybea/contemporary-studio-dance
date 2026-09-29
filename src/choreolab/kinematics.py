from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class SkeletonMap:
    pelvis: int
    left_shoulder: int
    right_shoulder: int
    left_wrist: int
    right_wrist: int
    left_ankle: int
    right_ankle: int


def _safe_norm(x: np.ndarray, axis: int = -1) -> np.ndarray:
    return np.sqrt(np.sum(np.square(x), axis=axis) + 1e-8)


def _velocity(x: np.ndarray, fps: float) -> np.ndarray:
    if len(x) < 2:
        return np.zeros_like(x)
    v = np.gradient(x, axis=0) * fps
    return v


def _acceleration(x: np.ndarray, fps: float) -> np.ndarray:
    return _velocity(_velocity(x, fps), fps)


def body_scale(positions: np.ndarray, skel: SkeletonMap) -> float:
    shoulders = _safe_norm(
        positions[:, skel.left_shoulder] - positions[:, skel.right_shoulder]
    )
    ankles = _safe_norm(
        positions[:, skel.left_ankle] - positions[:, skel.right_ankle]
    )
    scale = float(np.nanmedian(np.concatenate([shoulders, ankles])))
    return max(scale, 1e-6)


def horizontal_path_length(track: np.ndarray) -> float:
    if len(track) < 2:
        return 0.0
    delta = np.diff(track[:, [0, 2]], axis=0)
    return float(np.sum(_safe_norm(delta)))


def yaw_from_pair(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    line = right - left
    return np.unwrap(np.arctan2(line[:, 2], line[:, 0]))


def normalized_cross_correlation_lag(
    driver: np.ndarray,
    follower: np.ndarray,
    max_lag_frames: int,
) -> tuple[int, float]:
    a = np.asarray(driver, dtype=float)
    b = np.asarray(follower, dtype=float)

    if len(a) < 4 or len(b) < 4:
        return 0, 0.0

    a = (a - a.mean()) / (a.std() + 1e-8)
    b = (b - b.mean()) / (b.std() + 1e-8)

    best_lag = 0
    best_corr = -1.0
    max_lag_frames = max(0, min(max_lag_frames, len(a) - 2))

    for lag in range(max_lag_frames + 1):
        aa = a[: len(a) - lag] if lag else a
        bb = b[lag:] if lag else b
        if len(aa) < 3:
            continue
        corr = float(np.mean(aa * bb))
        if corr > best_corr:
            best_lag = lag
            best_corr = corr

    return best_lag, best_corr


def analyse_pose_sequence(
    positions: np.ndarray,
    fps: float,
    skel: SkeletonMap,
) -> dict:
    """Extract interpretable kinematic descriptors from a 3D joint sequence.

    Parameters
    ----------
    positions:
        Array shaped [frames, joints, 3].
    fps:
        Frames per second.
    skel:
        Joint indices required by the analyser.

    The output intentionally contains measured descriptors rather than claims
    about choreographic authorship or identity.
    """
    p = np.asarray(positions, dtype=float)
    if p.ndim != 3 or p.shape[-1] != 3:
        raise ValueError("positions must have shape [frames, joints, 3]")
    if fps <= 0:
        raise ValueError("fps must be positive")

    scale = body_scale(p, skel)
    pelvis = p[:, skel.pelvis]

    pelvis_v = _velocity(pelvis, fps)
    pelvis_a = _acceleration(pelvis, fps)

    shoulder_yaw = yaw_from_pair(
        p[:, skel.left_shoulder], p[:, skel.right_shoulder]
    )
    hip_proxy_left = 0.5 * (pelvis + p[:, skel.left_ankle])
    hip_proxy_right = 0.5 * (pelvis + p[:, skel.right_ankle])
    lower_yaw = yaw_from_pair(hip_proxy_left, hip_proxy_right)

    torso_twist = np.unwrap(shoulder_yaw - lower_yaw)
    torso_angular_speed = np.abs(_velocity(torso_twist[:, None], fps)[:, 0])

    wrists = np.stack(
        [p[:, skel.left_wrist], p[:, skel.right_wrist]], axis=1
    )
    ankles = np.stack(
        [p[:, skel.left_ankle], p[:, skel.right_ankle]], axis=1
    )

    wrist_speed = _safe_norm(_velocity(wrists, fps), axis=-1).mean(axis=1)
    ankle_speed = _safe_norm(_velocity(ankles, fps), axis=-1).mean(axis=1)
    distal_speed = 0.5 * (wrist_speed + ankle_speed)

    lag_frames, lag_corr = normalized_cross_correlation_lag(
        torso_angular_speed,
        distal_speed,
        max_lag_frames=max(1, int(round(0.5 * fps))),
    )

    left_speed = (
        _safe_norm(_velocity(p[:, skel.left_wrist], fps))
        + _safe_norm(_velocity(p[:, skel.left_ankle], fps))
    )
    right_speed = (
        _safe_norm(_velocity(p[:, skel.right_wrist], fps))
        + _safe_norm(_velocity(p[:, skel.right_ankle], fps))
    )
    asymmetry = float(
        np.mean(np.abs(left_speed - right_speed))
        / (np.mean(left_speed + right_speed) + 1e-8)
    )

    distal_points = np.concatenate([wrists, ankles], axis=1)
    radial = _safe_norm(distal_points - pelvis[:, None, :], axis=-1) / scale

    floor_y = np.nanpercentile(
        np.concatenate(
            [p[:, skel.left_ankle, 1], p[:, skel.right_ankle, 1]]
        ),
        10,
    )
    pelvis_height = (pelvis[:, 1] - floor_y) / scale
    standing_ref = max(float(np.nanpercentile(pelvis_height, 90)), 1e-6)

    duration = max((len(p) - 1) / fps, 1e-6)
    travel = horizontal_path_length(pelvis) / scale / duration

    vertical_speed = np.abs(pelvis_v[:, 1]) / scale
    vertical_accel = np.abs(pelvis_a[:, 1]) / scale

    return {
        "frames": int(len(p)),
        "fps": float(fps),
        "duration_seconds": float(duration),
        "body_scale": float(scale),
        "travel_speed_body_scales_per_second": float(travel),
        "mean_torso_twist_speed_rad_s": float(np.mean(torso_angular_speed)),
        "torso_to_distal_best_lag_seconds": float(lag_frames / fps),
        "torso_to_distal_lag_correlation": float(lag_corr),
        "left_right_velocity_asymmetry": float(asymmetry),
        "mean_distal_extension_body_scales": float(np.mean(radial)),
        "max_distal_extension_body_scales": float(np.max(radial)),
        "low_level_fraction": float(np.mean(pelvis_height < 0.55 * standing_ref)),
        "mean_vertical_speed_body_scales_per_second": float(np.mean(vertical_speed)),
        "vertical_acceleration_variability": float(np.std(vertical_accel)),
    }


def indices_from_names(
    joint_names: Sequence[str],
    aliases: dict[str, Sequence[str]] | None = None,
) -> SkeletonMap:
    names = [str(x).strip().lower() for x in joint_names]
    aliases = aliases or {
        "pelvis": ("pelvis", "hips", "hip"),
        "left_shoulder": ("left_shoulder", "l_shoulder", "leftshoulder"),
        "right_shoulder": ("right_shoulder", "r_shoulder", "rightshoulder"),
        "left_wrist": ("left_wrist", "l_wrist", "leftwrist"),
        "right_wrist": ("right_wrist", "r_wrist", "rightwrist"),
        "left_ankle": ("left_ankle", "l_ankle", "leftankle"),
        "right_ankle": ("right_ankle", "r_ankle", "rightankle"),
    }

    found = {}
    for field, candidates in aliases.items():
        for c in candidates:
            if c.lower() in names:
                found[field] = names.index(c.lower())
                break
        if field not in found:
            raise KeyError(
                f"Could not find required joint '{field}'. Available names: {names}"
            )

    return SkeletonMap(**found)
