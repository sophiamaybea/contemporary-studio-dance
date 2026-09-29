# Contemporary Choreography Lab

A reference-driven contemporary-dance analysis and choreography system.

The lab is designed to answer a harder question than **"what pose is the dancer making?"**:

> **What physical rule caused one movement to become the next?**

It learns reusable movement grammar from private reference dances, turns that grammar into project-specific choreographic direction, uses **CustomDance** as the 3D motion-generation engine, and scores candidate motion before accepting it.

## Current movement target

Reference Corpus 001 contains the first nine supplied contemporary-dance references. Its strongest recurring qualities are:

- momentum-driven transitions
- torso initiation and spirals
- asymmetry and limb lag
- suspension, collapse and rebound
- large technical extensions embedded inside transitions
- constant level changes and travelling
- controlled off-axis balance
- groove and weighted knees underneath larger phrases
- deliberately odd / crooked / non-pretty moments
- small gestures that propagate into whole-body movement

The lab currently models four composable dialects:

**FLOAT · FRACTURE · RELEASE · TRAVEL**

## Architecture

```text
PRIVATE REFERENCE DANCES
          |
          v
3D pose / SMPL extraction
          |
          v
KINEMATIC ANALYSIS
velocity · acceleration · travel · torso rotation · limb lag · levels
          |
          v
MOVEMENT GRAMMAR
          |
MUSIC ---> CHOREOGRAPHER AGENT
                    |
                    v
                CUSTOMDANCE
                    |
                    v
             candidate motions
                    |
                    v
               STYLE CRITIC
               /          \
            reject        accept
              |             |
              +---- retry --+
                            |
                            v
                    connected 3D dance
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## CustomDance

The project integrates [XulongT/CustomDance](https://github.com/XulongT/CustomDance) as a pinned upstream engine rather than copying and diverging from its source.

Pinned revision:

```text
bfd692329795b2547d477330d29af767cd2c7a5a
```

Bootstrap it with:

```bash
bash scripts/bootstrap_customdance.sh
```

Then follow the upstream CustomDance README to install its environment, models, FineDance data and SMPL resources.

## Install the lab

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Analyse extracted motion

The first numerical analyser accepts an NPZ containing:

- `positions`: `[frames, joints, 3]`
- `joint_names`: joint-name array
- `fps`: scalar, or provide `--fps`

Required semantic joints are pelvis, left/right shoulder, wrist and ankle.

```bash
choreolab analyse-npz \
  --input local/private/reference-001.npz \
  --output outputs/reference-001.json
```

It currently measures interpretable motion descriptors including:

- travel speed
- torso twist speed
- torso-to-distal motion lag
- left/right velocity asymmetry
- extension amplitude
- low-level / floorward movement
- vertical speed
- acceleration variability

The raw-video-to-3D-pose stage is intentionally pluggable. This repo does **not** claim that a weak 2D pose estimate is equivalent to understanding choreography.

## Score a candidate movement

```bash
choreolab score \
  --profile references/corpus-001/style-profile.yaml \
  --candidate examples/candidate.yaml
```

The critic rewards the qualities visible across the reference corpus and penalises patterns such as generic lyrical choreography, pose-reset-pose phrasing, obvious eight-count construction and detached tricks.

## Build a CustomDance intent

The first live project is **The Night They Drove Old Dixie Down**.

```bash
choreolab build-intent \
  --profile references/corpus-001/style-profile.yaml \
  --project projects/the-night-they-drove-old-dixie-down/project.yaml \
  --output outputs/dixie/customdance-intent.json
```

This produces a reproducible global intent + anchor payload for the CustomDance workflow.

## Repository map

```text
src/choreolab/
  kinematics.py             measured movement features
  reference_analyzer.py     pose-file analysis
  schema.py                 data contracts
  critic.py                 candidate scoring / rejection
  intent.py                 movement grammar -> direction
  customdance_adapter.py    CustomDance handoff
  cli.py

references/corpus-001/
  style-profile.yaml
  analysis-schema.yaml

projects/
  the-night-they-drove-old-dixie-down/

scripts/
  bootstrap_customdance.sh

vendor/
  README.md                 pinned upstream information

legacy/
  original routine files
```

## Reference material

Source dance videos stay private/local and are excluded by `.gitignore`. The repository is for derived measurements, annotations and abstract movement grammar, not redistribution or frame-for-frame reproduction of source choreography.

See [docs/REFERENCE_POLICY.md](docs/REFERENCE_POLICY.md).
