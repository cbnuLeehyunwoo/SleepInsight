import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

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

# 1. 상자수염 그래프 한 화면에 표시
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
metrics = ['ram', 'storage', 'battery', 'weight']
titles = ['연도별 RAM', '연도별 저장공간', '연도별 배터리 용량', '연도별 무게']
ylabels = ['RAM (GB)', '저장공간 (GB)', '배터리 (mAh)', '무게 (그램)']
palettes = ['Blues', 'Greens', 'Reds', 'Purples']

for ax, metric, title, ylabel, palette in zip(axes.flatten(), metrics, titles, ylabels, palettes):
    sns.boxplot(x='year', y=metric, data=subset, palette=palette, ax=ax)
    ax.set_title(title, fontproperties=font_prop)
    ax.set_xlabel('연도', fontproperties=font_prop)
    ax.set_ylabel(ylabel, fontproperties=font_prop)

plt.tight_layout()
plt.show()

# 2. OS별 통계 및 가격 그래프 한 화면에 표시
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# OS별 평균 통계 계산
os_grouped_stats = subset.groupby('os_group')[['ram', 'storage', 'battery', 'weight']].mean()
os_grouped_stats.columns = ['평균 RAM (GB)', '평균 저장공간 (GB)', '평균 배터리 (mAh)', '평균 무게 (그램)']

# OS별 통계 그래프
sns.barplot(x=os_grouped_stats.index, y=os_grouped_stats['평균 RAM (GB)'], palette='Blues', ax=axes[0, 0])
axes[0, 0].set_title('OS별 평균 RAM (GB)', fontproperties=font_prop)
axes[0, 0].set_xlabel('운영체제', fontproperties=font_prop)
axes[0, 0].set_ylabel('RAM (GB)', fontproperties=font_prop)

sns.barplot(x=os_grouped_stats.index, y=os_grouped_stats['평균 저장공간 (GB)'], palette='Greens', ax=axes[0, 1])
axes[0, 1].set_title('OS별 평균 저장공간 (GB)', fontproperties=font_prop)
axes[0, 1].set_xlabel('운영체제', fontproperties=font_prop)
axes[0, 1].set_ylabel('저장공간 (GB)', fontproperties=font_prop)

sns.barplot(x=os_grouped_stats.index, y=os_grouped_stats['평균 배터리 (mAh)'], palette='Reds', ax=axes[0, 2])
axes[0, 2].set_title('OS별 평균 배터리 (mAh)', fontproperties=font_prop)
axes[0, 2].set_xlabel('운영체제', fontproperties=font_prop)
axes[0, 2].set_ylabel('배터리 (mAh)', fontproperties=font_prop)

sns.barplot(x=os_grouped_stats.index, y=os_grouped_stats['평균 무게 (그램)'], palette='Purples', ax=axes[1, 0])
axes[1, 0].set_title('OS별 평균 무게 (그램)', fontproperties=font_prop)
axes[1, 0].set_xlabel('운영체제', fontproperties=font_prop)
axes[1, 0].set_ylabel('무게 (그램)', fontproperties=font_prop)

# OS별 평균 가격
os_price_stats = subset.groupby('os_group')['price_usd'].mean().reset_index()
os_price_stats.columns = ['운영체제', '평균 가격 (USD)']

sns.barplot(x='운영체제', y='평균 가격 (USD)', data=os_price_stats, palette='coolwarm', ax=axes[1, 1])
axes[1, 1].set_title('OS별 평균 가격 (USD)', fontproperties=font_prop)
axes[1, 1].set_xlabel('운영체제', fontproperties=font_prop)
axes[1, 1].set_ylabel('평균 가격 (USD)', fontproperties=font_prop)

# 빈 공간 비우기
axes[1, 2].axis('off')

plt.tight_layout()
plt.show()
