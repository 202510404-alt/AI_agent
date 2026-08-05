Task 2: 파일 a 내부 지도 읽기 및 터미널 출력 실행 코드 구현
ID: TASK-002

Target File: a [📂 a]

의존성: TASK-001

설명:

a 파일 내에 Python 또는 관련 실행 스크립트로 지도 파일 내용을 읽는 코드 작성.

지도 파일의 텍스트 내용을 읽어 터미널 표준 출력(sys.stdout / print)으로 출력하는 메인 실행 로직 추가.

디버깅 로그 명세 (DebugLogSpec):

Location: 파일 출력 완료 직후

Message: [DEBUG_LOG] Codebase map file content successfully read and printed. Line count: {line_count}

Predict Output: [DEBUG_LOG] Codebase map file content successfully read and printed. Line count: 41 (또는 실제 출력 줄 수)

Toggle Key: DEBUG_TASK_002

단독 실행 진입점 (standalone_entrypoint):

python3 a

예측 동작 요약 (predicted_summary):

a 파일을 단독 실행 시 AI 코드베이스 맵의 텍스트가 터미널에 정상적으로 출력되고 디버그 로그가 기록됩니다.