from fastapi import FastAPI
from openai import OpenAI
from typing import Union
import config as cfg
from typing import List
from PythonServer.Character.Character import Character
from PythonServer.serverIO import input, output
from PythonServer.connectLLM import startServer as serverLauncher
from PythonServer.connectLLM.requestHandler import requestHandler
from PythonServer.Character.CharacterHandler import CharacterHandler
from contextlib import asynccontextmanager
import subprocess

#Handler
request_handler: requestHandler = None
character_handler: CharacterHandler = None
#llm_server
llm_server_flag: bool = False
llm_controller:subprocess.Popen = None
#character
character: Character = None
# llm server client
client_to_LLM: OpenAI


@asynccontextmanager
async def lifespan(app: FastAPI):
    global character_handler
    # When server starts this code will started first
    
    character_handler = CharacterHandler()
    yield # From here, FastAPI's application starts
    
    # This code will be started after server ends
    
# FastAPI instance
app = FastAPI(lifespan=lifespan)

# Start LLM server
# select AI model is not implemented yet
@app.post("/start_llm_server/", response_model = Union[output.UserOut_startLLMResponse, output.UserOut_error])
def start_llm_server(user: input.Item_startLLMServer):
    global llm_controller, llm_server_flag, client_to_LLM, request_handler
    server_info: dict = {}

    # If server is already turned on
    if(llm_server_flag):
        response = output.UserOut_error(
            error_location="Error from start_llm_server in delta_me13_server.py",
            error_detail="LLM server is already activated!"
        )
        return response

    #start llm server
    try:
        llm_controller = serverLauncher.startServer(mode = user.mode, chat_template = user.chat_template)
        llm_server_flag = True
        #TODO this seems messy --> needs to fix config
        client_to_LLM = OpenAI(base_url=f"http://{cfg.LLM_SERVER_CONFIG['HOST']}:{cfg.LLM_SERVER_CONFIG['PORT']}/v1", api_key="sk-no-key-needed")
        request_handler = requestHandler(client_to_LLM)

        #TODO add command_handler

        #-------------------------
        #TODO make server_info json
        server_info = {}

        #-------------------------
        response = output.UserOut_startLLMResponse(
            is_normal = True,
            is_LLM_server_started=True,
            llm_server_info=server_info
        )
    except Exception as e:
        error_msg:str = f"Error starting LLM server: {e}"
        llm_server_flag = False     # It doesn't need it but for clarification
        print(error_msg)
        response = output.UserOut_error(
                error_location="Error from start_llm_server in delta_me13_server.py",
                error_detail=error_msg
            )
        return response
        
    # Make response model
    response = output.UserOut_startLLMResponse(
        is_normal = True,
        is_LLM_server_started=llm_server_flag,
        llm_server_info=server_info
    )

    return response
# CHARACTER-------------------------------------------------------------------------------------
# Select character(show character, character load)
# show saved characters
@app.get("/show_saved_characters/", response_model= Union[output.UserOut_showSavedCharacter, output.UserOut_error])
def show_saved_character():
    global character_handler
    try:
        return output.UserOut_showSavedCharacter(
            is_normal = True,
            Characters=character_handler.getSavedCharacters()
        )
    except Exception as e:
        return output.UserOut_error(
            error_location="Error from show_saved_character from delta_me13_server.py",
            error_detail=e.__str__()
        )

# load character
@app.put("/load_character/", response_model = Union[output.UserOut_loadCharacter, output.UserOut_error])
def load_character(user: input.Item_loadCharacter):
    global character, character_handler
    if(character != None):
        return output.UserOut_error(
            error_location="Error from select_character from delta_me13_server.py",
            error_detail="Character already exists!"
        )
    elif(not character_handler.checkCharacter(user.character_file_name)):
        return output.UserOut_error(
            error_location="Error from select_character from delta_me13_server.py",
            error_detail=f"Character {user.character_file_name} does not exist in charcter save folder!"
        )
    
    try:
        character = Character(user.character_file_name)

        return output.UserOut_loadCharacter(
            is_normal = True,
            is_char_exists=True,
            loaded_character=character.getCharInfo()
        )
    except Exception as e:
        character = None
        return output.UserOut_error(
            error_location="Error from select_character from delta_me13_server.py",
            error_detail="Something went wrong while generating character!\n" + e.__str__()
        )

# Change character's personality
@app.patch("/change_character_personality/", response_model= Union[output.UserOut_changePersonality, output.UserOut_error])
def change_character_personality(user: input.Item_changePersonality):
    global character
    if(character.updatePersonality(user.MBTI_to)):
        return output.UserOut_changePersonality(
            is_normal=True,
            is_changed=True
        )
    else:
        return output.UserOut_error(
            error_location="Error from change_character_personality in delta_me13_server.py",
            error_detail=f"Some how failed to update MBTI(personality). {user.MBTI_to} could not be one of MBTI."
        )
    
# Generate character
@app.post("/generate_character/", response_model=Union[output.UserOut_generateCharacter, output.UserOut_error])
def generate_character(user: input.Item_generateCharacter):
    global character_handler, character
    try:
        character_handler.makeNewCharacter(user)
    except Exception as e:
        return output.UserOut_error(
            error_location="Error from generate_character while generating character in delta_me13_server.py",
            error_detail=e
        )
    if(user.is_this_char_target):
        if(character != None):
            return output.UserOut_error(
                error_location="Error from select_character from delta_me13_server.py",
                error_detail="Character already exists!"
            )
        elif(not character_handler.checkCharacter(user.file_name)):
            return output.UserOut_error(
                error_location="Error from select_character from delta_me13_server.py",
                error_detail=f"Character {user.file_name} does not exist in charcter save folder!"
            )
        try:
            character = Character(user.file_name)

        except Exception as e:
            return output.UserOut_error(
                error_location="Error from select_character from delta_me13_server.py",
                error_detail="Something went wrong while generating character!\n" + e.__str__
            )
    
    return output.UserOut_generateCharacter(
        is_normal=True,
        is_generated=True,
    )

# CHARACTER ENDS--------------------------------------------------------------------------------
 
    
# Chat    
@app.post("/chat_with_character/", response_model = Union[output.UserOut_Chat, output.UserOut_error])
def chat_with_character(user: input.Item_Chat):
    global character, request_handler
    # check character is loaded
    if(character == None):
        return output.UserOut_error(
            error_location="Error from chat_with_character in delta_me13_server.py",
            error_detail="Character is not loaded!"
        )
    
    # TODO user validate


    #--------------------------
    if(request_handler == None):
        return output.UserOut_error(
            error_location="Error from chat_with_character in delta_me13_server.py",
            error_detail="request_handler is not loaded yet"
        )
    
    try:
        # result[0]: full content (goes to client) result[1]: only message (goes to character's memory) <--- not yet
        result: List[str] = request_handler.sendMsg(user.chat, character)
        character.updateMemory(result[1], user.chat)
        #TODO seperate it into think, answer, from server
        return output.UserOut_Chat(
            is_normal = True,
            character_name=character.name,
            thinking="NOT YET",
            response=result[1],
            etc_server="NOT YET"
        )

    except Exception as e:
        return output.UserOut_error(
            error_location="Error from chat_with_character in delta_me13_server.py",
            error_detail=e.__str__()
        )
    