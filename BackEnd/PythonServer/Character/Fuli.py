"""
# Name of this class, Fuli, is inspired by the game HSR.
This class handles the memory of the Character.
If there is no VDB, GDB in the character's folder, It will automatically generate new GDB and VDB file.
If ther is both VDB and GDB, it will use them as character's memory.

GDB: General data base
    This is a save file of every conversation with user as a array of a dictionary.
    In each conversation, Fuli gives to character last k(Parameter of searchGDB function) conversations.
VDB: Vector data base
    This is a vector save file of every conversation with user as a .index file.
    This VDB is made based on faiss-cpu.
    For sentence transformer, it is using paraphrase-multilingual-mpnet-base-v2 model
    In each conversation, Fuli gives to character k(Parameter of getRandomVDB) conversations from VDB.
    * This needs optimization because it saves whole conversation with user.
"""
import numpy as np
import faiss, json, random
from pathlib import Path
from sentence_transformers import SentenceTransformer as ST

# paraphrase-multilingual-mpnet-base-v2 model for multilingual purpose
ST_MODEL_PATH = Path(__file__).resolve().parent / "models" / "models--sentence-transformers--paraphrase-multilingual-mpnet-base-v2"/"snapshots"/"4328cf26390c98c5e3c738b4460a05b95f4911f5"
if not ST_MODEL_PATH.exists():
    raise FileNotFoundError(f"Cannot find model folder: {ST_MODEL_PATH}")
# Current gpu has only 16 gb. So, use cpu first
model = ST(str(ST_MODEL_PATH), device='cpu')
EMBEDDING_DIMENSION = model.get_sentence_embedding_dimension()

# this vector db is run on CPU
class Fuli:
    # d = demension
    d: int
    name: str
    # db(memory)
    vector_db: faiss.Index
    general_db: list[dict]
    # file path
    db_file_path_index: Path
    db_file_path_json: Path

    def __init__(self, name: str):
        self.name = name
        self.db_file_path_index = Path(__file__).resolve().parent / "CharacterSave" / self.name/"VectorDB"
        self.db_file_path_json = Path(__file__).resolve().parent / "CharacterSave" / self.name/"GeneralDB"
        index_path = self.db_file_path_index / f"{self.name}_VDB.index"
        json_path = self.db_file_path_json / f"{self.name}_GDB.json"

        # load .json and .index 
        if index_path.exists() and json_path.exists():
            print(f"'{self.name}' Calling DB...")
            self.vector_db = faiss.read_index(str(index_path))
            self.d = self.vector_db.d
            with open(json_path, 'r', encoding='utf-8') as f:
                self.general_db = json.load(f)
        else:
            self.d = EMBEDDING_DIMENSION
            print(f"'{self.name}' Generating new DB (demension: {self.d})...")
            self.vector_db = faiss.IndexFlatL2(self.d)
            self.general_db = []
 
    #change text to d demension vector
    @staticmethod
    def _get_vector_from_text(text: str) -> np.ndarray:
        embedding = model.encode(text)
        return embedding.astype(np.float32).reshape(1, -1)

    #add conversation to both GDB and VDB
    def add_conversation(self, conversation: dict) -> None:
        vectored_text = Fuli._get_vector_from_text(conversation['user'])
        #save
        self.vector_db.add(vectored_text)
        self.general_db.append(conversation)

    #get searched data from VDB
    def searchVDB(self, user_input:str, k:int = 5) -> list[dict]:
        if self.vector_db.ntotal == 0:
            return []
        #when k is smaller then number of vector db num
        elif k > self.vector_db.ntotal:
            k = self.vector_db.ntotal 

        user_input_vector = Fuli._get_vector_from_text(user_input)
        _, indices = self.vector_db.search(user_input_vector, k) # _ is distances 

        valid_indices = [i for i in indices[0] if i >= 0]

        return [self.general_db[i] for i in valid_indices]
    
    # get random memory from VDB
    def getRandomVDB(self, k: int = 5) -> list[dict]: 
        ntotal = self.vector_db.ntotal
        if ntotal == 0:
            return []

        k = min(k, ntotal)

        random_indices = random.sample(range(ntotal), k)

        return [self.general_db[i] for i in random_indices]

    #get searched data from GDB
    def searchGDB(self, k:int = 1) -> list[dict]:
        if k > len(self.general_db):
            k = len(self.general_db)
        return self.general_db[-k:]

    def saveDB(self) -> None:
        # --- VectorDB ---
        self.db_file_path_index.mkdir(parents=True, exist_ok=True)
        save_path_index = self.db_file_path_index / f"{self.name}_VDB.index"
        faiss.write_index(self.vector_db, str(save_path_index))

        # --- GeneralDB ---
        self.db_file_path_json.mkdir(parents=True, exist_ok=True)
        save_path_json = self.db_file_path_json / f"{self.name}_GDB.json"
        with open(save_path_json, 'w', encoding='utf-8') as f:
            json.dump(self.general_db, f, ensure_ascii=False, indent=4)
        
        print(f"'{self.name}' DB save complete.")
