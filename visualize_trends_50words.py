""""""

50ワード基準での技術トレンド可視化50ワード基準での技術トレンド可視化

"""

レポート内の出現順：

  04_top_technologies.png (3章冒頭)import json

  05_languages_trend.png (3.1節)import matplotlib

  06_web_mapping_libraries.png (3.2節)# バックエンド設定の前にフォントを設定

  07_cloud_formats_trend.png (3.3節)matplotlib.use('Agg')  # GUIなしバックエンド

  08_tech_categories_comparison.png (3.3節)

"""import matplotlib.pyplot as plt

import matplotlib.font_manager as fm

import jsonimport seaborn as sns

import matplotlibimport numpy as np

# バックエンド設定from pathlib import Path

matplotlib.use('Agg')import warnings



import matplotlib.pyplot as plt# フォント警告を抑制

import seaborn as snswarnings.filterwarnings('ignore', message='Glyph .* missing from font')

import numpy as npwarnings.filterwarnings('ignore', category=UserWarning)

from pathlib import Path

import warnings# スタイル設定（フォント設定の前に）

sns.set_style("whitegrid")

# フォント警告を抑制colors = sns.color_palette("husl", 8)

warnings.filterwarnings('ignore', message='Glyph .* missing from font')

warnings.filterwarnings('ignore', category=UserWarning)# 日本語フォントを明示的に設定（seabornの後に設定して上書き）

plt.rcParams.update({

# スタイル設定（フォント設定の前に）    'font.sans-serif': ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic'],

sns.set_style("whitegrid")    'font.family': 'sans-serif',

colors = sns.color_palette("husl", 8)    'axes.unicode_minus': False,

})

# 日本語フォント設定（seabornの後に設定して上書き）

plt.rcParams.update({print(f"使用するフォント: {plt.rcParams['font.sans-serif'][0]}")

    'font.sans-serif': ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', 'Meiryo'],print(f"実際のfont.family: {plt.rcParams['font.family']}")

    'font.family': 'sans-serif',

    'axes.unicode_minus': False,# グラフディレクトリ作成

})Path('graphs').mkdir(exist_ok=True)



print(f"使用するフォント: {plt.rcParams['font.sans-serif'][0]}")# データ読み込み

with open('tech_trends_50words.json', 'r', encoding='utf-8') as f:

# グラフディレクトリ作成    data = json.load(f)

Path('graphs').mkdir(exist_ok=True)

results = data['results']

# データ読み込みyears = [2022, 2023, 2024, 2025]

with open('tech_trends_50words.json', 'r', encoding='utf-8') as f:

    data = json.load(f)# ===== 1. プログラミング言語の推移 =====

fig, ax = plt.subplots(figsize=(12, 6))

results = data['results']

years = [2022, 2023, 2024, 2025]languages = ['Python', 'JavaScript', 'Java', 'Rust', 'R']

for i, lang in enumerate(languages):

# ===== 1. トップ20技術（横棒グラフ） =====    if lang in results['languages']:

# レポート内位置: 3章冒頭        counts = [results['languages'][lang]['yearly'].get(str(year), 0) for year in years]

# ファイル名: 04_top_technologies.png        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

                label=lang, color=colors[i])

# 全技術を合計でソート

all_techs = []ax.set_xlabel('年', fontsize=12, fontweight='bold')

for category, tech_dict in results.items():ax.set_ylabel('発表数', fontsize=12, fontweight='bold')

    for tech_name, tech_data in tech_dict.items():ax.set_title('プログラミング言語の年次推移（50ワード基準）\nタイトルまたはabstract冒頭50ワードで主要トピック扱い', 

        all_techs.append({             fontsize=14, fontweight='bold', pad=20)

            'name': tech_name,ax.legend(fontsize=11, loc='best')

            'total': tech_data['total']ax.grid(True, alpha=0.3)

        })ax.set_xticks(years)



all_techs.sort(key=lambda x: x['total'], reverse=True)plt.tight_layout()

top20 = all_techs[:20]plt.savefig('graphs/04_languages_trend_50words.png', dpi=300, bbox_inches='tight')

print("✓ graphs/04_languages_trend_50words.png を生成")

fig, ax = plt.subplots(figsize=(12, 10))plt.close()



names = [t['name'] for t in top20][::-1]# ===== 2. クラウドネイティブフォーマットの推移 =====

totals = [t['total'] for t in top20][::-1]fig, ax = plt.subplots(figsize=(12, 6))



bars = ax.barh(range(len(names)), totals, color=colors[0], alpha=0.8)formats = ['COG', 'PMTiles', 'Zarr', 'GeoParquet']

