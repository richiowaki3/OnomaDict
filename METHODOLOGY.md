# Methodology and Theoretical Background

Overview of the construction methodology, theoretical references, and data-processing pipeline of the **Unexplored Onomatopoeia Dictionary (JP & KR)**.

---

## 1. Design Philosophy

This dictionary formalizes Japanese and Korean onomatopoeia as points in a multidimensional latent space of physical and sensory dimensions. It externalizes the Transformer architecture (Encoder $\rightarrow$ Latent Representation $\rightarrow$ Decoder): sensory perception serves as the shared intermediate representation, while each language's phonological and sound-symbolic rules act as language-specific encoders and decoders.

The goal is to serve as a cross-modal conversion hub spanning dance choreography, acoustic synthesis, computer graphics, motion design, lighting, and natural language processing. 

The project originates from the unmapped blank regions in the tactile matrix of onomatopoeia (Hayakawa, Matsui & Watanabe, 2010), raising the fundamental question: *Do physical sensations exist for which no word yet exists in natural language?*

---

## 2. Vector Structure (16 Core Axes + Phrasing + Accent)

| Category | Axes | Theoretical Origin / Source |
| :--- | :--- | :--- |
| **A. Effort** | $x_1$ Weight, $x_2$ Time, $x_3$ Space, $x_4$ Flow | Laban Movement Analysis (LMA Effort Factors) |
| **B. Acoustic** | $x_5$ Hardness, $x_6$ Moisture, $x_7$ Frequency, $x_8$ Decay | Acoustic Physics & Signal Processing |
| **C. Extended** | $x_9$ Reynolds, $x_{10}$ Boyle, $x_{11}$ Temperature, $x_{12}$ Color ($\rightarrow$ CIELAB) | Fluid Dynamics, Haptics, and Colorimetry |
| **D. Phrasing** | $x_{13}$ Accent, $x_{14}$ Contour, $x_{15}$ Meter, $x_{16}$ Regularity | Phrase-scale Meter & Rhythmic Envelope |
| **Accent Layer** | Pitch Accent Type (UniDic) | Pitch Accent / Prosodic Nucleus |

### Purification of $x_2$ Time vs. Acoustic Decay ($x_8$)
- **$x_2$ Time** is defined strictly as the internal **attitude toward time** (sudden vs. sustained impulse), representing pure kinematic effort quality. It does not measure physical sound duration.
- **$x_8$ Decay** captures the physical acoustic decay, reverberation, and ADSR envelope cutoff in Category B.

### Epistemological Layering (Naïve Physics vs. Real Physics)
- **Category A (Effort)** represents human perceptual and embodied movement quality — **Naïve Physics** (an observer-dependent cognitive model of motion).
- **Categories B & C (Reynolds Fluid Dynamics, Acoustic Physics)** represent **Real Physics** (measurable fluid mechanics and acoustic signal parameters).
- Because Category A and Categories B/C belong to distinct epistemological domains, they should not be treated as equivalent isotropic coordinates during distance computation without appropriate domain weighting.

---

## 3. Data Processing & Machine Learning Pipeline

1. **Cleaning & Transduction**: Kana/Hangul $\rightarrow$ IPA transducers regenerate all IPA representations and verify originals against phonological databases; features undergo log-normalization, ordinal scaling, and sRGB $\rightarrow$ CIELAB (D65) color transformation.
2. **Dimensionality Reduction & Analysis**: Principal Component Analysis (PCA) reveals effective rank $\approx 3$ (Impact, Mass, Temperature). A strong intrinsic physical correlation exists between $x_2$ Time and $x_8$ Decay ($r \approx 0.83$).
3. **Morphological Template Separation**: Words are decomposed into structural morphological classes (reduplications, geminates, moraic nasals, -ri endings, etc.) to decouple root symbolism from structural template effects.
4. **Phoneme Sub-dictionary & Feature Mapping**: Word roots are expanded into consonant, vowel, voicing, palatalization, and terminal features. Ridge regression models learn a forward mapping from phonological features to 16D vectors.
5. **Sparse Region Detection & Inverse Generation**: Candidate forms are systematically sampled $\rightarrow$ forward vectors are predicted $\rightarrow$ coordinates farthest from existing lexical items are identified via $k$-NN distance $\rightarrow$ candidates are filtered by articulatory constraints $\rightarrow$ 56 novel synthetic onomatopoeia are created.
6. **Deterministic Acoustic Synthesis**: A mapping engine translates 16D vectors directly into Web Audio / Python DSP synthesis parameters (ADSR, FM/subtractive waveforms, granular density, and reverberation).
7. **Empirical D-Axis Calibration**: Audio envelope analysis calibrates phrase-level axes ($x_{13} - x_{16}$) using IOI variation coefficient ($x_{16}$), energy centroid ($x_{13}$), amplitude trend ($x_{14}$), and onset density ($x_{15}$).
8. **Pitch Accent & Prosodic Alignment**: UniDic alignment assigns pitch accent nuclei and flags dialectal or back-loaded prosodic variants.

