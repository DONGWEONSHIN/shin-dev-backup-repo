# 📜 음식점 클러스터링 지도 프로젝트 (Food Map Clustering Project)

서울시 일반음식점 데이터를 기반으로, 음식점 위치를 클러스터링하여 주요 상권을 시각화하는 프로젝트입니다.  
지도 기반의 상권 분석, 밀도 기반 클러스터링(DBSCAN), 중심 기반 클러스터링(KMeans, MeanShift) 등을 활용합니다.

---

## 📁 프로젝트 구성

```
foodmap-clustering-project/
├── data/              # 원본 및 전처리된 CSV 파일
├── notebooks/         # 단계별 분석 노트북 (01~03)
├── outputs/           # 지도, 시각화 이미지, 결과 HTML
├── src/               # 재사용 가능한 코드 (전처리, 클러스터링 등)
├── docs/              # 문서 및 분석 요약, 발표자료
├── README.md          # 현재 문서
├── requirements.txt   # 필수 라이브러리 목록
├── .gitignore         # Git 제외 파일 설정
```

---

## 🔧 사용 방법

### 1. 환경 설정 (Miniconda 권장)

```bash
conda create -n foodmap-env python=3.10
conda activate foodmap-env
pip install -r requirements.txt
```

### 2. Jupyter 노트북 실행

```bash
jupyter lab
```

### 3. 분석 단계

| 단계 | 파일 | 설명 |
|------|------|------|
| 1️⃣ | `01_data_cleaning.ipynb` | 데이터 로딩, 좌표 변환 (EPSG:2097 → 위경도) |
| 2️⃣ | `02_clustering.ipynb` | KMeans/DBSCAN/MeanShift로 군집화 |
| 3️⃣ | `03_visualization.ipynb` | Folium 지도에 클러스터 시각화 |

---

## 📊 주요 기능

- ✅ 공공데이터 기반 좌표 변환 및 정제
- ✅ KMeans 기반 중심 클러스터링 (Elbow, Silhouette 실험)
- ✅ DBSCAN 기반 밀도 클러스터링 (노이즈 감지)
- ✅ MeanShift로 자동 클러스터 수 탐지
- ✅ Folium 기반 지도 시각화

---

## 📌 데이터 출처

- 서울 열린데이터광장:  
  [서울시 일반음식점 인허가 정보](https://data.seoul.go.kr/dataList/OA-16094/S/1/datasetView.do)

---

## ✨ 향후 발전 방향

- 클러스터별 업종 분석 및 상권 유형 분류
- 웹앱(Streamlit 등)으로 시각화 인터페이스 구현
- 상권 추천 시스템 확장

---

## 👤 작성자

| 이름 | GitHub |
|------|--------|
| DONGWEONSHIN | [@DONGWEONSHIN](https://github.com/DONGWEONSHIN) |
