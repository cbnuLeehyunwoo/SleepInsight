import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import numpy as np

# 한글 폰트 설정 (윈도우 기준)
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # Malgun Gothic 경로
font_prop = font_manager.FontProperties(fname=font_path)

# 파일 경로
file_path = r"C:\Users\이현우\Downloads\processed_data2.csv"

# 데이터 로드
data = pd.read_csv(file_path)

# 'year' 열에서 연도만 추출
data['year'] = pd.to_datetime(data['year'], errors='coerce').dt.year

# OS 종류 간소화
data['os'] = data['os'].str.lower()
data['os_group'] = data['os'].apply(lambda x: 'Android' if 'android' in x else ('iOS' if 'ios' in x else 'Others'))

# 조건에 맞는 데이터를 제외
filtered_data = data[~((data['weight'] >= 300) | 
                       (data['storage'] >= 1000) | 
                       (data['ram'] >= 20) | 
                       (data['battery'] >= 10000))]

# 필요한 열만 선택하고 결측치 제거
subset = filtered_data[['year', 'ram', 'storage', 'battery', 'weight', 'os_group', 'price_usd']].dropna()

# 그래프 스타일 설정
sns.set(style="whitegrid")

# 3. 가격과 다른 항목(램, 배터리, 무게, 저장공간) 사이의 관계 회귀선 포함 산점도 (연도별 회귀선)
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 색상 팔레트 설정
palette = sns.color_palette("viridis", len(subset['year'].unique()))

# 1. RAM과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='ram', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': palette[idx]}, 
                line_kws={'color': palette[idx]}, ax=axes[0, 0], label=f'{year}')
axes[0, 0].set_title('가격과 RAM의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0, 0].set_xlabel('RAM (GB)', fontproperties=font_prop)
axes[0, 0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0, 0].legend(title="연도", prop=font_prop)

# 2. 배터리와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='battery', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': palette[idx]}, 
                line_kws={'color': palette[idx]}, ax=axes[0, 1], label=f'{year}')
axes[0, 1].set_title('가격과 배터리의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0, 1].set_xlabel('배터리 (mAh)', fontproperties=font_prop)
axes[0, 1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0, 1].legend(title="연도", prop=font_prop)

# 3. 무게와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='weight', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': palette[idx]}, 
                line_kws={'color': palette[idx]}, ax=axes[1, 0], label=f'{year}')
axes[1, 0].set_title('가격과 무게의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1, 0].set_xlabel('무게 (그램)', fontproperties=font_prop)
axes[1, 0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1, 0].legend(title="연도", prop=font_prop)

# 4. 저장공간과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='storage', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': palette[idx]}, 
                line_kws={'color': palette[idx]}, ax=axes[1, 1], label=f'{year}')
axes[1, 1].set_title('가격과 저장공간의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1, 1].set_xlabel('저장공간 (GB)', fontproperties=font_prop)
axes[1, 1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1, 1].legend(title="연도", prop=font_prop)

plt.tight_layout()
plt.show()
