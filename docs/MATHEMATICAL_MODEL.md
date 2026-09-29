# Mathematical Choreography Model

Contemporary Choreography Lab models dance as a **coupled dynamical system** rather than a sequence of named moves.

Let the dancer state at time `t` be:

```text
X(t) = [q(t), qdot(t), qddot(t), c(t), s(t), f(t), e(t), m(t)]
```

where:

- `q(t)` = joint configuration / pose
- `qdot(t)` = joint velocity
- `qddot(t)` = joint acceleration
- `c(t)` = centre of mass
- `s(t)` = support state / base of support
- `f(t)` = facing + travel direction
- `e(t)` = effort / dynamic quality vector
- `m(t)` = musical state

The choreography engine does not ask only "what pose comes next?"
It asks:

```text
dX/dt = F(X(t), M(t), G, I(t), H(t))
```

where:

- `M(t)` = musical features over time
- `G` = learned movement grammar
- `I(t)` = project-specific choreographic intent
- `H(t)` = movement history

This makes transitions causal.

## 1. Musical field

For each time step:

```text
M(t) = [
  pulse(t),
  onset(t),
  loudness(t),
  spectral_flux(t),
  harmonic_tension(t),
  vocal_density(t),
  phrase_position(t)
]
```

Movement does not need to follow every beat directly.

Instead define a response delay:

```text
R(t) = M(t - tau(t))
```

where `tau(t)` can be positive, zero or negative.

That allows:
- anticipation
- exact accent
- delayed arrival
- phrase-spanning motion

## 2. Momentum continuity

Let whole-body momentum proxy be:

```text
P(t) = sum_i w_i * qdot_i(t)
```

A transition should conserve some directional or energetic information:

```text
C_momentum = cosine(P(t-1), P(t))
```

A high-quality phrase often preserves momentum while changing its pathway.

## 3. Controlled instability

Let the projected centre of mass be `c_xy(t)` and the support polygon be `S(t)`.

Define instability:

```text
D_support(t) = signed_distance(c_xy(t), S(t))
```

- negative: centre of mass safely inside support
- near zero: edge of balance
- positive: body must catch, step, fall or redirect

This gives us intentional off-axis movement.

## 4. Asymmetry

Let left and right limb velocity vectors be `v_L(t)` and `v_R(t)`.

```text
A(t) = ||v_L(t) - mirror(v_R(t))|| / (||v_L(t)|| + ||v_R(t)|| + eps)
```

The reference corpus prefers relatively high asymmetry.

## 5. Limb lag

If torso rotational velocity is `omega_T(t)` and distal limb velocity is `v_D(t)`, estimate:

```text
tau_lag = argmax_tau corr(omega_T(t), v_D(t + tau))
```

Positive `tau_lag` means the limbs arrive after the torso.

This is one of the strongest qualities in the reference corpus.

## 6. Suspension

A suspension event is not just "slow movement".

Define:

```text
S(t) = high(extension(t))
       * low(vertical_velocity(t))
       * high(balance_risk(t))
```

So a long line with nearly frozen vertical travel while the body is slightly off-axis scores highly.

## 7. Collapse and rebound

Let vertical centre-of-mass velocity be `v_y(t)`.

Collapse:

```text
K_down(t) = max(0, -v_y(t))
```

Rebound:

```text
K_up(t + dt) = max(0, v_y(t + dt))
```

A meaningful collapse-rebound relation can be:

```text
R_cr = integral(K_down) * integral(K_up) * temporal_proximity
```

This rewards a fall that physically generates the recovery.

## 8. Gesture propagation

Let `g_0` be the initiating joint group and `g_1 ... g_n` be downstream groups.

A gesture becomes whole-body choreography when activation propagates:

```text
g_0(t)
 -> g_1(t + delta_1)
 -> g_2(t + delta_2)
 -> ...
 -> g_n(t + delta_n)
```

We can estimate propagation quality from ordered cross-correlation peaks.

Example:

```text
wrist -> elbow -> shoulder -> ribs -> pelvis -> step
```

## 9. Interestingness

The system should avoid both randomness and predictability.

Define:

```text
I = novelty * coherence
```

with:

```text
novelty = distance(candidate, recent_motion_history)
coherence = similarity(candidate_dynamics, target_grammar)
```

Too little novelty = generic / repetitive.
Too little coherence = random movement.

The useful region is a middle band.

## 10. Candidate objective

For candidate motion `x`:

```text
Score(x) =
  w1 * musical_fit
+ w2 * momentum_continuity
+ w3 * weight_logic
+ w4 * asymmetry
+ w5 * limb_lag
+ w6 * suspension
+ w7 * gesture_propagation
+ w8 * dynamic_contrast
+ w9 * interestingness
- penalties
```

The critic can then reject candidates before CustomDance connects them.

## 11. Project curve

Each song gets its own target curves:

```text
T_project(t) = [
  restraint(t),
  instability(t),
  extension(t),
  groove(t),
  floor_proximity(t),
  eccentricity(t),
  travel(t),
  release(t)
]
```

The generator tries to minimise:

```text
L = integral ||F_candidate(t) - T_project(t)||^2 dt
    + lambda_1 * discontinuity
    + lambda_2 * cliche_penalty
    + lambda_3 * imitation_penalty
```

This is the core mathematical view of choreography in the lab.
