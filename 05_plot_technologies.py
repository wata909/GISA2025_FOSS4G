#!/usr/bin/env python3
"""
50ワード基準での技術トレンド可視化
"""

import json
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
colors = sns.color_palette("husl", 8)

plt.rcParams.update({
    'font.sans-serif': ['Hiragino Sans', 'Hiragino Kaku Gothic ProN'],
    'font.family': 'sans-serif',
    'axes.unicode_minus': False,
})

Path('graphs').mkdir(exist_ok=True)

with open('tech_trends_50words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = data['results']
years = [2022, 2023, 2024, 2025]

print("グラフ生成開始...")

# 1. トップ20技術
all_techs = []
for category, tech_dict in results.items():
    for tech_name, tech_data in tech_dict.items():
        all_techs.append({'name': tech_name, 'total': tech_data['total']})

all_techs.sort(key=lambda x: x['total'], reverse=True)
top20 = all_techs[:20]

fig, ax = plt.subplots(figsize=(12, 10))
names = [t['name'] for t in top20][::-1]
totals = [t['total'] for t in top20][::-1]
bars = ax.barh(range(len(names)), totals, color=colors[0], alpha=0.8)

for i, (bar, total) in enumerate(zip(bars, totals)):
    ax.text(total + 2, i, str(total), va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=11)
ax.set_xlabel('発表数（4年間合計）', fontsize=12, fontweight='bold')
ax.set_title('トップ20技術（2022-2025、50ワード基準）', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('graphs/04_top_technologies.png', dpi=300, bbox_inches='tight')
print("✓ 04_top_technologies.png")
plt.close()

# 2. プログラミング言語
fig, ax = plt.subplots(figsize=(12, 6))
languages = ['Python', 'JavaScript', 'Java', 'Rust', 'R']
for i, lang in enumerate(languages):
    if lang in results['languages']:
        counts = [results['languages'][lang]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=lang, color=colors[i])

ax.set_xlabel('年', fontsize=12, fontweight='bold')
ax.set_ylabel('発表数', fontsize=12, fontweight='bold')
ax.set_title('プログラミング言語の年次推移（50ワード基準）', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xticks(years)
plt.tight_layout()
plt.savefig('graphs/05_languages_trend.png', dpi=300, bbox_inches='tight')
print("✓ 05_languages_trend.png")
plt.close()

# 3. Webマッピング
fig, ax = plt.subplots(figsize=(12, 6))
web_libs = ['MapLibre', 'OpenLayers', 'Leaflet', 'Cesium', 'deck.gl']
for i, lib in enumerate(web_libs):
    if lib in results['web_mapping']:
        counts = [results['web_mapping'][lib]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=lib, color=colors[i])

ax.set_xlabel('年', fontsize=12, fontweight='bold')
ax.set_ylabel('発表数', fontsize=12, fontweight='bold')
ax.set_title('Webマッピングライブラリの年次推移（50ワード基準）', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xticks(years)
plt.tight_layout()
plt.savefig('graphs/06_web_mapping_libraries.png', dpi=300, bbox_inches='tight')
print("✓ 06_web_mapping_libraries.png")
plt.close()

# 4. クラウドフォーマット
fig, ax = plt.subplots(figsize=(12, 6))
formats = ['COG', 'PMTiles', 'Zarr', 'GeoParquet']
for i, fmt in enumerate(formats):
    if fmt in results['data_formats']:
        counts = [results['data_formats'][fmt]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=fmt, color=colors[i])

ax.set_xlabel('年', fontsize=12, fontweight='bold')
ax.set_ylabel('発表数', fontsize=12, fontweight='bold')
ax.set_title('クラウドネイティブフォーマットの年次推移（50ワード基準）', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xticks(years)
plt.tight_layout()
plt.savefig('graphs/07_cloud_formats_trend.png', dpi=300, bbox_inches='tight')
print("✓ 07_cloud_formats_trend.png")
plt.close()

# 5. 技術カテゴリ比較
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('技術カテゴリ別トレンド比較（50ワード基準）', fontsize=16, fontweight='bold')

ax = axes[0, 0]
desktop = ['QGIS', 'GRASS GIS']
for i, tech in enumerate(desktop):
    if tech in results['desktop_gis']:
        counts = [results['desktop_gis'][tech]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=tech, color=colors[i])
ax.set_title('デスクトップGIS', fontsize=13, fontweight='bold')
ax.set_ylabel('発表数', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

ax = axes[0, 1]
servers = [('GeoServer', 'servers'), ('PostgreSQL', 'databases'), ('GDAL', 'data_processing')]
for i, (tech, category) in enumerate(servers):
    if tech in results[category]:
        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=tech, color=colors[i])
ax.set_title('サーバー・データ処理', fontsize=13, fontweight='bold')
ax.set_ylabel('発表数', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

ax = axes[1, 0]
apis = ['STAC', 'OGC API', 'WMS']
for i, tech in enumerate(apis):
    if tech in results['api_standards']:
        counts = [results['api_standards'][tech]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=tech, color=colors[i])
ax.set_title('API/標準', fontsize=13, fontweight='bold')
ax.set_xlabel('年', fontsize=11)
ax.set_ylabel('発表数', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

ax = axes[1, 1]
cloud_ai = [('AWS', 'cloud_infra'), ('Machine Learning', 'ai_ml'), ('Kubernetes', 'cloud_infra')]
for i, (tech, category) in enumerate(cloud_ai):
    if tech in results[category]:
        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, label=tech, color=colors[i])
ax.set_title('クラウド・AI/ML', fontsize=13, fontweight='bold')
ax.set_xlabel('年', fontsize=11)
ax.set_ylabel('発表数', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

plt.tight_layout()
plt.savefig('graphs/08_tech_categories_comparison.png', dpi=300, bbox_inches='tight')
print("✓ 08_tech_categories_comparison.png")
plt.close()

print("\n完了: すべてのグラフを生成しました")
