#!/usr/bin/env python3
"""
FOSS4G 2022-2025のGIS学会向け分析
アカデミックトラックを除外し、開発・実用面のトレンドを分析
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter, defaultdict
import json

def is_academic_track(track_name, event_type):
    """アカデミックトラック判定"""
    if not track_name and not event_type:
        return False
    
    track_lower = track_name.lower() if track_name else ""
    type_lower = event_type.lower() if event_type else ""
    
    academic_keywords = [
        'academic', 'research', 'paper', 'アカデミック', '学術'
    ]
    
    return any(keyword in track_lower or keyword in type_lower for keyword in academic_keywords)

def analyze_non_academic_schedule(xml_file, year):
    """アカデミックトラック以外の発表を分析"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # カンファレンス情報
        conference = root.find('conference')
        conf_title = conference.find('title').text if conference.find('title') is not None else "Unknown"
        conf_start = conference.find('start').text if conference.find('start') is not None else "Unknown"
        conf_end = conference.find('end').text if conference.find('end') is not None else "Unknown"
        
        # 全イベント
        events = root.findall('.//event')
        total_events = len(events)
        
        # 除外するタイプ（発表以外）
        excluded_types = {
            'morning tea', 'afternoon tea', 'lunch', 'break', 'reception',
            'ceremony', 'registration', 'welcome', 'closing', 'coffee',
            'networking', 'social', 'dinner', 'ice breaker', 'icebreaker',
            'breakfast', 'party', 'gala', 'opening'
        }
        
        # 統計データ
        type_counter = Counter()
        track_counter = Counter()
        presentations = []
        academic_count = 0
        
        for event in events:
            event_type_elem = event.find('type')
            track_elem = event.find('track')
            title_elem = event.find('title')
            abstract_elem = event.find('abstract')
            description_elem = event.find('description')
            
            event_type = event_type_elem.text if event_type_elem is not None and event_type_elem.text else "Unknown"
            track = track_elem.text if track_elem is not None and track_elem.text else "Unknown"
            title = title_elem.text if title_elem is not None and title_elem.text else "No title"
            
            # トラック名の正規化
            if track:
                track_lower = track.lower()
                # "Use Cases and Applications" / "Use cases and applications" を統一
                if 'use case' in track_lower and 'application' in track_lower:
                    track = "Use cases & applications"
                # "State of Software" / "State of software" を統一
                elif 'state of software' in track_lower:
                    track = "State of software"
                # "Community" 系を統一
                elif 'community' in track_lower and ('collaboration' in track_lower or 'foundation' in track_lower or 'impact' in track_lower):
                    if 'foundation' in track_lower:
                        track = "Community & Foundation"
                    else:
                        track = "Community, Collaboration & Impact"
            
            # break、lunch等を除外
            if any(excluded in event_type.lower() for excluded in excluded_types):
                continue
            
            # アカデミックトラックの判定と除外
            if is_academic_track(track, event_type):
                academic_count += 1
                continue
            
            # 非アカデミックの発表として集計
            abstract = abstract_elem.text if abstract_elem is not None and abstract_elem.text else ""
            description = description_elem.text if description_elem is not None and description_elem.text else ""
            
            presentations.append({
                'title': title,
                'type': event_type,
                'track': track,
                'abstract': abstract,
                'description': description
            })
            type_counter[event_type] += 1
            track_counter[track] += 1
        
        return {
            'year': year,
            'conference_title': conf_title,
            'start_date': conf_start,
            'end_date': conf_end,
            'total_events': total_events,
            'total_presentations': len(presentations),
            'academic_presentations': academic_count,
            'non_academic_presentations': len(presentations),
            'types': dict(type_counter.most_common()),
            'tracks': dict(track_counter.most_common()),
            'presentations': presentations
        }
    
    except Exception as e:
        print(f"エラーが発生しました ({year}): {e}")
        return None

def categorize_presentations(yearly_data):
    """発表をカテゴリに分類"""
    categories = {
        'State of Software': ['state of software'],
        'Use Cases & Applications': ['use cases', 'use case', 'applications'],
        'Data & Infrastructure': ['open data', 'api', 'infrastructure'],
        'Community & Foundation': ['community', 'foundation', 'local chapter', 'osgeo']
    }
    
    categorized = {year: defaultdict(int) for year in yearly_data.keys()}

