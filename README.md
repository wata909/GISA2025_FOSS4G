# FOSS4G 2022-2025 トレンド分析プロジェクト

**GIS学会 FOSS4G特別セッション 2025**  
**分析者**: 岩崎亘典（鳥取大学）  
**最終更新**: 2025年10月29日

---

## 🎯 このプロジェクトについて

このプロジェクトは、**FOSS4G国際会議（2022-2025年）の4年間の発表内容を分析**し、オープンソース地理空間技術のトレンドを明らかにするものです。

### プロジェクトの目的

1. **開発・実用トレンドの可視化**: Academic Track以外を対象に、技術の動向を把握
2. **技術の主流化の定量評価**: 「タイトルや冒頭で言及される」= 主要テーマとして扱われる技術を抽出
3. **GIS学会への知見提供**: 日本の地理空間情報コミュニティに向けた情報発信

### 分析の特徴

- ✅ **アカデミックトラックを除外**: 実務・開発動向に焦点
- ✅ **50ワード基準**: タイトルまたはabstractの冒頭50ワードに言及される技術のみカウント（主要トピックの識別）
- ✅ **4年間の時系列分析**: 2022-2025の変化を追跡
- ✅ **984件の発表を分析**: 総発表数1,038件からAcademicトラックを除外

---

## 📁 ファイル構成

```text
GISA_20251029/
├── README.md                           # このファイル
├── requirements.txt                    # Python依存パッケージ一覧
├── GIS_SOCIETY_REPORT.md               # 📄 分析レポート（メイン成果物）
│
├── 📊 graphs/                          # グラフ画像（レポート掲載順）
│   ├── 01_presentation_trend.png       # 発表数推移
│   ├── 02_main_tracks_evolution.png    # 主要トラック推移
│   ├── 03_track_categories_distribution.png  # カテゴリ分布
│   ├── 04_top_technologies.png         # トップ20技術
│   ├── 05_languages_trend.png          # プログラミング言語推移
│   ├── 06_web_mapping_libraries.png    # Webマッピングライブラリ推移
│   ├── 07_cloud_formats_trend.png      # クラウドフォーマット推移
│   └── 08_tech_categories_comparison.png  # 技術カテゴリ比較
│
├── 📁 データファイル（入力）
│   ├── schedule_2022.xml               # FOSS4G 2022 公式スケジュール
│   ├── schedule_2023.xml               # FOSS4G 2023 公式スケジュール
│   ├── schedule_2024.xml               # FOSS4G 2024 公式スケジュール
│   └── schedule_2025.xml               # FOSS4G 2025 公式スケジュール
│
├── 📁 データファイル（出力）
│   ├── gis_society_analysis.json       # GIS学会向け分析データ（984発表）
│   └── tech_trends_50words.json        # 50ワード基準技術トレンド
│
└── 🐍 Pythonスクリプト
    ├── analyze_gis_society.py          # データ抽出（アカデミック除外）
    ├── analyze_tech_trends_50words.py  # 技術トレンド分析（50ワード基準）
    ├── visualize_statistics.py         # 基本統計グラフ生成
    ├── visualize_gis_society.py        # GIS学会向けグラフ生成
    ├── visualize_trends_50words.py     # 技術トレンドグラフ生成
    ├── organize_files.py               # ファイル整理ユーティリティ
    └── summary.py                      # サマリ生成
```

---

## 分析手法の詳細

### 1. データ抽出とフィルタリング

#### アカデミックトラック除外
- FOSS4G会議には「Academic Track」が存在し、査読付き学術論文が発表される
- 本分析では**開発・実用の動向**に焦点を当てるため、これを除外
- 対象: 984件（全1,038件から学術54件を除外）

#### 除外対象
- 学術トラック（Academic Track）
- 非発表イベント（休憩、昼食、レセプション等）

### 2. 50ワード基準カウント

技術が「主要トピック」として扱われているかを判定する基準：

- ✅ **カウント対象**: タイトル **または** abstractの冒頭50ワードに言及
- ❌ **カウント対象外**: 後半部分のみの言及（サブツールとしての使用）

**基準の根拠:**
- 学術論文の慣習: 冒頭部分に主要テーマを提示
- タイトルへの言及: 最も重要なトピックである証拠
- 50ワード: abstractの主要部分（背景・目的）をカバーする適切な長さ

**例:**
```text
✅ "Python-based geospatial analysis using OpenStreetMap data..."
   → Pythonが主要トピック

❌ "...we implemented the tool using Python and PostgreSQL"
   → Pythonは実装詳細、主要トピックではない
```

### 3. トラック名正規化

年度間のトラック名のバリエーションを統一：

- 大文字小文字の統一: `use cases` → `Use cases`
- 記号の統一: `and` ↔ `&` の変換
- スペースの正規化

---

## 📊 主要な分析結果

### 発見1: プログラミング言語トレンド

| 言語 | 総言及数 | トレンド |
|------|----------|----------|
| **Python** | 73件 | 🟢 安定的な優位性 |
| **Rust** | 6件 | 🚀 +500% 成長（1→6件） |
| **JavaScript** | 21件 | 🟢 Web分野で安定 |
| **TypeScript** | 10件 | 📈 型安全性への移行 |

### 発見2: Webマッピングライブラリ

| ライブラリ | 総言及数 | トレンド |
|-----------|----------|----------|
| **MapLibre** | 12件 | 🚀 +200% 成長（4→12件） |
| **Leaflet** | 11件 | 🟢 安定的な人気 |
| **OpenLayers** | 19件 | 🟢 エンタープライズで強固 |

### 発見3: クラウドネイティブ技術

