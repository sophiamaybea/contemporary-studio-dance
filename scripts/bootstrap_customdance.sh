#!/usr/bin/env bash
set -euo pipefail

CUSTOMDANCE_REPO="https://github.com/XulongT/CustomDance.git"
CUSTOMDANCE_COMMIT="bfd692329795b2547d477330d29af767cd2c7a5a"
TARGET="vendor/CustomDance"

mkdir -p vendor

if [ -d "$TARGET/.git" ]; then
  echo "CustomDance already cloned. Fetching pinned revision..."
  git -C "$TARGET" fetch origin
else
  git clone "$CUSTOMDANCE_REPO" "$TARGET"
fi

git -C "$TARGET" checkout "$CUSTOMDANCE_COMMIT"

echo
echo "CustomDance pinned at:"
git -C "$TARGET" rev-parse HEAD
echo
echo "Next: follow vendor/CustomDance/README.md to install its environment and resources."
