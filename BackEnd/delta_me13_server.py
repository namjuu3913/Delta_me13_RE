from fastapi import FastAPI
from contextlib import asynccontextmanager
from PythonServer.Global import state
from PythonServer.pyServerRouters import http_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When server starts this code will started first
    
    state.character_handler = state.CharacterHandler()
    yield # From here, FastAPI's application starts
    
    # This code will be started after server ends
    
# FastAPI instance
app = FastAPI(lifespan=lifespan)

# http router
app.include_router(http_router.router)

# websocket goes here