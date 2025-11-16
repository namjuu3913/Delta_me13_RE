import json
from PythonServer.Character.Fuli import Fuli
from PythonServer.customPY.default_class import Conversation
from pathlib import Path
from typing import List, Dict, Any

class Character:
    def __init__(self, char_name:str, last_num: int,
                 recent_num:int, impressive_num:int,
                 long_num:int, background_num:int,
                 emotion_num:int  ):
        char_data_path = Path(__file__).resolve().parent/"CharacterSave"/char_name/f"{char_name}.json"
        print(char_data_path)

        with open(f"{char_data_path}", "r", encoding="utf-8") as f:
            char_data = json.load(f)

        self.name = char_data["name"]
        self.sex = char_data["sex"]
        self.MBTI = char_data["MBTI"]
        self.age = char_data["age"]
        self.back_story: List[str] = char_data["back_story"]
        self.constraints: List[str] = char_data["constraints"]
        self.safety: List[str] = char_data["safety"]

        self.memory = Fuli(self.name, last_num , recent_num, impressive_num, long_num, background_num, emotion_num)

        self.last_coversation : Conversation


    def updateMemory(self, conver_in : Conversation):
        self.memory.update_memory(conver_in)
        self.updateLastConversation(conver_in)


    def updateLastConversation(self, conv : Conversation):
        self.last_coversation = conv


    # change personality    
    def updatePersonality(self, target_personality:str)->bool:
        mbti_types = {
            'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
            'ISTP', 'ISFP', 'INFP', 'INTP',
            'ESTP', 'ESFP', 'ENFP', 'ENTP',
            'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
        }
        is_mbti = lambda target_personality: target_personality.upper() in mbti_types
        if(is_mbti):
            self.MBTI = target_personality
            return True
        else:
            return False
        

    # update emotion
    def update_emotion(self, VAD_raw_str: str):
        if not self.memory.get_emotion(VAD_str = VAD_raw_str):
            raise Exception("Emotion update in Fuli failed!!!!")


    # get total memory
    async def getMemory(self, user_input:str) -> dict:
        return await self.memory.get_memories(user_input)
    

        
    async def getCharJsonLLM(self, user_input:str) -> dict:
        memory_data = await self.getMemory(user_input)
        j:json = {
            "name"          : self.name,
            "MBTI"          : self.MBTI,
            "sex"           : self.sex,
            "age"           : self.age,
            "backstory"     : self.back_story,
            "constraints"   : self.constraints,
            "safety"        : self.safety,
            "memory"        : memory_data
            }
        return j


    def getCharInfo(self) -> dict:
        j:json = {
            "name"          : self.name,
            "MBTI"          : self.MBTI,
            "sex"           : self.sex,
            "age"           : self.age,
            "backstory"     : self.back_story,
            "constraints"   : self.constraints,
            "safety"        : self.safety
            # "last_memory"   : self.getMemory(self.last_coversation.user_context)
            }
        return j


    def turn_off_character(self) -> None:
        self.memory.turn_off()
        return


