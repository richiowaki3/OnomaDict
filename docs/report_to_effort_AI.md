# Dictionary Verification Report: Orthogonality of $x_{16}$ Regularity and $x_9$ Reynolds

> [!NOTE]
> Research Note: Citations and claims under ongoing empirical verification.

---

## Conclusion
**$x_{16}$ (Regularity) and $x_9$ (Reynolds Turbulence) are orthogonal ($r = -0.16$). The functional separation holds.**

---

## 1. Metric Independence Verification
- Full dataset (764 words): Correlation between $x_{16}$ and $x_9$ is **$r = -0.16$**.
- Reduplicated words only ($x_{15} > 0, n = 616$): **$r = -0.08$**.
- $x_{16}$ against all other 11 core axes: $|r| < 0.16$ across all axes.

Words populate all 4 quadrants of the $x_{16} \times x_9$ space as expected:

| | $x_9$ Laminar (Smooth) | $x_9$ Turbulent (Rough) |
| :--- | :--- | :--- |
| **$x_{16}$ Regular** | *an-an*, *uka-uka*, *ā-n* | *kasa-kasa*, *ira-ira*, *kasu-kasu* |
| **$x_{16}$ Irregular** | *assari*, *uttori*, *unzari* | *ata-futa*, *kasa-koso*, *uro-choro* |

---

## 2. Dataset Specifics & Observations
- **$x_9$ Turbulence Bias**: Existing words skew toward medium/high turbulence ($x_{9\text{\_norm}}$ mean $\approx 5.6 - 6.0$), reflecting the natural concentration of Japanese onomatopoeia in impact and friction events.
- **Continuous Calibration Plan**: Discrete morphological priors $\{0, 1, 8\}$ will be continuously calibrated using real audio envelope DSP measurements (inter-onset interval variance for $x_{16}$, energy time-centroid for $x_{13}$ accent).

---

## 3. Bundled Files
- `onomatopoeia_extended_D.csv`: Full 764-word dataset appending $x_{13} - x_{16}$ and morphological labels without mutating core axes $x_1 - x_{12}$.