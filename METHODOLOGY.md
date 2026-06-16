# 手法と理論的背景 / Methodology and Theoretical Background

> 未開拓オノマトペ辞書 (Unexplored Onomatopoeia Dictionary) の構築手法、使用した理論・論文、データ処理パイプラインの概要。
> Overview of the construction methodology, theoretical references, and data-processing pipeline of the Unexplored Onomatopoeia Dictionary.

---

## 1. 設計思想 / Design Philosophy

**JP:** 本辞書は、日本語オノマトペを「物理・感覚の潜在空間」上の点として記述する。トランスフォーマーが言語を潜在ベクトルへ符号化（encode）し別表層へ復号（decode）する構造を外在化し、感覚を共通の中間表現、各言語の音韻規則を符号化器／復号器とみなす。これにより詩・音楽・舞踊・色を横断する状態変換ハブを目指す。起点は早川・松井・渡邊「オノマトペの触り心地マップ」におけるマトリクスの空白領域——「言い方のない感覚は存在するか」という問い。

**EN:** The dictionary describes Japanese onomatopoeia as points in a latent space of physical and sensory dimensions. It externalizes the transformer encoder/decoder structure: sensation is the shared intermediate representation, and each language's phonological rules act as encoder/decoder. The aim is a cross-modal conversion hub spanning poetry, music, dance, and color. The origin is the blank regions in the onomatopoeia tactile map (Hayakawa, Matsui & Watanabe), and the question: do sensations exist for which no word yet exists?

---

## 2. ベクトル構造 / Vector Structure (16 axes + accent layer)

| Category | Axes | 由来 / Source |
|---|---|---|
| A. Effort | x1 Weight, x2 Time, x3 Space, x4 Flow | Laban Movement Analysis (Effort) |
| B. Acoustic | x5 Hardness, x6 Moisture, x7 Frequency, x8 Decay | 音響物理 / acoustic physics |
| C. Extended | x9 Reynolds, x10 Boyle, x11 Temperature, x12 Color(→CIELAB) | 流体力学・触覚・色彩 / fluid dynamics, haptics, color |
| D. Phrasing | x13 Accent, x14 Contour, x15 Meter, x16 Regularity | フレージング／拍節 / phrasing & meter |
| Accent | UniDic accent type | 東京式アクセント / Tokyo-dialect pitch accent |

**JP:** x2 Time は「時間への態度（突発↔持続）」であり音の長さではない。ADSRはB側の派生。x9 Reynolds・x7 Frequencyは生値を保持しつつlog10正規化列を併設。x11は序数化、x12はsRGB→CIELAB(D65)変換。

**EN:** x2 Time is the *attitude toward time* (sudden vs. sustained), not duration; ADSR is derived on the B side. x9 and x7 keep raw values alongside log10-normalized columns. x11 is ordinalized; x12 is converted sRGB→CIELAB (D65).

---

## 3. パイプライン / Pipeline

**JP:**
1. **クリーニング** — かな→IPA変換器を実装し全語のIPAを機械再生成・原文照合。スケール正規化（log10、序数化、CIELAB）。
2. **次元分析** — 相関行列のPCA。実効次元はおおむね3（衝撃性・質量・温度）。x2×x8に強相関（r≈0.83）。
3. **形態テンプレート分離** — 語を9類型（畳語・促音単発・撥音単発・り単発・長音 等）に分解し、語根とテンプレート効果を分離。
4. **音素サブ辞書** — 語根を子音/母音/濁音/拗音/語尾の素性に展開し、リッジ回帰で素性→ベクトルの順方向モデルを学習（597語根）。
5. **疎領域検出と逆変換** — 候補語形を列挙→順方向モデルで予測→既存語から最遠の座標を選定（k近傍距離）→共鳴条件・調音ジェスチャー制約で選別→56語を生成。
6. **音響合成** — 16軸→ADSR・波形・グラニュラー・残響への決定論的写像（Web Audio / Python一括レンダラ）。
7. **D軸の実測較正** — 合成音エンベロープ解析でx13–x16を測定（IOI変動係数→x16、エネルギー時間重心→x13・τ、振幅トレンド→x14、オンセット密度→x15）。
8. **アクセント層** — UniDic(fugashi/unidic-lite)でアクセント核位置を付与。後ろ寄り語に variant フラグ。