for i, fmt in enumerate(formats):

# 各バーに数値を表示    if fmt in results['data_formats']:

for i, (bar, total) in enumerate(zip(bars, totals)):        counts = [results['data_formats'][fmt]['yearly'].get(str(year), 0) for year in years]

    ax.text(total + 2, i, str(total), va='center', fontsize=10, fontweight='bold')        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

                label=fmt, color=colors[i])

ax.set_yticks(range(len(names)))

ax.set_yticklabels(names, fontsize=11)ax.set_xlabel('年', fontsize=12, fontweight='bold')

ax.set_xlabel('発表数（4年間合計）', fontsize=12, fontweight='bold')ax.set_ylabel('発表数', fontsize=12, fontweight='bold')

ax.set_title('トップ20技術（2022-2025、50ワード基準）\nタイトルまたはabstract冒頭50ワードで主要トピック扱い', ax.set_title('クラウドネイティブフォーマットの年次推移（50ワード基準）', 

             fontsize=14, fontweight='bold', pad=20)             fontsize=14, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3, axis='x')ax.legend(fontsize=11, loc='best')

ax.grid(True, alpha=0.3)

plt.tight_layout()ax.set_xticks(years)

plt.savefig('graphs/04_top_technologies.png', dpi=300, bbox_inches='tight')

print("✓ graphs/04_top_technologies.png を生成")plt.tight_layout()

plt.close()plt.savefig('graphs/05_cloud_formats_trend_50words.png', dpi=300, bbox_inches='tight')

print("✓ graphs/05_cloud_formats_trend_50words.png を生成")

# ===== 2. プログラミング言語の推移 =====plt.close()

# レポート内位置: 3.1節

# ファイル名: 05_languages_trend.png# ===== 3. Webマッピングライブラリの推移 =====

fig, ax = plt.subplots(figsize=(12, 6))

fig, ax = plt.subplots(figsize=(12, 6))

web_libs = ['MapLibre', 'OpenLayers', 'Leaflet', 'Cesium', 'deck.gl']

languages = ['Python', 'JavaScript', 'Java', 'Rust', 'R']for i, lib in enumerate(web_libs):

for i, lang in enumerate(languages):    if lib in results['web_mapping']:

    if lang in results['languages']:        counts = [results['web_mapping'][lib]['yearly'].get(str(year), 0) for year in years]

        counts = [results['languages'][lang]['yearly'].get(str(year), 0) for year in years]        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8,                 label=lib, color=colors[i])

                label=lang, color=colors[i])

ax.set_xlabel('年', fontsize=12, fontweight='bold')

ax.set_xlabel('年', fontsize=12, fontweight='bold')ax.set_ylabel('発表数', fontsize=12, fontweight='bold')

ax.set_ylabel('発表数', fontsize=12, fontweight='bold')ax.set_title('Webマッピングライブラリの年次推移（50ワード基準）', 

ax.set_title('プログラミング言語の年次推移（50ワード基準）\nタイトルまたはabstract冒頭50ワードで主要トピック扱い',              fontsize=14, fontweight='bold', pad=20)

             fontsize=14, fontweight='bold', pad=20)ax.legend(fontsize=11, loc='best')

ax.legend(fontsize=11, loc='best')ax.grid(True, alpha=0.3)

ax.grid(True, alpha=0.3)ax.set_xticks(years)

ax.set_xticks(years)

plt.tight_layout()

plt.tight_layout()plt.savefig('graphs/06_web_mapping_libraries_50words.png', dpi=300, bbox_inches='tight')

plt.savefig('graphs/05_languages_trend.png', dpi=300, bbox_inches='tight')print("✓ graphs/06_web_mapping_libraries_50words.png を生成")

print("✓ graphs/05_languages_trend.png を生成")plt.close()

plt.close()

# ===== 4. 技術カテゴリ比較（4パネル） =====

# ===== 3. Webマッピングライブラリの推移 =====fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# レポート内位置: 3.2節fig.suptitle('技術カテゴリ別トレンド比較（50ワード基準）', fontsize=16, fontweight='bold', y=0.995)

# ファイル名: 06_web_mapping_libraries.png

# 4-1: デスクトップGIS

fig, ax = plt.subplots(figsize=(12, 6))ax = axes[0, 0]

desktop = ['QGIS', 'GRASS GIS']

web_libs = ['MapLibre', 'OpenLayers', 'Leaflet', 'Cesium', 'deck.gl']for i, tech in enumerate(desktop):

