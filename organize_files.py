#!/usr/bin/env python3
"""
FOSS4G分析ファイルの整理スクリプト

画像ファイルをレポート内の出現順に01-08にリネームし、
必要なファイルを全てGISA_20251029フォルダにまとめます。
"""

import shutil
import os
from pathlib import Path

# ソースディレクトリとターゲットディレクトリ
source_dir = Path(__file__).parent.parent
target_dir = Path(__file__).parent

# レポート内の出現順に画像ファイルをマッピング
# 新ファイル名: 旧ファイル名
image_mapping = {
    '01_presentation_trend.png': '03_presentation_trend.png',
    '02_main_tracks_evolution.png': '01_main_tracks_evolution.png',
    '03_track_categories_distribution.png': '02_track_categories_distribution.png',
    '04_top_technologies.png': '08_top_technologies_50words.png',
    '05_languages_trend.png': '04_languages_trend_50words.png',
    '06_web_mapping_libraries.png': '06_web_mapping_libraries_50words.png',
    '07_cloud_formats_trend.png': '05_cloud_formats_trend_50words.png',
    '08_tech_categories_comparison.png': '07_tech_categories_comparison_50words.png',
}

# データファイルのリスト
data_files = [
    'gis_society_analysis.json',
    'tech_trends_50words.json',
    'schedule_2022.xml',
    'schedule_2023.xml',
    'schedule_2024.xml',
    'schedule_2025.xml',
]

# スクリプトファイルのリスト
script_files = [
    'analyze_gis_society.py',
    'analyze_tech_trends_50words.py',
    'visualize_gis_society.py',
    'visualize_statistics.py',
    'visualize_trends_50words.py',
]

def main():
    print("=" * 60)
    print("FOSS4G分析ファイルの整理")
    print("=" * 60)
    
    # 1. 画像ファイルのコピーとリネーム
    print("\n1. 画像ファイルをコピー中...")
    graphs_source = source_dir / 'graphs'
    graphs_target = target_dir / 'graphs'
    
    for new_name, old_name in image_mapping.items():
        source_file = graphs_source / old_name
        target_file = graphs_target / new_name
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"  ✓ {old_name:40s} → {new_name}")
        else:
            print(f"  ✗ {old_name} が見つかりません")
    
    # 2. データファイルのコピー
    print("\n2. データファイルをコピー中...")
    for filename in data_files:
        source_file = source_dir / filename
        target_file = target_dir / filename
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} が見つかりません")
    
    # 3. スクリプトファイルのコピー
    print("\n3. スクリプトファイルをコピー中...")
    for filename in script_files:
        source_file = source_dir / filename
        target_file = target_dir / filename
        
        if source_file.exists():
            shutil.copy2(source_file, target_file)
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} が見つかりません")
    
    # 4. README.mdのコピー（レポートの更新版を作成）
    print("\n4. レポートを作成中...")
    
    print("\n" + "=" * 60)
    print("✓ ファイルの整理が完了しました")
    print("=" * 60)
    print(f"\n出力先: {target_dir}")
    print("\nファイル構成:")
    print("  ├── graphs/          # グラフ画像（01-08）")
    print("  ├── *.py             # 分析スクリプト")
    print("  ├── *.json           # データファイル")
    print("  ├── *.xml            # スケジュールデータ")
    print("  └── GIS_SOCIETY_REPORT.md  # 分析レポート")

if __name__ == '__main__':
    main()
