# 사람 수 감지 프로젝트 (YOLOv5)

이 프로젝트는 YOLOv5 객체 탐지 모델을 활용하여 이미지 속 사람의 수를 자동으로 감지하고 카운트합니다.

## 주요 기능
- YOLOv5를 이용한 이미지 내 사람 객체 탐지
- 감지된 사람 수 카운트 및 시각화
- 결과 이미지 저장

## 필요 환경
- Python 3.8 이상
- PyTorch
- OpenCV
- numpy
- (선택) GPU 환경 권장

## 설치 및 실행 방법
1. YOLOv5 저장소 클론 및 환경 준비
    ```bash
    git clone https://github.com/ultralytics/yolov5.git
    cd yolov5
    pip install -r requirements.txt
    ```
2. 추가 라이브러리 설치
    ```bash
    pip install opencv-python numpy
    ```
3. `detect_people.ipynb` 노트북을 실행하여 `classroom.jpg` 등 이미지에서 사람 수를 감지합니다.

## 사용 예시
- `detect_people.ipynb`를 열고 셀을 순서대로 실행하면, `classroom.jpg` 이미지에서 사람을 감지하고, 감지 결과가 `output.jpg`로 저장됩니다.

## 참고사항
- `yolov5s.pt`는 사전학습된 YOLOv5 모델 가중치 파일입니다.
- 더 다양한 이미지를 분석하려면 `image_path`를 원하는 이미지 파일명으로 변경하세요.
- GPU 환경에서 실행하면 속도가 크게 향상됩니다.

## 파일 설명
- `detect_people.ipynb`: 메인 분석 코드
- `classroom.jpg`: 예제 이미지
- `output.jpg`: 결과 이미지(사람 감지 시각화)
- `yolov5s.pt`: 사전학습된 모델 가중치 파일 