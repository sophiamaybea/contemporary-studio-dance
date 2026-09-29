from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .schema import Candidate, CandidateEvaluation, StyleProfile


DEFAULT_WEIGHTS: Dict[str, float] = {
    "momentum_causality": 0.20,
    "weight_transfer": 0.18,
    "spiral": 0.10,
    "asymmetry": 0.10,
    "suspension": 0.08,
    "acceleration_change": 0.08,
    "level_changes": 0.06,
    "eccentricity": 0.06,
    "gesture_evolution": 0.05,
    "virtuosity": 0.04,
    "groove": 0.05,
}

FLAG_PENALTIES = {
    "generic_lyrical": 0.30,
    "obvious_eight_count": 0.25,
    "pose_reset_pose": 0.25,
    "decorative_arm_waves": 0.20,
    "trick_for_trick_sake": 0.20,
    "literal_lyric_mime": 0.20,
    "symmetrical_resolution": 0.12,
}


@dataclass
class StyleCritic:
    threshold: float = 0.72

    def evaluate(
        self,
        candidate: Candidate,
        profile: StyleProfile,
        weights: Dict[str, float] | None = None,
    ) -> CandidateEvaluation:
        weights = weights or DEFAULT_WEIGHTS
        component_scores: Dict[str, float] = {}

        for feature, weight in weights.items():
            target = getattr(profile.features, feature)
            observed = getattr(candidate.features, feature)
            similarity = max(0.0, 1.0 - abs(target - observed))
            component_scores[feature] = similarity * weight

        base = sum(component_scores.values())
        total_weight = sum(weights.values()) or 1.0
        normalized = base / total_weight

        penalties = {
            flag: FLAG_PENALTIES[flag]
            for flag in candidate.flags
            if flag in FLAG_PENALTIES
        }
        score = max(0.0, normalized - sum(penalties.values()))

        reasons = []
        if candidate.features.momentum_causality < 0.6:
            reasons.append("Transitions feel insufficiently caused by prior momentum.")
        if candidate.features.asymmetry < 0.55:
            reasons.append("Movement is too symmetrical for the target grammar.")
        if candidate.features.eccentricity < 0.45:
            reasons.append("Candidate lacks the desired oddness / unexpected joint relationships.")
        if penalties:
            reasons.append("Detected discouraged movement clichés: " + ", ".join(sorted(penalties)))

        return CandidateEvaluation(
            candidate_id=candidate.id,
            score=round(score, 4),
            accepted=score >= self.threshold,
            component_scores={k: round(v, 4) for k, v in component_scores.items()},
            penalties=penalties,
            reasons=reasons,
        )
