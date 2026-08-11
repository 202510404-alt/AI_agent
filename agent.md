# 🤖 Jjap-Cursor / ASE-OS — AI Agent Operational Protocol (`agent.md`)

> **[AI 에이전트 필독 문서]**  
> 본 문서는 **Jjap-Cursor / ASE-OS** 프로젝트에서 작업하는 모든 AI 에이전트(LLM, Assistant, Agent Core 모듈 등)가 준수해야 할 행동 수칙, 대화형 RAG 작업 절차, 아키텍처 명세 및 검증 규격을 정의합니다.

---

## 📌 1. 프로젝트 개요 (Overview)

- **프로젝트 명**: AI Agent — Jjap-Cursor / ASE-OS
- **핵심 목표**: LLM 친화적 코드베이스 인덱싱 + 멀티 에이전트 자동화 파이프라인 구축
- **설계 철학**: **"좋은 LLM보다 좋은 Retriever"** (토큰 최소화, 정밀 코드 조각 기반 컨텍스트 제공)
- **주요 SSOT 문서**:
  - 📋 [`agent_plan.md`](./agent_plan.md) — 아키텍처, 레이어, 스키마 단일 진실 공급원 (v1.3)
  - 📜 [`System Prompt.md`](./System Prompt.md) — 에이전트 시스템 프롬프트 프로토콜
  - 🗺️ [`system_maps/AI_CODEBASE_MAP.md`](./system_maps/AI_CODEBASE_MAP.md) — AI용 초경량 코드베이스 지도

---

## ⚠️ 2. 절대 준수 5대 수칙 (Core Directives)

1. **경로 추측 절대 금지 (No Hallucination)**
   - 파일 경로, 함수명, 라인 번호를 절대로 임의로 추측하거나 생략하지 마십시오.
   - 반드시 [`system_maps/AI_CODEBASE_MAP.md`](./system_maps/AI_CODEBASE_MAP.md)의 `[📂 실제경로]`와 라인 번호(`[L시작-끝]`)에 기재된 명세를 사용합니다.

2. **기존 아키텍처 및 프로토콜 유지 (Preserve Architecture)**
   - 기존 클래스명, 함수 시그니처, 반환 튜플 구조, `self.vars` 프로토콜을 엄격히 준수합니다.
   - 존재하지 않는 헬퍼 메서드나 외부 라이브러리를 임의로 창조하지 마십시오.

3. **선(先) 수색, 후(後) 코딩 (Slice First, Code Later)**
   - 변경할 코드의 내부 구현을 모르는 상태에서 추측성 코드를 먼저 작성하지 마십시오.
   - 반드시 **Navigator Request** 또는 **Need More Context Protocol**을 사용해 코드 슬라이스를 먼저 요청 및 확인한 후 작업을 진행하십시오.

4. **컨텍스트 에스컬레이션 정책 준수 (Context Escalation Policy)**
   - 토큰 낭비를 막기 위해 전체 파일 요청은 원칙적으로 금지됩니다.
   - 정적 분석 실패나 심볼 해석 불가 등 명확한 사유가 입증된 경우에 한해 승인 후 에스컬레이션을 적용합니다.

5. **실제 검증 수행 후 완료 선언 (Always Verify)**
   - 파일 편집만으로 작업을 끝내지 마십시오.
   - 변경 후 반드시 검증 스크립트(`run_test.py` 또는 `start.py`)를 실행하여 테스트 통과 및 부작용 여부를 확인하고 최종 결과를 보고하십시오.

---

## 🏗️ 3. 시스템 구성 및 레이어 구조

