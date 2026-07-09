{
  "symbols": [
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::SemanticNavigator",
      "full_name": "SemanticNavigator",
      "name": "SemanticNavigator",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 11,
      "end_line": 208,
      "range": [
        11,
        208
      ],
      "signature": "class SemanticNavigator:",
      "calls": [],
      "used_by": [
        "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.__init__"
      ]
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::SemanticNavigator.__init__",
      "full_name": "SemanticNavigator.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "SemanticNavigator",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 12,
      "end_line": 16,
      "range": [
        12,
        16
      ],
      "signature": "def __init__(...)",
      "calls": [
        "_load_database"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::SemanticNavigator._load_database",
      "full_name": "SemanticNavigator._load_database",
      "name": "_load_database",
      "type": "method",
      "parent": "SemanticNavigator",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 18,
      "end_line": 25,
      "range": [
        18,
        25
      ],
      "signature": "def _load_database(...)",
      "calls": [
        "open",
        "load",
        "exists"
      ],
      "used_by": [
        "python_agent_tools/agent_navigator.py::SemanticNavigator.__init__"
      ]
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::SemanticNavigator.extract_multi_slices",
      "full_name": "SemanticNavigator.extract_multi_slices",
      "name": "extract_multi_slices",
      "type": "method",
      "parent": "SemanticNavigator",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 30,
      "end_line": 208,
      "range": [
        30,
        208
      ],
      "signature": "def extract_multi_slices(...)",
      "calls": [
        "print",
        "any",
        "min",
        "readlines",
        "join",
        "print_exc",
        "int",
        "get",
        "len",
        "repr",
        "set",
        "exists",
        "endswith",
        "replace",
        "strip",
        "max",
        "findall",
        "split",
        "open",
        "list",
        "append"
      ],
      "used_by": [
        "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.execute_slicing_pipeline"
      ]
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI",
      "full_name": "JjapCursorNavigatorGUI",
      "name": "JjapCursorNavigatorGUI",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 213,
      "end_line": 339,
      "range": [
        213,
        339
      ],
      "signature": "class JjapCursorNavigatorGUI:",
      "calls": [],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.__init__",
      "full_name": "JjapCursorNavigatorGUI.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "JjapCursorNavigatorGUI",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 214,
      "end_line": 263,
      "range": [
        214,
        263
      ],
      "signature": "def __init__(...)",
      "calls": [
        "SemanticNavigator",
        "geometry",
        "Label",
        "Text",
        "Button",
        "Frame",
        "insert",
        "pack",
        "title"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.execute_slicing_pipeline",
      "full_name": "JjapCursorNavigatorGUI.execute_slicing_pipeline",
      "name": "execute_slicing_pipeline",
      "type": "method",
      "parent": "JjapCursorNavigatorGUI",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 265,
      "end_line": 320,
      "range": [
        265,
        320
      ],
      "signature": "def execute_slicing_pipeline(...)",
      "calls": [
        "get",
        "extract_multi_slices",
        "insert",
        "open",
        "write",
        "join",
        "showerror",
        "startswith",
        "showwarning",
        "strip",
        "config",
        "append",
        "rstrip",
        "delete"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/agent_navigator.py::JjapCursorNavigatorGUI.manual_export_file",
      "full_name": "JjapCursorNavigatorGUI.manual_export_file",
      "name": "manual_export_file",
      "type": "method",
      "parent": "JjapCursorNavigatorGUI",
      "file": "python_agent_tools/agent_navigator.py",
      "start_line": 322,
      "end_line": 339,
      "range": [
        322,
        339
      ],
      "signature": "def manual_export_file(...)",
      "calls": [
        "write",
        "open",
        "showinfo",
        "asksaveasfilename",
        "showerror",
        "str"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/context_builder.py::ContextBuilder",
      "full_name": "ContextBuilder",
      "name": "ContextBuilder",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/context_builder.py",
      "start_line": 13,
      "end_line": 107,
      "range": [
        13,
        107
      ],
      "signature": "class ContextBuilder:",
      "calls": [],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/context_builder.py::ContextBuilder.__init__",
      "full_name": "ContextBuilder.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "ContextBuilder",
      "file": "python_agent_tools/context_builder.py",
      "start_line": 16,
      "end_line": 18,
      "range": [
        16,
        18
      ],
      "signature": "def __init__(...)",
      "calls": [
        "Path"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/context_builder.py::ContextBuilder.read_and_clean_file",
      "full_name": "ContextBuilder.read_and_clean_file",
      "name": "read_and_clean_file",
      "type": "method",
      "parent": "ContextBuilder",
      "file": "python_agent_tools/context_builder.py",
      "start_line": 20,
      "end_line": 78,
      "range": [
        20,
        78
      ],
      "signature": "def read_and_clean_file(...)",
      "calls": [
        "FileNotFoundError",
        "split",
        "exists",
        "open",
        "readlines",
        "join",
        "endswith",
        "startswith",
        "enumerate",
        "strip",
        "append",
        "len"
      ],
      "used_by": [
        "python_agent_tools/context_builder.py::ContextBuilder.assemble_ai_prompt"
      ]
    },
    {
      "symbol_id": "python_agent_tools/context_builder.py::ContextBuilder.assemble_ai_prompt",
      "full_name": "ContextBuilder.assemble_ai_prompt",
      "name": "assemble_ai_prompt",
      "type": "method",
      "parent": "ContextBuilder",
      "file": "python_agent_tools/context_builder.py",
      "start_line": 80,
      "end_line": 107,
      "range": [
        80,
        107
      ],
      "signature": "def assemble_ai_prompt(...)",
      "calls": [
        "read_and_clean_file",
        "append",
        "str",
        "join"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::parse_python_file",
      "full_name": "parse_python_file",
      "name": "parse_python_file",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 41,
      "end_line": 102,
      "range": [
        41,
        102
      ],
      "signature": "def parse_python_file(...)",
      "calls": [
        "getattr",
        "parse",
        "set",
        "open",
        "extend",
        "remove",
        "list",
        "join",
        "isinstance",
        "read",
        "append",
        "sorted"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::collect_target_files",
      "full_name": "collect_target_files",
      "name": "collect_target_files",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 105,
      "end_line": 134,
      "range": [
        105,
        134
      ],
      "signature": "def collect_target_files(...)",
      "calls": [
        "print",
        "any",
        "exists",
        "replace",
        "walk",
        "append",
        "sorted",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::load_registry",
      "full_name": "load_registry",
      "name": "load_registry",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 137,
      "end_line": 151,
      "range": [
        137,
        151
      ],
      "signature": "def load_registry(...)",
      "calls": [
        "print",
        "get",
        "items",
        "rpartition",
        "exists",
        "open",
        "setdefault",
        "as_posix",
        "append",
        "load",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::load_protocols",
      "full_name": "load_protocols",
      "name": "load_protocols",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 154,
      "end_line": 169,
      "range": [
        154,
        169
      ],
      "signature": "def load_protocols(...)",
      "calls": [
        "print",
        "get",
        "items",
        "exists",
        "open",
        "setdefault",
        "as_posix",
        "append",
        "load",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::main",
      "full_name": "main",
      "name": "main",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 172,
      "end_line": 245,
      "range": [
        172,
        245
      ],
      "signature": "def main(...)",
      "calls": [
        "print",
        "join",
        "unlink",
        "parse_python_file",
        "items",
        "write",
        "range",
        "relative_to",
        "mkdir",
        "len",
        "load_registry",
        "set",
        "exists",
        "load_protocols",
        "endswith",
        "replace",
        "as_posix",
        "open",
        "add",
        "collect_target_files",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::generate_ai_optimized_map"
      ]
    },
    {
      "symbol_id": "python_agent_tools/create_ai_map.py::generate_ai_optimized_map",
      "full_name": "generate_ai_optimized_map",
      "name": "generate_ai_optimized_map",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/create_ai_map.py",
      "start_line": 252,
      "end_line": 254,
      "range": [
        252,
        254
      ],
      "signature": "def generate_ai_optimized_map(...)",
      "calls": [
        "main"
      ],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::run_pipeline"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2",
      "full_name": "AdvancedIndexerV2",
      "name": "AdvancedIndexerV2",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/indexer.py",
      "start_line": 25,
      "end_line": 295,
      "range": [
        25,
        295
      ],
      "signature": "class AdvancedIndexerV2:",
      "calls": [],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::run_pipeline"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2.__init__",
      "full_name": "AdvancedIndexerV2.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 34,
      "end_line": 42,
      "range": [
        34,
        42
      ],
      "signature": "def __init__(...)",
      "calls": [],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2._get_sha256",
      "full_name": "AdvancedIndexerV2._get_sha256",
      "name": "_get_sha256",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 44,
      "end_line": 45,
      "range": [
        44,
        45
      ],
      "signature": "def _get_sha256(...)",
      "calls": [
        "sha256",
        "encode",
        "hexdigest"
      ],
      "used_by": [
        "python_agent_tools/indexer.py::AdvancedIndexerV2.index_file"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2._extract_skeleton",
      "full_name": "AdvancedIndexerV2._extract_skeleton",
      "name": "_extract_skeleton",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 47,
      "end_line": 63,
      "range": [
        47,
        63
      ],
      "signature": "def _extract_skeleton(...)",
      "calls": [
        "parse",
        "isinstance",
        "append",
        "join"
      ],
      "used_by": [
        "python_agent_tools/indexer.py::AdvancedIndexerV2.index_file"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2.parse_protocols_and_registries",
      "full_name": "AdvancedIndexerV2.parse_protocols_and_registries",
      "name": "parse_protocols_and_registries",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 65,
      "end_line": 98,
      "range": [
        65,
        98
      ],
      "signature": "def parse_protocols_and_registries(...)",
      "calls": [
        "parse",
        "isinstance",
        "lower",
        "type"
      ],
      "used_by": [
        "python_agent_tools/indexer.py::AdvancedIndexerV2.index_file"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2.index_file",
      "full_name": "AdvancedIndexerV2.index_file",
      "name": "index_file",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 100,
      "end_line": 214,
      "range": [
        100,
        214
      ],
      "signature": "def index_file(...)",
      "calls": [
        "print",
        "_get_sha256",
        "int",
        "parse_protocols_and_registries",
        "stat",
        "isinstance",
        "relative_to",
        "str",
        "parse",
        "set",
        "read",
        "as_posix",
        "getattr",
        "upper",
        "open",
        "list",
        "_extract_skeleton",
        "walk",
        "append"
      ],
      "used_by": [
        "python_agent_tools/indexer.py::AdvancedIndexerV2.scan_project"
      ]
    },
    {
      "symbol_id": "python_agent_tools/indexer.py::AdvancedIndexerV2.scan_project",
      "full_name": "AdvancedIndexerV2.scan_project",
      "name": "scan_project",
      "type": "method",
      "parent": "AdvancedIndexerV2",
      "file": "python_agent_tools/indexer.py",
      "start_line": 216,
      "end_line": 295,
      "range": [
        216,
        295
      ],
      "signature": "def scan_project(...)",
      "calls": [
        "makedirs",
        "print",
        "get",
        "any",
        "set",
        "exists",
        "open",
        "dump",
        "list",
        "replace",
        "as_posix",
        "walk",
        "append",
        "sorted",
        "index_file",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::run_pipeline"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_lookup.py::load_json",
      "full_name": "load_json",
      "name": "load_json",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_lookup.py",
      "start_line": 9,
      "end_line": 14,
      "range": [
        9,
        14
      ],
      "signature": "def load_json(...)",
      "calls": [
        "print",
        "exists",
        "open",
        "load",
        "exit"
      ],
      "used_by": [
        "python_agent_tools/jjap_lookup.py::lookup_symbol",
        "python_agent_tools/jjap_lookup.py::show_skeleton"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_lookup.py::lookup_symbol",
      "full_name": "lookup_symbol",
      "name": "lookup_symbol",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_lookup.py",
      "start_line": 16,
      "end_line": 43,
      "range": [
        16,
        43
      ],
      "signature": "def lookup_symbol(...)",
      "calls": [
        "get",
        "print",
        "upper",
        "load_json",
        "lower",
        "len"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/jjap_lookup.py::show_skeleton",
      "full_name": "show_skeleton",
      "name": "show_skeleton",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_lookup.py",
      "start_line": 45,
      "end_line": 61,
      "range": [
        45,
        61
      ],
      "signature": "def show_skeleton(...)",
      "calls": [
        "keys",
        "get",
        "print",
        "load_json"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever",
      "full_name": "JjapRetriever",
      "name": "JjapRetriever",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 9,
      "end_line": 129,
      "range": [
        9,
        129
      ],
      "signature": "class JjapRetriever:",
      "calls": [],
      "used_by": [
        "python_agent_tools/jjap_retriever.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever.__init__",
      "full_name": "JjapRetriever.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "JjapRetriever",
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 16,
      "end_line": 21,
      "range": [
        16,
        21
      ],
      "signature": "def __init__(...)",
      "calls": [
        "_load_symbols"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever._load_symbols",
      "full_name": "JjapRetriever._load_symbols",
      "name": "_load_symbols",
      "type": "method",
      "parent": "JjapRetriever",
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 23,
      "end_line": 37,
      "range": [
        23,
        37
      ],
      "signature": "def _load_symbols(...)",
      "calls": [
        "print",
        "get",
        "exists",
        "open",
        "load",
        "len"
      ],
      "used_by": [
        "python_agent_tools/jjap_retriever.py::JjapRetriever.__init__"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol",
      "full_name": "JjapRetriever.retrieve_symbol",
      "name": "retrieve_symbol",
      "type": "method",
      "parent": "JjapRetriever",
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 39,
      "end_line": 98,
      "range": [
        39,
        98
      ],
      "signature": "def retrieve_symbol(...)",
      "calls": [
        "get",
        "print",
        "_find_best_match",
        "_safe_truncate",
        "exists",
        "open",
        "rstrip",
        "extend",
        "min",
        "readlines",
        "join",
        "startswith",
        "len",
        "strip",
        "append",
        "max",
        "next"
      ],
      "used_by": [
        "python_agent_tools/jjap_retriever.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever._find_best_match",
      "full_name": "JjapRetriever._find_best_match",
      "name": "_find_best_match",
      "type": "method",
      "parent": "JjapRetriever",
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 100,
      "end_line": 117,
      "range": [
        100,
        117
      ],
      "signature": "def _find_best_match(...)",
      "calls": [
        "get",
        "print",
        "lower"
      ],
      "used_by": [
        "python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::JjapRetriever._safe_truncate",
      "full_name": "JjapRetriever._safe_truncate",
      "name": "_safe_truncate",
      "type": "method",
      "parent": "JjapRetriever",
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 119,
      "end_line": 129,
      "range": [
        119,
        129
      ],
      "signature": "def _safe_truncate(...)",
      "calls": [
        "print",
        "join",
        "splitlines",
        "append",
        "len"
      ],
      "used_by": [
        "python_agent_tools/jjap_retriever.py::JjapRetriever.retrieve_symbol"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_retriever.py::main",
      "full_name": "main",
      "name": "main",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_retriever.py",
      "start_line": 132,
      "end_line": 140,
      "range": [
        132,
        140
      ],
      "signature": "def main(...)",
      "calls": [
        "print",
        "cwd",
        "retrieve_symbol",
        "JjapRetriever",
        "len"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::generate_ai_optimized_map"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::import_file_directly",
      "full_name": "import_file_directly",
      "name": "import_file_directly",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 20,
      "end_line": 28,
      "range": [
        20,
        28
      ],
      "signature": "def import_file_directly(...)",
      "calls": [
        "ImportError",
        "spec_from_file_location",
        "module_from_spec",
        "exec_module",
        "str"
      ],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::run_pipeline"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::run_pipeline",
      "full_name": "run_pipeline",
      "name": "run_pipeline",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 30,
      "end_line": 73,
      "range": [
        30,
        73
      ],
      "signature": "def run_pipeline(...)",
      "calls": [
        "AdvancedIndexerV2",
        "print",
        "get",
        "update_map",
        "scan_project",
        "generate_ai_optimized_map",
        "print_exc",
        "import_file_directly"
      ],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::CodeChangeHandler.dispatch",
        "python_agent_tools/jjap_watcher.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::CodeChangeHandler",
      "full_name": "CodeChangeHandler",
      "name": "CodeChangeHandler",
      "type": "class",
      "parent": null,
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 76,
      "end_line": 99,
      "range": [
        76,
        99
      ],
      "signature": "class CodeChangeHandler:",
      "calls": [],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::main"
      ]
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::CodeChangeHandler.__init__",
      "full_name": "CodeChangeHandler.__init__",
      "name": "__init__",
      "type": "method",
      "parent": "CodeChangeHandler",
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 77,
      "end_line": 79,
      "range": [
        77,
        79
      ],
      "signature": "def __init__(...)",
      "calls": [],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::CodeChangeHandler.dispatch",
      "full_name": "CodeChangeHandler.dispatch",
      "name": "dispatch",
      "type": "method",
      "parent": "CodeChangeHandler",
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 81,
      "end_line": 99,
      "range": [
        81,
        99
      ],
      "signature": "def dispatch(...)",
      "calls": [
        "print",
        "any",
        "run_pipeline",
        "as_posix",
        "time",
        "Path"
      ],
      "used_by": []
    },
    {
      "symbol_id": "python_agent_tools/jjap_watcher.py::main",
      "full_name": "main",
      "name": "main",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/jjap_watcher.py",
      "start_line": 101,
      "end_line": 127,
      "range": [
        101,
        127
      ],
      "signature": "def main(...)",
      "calls": [
        "print",
        "stop",
        "CodeChangeHandler",
        "Observer",
        "join",
        "sleep",
        "run_pipeline",
        "start",
        "schedule",
        "str"
      ],
      "used_by": [
        "python_agent_tools/create_ai_map.py::generate_ai_optimized_map"
      ]
    },
    {
      "symbol_id": "python_agent_tools/update_map.py::update_map",
      "full_name": "update_map",
      "name": "update_map",
      "type": "function",
      "parent": null,
      "file": "python_agent_tools/update_map.py",
      "start_line": 4,
      "end_line": 89,
      "range": [
        4,
        89
      ],
      "signature": "def update_map(...)",
      "calls": [
        "print",
        "get",
        "items",
        "any",
        "exists",
        "upper",
        "open",
        "write",
        "join",
        "keys",
        "len",
        "strip",
        "append",
        "load",
        "sorted",
        "Path"
      ],
      "used_by": [
        "python_agent_tools/jjap_watcher.py::run_pipeline"
      ]
    }
  ]
}