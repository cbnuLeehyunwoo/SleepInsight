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

# 조건에 맞는 데이터를 제외
filtered_data = data[~((data['weight'] >= 300) | 
                       (data['storage'] >= 1000) | 
                       (data['ram'] >= 20) | 
                       (data['battery'] >= 10000))]

# 필요한 열만 선택하고 결측치 제거
subset = filtered_data[['year', 'ram', 'storage', 'battery', 'weight']].dropna()

# 그래프 스타일 설정
sns.set(style="whitegrid")

# 상자수염 그래프 그리기
plt.figure(figsize=(12, 8))

# RAM 상자수염 그래프
plt.subplot(2, 2, 1)
sns.boxplot(x='year', y='ram', data=subset, palette='Blues')
plt.title('연도별 RAM', fontproperties=font_prop)
plt.xlabel('연도', fontproperties=font_prop)
plt.ylabel('RAM (GB)', fontproperties=font_prop)

# Storage 상자수염 그래프
plt.subplot(2, 2, 2)
sns.boxplot(x='year', y='storage', data=subset, palette='Greens')
plt.title('연도별 저장공간', fontproperties=font_prop)
plt.xlabel('연도', fontproperties=font_prop)
plt.ylabel('저장공간 (GB)', fontproperties=font_prop)

# Battery 상자수염 그래프
plt.subplot(2, 2, 3)
sns.boxplot(x='year', y='battery', data=subset, palette='Reds')
plt.title('연도별 배터리 용량', fontproperties=font_prop)
plt.xlabel('연도', fontproperties=font_prop)
plt.ylabel('배터리 (mAh)', fontproperties=font_prop)

# Weight 상자수염 그래프
plt.subplot(2, 2, 4)
sns.boxplot(x='year', y='weight', data=subset, palette='Purples')
plt.title('연도별 무게', fontproperties=font_prop)
plt.xlabel('연도', fontproperties=font_prop)
plt.ylabel('무게 (그램)', fontproperties=font_prop)

plt.tight_layout()
plt.show()
