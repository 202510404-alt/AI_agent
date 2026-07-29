아래 6개 파일로 구성된 "AI 코드베이스 맵 생성기(Universal Indexer)"의 구조적 결함을 수정한다.
대상 파일: indexer.py, tree_sitter_parser.py, create_ai_map.py, js_parser.py, py_parser.py, java_parser.py

목표: 최종 산출물인 AI_CODEBASE_MAP.md 하나만 보고도, AI 에이전트가 어떤 작업 요청이든
"어느 파일의 몇 번째~몇 번째 줄을 확인해야 하는지"를 정확히 판단할 수 있도록
정적 분석 정보의 밀도와 정확성을 높인다. AI(LLM) 호출 없이 순수 정적 분석만으로 처리한다.
토큰 효율을 고려해 저밀도 정보(원문 그대로 슬라이스)는 줄이고, 고밀도 정보(시그니처/관계/의도)를 늘린다.

다음 항목을 전부 수정할 것. 항목별로 왜 문제인지 확인 후 진행:

---

[버그 수정 - 최우선]

1. imports 정보 유실 버그
   - create_ai_map.py의 build_rich_symbols_summary()에서
     file_meta.get("imports", []) 를 호출하지만, 각 파서(js_parser.py, py_parser.py,
     java_parser.py, tree_sitter_parser.py)의 file_context에는 "imports" 키가 저장된 적이 없다
     (hash, symbols_summary, skeleton만 저장됨). 결과적으로 imports는 항상 빈 리스트로
     처리되어 최종 맵에 의존성 정보가 전혀 표시되지 않는다.
   - 각 파서가 file_context[rel_path_str]에 "imports": [...] 키를 실제 리스트 형태로
     별도 저장하도록 수정하고, create_ai_map.py가 이를 정상적으로 읽어 맵에 반영하도록 수정.

2. used_by(역참조) 미계산 문제
   - 모든 파서가 심볼 생성 시 "used_by": [] 로 고정 초기화만 하고, indexer.py 어디에도
     전체 심볼 수집 후 calls를 역으로 매핑하는 2차 패스가 없다.
   - indexer.py의 save_index_data() 호출 직전(scan_project 완료 후)에
     전체 self.symbols를 순회하며, 각 심볼의 calls 리스트에 있는 함수명을 찾아
     해당 대상 심볼의 used_by 리스트에 현재 심볼의 symbol_id를 추가하는
     역인덱스 계산 메서드(예: _build_reverse_call_index)를 추가하고 scan_project 안에서 호출.

3. 심볼 10개 절단 문제
   - create_ai_map.py의 build_rich_symbols_summary()에서
     matched_symbols[:10] 으로 파일당 심볼을 10개까지만 잘라서 보여주고 있으며,
     11개 이상인 경우 나머지가 아무 표시 없이 사라진다.
   - 절단 로직을 제거하고 전체 심볼을 표시하되, 파일이 지나치게 큰 경우(예: 30개 초과)에는
     생략하지 말고 "... (+N more)" 형태로 잘린 사실 자체를 명시. 침묵 손실이 없게 할 것.

---

[정보 추가 - 필수]

4. 함수 시그니처(파라미터명+타입) 추출
   - py_parser.py: ast.FunctionDef/AsyncFunctionDef의 args를 순회하여
     파라미터명과 타입 힌트(annotation)를 "name: type" 형식으로 추출, 심볼 정보에 포함.
   - js_parser.py: 정규식 기반으로 함수 선언부 괄호 안 파라미터 목록을 추출(TS 타입 있으면 포함).
   - tree_sitter_parser.py: function/method 노드의 parameters 필드를 순회하여 추출.
   - java_parser.py: 이미 타입은 추출 중이니 파라미터 "이름"도 함께 추출하도록 보완
     (현재는 타입명만 남기고 변수명을 버림).
   - 심볼 dict에 "signature" 필드로 저장하고, 최종 맵 출력(build_rich_symbols_summary)에
     함수명 옆에 시그니처를 표시.

