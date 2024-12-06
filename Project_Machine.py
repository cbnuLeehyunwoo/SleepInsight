import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import re

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 환경: 맑은 고딕
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터 로드
file_path = r"C:\Users\이현우\Downloads\processed_data2.csv"
data = pd.read_csv(file_path)

# 데이터 전처리
data = data[data['battery'] < 10000]  # 배터리 10000mAh 이상 제외
data = data[~data['phone_model'].str.contains('Tab', case=False)]  # 'Tab'이 포함된 모델명 제외
data['year'] = pd.to_datetime(data['year'], errors='coerce').dt.year  # 연도 추출
data['os'] = data['os'].str.lower()
data['os_group'] = data['os'].apply(lambda x: 'Android' if 'android' in x else ('iOS' if 'ios' in x else 'Others'))

# CPU 속도 계산
def calculate_cpu_speed(cpu_description):
    total_speed = 0
    cores_and_speeds = re.findall(r"(\d+)x(\d+\.\d+) GHz", cpu_description)
    for core_count, speed in cores_and_speeds:
        total_speed += int(core_count) * float(speed)
    part_speeds = re.split(r'&', cpu_description)
    for part in part_speeds:
        speeds = re.findall(r"(\d+\.?\d*) GHz", part)
        for speed in speeds:
            total_speed += float(speed)
    return total_speed if total_speed > 0 else np.nan

data['cpu_speed'] = data['cpu'].apply(calculate_cpu_speed)

# 필요한 열만 선택 및 결측치 제거
subset = data[['ram', 'storage', 'battery', 'weight', 'cpu_speed', 'display_size', 'price_usd']].dropna()

# 독립 변수와 종속 변수 설정
X = subset[['ram', 'storage', 'battery', 'weight', 'cpu_speed', 'display_size']]
y = subset['price_usd']

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 다항 회귀 피처 생성
degree = 2  # 다항 차수
poly = PolynomialFeatures(degree)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# 모델 학습
model = LinearRegression()
model.fit(X_train_poly, y_train)

# 예측 및 평가
y_pred_train = model.predict(X_train_poly)
y_pred_test = model.predict(X_test_poly)

train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"훈련 데이터 RMSE: {train_rmse:.2f}, R²: {train_r2:.2f}")
print(f"테스트 데이터 RMSE: {test_rmse:.2f}, R²: {test_r2:.2f}")

# 예측 결과 시각화
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_test, alpha=0.7, label='예측 값 vs 실제 값')
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linestyle='--', label='이상적')
plt.title('실제 가격 vs 예측 가격')
plt.xlabel('실제 가격 (USD)')
plt.ylabel('예측 가격 (USD)')
plt.legend()
plt.grid(True)
plt.show()
