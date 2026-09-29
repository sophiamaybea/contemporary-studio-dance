from choreolab.critic import StyleCritic
from choreolab.schema import Candidate, MovementFeatures, StyleProfile


def features(value: float) -> MovementFeatures:
    return MovementFeatures(**{
        name: value
        for name in MovementFeatures.model_fields
    })


def test_matching_candidate_scores_high():
    profile = StyleProfile(name="target", features=features(0.8))
    candidate = Candidate(id="good", features=features(0.8))
    result = StyleCritic(threshold=0.7).evaluate(candidate, profile)
    assert result.accepted
    assert result.score > 0.95


def test_cliche_flags_apply_penalty():
    profile = StyleProfile(name="target", features=features(0.8))
    candidate = Candidate(
        id="cliche",
        features=features(0.8),
        flags=["generic_lyrical", "pose_reset_pose"],
    )
    result = StyleCritic(threshold=0.7).evaluate(candidate, profile)
    assert not result.accepted
    assert result.score < 0.7
