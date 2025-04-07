import os

import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import train_test_split

# 1. 데이터 로드
INPUT_PATH = "../data/cleaned_apt_trades_mapo_2024.csv"
df = pd.read_csv(INPUT_PATH)

# 2. 특성과 타깃 정의
features = ["area_m2", "floor", "year_built", "lat", "lng"]
target = "price"

X = df[features]
y = df[target]

# 3. 학습/검증 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# 4. 모델 정의 및 학습
model = xgb.XGBRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=4,
    random_state=42,
)

model.fit(X_train, y_train)

# 5. 예측 및 평가
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

print(f"MAE (평균 오차): {mae:.2f} 만원")
print(f"RMSE (제곱 평균 오차): {rmse:.2f} 만원")

# 6. 예측 결과 일부 출력
y_test_sample = y_test.reset_index(drop=True)
compare_df = pd.DataFrame(
    {
        "실제값": y_test_sample,
        "예측값": np.round(y_pred, 0),
    }
)
print("\n 예측 결과 샘플:")
print(compare_df.head(10))

# 7. 모델 저장
os.makedirs("../models", exist_ok=True)
joblib.dump(model, "../models/xgboost_price_model.pkl")
print("모델 저장 완료: xgboost_price_model.pkl")
