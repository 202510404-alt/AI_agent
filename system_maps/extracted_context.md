# ==========================================================================# 🎯 AI 전역 가이드라인: 무결성과 확장성의 황금 밸런스 규칙# 소스를 분석, 리팩토링 및 수정 요청할 때 아래 최적화 규칙을 무조건 엄격히 준수하십시오.## 1. 구조 유지: 프로젝트 내 기존 클래스/함수명 명세 및 self.vars 데이터 프로토콜은 엄격히 준수하십시오.# 2. 환각 방지: 존재하지 않는 가짜 함수 창조 절대 금지! 절대값 연산은 순정 내장 함수 abs()를 쓰십시오.# 3. 개발 자유: 위 최소 조건 내에서 알고리즘, 물리 수식, 이동 로직은 자유롭고 창의적으로 짜십시오.# ==========================================================================# 📄 [요청 1] TARGET: tools/python_agent_tools/indexer.py (100-150라인)# ----------------------------------------------------------```python    def index_file(self, file_path: Path):
        # 마스터 루트 기준의 올바른 상대 경로 추출
        rel_path_str = file_path.relative_to(self.project_root).as_posix()
        
        try:
            mtime = int(file_path.stat().st_mtime)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_hash = self._get_sha256(content)

            # 💡 [형님 맞춤형 분기] 파이썬 파일일 때만 내부 클래스/함수 정밀 분석
            # 💡 [형님 맞춤형 분기] 파이썬 파일일 때만 내부 클래스/함수 정밀 분석
            if file_path.suffix == ".py":
                skeleton = self._extract_skeleton(content)
                self.parse_protocols_and_registries(content, rel_path_str)
                
                # 심볼 맵 구성 로직 및 양방향 추적용 symbols 장부 적재
                # 💡 tools/python_agent_tools/indexer.py 내부의 ast.parse 순회 구역 교정
                try:
                    tree = ast.parse(content)
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                            
                            # ➡️ [중요] "type": "class" 규격을 칼같이 주입합니다.
                            self.symbols.append({
                                "name": node.name,
                                "type": "class", # 👈 🚨 여기에 타잎을 명시해야 워처가 안 죽습니다!
                                "file": rel_path_str,
                                "start_line": node.lineno,
                                "end_line": getattr(node, "end_lineno", node.lineno),
                                "used_by": []
                            })
                            
                            for sub in node.body:
                                if isinstance(sub, ast.FunctionDef):
                                    self.definition_map[f"{node.name}.{sub.name}"] = f"{rel_path_str}:{sub.lineno}"
                                    
                                    # ➡️ [중요] 클래스 내부 메서드도 함수 규격 주입
                                    self.symbols.append({
                                        "name": sub.name,
                                        "type": "function", # 👈 🚨 타잎 주입!
                                        "file": rel_path_str,
                                        "start_line": sub.lineno,
                                        "end_line": getattr(sub, "end_lineno", sub.lineno),
                                        "used_by": []
                                    })
                                    
                        elif isinstance(node, ast.FunctionDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"```# 📄 [요청 1 ➡️ 불러온함수 (parse_protocols_and_registries 본체)] TARGET: python_agent_tools/indexer.py (65-98라인)# ----------------------------------------------------------```python    def parse_protocols_and_registries(self, content: str, rel_path_str: str):
        """[범용성 자동 지능 엔진] 하드코딩 없이 클래스의 성격을 파악하여 장부에 자동 분배"""
        try:
            tree = ast.parse(content)
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue

                # 🛡️ 1. 데이터 프로토콜 스캔: 이름에 Variables 또는 vars가 들어가면 데이터 명세서로 징집
                if "Variables" in node.name or "vars" in node.name.lower():
                    fields = {}
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef) and sub_node.name == "__init__":
                            for stmt in sub_node.body:
                                if isinstance(stmt, ast.Assign):
                                    for target in stmt.targets:
                                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                                            val_str = "Unknown"
                                            if isinstance(stmt.value, ast.Constant):
                                                val_str = f"{type(stmt.value.value).__name__} (기본값: {stmt.value.value})"
                                            fields[target.attr] = val_str
                    
                    self.data_protocols[node.name] = {
                        "defined_in": rel_path_str,
                        "fields": fields
                    }
                
                # 🧱 2. 범용 레지스트리 상수 스캔: 폴더 불문! 모든 핵심 구동 클래스(플랫폼, 플레이어, 적 등)를 상수로 맵핑
                else:
                    if node.name not in ["AppState"]:
                        self.registry_constants[node.name] = f"{rel_path_str}::{node.name}"
                        
        except Exception:
            pass```# 📄 [요청 1 ➡️ 불러온함수 (_get_sha256 본체)] TARGET: python_agent_tools/indexer.py (44-45라인)# ----------------------------------------------------------```python    def _get_sha256(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()```# 📄 [요청 1 ➡️ 불러온함수 (_extract_skeleton 본체)] TARGET: python_agent_tools/indexer.py (47-63라인)# ----------------------------------------------------------```python    def _extract_skeleton(self, content: str) -> str:
        try:
            tree = ast.parse(content)
            skeleton_lines = []
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    skeleton_lines.append(f"class {node.name}:")
                    for sub_node in node.body:
                        if isinstance(sub_node, ast.FunctionDef):
                            skeleton_lines.append(f"    def {sub_node.name}(...):")
                            skeleton_lines.append(f"        ...")
                elif isinstance(node, ast.FunctionDef):
                    skeleton_lines.append(f"def {node.name}(...):")
                    skeleton_lines.append(f"    ...")
            return "\n".join(skeleton_lines)
        except Exception:
            return ""```# 📄 [요청 1 ➡️ 불러온함수 (index_file 본체)] TARGET: python_agent_tools/indexer.py (100-173라인)# ----------------------------------------------------------```python    def index_file(self, file_path: Path):
        # 마스터 루트 기준의 올바른 상대 경로 추출
        rel_path_str = file_path.relative_to(self.project_root).as_posix()
        
        try:
            mtime = int(file_path.stat().st_mtime)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            file_hash = self._get_sha256(content)

            # 💡 [형님 맞춤형 분기] 파이썬 파일일 때만 내부 클래스/함수 정밀 분석
            # 💡 [형님 맞춤형 분기] 파이썬 파일일 때만 내부 클래스/함수 정밀 분석
            if file_path.suffix == ".py":
                skeleton = self._extract_skeleton(content)
                self.parse_protocols_and_registries(content, rel_path_str)
                
                # 심볼 맵 구성 로직 및 양방향 추적용 symbols 장부 적재
                # 💡 tools/python_agent_tools/indexer.py 내부의 ast.parse 순회 구역 교정
                try:
                    tree = ast.parse(content)
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                            
                            # ➡️ [중요] "type": "class" 규격을 칼같이 주입합니다.
                            self.symbols.append({
                                "name": node.name,
                                "type": "class", # 👈 🚨 여기에 타잎을 명시해야 워처가 안 죽습니다!
                                "file": rel_path_str,
                                "start_line": node.lineno,
                                "end_line": getattr(node, "end_lineno", node.lineno),
                                "used_by": []
                            })
                            
                            for sub in node.body:
                                if isinstance(sub, ast.FunctionDef):
                                    self.definition_map[f"{node.name}.{sub.name}"] = f"{rel_path_str}:{sub.lineno}"
                                    
                                    # ➡️ [중요] 클래스 내부 메서드도 함수 규격 주입
                                    self.symbols.append({
                                        "name": sub.name,
                                        "type": "function", # 👈 🚨 타잎 주입!
                                        "file": rel_path_str,
                                        "start_line": sub.lineno,
                                        "end_line": getattr(sub, "end_lineno", sub.lineno),
                                        "used_by": []
                                    })
                                    
                        elif isinstance(node, ast.FunctionDef):
                            self.definition_map[node.name] = f"{rel_path_str}:{node.lineno}"
                            
                            # ➡️ [중요] 일반 전역 함수 규격 주입
                            self.symbols.append({
                                "name": node.name,
                                "type": "function", # 👈 🚨 타잎 주입!
                                "file": rel_path_str,
                                "start_line": node.lineno,
                                "end_line": getattr(node, "end_lineno", node.lineno),
                                "used_by": []
                            })
                except Exception:
                    pass
            else:
                # 💡 [형님 맞춤형 분기] 비-파이썬 파일은 문법 에러를 내지 않고 안전하게 경로와 기본 정보만 보존!
                skeleton = f"Non-Python File ({file_path.suffix.upper()})"

            # 장부에 안전하게 세이브
            self.files_context[rel_path_str] = {
                "hash": file_hash,
                "mtime": mtime,
                "skeleton": skeleton
            }
        except Exception as e:
            print(f"⚠️ [파일 수집 예외 패스] {rel_path_str}: {str(e)}")```