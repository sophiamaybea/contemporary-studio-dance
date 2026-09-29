# Motion-capture dependencies

## DuoMo

Repository:
https://github.com/facebookresearch/DuoMo

Pinned commit:
`cfc1cdc44368228438ff579158f19e135173fa42`

Purpose:
monocular video -> body motion estimation.

## HTD-Refine

Repository:
https://github.com/ant-research/HTD-Refine

Pinned commit:
`2fcd6ddef3c4eb75a636062245f80a0136c09b7e`

Purpose:
refine human-motion recovery using high-order temporal dynamics, including velocity and acceleration consistency.

Run:

```bash
bash scripts/bootstrap_motion_capture.sh
```

Third-party checkpoints, body models and datasets remain subject to their own licenses.
