from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from .critic import StyleCritic
from .customdance_adapter import CustomDanceAdapter
from .schema import Candidate, StyleProfile


def _yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def cmd_build_intent(args):
    profile = StyleProfile.model_validate(_yaml(args.profile))
    project = _yaml(args.project)
    adapter = CustomDanceAdapter()
    path = adapter.write_payload(
        args.output,
        profile,
        project["intent"],
        project.get("anchors", []),
    )
    print(path)


def cmd_score(args):
    profile = StyleProfile.model_validate(_yaml(args.profile))
    candidate = Candidate.model_validate(_yaml(args.candidate))
    evaluation = StyleCritic(threshold=args.threshold).evaluate(candidate, profile)
    print(json.dumps(evaluation.model_dump(), indent=2))


def main():
    parser = argparse.ArgumentParser(prog="choreolab")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("build-intent", help="Build a CustomDance-ready intent payload.")
    p.add_argument("--profile", required=True)
    p.add_argument("--project", required=True)
    p.add_argument("--output", default="outputs/customdance-intent.json")
    p.set_defaults(func=cmd_build_intent)

    p = sub.add_parser("score", help="Score a candidate motion against a style profile.")
    p.add_argument("--profile", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--threshold", type=float, default=0.72)
    p.set_defaults(func=cmd_score)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
