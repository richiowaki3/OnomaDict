# Technical Specification: Onomatopoeia Vector & Classification Schema

This document provides a comprehensive technical specification of the vector structure, metadata, and **bitmask/integer classification schema** used in the Unexplored Onomatopoeia Dictionary (`onomatopoeia_dictionary_jp` and `onomatopoeia_dictionary_kr`).

---

## 1. Epistemological Foundation (Naïve Physics vs. Real Physics)

The physical axes in this dictionary are categorized into two distinct epistemological domains:

- **Naïve Physics (Subjective Perception)**: The quality of movement as perceived and performed by humans (observer-dependent physical model). → **Category A (Laban Effort)**.
- **Real Physics (Objective Physics)**: Physical measurements and fluid dynamics. → **Category B (Acoustic Physics)** and **Category C (Reynolds Fluid Dynamics)**.

> **Caution**: Distance metrics and machine learning models must not treat Category A and Categories B/C as equivalent physical dimensions without proper domain weighting.

---

## 2. Bitmask & Classification Schema

By employing bitwise operations (powers of 2), multiple attributes can be combined into a single integer value (e.g., `Attribute A (1) + Attribute B (256) = 257`), enabling highly efficient filtering and multi-label search with minimal file size.

### 2.1 `cat_bit` — Classical 5-Category Bitmask
Categorizes the fundamental expressive function of the word based on traditional sound symbolism and linguistics.

| Bit Value | Binary | Category Name | Description & Examples |
| :--- | :--- | :--- | :--- |
| **`1`** | `2^0` | **Voice (擬声語 / Phonomime)** | Human or animal voices (e.g., *ahaha*, *bow-wow*, *하하하*) |
| **`2`** | `2^1` | **Sound Effect (擬音語 / Phenomime)** | Inanimate physical or environmental sounds (e.g., *bang*, *drip*, *쿵*) |
| **`4`** | `2^2` | **State & Motion (擬態語 / Psychomime)** | Visual aspects, motions, and physical states (e.g., *sparkling*, *반짝반짝*) |
| **`8`** | `2^3` | **Emotion (擬情語 / Pathomime)** | Psychological states, feelings, and moods (e.g., *fluttering*, *두근두근*) |
| **`16`** | `2^4` | **Somatosensory Pain (擬痛語 / Algomime)** | Sensations of physical pain or discomfort (e.g., *throbbing*, *찌릿찌릿*) |

* **Calculation Example**: A word describing both physical movement (`4`) and pain (`16`) has a `cat_bit` value of `20` ($4 + 16$).

---

### 2.2 `dom_bit` — Sensory & Semantic Domain Bitmask
Defines multi-sensory domains, physical qualities, and contextual applications.

| Bit Value | Binary | Domain Name | Description & Coverage |
| :--- | :--- | :--- | :--- |
| **`1`** | `2^0` | **Texture & Touch** | Surface feel, hardness, elasticity (e.g., smooth, sticky, rough) |
| **`2`** | `2^1` | **Dynamics & Motion** | Physical movement, trajectory, oscillation, impact |
| **`4`** | `2^2` | **Temperature** | Thermal sensations (e.g., piping hot, freezing cold) |
| **`8`** | `2^3` | **Speed & Rhythm** | Tempo, timing, acceleration, burst frequency |
| **`16`** | `2^4` | **Color & Light** | Brightness, luminescence, color patterns (e.g., glittering) |
| **`32`** | `2^5` | **Density & Distance** | Spatial concentration, overcrowding, distance, alignment |
| **`64`** | `2^6` | **Connection & Relation** | Interpersonal intimacy, friction, binding, attachment |
| **`128`** | `2^7` | **Silence & Quietness** | Muffled sounds, quiet environments, tranquility |
| **`256`** | `2^8` | **Taste & Flavor** | Food textures, gustatory sensations (e.g., crispy, juicy) |
| **`512`** | `2^9` | **Mass & Weight** | Heaviness, lightness, gravity impact (e.g., heavy thud) |
| **`1024`** | `2^10` | **Smell & Odor** | Olfactory qualities and scents |
| **`2048`** | `2^11` | **Psychological / Emotion** | Mental states, stress, excitement, relaxation |
| **`4096`** | `2^12` | **Weather & Nature** | Rain, wind, thunder, natural phenomena |
| **`8192`** | `2^13` | **Creatures & Animals** | Animal cries, insect movements, barks, meows |
| **`16384`**| `2^14` | **Physiology & Body** | Internal organ sensations, breathing, pulse, heartbeat |

