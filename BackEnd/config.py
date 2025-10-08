# config.py
"""
A file that manages the main settings of the application.
Defines the path, network information, model parameters, etc. required to run the server.
"""

import sys
from pathlib import Path

# BASE location
if getattr(sys, 'frozen', False):
    #.exe 
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    #.py 
    BASE_DIR = Path(__file__).resolve().parent

# python server
PYTHON_SERVER_CONFIG = {
    # name
    "NAME" : "δ_me13",
    # version
    "VERSION" : "prototype"
    }

# Llama.cpp server
LLM_SERVER_CONFIG = {
    # model and llama.cpp location
    "BIN": BASE_DIR / "LLMServer" / "llama_cpp" / "llama-server.exe",
    "MODEL": BASE_DIR/ "LLMServer" / "models" / "Qwen3-14B-Q4_K_M.gguf",

    # network config
    "HOST": "127.0.0.1",
    "PORT": 8002,

    # model performance and parameter
    "CTX_SIZE": 8192,        # Total tokens
    "NGL": -1,               # GPU layers(-1 means put everything on gpu)
    "ALIAS": "gpt-oss-20b",  # Alias to use to identify models in the API

    # server options
    "VERBOSE": True,         # Will it print detailed logs?
    "BATCH_SIZE": 1024,      # Batch size for prompt
    "FLASH_ATTN": True,      # Use Flash Attention or not
    }




