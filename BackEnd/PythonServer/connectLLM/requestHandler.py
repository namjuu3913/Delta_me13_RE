from openai import AsyncOpenAI, BadRequestError, OpenAIError
from PythonServer.Character.Character import Character
from pathlib import Path
from typing import List, Any, Dict
import BackEnd.Config.config as cfg
import re, warnings, json

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
    client : AsyncOpenAI
    temperature:float = 0.9
    max_tokens:int = 2000

    def __init__(self, client:AsyncOpenAI):
        self.client  = client

    async def sendMsg(self, user_input:str, character:Character) -> List[dict]:
        # get info first
        character_info_and_mem:dict = await character.getCharJsonLLM(user_input)

        # find character's emotion----------------------------------------------------
        psycologist_response_system_msg = self.psycologist_response_card(json.dumps(character_info_and_mem, ensure_ascii=False, indent=2))

        messages_psycologist_response = [
                    {"role": "system", "content": psycologist_response_system_msg},
                    {"role": "user", "content": f"Analyze the reaction to this user input: '{user_input}'"},
        ]
        try:
            r_psy = await self.client.chat.completions.create(
                model = ALIAS,
                messages = messages_psycologist_response,
                temperature = 0.0,
                max_tokens = self.max_tokens,
            )

            if not r_psy.choices or not r_psy.choices[0].message.content:
                raise Exception("LLM response did not contain any content.")
                
            llm_psy_content = r_psy.choices[0].message.content
            psycologist_raw_str = self._parse_llm_response(llm_psy_content)["answer"]

        except BadRequestError as e:
            body = getattr(getattr(e, "response", None), "text", None)
            raise Exception("400 from server:", body or str(e))

        # try to parse psycologist_raw_str as json
        try: 
            if not isinstance(psycologist_raw_str, str):
                warnings.warn(f"Error: it is not JSON string but {type(psycologist_raw_str)}.", TypeError)
            
            else:
                psycologist_parsed_json:dict = json.loads(psycologist_raw_str)        
                # succeed to parse it as json
                print("RequestHandler says: psycologist response successfully parsed to json!!!")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed: str is not json format. \nError: {e}\n Raw String: {psycologist_raw_str}")
        except TypeError:
            raise Exception(f"Failed: it is not str. (type: {type(psycologist_raw_str)}).")

        # is it right format of json?
        required_keys = {"Valence", "Dominance", "Arousal"}
        if required_keys.issubset(psycologist_parsed_json.keys()):
            print("Success: 'Valance', 'Dominance', 'Arousal' keys are in it.")
        else:
            missing_keys = required_keys - psycologist_parsed_json.keys()
            raise Exception(f"Keys are missing in the response!! \nMissing keys : {missing_keys}\nRaw String: {psycologist_raw_str}")

        # update character's emotion state
        character.update_emotion(json.dumps(psycologist_parsed_json, ensure_ascii = False, indent = 1))
        #------------------------------------------------------------------------------


        # get actual character's response----------------------------------------------- 
        character_response_system_msg = self.character_response_card_from_json(character_info_and_mem, character)

        messages_actual_response = [
                    {"role": "system", "content": character_response_system_msg},
                    {"role": "user", "content": user_input},
                ]
        
        try:
            r_char = await self.client.chat.completions.create(
                model = ALIAS,
                messages = messages_actual_response,
                temperature = self.temperature,
                max_tokens = self.max_tokens,
            )

            if not r_char.choices or not  r_char.choices[0].message.content:
                raise Exception("LLM response did not contain any content.")
                
            llm_content = r_char.choices[0].message.content
            parsed_response = self._parse_llm_response(llm_content)
            
            return [parsed_response, r_char.model_dump()]


        except BadRequestError as e:
            body = getattr(getattr(e, "response", None), "text", None)
            raise Exception("400 from server:", body or str(e))
        
    def _parse_llm_response(self, content: str) -> dict:
        """From string answer from llm, devide 'think' and 'answer'."""
        think_content = ""
        answer_content = ""

        matched_result:List[str] = self._cut_based_on_llm_type()

        think_match = re.search(matched_result[0], content, re.DOTALL | re.IGNORECASE)
        if think_match:
            think_content = think_match.group(1).strip()
            content = content.replace(think_match.group(0), "").strip()
        
        answer_match = re.search(matched_result[1], content, re.DOTALL | re.IGNORECASE)
        if answer_match:
            answer_content = answer_match.group(1).strip()
        else:
            answer_content = content

        return {"think": think_content, "answer": answer_content}
    
    def psycologist_response_card(self, participant:str) -> str:
        return f"""
        You are the world's best psycologist
        Analyze the VAD vector emotion vector of the following participant when participant was asked input question and return a JSON object 
        with three values: Valence, Dominance, and Arousal with float value between -1 and 1. 

        Rules:
            - Each value should be a float number between -1 and 1. 

            - Only return the JSON object, no extra text

            - The JSON format will looks like this:
                {{
                    "Valence" : float value,
                    "Dominance" : float value,
                    "Arousal"   : float value
                }}

        participant: {participant}
        """

    def character_response_card_from_json(self, j: Dict[str, Any], char:Character) -> str:
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
        {name}'s current emotion: {str(char.memory.simple_emotion_result)}
        {name}'s current state: {str(char.memory.simple_emotion_analysis_token)}

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
    
    def _cut_based_on_llm_type(self)-> List[str]:
        model_patterns = {
            "Qwen3": [r'<think>(.*?)</think>', r'<answer>(.*?)</answer>'],
            "Llama3": [r'\[THINK\](.*?)\[/THINK\]', r'\[ANSWER\](.*?)\[/ANSWER\]'],
            # add other patterns here
            
        }

        # Find the keywords in ALIAS and return
        for keyword, patterns in model_patterns.items():
            if keyword in ALIAS:
                return patterns
                
        # default
        default_patterns = [r'<think>(.*?)</think>', r'<answer>(.*?)</answer>']
        return default_patterns