from openai import OpenAI
from typing import Optional
import subprocess
from PythonServer.Character.Character import Character
from PythonServer.connectLLM.requestHandler import requestHandler
from PythonServer.Character.CharacterHandler import CharacterHandler

# Handler
request_handler: Optional[requestHandler] = None
character_handler: Optional[CharacterHandler] = None
# llm_server
llm_server_flag: bool = False
llm_controller: Optional[subprocess.Popen] = None
# character
character: Optional[Character] = None
# llm server client
client_to_LLM: Optional[OpenAI] = None