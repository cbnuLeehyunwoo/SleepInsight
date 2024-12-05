import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import numpy as np
import re

# 파일 경로
file_path = r"C:\Users\이현우\Downloads\processed_data2.csv"

# 데이터 로드
data = pd.read_csv(file_path)

# 배터리 10000mAh 이상 제외
data = data[data['battery'] < 10000]

# 'Tab'이 포함된 모델명 제외
data = data[~data['phone_model'].str.contains('Tab', case=False)]

# 'year' 열에서 연도만 추출
data['year'] = pd.to_datetime(data['year'], errors='coerce').dt.year

# OS 종류 간소화
data['os'] = data['os'].str.lower()
data['os_group'] = data['os'].apply(lambda x: 'Android' if 'android' in x else ('iOS' if 'ios' in x else 'Others'))

# 정규 표현식 패턴 (GHz 값을 추출)
pattern = r"(\d+\.\d+) GHz" 

def calculate_cpu_speed(cpu_description):
    speeds = re.findall(pattern, cpu_description)  # 정규 표현식으로 GHz 값 추출
    total_speed = 0
    for speed in speeds:
        speed_value = float(speed)  # GHz 값을 float로 변환
        total_speed += speed_value  # 각 GHz 값들을 더함
    
    return total_speed  # 평균이 아닌 총합을 반환


# CPU 칼럼을 숫자 형태로 변환
data['cpu_speed'] = data['cpu'].apply(calculate_cpu_speed)

# 필요한 열만 선택하고 결측치가 있는지 확인
subset = data[['year', 'ram', 'storage', 'battery', 'weight', 'os_group', 'price_usd', 'cpu_speed', 'display_size']]

# 결측치가 있는지 확인
missing_data = subset.isnull().sum()

# 결측치가 있는 경우, 어떤 열에서 결측치가 있는지 출력
if missing_data.any():
    print("결측치가 포함된 열:")
    print(missing_data[missing_data > 0])
    # 결측치가 포함된 행 제거
    subset = subset.dropna()
else:
    print("결측치가 없습니다.")

# 폰트 설정 (한글 폰트 경로 명시)
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # Windows에서 사용하는 한글 폰트 경로
font_prop = font_manager.FontProperties(fname=font_path)

# 그래프 스타일 설정
sns.set(style="whitegrid")

# 1. CPU와 가격의 관계 (연도별 회귀선)
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

# 색상 팔레트 설정
palette = sns.color_palette("viridis", len(subset['year'].unique()))

# 1. CPU와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='cpu_speed', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 CPU 성능의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('CPU 성능 (GHz)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="year", prop=font_prop)

# 2. 배터리와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='battery', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 배터리의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('배터리 (mAh)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="year", prop=font_prop)

plt.tight_layout()
plt.show()

# 3. 무게와 가격의 관계 (연도별 회귀선)
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

# 3. 무게와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='weight', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 무게의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('무게 (그램)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="year", prop=font_prop)

# 4. 디스플레이 크기와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='display_size', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 디스플레이 크기 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('디스플레이 크기 (인치)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="year", prop=font_prop)

plt.tight_layout()
plt.show()

# 5. RAM과 가격의 관계 (연도별 회귀선)
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

# 5. RAM과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='ram', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 RAM의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('RAM (GB)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="year", prop=font_prop)

# 6. 저장공간과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='storage', y='price_usd', data=year_data, scatter_kws={'s': 30, 'edgecolor': 'k', 'color': palette[idx]},
                line_kws={'color': palette[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 저장공간의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('저장공간 (GB)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="year", prop=font_prop)

plt.tight_layout()
plt.show()