5. docstring/주석 요약 1줄 추출
   - py_parser.py: ast.get_docstring(node)의 첫 줄(또는 최대 80자)을 추출.
   - js_parser.py, tree_sitter_parser.py: 함수/클래스 선언 바로 위 /** */ 또는 // 주석의
     첫 줄을 추출.
   - java_parser.py: Javadoc(/** */) 첫 줄 추출.
   - 심볼 dict에 "summary" 필드로 저장, 없으면 빈 문자열. 최종 맵에 함수 옆 짧게 표시
     (예: "🎯 def foo(x: int) — 사용자 인증 토큰을 검증한다 [L10-L25]").
   - 토큰 절약을 위해 반드시 1줄, 최대 80~100자로 강제 절단.

6. definition_map 이름 충돌 시 덮어쓰기 방지
   - 현재 indexer.py의 self.definition_map.update(f_def_map) 방식은 동일 이름(예: init,
     handler)이 여러 파일에 있을 경우 마지막 파일이 이전 정보를 덮어써 유실시킨다.
   - definition_map의 값을 단일 문자열이 아니라 리스트(List[str])로 변경하여
     동일 이름이 여러 위치에 정의된 경우 전부 보존하도록 수정.
   - 이 변경에 맞춰 definition_map을 사용하는 모든 파서 및 create_ai_map.py 쪽 로직도
     리스트 구조에 맞게 업데이트.

7. skeleton 필드 최적화
   - tree_sitter_parser.py의 skeleton은 현재 content[:400]으로 파일 앞부분을 단순 슬라이스
     하는데, 최종 맵에는 사용되지도 않고 토큰만 낭비한다. 이 필드를 제거하거나,
     "심볼별 시그니처+summary 1줄" 조합으로 대체.
   - py_parser.py의 skeleton은 top-level 함수/클래스 전체 소스를 통째로 넣어 파일이 크면
     토큰이 급증한다. 이것도 "시그니처+summary" 압축 형태로 대체하는 방향을 검토하고 적용.

---

[정보 추가 - 권장]

8. tree_sitter_parser.py의 calls 미추출 문제
   - 현재 tree-sitter 경로(js/ts/tsx/go/rust/c/cpp/java 중 tree_sitter가 처리하는 언어)는
     calls를 전혀 추출하지 않아 항상 빈 배열이다.
   - call_expression 노드를 순회하여 호출되는 함수명을 잡아 심볼의 calls 리스트에 채우는
     로직을 traverse() 안에 추가.

9. tree_sitter_parser.py의 메서드-클래스 소속 표기 통일
   - py_parser.py, java_parser.py는 메서드를 "ClassName.method" 형태의 full_name으로
     기록하는데, tree_sitter_parser.py는 메서드도 독립 함수처럼 처리하여 소속 클래스 정보가
     없다. 부모 노드를 거슬러 올라가 클래스 소속이면 full_name을 "ClassName.method"로
     통일할 것.

10. 파일 총 라인 수 표기
    - 각 파서의 file_context에 "total_lines": len(lines) 필드를 추가하고
      최종 맵 출력 시 파일명 옆에 라인 수를 표시. (파일 크기 파악용, 계산 비용 거의 없음)

---

[검증]

수정 완료 후 다음을 검증할 것:
- 기존 5대 장부(symbols, files_context, definition_map, data_protocols, registry_constants)
  구조와 반환 튜플 순서(symbols, file_context, definition_map, data_protocols,
  registry_constants)는 절대 깨뜨리지 말 것 — indexer.py의 index_file()이 이 순서를
  그대로 언패킹하고 있음.
- 수정 후 실제로 파이썬/JS/자바 샘플 파일 각 1개씩 만들어 indexer.py → create_ai_map.py
  순서로 실행해보고, AI_CODEBASE_MAP.md에 imports, signature, summary, used_by,
  전체 심볼(10개 초과 포함)이 실제로 반영되는지 확인.
- 기존 DEBUG_LOG / DEBUG 플래그와 로그 포맷(이모지 포함 한국어 로그 스타일)은 유지.
- 각 파서 파일은 여전히 독립적으로 동작해야 하며(다른 파서에 의존하지 않음),
  extract_symbols(file_path, project_root) 시그니처는 변경하지 말 것.

수정이 끝나면 변경된 부분을 파일별로 diff 요약으로 정리해서 보여줄 것.