def print_gis_society_statistics(stats_list):
    """GIS学会向け統計表示"""
    print("=" * 100)
    print("FOSS4G 2022-2025 開発・実用トレンド分析（GIS学会向け）")
    print("=" * 100)
    print()
    
    # 年次サマリー
    print("📊 年次サマリー（アカデミックトラック除外）")
    print("-" * 100)
    print(f"{'年度':<8} {'開催地':<30} {'全発表':>10} {'学術':>8} {'開発/実用':>10} {'割合':>8}")
    print("-" * 100)
    
    for stats in stats_list:
        year = stats['year']
        title = stats['conference_title'].replace('FOSS4G ', '').replace(' general tracks', '')[:30]
        total = stats['total_presentations'] + stats['academic_presentations']
        academic = stats['academic_presentations']
        non_academic = stats['non_academic_presentations']
        ratio = (non_academic / total * 100) if total > 0 else 0
        
        print(f"{year:<8} {title:<30} {total:>10} {academic:>8} {non_academic:>10} {ratio:>7.1f}%")
    
    print()
    
    # 開発・実用分野の主要トラック
    print("🎯 開発・実用分野の主要トラック（各年トップ5）")
    print("-" * 100)
    
    for stats in stats_list:
        year = stats['year']
        print(f"\n【{year}年】総発表数: {stats['non_academic_presentations']}件")
        print(f"  {'トラック名':<50} {'件数':>8} {'割合':>8}")
        print("  " + "-" * 68)
        
        total = stats['non_academic_presentations']
        for track, count in sorted(stats['tracks'].items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  {track:<50} {count:>8} {percentage:>7.1f}%")
    
    print()
    
    # 4年間の総括
    print("📈 4年間の総括（2022-2025）")
    print("-" * 100)
    
    total_all = sum(s['total_presentations'] + s['academic_presentations'] for s in stats_list)
    total_academic = sum(s['academic_presentations'] for s in stats_list)
    total_non_academic = sum(s['non_academic_presentations'] for s in stats_list)
    
    print(f"全発表数:           {total_all:>6}件")
    print(f"学術発表:           {total_academic:>6}件 ({total_academic/total_all*100:>5.1f}%)")
    print(f"開発/実用発表:      {total_non_academic:>6}件 ({total_non_academic/total_all*100:>5.1f}%)")
    
    # 全トラックを集計（非アカデミックのみ）
    all_tracks = {}
    for stats in stats_list:
        for track, count in stats['tracks'].items():
            all_tracks[track] = all_tracks.get(track, 0) + count
    
    top_tracks = sorted(all_tracks.items(), key=lambda x: x[1], reverse=True)[:8]
    
    print()
    print("4年間で最も多かった開発/実用トラック（トップ8）:")
    for i, (track, count) in enumerate(top_tracks, 1):
        print(f"  {i}. {track:<50} {count:>4}件")
    
    print()
    print("=" * 100)

def main():
    """メイン処理"""
    base_path = Path(__file__).parent
    
    # 分析対象ファイル
    years_files = [
        (2022, base_path / 'schedule_2022.xml'),
        (2023, base_path / 'schedule_2023.xml'),
        (2024, base_path / 'schedule_2024.xml'),
        (2025, base_path / 'schedule_2025.xml'),
    ]
    
    # 各年のデータを分析
    all_stats = []
    for year, xml_file in years_files:
        if xml_file.exists():
            print(f"分析中: {year}年 ({xml_file.name})...")
            stats = analyze_non_academic_schedule(xml_file, year)
            if stats:
                all_stats.append(stats)
        else:
            print(f"警告: {xml_file} が見つかりません")
    
    print()
    
    # 結果表示
    if all_stats:
        print_gis_society_statistics(all_stats)
        
        # JSON出力
        output_file = base_path / 'presentations_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_stats, f, ensure_ascii=False, indent=2)
        print(f"\n✅ GIS学会向け分析データを {output_file} に保存しました")
    else:
        print("分析可能なデータがありませんでした。")

if __name__ == "__main__":
    main()
