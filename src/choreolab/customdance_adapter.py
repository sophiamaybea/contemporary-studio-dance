from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .intent import global_intent
from .schema import StyleProfile


class CustomDanceAdapter:
    """Bridge between ChoreoLab intent/critique and a local CustomDance checkout.

    The upstream app remains responsible for retrieval, in-painting and SMPL export.
    This adapter owns reproducible intent payloads and project handoff files.
    """

    def __init__(self, root: str | Path = "vendor/CustomDance") -> None:
        self.root = Path(root)

    def check_install(self) -> None:
        if not (self.root / "README.md").exists():
            raise RuntimeError(
                "CustomDance is not bootstrapped. Run scripts/bootstrap_customdance.sh first."
            )

    def build_project_payload(
        self,
        profile: StyleProfile,
        project_intent: str,
        anchors: list[dict[str, Any]] | None = None,
    ) -> Dict[str, Any]:
        return {
            "global_intent": global_intent(profile, project_intent),
            "anchors": anchors or [],
            "critic_profile": profile.model_dump(),
        }

    def write_payload(
        self,
        output: str | Path,
        profile: StyleProfile,
        project_intent: str,
        anchors: list[dict[str, Any]] | None = None,
    ) -> Path:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self.build_project_payload(profile, project_intent, anchors)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path
