# Unexplored Onomatopoeia & Ideophone Dictionary (JP, KR, AF)

A cross-lingual multidimensional vector dictionary of Japanese (JP: 2,061 words / 1,066 seeds), Korean (KR: 5,050 words / 2,985 seeds), and African Ideophones (AF: 245 seed entries across 9 languages), formalized across physical, sensory, motion, rhythm, accent, and sound-symbolic metadata.

Designed as a conversion hub across choreography, acoustic synthesis, computer graphics, motion design, lighting, and natural language processing.

> For theoretical methodology, references, and pipeline details, see [METHODOLOGY.md](METHODOLOGY.md).

---

## Multilingual Directory Structure

The Japanese (JP), Korean (KR), and African Ideophone (AF) dictionaries are organized into independent directories. Japanese and Korean provide **Full Versions (2,061 and 5,050 entries)** alongside **Data-Compressed Versions (Numeric Bitmasks & Seed Compression)**, while African Ideophones provide a dedicated **Seed-Compressed Dictionary (245 seed entries)**.

```
data/
├── jp/  (Japanese Onomatopoeia Dictionary)
│   ├── onomatopoeia_dictionary_jp.csv           ← Full Version (2,061 entries)
│   ├── onomatopoeia_dictionary_jp.json          ← Full Version JSON (2,061 entries)
│   ├── onomatopoeia_dictionary_jp_compact.csv   ← Data-Compressed Version CSV (2,061 entries)
│   ├── onomatopoeia_dictionary_jp_compact1.json ← Data-Compressed Version JSON 1 (Numeric bitmasks, 2,061 entries)
│   └── onomatopoeia_dictionary_jp_compact2.json ← Data-Compressed Version JSON 2 (Seed Compression / 語根圧縮, 1,066 seed entries)
├── kr/  (Korean Onomatopoeia Dictionary)
│   ├── onomatopoeia_dictionary_kr.csv           ← Full Version (5,050 entries)
│   ├── onomatopoeia_dictionary_kr.json          ← Full Version JSON (5,050 entries)
│   ├── onomatopoeia_dictionary_kr_compact.csv   ← Data-Compressed Version CSV (5,050 entries)
│   ├── onomatopoeia_dictionary_kr_compact1.json ← Data-Compressed Version JSON 1 (Numeric bitmasks, 5,050 entries)
│   └── onomatopoeia_dictionary_kr_compact2.json ← Data-Compressed Version JSON 2 (Seed Compression / 語根圧縮, 2,985 seed entries)
└── af/  (African Ideophones Dictionary - Seed Compression / 語根圧縮)
    └── onomatopoeia_dictionary_af_compact2.json ← Seed-Compressed Version JSON 2 (245 seed entries, 9 African languages)
```

---

## Dataset Variations

### 1. Full Version (onomatopoeia_dictionary_XX.csv / .json)
- **Features**: Includes English definitions (`meaning_en`), English sound-symbolic rationales (`rationale`), Romanization / pronunciation, tone patterns, and category names.

### 2. Data-Compressed Version 1 (onomatopoeia_dictionary_XX_compact1.json / .csv)
- **Features**: Removes natural language text (`meaning_en`, `rationale`, `flags`) to minimize payload size (65–80% size reduction). Category metadata is represented as **numeric bitmasks** or compact codes for millisecond-level filtering.

### 3. Seed-Compressed Version 2 (onomatopoeia_dictionary_XX_compact2.json / 語根圧縮)
- **Features**: Decomposes words into core sound-symbolic **Seeds (語根)** and **Delta Modifiers** (consonant shifts, vowel tone shifts, morphological templates). Allows AI engines and client runtimes to reconstruct 16D vectors programmatically with maximum token efficiency.

---

## Vector Schema (16 Axes + Accent + Metadata)

