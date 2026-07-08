# ==========================================================================# 🎯 AI 전역 가이드라인: 무결성과 확장성의 황금 밸런스 규칙# 소스를 분석, 리팩토링 및 수정 요청할 때 아래 최적화 규칙을 무조건 엄격히 준수하십시오.## 1. 구조 유지: 프로젝트 내 기존 클래스/함수명 명세 및 self.vars 데이터 프로토콜은 엄격히 준수하십시오.# 2. 환각 방지: 존재하지 않는 가짜 함수 창조 절대 금지! 절대값 연산은 순정 내장 함수 abs()를 쓰십시오.# 3. 개발 자유: 위 최소 조건 내에서 알고리즘, 물리 수식, 이동 로직은 자유롭고 창의적으로 짜십시오.# ==========================================================================# 📄 [요청 1] TARGET: tools/python_agent_tools/agent_navigator.py (35-55라인)# ----------------------------------------------------------```python        3. .jjap_symbols.json 장부와 대조 시, 'tools/' 경로 프리픽스 불일치 및 used_by 내부의 
           'AdvancedIndexerV2.scan_project' vs 'scan_project' 같은 클래스명 유무 오차를 유연하게 필터링하여 2차 기습 징집합니다.
        """
        
        print("\n" + "="*60)
        print("🚨 [DEBUGGER ON] 내비게이터 멀티 슬라이싱 파이프라인 기동!!!")
        print(f"📥 유저 입력 프롬프트: {repr(raw_prompt)}")
        print("="*60)

        pattern = r"([a-zA-Z0-9_\-\./]+)\s*:\s*(\d+)(?:\s*-\s*(\d+))?"
        matches = re.findall(pattern, raw_prompt)

        print(f"🔍 정규식 1차 타겟 스캔 결과: {matches}")
        if not matches:
            print("⚠️ [DEBUG] 매칭되는 파일 경로 및 라인 규격이 없습니다. 빈 배열 리턴.")
            return []

        extracted_slices = []
        req_num = 1

        for match in matches:```# 📄 [요청 2] TARGET: tools/python_agent_tools/agent_navigator.py (328-328라인)# ----------------------------------------------------------```python    root_window.mainloop()```