"""
技術トレンドの厳密カウント - 50ワード基準
タイトル or abstractの冒頭50ワード以内で主要トピックとして扱われた場合のみカウント
"""

import json
import xml.etree.ElementTree as ET
from collections import defaultdict

def is_main_topic(title, abstract, keywords, word_limit=50):
    """
    タイトルまたはabstractの冒頭N単語以内でキーワードが主要トピックとして言及されているかチェック
    """
    title_lower = title.lower()
    abstract_lower = abstract.lower()
    
    # abstractの冒頭N単語を取得
    words = abstract_lower.split()[:word_limit]
    abstract_start = ' '.join(words)
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in title_lower or keyword_lower in abstract_start:
            return True
    return False

def is_academic_track(track_name):
    """アカデミックトラックの判定"""
    academic_keywords = [
        'academic', 'research', 'science', 'scientific',
        'theory', 'theoretical', 'study', 'studies'
    ]
    track_lower = track_name.lower()
    return any(keyword in track_lower for keyword in academic_keywords)

def analyze_technology_trends():
    """全技術カテゴリの年次トレンドを分析（50ワード基準）"""
    
    # XMLファイルの定義
    xml_files = {
        2022: 'schedule_2022.xml',
        2023: 'schedule_2023.xml',
        2024: 'schedule_2024.xml',
        2025: 'schedule_2025.xml'
    }
    
    # 技術カテゴリとキーワードの定義
    technologies = {
        'languages': {
            'Python': ['python', 'py3', 'python3'],
            'JavaScript': ['javascript', 'js', 'node.js', 'nodejs'],
            'Rust': ['rust', 'rust-lang'],
            'Java': ['java', 'openjdk'],
            'TypeScript': ['typescript'],
            'Go': ['golang', 'go language'],
            'C++': ['c++', 'cpp'],
            'R': [' r ', 'r language', 'rstudio'],
        },
        'desktop_gis': {
            'QGIS': ['qgis'],
            'GRASS GIS': ['grass gis', 'grass7', 'grass8'],
            'SAGA GIS': ['saga gis'],
        },
        'web_mapping': {
            'MapLibre': ['maplibre', 'maplibre-gl'],
            'OpenLayers': ['openlayers', 'ol3', 'ol4', 'ol5', 'ol6', 'ol7'],
            'Leaflet': ['leaflet', 'leaflet.js'],
            'deck.gl': ['deck.gl', 'deck gl'],
            'Cesium': ['cesium', 'cesiumjs'],
        },
        'data_formats': {
            'COG': ['cog', 'cloud-optimized geotiff', 'cloud optimized geotiff'],
            'PMTiles': ['pmtiles'],
            'Zarr': ['zarr'],
            'GeoParquet': ['geoparquet'],
        },
        'api_standards': {
            'STAC': ['stac', 'spatio-temporal asset catalog', 'spatiotemporal asset catalog'],
            'OGC API': ['ogc api'],
            'WMS': ['wms', 'web map service'],
            'WFS': ['wfs', 'web feature service'],
        },
        'data_processing': {
            'GDAL': ['gdal', 'ogr'],
        },
        'databases': {
            'PostgreSQL': ['postgresql', 'postgres', 'postgis'],
        },
        'servers': {
            'GeoServer': ['geoserver'],
            'GeoNode': ['geonode'],
            'MapServer': ['mapserver', 'mapserv'],
        },
        'cloud_infra': {
            'AWS': ['aws', 'amazon web services'],
            'Docker': ['docker'],
            'Kubernetes': ['kubernetes', 'k8s'],
            'Azure': ['azure', 'microsoft azure'],
        },
        'ai_ml': {
            'Machine Learning': ['machine learning', 'ml model', 'scikit-learn', 'sklearn'],
            'Deep Learning': ['deep learning', 'neural network', 'tensorflow', 'pytorch'],
        }
    }
    
    results = {}
    
    for category, tech_dict in technologies.items():
        results[category] = {}
        
        for tech_name, keywords in tech_dict.items():
            yearly_counts = {}
            total_count = 0
            
            for year, xml_file in xml_files.items():
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    count = 0
                    
                    for event in root.findall('.//event'):
                        # トラック情報を取得
                        track = event.find('.//track')
                        track_name = track.text if track is not None and track.text else ""
                        
                        # アカデミックトラックを除外
                        if is_academic_track(track_name):
                            continue
                        
                        title_elem = event.find('.//title')
                        abstract_elem = event.find('.//abstract')
                        
                        title = title_elem.text if title_elem is not None and title_elem.text else ""
                        abstract = abstract_elem.text if abstract_elem is not None and abstract_elem.text else ""
                        
                        if is_main_topic(title, abstract, keywords, word_limit=50):
                            count += 1
                    
                    yearly_counts[year] = count
                    total_count += count
                    
                except FileNotFoundError:
                    print(f"Warning: {xml_file} not found")
                    yearly_counts[year] = 0
            
            results[category][tech_name] = {
                'total': total_count,
                'yearly': yearly_counts
            }
    
    return results

