import numpy as np

from choreolab.transcription import (
    binary_contact_loss,
    repair_mask,
    source_fidelity_losses,
    weighted_fidelity_loss,
)


def test_identical_motion_has_zero_loss():
    pose = np.zeros((20, 6, 3), dtype=float)
    root = np.zeros((20, 3), dtype=float)

    losses = source_fidelity_losses(
        source_pose=pose,
        result_pose=pose.copy(),
        source_root=root,
        result_root=root.copy(),
        fps=30.0,
    )

    assert weighted_fidelity_loss(losses) == 0.0


def test_contact_mismatch_is_detected():
    a = np.array([[1, 0], [1, 1]], dtype=int)
    b = np.array([[1, 1], [0, 1]], dtype=int)
    assert binary_contact_loss(a, b) == 0.5


def test_repair_mask_only_unlocks_low_confidence_frames():
    c = np.array([0.9, 0.4, 0.7, 0.2])
    mask = repair_mask(c, threshold=0.55)
    assert mask.tolist() == [False, True, False, True]
