# Source-faithful dance transcription

This mode is for preserving the choreography of a supplied reference dance rather than generating a new routine from stylistic prompts.

## Principle

The source video is the authority.

The pipeline is:

```text
source video
   |
   v
monocular human motion recovery
   |
   v
SMPL / world-space body track
   |
   v
high-order dynamics refinement
   |
   v
mathematical transcription
   |
   +--> exact timing / trajectory / weight / levels / turns / contacts
   |
   v
retarget to performer
   |
   v
optional gap repair for low-confidence frames only
```

## Recovery stack

The preferred 2026 stack is:

1. **DuoMo** for body-motion estimation from monocular video.
2. **HTD-Refine** for high-order temporal refinement of recovered motion.
3. ChoreoLab's fidelity layer for timing, velocity, acceleration, trajectory and contact preservation.
4. **CustomDance only as a repair tool** where the recovered source has genuine occlusion or missing motion.

This is deliberately different from generative mode.

## Source fidelity objective

Let source motion be `X_s(t)` and reconstructed / retargeted motion be `X_r(t)`.

We minimise:

```text
L_total =
    w_pose    * L_pose
  + w_vel     * L_velocity
  + w_acc     * L_acceleration
  + w_root    * L_root_trajectory
  + w_contact * L_contact
  + w_phase   * L_phase
  + w_facing  * L_facing
  + w_level   * L_level
```

with strong weights on motion dynamics rather than pose alone.

### Pose

```text
L_pose = mean ||q_r(t) - q_s(t)||^2
```

### Velocity

```text
L_velocity = mean ||qdot_r(t) - qdot_s(t)||^2
```

### Acceleration

```text
L_acceleration = mean ||qddot_r(t) - qddot_s(t)||^2
```

### Root trajectory

```text
L_root = mean ||c_r(t) - c_s(t)||^2
```

### Contacts

For binary contact state `k(t)`:

```text
L_contact = mean XOR(k_r(t), k_s(t))
```

### Musical phase

The reconstruction should preserve when events occur, not merely their order.

```text
L_phase = mean |phi_r(event_i) - phi_s(event_i)|
```

## Repair mask

Generative repair is allowed only where source confidence is low.

```text
repair(t) = 1 if confidence(t) < tau else 0
```

High-confidence source motion is locked.

## Retargeting

Retargeting may change:
- bone lengths
- neutral body proportions
- global scale

It should preserve:
- joint-angle relationships
- timing
- root trajectory shape
- foot contacts
- turn count and direction
- level changes
- dynamic accents
- movement causality

## Copyright / provenance

Keep source videos local/private unless redistribution rights are clear. Store source links, provenance, derived measurements and motion data according to the intended use and applicable rights.
