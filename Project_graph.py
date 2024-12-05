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

# 'Tab'이 포함된 모델명 제외
data = data[~data['phone_model'].str.contains('Tab', case=False, na=False)]

# 'year' 열에서 연도만 추출
data['year'] = pd.to_datetime(data['year'], errors='coerce').dt.year

# OS 종류 간소화
data['os'] = data['os'].str.lower()
data['os_group'] = data['os'].apply(lambda x: 'Android' if 'android' in x else ('iOS' if 'ios' in x else 'Others'))

# 정규 표현식 패턴 (GHz 값을 추출)
pattern = r"(\d+\.\d+) GHz"  # 예: 3.36 GHz, 2.8 GHz와 같은 형태

# CPU 성능을 계산하는 함수
def calculate_cpu_speed(cpu_description):
    # GHz 값을 추출
    speeds = re.findall(pattern, cpu_description)
    
    # 각 코어별로 속도 및 개수를 추출하여 성능 계산
    total_speed = 0
    for speed in speeds:
        speed_value = float(speed)
        # GHz 값과 같은 코어의 개수 추출 (예: 1x3.36 GHz -> 1개 코어가 3.36GHz)
        core_count = cpu_description.count(speed)
        total_speed += core_count * speed_value
    
    # 평균 GHz 계산
    total_cores = sum([int(core.split('x')[0]) for core in re.findall(r"(\d+)x\d+\.\d+ GHz", cpu_description)])
    if total_cores == 0:
        return 0
    average_speed = total_speed / total_cores
    return average_speed

# CPU 칼럼을 숫자 형태로 변환
data['cpu_speed'] = data['cpu'].apply(calculate_cpu_speed)

# 필요한 열만 선택하고 결측치 제거
subset = data[['year', 'ram', 'storage', 'battery', 'weight', 'os_group', 'price_usd', 'cpu_speed', 'display_size']].dropna()

# 폰트 설정 (한글 폰트 경로 명시)
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # Windows에서 사용하는 한글 폰트 경로
font_prop = font_manager.FontProperties(fname=font_path)

# 그래프 스타일 설정
sns.set(style="whitegrid")

# 첫 번째 세트: CPU 성능과 가격의 관계, RAM과 가격의 관계
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1x2 그리드

# 1. CPU 성능과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='cpu_speed', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 CPU 성능의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('CPU 성능 (GHz)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="연도", prop=font_prop)

# 2. RAM과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='ram', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 RAM의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('RAM (GB)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="연도", prop=font_prop)

# 그래프 간격 조정 후 출력
plt.tight_layout()
plt.show()

# 두 번째 세트: 배터리와 가격의 관계, 저장공간과 가격의 관계
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1x2 그리드

# 3. 배터리와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='battery', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 배터리의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('배터리 (mAh)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="연도", prop=font_prop)

# 4. 저장공간과 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='storage', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 저장공간의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('저장공간 (GB)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="연도", prop=font_prop)

# 그래프 간격 조정 후 출력
plt.tight_layout()
plt.show()

# 세 번째 세트: 디스플레이 크기와 가격의 관계, 무게와 가격의 관계
fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1x2 그리드

# 5. 디스플레이 크기와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='display_size', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[0], label=f'{year}')
axes[0].set_title('가격과 디스플레이 크기 (연도별 회귀선)', fontproperties=font_prop)
axes[0].set_xlabel('디스플레이 크기 (인치)', fontproperties=font_prop)
axes[0].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[0].legend(title="연도", prop=font_prop)

# 6. 무게와 가격의 관계 (연도별 회귀선)
for idx, year in enumerate(subset['year'].unique()):
    year_data = subset[subset['year'] == year]
    sns.regplot(x='weight', y='price_usd', data=year_data, scatter_kws={'s': 50, 'edgecolor': 'k', 'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, 
                line_kws={'color': sns.color_palette("viridis", len(subset['year'].unique()))[idx]}, ax=axes[1], label=f'{year}')
axes[1].set_title('가격과 무게의 관계 (연도별 회귀선)', fontproperties=font_prop)
axes[1].set_xlabel('무게 (그램)', fontproperties=font_prop)
axes[1].set_ylabel('가격 (USD)', fontproperties=font_prop)
axes[1].legend(title="연도", prop=font_prop)

# 그래프 간격 조정 후 출력
plt.tight_layout()
plt.show()
