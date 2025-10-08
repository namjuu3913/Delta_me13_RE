## About the Project
Delta-me13_py is a character chatbot that runs locally using a quantized GGUF LLM and multilingual sentence embeddings. It aims to provide responsive, multilingual dialog while keeping resource usage modest. I started this project after I got inspiration from a game named HSR(Honkai Star Rail). Currently, this code is somewhat messy and runs on hopes and dreams now, but I will work on fixing it.

Because I'm Korean, some part of the code is written in Korean. I will gradually change those into English later.

## Development environment
* OS: Windows 11
* IDE: Visual Studio 2022
* CudaToolKit: 12.9
* CPU: Ryzen 9 7900x
* GPU: RTX 5080
* DRAM: 96 GB DDR5 RAM

## Goal of this project
I have goals for this project, and I need collaborators to achieve them.

**Goals**
* GUI
* Implement the emotion module. (for more humanlike actions)
* Add function calls. (make the character act)
* Add a simulation module to simulate the action of a virtual persona(character) in a series of events.
* Add custom C++ lib
* Most importantly, enhance Python and C++ skills


## Highlights
- Multilingual conversations via `paraphrase-multilingual-mpnet-base-v2`
- Local LLM (GGUF) inference for privacy and speed
- Tried simple fine-tuning with RAG using FAISS-based vector search for fast retrieval over dialogue/context


## Installation

Follow these steps to set up the project environment locally. This guide covers installing necessary system-level dependencies, setting up a Python virtual environment, and downloading the required models.

