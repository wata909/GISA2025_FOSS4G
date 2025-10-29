#!/usr/bin/env python3
"""
FOSS4G 2022-2025のGIS学会向けグラフ可視化
開発・実用トレンドに焦点を当てたグラフ生成
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
import warnings

# フォント警告を抑制
warnings.filterwarnings('ignore', message='Glyph .* missing from font')

# 日本語フォント設定（macOS対応）
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

def load_gis_society_data():
    """GIS学会向けデータを読み込む"""
    json_file = Path(__file__).parent / 'gis_society_analysis.json'
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_academic_vs_practical(stats_list, output_dir):
    """学術 vs 開発・実用の比較"""
    years = [s['year'] for s in stats_list]
    academic = [s['academic_presentations'] for s in stats_list]
    practical = [s['non_academic_presentations'] for s in stats_list]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 積み上げ棒グラフ
    x = np.arange(len(years))
    width = 0.6
    
    p1 = ax1.bar(x, practical, width, label='開発・実用', color='#3498db', edgecolor='black', linewidth=1.5)
    p2 = ax1.bar(x, academic, width, bottom=practical, label='学術', color='#e74c3c', edgecolor='black', linewidth=1.5)
    
    ax1.set_ylabel('発表数', fontsize=14, fontweight='bold')
    ax1.set_xlabel('年度', fontsize=14, fontweight='bold')
    ax1.set_title('FOSS4G 発表構成の推移', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.legend(fontsize=12, loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 値を表示
    for i, (p, a) in enumerate(zip(practical, academic)):
        total = p + a
        ax1.text(i, total + 5, f'{total}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        if p > 0:
            ax1.text(i, p/2, f'{p}', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
        if a > 0:
            ax1.text(i, p + a/2, f'{a}', ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    
    # 割合の円グラフ（4年間合計）
    total_academic = sum(academic)
    total_practical = sum(practical)
    
    labels = ['開発・実用', '学術']
    sizes = [total_practical, total_academic]
    colors = ['#3498db', '#e74c3c']
    explode = (0.05, 0)
    
    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 14, 'fontweight': 'bold'})
    ax2.set_title('4年間の発表構成比\n(総数: {})'.format(total_academic + total_practical), 
                  fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / '02_academic_vs_practical.png', dpi=300, bbox_inches='tight')
    print(f"✓ 学術vs開発・実用グラフを保存: 02_academic_vs_practical.png")
    plt.close()

def plot_main_tracks_evolution(stats_list, output_dir):
    """主要トラックの進化（積み上げ棒グラフ）"""
    # 4年間の主要トラックを特定
    all_tracks = {}
    for stats in stats_list:
        for track, count in stats['tracks'].items():
            all_tracks[track] = all_tracks.get(track, 0) + count
    
    # トップ10トラックを選択（より多くのトラックを表示）
    top_tracks = sorted(all_tracks.items(), key=lambda x: x[1], reverse=True)[:10]
    top_track_names = [t[0] for t in top_tracks]
    
    years = [s['year'] for s in stats_list]
    
    fig, ax = plt.subplots(figsize=(14, 9))
    
    # 各トラックのデータを準備
    data_matrix = []
    for track_name in top_track_names:
        counts = [stats['tracks'].get(track_name, 0) for stats in stats_list]
        data_matrix.append(counts)
    
    # カラーパレット
    colors = sns.color_palette("Set3", len(top_track_names))
    
    # 積み上げ棒グラフ
    x = np.arange(len(years))
    width = 0.6
    bottom = np.zeros(len(years))
    
    bars = []
    for idx, (track_name, counts) in enumerate(zip(top_track_names, data_matrix)):
        # トラック名を短縮
        short_name = track_name[:35] + '...' if len(track_name) > 35 else track_name
        bar = ax.bar(x, counts, width, label=short_name, bottom=bottom, 
                    color=colors[idx], edgecolor='white', linewidth=0.5)
        bars.append(bar)
        bottom += np.array(counts)
    
    # 総数を各バーの上に表示
    for i, (year_idx, year) in enumerate(zip(x, years)):
        total = bottom[i]
        ax.text(year_idx, total + 5, f'{int(total)}件', 
               ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('年度', fontsize=14, fontweight='bold')
    ax.set_ylabel('発表数', fontsize=14, fontweight='bold')
    ax.set_title('主要トラックの推移（開発・実用分野トップ10、積み上げ）', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.legend(fontsize=9, loc='upper left', bbox_to_anchor=(1.01, 1), framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / '01_main_tracks_evolution.png', dpi=300, bbox_inches='tight')
    print(f"✓ 主要トラック推移グラフを保存: 01_main_tracks_evolution.png")
    plt.close()

def plot_track_categories_by_year(stats_list, output_dir):
    """各年のトラックカテゴリ分布"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    # トラックをカテゴリ分類
    def categorize_track(track_name):
        track_lower = track_name.lower()
        if 'state of' in track_lower or 'software' in track_lower:
            return 'ソフトウェア状況'
        elif 'use case' in track_lower or 'application' in track_lower:
            return '実用事例・応用'
        elif 'community' in track_lower or 'foundation' in track_lower or 'collaboration' in track_lower:
            return 'コミュニティ'
        elif 'data' in track_lower or 'cloud' in track_lower or 'infrastructure' in track_lower or 'api' in track_lower:
            return 'データ・基盤'
        elif 'tool' in track_lower or 'library' in track_lower or 'visualisation' in track_lower or 'visualization' in track_lower:
            return 'ツール・ライブラリ'
        elif 'transition' in track_lower or 'education' in track_lower or 'training' in track_lower:
            return '普及・教育'
        elif 'lightning' in track_lower:
            return 'ライトニングトーク'
        elif 'workshop' in track_lower:
            return 'ワークショップ'
        else:
            return 'その他'
    
    # すべての年のカテゴリを収集して、統一的な色を割り当て
    all_categories = set()
    for stats in stats_list:
        for track in stats['tracks'].keys():
            category = categorize_track(track)
            all_categories.add(category)
    
    # カテゴリごとに固定色を割り当て
    category_list = sorted(all_categories)
    color_palette = sns.color_palette("Set3", len(category_list))
    category_colors = {cat: color_palette[i] for i, cat in enumerate(category_list)}
    
    for idx, stats in enumerate(stats_list):
        ax = axes[idx]
        year = stats['year']
        
        # カテゴリ集計
        category_counts = {}
        for track, count in stats['tracks'].items():
            category = categorize_track(track)
            category_counts[category] = category_counts.get(category, 0) + count
        
        # トップ8カテゴリ
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        categories = [c[0] for c in sorted_categories]
        counts = [c[1] for c in sorted_categories]
        
        # 各カテゴリの色を統一的に設定
        colors = [category_colors[cat] for cat in categories]
        
        wedges, texts, autotexts = ax.pie(counts, labels=categories, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        ax.set_title(f'{year}年 トラックカテゴリ分布\n(総数: {stats["non_academic_presentations"]}件)', 
                     fontsize=12, fontweight='bold', pad=10)
    
    plt.suptitle('FOSS4G トラックカテゴリの分布（開発・実用分野）', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(output_dir / '02_track_categories_distribution.png', dpi=300, bbox_inches='tight')
    print(f"✓ トラックカテゴリ分布グラフを保存: 02_track_categories_distribution.png")
    plt.close()

def plot_foss4g_growth_history(stats_list, output_dir):
    """FOSS4G成長の歴史（2004-2025）"""
    # 歴史的データ（推定値を含む）
    historical_data = {
        2004: 200,   # 初回・チュラロンコン大学
        2006: 350,   # OSGeo発足後初
        2008: 450,
        2010: 550,
        2012: 600,
        2014: 700,
        2016: 750,
        2018: 850,
        2020: 200,   # COVID-19影響（オンライン）
        2021: 400,   # オンライン/ハイブリッド
        2022: 328,   # 実データ
        2023: 296,   # 実データ
        2024: 131,   # 実データ
        2025: 283,   # 実データ
        2026: 800,   # 広島予測
    }
    
    years = list(historical_data.keys())
    participants = list(historical_data.values())
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 実データと推定データを分けて描画
    real_data_start = 2022
    estimated_idx = [i for i, y in enumerate(years) if y < real_data_start]
    real_idx = [i for i, y in enumerate(years) if y >= real_data_start]
    future_idx = [i for i, y in enumerate(years) if y >= 2026]
    
    # 推定データ
    ax.plot([years[i] for i in estimated_idx], [participants[i] for i in estimated_idx],
            'o--', color='#95a5a6', linewidth=2, markersize=6, label='推定値', alpha=0.7)
    
    # 実データ
    ax.plot([years[i] for i in real_idx if years[i] < 2026], 
            [participants[i] for i in real_idx if years[i] < 2026],
            'o-', color='#3498db', linewidth=3, markersize=10, label='実データ', markeredgecolor='black', markeredgewidth=1.5)
    
    # 2026予測
    ax.plot([2025, 2026], [participants[-2], participants[-1]],
            's-', color='#e74c3c', linewidth=3, markersize=12, label='2026広島（予測）', markeredgecolor='black', markeredgewidth=1.5)
    
    # 重要なイベントをアノテーション
    ax.annotate('初回FOSS4G\n(バンコク)', xy=(2004, 200), xytext=(2004, 350),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                fontsize=10, ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.annotate('OSGeo発足', xy=(2006, 350), xytext=(2006, 500),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                fontsize=10, ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
    
    ax.annotate('COVID-19', xy=(2020, 200), xytext=(2018, 100),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                fontsize=10, ha='center', bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.7))
    
    ax.annotate('FOSS4G 2026\n広島開催', xy=(2026, 800), xytext=(2026, 950),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.7', facecolor='orange', alpha=0.8, edgecolor='red', linewidth=2))
    
    ax.set_xlabel('年度', fontsize=14, fontweight='bold')
    ax.set_ylabel('発表数（推定含む）', fontsize=14, fontweight='bold')
    ax.set_title('FOSS4Gの21年の歩み（2004-2026）', fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'foss4g_history_2004_2026.png', dpi=300, bbox_inches='tight')
    print(f"✓ FOSS4G歴史グラフを保存: foss4g_history_2004_2026.png")
    plt.close()

def main():
    """メイン処理"""
    print("=" * 80)
    print("FOSS4G GIS学会向けグラフ可視化")
    print("=" * 80)
    print()
    
    # データ読み込み
    stats_list = load_gis_society_data()
    
    # 出力ディレクトリ
    output_dir = Path(__file__).parent / 'graphs'
    output_dir.mkdir(exist_ok=True)
    
    print("GIS学会向けグラフ生成中...")
    print()
    
    # グラフ生成（academic_vs_practicalは削除）
    plot_main_tracks_evolution(stats_list, output_dir)
    plot_track_categories_by_year(stats_list, output_dir)
    
    print()
    print("=" * 80)
    print(f"✅ すべてのGIS学会向けグラフを {output_dir} に保存しました")
    print("=" * 80)

if __name__ == "__main__":
    main()
