#!/usr/bin/env bash
set -euo pipefail

mkdir -p vendor

clone_pin () {
  local repo="$1"
  local target="$2"
  local commit="$3"

  if [ -d "$target/.git" ]; then
    git -C "$target" fetch origin
  else
    git clone "$repo" "$target"
  fi

  git -C "$target" checkout "$commit"
  echo "$target -> $(git -C "$target" rev-parse HEAD)"
}

clone_pin "https://github.com/facebookresearch/DuoMo.git"   "vendor/DuoMo"   "cfc1cdc44368228438ff579158f19e135173fa42"

clone_pin "https://github.com/ant-research/HTD-Refine.git"   "vendor/HTD-Refine"   "2fcd6ddef3c4eb75a636062245f80a0136c09b7e"

echo
echo "Motion-capture sources are pinned."
echo "Follow each upstream README for environment, checkpoints and SMPL/SMPL-X assets."