# 分析実行
print("=" * 80)
print("技術トレンド分析 - 50ワード基準")
print("タイトル or abstractの冒頭50ワード以内で主要トピックとして扱われた場合のみカウント")
print("=" * 80)
print()

results = analyze_technology_trends()

# カテゴリごとに結果を表示
category_names = {
    'languages': 'プログラミング言語',
    'desktop_gis': 'デスクトップGIS',
    'web_mapping': 'Webマッピング',
    'data_formats': 'クラウドネイティブフォーマット',
    'api_standards': 'API/標準',
    'data_processing': 'データ処理',
    'databases': 'データベース',
    'servers': 'サーバー',
    'cloud_infra': 'クラウドインフラ',
    'ai_ml': 'AI/機械学習'
}

for category, category_jp in category_names.items():
    print(f"\n【{category_jp}】")
    print("-" * 80)
    
    # 合計件数でソート
    sorted_techs = sorted(
        results[category].items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )
    
    for tech_name, data in sorted_techs:
        total = data['total']
        yearly = data['yearly']
        
        if total > 0:
            yearly_str = f"{yearly.get(2022, 0):3}/{yearly.get(2023, 0):3}/{yearly.get(2024, 0):3}/{yearly.get(2025, 0):3}"
            print(f"  {tech_name:25} Total: {total:4}  ({yearly_str})")

# JSONに保存
output = {
    'metadata': {
        'criteria': '50ワード基準',
        'description': 'タイトル or abstractの冒頭50ワード以内で主要トピックとして扱われた発表のみカウント',
        'years': [2022, 2023, 2024, 2025],
        'total_presentations': 984,
        'note': 'アカデミックトラックは除外'
    },
    'results': results
}

with open('tech_trends_50words.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("結果を tech_trends_50words.json に保存しました")
print("=" * 80)

# サマリー統計
print("\n【サマリー統計】")
print("-" * 80)

total_mentions = 0
for category in results.values():
    for tech_data in category.values():
        total_mentions += tech_data['total']

print(f"総カウント数: {total_mentions}")
print(f"カテゴリ数: {len(results)}")

# トップ20技術
print("\n【トップ20技術（全カテゴリ）】")
print("-" * 80)

all_techs = []
for category, tech_dict in results.items():
    for tech_name, data in tech_dict.items():
        all_techs.append({
            'name': tech_name,
            'category': category,
            'total': data['total'],
            'yearly': data['yearly']
        })

all_techs.sort(key=lambda x: x['total'], reverse=True)

print(f"{'順位':<4} {'技術名':<20} {'合計':>6} {'2022':>6} {'2023':>6} {'2024':>6} {'2025':>6}")
print("-" * 80)

for i, tech in enumerate(all_techs[:20], 1):
    y = tech['yearly']
    print(f"{i:<4} {tech['name']:<20} {tech['total']:>6} "
          f"{y.get(2022, 0):>6} {y.get(2023, 0):>6} {y.get(2024, 0):>6} {y.get(2025, 0):>6}")
