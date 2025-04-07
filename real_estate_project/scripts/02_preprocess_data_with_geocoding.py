# preprocess_data_with_geocoding.py

import os

import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

# 1. 환경 변수 불러 오기
load_dotenv()
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

# 2. 파일 로드
INPUT_PATH = "../data/apt_trades_mapo_2024.csv"
OUTPUT_PATH = "../data/cleaned_apt_trades_mapo_2024.csv"
df = pd.read_csv(INPUT_PATH)

# 3. 컬럼 정리 (한글 -> 영문)
df = df.rename(
    columns={
        "아파트": "apt_name",
        "법정동": "district",
        "도로명주소": "road_address",
        "거래금액": "price",
        "전용면적": "area_m2",
        "층": "floor",
        "건축년도": "year_built",
        "계약일": "contract_date",
    }
)

# 4. 타입 변환 및 정리
for col in ["price", "area_m2", "floor", "year_built"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["contract_date"] = pd.to_datetime(df["contract_date"], errors="coerce")

# 5. 이상치 제거
initial_len = len(df)
df = df.dropna(subset=["price", "area_m2", "contract_date"])
df = df.dropna(subset=["road_address", "district", "apt_name"])
df = df[df["price"] > 0]
print(f"이상치 제거: {initial_len - len(df)}건 제거됨")

# 6. 도로명 주소 생성
df["address"] = "서울 마포구" + " " + df["road_address"]


# 7. 주소 -> 위경도 변환 함수 (카카오)
def geocode_address(addr):
    try:
        res = requests.get(
            "https://dapi.kakao.com/v2/local/search/address.json",
            params={"query": addr},
            headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
            timeout=3,
        )
        res.raise_for_status()
        documents = res.json().get("documents")
        if documents:
            return documents[0]["y"], documents[0]["x"]
        return None, None

    except:
        return None, None


# 8. tqdm 적용하여 위경도 수집
df["lat"] = None
df["lng"] = None

print("주소 -> 위경도 변환 중 ...")
for idx in tqdm(df.index):
    lat, lng = geocode_address(df.at[idx, "address"])
    df.at[idx, "lat"] = lat
    df.at[idx, "lng"] = lng

# 9. 저장
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
print(f"저장 완료: {OUTPUT_PATH}")
