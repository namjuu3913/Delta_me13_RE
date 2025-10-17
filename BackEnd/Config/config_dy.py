from pathlib import Path
#
# Apply this after frontEnd finishes
#
class config_dy:
    chat_config_flag:bool = False
    llm_config_flag:bool = False
    # llama.cpp server config
    MODEL: Path
    PORT: int = 8129
    CTX_SIZE: int
    NGL: int
    ALIAS: str
    BATCH_SIZE: int
    #TODO
    VERBOSE: bool = True
    FLASH_ATTN: bool = True

    # chat config
    TEMPERATURE: float
    MAX_TOKENS: int

    def update_chat_config(self, change_to: dict) -> None:
        """Updates the chat-related configuration attributes."""
        self.TEMPERATURE = change_to["TEMPERATURE"]
        self.MAX_TOKENS = change_to["MAX_TOKENS"]
        self.chat_config_flag = True
    
    def update_llm_server_config(self, change_to: dict) -> None:
        """Updates the llama.cpp server-related configuration attributes."""
        self.MODEL = change_to["MODEL"]
        self.PORT = change_to["PORT"]
        self.CTX_SIZE = change_to["CTX_SIZE"]
        self.NGL = change_to["NGL"]
        self.ALIAS = change_to["ALIAS"]
        self.BATCH_SIZE = change_to["BATCH_SIZE"]
        self.VERBOSE = change_to.get("VERBOSE", self.VERBOSE)
        self.FLASH_ATTN = change_to.get("FLASH_ATTN", self.FLASH_ATTN)
        self.llm_config_flag = True

    def get_chat_config(self) -> dict:
        if(not self.chat_config_flag):
            raise Exception("Chat config is not yet initialized")
        
        return {
            "TEMPERATURE" : self.TEMPERATURE,
            "MAX_TOKENS" : self.MAX_TOKENS
        }
    
    def get_llm_server_config(self) -> dict:
        if(not self.llm_config_flag):
            raise Exception("LLM server config is not yet initialized")
        
        return{
            "MODEL" : self.MODEL,
            "PORT" : self.PORT,
            "CTX_SIZE" : self.CTX_SIZE,
            "NGL" : self.NGL,
            "ALIAS" : self.ALIAS,
            "BATCH_SIZE" : self.BATCH_SIZE,
            "VERBOSE": self.VERBOSE,
            "FLASH_ATTN" : self.FLASH_ATTN
        }