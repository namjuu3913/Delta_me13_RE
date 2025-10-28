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
    
    # This code will be started after server ends
    subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(state.llm_controller.pid)],
                check=True
            )
    
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