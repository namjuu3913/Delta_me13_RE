from openai import OpenAI, BadRequestError, OpenAIError
from PythonServer.Character.Character import Character
from pathlib import Path
from typing import List, Any, Dict
import config as cfg
import re

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

    def sendMsg(self, user_input:str, character:Character) -> List[dict]:
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
                
            llm_content = r.choices[0].message.content
            parsed_response = self._parse_llm_response(llm_content)
            
            return [parsed_response, r.model_dump()]


        except BadRequestError as e:
            body = getattr(getattr(e, "response", None), "text", None)
            raise Exception("400 from server:", body or str(e))
        
    def _parse_llm_response(self, content: str) -> dict:
        """From string answer from llm, devide 'think' and 'answer'."""
        think_content = ""
        answer_content = ""

        think_match = re.search(r'\[THINK\](.*?)\[/THINK\]', content, re.DOTALL)
        if think_match:
            think_content = think_match.group(1).strip()
            content = content.replace(think_match.group(0), "").strip()
        
        answer_match = re.search(r'\[ANSWER\](.*?)\[/ANSWER\]', content, re.DOTALL)
        if answer_match:
            answer_content = answer_match.group(1).strip()
        else:
            answer_content = content

        return {"think": think_content, "answer": answer_content}

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
    