import sys, os

PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from PythonServer.Global import state
from PythonServer.pyServerRouters import http_router
import subprocess
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When server starts this code will started first
    state.character_handler = state.CharacterHandler()
    
    yield # From here, FastAPI's application starts
    
    print(f"Shutting down LLM controller (PID: {state.llm_controller.pid})...")
    
    pid_to_kill = state.llm_controller.pid

    # save log
    if state.Character != None:
        state.Character.turn_off_character()

    try:
        if sys.platform == "win32":
            # Windows: taskkill 
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid_to_kill)],
                check=True,
                capture_output=True, # prevent log to mess up terminal
                text=True
            )
            print(f"Successfully sent taskkill to PID {pid_to_kill}")
            
        else:
            # Linux / macOS: os.kill 
            # signal.SIGKILL == taskkill
            os.kill(pid_to_kill, signal.SIGKILL)
            print(f"Successfully sent SIGKILL to PID {pid_to_kill}")

    except Exception as e:
        print(f"Error while trying to kill process {pid_to_kill}: {e}")
    
# FastAPI instance
app = FastAPI(lifespan=lifespan)

allows = [
    "http://localhost:5173",
    "http://localhost:5173/",
    "http://localhost:5173/chatNow",
    "http://localhost:5173/charDesignEvery",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allows,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http router
app.include_router(http_router.router)

# websocket goes here