**EN:**
1. **Cleaning** — kana→IPA transducer regenerates all IPA and cross-checks originals; scale normalization (log10, ordinal, CIELAB).
2. **Dimensionality** — PCA on the correlation matrix; effective rank ≈3 (impact / mass / temperature). Strong x2×x8 correlation (r≈0.83).
3. **Morphological template separation** — words decomposed into 9 types (reduplication, geminate-final, moraic-nasal-final, -ri, long-vowel, etc.); roots and template effects separated.
4. **Phoneme sub-dictionary** — roots expanded into consonant/vowel/voicing/palatalization/ending features; ridge regression learns a forward feature→vector model (597 roots).
5. **Sparse-region detection & inverse generation** — enumerate candidate forms → predict vectors → select coordinates farthest from existing words (k-NN distance) → filter by resonance and articulatory-gesture constraints → 56 generated words.
6. **Acoustic synthesis** — deterministic mapping from 16 axes to ADSR, waveform, granular layer, reverb (Web Audio + Python batch renderer).
7. **D-axis empirical calibration** — envelope analysis of synthesized audio measures x13–x16 (IOI coefficient of variation→x16, energy time-centroid→x13/τ, amplitude trend→x14, onset density→x15).
8. **Accent layer** — UniDic (fugashi/unidic-lite) assigns accent-core positions; back-loaded words flagged as variants.

---

## 4. 主要な知見 / Key Findings

**JP:**
- **x2×x8の相関は物理法則**：テンプレート分離後も相関が残存（r≈0.82）。「突発的事象は速く減衰する」現実の制約の反映であり、表記の癖ではない。
- **x16とx9は独立**：拍のジッター(x16)と媒質の乱流(x9)は実測でほぼ直交（r≈−0.03）。Sieversのジッターを時間・空間で分担する設計の妥当性を実証。
- **エンコーダ限界の検出**：温度のモデル適合度が突出して低い（R²≈0.20）。ただしこれは「温度を連想させる語彙が少ない」という意味ではない（ことこと・ぐつぐつ・ほんわか・ひんやり等、連想語は豊富）。**音が温度を直接担う音象徴ルールが手薄**という意味であり、温度を直接背負う資源は気音（「ほ」を挟むと熱くなる：ほんわか・ほっ・しゅぽっ）にほぼ限られ、重さの清濁ルール（トントン→ドンドン）のような汎用性を欠く。温度オノマトペの多くは運動（ことこと＝鍋）・硬さ（かちこち＝凍結）・気流（ひゅーひゅー）を経由した間接表現で、音ベクトルが温度を直接指していないため、音素→温度の直接予測は当たりにくい。一方「突発×持続（鐘の音）」は当初「届かない座標」と誤判定したが、複合（2ブロック合体）で到達可能と判明：「カッキーン」=〈カッ:突発〉+〈キーン:持続〉。後アクセントは振幅アクセント（前重心固定でよい）とピッチアクセント（表記不可視・方言依存）に分離して扱う。
- **複合＝結合性（compositionality）**：オノマトペの複合は複合動詞（「汲み上げる」）と同じ言語の合成原理。中身は突発+持続（カッキーン）に限らず、突発+突発（がたぴし＝戸の連続音）、同時音の並置（しゅーごう＝風切り音＋エンジン低音）もある。現実での継時/同時関係は語に内在せず、適用される現実が決める（解釈は開いておく）。音素(きゃ=k+ゃ)→語根反復(きらきら)→ブロック連結(カッキーン)と同じ合成原理が入れ子で働く。**実装規則：複合は2ブロック（A+B）まで。3ブロック以上（A+B+C）は採らない。**
- **補間と外挿**：生成語は潜在空間内側の補間であり、空間外への外挿ではない。

