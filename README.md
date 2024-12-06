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

4. 가격과 화면 크기와의 관계
![image](https://github.com/user-attachments/assets/6c03049e-21c7-4243-909c-9bc47a3a59ac)

5. 가격과 램의 관계
![image](https://github.com/user-attachments/assets/c7f091a6-55b2-4d2b-9539-4c2e32e71165)

6. 가격과 저장공간의 관계
![image](https://github.com/user-attachments/assets/92860a3b-dd51-4051-9edf-e132bf5f3a73)