### Category Metadata
- **Category (category / cat_bit)**: Phonomime (Voice: 1), Phenomime (Sound: 2), Psychomime (State/Manner: 4), Pathomime (Emotion: 8), Algomime (Pain: 16).
- **Domain (domain / dom_bit)**: Texture (1), Dynamics (2), Temperature (4), Speed/Tempo (8), Color/Light (16), Density/Distance (32), Relationship (64), Silence (128), Taste (256), Mass/Weight (512), Smell (1024), Emotion (2048), Weather/Nature (4096), Living Beings (8192), Human Body/Physiology (16384).
- **Polarity (polarity / pol_code)**: Positive (1), Negative (2), Neutral (0).
- **Intensity (intensity / int_bit)**: Unvoiced/Light (1), Voiced/Heavy (2), Semi-voiced/Crisp (4).
- **Tone (tone / tone_code)**: Bright/Light/Small (1), Dark/Heavy/Large (2), Neutral (0).
- **Morphology (morphology / morph_bit)**: Reduplication (1), Geminate (2), Moraic Nasal (4), -ri Ending (8), Long Vowel (16), Single/Other (32).
- **Stem Origin (stem_origin / stem_bit)**: Mimetic Pure Root (1), Verb-derived (2), Adjective-derived (4), Noun-derived (8), Adverbial/Functional (16), Somatic/Body-derived (32).

### Category A: Laban Effort (Instantaneous Movement Quality)
- effort.weight (x1): Weight (0: Light ↔ 9: Heavy)
- effort.time (x2): Attitude toward Time (0: Sustained ↔ 9: Sudden)
- effort.space (x3): Space (0: Indirect ↔ 9: Direct)
- effort.flow (x4): Flow (0: Free ↔ 9: Bound/Inhibited)

### Category B: Acoustic Physics
- acoustic.hardness (x5): Hardness (0: Rigid ↔ 9: Fluid)
- acoustic.moisture (x6): Moisture (0: Dry ↔ 9: Saturated)
- acoustic.freq_hz (x7_hz): Acoustic Frequency (100–3500 Hz / African Tone scaling)
- acoustic.freq_norm (x7_norm): log10 / linear Normalized Frequency (0–1 or 0–9)
- acoustic.decay (x8): Sound Decay (0: Sustained ↔ 9: Sudden Cutoff)

### Category C: Extended Sensory & Fluid Dynamics
- extended.reynolds (x9_re): Reynolds Number (100–20000) / Period
- extended.reynolds_norm (x9_norm): Normalized Reynolds / Period (0–1 or 0–9)
- extended.boyle (x10): Boyle Number / Arousal Intensity (0–1 or 0–9)
- extended.temp_code (x11): Tactile Temperature / Impact Hardness
- extended.temp_ord (x11_ord): Temperature / Hardness Grade (1–5)
- extended.color_hex (x12): sRGB Color HEX
- extended.lab (L, a, b): CIELAB Color Coordinates (D65)

### Category D: Phrasing & Meter (Phrase Scale)
- phrasing.accent (x13): Peak Timestamp / Tone Pattern Code (0: Monotone Low, 1: High, 2: Falling, 3: Rising, 4: Complex)
- phrasing.contour (x14): Envelope Trend / Frequency Contour Slope
- phrasing.meter (x15): Onset Density / Metric Regularity
- phrasing.regularity (x16): Rhythmic / Tactile Surface Regularity

---

## Raw URL Access

### Japanese (JP)
- Full JSON (2,061 entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/jp/onomatopoeia_dictionary_jp.json
- Compact JSON 1 (Numeric Bitmasks, 2,061 entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/jp/onomatopoeia_dictionary_jp_compact1.json
- Compact JSON 2 (Seed Compression / 語根圧縮, 1,066 seed entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/jp/onomatopoeia_dictionary_jp_compact2.json

### Korean (KR)
- Full JSON (5,050 entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/kr/onomatopoeia_dictionary_kr.json
- Compact JSON 1 (Numeric Bitmasks, 5,050 entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/kr/onomatopoeia_dictionary_kr_compact1.json
- Compact JSON 2 (Seed Compression / 語根圧縮, 2,985 seed entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/kr/onomatopoeia_dictionary_kr_compact2.json

### African Ideophones (AF: 9 Languages)
- Seed-Compressed JSON (語根圧縮, 245 seed entries): https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/af/onomatopoeia_dictionary_af_compact2.json

---

## License
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (Creative Commons Attribution 4.0 International).
Feel free to use, modify, and redistribute. Please credit Richi Owaki and Unexplored Onomatopoeia Dictionary.