* **Calculation Example**: A word representing **Texture** (`1`), **Taste** (`256`), and **Emotion** (`2048`) has a `dom_bit` value of `2305` ($1 + 256 + 2048$).

---

### 2.3 `pol_code` — Sentiment Polarity Code (Single Integer)
Represents the affective valence and comfort level associated with the term.

* **`1`**: **Positive / Pleasant (快)** — Comfortable, enjoyable, gentle, or desirable states.
* **`2`**: **Negative / Unpleasant (不快)** — Painful, irritating, uncomfortable, or distressing states.
* **`0`**: **Neutral (中立)** — Objective physical descriptions without inherent emotional polarity.

---

### 2.4 `int_bit` — Phonetic Intensity & Consonant Class Bitmask
Captures phonetic sound symbolism and consonant variation dynamics.

#### Japanese Phonetic System:
* **`1`** (`2^0`): **Voiceless Consonants (清音)** — Light, small, clean, or swift sounds (e.g., *k*, *s*, *t*).
* **`2`** (`2^1`): **Voiced Consonants (濁音)** — Heavy, large, dull, or intense sounds (e.g., *g*, *z*, *d*, *b*).
* **`4`** (`2^2`): **Semi-Voiced Consonants (半濁音)** — Elastic, popping, cute, or springy sounds (e.g., *p*).

#### Korean Consonant Triad System (자음 삼화음):
* **`1`** (`2^0`): **Plain Consonant / 평음** — Standard, baseline intensity (e.g., ㄱ, ㄷ, ㅂ).
* **`2`** (`2^1`): **Aspirated Consonant / 거센소리(격음)** — Light, bursting, or sharp sound (e.g., ㅋ, ㅌ, ㅍ).
* **`4`** (`2^2`): **Tense Consonant / 된소리(경음)** — Hard, dense, or heavy impact (e.g., ㄲ, ㄸ, ㅃ).

---

### 2.5 `tone_code` — Vowel Harmony & Tone Code (Single Integer)
Encodes vowel resonance, pitch, and scale nuances (essential for cross-linguistic acoustic alignment and Korean vowel harmony).

* **`1`**: **Bright / Light / Small Scale (陽母音 / Bright Tone)**
  * High pitch, small object, light motion, cheerful atmosphere.
  * *Japanese*: High/front vowels (a, i, e).
  * *Korean*: Yang vowels (ㅏ, ㅗ, ㅑ).
* **`2`**: **Dark / Heavy / Large Scale (陰母音 / Dark Tone)**
  * Low pitch, massive object, slow/heavy motion, gloomy atmosphere.
  * *Japanese*: Low/back vowels (u, o).
  * *Korean*: Yin vowels (ㅓ, ㅜ, ㅡ).
* **`0`**: **Neutral** — Balanced or compound vowel structure.

---

### 2.6 `morph_bit` — Morphological & Phonological Pattern Bitmask
Encodes structural and rhythmic word formation patterns.

| Bit Value | Binary | Morphological Pattern | Description & Examples |
| :--- | :--- | :--- | :--- |
| **`1`** | `2^0` | **Reduplication (畳語 / 첩어)** | Repeated sound units (e.g., *kira-kira*, *banjjag-banjjag*) |
| **`2`** | `2^1` | **Geminate / Coda (促音 / 받침)** | Contains a glottal stop / pause ("っ" or final consonant) |
| **`4`** | `2^2` | **Moraic Nasal (撥音)** | Contains a moraic nasal ("ん" or final "n/m/ng") |
| **`8`** | `2^3` | **State-Change "-ri" / Single** | Ends in "-ri" denoting state transition, or single-shot root |
| **`16`** | `2^4` | **Prolonged Vowel (長音)** | Contains an extended vowel duration ("ー") |
| **`32`** | `2^5` | **Other / Derivative** | Suffix derivatives (e.g., *-georida*, *-daeda*) or isolated forms |

---

