# config.py
"""
A file that manages the main settings of the application.
Defines the path, network information, model parameters, etc. required to run the server.
"""
from pathlib import Path

#.py 
BASE_DIR = Path(__file__).resolve().parent

# Fixed config
FIXED_CONFIG = {
    "BIN": BASE_DIR / "LLMServer" / "llama_cpp" / "llama-server.exe",
    "HOST": "127.0.0.1",
}

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
    # "MODEL": BASE_DIR/ "LLMServer" / "models" / "Qwen3-14B-Q4_K_M.gguf",
    "MODEL": BASE_DIR/ "LLMServer" / "models" / "Qwen3-0.6B-Q8_0.gguf",

    # network config
    "HOST": "127.0.0.1",
    "PORT": 8129,

    # model performance and parameter
    "CTX_SIZE": 8192,        # Total tokens
    "NGL": -1,               # GPU layers(-1 means put everything on gpu)
    "ALIAS": "Qwen3-14B",    # Alias to use to identify models in the API

    # server options
    "VERBOSE": True,         # Will it print detailed logs?
    "BATCH_SIZE": 1024,      # Batch size for prompt
    "FLASH_ATTN": True,      # Use Flash Attention or not
}




