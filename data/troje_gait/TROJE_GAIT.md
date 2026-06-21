# Biological Motion (Human Gait) Analysis and Synthesis Framework
This report outlines the scientific background, mathematical formulations, and code implementation of Nikolaus F. Troje's seminal 2002 paper on human gait patterns, based on the extracted data from the HTML5/JS BMWalker project.

---

## 1. 論文情報 (Paper Information)
* **Title**: Decomposing biological motion: A framework for analysis and synthesis of human gait patterns
* **Author**: Nikolaus F. Troje
* **Journal**: *Journal of Vision* (2002), 2(5), 371–387
* **DOI / Access**: Open Access (https://doi.org/10.1167/2.5.2)

### 科学的貢献と背景 (Scientific Contribution & Background)
Troje (2002) proposed a mathematical framework to decompose the complex 3D trajectories of human gait (walking patterns) into linear components using **Fourier Analysis** and **Principal Component Analysis (PCA)**. 

By analyzing point-light displays (PLD) of walking humans, Troje showed that:
1. **Fourier Series representation** can compress the complex, periodic 3D paths of individual joint markers into a few harmonic coefficients.
2. **PCA (Principal Component Analysis)** applied to these coefficients yields orthogonal axes representing major structural and behavioral traits:
   * **Body Structure / Gender** (gender: feminine vs. masculine)
   * **Weight** (heavy vs. light)
   * **Nervousness** (nervous/active vs. relaxed)
   * **Happiness** (happy vs. sad)
3. **Linear Synthesis**: Any arbitrary combination of these traits can be synthesized dynamically by scaling and adding the respective PCA vectors to the average walk cycle.

---

## 2. 歩行データの表現方法 (Data Representation)
For a human walker, the system tracks **$N = 15$ markers** (joint positions) in 3D space:
1. Head (頭)
2. Clavicles (鎖骨)
3. L-Shoulder (左肩)
4. L-Elbow (左肘)
5. L-Hand (左手)
6. R-Shoulder (右肩)
7. R-Elbow (右肘)
8. R-Hand (右手)
9. Belly (腹部)
10. L-Hip (左股関節)
11. L-Knee (左膝)
12. L-Ankle (左足首)
13. R-Hip (右股関節)
14. R-Knee (右膝)
15. R-Ankle (右足首)

Each marker has $3$ spatial coordinates ($x$: depth/longitudinal, $y$: lateral, $z$: vertical), yielding a total of **$3N = 45$ spatial coordinate trajectories**.

### フーリエ記述子による圧縮 (Fourier Decomposition)
Since walking is highly periodic, the 3D trajectory of coordinate $i$ (where $i \in [0, 44]$) over a single cycle is represented using a second-order Fourier series:
$$x_i(t) = a_{i,0} + a_{i,1} \sin(\theta(t)) + b_{i,1} \cos(\theta(t)) + a_{i,2} \sin(2\theta(t)) + b_{i,2} \cos(2\theta(t))$$

Where:
* $a_{i,0}$ is the **static mean offset** (resting position) of the coordinate.
* $a_{i,1}, b_{i,1}$ are the **fundamental frequency (1st harmonic)** sine/cosine coefficients.
* $a_{i,2}, b_{i,2}$ are the **2nd harmonic** sine/cosine coefficients.
* $\theta(t)$ is the **phase angle** of the walk cycle at time $t$.

### データベクトルの次元数 (Vector Dimensions)
The complete gait pattern of an individual is represented by a single vector $\mathbf{v}$ containing all coordinates' Fourier coefficients, plus:
* **Frequency scaling factor** (歩行周期に対応するフレーム数)
* **Translation speed factor** (前方移動速度)

The total size of the descriptor vector is:
$$\text{Length} = 5 \times (3N + 1) = 230 \text{ dimensions}$$

Here, the $(3N + 1) = 46$ elements represent:
* Indices $0 \dots 44$: The 45 spatial coordinates ($x, y, z$ for 15 markers).
* Index $45$: The frequency scaling factor.
* Inside the data structure, translation speed is placed at index $137$ ($45 + 2 \times 46$), representing the $b_{i,1}$ cosine coefficient for frequency translation.

---

## 3. 歩行合成の計算式 (Dynamic Synthesis Equations)
Let $b, w, n, h \in [-6.0, 6.0]$ represent the user-defined slider values for:
* $b$: Body Structure (Gender)
* $w$: Weight
* $n$: Nervousness
* $h$: Happiness

Any synthesized walker vector $\mathbf{v}$ is reconstructed as a linear combination:
$$\mathbf{v} = \mathbf{v}_{\text{mean}} + b \cdot \mathbf{v}_{\text{body}} + w \cdot \mathbf{v}_{\text{weight}} + n \cdot \mathbf{v}_{\text{nervous}} + h \cdot \mathbf{v}_{\text{happy}}$$

Where:
* $\mathbf{v}_{\text{mean}}$ is the mean walker vector (`meanwalker[0]`).
* $\mathbf{v}_{\text{body}}, \mathbf{v}_{\text{weight}}, \mathbf{v}_{\text{nervous}}, \mathbf{v}_{\text{happy}}$ are the PCA axis vectors of length 230.

### 3.1 周期・位相の計算 (Period and Phase Angle)
The base frequency scaling factor $F$ is computed at index $45$:
$$F = \mathbf{v}_{\text{mean}}[45] + b \cdot \mathbf{v}_{\text{body}}[45] + w \cdot \mathbf{v}_{\text{weight}}[45] + n \cdot \mathbf{v}_{\text{nervous}}[45] + h \cdot \mathbf{v}_{\text{happy}}[45]$$

Given physical time $t_{\text{ms}}$ and speed scaling factor $S$ (default is $1.0$), the phase angle $\theta(t)$ (in radians) is:
$$\theta(t) = \frac{t_{\text{ms}}}{1000} \cdot 2\pi \cdot \frac{120}{\text{Frequency}}$$
$$\text{Frequency} = \frac{F}{S}$$
Thus,
$$\theta(t) = t_{\text{sec}} \cdot 2\pi \cdot \frac{120 \cdot S}{F}$$
*Note: $120$ comes from the original 120 Hz camera sampling rate. The value $F$ represents the cycle period in frames at 120 Hz.*

### 3.2 マーカー座標の計算 (Marker Coordinate Computation)
For each coordinate $i \in [0, 44]$:
1. **静的初期座標 (Static Position)**:
   $$C_{i,\text{init}} = \mathbf{v}_{\text{mean}}[i] + b \cdot \mathbf{v}_{\text{body}}[i] + w \cdot \mathbf{v}_{\text{weight}}[i] + n \cdot \mathbf{v}_{\text{nervous}}[i] + h \cdot \mathbf{v}_{\text{happy}}[i]$$

2. **動的運動項 (Dynamic Motion Component)**:
   Define the step offset $j = 46$ ($3N + 1$):
   * Sine 1st Harmonic: $S_{i,1} = \mathbf{v}[i + j]$
   * Cosine 1st Harmonic: $C_{i,1} = \mathbf{v}[i + 2j]$
   * Sine 2nd Harmonic: $S_{i,2} = \mathbf{v}[i + 3j]$
   * Cosine 2nd Harmonic: $C_{i,2} = \mathbf{v}[i + 4j]$

   $$M_i(t) = S_{i,1} \sin(\theta(t)) + C_{i,1} \cos(\theta(t)) + S_{i,2} \sin(2\theta(t)) + C_{i,2} \cos(2\theta(t))$$

3. **合成された座標 (Synthesized Position)**:
   $$P_i(t) = C_{i,\text{init}} + M_i(t)$$

### 3.3 移動速度の計算 (Translation Speed)
The translation speed coefficient $tspeed$ (in mm/frame) is evaluated at index $137$:
$$tspeed = \mathbf{v}_{\text{mean}}[137] + b \cdot \mathbf{v}_{\text{body}}[137] + w \cdot \mathbf{v}_{\text{weight}}[137] + n \cdot \mathbf{v}_{\text{nervous}}[137] + h \cdot \mathbf{v}_{\text{happy}}[137]$$

The forward displacement $X_{\text{trans}}(t)$ at time $t$ is:
$$X_{\text{trans}}(t) = S \cdot tspeed \cdot 120 \cdot t_{\text{sec}}$$

---

## 4. 抽出データの実数値例 (Numerical Examples from Extracted Data)
Using the extracted `gait_data.json`, we find the following concrete values for the human model:

### 周期項 (Frequency Parameter at Index 45)
* $\bar{F}_{\text{mean}} = 126.0309$ frames (at 120 Hz, base period $T_0 \approx 1.05$ seconds, or $0.95$ Hz)
* $\mathbf{v}_{\text{body}}[45] = -0.8901$
* $\mathbf{v}_{\text{weight}}[45] = 1.6544$
* $\mathbf{v}_{\text{nervous}}[45] = -2.0459$ (nervousness shortens the period, making the walk faster)
* $\mathbf{v}_{\text{happy}}[45] = -1.5082$ (happiness also speeds up the walking rate)

### 前方移動速度項 (Translation Speed Parameter at Index 137)
* $\bar{tspeed}_{\text{mean}} = 11.3014$ mm/frame (at 120 Hz, base speed $V_0 = 1356.17$ mm/s $\approx 1.36$ m/s)
* $\mathbf{v}_{\text{body}}[137] = 0.3489$
* $\mathbf{v}_{\text{weight}}[137] = -0.1108$
* $\mathbf{v}_{\text{nervous}}[137] = 0.6398$ (nervousness increases travel speed)
* $\mathbf{v}_{\text{happy}}[137] = 0.4348$ (happiness increases travel speed)

### 静的頭部マーカー座標 (Head Marker at $t=0$, Index 0, 15, 30)
* **$X$ (Depth)**: Mean = $-10.7519$ mm, Gender Modifier = $+10.8623$
* **$Y$ (Lateral)**: Mean = $0.0000$ mm, Gender Modifier = $0.0000$ (centered midsagittally)
* **$Z$ (Vertical)**: Mean = $1640.6199$ mm, Gender Modifier = $+0.5983$ (the height of the head is $\approx 1.64$ m)

---

## 5. 描画・カメラ投影 (Rendering and Camera Projection)
Before rendering, the 3D marker coordinates are centered and rotated using the camera's azimuth (方位角), elevation (仰角), and roll (回転角), and then scaled:
1. **Centering offsets**:
   $$x_{\text{off}} = -\frac{X_{\text{max}} + X_{\text{min}}}{2}, \quad y_{\text{off}} = -\frac{Y_{\text{max}} + Y_{\text{min}}}{2}, \quad z_{\text{off}} = -\frac{Z_{\text{max}} + Z_{\text{min}}}{2}$$
2. **Size normalization**:
   $$size\_factor = Z_{\text{max}} - Z_{\text{min}}$$
3. **Screen Projection (Orthographic/Perspective)**:
   The rotated coordinates $\mathbf{v}' = [x', y', z']^T$ are projected onto the screen:
   $$\text{Screen } X = \frac{y'}{size\_factor} \times \text{Height} \times 37$$
   $$\text{Screen } Y = -\frac{z'}{size\_factor} \times \text{Height} \times 37$$
   *(37 pixels per degree of visual angle, scaling height to biological standards)*