| 技術 | 総言及数 | トレンド |
|------|----------|----------|
| **STAC** | 52件 | ⭐ デファクトスタンダード |
| **PMTiles** | 7件 | 🚀 +300% 成長 |
| **Zarr** | 6件 | 🆕 新フォーマット台頭 |
| **AWS** | 14件 | � +600% 成長 |

### 発見4: トラック構成の変化

- **Use cases & applications**: 最大カテゴリ（33-40%）
- **State of software**: 安定的な第2位（22-30%）
- **Academic Track**: 2023年に明示的に分離（2022年は混在）

---

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# リポジトリのディレクトリに移動
cd GISA_20251029

# 必要なパッケージをインストール
pip install -r requirements.txt
```

### 2. データ分析の実行

```bash
# ステップ1: XMLデータから分析データを生成
python analyze_gis_society.py          # → gis_society_analysis.json
python analyze_tech_trends_50words.py  # → tech_trends_50words.json

# ステップ2: グラフを生成
python visualize_statistics.py         # → graphs/01-03
python visualize_gis_society.py        # → graphs/追加グラフ
python visualize_trends_50words.py     # → graphs/04-08
```

### 3. 結果の確認

```bash
# レポートを開く
open GIS_SOCIETY_REPORT.md

# グラフを確認
open graphs/
```

---

## 📈 生成されるグラフ一覧

### 1. 基本統計

| グラフ | 説明 | レポート箇所 |
|--------|------|--------------|
| 01_presentation_trend.png | 発表数の年次推移 | 1.2節 |
| 02_main_tracks_evolution.png | 主要トラックの推移（積み上げ棒グラフ） | 2.1節 |
| 03_track_categories_distribution.png | トラックカテゴリ分布（4年分） | 2.2節 |

### 2. 技術トレンド（50ワード基準）

| グラフ | 説明 | レポート箇所 |
|--------|------|--------------|
| 04_top_technologies.png | トップ20技術（横棒グラフ） | 3章冒頭 |
| 05_languages_trend.png | プログラミング言語推移 | 3.1節 |
| 06_web_mapping_libraries.png | Webマッピングライブラリ推移 | 3.2節 |
| 07_cloud_formats_trend.png | クラウドネイティブフォーマット推移 | 3.3節 |
| 08_tech_categories_comparison.png | 技術カテゴリ4パネル比較 | 3.3節 |

## 📝 データ形式

### 入力: XMLスケジュールファイル

FOSS4G公式サイトから取得したスケジュールXML:

```xml
<schedule>
  <conference>
    <title>FOSS4G 2024</title>
    <start>2024-12-02</start>
    <end>2024-12-08</end>
  </conference>
  <day date="2024-12-03">
    <room name="Plenary">
      <event id="123">
        <title>Building scalable geospatial pipelines with Python</title>
        <track>Use cases &amp; applications</track>
        <type>talk</type>
        <abstract>We present a Python-based approach...</abstract>
      </event>
    </room>
  </day>
</schedule>
```

### 出力1: gis_society_analysis.json

年度別の統計サマリ:

```json
[
  {
    "year": 2024,
    "total_presentations": 253,
    "academic_presentations": 21,
    "non_academic_presentations": 232,
    "tracks": {
      "Use cases & applications": 93,
      "State of software": 74,
      "Community & foundation": 34,
      "Academic Track": 21,
      "Cartography": 18,
      "Education & outreach": 13
    },
    "track_categories": {
      "practical": 93,
      "technical": 74,
      "community": 34,
      "academic": 21,
      "specialized": 31
    }
  }
]
```

### 出力2: tech_trends_50words.json

技術別・年度別の詳細カウント:

```json
{
  "metadata": {
    "criteria": "50ワード基準",
    "description": "タイトル or abstractの冒頭50ワード以内で主要トピックとして扱われた発表のみカウント",
    "total_analyzed": 984
  },
  "results": {
    "languages": {
      "Python": {
        "total": 73,
        "yearly": {"2022": 23, "2023": 11, "2024": 20, "2025": 19}
      },
      "Rust": {
        "total": 6,
        "yearly": {"2022": 1, "2023": 0, "2024": 3, "2025": 2}
      }
    },
    "web_mapping": {
      "MapLibre": {
        "total": 12,
        "yearly": {"2022": 4, "2023": 3, "2024": 3, "2025": 2}
      }
    }
  }
}
```

---

## ️ 技術スタック

このプロジェクトで使用している技術:

- **Python 3.8+**: スクリプト言語
- **matplotlib**: グラフ描画
- **seaborn**: 統計的可視化
- **numpy**: 数値計算
- **pandas**: データ分析（オプション）
- **lxml**: XML高速パース

---

## 📚 参考情報

- **FOSS4G公式サイト**: <https://foss4g.org/>
- **OSGeo Foundation**: <https://www.osgeo.org/>
- **FOSS4G 2026 Hiroshima**: （準備中）
- **GIS学会FOSS4G分科会**: <https://sites.google.com/site/foss4gsig/>

---

## 📖 関連ドキュメント

- `GIS_SOCIETY_REPORT.md`: 詳細な分析レポート（メイン成果物）
- `graphs/`: 8つの可視化グラフ
- `*.json`: 機械可読な分析結果データ

---

## 🤝 貢献

このプロジェクトはGIS学会FOSS4G分科会の活動の一環です。改善提案やバグ報告は歓迎します。

---

## 📧 お問い合わせ

**岩崎亘典**  
鳥取大学  
GIS学会 FOSS4G分科会

---

## 📄 ライセンス

このデータおよび分析結果は、GIS学会FOSS4G特別セッション2025での発表資料として作成されました。

---

**更新履歴**:

- 2025-10-29: READMEを全面改訂、プロジェクト概要を明確化
- 2025-01: 初版作成
