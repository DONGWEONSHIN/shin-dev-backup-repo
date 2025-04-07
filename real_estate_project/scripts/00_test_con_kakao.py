# 03_test_api_connection_kakao.py

import os

import requests
from dotenv import load_dotenv

# 1. 환경 변수 불러 오기
load_dotenv()
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

# 2. 테스트할 주소
# address = "서울 마포구 대흥로 175"
# address = "서울 마포구 마포대로 115-8"
address = "서울 마포구 방울내로1길 41-14"

# 3. 주소 -> 위경도 변환 함수 (카카오)
res = requests.get(
    "https://dapi.kakao.com/v2/local/search/address.json",
    params={"query": address},
    headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"},
)

# 4. 결과 확인
print(res.json())
