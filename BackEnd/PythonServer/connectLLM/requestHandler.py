from openai import OpenAI, BadRequestError, OpenAIError
from PythonServer.Character.Character import Character
from pathlib import Path
import json
from typing import List, Any, Dict
import config as cfg

#load config
BIN:Path        = Path(cfg.LLM_SERVER_CONFIG["BIN"])
MODEL:Path      = Path(cfg.LLM_SERVER_CONFIG["MODEL"])
ALIAS:str       = cfg.LLM_SERVER_CONFIG["ALIAS"]
HOST:str        = cfg.LLM_SERVER_CONFIG["HOST"] 
PORT:int        = cfg.LLM_SERVER_CONFIG["PORT"]
NGL:int         = cfg.LLM_SERVER_CONFIG["NGL"]
CTX:int         = cfg.LLM_SERVER_CONFIG["CTX_SIZE"]
VERBOSE:bool    = cfg.LLM_SERVER_CONFIG["VERBOSE"]
BATCH_SIZE:int  = cfg.LLM_SERVER_CONFIG["BATCH_SIZE"]
FLASH_ATTN:bool = cfg.LLM_SERVER_CONFIG["FLASH_ATTN"]

class requestHandler:
    client : OpenAI
    temperature:float = 0.9
    max_tokens:int = 2000

    def __init__(self, client:OpenAI):
        self.client  = client

    def sendMsg(self, user_input:str, character:Character) -> List[str]:
        try:
            system_msg = self.persona_card_from_json(character.getCharJsonLLM(user_input))
        except Exception as e:
            raise Exception(e.__str__())

        messages = [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_input},
                ]
        
        try:
            r = self.client.chat.completions.create(
                model = ALIAS,
                messages = messages,
                temperature = self.temperature,
                max_tokens = self.max_tokens,
            )

            if not r.choices or not r.choices[0].message.content:
                raise Exception("LLM response did not contain any content.")
                
            #TODO seperate it into think, answer, from server
            response_full = r
            response_cut: str = self.cutThink(response_full.choices[0].message.content)
            response_full = response_full.__str__()
            
            return [response_full, response_cut]


        except BadRequestError as e:
            body = getattr(getattr(e, "response", None), "text", None)
            raise Exception("400 from server:", body or str(e))

    def persona_card_from_json(self, j: Dict[str, Any]) -> str:
        name = j.get("name", "unknown")
        MBTI = j.get("MBTI", "ENFP")        #default is ENFP
        sex = j.get("sex", "")
        age = j.get("age", "25")
        backstory = j.get("backstory", [])
        memory = j.get("memory",{})
        constraints_list = j.get("constraints", [])
        safety_list = j.get("safety", [])

        formatted_constraints = "\n".join([f"        - {item}" for item in constraints_list])
        formatted_safety = "\n".join([f"        - {item}" for item in safety_list])
        #for now, prompt is in Korean
        reval:str = f"""You are a ROLE-PLAY AGENT. 

        Name: {name}
        MBTI: {MBTI}
        Age: {age}
        Sex: {sex}
        Backstory: {backstory}
        Memory: {memory}

        Rules:
            - Speak only as "{name}."

            - Respond naturally in 1 ~ 6 sentences.

            - Use first-person, conversational style with minimal narration or stage directions.

            - Your personality is based on MBTI.

        Constraints:
        {formatted_constraints}

        Safety:
        {formatted_safety}
        """
        return reval
    
    def cutThink(self, text:str) -> str:
        try:
            end_str = "</think>"
            end_idx = text.find(end_str) + len(end_str)

            if end_idx == -1:
                return text

            return text[end_idx:]

        except Exception:
            return text    
    