### 2.7 `stem_bit` — Etymological Derivation Origin Bitmask
Identifies the primary lexical source or part-of-speech derivation of the word stem.

| Bit Value | Binary | Derivation Origin | Description & Examples |
| :--- | :--- | :--- | :--- |
| **`1`** | `2^0` | **Primary Onomatopoeia (Mimetic Pure Root)** | Pure sound-symbolic root (e.g., *ton-ton*, *kung*) |
| **`2`** | `2^1` | **Verb-Derived Stem** | Derived from a verb stem (e.g., *koro-koro* $\leftarrow$ *korogaru*) |
| **`4`** | `2^2` | **Noun-Derived Stem** | Derived from a noun (e.g., *nami-nami* $\leftarrow$ *nami* [wave]) |
| **`8`** | `2^3` | **Adjective / Other Stem** | Derived from an adjective or sensory state (e.g., *atsu-atsu* $\leftarrow$ *atsui*) |
| **`16`** | `2^4` | **Adverbial / Functional** | Functional or adverbial roots |
| **`32`** | `2^5` | **Somatic / Body-Derived** | Derived from bodily functions or physiological states |

---

## 3. Core 16 Vector Axes ($x_1 - x_{16}$)

Vector representation: $V = [A / B / C / D]$

### Category A: Laban Effort (Movement Quality / Naïve Physics)
- **`x1` Weight** (0: Light $\leftrightarrow$ 9: Heavy): Kinetic effort quality, internal force/mass.
- **`x2` Time** (0: Sustained $\leftrightarrow$ 9: Sudden): **Attitude toward time** (instant vs. gradual), distinct from sound duration.
- **`x3` Space** (0: Indirect $\leftrightarrow$ 9: Direct): Trajectory focus and straightness.
- **`x4` Flow** (0: Free $\leftrightarrow$ 9: Bound/Inhibited): Impedance, stiffness, and resistance to stopping.

### Category B: Acoustic Physics (Real Physics / Measurements)
- **`x5` Hardness** (0: Rigid $\leftrightarrow$ 9: Fluid): Structural stiffness of sound source.
- **`x6` Moisture** (0: Dry $\leftrightarrow$ 9: Saturated): Tactile/acoustic humidity.
- **`x7_hz` Frequency**: Estimated center frequency in Hz.
- **`x7_norm` Frequency (Normalized)** (0 $\leftrightarrow$ 9): $\log_{10}$ normalized frequency.
- **`x8` Decay / Duration** (0: Sustained/Drone $\leftrightarrow$ 9: Sudden Cutoff/Staccato): Acoustic tail/decay structure.

### Category C: Extended Sensory & Fluid Dynamics
- **`x9_re` Reynolds Number**: Raw Reynolds number ($100 - 20000$) of oral airflow.
- **`x9_norm` Reynolds (Normalized)** (0 $\leftrightarrow$ 9): $\log_{10}$ normalized Reynolds number.
- **`x10` Boyle Number** (0 $\leftrightarrow$ 9): Pressure change, compressibility, and bubble dynamics.
- **`x11` Temperature**: Categorical thermal rating (`ccc`, `cc`, `c`, `mc`, `0`, `mh`, `h`, `hh`, `hhh`).
- **`x11_ord` Temperature (Ordinal)** (0 $\leftrightarrow$ 8): Ordinal numeric representation.
- **`x12` Color**: sRGB color code (HEX format).
- **`L`, `a`, `b` CIELAB Color**: CIELAB D65 color coordinates.

### Category D: Phrasing & Meter (Phrase Scale Temporal Layer)
- **`x13` Accent** (0: Impulse-leading $\leftrightarrow$ 9: Impact-lagging): Peak energy timestamp within phrase.
- **`x14` Contour** (0: Accelerating $\leftrightarrow$ 9: Decelerating): Energy and envelope trend over time.
- **`x15` Meter** (0: Single-shot $\leftrightarrow$ 9: High Density Repetition): Retrigger frequency / onset density.
- **`x16` Regularity** (0: Regular $\leftrightarrow$ 9: Irregular / Jitter): Temporal jitter of onsets (orthogonal to spatial turbulence $x_9$).

---

## 4. License
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Free to use, modify, and distribute with attribution to Richi Owaki and Unexplored Onomatopoeia Dictionary.
