import numpy as np

from choreolab.kinematics import SkeletonMap, analyse_pose_sequence


def test_pose_analyser_returns_expected_metrics():
    frames = 60
    joints = 7
    p = np.zeros((frames, joints, 3), dtype=float)

    # pelvis travels horizontally
    p[:, 0, 0] = np.linspace(0, 2, frames)
    p[:, 0, 1] = 1.0

    # shoulders
    p[:, 1] = p[:, 0] + np.array([-0.3, 0.5, 0.0])
    p[:, 2] = p[:, 0] + np.array([0.3, 0.5, 0.0])

    # wrists
    p[:, 3] = p[:, 0] + np.array([-0.8, 0.4, 0.0])
    p[:, 4] = p[:, 0] + np.array([0.8, 0.4, 0.0])

    # ankles
    p[:, 5] = p[:, 0] + np.array([-0.2, -1.0, 0.0])
    p[:, 6] = p[:, 0] + np.array([0.2, -1.0, 0.0])

    skel = SkeletonMap(
        pelvis=0,
        left_shoulder=1,
        right_shoulder=2,
        left_wrist=3,
        right_wrist=4,
        left_ankle=5,
        right_ankle=6,
    )

    result = analyse_pose_sequence(p, fps=30, skel=skel)

    assert result["frames"] == frames
    assert result["travel_speed_body_scales_per_second"] > 0
    assert result["max_distal_extension_body_scales"] > 1