1.  **Prerequisites**
    Before you begin, ensure you have the following software installed on your system.
    
    * Python 3.11: This code is based on Python 3.11
        * You can download it from the [Python Downloads](https://www.python.org/downloads/)
    * NVIDIA CUDA Toolkit 12.9: Required for GPU acceleration.
        * You can download it from the [NVIDIA CUDA Toolkit Archive.](https://developer.nvidia.com/cuda-12-9-0-download-archive)
    * Git LFS (Large File Storage): This project uses Git LFS to manage large model files.
        * Download and install it from the [official Git LFS website.](https://git-lfs.com/) After installing, run ``` git lfs install``` in your terminal once to initialize it.
          
3.  Setup Steps
    1. Clone the Repository
    ```sh
    git clone https://github.com/namjuu3913/Delta_me13_py.git
    ```
    
    2. Navigate to the project directory.
    ```sh
    cd Delta_me13_py
    ```
    
    3. Create a Python Virtual Environment

       I recommend using a virtual environment to isolate project dependencies. The following command will create a folder named .venv in your project directory.
    ```sh
    
    python -m venv .venv
    ```
    
    4. Activate the Virtual Environment

        You must activate the environment before installing packages.
       * On Windows (PowerShell/CMD):
         ```sh
            .\.venv\Scripts\Activate
         ```
       * On macOS/Linux (Bash/Zsh):
         ```sh
            source .venv/bin/activate
         ```
        (I'm not sure it will work on macOS and Linux)
    
    5. Install Required Python Packages

        Install all the necessary libraries from the requirements.txt file into your active virtual environment.
         ```sh
            pip install -r requirements.txt
         ```

    6. Download Large Model Files

       Finally, pull the large model and data files managed by Git LFS.
     ```sh
     git lfs pull
     ```
     
 4. Download Models
   * #### LLM (GGUF)
     
     You can download any GGUF-formatted model from [huggingface](https://huggingface.co/) in the ```AI/models``` folder.
     
     Recommended & tested: Qwen3-14B-Q4_K_M, (see the model on [Hugging Face](https://huggingface.co/Qwen))
     
   * #### Sentence transformer model
   
     **Use paraphrase-multilingual-mpnet-base-v2 model.**

     If you download it with sentence transformer, it usually downloaded at ```C:\Users\UserName\.cache\huggingface\hub```

     Put the file in the ```projecfile/Character/models``` file

     Model: [Sentence-Transformers page.](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2).

**System Requirements**

Desktop
* Small models(1b ~ 8b): 8–12 GB VRAM
* Medium models (14B–20B): 16 GB VRAM or more
* GPU: NVIDIA recommended. Not tested on Intel or AMD (Ryzen) GPUs.
* System RAM (DRAM): 32 GB recommended. Not tested with 16–32 GB. For smoother operation, 48 GB or more is recommended.

Laptop
* CPU/GPU: A recent CPU with built-in AI acceleration *or* a dedicated GPU model.
* Memory: Unified memory or high-bandwidth RAM such as LPDDR5.
* Capacity: 48 GB (preferred) or at least 32 GB.
* Tested configuration:
    * Verified working on an HX 370 system with 64 GB DDR5. (Used Qwen3 -14b and Qwen3 -8b)
    * Verified working on laptop with i5 13th CPU and 16GB ram. (Used Qwen3 -8b) 

Operating System
* Recommended: Windows
* Not tested: macOS, Linux

You are now ready to run the project!





## How to use it

#### Using saved character
1. Enable .venv
```sh
project path> .\.venv\Scripts\Activate
```

2. Start the code
```sh
(project root path) python delta_me13_py.py
```

3. Choose a language you want to use.
```sh
What language do you want to use? Be careful about typos. I haven't made a validator for the language. (default: Korean) :
```

The output will look like this. It supports 50 languages. (Check README.md of paraphrase-multilingual-mpnet-base-v2 for language support) If you choose a language, the virtual persona will speak that language. And since I didn't make a validator yet, be careful with typos.

4. Choose a character
```sh
Character name: 
```
You can input the name of the character from here. If you type a character that is already in the ```Character/CharacterSave``` file, It will start the llama.cpp local server and start the chat with the character. I put the test character named Argenti which is from HSR.

5. Exit the chat
You can type ```-/exit``` to end the chat. You MUST turn off the server after you finish it.

#### Generate new character
* *Method 1*: Make a character file by yourself.(**recommanded**)
You can make a character file manually in the ```CharacterSave``` folder.
The folder should look like this:
```sh
Character name folder(ex. Andrew)
    backstory
    GeneralDB
    VectorDB
    Character name.json(ex. Andrew.json)
```
You must put GeneralDB, VectorDB, and Character name.json.

And for .json file, the format will be like:
```sh
{
    "name": "",
    "sex": "",
    "MBTI": "",
    "age": "",
    "back_story": "",
    "constraints": [],
    "safety": [
        "",
        "",
        ""
    ]
}
```
    The character is made with these traits:
    * name: The character's name
    * sex: The character's gender. (It works well with classic male and female, but I haven't tested it with other genders. I will test it with various genders later.)
    * MBTI: This is the most important aspect of the character. Based on MBTI, AI will make a personality for the character.
    * Age: Age of the Character
    * back_story: Back story of the character. Be careful with the number of tokens. It is usually a long string.
    * constraints: Constraints of the character
    * safety: Safety of the character.




* *Method 2*: Make a character file in the code
1. Enter the new character's name
```sh
Character name: Jamal
Jamal seems not to be in the Character Save folder. Do you want to make a new character, Jamal? (Y : N) : Y
```
If you enter a new character's name at ```Character name:```, it will ask you to make a new character. If you enter Y, it will proceed to the next step. If you enter N, it will go back to ```Character name:```

2. Make a new character
```sh
Creating folder for character 'Jamal'...
Successfully created folder for 'Jamal'!

-----------------------------------------------------------------------
Now, please enter the character's detailed information.
Finish lists with an empty line or type END/DONE/QUIT/Q.
The example below shows the format you will be following.

Example:
{
    "name": "Kaelus",
    "sex": "Male",
    "MBTI": "INTP",
    "age": "Unknown (Records Lost)",
    "back_story": "I am Kaelus, the last librarian of the 'Starlight Archive,'...",
    "constraints": [
        "Your personality must be based on your MBTI.",
        "You must adhere to the role of 'Kaelus' until the end, not an AI.",
        ...
    ],
    "safety": [
        "Never ask for or record personal information.",
        "Politely refuse unethical or dangerous requests...",
        ...
    ]
}
-----------------------------------------------------------------------

Sex:
```
After you enter Y, it will automatically make a new character's folder in ```CharacterSave``` folder. Then the output will be like this. 

The character is made with these traits:
* name: The character's name
* sex: The character's gender. (It works well with classic male and female, but I haven't tested it with other genders. I will test it with various genders later.)
* MBTI: This is the most important aspect of the character. Based on MBTI, AI will make a personality for the character.
* Age: Age of the Character
* back_story: Back story of the character. Be careful with the number of tokens. It is usually a long string.
* constraints: Constraints of the character
* safety: Safety of the character.

If you want to see the example, you can translate argenti.json for reference.

### *Since this is a new feature for this project, it makes a lot of errors here.* 


#### Command
During the chat, you can adjust the value or check a character's memory with ```-/open command```.

Current commands are:
```sh
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
```


## User Sequence diagram

```mermaid
flowchart TD

A[Choose language between 50 languages] --> B[Choose character]
B --> C(Does character folder exist in CharacterSave folder?)
C -- No -->D[Character generation]
C -- Yes --> E[Read character info]
D --> F[Generate character class and other classes like CommandHandler, RequestHandler]
E --> F[Generate character class and other classes like CommandHandler, RequestHandler]
F --> G(Start local AI server using llama.cpp)
G -- No --> H[Program crashes]
G -- Yes --> J[Server successflly loaded]
J --> K(Is this user's first chat?)
K -- Yes -->L[Automatically input: introduce yourself]
K -- No -->M[Gets input from user]
M --> P[Request to AI local server]
L --> P[Request to AI local server]
P--> Q(Is language Korean?)
Q -- Yes --> R[Show output]
Q -- No --> S[Request to AI server again to translate output into selected language]
S --> R
R --> T(Does the user want to continue?)
T -- Yes --> K
T -- No -->U[End]
```

## License

This project is distributed under the MIT License. See the ```LICENSE``` file for details.


## Acknowledgments & Key Dependencies

* NVIDIA CUDA Toolkit — GPU computing platform and model. Version 12.9 is used here. 

    License: NVIDIA Software License Agreement.

* PyTorch — Deep learning framework for research to production.

    License: BSD-style.

* Hugging Face Transformers — Pretrained models for text/vision/audio.

    License: Apache 2.0.

* Sentence Transformers — State-of-the-art sentence/text/image embeddings.

    License: Apache 2.0.

* Faiss — Efficient similarity search and clustering for dense vectors.

    License: MIT.

* llama.cpp — The platform that actually runs LLM and opens the server.

    License: MIT.


