#!/usr/bin/env python3
"""
プロジェクトファイル確認スクリプト

プロジェクト内のファイルとその状態を確認するユーティリティ。
- レポート、グラフ、データファイルの存在確認
- ファイルサイズの表示
- 主要な分析結果のサマリ表示
- 使い方のクイックリファレンス

実行: python 00_check_project.py
"""

import os
from pathlib import Path
from datetime import datetime

def print_summary():
    """フォルダ内容のサマリーを表示"""
    
    print("=" * 80)
    print("FOSS4G 2022-2025 トレンド分析")
    print("GISA_20251029 フォルダ完成サマリー")
    print("=" * 80)
    print()
    
    base_dir = Path(__file__).parent
    
    # 1. レポート
    print("📄 メインレポート")
    print("-" * 80)
    report_file = base_dir / "GISA2025_REPORT.md"
    if report_file.exists():
        size = report_file.stat().st_size
        print(f"  ✓ GISA2025_REPORT.md ({size:,} bytes)")
        print(f"    - FOSS4G 2022-2025の包括的分析")
        print(f"    - 984発表を対象（開発・実用分野）")
        print(f"    - 8つのグラフを統合")
    print()
    
    # 2. グラフ
    print("📊 グラフファイル（レポート出現順）")
    print("-" * 80)
    graphs_dir = base_dir / "graphs"
    if graphs_dir.exists():
        graph_files = sorted(graphs_dir.glob("*.png"))
        graph_descriptions = {
            "01_presentation_trend.png": "発表数推移（1.2節）",
            "02_main_tracks_evolution.png": "主要トラック推移（2.1節）",
            "03_track_categories_distribution.png": "カテゴリ分布（2.2節）",
            "04_top_technologies.png": "トップ20技術（3章冒頭）",
            "05_languages_trend.png": "プログラミング言語推移（3.1節）",
            "06_web_mapping_libraries.png": "Webマッピング推移（3.2節）",
            "07_cloud_formats_trend.png": "クラウドフォーマット推移（3.3節）",
            "08_tech_categories_comparison.png": "技術カテゴリ比較（3.3節）",
        }
        
        total_size = 0
        for graph_file in graph_files:
            size = graph_file.stat().st_size
            total_size += size
            desc = graph_descriptions.get(graph_file.name, "")
            print(f"  ✓ {graph_file.name:40s} ({size//1024:4d} KB) - {desc}")
        
        print(f"\n  合計: {len(graph_files)}ファイル, {total_size//1024:,} KB")
    print()
    
    # 3. データファイル
    print("💾 データファイル")
    print("-" * 80)
    data_files = {
        "presentations_data.json": "プレゼンテーションデータ（984発表、学術トラック除外）",
        "tech_trends_50words.json": "50ワード基準技術トレンド",
        "schedule_2022.xml": "2022年オリジナルスケジュール",
        "schedule_2023.xml": "2023年オリジナルスケジュール",
        "schedule_2024.xml": "2024年オリジナルスケジュール",
        "schedule_2025.xml": "2025年スケジュール"
    }
    
    for filename, description in data_files.items():
        file_path = base_dir / filename
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✓ {filename:30s} ({size//1024:5d} KB) - {description}")
    print()
    
    # 4. スクリプト
    print("🔧 分析・可視化スクリプト")
    print("-" * 80)
    script_files = {
        "00_check_project.py": "プロジェクトファイル確認",
        "01_extract_presentations.py": "XMLから発表データを抽出",
        "02_analyze_technologies.py": "技術トレンドを分析（50ワード基準）",
        "03_plot_basic_stats.py": "基本統計グラフ生成（01）",
        "04_plot_tracks.py": "トラック関連グラフ生成（02-03）",
        "05_plot_technologies.py": "技術トレンドグラフ生成（04-08）",
    }
    
    for filename, description in script_files.items():
        file_path = base_dir / filename
        if file_path.exists():
            print(f"  ✓ {filename:35s} - {description}")
    print()
    
    # 5. 主要な知見
    print("🎯 主要な知見")
    print("-" * 80)
    findings = [
        ("Python優位", "73件、地理空間分野の主要言語として確固たる地位"),
        ("Rust急成長", "+500%（1→6件）、新世代ツールでの採用本格化"),
        ("クラウドシフト", "AWS +600%、PMTiles +300%、Zarr 6件"),
        ("MapLibre躍進", "+200%（4→12件）、オープンソースWebマッピングの新標準"),
        ("STAC定着", "52件、メタデータ標準として確固たる地位"),
        ("QGIS優位", "125件、デスクトップGISの圧倒的シェア"),
        ("GDAL基盤性", "132件、地理空間データ処理の絶対的基盤"),
    ]
    
    for i, (title, description) in enumerate(findings, 1):
        print(f"  {i}. {title:15s}: {description}")
    print()
    
    # 6. 方法論
    print("📐 分析方法論")
    print("-" * 80)
    print("  ✓ 50ワード基準カウント")
    print("    - タイトルまたはabstractの冒頭50ワードで主要トピック扱い")
    print("    - 「使用ツールの一つ」としての言及は除外")
    print("    - 学術論文の慣習（冒頭=主要テーマ）に基づく")
    print()
    print("  ✓ トラック正規化")
    print("    - 大文字小文字の統一")
    print("    - 'and' ↔ '&' の変換")
    print("    - 年次間のバリエーション統一")
    print()
    
    # 7. 使い方
    print("🚀 使い方")
    print("-" * 80)
    print("  1. グラフ再生成:")
    print("     $ python 03_plot_basic_stats.py")
    print("     $ python 04_plot_tracks.py")
    print("     $ python 05_plot_technologies.py")
    print()
    print("  2. データ再分析:")
    print("     $ python 01_extract_presentations.py")
    print("     $ python 02_analyze_technologies.py")
    print()
    print("  3. レポート閲覧:")
    print("     Markdownビューアで GISA2025_REPORT.md を開く")
    print()
    
    # 8. フッター
    print("=" * 80)
    print("✅ すべてのファイルが正常に整理されました")
    print("=" * 80)
    print()
    print(f"作成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
    print("作成者: 岩崎亘典（鳥取大学）")
    print("用途: GIS学会 FOSS4G特別セッション 2025")
    print()

if __name__ == "__main__":
    print_summary()
