# 🏙️ 서울 마포구 아파트 실거래가 분석 및 가격 예측 프로젝트

## 📌 프로젝트 개요

본 프로젝트는 서울 마포구의 아파트 실거래가 데이터를 기반으로,
- 가격 예측 머신러닝 모델을 학습하고
- SHAP을 통해 모델을 해석하며
- 지도 위에 '가성비 좋은 지역'을 시각화한 프로젝트입니다.

> ✅ 핵심 질문: **“서울 마포구에서 예측 대비 저렴하게 거래된 아파트는 어디인가?”**

---

## 🗂️ 폴더 구조

```
real_estate_project/
├── data/               # 데이터셋 (원본, 전처리 결과 포함)
├── models/             # 학습된 XGBoost 모델
├── outputs/            # 시각화 결과 (SHAP, 지도 등)
├── scripts/            # Python 실행 코드
├── notebooks/          # 주피터 노트북 (EDA)
├── .env                # API 키 저장 (gitignore 권장)
├── .gitignore
├── env.yml             # Conda 환경 정의
└── README.md
```

---

## 🔧 사용 기술

- **Python 3.10**, Conda 가상환경
- 📈 모델: `XGBoost`
- 💡 해석: `SHAP`
- 📍 지도 시각화: `folium`
- 🧹 전처리: `pandas`, `Kakao API`

---

## 📈 분석 흐름

1. **데이터 수집**  
   - 공공데이터포털 API 사용 (RTMSDataSvcAptTradeDev)
   - 도로명 주소 생성 → 카카오 API로 위경도 변환

2. **전처리 및 EDA**
   - 이상치 제거, 가격 정규화, 변수 분포 시각화

3. **가격 예측 모델 학습**
   - `XGBoost` 회귀 모델 학습
   - MAE, RMSE, R² 기반 평가

4. **모델 해석**
   - SHAP으로 전체 변수 중요도 및 개별 예측 해석

5. **지도 시각화**
   - 예측 vs 실제 가격 비율(`value_ratio`)로 가성비 마커 생성
   - 마커 색상으로 가성비 정도 표시 (`green` < `orange` < `red`)

---

## 📍 결과물 예시

- SHAP 요약 그래프: `outputs/shap_summary_plot.png`
- 예시 예측 해석: `outputs/shap_waterfall_sample0.png`
- 지도 결과물: `outputs/mapo_price_map.html`

---

## 📌 향후 발전 방향 (선택)

- Streamlit 대시보드 구현
- 기간별 시계열 예측 추가
- 주변 편의시설, 교통 등 피처 확장

---

## 🙌 기여

이 프로젝트는 머신러닝과 데이터 시각화를 학습하고 싶은 분들에게 열려 있습니다.  
PR이나 이슈 환영합니다! 😊