```text
AI_agent/
├── agent_plan.md                     # 📋 최우선 SSOT 문서
├── agent.md                          # 🤖 에이전트 행동 수칙 (본 문서)
├── System Prompt.md                  # 📜 프롬프트 행동 강령
├── start.py                          # 🚀 통합 기동 스크립트
├── run_test.py                       # 🧪 통합 검증 스크립트
│
├── agent_core/                       # 🚧 Agent Core (WIP)
│   ├── plan/                         #   Gemini Planner, Prompt Builder, Schemas
│   ├── tasks/                        #   Task Graph & Task Management
│   ├── execution/                    #   Standalone Runner & Patcher
│   ├── validation/                   #   Result Validator
│   ├── llm/                          #   Gemini API Wrapper
│   └── memory/                       #   Project Model & Context Memory
│
├── tools/
│   ├── universal_indexer/            # 🟢 Universal Indexer & Extractor
│   │   ├── indexer.py                #   AST/심볼 인덱서
│   │   ├── create_ai_map.py          #   AI_CODEBASE_MAP.md 생성기
│   │   ├── agent_navigator.py        #   GUI/CLI 기반 심볼 검색·추출기
│   │   ├── jjap_retriever.py         #   심볼 단위 코드 정밀 추출기
│   │   ├── jjap_watcher.py           #   실시간 감시기
│   │   └── core_parsers/             #   언어별 파서 (py, js, java, tree-sitter)
│   │
│   └── multi_agent_system/           # 🟡 Multi-Agent Utilities
│       ├── code_patcher.py           #   코드 패처
│       ├── terminal_runner.py        #   터미널 실행기
│       └── agent_session.py          #   세션 관리기
│
└── system_maps/                      # 📂 초경량 코드베이스 지도
    ├── AI_CODEBASE_MAP.md
    └── CODEBASE_MAP.md
```

---

## 🔄 4. 에이전트 대화형 RAG 파이프라인 (Workflow)

```
[Step 1: 지도 파싱]      AI_CODEBASE_MAP.md 조회 → 타겟 파일/심볼 식별
         │
[Step 2: 슬라이스 요청]   [CLI_LOCATION_SPEC] 또는 JSON 프로토콜 출력
         │
[Step 3: 코드 수신]      Retriever가 추출한 정밀 컨텍스트 분석
         │
[Step 4: 정밀 패치]      최소 범위 코드 수정 및 리팩토링 수행
         │
[Step 5: 실행 및 검증]   run_test.py 단독 실행 및 로그/결과 대조
```

---

## 📝 5. 프로토콜 규격 (Protocols & Formats)

### 5.1 Navigator Request Format (CLI/GUI용)
에이전트가 코드 슬라이스를 요청할 때 출력하는 포맷입니다.

```text
[CLI_LOCATION_SPEC]
tools/universal_indexer/indexer.py:97-168
agent_core/plan/prompt_builder.py:20-55
```

### 5.2 Need More Context Protocol (표준 JSON)
에이전트 파이프라인 내부 자동 연동 시 사용하는 표준 요청 스키마입니다.

```json
{
  "need": [
    {
      "file": "tools/universal_indexer/indexer.py",
      "symbol": "index_file",
      "reason": "반환 튜플 및 심볼 메타데이터 스키마 확장 구조 확인 필요"
    }
  ]
}
```

### 5.3 디버깅 로그 예측-검증 규격 (Debug Log Protocol)
코드 수정 시 디버깅 로그를 삽입할 경우 사전 예측치와 실제 출력을 대조해야 합니다.

- **로그 포맷**: `[DEBUG_LOG][모듈명] 변수명: 값`
- **검증 절차**: 스크립트 실행 후 캡처된 로그 메시지가 사전 예측 문자열과 일치하는지 확인.

---

## 🧪 6. 검증 및 디버깅 가이드 (Validation)

- **테스트 실행**:
  ```bash
  python run_test.py
  ```
- **로그 및 모니터링 수칙**:
  - 기존 이모지 스타일의 한국어 로그 포맷을 유지할 것 (`🟢`, `🟡`, `🚨`, `🔍` 등)
  - 예외 발생 시 예외를 무시하지 않고 스택 트레이스 원인을 분석할 것.

---
*마지막 업데이트: 2026-08-11*
