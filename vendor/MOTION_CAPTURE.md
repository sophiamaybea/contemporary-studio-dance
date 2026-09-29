# Motion-capture dependencies

The source-faithful mode uses two complementary recovery paths.

## Primary path: DuoMo

Repository:
https://github.com/facebookresearch/DuoMo

Pinned commit:
`cfc1cdc44368228438ff579158f19e135173fa42`

Purpose:
monocular video -> world-space body motion estimation.

License note:
DuoMo is released under a non-commercial research licence. Do not assume commercial-use permission.

## Dynamics-refined path: GVHMR -> HTD-Refine

### GVHMR

Repository:
https://github.com/zju3dv/GVHMR

Pinned commit:
`ee960bb6e2ea2d381aa97f08e9b71ef320b624b1`

Purpose:
initial world-grounded SMPL motion recovery.

### HTD-Refine

Repository:
https://github.com/ant-research/HTD-Refine

Pinned commit:
`2fcd6ddef3c4eb75a636062245f80a0136c09b7e`

Purpose:
refine the recovered motion using estimated 3D velocity and acceleration.

HTD-Refine currently documents GVHMR and TRAM as supported HMR initialisations. ChoreoLab therefore does **not** pretend that DuoMo output can be passed directly into HTD-Refine without an adapter.

## Why run two paths?

For an "actual dance" transcription, we care about more than pose accuracy.

ChoreoLab can compare:
- 2D reprojection consistency
- root trajectory
- contact stability
- velocity / acceleration structure
- temporal phase
- visual overlay

and choose the stronger track or selectively reconcile low-confidence regions.

Run:

```bash
bash scripts/bootstrap_motion_capture.sh
```

Third-party checkpoints, body models and datasets remain subject to their own licences.
