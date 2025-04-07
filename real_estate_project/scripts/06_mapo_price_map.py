import folium
import joblib
import pandas as pd
from folium.plugins import MarkerCluster

# 1. 데이터 및 모델 로드
df = pd.read_csv("../data/cleaned_apt_trades_mapo_2024.csv")
model = joblib.load("../models/xgboost_price_model.pkl")

# 2. 예측값 계산 및 가성비 지표 생성
features = ["area_m2", "floor", "year_built", "lat", "lng"]
df["predicted"] = model.predict(df[features])
df["value_ratio"] = df["price"] / df["predicted"]  # 1보다 작으면 예측보다 저렴

# 3. 지도 생성 (마포구 중심)
m = folium.Map(location=[37.55, 126.94], zoom_start=13)
marker_cluster = MarkerCluster().add_to(m)

# 4. 마커 추가
for _, row in df.iterrows():
    color = (
        "green"
        if row["value_ratio"] < 0.9
        else ("orange" if row["value_ratio"] <= 1.1 else "red")
    )
    tooltip = f"{row['apt_name']} ({row['contract_date']})\n\n실제: {row['price']:.0f} / 예측: {row['predicted']:.0f}"
    folium.CircleMarker(
        location=(row["lat"], row["lng"]),
        radius=6,
        color=color,
        fill=True,
        fill_opacity=0.7,
        tooltip=tooltip,
    ).add_to(marker_cluster)

# 5. 저장
m.save("../outputs/mapo_price_map.html")
print("마포구 지도 저장 완료 : mapo_price_map.html")
