from __future__ import annotations

from .schema import StyleProfile


def global_intent(profile: StyleProfile, project_intent: str) -> str:
    f = profile.features
    qualities = []

    if f.momentum_causality >= 0.75:
        qualities.append("Make each movement appear physically caused by the movement before it.")
    if f.spiral >= 0.75:
        qualities.append("Use strong torso spirals and continuously changing orientation.")
    if f.asymmetry >= 0.75:
        qualities.append("Prefer asymmetry, delayed limbs and unresolved body relationships.")
    if f.suspension >= 0.70:
        qualities.append("Use suspension and delayed arrival rather than constant beat-hitting.")
    if f.eccentricity >= 0.60:
        qualities.append("Allow peculiar, crooked or deliberately non-pretty moments.")
    if f.groove >= 0.50:
        qualities.append("Let weighted knees, foot rhythm and pulse live underneath larger phrases.")
    if f.virtuosity >= 0.60:
        qualities.append("Permit technical virtuosity only when it emerges from momentum rather than presentation.")

    avoids = "; ".join(profile.avoid)
    return (
        project_intent.strip()
        + "\n\nMovement grammar:\n- "
        + "\n- ".join(qualities)
        + (f"\n\nAvoid: {avoids}." if avoids else "")
    )