---

## 4. Key Scientific Findings

- **Physical Law Constraint ($x_2 \times x_8$)**: The correlation between $x_2$ Time (impulse) and $x_8$ Decay ($r \approx 0.82$) remains strong even after removing morphological template effects. This reflects the physical law that sudden impact events decay rapidly.
- **Orthogonality of Temporal Jitter ($x_{16}$) and Spatial Turbulence ($x_9$)**: Rhythmic timing jitter ($x_{16}$) and medium turbulence ($x_9$) are nearly orthogonal in measurement ($r \approx -0.03$), validating the separation of temporal vs. spatial micro-irregularities.
- **Encoder Capacity & Direct Sound Symbolism Limits**: Temperature prediction shows lower fit ($R^2 \approx 0.20$). While Japanese and Korean possess rich thermal-evoking words (*kotokoto*, *hin'yari*, *gutsugutsu*), direct phonetic sound symbolism for heat is limited primarily to aspirated airflow / breath sounds (e.g., inserting *ho-*). Most thermal terms convey temperature indirectly through motion, acoustic resonance, or fluid state.
- **Compositionality via Compounding**: Compound onomatopoeia operate under syntactic compositionality (similar to compound verbs). Compound words combine distinct acoustic blocks (e.g., *kakkīn* = $\langle$*ka'*: sudden impact$\rangle$ + $\langle$*kīn*: sustained resonance$\rangle$). In this pipeline, compounding is bounded to 2-block combinations ($A+B$).

---

## 5. Theoretical References

- **Noguchi, M.** — *Human Being as a Primordial Life Form*: Embodied language and movement exploration.
- **Laban, R.** — *Movement Analysis*: Effort Theory (Weight, Time, Space, Flow).
- **Hayakawa, T., Matsui, S., & Watanabe, J. (2010)** — "Tactile Map of Onomatopoeia," *Transactions of the Virtual Reality Society of Japan*, 15(3), 487–490.
- **TECHTILE (YCAM & Keio University, 2011–2012)** — Haptic-audio cross-modal transformation toolkit.
- **Hamano, S. (1998)** — *The Sound-Symbolic System of Japanese*, CSLI Publications.
- **Sievers, B., Polansky, L., Casey, M., & Wheatley, T. (2013)** — "Music and movement share a dynamic structure that supports universal expressions of emotion," *PNAS*, 110(1), 70–75.
- **Russell, J. (1980)** — "A circumplex model of affect," *JPSP*, 39(6), 1161–1178.
- **Dingemanse, M. (2012)** — Implicational hierarchy of ideophones.
- **Choreographic Lineage**: CCL (Choreographic Coding Lab; The Forsythe Company / Motion Bank), RAM (Reactor for Awareness in Motion, YCAM).

---

## 6. Authorship & Project Evolution

- **Initial Dictionary**: Richi Owaki + Gemini (2025, 708 words)
- **Multilingual Expansion & Redesign (v3)**: Richi Owaki + Claude (2026) — Japanese (2,061 words) and Korean (1,184 words) dictionaries, 16-axis ML vectorization, etymological root origin tags (`stem_bit`), and data-compressed bitmask versions.
