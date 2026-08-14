import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from agent_core.debug_agent import DebugVerifier

verifier = DebugVerifier(ROOT_DIR)
target_file = "scratch/test_debug_agent.py"

# 1. Stdio 채널 테스트 (sys.executable 활용)
mission_stdio = {
    "entrypoint": f"{sys.executable} -c \"print('[DEBUG] Stdio test passed')\"",
    "expected_terminal_outputs": ["\\[DEBUG\\] Stdio test passed"]
}
res_stdio = verifier.verify(mission_stdio, target_file)
print("=== Stdio Test Result ===")
print("Verified:", res_stdio["verified"])
print("Matched:", res_stdio["matched_patterns"])
print("Message:", res_stdio["message"])

# 2. File 채널 테스트
test_log_file = ROOT_DIR / "agent_debug.log"
with open(test_log_file, "w", encoding="utf-8") as f:
    f.write("[LOG_FILE] Debug log saved successfully\n")

mission_file = {
    "debug_log_spec": {
        "channel_type": "file",
        "log_file_path": "agent_debug.log",
        "expected_patterns": ["\\[LOG_FILE\\] Debug log saved"]
    }
}
res_file = verifier.verify(mission_file, target_file)
print("\n=== File Test Result ===")
print("Verified:", res_file["verified"])
print("Matched:", res_file["matched_patterns"])
print("Message:", res_file["message"])
