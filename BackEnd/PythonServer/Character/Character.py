import json
from PythonServer.Character.Fuli import Fuli
from pathlib import Path
from typing import List, Dict, Any

class Character:
    def __init__(self, char_name:str, GM:int = 10, LTM:int = 5):
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

        self.memory = Fuli(self.name)

        self.short_term_mem_num:int = GM
        self.long_term_mem_num:int = LTM

        self.last_coversation:json

    def updateMemory(self, answer:str, user_input:str):
        conversation: json = {
            "user" : user_input,
            self.name : answer
        }
        self.memory.add_conversation(conversation)
        self.memory.saveDB()
        self.updateLastConversation(conversation)

    def updateLastConversation(self, conv:json):
        self.last_coversation = conv

    #get conversations from last general_mem_max turns
    def getShortTermMem(self) -> str:  
        return self.memory.searchGDB(self.short_term_mem_num)

    #memory from vector database(num = long_term_mem_num)
    def getLongTermMem(self, user_input:str):
        return self.memory.searchVDB(user_input, self.long_term_mem_num)

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

    # list[dict] to str -> Not using now
    def format_conversations_to_string(self,conversations: list[dict]) -> str:
        if not conversations:
            return "No related conversation"
        formatted_list = [f"User: {conv['user']}\n{self.name}: {conv['from_you']}" for conv in conversations]
        return "\n\n".join(formatted_list)

    #get total memory
    def getMemoryForLLM(self, user_input:str) -> dict:
        return {
            f"conversations from last {self.long_term_mem_num} turns" : self.getShortTermMem(),
            "relative conversations from DB" : self.getLongTermMem(user_input)
            }

    def changeNumOfMem(self, num_vdb, num_gdb) -> None:
        if num_vdb:
            self.long_term_mem_num = num_vdb
        if num_gdb:
            self.short_term_mem_num = num_gdb

    def getMemoryForUser(self) -> dict:
        return (f"""
        conversations from last {self.long_term_mem_num} turns:\n
        {self.getShortTermMem()}\n
        \n
        relative conversations from DB:\n
        {self.memory.getRandomVDB(10)}"""
        )
        
    def getCharJsonLLM(self, user_input:str) -> dict:
        j:json = {
            "name"          : self.name,
            "MBTI"          : self.MBTI,
            "sex"           : self.sex,
            "age"           : self.age,
            "backstory"     : self.back_story,
            "constraints"   : self.constraints,
            "safety"        : self.safety,
            "memory"        : self.getMemoryForLLM(user_input)
            }
        return j

    # without mem for now
    def getCharInfo(self) -> dict:
        j:json = {
            "name"          : self.name,
            "MBTI"          : self.MBTI,
            "sex"           : self.sex,
            "age"           : self.age,
            "backstory"     : self.back_story,
            "constraints"   : self.constraints,
            "safety"        : self.safety
            }
        return j



