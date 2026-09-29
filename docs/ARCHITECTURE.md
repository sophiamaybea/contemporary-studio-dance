# Architecture

## Goal

Contemporary Choreography Lab learns a **movement grammar** from a private reference corpus and uses that grammar to direct, select and critique original choreography produced with CustomDance.

The system is intentionally split into two layers:

1. **Choreographic intelligence** — reference analysis, style grammar, music/phrase intent, candidate critique.
2. **Motion synthesis** — CustomDance retrieval + diffusion in-painting + SMPL motion export.

## Pipeline

```text
private reference videos
        |
        v
pose / motion extraction
        |
        v
feature + transition analysis
        |
        v
movement grammar
        |
music -> choreographer agent -> CustomDance
                         |          |
                         |          v
                         +---- candidate motions
                                  |
                                  v
                              style critic
                             /           \
                         reject          accept
                           |               |
                           +---- retry ----+
                                           |
                                           v
                                  connected SMPL motion
```

## What the grammar describes

The system should model more than poses:

- initiation source: sternum, ribs, pelvis, head, distal limb
- centre-of-mass travel and base of support
- support foot and foot-contact changes
- floor contacts
- level and level-change velocity
- facing vs travel direction
- torso rotation and spiral
- limb lag relative to torso
- acceleration / deceleration / suspension
- collapse, rebound and recovery
- off-axis balance
- pathway curvature
- asymmetry
- gesture-to-whole-body propagation
- musical anticipation, delay and selective accents
- transition causality

The objective is not to reproduce a source routine. It is to learn reusable relationships such as:

`sternum rotates -> support foot pivots -> free leg releases -> arm trails -> step catches the fall`

## Dialects

Reference Corpus 001 is represented as four composable dialects:

- **FLOAT** — suspension, extension, long curves, off-axis balance
- **FRACTURE** — interruption, contraction, redirection, crooked shape
- **RELEASE** — collapse, floor contact, fold, rebound, recovery
- **TRAVEL** — spirals, diagonals, walking mutations, momentum

A project may blend these differently by musical section.

## CustomDance boundary

CustomDance stays an upstream dependency. The lab pins a known commit and bootstraps it into `vendor/CustomDance`. This prevents a copied fork from silently drifting while allowing deliberate upgrades.

The lab owns:
- style profiles
- reference-corpus metadata
- choreographic intent generation
- candidate scoring / rejection
- project dramaturgy
- provenance

CustomDance owns:
- temporal anchor workflow
- movement retrieval
- diffusion in-painting
- SMPL editing/export