for i, lib in enumerate(web_libs):    if tech in results['desktop_gis']:

    if lib in results['web_mapping']:        counts = [results['desktop_gis'][tech]['yearly'].get(str(year), 0) for year in years]

        counts = [results['web_mapping'][lib]['yearly'].get(str(year), 0) for year in years]        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8,                 label=tech, color=colors[i])

                label=lib, color=colors[i])ax.set_title('デスクトップGIS', fontsize=13, fontweight='bold')

ax.set_ylabel('発表数', fontsize=11)

ax.set_xlabel('年', fontsize=12, fontweight='bold')ax.legend(fontsize=10)

ax.set_ylabel('発表数', fontsize=12, fontweight='bold')ax.grid(True, alpha=0.3)

ax.set_title('Webマッピングライブラリの年次推移（50ワード基準）', ax.set_xticks(years)

             fontsize=14, fontweight='bold', pad=20)

ax.legend(fontsize=11, loc='best')# 4-2: サーバー/データベース

ax.grid(True, alpha=0.3)ax = axes[0, 1]

ax.set_xticks(years)servers = [

    ('GeoServer', 'servers'),

plt.tight_layout()    ('PostgreSQL', 'databases'),

plt.savefig('graphs/06_web_mapping_libraries.png', dpi=300, bbox_inches='tight')    ('GDAL', 'data_processing')

print("✓ graphs/06_web_mapping_libraries.png を生成")]

plt.close()for i, (tech, category) in enumerate(servers):

    if tech in results[category]:

# ===== 4. クラウドネイティブフォーマットの推移 =====        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]

# レポート内位置: 3.3節        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

# ファイル名: 07_cloud_formats_trend.png                label=tech, color=colors[i])

ax.set_title('サーバー・データ処理', fontsize=13, fontweight='bold')

fig, ax = plt.subplots(figsize=(12, 6))ax.set_ylabel('発表数', fontsize=11)

ax.legend(fontsize=10)

formats = ['COG', 'PMTiles', 'Zarr', 'GeoParquet']ax.grid(True, alpha=0.3)

for i, fmt in enumerate(formats):ax.set_xticks(years)

    if fmt in results['data_formats']:

        counts = [results['data_formats'][fmt]['yearly'].get(str(year), 0) for year in years]# 4-3: API/標準

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, ax = axes[1, 0]

                label=fmt, color=colors[i])apis = ['STAC', 'OGC API', 'WMS']

for i, tech in enumerate(apis):

ax.set_xlabel('年', fontsize=12, fontweight='bold')    if tech in results['api_standards']:

ax.set_ylabel('発表数', fontsize=12, fontweight='bold')        counts = [results['api_standards'][tech]['yearly'].get(str(year), 0) for year in years]

ax.set_title('クラウドネイティブフォーマットの年次推移（50ワード基準）',         ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

             fontsize=14, fontweight='bold', pad=20)                label=tech, color=colors[i])

ax.legend(fontsize=11, loc='best')ax.set_title('API/標準', fontsize=13, fontweight='bold')

ax.grid(True, alpha=0.3)ax.set_xlabel('年', fontsize=11)

ax.set_xticks(years)ax.set_ylabel('発表数', fontsize=11)

ax.legend(fontsize=10)

plt.tight_layout()ax.grid(True, alpha=0.3)

plt.savefig('graphs/07_cloud_formats_trend.png', dpi=300, bbox_inches='tight')ax.set_xticks(years)

print("✓ graphs/07_cloud_formats_trend.png を生成")

plt.close()# 4-4: クラウド/AI

ax = axes[1, 1]

# ===== 5. 技術カテゴリ比較（4パネル） =====cloud_ai = [

# レポート内位置: 3.3節    ('AWS', 'cloud_infra'),

# ファイル名: 08_tech_categories_comparison.png    ('Machine Learning', 'ai_ml'),

    ('Kubernetes', 'cloud_infra')

fig, axes = plt.subplots(2, 2, figsize=(16, 12))]

fig.suptitle('技術カテゴリ別トレンド比較（50ワード基準）', fontsize=16, fontweight='bold', y=0.995)for i, (tech, category) in enumerate(cloud_ai):

    if tech in results[category]:

# 5-1: デスクトップGIS        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]

ax = axes[0, 0]        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

desktop = ['QGIS', 'GRASS GIS']                label=tech, color=colors[i])

for i, tech in enumerate(desktop):ax.set_title('クラウド・AI/ML', fontsize=13, fontweight='bold')

    if tech in results['desktop_gis']:ax.set_xlabel('年', fontsize=11)

        counts = [results['desktop_gis'][tech]['yearly'].get(str(year), 0) for year in years]ax.set_ylabel('発表数', fontsize=11)

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, ax.legend(fontsize=10)

                label=tech, color=colors[i])ax.grid(True, alpha=0.3)

