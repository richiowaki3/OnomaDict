# 未開拓オノマトペ辞書 (Unexplored Onomatopoeia Dictionary)

日本語オノマトペ 2,061語を、物理・感覚・運動・リズム・アクセント・メタタグの多層ベクトルおよびビットフラグとして記述した辞書。
旧764語から1,297語を追加拡充し、全語彙に16次元コアベクトルおよびメタタグを採録しています。

身体表現・音響合成・モーション・色彩・自然言語処理など、任意のジャンルへ状態を変換するハブとして使うことを想定しています。

> 手法・理論・パイプラインの詳細は [METHODOLOGY.md](METHODOLOGY.md)（日英併記）を参照。
> See [METHODOLOGY.md](METHODOLOGY.md) for the full methodology, references, and pipeline (JP/EN).

---

## 辞書データの2つのバリエーション（同一データ内容）

本辞書は、用途に合わせて全内容が同一の**2種類のバリエーション（フルバージョン / データ圧縮バージョン）**を提供しています。

### 1. フルバージョン（説明書きあり・人間参照および詳細分析用）
- **data/onomatopoeia_dictionary.csv** (UTF-8, 36列)
- **data/onomatopoeia_dictionary.json** (JSON構造化・整形済み)
- **特徴**: 言葉の意味（meaning）およびベクトル配置の物理・感覚解説文（
ationale）が含まれています。カテゴリー分類は直感的に理解しやすい日本語名称（テキスト表記）で格納されています。

### 2. データ圧縮バージョン（説明書きなし・アプリ高速通信およびビット演算用）
- **data/onomatopoeia_dictionary_compact.csv** (UTF-8, 31列, 約67%軽量化)
- **data/onomatopoeia_dictionary_compact.json** (ミニファイ圧縮, 約79%軽量化)
- **特徴**: アプリケーション通信やリアルタイム処理のために自然文テキスト（meaning, 
ationale, lags）を完全除去。カテゴリー情報は**ビットフラグ（数値）**で格納されており、通信量を大幅削減するとともにビットAND演算 ((dom_bit & 1) != 0) によるミリ秒単位の高速フィルタリングに対応しています。

---

## ベクトル構造（4カテゴリ + アクセント層 + ビットフラグ）

### ビットフラグ・カテゴリ層 (Bitmask Metadata)
- **cat_bit / category**: 古典5分類 (1:擬声語, 2:擬音語, 4:擬態語, 8:擬情語, 16:擬痛語 のビット和)
- **dom_bit / domain**: 感覚・属性ドメイン (1:テクスチャー, 2:ダイナミクス, 4:温度, 8:スピード, 16:色光, 32:密集, 64:関係性, 128:静寂, 256:味, 512:質量, 1024:匂い, 2048:感情, 4096:気象自然, 8192:生き物, 16384:人体生理 のビット和)
- **pol_code / polarity**: 感情価 (1:快, 2:不快, 0:中立)
- **int_bit / intensity**: 音韻強度 (1:清音, 2:濁音, 4:半濁音 のビット和)
- **	one_code / 	one**: 明暗スケール (1:明るい・軽い・小, 2:暗い・重い・大, 0:中立)
- **morph_bit / morphology**: 形態パターン (1:畳語, 2:促音, 4:撥音, 8:「り」変化, 16:長音, 32:その他 のビット和)

### Category A: ラバン・エフォート（瞬間の動きの質）
| キー | 内容 | 範囲 |
|---|---|---|
| effort.weight (x1) | 重さ 0:軽い↔9:重い | 0–9 |
| effort.time (x2) | 時間への態度 0:持続的↔9:突発的（音の長さではない） | 0–9 |
| effort.space (x3) | 空間 0:間接的↔9:直接的 | 0–9 |
| effort.flow (x4) | 流れ 0:自由↔9:抑制 | 0–9 |

### Category B: 音響物理
| キー | 内容 | 範囲 |
|---|---|---|
| acoustic.hardness (x5) | 硬度 0:剛体↔9:流体 | 0–9 |
| acoustic.moisture (x6) | 湿度 0:乾燥↔9:飽和 | 0–9 |
| acoustic.freq_hz (x7) | 周波数 生値 | 100–3500 Hz |
| acoustic.freq_norm | x7のlog10正規化 | 0–9 |
| acoustic.decay (x8) | 減衰 0:持続↔9:突発遮断 | 0–9 |

### Category C: 拡張感覚・物理・心理
| キー | 内容 | 範囲 |
|---|---|---|
| extended.reynolds (x9) | レイノルズ数 生値（層流↔乱流） | 100–20000 |
| extended.reynolds_norm | x9のlog10正規化 | 0–9 |
| extended.boyle (x10) | 圧縮性・気泡特性 | 0–9 |
| extended.temp_code (x11) | 触知温度 | ccc,cc,c,mc,0,mh,h,hh,hhh |
| extended.temp_ord | x11の序数 | 0–8 |
| extended.color_hex (x12) | 色 sRGB HEX | — |
| extended.lab | x12のCIELAB [L*,a*,b*] (D65) | — |

### Category D: フレージング／拍節（複数の動きのまとまり）
| キー | 内容 | 範囲 |
|---|---|---|
| phrasing.accent (x13) | アクセント 0:衝撃先行↔9:蓄勢後発 | 0–9 |
| phrasing.contour (x14) | 推移 0:加速↔9:減勢 | 0–9 |
| phrasing.meter (x15) | 拍 0:単発↔9:高頻度反復 | 0–9 |
| phrasing.regularity (x16) | 規則性 0:規則的↔9:不規則ジッター | 0–9 |

---

## アプリからの参照例

`
# フルバージョン (JSON)
https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/onomatopoeia_dictionary.json

# データ圧縮バージョン (Compact JSON)
https://raw.githubusercontent.com/richiowaki3/OnomaDict/main/data/onomatopoeia_dictionary_compact.json
`

---

## ライセンス
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)（クリエイティブ・コモンズ 表示 4.0 国際）。
商用を含め誰でも自由に利用・改変・再配布できます。クレジット表示（Richi Owaki および本辞書名）をお願いいたします。
