import sys
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent / "BackEnd" / ""
    else:
        return Path(__file__).resolve().parent
    
    