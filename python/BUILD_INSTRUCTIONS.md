# 숫자 맞추기 게임 빌드 가이드 (Build Instructions)

이 문서는 파이썬 코드를 실행 파일(`.exe` 또는 `.app`)로 만드는 방법을 설명합니다.

## 1. 사전 준비 (Prerequisites)

빌드 전에 아래 라이브러리들이 설치되어 있어야 합니다.

```bash
# UI 및 이미지 라이브러리 설치
pip install customtkinter Pillow

# 빌드 도구 설치
pip install pyinstaller
```

## 2. 운영체제별 빌드 명령어

터미널(또는 PowerShell)에서 `python/` 폴더로 이동한 후 아래 명령어를 실행하세요.

### 윈도우 (Windows - .exe 파일)
```powershell
pyinstaller --noconsole --onefile --add-data "Paperlogy-5Medium.ttf;." --name "숫자맞추기" num_guess.py
```
*   **주의**: 윈도우는 파일 경로 구분자로 세미콜론(`;`)을 사용합니다.

### 맥 (macOS - .app 패키지)
```bash
pyinstaller --noconsole --onefile --windowed --add-data "Paperlogy-5Medium.ttf:." --name "숫자맞추기" num_guess.py
```
*   **주의**: 맥은 파일 경로 구분자로 콜론(`:`)을 사용합니다.
*   `--windowed` 옵션은 맥 전용 앱 번들을 생성하는 데 필수입니다.

## 3. 주요 참고 사항

1.  **결과물 위치**: 빌드가 완료되면 프로젝트 폴더 내의 `dist/` 폴더 안에 실행 파일이 생성됩니다.
2.  **폰트 내장**: 위 명령어들은 `Paperlogy-5Medium.ttf` 폰트 파일을 실행 파일 안에 포함시킵니다. 사용자가 별도로 폰트를 설치할 필요가 없습니다.
3.  **임시 폴더**: 실행 파일은 실행 시 시스템 임시 폴더에 리소스를 풀어서 사용하며, 프로그램 종료 시 자동으로 해당 폴더를 삭제합니다.
4.  **아이콘**: 만약 전용 아이콘(`.ico` 또는 `.icns`)을 사용하고 싶다면 명령어에 `--icon="아이콘파일경로"` 옵션을 추가하면 됩니다.
