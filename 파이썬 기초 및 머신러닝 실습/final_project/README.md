# 지뢰찾기 헬퍼 (Minesweeper Helper)

지뢰찾기 게임을 플레이할 때 지뢰의 위치를 예측하여 시각적으로 표시해주는 도구입니다.

## 주요 기능

* **특정 키 입력 감지**: 사용자가 지정한 특정 키(기본값: F9)를 누르면 헬퍼 기능이 활성화됩니다.
* **게임 화면 캡처**: 활성화된 지뢰찾기 게임 화면을 캡처합니다.
* **이미지 분석**: 캡처된 이미지에서 각 셀의 숫자, 빈칸, 깃발, 그리고 지뢰로 추정되는 위치를 분석합니다.
* **지뢰 위치 표시**: 분석된 정보를 바탕으로 지뢰가 있을 것으로 예상되는 위치를 화면에 표시합니다.

## 설치 방법

### 요구 사항

* Python 3.6 이상
* 필수 라이브러리: keyboard, Pillow, OpenCV-Python, NumPy

### 설치 과정

1. 저장소를 클론하거나 다운로드합니다.
2. 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

## 사용 방법

1. 프로그램을 실행합니다.

```bash
python main.py
```

2. 지뢰찾기 게임을 실행합니다.
3. 게임 화면이 보이는 상태에서 F9 키(또는 설정된 트리거 키)를 누릅니다.
4. 지뢰찾기 헬퍼가 게임 화면을 분석하여 지뢰 위치를 예측합니다.
5. 예측된 지뢰 위치가 화면에 표시됩니다.

## 설정 변경

설정 메뉴에서 다음 항목을 변경할 수 있습니다:

* 트리거 키
* 캡처 모드 (전체 화면, 활성 창, 지정 영역)
* 표시 모드 (오버레이, 창, 이미지)
* 오버레이 색상 및 두께
* 디버그 모드 활성화/비활성화

## 프로젝트 구조

```
minesweeper_helper/
│
├── main.py                     # 메인 실행 파일
├── requirements.txt            # 필요한 라이브러리 목록
├── README.md                   # 프로젝트 설명 및 사용 방법
│
├── config/                     # 설정 관련 파일
│   ├── __init__.py
│   └── settings.py             # 기본 설정 값 및 설정 관리
│
├── core/                       # 핵심 기능 모듈
│   ├── __init__.py
│   ├── key_listener.py         # 키 입력 감지 모듈
│   ├── screen_capture.py       # 화면 캡처 모듈
│   ├── image_processor.py      # 이미지 전처리 모듈
│   ├── grid_detector.py        # 게임 격자 감지 모듈
│   ├── cell_analyzer.py        # 셀 내용 분석 모듈
│   ├── mine_predictor.py       # 지뢰 위치 예측 모듈
│   └── result_display.py       # 결과 표시 모듈
│
├── utils/                      # 유틸리티 함수
│   ├── __init__.py
│   ├── image_utils.py          # 이미지 처리 유틸리티
│   ├── logging_utils.py        # 로깅 유틸리티
│   └── debug_utils.py          # 디버깅 유틸리티
│
├── gui/                        # GUI 관련 모듈
│   ├── __init__.py
│   ├── main_window.py          # 메인 GUI 창
│   ├── settings_dialog.py      # 설정 다이얼로그
│   └── overlay.py              # 게임 화면 위에 표시할 오버레이
│
├── resources/                  # 리소스 파일
│   └── templates/              # 템플릿 매칭용 이미지
│
└── tests/                      # 테스트 코드
    └── __init__.py
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
