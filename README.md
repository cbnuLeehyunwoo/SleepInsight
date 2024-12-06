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
