#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <project-slug> <local-video.mp4>"
  echo "Example: $0 shelter-from-the-storm /path/to/shelter.mp4"
  exit 1
fi

PROJECT="$1"
VIDEO="$2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/outputs/$PROJECT/source-transcription"

mkdir -p "$OUT"

if [ ! -f "$VIDEO" ]; then
  echo "Video not found: $VIDEO" >&2
  exit 1
fi

echo "Source-faithful transcription target: $PROJECT"
echo "Video: $VIDEO"
echo
echo "1) Run DuoMo primary recovery:"
echo "   cd $ROOT/vendor/DuoMo"
echo "   python scripts/inference.py --video_path \"$VIDEO\""
echo
echo "2) Run GVHMR on the same 30 FPS-normalised source and save its HMR result."
echo
echo "3) Refine the GVHMR track with HTD-Refine:"
echo "   htd-refine-pva --input \"$VIDEO\" --output \"$OUT/pva_results.pt\""
echo "   htd-refine-opt --video \"$VIDEO\" --pva_result \"$OUT/pva_results.pt\" \\"
echo "     --source gvhmr --motion /path/to/hmr4d_results.pt \\"
echo "     --output_root \"$OUT/htd\" --run_optimization --render"
echo
echo "4) Convert both recovered tracks to the ChoreoLab canonical NPZ/SMPL interchange."
echo "5) Score source fidelity with pose + velocity + acceleration + root + contact losses."
echo "6) Lock high-confidence source motion; allow CustomDance only inside repair-mask intervals."
echo
echo "Note: HTD-Refine currently expects 30 FPS input."
