from pydantic import BaseModel
from typing import List, Dict, Any
# json input

# Base
class ItemBase(BaseModel):  
    user_name: str

# Start llm server
class Item_startLLMServer(BaseModel):
    llm_model_name : str
    mode: str = "new_console"
    chat_template:str = "chatml"

# Select Character
class Item_loadCharacter(BaseModel):
    character_file_name: str

# change psersonality (Change MBTI for now)
# TODO: Based on change_type, it will change character's info
class Item_changePersonality(ItemBase):
    MBTI_to: str

# generate character
class Item_generateCharacter(ItemBase):
    is_this_char_target:bool    # if this is true, server will automatically load this character to chat 
    file_name:str
    name:str
    sex:str
    MBTI:str
    age:str
    back_story:List[str]
    constraints:List[str]
    safety:List[str]

# user chat request
class Item_Chat(ItemBase):  
    chat: str

# get info of servers (deal with request_type of base)
class Item_serverInfo(ItemBase):
    pass
    