**EN:**
- **x2×x8 correlation is physical law**: it persists after template separation (r≈0.82), reflecting the real constraint that sudden events decay quickly — not an orthographic artifact.
- **x16 and x9 are independent**: rhythmic jitter (x16) and medium turbulence (x9) are nearly orthogonal in measurement (r≈−0.03), validating the split-assignment of Sievers' jitter across time and space.
- **Encoder-limit detection**: temperature shows markedly low model fit (R²≈0.20). This does *not* mean Japanese lacks temperature-evoking vocabulary (kotokoto, gutsugutsu, honwaka, hin'yari are plentiful). Rather, the **direct sound-symbolic rule** for temperature is thin: the resource that directly carries heat is largely limited to breath sounds (inserting "ho" makes things warm: honwaka, ho', shupo'), lacking the generality of the weight rule (tonton→donton). Most temperature onomatopoeia are indirect — via motion (kotokoto = a pot), hardness (kachikochi = freezing), or airflow (hyūhyū) — so the sound vector does not point at temperature directly, and phoneme→temperature prediction fits poorly. By contrast, "sudden-yet-sustained (bell tones)," initially misjudged as unreachable, turns out reachable via **composition (2-block compounding)**: "kakkīn" = ⟨ka' : sudden⟩ + ⟨kīn : sustained⟩. Back-loaded accent is split into amplitude accent (fix to front) and pitch accent (orthographically invisible, dialect-dependent).
- **Composition = compositionality**: onomatopoeic compounding follows the same principle as compound verbs ("kumi-ageru" = scoop + raise). The pairing is not limited to sudden+sustained (kakkīn); it includes sudden+sudden (gatapishi = a door's repeated knocks) and juxtaposed simultaneous sounds (shūgō = air-cutting hiss + low engine roar). Whether the reality is sequential or simultaneous is not encoded in the word but decided by the referent (interpretation left open). The same compositional principle nests across levels: phoneme (kya = k+ya) → root reduplication (kirakira) → block concatenation (kakkīn). **Implementation rule: compounds are limited to two blocks (A+B); three or more (A+B+C) are not used.**
- **Interpolation vs. extrapolation**: generated words are interpolations within the latent space, not extrapolations beyond it.

---

## 5. 理論的参照 / Theoretical References

- 野口三千三 *原初生命体としての人間* — 身体感覚に基づくことばと動きの探求 / embodied exploration of word and movement.
- Laban, R. — Movement Analysis, Effort theory (Weight/Time/Space/Flow).
- 早川智彦・松井茂・渡邊淳司「オノマトペの触り心地マップ」日本バーチャルリアリティ学会論文誌 15(3), 487–490, 2010 — 起点となる触感マトリクス / originating tactile matrix.
- TECHTILE (YCAM × 慶應義塾大学, 2011–2012) — 触覚と音響信号の相互変換ツールキット / haptic–audio signal toolkit.
- Hamano, S. (1998) *The Sound-Symbolic System of Japanese* — 子音/母音/濁音の音象徴 / sound symbolism (voicing=mass, etc.).
- Sievers, Polansky, Casey & Wheatley (2013) "Music and movement share a dynamic structure," PNAS 110(1):70–75 — 音楽と運動が共有する動的5パラメータ / shared dynamic parameters.
- Russell, J. (1980) "A circumplex model of affect," JPSP 39(6):1161–1178 — 感情の2軸（快不快×覚醒）/ core-affect dimensions.
- Dingemanse, M. (2012) — イデオフォンの含意階層 / implicational hierarchy of ideophones.
- Ekman & Friesen (1969) — 表示規則（表出の文化依存）/ display rules.
- UniDic — 国立国語研究所 / National Institute for Japanese Language and Linguistics (accent data).

### 関連実装系譜 / Related implementation lineage
CCL (Choreographic Coding Lab; The Forsythe Company / Motion Bank), RAM (Reactor for Awareness in Motion, YCAM) — 専門家向け振付・運動解析手法の「解放」という文脈に位置づく。
Positioned within the "liberation" of specialist choreographic/movement-analysis methods via accessible AI tooling.

---

## 6. 制作 / Authorship

- 第1辞書 / First dictionary: Richi Owaki + Gemini (2025, 708 words)
- 設計見直し・本版 / Redesign (this version): Richi Owaki + Claude (2026)
- エフォート理論の機構論的再定式化を別系統と並行 / mechanistic reformulation of Effort theory developed in parallel.
- 今後 / Roadmap: 外国語（韓国語・声調言語）の拡張 / extension to other languages (Korean, tonal languages).
