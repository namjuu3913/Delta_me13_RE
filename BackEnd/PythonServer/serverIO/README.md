
# API

* ## start_llm_server
    * Request URL: http://127.0.0.1:8000/start_llm_server/
    * Type: POST
    * Parameters: No parameters
    * Request body: 
        ```sh
        {
            "user_name": "string",
            "llm_model_name": "string",
            "mode": "new_console",
            "chat_template": "chatml"
        }
        ```
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "is_LLM_server_started": true,
            "llm_server_info": {}
        }
        ```
    * Purpose: Turn on the local llm server(llama.cpp)
    * NOTE: If llm server is already opened, it will return error response.

* ## show_saved_characters
    * Request URL: http://127.0.0.1:8000/show_saved_characters/
    * Type: GET
    * Parameters: No parameters
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "Characters": [] (array of json)
        }
        ```
        [Characters README.md](../Character/README.md)
    * Purpose: Returns the info of saved character.

* ## load_character
    * Request URL: http://127.0.0.1:8000/load_character/
    * Type: PUT
    * Parameters: No parameters
    * Request body: 
        ```sh
        {
            "user_name": "string",
            "character_file_name": "string"
        }
        ```
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "is_char_exists": true,
            "loaded_character": {}
        }
        ```
    * Purpose: Load character to chat.
    * NOTE: If Character is already loaded, Character is not exists or something sent wrong, it will return error response.

* ## change_character_personality
    * Request URL: http://127.0.0.1:8000/change_character_personality/
    * Type: PATCH
    * Parameters: No parameters
    * Request body: 
        ```sh
        {
            "user_name": "string",
            "MBTI_to": "string"
        }
        ```
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "is_changed": true
        }
        ```
    * Purpose: Change character's personality.
    * NOTE: If something went wrong, it will return error response


* ## generate_character
    * Request URL: http://127.0.0.1:8000/generate_character/
    * Type: POST
    * Parameters: No parameters
    * Request body: 
        ```sh
        {
            "user_name": "string",
            "is_this_char_target": true,
            "file_name": "string",
            "name": "string",
            "sex": "string",
            "MBTI": "string",
            "age": "string",
            "back_story": [
                "string"
            ],
            "constraints": [
                "string"
            ],
            "safety": [
                "string"
            ]
        }
        ```
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "is_generated": true
        }
        ```
    * Purpose: Make new character
    * NOTE: If is_this_char_target is true, the character to chat is automatically set to new character. 


* ## chat_with_character
    * Request URL: http://127.0.0.1:8000/chat_with_character/
    * Type: POST
    * Parameters: No parameters
    * Request body: 
        ```sh
        {
            "user_name": "string",
            "chat": "string"
        }
        ```
    * Response body: 
        ```sh
        {
            "is_normal": true,
            "character_name": "string",
            "response": {
                "think" : "string",
                "answer" : "string"
            },
            "everything": {}
        }
        ```
    * Purpose: Make new character
    * NOTE: If is_this_char_target is true, the character to chat is automatically set to new character. 
