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
    total_speed = 0
    
    # 'x'와 '&'를 모두 처리할 수 있도록 정규 표현식 수정
    # "x"가 포함된 형식 (예: "2x2.0 GHz" 또는 "1x3.00 GHz")
    cores_and_speeds = re.findall(r"(\d+)x(\d+\.\d+) GHz", cpu_description)
    for core_count, speed in cores_and_speeds:
        core_count = int(core_count)  # 코어 수 (정수로 변환)
        speed_value = float(speed)    # GHz 값 (실수로 변환)
        total_speed += core_count * speed_value  # 코어 수 * 속도 값 추가
    
    # '&'를 기준으로 각 속도 항목 처리 (예: "2x2.0 GHz" & "6x1.8 GHz")
    part_speeds = re.split(r'&', cpu_description)  # &로 분리하여 각 항목 처리
    for part in part_speeds:
        # 'x'가 포함된 경우를 처리 (예: "2x2.0 GHz")
        cores_and_speeds = re.findall(r"(\d+)x(\d+\.\d+) GHz", part)
        for core_count, speed in cores_and_speeds:
            core_count = int(core_count)
            speed_value = float(speed)
            total_speed += core_count * speed_value
        
        # 'x'가 없는 경우 (예: "2.0 GHz")
        speeds = re.findall(r"(\d+\.?\d*) GHz", part)
        for speed in speeds:
            total_speed += float(speed)
    
    # 만약 계산된 속도가 0이라면, NaN으로 반환
    if total_speed == 0:
        return np.nan
    
    return total_speed
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

# OS별 데이터 집계

os_summary = subset.groupby('os_group').agg(
    avg_ram=('ram', np.mean),          # 평균 RAM
    avg_storage=('storage', np.mean),   # 평균 저장공간
    count=('os_group', 'size'),         # 각 OS의 개수
    avg_price=('price_usd', np.mean),   # 평균 가격
    price_std=('price_usd', np.std),    # 가격의 표준편차
    avg_cpu=('cpu_speed', np.mean)      # 평균 CPU 속도
).reset_index()

# 시각화 - OS별 평균 RAM, 저장공간, 가격의 표준편차, OS 개수, CPU 속도
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# OS별 평균 RAM
sns.barplot(x='os_group', y='avg_ram', data=os_summary, ax=axes[0, 0], palette='Blues')
axes[0, 0].set_title('OS별 평균 RAM (GB)', fontproperties=font_prop)
axes[0, 0].set_ylabel('RAM (GB)', fontproperties=font_prop)

# OS별 평균 저장공간
sns.barplot(x='os_group', y='avg_storage', data=os_summary, ax=axes[0, 1], palette='Greens')
axes[0, 1].set_title('OS별 평균 저장공간 (GB)', fontproperties=font_prop)
axes[0, 1].set_ylabel('저장공간 (GB)', fontproperties=font_prop)

# OS별 OS 개수
sns.barplot(x='os_group', y='count', data=os_summary, ax=axes[0, 2], palette='Reds')
axes[0, 2].set_title('OS별 개수', fontproperties=font_prop)
axes[0, 2].set_ylabel('개수', fontproperties=font_prop)

# OS별 가격의 표준편차
sns.barplot(x='os_group', y='price_std', data=os_summary, ax=axes[1, 0], palette='Purples')
axes[1, 0].set_title('OS별 가격 표준편차 (USD)', fontproperties=font_prop)
axes[1, 0].set_ylabel('가격 표준편차 (USD)', fontproperties=font_prop)

# OS별 평균 가격
sns.barplot(x='os_group', y='avg_price', data=os_summary, ax=axes[1, 1], palette='Oranges')
axes[1, 1].set_title('OS별 평균 가격 (USD)', fontproperties=font_prop)
axes[1, 1].set_ylabel('평균 가격 (USD)', fontproperties=font_prop)

# OS별 평균 CPU 속도
sns.barplot(x='os_group', y='avg_cpu', data=os_summary, ax=axes[1, 2], palette='coolwarm')
axes[1, 2].set_title('OS별 평균 CPU 속도 (GHz)', fontproperties=font_prop)
axes[1, 2].set_ylabel('CPU 속도 (GHz)', fontproperties=font_prop)

plt.tight_layout()
plt.show()

