# AI Agent — Jjap-Cursor / ASE-OS

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Indexer-Prototype%20Ready-green)
![Status](https://img.shields.io/badge/Agent%20Core-WIP-yellow)
![License](https://img.shields.io/badge/License-Private-lightgrey)

> **LLM 친화적 코드베이스 인덱싱 + 멀티 에이전트 자동화**를 목표로 하는 AI 코딩 에이전트 플랫폼입니다.  
> "좋은 LLM보다 좋은 Retriever" 철학 아래, 토큰을 최소화하면서 정확한 컨텍스트만 AI에게 전달하는 파이프라인을 구축합니다.

---

## 개요

| 구분 | 설명 |
|------|------|
| **핵심 목표** | 코드베이스를 AST/심볼 단위로 분석하고, AI 최적화 지도를 생성한 뒤, 에이전트가 필요한 코드만 정밀 추출·수정 |
| **설계 철학** | AI Map → Slice → Task → Patch — 전체 파일 대신 **필요한 심볼만** 로드 |
| **SSOT 문서** | [`agent_plan.md`](./agent_plan.md) — 아키텍처, 레이어, 인터페이스 규격의 단일 진실 공급원 |
| **AI 지도** | [`system_maps/AI_CODEBASE_MAP.md`](./system_maps/AI_CODEBASE_MAP.md) — 에이전트용 초경량 코드베이스 지도 |

---

## 개발 상태

| 모듈 | 상태 | 설명 |
|------|:----:|------|
| 🟢 **Universal Indexer & File Extractor** (`tools/universal_indexer/`) | **프로토타입 완료** | 다언어 AST/심볼 분석, AI 지도 생성, 코드 슬라이싱·추출, 실시간 Watcher, GUI Navigator |
| 🟡 **Multi-Agent Utilities** (`tools/multi_agent_system/`) | **부분 구현** | 코드 패처, 터미널 실행기, 세션 관리 등 기반 모듈 존재 |
| 🚧 **Agent Core** (`agent_core/`) | **개발 진행 중 (WIP)** | Gemini 플래너, 프롬프트 빌더, Task Graph, Validator 등 [`agent_plan.md`](./agent_plan.md) 기준 순차 구현 예정 |
| ⚪ **Extraction Target** (`extraction_target_project/`) | **테스트용 샘플** | 인덱서·추출기 검증용 대상 폴더 (내부 코드 내용은 프로젝트 기능과 무관) |

### 레이어별 진행률 (요약)

```
Level 0  Knowledge Layer (Indexer/Map/Retriever)  ████████░░  ~80%  🟢
Level 1  Project Memory                           ███░░░░░░░  ~30%  🟡
Level 2+ Agent Pipeline (Planner → Validator)    ░░░░░░░░░░   ~5%  🚧
```

---

## 프로젝트 구조

```
AI_agent/
├── start.py                          # 🚀 통합 기동 스크립트 (환경 세팅 + 파이프라인 실행)
├── agent_plan.md                     # 📋 아키텍처 SSOT (v1.3)
│
├── agent_core/                       # 🚧 에이전트 코어 (WIP)
│   └── plan/
│       ├── gemini_client.py          #   Gemini API 클라이언트
│       ├── prompt_builder.py         #   프롬프트 빌더
│       └── schemas.py                #   공통 스키마 정의
│
├── tools/
│   ├── universal_indexer/            # 🟢 Universal Indexer & Extractor
│   │   ├── indexer.py                #   AST/심볼 인덱서 (Python, JS, Java 등)
│   │   ├── create_ai_map.py          #   AI_CODEBASE_MAP.md 생성
│   │   ├── agent_navigator.py        #   GUI 기반 심볼 검색·추출
│   │   ├── jjap_watcher.py           #   파일 변경 실시간 감시
│   │   ├── jjap_retriever.py         #   심볼 단위 코드 추출
│   │   ├── context_builder.py        #   AI용 압축 컨텍스트 빌더
│   │   ├── switch.py                 #   스캔 대상 모드 토글 (ROOT / EXTRACTION_TARGET)
│   │   └── core_parsers/             #   언어별 파서 (py, js, java, json …)
│   │
│   └── multi_agent_system/           # 🟡 멀티 에이전트 유틸리티
│       ├── code_patcher.py
│       ├── terminal_runner.py
│       └── agent_session.py
│
├── extraction_target_project/        # ⚪ 인덱서 테스트용 샘플 프로젝트
│
└── system_maps/                      # 📂 생성된 코드베이스 지도
    ├── AI_CODEBASE_MAP.md            #   AI 최적화 초경량 지도
    └── CODEBASE_MAP.md               #   상세 코드베이스 지도
```

---

## 빠른 시작

### 사전 요구 사항

| 항목 | 내용 |
|------|------|
| Python | **3.10+** 권장 (최소 3.8) |
| OS | Windows / macOS / Linux |
| 필수 패키지 | `watchdog` (실시간 파일 감시) |
| 선택 | `.venv` 가상환경, `google-genai` (Agent Core Gemini 연동 시) |

### 1. 가상환경 및 의존성 설치

```bash
# 가상환경 생성 (권장)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 필수 패키지 설치
pip install watchdog
```

> `start.py` 실행 시 `watchdog`이 없으면 **자동 설치**를 시도합니다.

### 2. 통합 파이프라인 실행 (`start.py`)

프로젝트 루트에서 아래 명령을 실행하면 전체 파이프라인이 기동됩니다.

```bash
python start.py
```

**실행 순서:**

| 단계 | 동작 |
|:----:|------|
| 0 | 의존성 검사 (`watchdog` 자동 설치) |
| 0-B | 인덱서 실행 → `AI_CODEBASE_MAP.md` 선제 생성 |
| 1 | 백그라운드 **Watcher** 가동 (파일 변경 실시간 감지) |
| 2 | **Agent Navigator** GUI 창 실행 (심볼 검색·추출) |
| 3 | GUI 종료 시 Watcher 자동 정리 |

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  start.py   │ ──▶ │  Indexer +   │ ──▶ │  jjap_watcher   │ (백그라운드)
│  (Launchpad)│     │  AI Map 생성  │     └─────────────────┘
└─────────────┘     └──────────────┘              │
                                                  ▼
                                         ┌─────────────────┐
                                         │ agent_navigator │ (GUI)
                                         └─────────────────┘
```

### 3. AI 코드 지도만 생성 (`create_ai_map.py`)

지도만 별도로 갱신하려면 **프로젝트 루트**에서 아래 순서로 실행합니다.

```bash
# Windows (PowerShell) — PYTHONPATH 설정
$env:PYTHONPATH=".;tools/universal_indexer"

# macOS / Linux
export PYTHONPATH=".:tools/universal_indexer"

# 1단계: 심볼 인덱싱 (system_memory/ 장부 생성)
python -c "from indexer import AdvancedIndexerV2; from pathlib import Path; AdvancedIndexerV2(Path('.')).scan_project()"

# 2단계: AI 최적화 지도 생성
python tools/universal_indexer/create_ai_map.py
```

> `start.py`는 위 과정을 자동으로 수행하므로, 일반적으로는 `python start.py`만 실행하면 됩니다.

**출력 파일:**

| 파일 | 위치 | 설명 |
|------|------|------|
| `.jjap_context.json` | `system_memory/` | 통합 심볼·파일 컨텍스트 장부 |
| `AI_CODEBASE_MAP.md` | `system_maps/` | AI 에이전트용 초경량 코드 지도 |
| `CODEBASE_MAP.md` | `system_maps/` | 상세 코드베이스 지도 |

---

## 스캔 모드 설정

[`tools/universal_indexer/switch.py`](./tools/universal_indexer/switch.py)에서 스캔 대상을 변경할 수 있습니다.

| 모드 | 값 | 스캔 범위 |
|------|-----|-----------|
| **ROOT** (기본) | `"ROOT"` | 프로젝트 전체 |
| **타깃 폴더** | `"EXTRACTION_TARGET_PROJECT"` | `extraction_target_project/` 내부만 |

```python
# tools/universal_indexer/switch.py
SCAN_MODE = "ROOT"  # 또는 "EXTRACTION_TARGET_PROJECT"
```

---

## 주요 기능 (Indexer)

- **다언어 AST/심볼 분석** — Python, JavaScript, Java, JSON 등 (`core_parsers/`)
- **AI 최적화 코드베이스 지도** — `[📂 실제경로]` 규격의 `AI_CODEBASE_MAP.md` 자동 생성
- **정밀 코드 슬라이싱** — 클래스·함수 단위 추출, 불필요 주석·DEBUG 블록 제거
- **실시간 파일 감시** — 변경 시 인덱스·지도 자동 갱신 (`jjap_watcher.py`)
- **GUI Navigator** — 심볼 검색 및 컨텍스트 추출 UI (`agent_navigator.py`)

---

## Agent Core 로드맵 (WIP)

[`agent_plan.md`](./agent_plan.md)에 정의된 17-Phase 로드맵을 순차 구현 중입니다.

| Phase | 컴포넌트 | 상태 |
|:-----:|----------|:----:|
| — | Gemini Client, Prompt Builder, Schemas | 🟡 스텁 |
| 1~10 | Master Planner, Task Graph, Worker, Validator … | 🚧 미착수 |
| 11~13 | File Lock, Debug Log Verification, Session Merge | ⏸️ Deferred |
| 14~17 | Project Model Builder, Dependency Analyzer, Cost Estimator … | 🚧 미착수 |

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [`agent_plan.md`](./agent_plan.md) | 아키텍처 SSOT, 레이어 정의, 인터페이스 규격 |
| [`tools/universal_indexer/README.md`](./tools/universal_indexer/README.md) | 인덱서 상세 사용법 및 4대 코어 프로토콜 |
| [`system_maps/AI_CODEBASE_MAP.md`](./system_maps/AI_CODEBASE_MAP.md) | AI 에이전트용 코드베이스 지도 (자동 생성) |

---

## 라이선스

Private — 내부 개발 프로젝트
