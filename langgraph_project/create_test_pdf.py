from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import os


def create_test_pdf():
    # Register Korean font
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    pdfmetrics.registerFont(TTFont("NanumGothic", font_path))

    # Create directory if it doesn't exist
    os.makedirs("documents", exist_ok=True)

    # Create PDF
    c = canvas.Canvas("documents/test.pdf", pagesize=letter)
    c.setFont("NanumGothic", 10)

    # Content about King Jangsu
    text = """고구려 장수왕(長壽王)의 영토 확장과 정책에 관한 역사적 기록

1. 장수왕의 즉위와 초기 정책 (391-413)
장수왕은 391년 광개토대왕의 아들로 즉위했다. 초기에는 아버지의 정책을 계승하여 영토 확장과 
중앙집권화를 추진했다. 특히 다음과 같은 정책들을 실행했다:
- 평양 천도 계획 수립 (392년)
- 북쪽 말갈족 정벌 (395-398년)
- 요동 지역 방어 체계 강화 (400-405년)

2. 평양 천도와 남진 정책 (427-450)
427년, 장수왕은 국내성에서 평양으로 수도를 옮겼다. 이는 다음과 같은 목적을 가지고 있었다:
- 한반도 중부 진출을 위한 전진 기지 확보
- 중국과의 교역로 확장
- 백제 견제를 위한 전략적 거점 마련

3. 대외 관계와 외교 정책
장수왕은 적극적인 대외 정책을 펼쳤다:
- 북위(北魏)와의 조공 관계 수립 (435년)
- 송(宋)과의 교류 확대 (450년대)
- 신라와의 동맹 관계 강화 (439년)

4. 백제 공격과 한강 유역 장악 (475)
475년, 장수왕은 백제 개로왕을 격파하고 한성을 함락시켰다:
- 한강 유역 전역 점령
- 백제 수도 한성 함락
- 개로왕 전사
- 백제의 웅진 천도 유발

5. 행정 제도 개혁
장수왕은 확장된 영토를 효율적으로 통치하기 위해 다음과 같은 제도를 도입했다:
- 5부 행정구역 체계 확립
- 지방관 파견 제도 정비
- 군사령부 설치
- 조세 제도 개편

6. 문화 정책
장수왕은 고구려의 문화 발전도 적극 추진했다:
- 불교 진흥 정책 실시
- 태학 설립과 교육 제도 정비
- 율령 반포
- 기록 문화 발전

7. 군사 제도 개혁
영토 확장을 뒷받침하기 위한 군사 제도 개혁을 실시했다:
- 기병 부대 강화
- 보병 체계 정비
- 성곽 방어 체계 구축
- 군량 보급 체계 확립

8. 장수왕 치세의 의의
장수왕의 재위 기간(391-491)은 고구려 역사상 가장 긴 100년이었으며, 다음과 같은 의의를 가진다:
- 고구려 최대 영토 확보
- 한반도 중부 지역 장악
- 동아시아 국제 질서에서 주도적 역할 수행
- 중앙집권체제 완성

이러한 장수왕의 업적은 고구려가 동아시아의 강대국으로 성장하는 결정적 기반이 되었다."""

    # Write text to PDF
    y = 750  # Starting y position
    for line in text.split("\n"):
        # Check if we need a new page
        if y < 50:
            c.showPage()
            c.setFont("NanumGothic", 10)
            y = 750

        # Write the line
        if line.strip():
            # Handle section titles (lines ending with numbers in parentheses)
            if any(year in line for year in ["(391-413)", "(427-450)", "(475)"]):
                c.setFont("NanumGothic", 12)
                c.drawString(50, y, line)
                c.setFont("NanumGothic", 10)
            else:
                # Split long lines to fit page width
                words = line.split()
                current_line = words[0]
                for word in words[1:]:
                    if (
                        c.stringWidth(current_line + " " + word, "NanumGothic", 10)
                        < 500
                    ):
                        current_line += " " + word
                    else:
                        c.drawString(50, y, current_line)
                        y -= 15
                        current_line = word
                c.drawString(50, y, current_line)
            y -= 15  # Move down for next line

    c.save()
    print("테스트 PDF 파일이 생성되었습니다: documents/test.pdf")


if __name__ == "__main__":
    create_test_pdf()
