import os
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import subprocess

# 인증키 불러오기
load_dotenv()
SERVICE_KEY = os.getenv("SERVICE_KEY")

# 설정
LAWD_CD = "11440"
DEAL_YMD = "202401"
OUTFILE = "../data/test_response.xml"

# curl 명령어 구성
url = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTradeDev/getRTMSDataSvcAptTradeDev"
full_url = f"{url}?serviceKey={SERVICE_KEY}&LAWD_CD={LAWD_CD}&DEAL_YMD={DEAL_YMD}&pageNo=1&numOfRows=10"

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
# print("curl 명령어:", " ".join(curl_command))

# curl 실행
print("curl 요청 실행 중...")
subprocess.run(curl_command, check=True)
print("XML 파일 저장 완료")

# XML 파싱
tree = ET.parse(OUTFILE)
root = tree.getroot()

# 정상 여부 확인
result_code = root.findtext(".//resultCode")
result_msg = root.findtext(".//resultMsg")


if result_code == "000":
    print("API 요청 성공")
    print("예시 데이터")
    for item in root.iter("item"):
        apt = item.findtext("aptNm")
        price = item.findtext("dealAmount").replace(",", "").strip()
        print(f"- 아파트명: {apt}, 거래금액: {price}")
    print("테스트 완료!")
else:
    print(f"API 요청 실패 : {result_msg} (코드: {result_code})")
