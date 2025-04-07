import os
import time
import xml.etree.ElementTree as ET

import pandas as pd
import requests
import subprocess
from dotenv import load_dotenv

# . env 파일에서 환경 변수 로드
load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

# 마포구 LAWD 코드
LAWD_CD = "11440"

# 수집 범위: 2024년 1월 ~ 12월
DEAL_YMDS = [f"2024{str(month).zfill(2)}" for month in range(1, 13)]

# 결과 누적 리스트
all_rows = []

for DEAL_YMD in DEAL_YMDS:
    print(f"요청 중: {DEAL_YMD}")

    # 저장용 임시 파일 경로
    OUTFILE = f"../data/tmp_{DEAL_YMD}.xml"

    url = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
    full_url = f"{url}?serviceKey={SERVICE_KEY}&LAWD_CD={LAWD_CD}&DEAL_YMD={DEAL_YMD}&pageNo=1&numOfRows=1000"

    # curl 명령어 실행
    curl_command = [
        "curl",
        "-s",
        "-X",
        "GET",
        full_url,
        "-H",
        "User-Agent: Mozilla",
        "-o",
        OUTFILE,
    ]

    subprocess.run(curl_command, check=True)

    # XML 파싱
    try:
        tree = ET.parse(OUTFILE)
        root = tree.getroot()

        result_code = root.findtext(".//resultCode")

        if result_code == "000":
            for item in root.iter("item"):
                try:
                    row = {
                        "아파트": item.findtext("aptNm"),
                        "법정동": item.findtext("umdNm"),
                        "도로명주소": f'{item.findtext("roadNm")} {int(item.findtext("roadNmBonbun"))}',
                        "거래금액": item.findtext("dealAmount")
                        .replace(",", "")
                        .strip(),
                        "전용면적": item.findtext("excluUseAr"),
                        "층": item.findtext("floor"),
                        "건축년도": item.findtext("buildYear"),
                        "계약일": f'{item.findtext("dealYear")}-{item.findtext("dealMonth").zfill(2)}-{item.findtext("dealDay").zfill(2)}',
                    }
                    all_rows.append(row)
                except Exception as e:
                    print("파싱 오류 (개별 항목):", e)
        else:
            print(f"요청 실패 (code: {result_code})")

    except Exception as e:
        print(f"XML 파싱 오류 ({DEAL_YMD}):", e)

# pandas DataFrame으로 변환 후 저장
df = pd.DataFrame(all_rows)
df.to_csv("../data/apt_trades_mapo_2024.csv", index=False, encoding="utf-8-sig")

print("저장 완료: apt_trades_mapo_2024.csv")
print(f"총 {len(df)} 건의 거래 데이터가 저장되었습니다.")
