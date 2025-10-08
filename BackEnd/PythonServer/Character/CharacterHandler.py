import json
from pathlib import Path
from typing import List, Dict, Any
from PythonServer.serverIO.input import Item_generateCharacter

class CharacterHandler:
    charac_save_path: Path = Path(__file__).resolve().parent / "CharacterSave"

    #Check there is a character folder in CharacterSave
    def checkCharacter(self, name_charac: str) -> bool:
        target_path = self.charac_save_path / name_charac
        return target_path.is_dir()
    

    #Make new Character
    def makeNewCharacter(self, character_ingre: Item_generateCharacter):
        # does character already exist?
        if self.checkCharacter(character_ingre.file_name):
            raise Exception(f"Character folder {character_ingre.file_name} already exists!")
        
        unwanted_fields = {'is_this_char_target'}
        new_character:dict = character_ingre.model_dump(exclude=unwanted_fields)

        new_char_path:Path = self.charac_save_path / character_ingre.file_name
        new_char_path.mkdir(parents=True, exist_ok=True)
        
        new_char_json_path:Path = new_char_path / f"{character_ingre.file_name}.json"
        try:
            with open(new_char_json_path, 'w', encoding='utf-8') as f:
                json.dump(new_character, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"Failed to generate Character!\ndetails: {e.__str__()}")
        

    #Search for every Character in character save folder and returns every character json
    def getSavedCharacters(self) -> List[Dict[str, Any]]:
        all_characters_json: List[Dict[str, Any]] = []

        for json_path in self.charac_save_path.glob("*/*.json"):
            try:
                with open(json_path, 'r', encoding="utf-8") as f:
                    data: dict = json.load(f)
                    all_characters_json.append(data)

            except Exception as e:
                raise e
            
        return all_characters_json