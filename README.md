# 未開拓オノマトペ辞書 (Unexplored Onomatopoeia Dictionary)

日本語オノマトペ 764語を、物理・感覚・運動・リズム・アクセントの多層ベクトルとして記述した辞書。
うち708語は既存語、56語は意味空間の空白（疎領域）を埋めるために生成された新語（`generated: true`）。

身体表現・音響合成・モーション・色彩など、任意のジャンルへ状態を変換するハブとして使うことを想定している。

> 手法・理論・パイプラインの詳細は [METHODOLOGY.md](METHODOLOGY.md)（日英併記）を参照。
> See [METHODOLOGY.md](METHODOLOGY.md) for the full methodology, references, and pipeline (JP/EN).

## 最新版ファイル

- **`data/onomatopoeia_dictionary.json`** — アプリ参照用（推奨。カテゴリ別に入れ子化）
- **`data/onomatopoeia_dictionary.csv`** — 表計算・分析用（UTF-8 BOM付き、36列フラット）
- `archive/` — 旧版（v1: 12軸 / v2: 16軸）。参照用に保存。

## ベクトル構造（4カテゴリ + アクセント層）

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
| phrasing.accent (x13) | アクセント 0:衝撃先行↔9:蓄勢後発 ※下記注 | 0–9 |
| phrasing.contour (x14) | 推移 0:加速↔9:減勢 | 0–9 |
| phrasing.meter (x15) | 拍 0:単発↔9:高頻度反復 | 0–9 |
| phrasing.regularity (x16) | 規則性 0:規則的↔9:不規則ジッター | 0–9 |
| phrasing.tau | 3点キーフレームのピーク時刻（時間重心, 0–1） | 0–1 |

x14/x15/x16 は合成音のエンベロープ解析による実測値。x13 は合成音からは
真値が出ない（前重心に縮退する）ため、形態型由来のprior値（`x13_status`参照）。

### アクセント層（UniDicによる東京式アクセント）
| キー | 内容 |
|---|---|
| accent.unidic_atype | アクセント核位置（0=平板, 1=頭高, 2以上=中高/尾高）。生成語等はnull |
| accent.accent_class | 頭高/中高・尾高/平板 |
| accent.default | front / back / flat |
| accent.variant | true=アクセントで意味が割れうる語（後ろ寄り237語。人手較正・方言対応の保留地） |
| accent.source | whole=語全体一致 / firsttoken=複合の先頭語 |

東京式のみ。方言差（関西「二時/虹」、山口「山口県/山口市」等）とオノマトペ固有の
ずれ、生成語のアクセントは未較正。`accent.variant=true` の語が要確認リスト。

### メタ情報
- `morph_type` — 形態型（畳語/促音単発/撥音単発/長音/複合異種 等9類型）
- `generated` — 生成語フラグ（疎領域充填、56語）

## 正規化の定義
- `freq_norm` = (log10(Hz) − log10(100)) / (log10(3500) − log10(100)) × 9
- `reynolds_norm` = (log10(Re) − log10(100)) / (log10(20000) − log10(100)) × 9

## 設計上の注意
- Category A（x1–x4）は確定・凍結。x2は「時間への態度」であり音の長さ・ADSRではない。
- x2とx8には強い相関（r≈0.83）があるが、これは「突発的な事象は速く減衰する」物理的制約の反映。
- x16（拍ジッター）とx9（媒質乱流）は独立（実測 r≈−0.03）。
- 生成語56語のベクトルは音素サブ辞書による予測値、色はモデル導出の暫定値。

## アプリからの参照

公開リポジトリ:
```
https://raw.githubusercontent.com/<user>/<repo>/main/data/onomatopoeia_dictionary.json
```

## 来歴
- オノマトペの語彙の空白をテーマとしたパフォーマンス制作が前提。
- 第1辞書: Richi Owaki + Gemini（2025年末、708語）。
- 設計見直し: Richi Owaki + Claude（2026年6月）。クリーニング、PCA、形態テンプレート分離、
  音素サブ辞書、疎領域の逆変換による56語生成、音響合成、D軸（フレージング）の実測較正、
  UniDicによるアクセント層付与。
- エフォート理論の機構論的再定式化を別系統と並行（A/D軸の設計根拠）。
- 今後: 外国語（韓国語・声調言語等）の拡張を予定。

### 理論的参照
Noguchi『原初生命体としての人間』, Laban (Effort), 早川・松井・渡邊「オノマトペの触り心地マップ」(2010),
TECHTILE (YCAM×慶應), Hamano (1998), Sievers et al. PNAS (2013), Russell (1980),
Dingemanse (2012), UniDic（国立国語研究所）.

## ライセンス
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)（クリエイティブ・コモンズ 表示 4.0 国際）。
商用を含め誰でも自由に利用・改変・再配布できます。条件はクレジット表示（Richi Owaki および本辞書名）のみ。
アクセント層はUniDic（国立国語研究所）を用いて付与。詳細はLICENSEファイル参照。