ax.set_title('デスクトップGIS', fontsize=13, fontweight='bold')ax.set_xticks(years)

ax.set_ylabel('発表数', fontsize=11)

ax.legend(fontsize=10)plt.tight_layout()

ax.grid(True, alpha=0.3)plt.savefig('graphs/07_tech_categories_comparison_50words.png', dpi=300, bbox_inches='tight')

ax.set_xticks(years)print("✓ graphs/07_tech_categories_comparison_50words.png を生成")

plt.close()

# 5-2: サーバー/データベース

ax = axes[0, 1]# ===== 5. トップ20技術（横棒グラフ） =====

servers = [# 全技術を合計でソート

    ('GeoServer', 'servers'),all_techs = []

    ('PostgreSQL', 'databases'),for category, tech_dict in results.items():

    ('GDAL', 'data_processing')    for tech_name, tech_data in tech_dict.items():

]        all_techs.append({

for i, (tech, category) in enumerate(servers):            'name': tech_name,

    if tech in results[category]:            'total': tech_data['total']

        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]        })

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

                label=tech, color=colors[i])all_techs.sort(key=lambda x: x['total'], reverse=True)

ax.set_title('サーバー・データ処理', fontsize=13, fontweight='bold')top20 = all_techs[:20]

ax.set_ylabel('発表数', fontsize=11)

ax.legend(fontsize=10)fig, ax = plt.subplots(figsize=(12, 10))

ax.grid(True, alpha=0.3)

ax.set_xticks(years)names = [t['name'] for t in top20][::-1]

totals = [t['total'] for t in top20][::-1]

# 5-3: API/標準

ax = axes[1, 0]bars = ax.barh(range(len(names)), totals, color=colors[0], alpha=0.8)

apis = ['STAC', 'OGC API', 'WMS']

for i, tech in enumerate(apis):# 各バーに数値を表示

    if tech in results['api_standards']:for i, (bar, total) in enumerate(zip(bars, totals)):

        counts = [results['api_standards'][tech]['yearly'].get(str(year), 0) for year in years]    ax.text(total + 2, i, str(total), va='center', fontsize=10, fontweight='bold')

        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 

                label=tech, color=colors[i])ax.set_yticks(range(len(names)))

ax.set_title('API/標準', fontsize=13, fontweight='bold')ax.set_yticklabels(names, fontsize=11)

ax.set_xlabel('年', fontsize=11)ax.set_xlabel('発表数（4年間合計）', fontsize=12, fontweight='bold')

ax.set_ylabel('発表数', fontsize=11)ax.set_title('トップ20技術（2022-2025、50ワード基準）\nタイトルまたはabstract冒頭50ワードで主要トピック扱い', 

ax.legend(fontsize=10)             fontsize=14, fontweight='bold', pad=20)

ax.grid(True, alpha=0.3)ax.grid(True, alpha=0.3, axis='x')

ax.set_xticks(years)

plt.tight_layout()

# 5-4: クラウド/AIplt.savefig('graphs/08_top_technologies_50words.png', dpi=300, bbox_inches='tight')

ax = axes[1, 1]print("✓ graphs/08_top_technologies_50words.png を生成")

cloud_ai = [plt.close()

    ('AWS', 'cloud_infra'),

    ('Machine Learning', 'ai_ml'),print("\n" + "=" * 80)

    ('Kubernetes', 'cloud_infra')print("すべてのグラフを生成しました（50ワード基準）")

]print("=" * 80)

for i, (tech, category) in enumerate(cloud_ai):
    if tech in results[category]:
        counts = [results[category][tech]['yearly'].get(str(year), 0) for year in years]
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 
                label=tech, color=colors[i])
ax.set_title('クラウド・AI/ML', fontsize=13, fontweight='bold')
ax.set_xlabel('年', fontsize=11)
ax.set_ylabel('発表数', fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xticks(years)

plt.tight_layout()
plt.savefig('graphs/08_tech_categories_comparison.png', dpi=300, bbox_inches='tight')
print("✓ graphs/08_tech_categories_comparison.png を生成")
plt.close()

print("\n" + "=" * 80)
print("すべてのグラフを生成しました（50ワード基準）")
print("  04_top_technologies.png")
print("  05_languages_trend.png")
print("  06_web_mapping_libraries.png")
print("  07_cloud_formats_trend.png")
print("  08_tech_categories_comparison.png")
print("=" * 80)
