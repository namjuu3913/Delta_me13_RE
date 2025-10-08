import config as cfg
from Character.Character import Character as Ch
from PythonServer.connectLLM import requestHandler as RH
from pathlib import Path

#load config
BIN:Path        = Path(cfg.SERVER_CONFIG["BIN"])
MODEL:Path      = Path(cfg.SERVER_CONFIG["MODEL"])
ALIAS:str       = cfg.SERVER_CONFIG["ALIAS"]
HOST:str        = cfg.SERVER_CONFIG["HOST"] 
PORT:int        = cfg.SERVER_CONFIG["PORT"]
NGL:int         = cfg.SERVER_CONFIG["NGL"]
CTX:int         = cfg.SERVER_CONFIG["CTX_SIZE"]
VERBOSE:bool    = cfg.SERVER_CONFIG["VERBOSE"]
BATCH_SIZE:int  = cfg.SERVER_CONFIG["BATCH_SIZE"]
FLASH_ATTN:bool = cfg.SERVER_CONFIG["FLASH_ATTN"]

class CommandHandler:
    def __init__(self, current_Char:Ch, requestHandler:RH):
        self.current_Char = current_Char
        self.requestHandler = requestHandler
    
    def isCommand(self, user_input:str)->int:
        if user_input == "-/open command":
            self.command()
            return 2 # command complete. continue

        elif user_input == "-/exit":
                return 3 # end conversation 
        else:
            return 1 #it's not a command

    def command(self):

        commands = {
            "help": self.printHelp,
            "show_memory": self.current_Char.getCharInfo,
            "show_memory_STM": self.current_Char.getShortTermMem,
            "show_memory_LTM": self.current_Char.memory.getRandomVDB,
            "show_serverinfo": self.print_server_info,
            "change_temp_or_maxtoken": self.change_temp_or_max_tokens
        }

        while True:
            print("\nThis is command handler. Enter a command or 'exit' to quit.")
            next_command = input("command: ").lower()

            if next_command == "exit":
                print("Exiting command handler.")
                break
            
            self.execute_command(next_command, commands)

    def execute_command(self, command_str, command_dict):
        """A helper function to find and execute a command from the dictionary."""
        func_to_run = command_dict.get(command_str)
        
        if func_to_run:
            result = func_to_run()
            if result:
                print(result)
        else:
            print(f"Error: Unknown command '{command_str}'. Type 'help' to see available commands.")
     
    def printHelp(self) -> str:
        """Returns a formatted string listing all available commands."""
        help_text = """
        Here are the available commands:

        [Memory Commands]
            show_memory         : Display all memory about the current character.
            show_memory_STM     : Show the character's short-term(GDB) memory.
            show_memory_LTM     : Show a random entry(for now) from the character's long-term memory(VDB).

        [Server Commands]
            show_serverInfo     : Display the current server and model configuration.

        [AI Settings]
            change_temp_or_maxtoken: Change the AI's temperature or max token settings.

        [General Commands]
            help                : Show this help message.
            exit                : Exit the command handler and return to the conversation.
                """
        return help_text

    def get_server_info(self) -> str:
        info = f"""
        Server BIN: {BIN}
        Model : {ALIAS}
        Address : http://{HOST}:{PORT}/v1
        n-gpu-layers : {NGL}
        ctx-size : {CTX}
        batch-size : {BATCH_SIZE}
        flash-attn : {FLASH_ATTN}
        """
        return info

    def change_temp_or_max_tokens(self):
        while True:
            print("To change temperature, enter 'temperature'. To change max tokens, enter 'max token'. If you want both, enter 'both'.")
            choice = input("What you want? : ").lower()

            # Temperature
            if choice == "temperature":
                while True:
                    val_str = input("Enter new temperature (0.0 to 1.0): ")
                    try:
                        val = float(val_str)
                        if 0.0 <= val <= 1.0:
                            self.requestHandler.temperature = val
                            print(f"Temperature updated to {val}")
                            break # Exit the inner while loop
                        else:
                            print("Error: Value must be between 0.0 and 1.0.")
                    except ValueError:
                        print("Error: Invalid input. Please enter a number.")
                break # Exit the main while loop

            # Max Tokens
            elif choice == "max token":
                while True:
                    val_str = input(f"Enter new max tokens (0 to {CTX}): ")
                    try:
                        val = int(val_str)
                        if 0 <= val <= CTX: # check against CTX
                            self.requestHandler.max_tokens = val
                            print(f" Max tokens updated to {val}")
                            break # Exit the inner while loop
                        else:
                            print(f"Error: Value must be between 0 and {CTX}.")
                    except ValueError:
                        print("Error: Invalid input. Please enter a whole number.")
                break # Exit the main while loop

            # Both
            elif choice == "both":
                # Temperature
                while True:
                    val_str = input("Enter new temperature (0.0 to 1.0): ")
                    try:
                        val = float(val_str)
                        if 0.0 <= val <= 1.0:
                            self.requestHandler.temperature = val
                            print(f"Temperature updated to {val}")
                            break # Exit the inner while loop
                        else:
                            print("Error: Value must be between 0.0 and 1.0.")
                    except ValueError:
                        print("Error: Invalid input. Please enter a number.")

                # Second, get and validate max tokens
                while True:
                    val_str = input(f"Enter new max tokens (0 to {CTX}): ")
                    try:
                        val = int(val_str)
                        if 0 <= val <= CTX:
                            self.requestHandler.max_tokens = val
                            print(f"Max tokens updated to {val}")
                            break # Exit the inner while loop
                        else:
                            print(f"Error: Value must be between 0 and {CTX}.")
                    except ValueError:
                        print("Error: Invalid input. Please enter a whole number.")
                
                break # Exit the main while loop

            else:
                print("Invalid command. Please enter 'temperature', 'max token', or 'both'.")
                            
