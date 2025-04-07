import joblib
import matplotlib.pyplot as plt
import pandas as pd
import shap

# 1. 데이터 및 모델 로드
df = pd.read_csv("../data/cleaned_apt_trades_mapo_2024.csv")
model = joblib.load("../models/xgboost_price_model.pkl")

# 2. SHAP explainer 생성
features = ["area_m2", "floor", "year_built", "lat", "lng"]
X = df[features]
explainer = shap.Explainer(model)
shap_values = explainer(X)

# %matplotlib inline
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# 3. 변수 중요도 시각화 (summary plot)
plt.figure()
plt.title("SHAP 변수 중요도 순위")
shap.plots.beeswarm(shap_values, show=False)
plt.tight_layout()
plt.savefig("../outputs/shap_summary_plot.png")
plt.close()
print("SHAP 변수 중요도 그래프 저장 완료 : shap_summary_plot.png")

# 4. 의사결정 예시 하나 출력
plt.figure()
sample_index = 0  # 첫 번째 샘플
shap.plots.waterfall(shap_values[sample_index], max_display=10, show=False)
plt.tight_layout()
plt.savefig("../outputs/shap_waterfall_sample0.png")
plt.close()
print("예시 거래에 대한 SHAP 해석 그래프 저장 완료: shap_waterfall_sample0.png")
