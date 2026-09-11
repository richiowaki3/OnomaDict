# Response from Effort AI: Calibration of D-Axis, Thresholds, and 3-Point Keyframes

> [!NOTE]
> Research Note: Citations and claims under ongoing empirical verification.

---

## 0. Synchronization of Premise (Category A Frozen)
Category A ($x_1 - x_4$) is frozen and locked: $x_1$ Weight, $x_2$ Time (purified as internal attitude toward time, without carrying acoustic duration), $x_3$ Space, and $x_4$ Flow. ADSR is separated into Category B ($x_8$), and phrasing is separated into Category D ($x_{13} - x_{16}$).

---

## 1. Received Data Verification
- $x_{16}$ currently takes 3 discrete values: $\{0:147, 1:456, 8:161\}$. $x_{13}$ defaults to 4 for 437 words. $x_{14}$ defaults to 5 for 639 words. $x_{15} \in \{0, 5, 6, 7\}$.
- $r(x_{16}, x_{9\text{\_norm}}) = -0.156$. Orthogonality and task division hold as designed.
- $x_{9\text{\_norm}}$ mean is $6.11$, median $6.5$, heavily skewed toward turbulence ($<4.5$ for 180 words, $\ge 4.5$ for 584 words).

**Conclusion**: Migration (appending D-axis) can proceed as planned.

---

## 2. Solution to Discrete Fixation: Real-Audio Envelope Calibration
Because morphological templates are finite, bootstrapping from morphological templates results in discrete cluster values. This is correct as an initial prior, but continuous calibration requires real-audio measurement:

- **$x_{16}$ Regularity** $\leftarrow$ Coefficient of Variation of Inter-Onset Interval (IOI): $\text{CV} = \text{std(IOI)} / \text{mean(IOI)}$. Single-shot words default to 0. Linear mapping of CV to scale $[0, 9]$.
- **$x_{13}$ Accent** $\leftarrow$ Normalized time centroid of the energy envelope within $[0, 1] \times 9$. Impulse-leading (low) vs. impact-lagging (high). Overwrites default value 4.
- **$x_{14}$ Contour** $\leftarrow$ Envelope peak amplitude slope over onsets. Acceleration/burst (low) vs. deceleration/fading (high), flat envelope (5).
- **$x_{15}$ Meter** $\leftarrow$ Onset density per unit time. Single-shot (0), continuous repeat (9).

Operational strategy: Values derived from `morph_type` serve as **priors**, while synthesized audio measurements **overwrite** priors to form continuous distributions.

---

## 3. Decisions on Key Questions

### Q1. Thresholds for $x_{16}$ / $x_9$
Quadrant thresholds are for visualization purposes only and do not affect underlying metric orthogonality:
- $x_{16}$ boundary: shift discrete boundary $2/7$ to the scale midpoint **4.5**.
- $x_9$ boundary: physical laminar/turbulent transition ($\text{Re} \approx 2300$) corresponds to **$x_{9\text{\_norm}} \approx 5.3$**.

### Q2. Level Handling for $3+$ Repetitions in $x_{15}$ Meter
No discrete level bins will be added. Onset density naturally handles $3+$ repetitions (e.g., *chinchirorin*, *peechiku*) as continuous higher density values.

### Q3. Interpolation Rules for 3-Point Keyframes
Keyframe envelope interpolation rules will align directly with Category A effort values ($x_1 - x_4$).