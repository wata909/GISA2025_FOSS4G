#!/usr/bin/env python3
"""
FOSS4G 2022-2025のグラフ可視化
基本統計のグラフを生成
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import warnings

# フォント警告を抑制
warnings.filterwarnings('ignore', message='Glyph .* missing from font')

# 日本語フォント設定（macOS対応）
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

def load_statistics():
    """統計データを読み込む（GIS学会向け正規化済みデータを使用）"""
    # 正規化済みのGIS学会向けデータを使用
    gis_json = Path(__file__).parent / 'presentations_data.json'
    if gis_json.exists():
        with open(gis_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # フォールバック: 元のyearly_statistics.json
    json_file = Path(__file__).parent / 'yearly_statistics.json'
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_presentation_trend(stats_list, output_dir):
    """発表数の年次推移グラフ（開発・実用分野）"""
    years = [s['year'] for s in stats_list]
    # GIS学会データの場合は'non_academic_presentations'を使用
    presentations = [s.get('non_academic_presentations', s.get('total_presentations', 0)) for s in stats_list]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 棒グラフ（すべて同じ色）
    bars = ax.bar(range(len(years)), presentations, color='#3498db', 
                  edgecolor='black', linewidth=1.5)
    
    # 値をバーの上に表示
    for bar, count in zip(bars, presentations):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}件',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('年度', fontsize=14, fontweight='bold')
    ax.set_ylabel('発表数', fontsize=14, fontweight='bold')
    ax.set_title('FOSS4G 発表数の年次推移（開発・実用分野、2022-2025）', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)  # 整数の年度をそのまま表示
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max(presentations) * 1.15)
    
    plt.tight_layout()
    plt.savefig(output_dir / '03_presentation_trend.png', dpi=300, bbox_inches='tight')
    print(f"✓ 発表数推移グラフを保存: 03_presentation_trend.png")
    plt.close()

def plot_type_distribution(stats_list, output_dir):
    """発表タイプの分布（各年）"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, stats in enumerate(stats_list):
        ax = axes[idx]
        year = stats['year']
        
        # トップ8のタイプを取得
        types_sorted = sorted(stats['types'].items(), key=lambda x: x[1], reverse=True)[:8]
        types_names = [t[0] for t in types_sorted]
        types_counts = [t[1] for t in types_sorted]
        
        # 円グラフ
        colors = sns.color_palette("husl", len(types_names))
        wedges, texts, autotexts = ax.pie(types_counts, labels=types_names, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        
        # テキストのフォーマット
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title(f'{year}年 発表タイプ分布\n(総数: {stats["total_presentations"]}件)', 
                     fontsize=12, fontweight='bold', pad=10)
    
    plt.suptitle('FOSS4G 発表タイプの分布 (2022-2025)', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(output_dir / 'type_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ タイプ分布グラフを保存: type_distribution.png")
    plt.close()

def plot_top_tracks_comparison(stats_list, output_dir):
    """主要トラックの年次比較（開発・実用分野）"""
    # 各年のトップ5トラックを集計
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x_pos = []
    labels = []
    colors_list = []
    
    color_palette = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    current_x = 0
    for idx, stats in enumerate(stats_list):
        year = stats['year']
        tracks_data = stats.get('tracks', {})
        tracks_sorted = sorted(tracks_data.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for track, count in tracks_sorted:
            x_pos.append(current_x)
            # トラック名を短縮
            short_track = track[:30] + '...' if len(track) > 30 else track
            labels.append(f"{short_track}\n({count})")
            colors_list.append(color_palette[idx])
            current_x += 1
        
        current_x += 0.5  # 年の間にスペース
    
    bars = ax.barh(range(len(x_pos)), [1]*len(x_pos), color=colors_list, 
                   edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(range(len(x_pos)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlim(0, 1.2)
    ax.set_title('各年のトップ5トラック比較（開発・実用分野）', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('')
    ax.set_xticks([])
    
    # 凡例
    legend_elements = [plt.Rectangle((0,0),1,1, fc=color_palette[i], edgecolor='black', label=f'{stats_list[i]["year"]}年')
                      for i in range(len(stats_list))]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'top_tracks_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ トラック比較グラフを保存: top_tracks_comparison.png")
    plt.close()

def plot_track_trends_over_years(stats_list, output_dir):
    """主要トラックの年次推移（開発・実用分野）"""
    # 全年のトラックデータを集計
    all_tracks = {}
    for stats in stats_list:
        # GIS学会データの場合は'tracks'キーを使用
        tracks_data = stats.get('tracks', {})
        for track, count in tracks_data.items():
            if track not in all_tracks:
                all_tracks[track] = {}
            all_tracks[track][stats['year']] = count
    
    # 総数が多い上位7トラックを選択
    track_totals = {track: sum(years.values()) for track, years in all_tracks.items()}
    top_tracks = sorted(track_totals.items(), key=lambda x: x[1], reverse=True)[:7]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    years = [s['year'] for s in stats_list]
    
    colors = sns.color_palette("husl", len(top_tracks))
    
    for idx, (track_name, total) in enumerate(top_tracks):
        track_data = all_tracks[track_name]
        counts = [track_data.get(year, 0) for year in years]
        
        # トラック名を短縮
        short_name = track_name[:40] + '...' if len(track_name) > 40 else track_name
        ax.plot(years, counts, marker='o', linewidth=2.5, markersize=8, 
                label=short_name, color=colors[idx])
    
    ax.set_xlabel('年度', fontsize=14, fontweight='bold')
    ax.set_ylabel('発表数', fontsize=14, fontweight='bold')
    ax.set_title('主要トラックの年次推移（開発・実用分野トップ7）', fontsize=16, fontweight='bold', pad=20)
    
    # 2024年の特殊事情を注釈として追加
    ax.annotate('※2024年はブラジル・Belém開催\n（アマゾン地域、アクセス困難）\nにより発表数が減少',
                xy=(2024, 5), xytext=(2024, 90),
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                fontsize=9, ha='center',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', color='red', lw=1.5))
    
    ax.legend(fontsize=9, loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(years)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'track_trends.png', dpi=300, bbox_inches='tight')
    print(f"✓ トラック推移グラフを保存: track_trends.png")
    plt.close()

def main():
    """メイン処理"""
    print("=" * 80)
    print("FOSS4G 2022-2025 グラフ可視化")
    print("=" * 80)
    print()
    
    # 統計データ読み込み
    stats_list = load_statistics()
    
    # 出力ディレクトリ
    output_dir = Path(__file__).parent / 'graphs'
    output_dir.mkdir(exist_ok=True)
    
    print("グラフ生成中...")
    print()
    
    # 必要なグラフのみ生成（track_trends, top_tracks_comparison, type_distributionは除外）
    plot_presentation_trend(stats_list, output_dir)
    
    print()
    print("=" * 80)
    print(f"✅ すべてのグラフを {output_dir} に保存しました")
    print("=" * 80)

if __name__ == "__main__":
    main()
