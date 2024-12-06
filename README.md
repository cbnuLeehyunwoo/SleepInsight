# 충북대학교 오픈소스개발프로젝트
---
## 오픈소스 API를 활용한 데이터 수집 및 분석을 목표로 한 기말 프로젝트

## ⏲ 프로젝트 기간
2024.11.12 ~ 2024.12.08

## 📁📋 데이터셋: 2017~2024년 11월 까지의 스마트폰 정보(제조사, 가격, RAM, OS, CPU.. 등등)
https://www.kaggle.com/datasets/jakubkhalponiak/phones-2024

##이상치 처리 및 결측치 제거:
1. 태블릿 데이터 제외
2. cubot사의 Cubot KingKongX 스마트폰 제외(배터리 크기가 너무 크게 출시됨, 평균값의 두배 이상)
3. CPU 데이터가 사진처럼 문자열로 되어있었기 때문에 
![image](https://github.com/user-attachments/assets/91ea2743-8419-43ee-852f-88b5c648b9ad)
정규 표현식을 통해 CPU의 총 클럭을 숫자로 변환하는 과정에서 문자로만 표현된 행들에 대한 처리를 고민하다가 제외하기로 결정(36개 데이터)
![image](https://github.com/user-attachments/assets/8ac6b194-e869-4f12-8ffb-65b82bf72d3f)

## 데이터 분석
가격과 변수들 간의 관계를 회귀선을 포함한 산점도로 표현
1. 가격과 CPU 성능과의 관계          
![image](https://github.com/user-attachments/assets/17036c2a-92c9-4db2-b23d-50503d51fa48)

2. 가격과 배터리 간의 관계        
![image](https://github.com/user-attachments/assets/77ae90d5-b3ca-48cf-823f-73ce3195422c)

3. 가격과 스마트폰 무게와의 관계
![image](https://github.com/user-attachments/assets/7112ef9a-be5f-4af4-b937-e1006fd493ed)

5. 가격과 화면 크기와의 관계        
![image](https://github.com/user-attachments/assets/6c03049e-21c7-4243-909c-9bc47a3a59ac)

6. 가격과 램의 관계          
![image](https://github.com/user-attachments/assets/c7f091a6-55b2-4d2b-9539-4c2e32e71165)

7. 가격과 저장공간의 관계         
![image](https://github.com/user-attachments/assets/92860a3b-dd51-4051-9edf-e132bf5f3a73)

OS 별로 그룹화하여 각 컬럼의 평균을 막대그래프로 표현
iOS, Android, Others
iOS, Android 외의 OS는 표본이 너무 적기 때문에Others 그룹으로 그룹화(Harmony OS, EMUI) 
1. OS별 개수           
![image](https://github.com/user-attachments/assets/f1d3af33-f819-49af-b2d4-183f3101fab9)

2. OS별 평균 램              
![image](https://github.com/user-attachments/assets/5a77285d-e7fc-47f4-a53a-f224697c9a5d)

3. OS별 평균 OS            
![image](https://github.com/user-attachments/assets/72d1ae18-c6d6-4f2d-b95b-d0463b7857f3)

4. OS별 평균 CPU 속도          
![image](https://github.com/user-attachments/assets/36fdd559-85e9-4b3e-829c-90a3c9c12028)

5. OS별 평균 가격           
![image](https://github.com/user-attachments/assets/2f444f91-20b6-4237-99da-e13472e71dca)

6. OS별 가격 표준편차         
![image](https://github.com/user-attachments/assets/95dca55b-874a-4308-b90c-d2e31f6ae72d)

## 머신러닝          
종속변수: ram, storage, battery, weight, cpu_speed, display_size       
독립변수: price_usd        
단항회귀 그래프 및 성능평가     
![image](https://github.com/user-attachments/assets/3f347286-1922-4429-8c51-cc786a1cf766)
![image](https://github.com/user-attachments/assets/591c61ca-117d-46ca-aeac-ceae4e0dad88)

다항회귀 그래프(2차) 및 성능평가         
![image](https://github.com/user-attachments/assets/7f314db9-7753-4d8b-8ea2-0d1f3141a14b)
![image](https://github.com/user-attachments/assets/119c48d8-826a-4b9c-976c-0f0c98c796d6)
     
다항회귀의 성능이 더 우수한 것을 알 수 있으며 Project_Machine.py 파일에는 현재 다항회귀가 구현되어있음

##응용 방향 설계
어플리케이션 Smartphone-insight 설계 제안
본 애플리케이션은 출시된 스마트폰의 정보를 기반으로 다음과 같은 기능을 수행한다
1. 스마트폰 스펙을 입력하면 해당 조건에 맞는 스마트폰 추천
2. 스펙과 가격을 입력하면 해당 가격의 합리성 여부 분석, 합리적이지 않다면 합리적인 제품들 추천
3. 향후 출시될 스마트폰의 가격 예측

