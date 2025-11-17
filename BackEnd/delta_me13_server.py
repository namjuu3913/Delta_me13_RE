import sys, os

PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from PythonServer.Global import state
from PythonServer.pyServerRouters import http_router
import subprocess, signal, asyncio
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When server starts this code will started first
    state.character_handler = state.CharacterHandler()
    
    yield # From here, FastAPI's application starts
    
    if state.character is not None: 
        print("--- Lifespan: Character found. Saving logs in thread... ---")
        try:
            await asyncio.to_thread(state.character.turn_off_character)
            print("--- Lifespan: Log saving finished. ---")
        except Exception as e:
            print(f"--- Lifespan: Error during log saving: {e} ---")
    else:
        print("--- Lifespan: No character loaded. Skipping log save. ---")

    pid_to_kill = None
    if state.llm_controller is not None:
        try:
            pid_to_kill = state.llm_controller.pid
            print(f"--- Lifespan: LLM controller found (PID: {pid_to_kill}). ---")
        except AttributeError:
            print("--- Lifespan: LLM controller found but has no PID. Skipping kill. ---")
    
    if pid_to_kill:
        try:
            print(f"--- Lifespan: Killing PID {pid_to_kill} in thread... ---")
            if sys.platform == "win32":
                await asyncio.to_thread(
                    subprocess.run,
                    ["taskkill", "/F", "/T", "/PID", str(pid_to_kill)],
                    check=True, capture_output=True, text=True
                )
            else:
                await asyncio.to_thread(os.kill, pid_to_kill, signal.SIGKILL)
            print("--- Lifespan: Kill signal sent. ---")
        except Exception as e:
            print(f"--- Lifespan: Error while trying to kill process {pid_to_kill}: {e} ---")
    else:
        print("--- Lifespan: No LLM controller PID found. Skipping kill. ---")

    print("--- Lifespan: Shutdown complete. ---")

    
    
# FastAPI instance
app = FastAPI(lifespan = lifespan)

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