# Server/startServer.py
import subprocess, sys, time, json, http.client, socket, threading
from pathlib import Path
import Config.config as cfg

#mostly written by vibe coding

#load config
BIN:Path        = Path(cfg.LLM_SERVER_CONFIG["BIN"])
# if it is Linux/MacOS, it will trim .exe <--- very dangerous
if sys.platform != "win32":
    BIN = BIN.with_suffix('')

MODEL:Path      = Path(cfg.LLM_SERVER_CONFIG["MODEL"])
ALIAS:str       = cfg.LLM_SERVER_CONFIG["ALIAS"]
HOST:str        = cfg.LLM_SERVER_CONFIG["HOST"] 
PORT:int        = cfg.LLM_SERVER_CONFIG["PORT"]
NGL:int         = cfg.LLM_SERVER_CONFIG["NGL"]
CTX:int         = cfg.LLM_SERVER_CONFIG["CTX_SIZE"]
VERBOSE:bool    = cfg.LLM_SERVER_CONFIG["VERBOSE"]
BATCH_SIZE:int  = cfg.LLM_SERVER_CONFIG["BATCH_SIZE"]
FLASH_ATTN:bool = cfg.LLM_SERVER_CONFIG["FLASH_ATTN"]


def startLlamaCppServer(mode: str = "new_console", chat_template: str | None = None)-> subprocess.Popen:
    if not BIN.exists():
        sys.exit(f"llama-server.exe not found: {BIN}")

    if not MODEL.exists():
        sys.exit(f"GGUF not found: {MODEL}")

    cmd = [
        str(BIN),
        "--model",          str(MODEL),
        "--alias",          ALIAS,
        "--host",           HOST, 
        "--port",           str(PORT),
        "--n-gpu-layers",   str(NGL),
        "--ctx-size",       str(CTX),
        "--batch-size",     str(BATCH_SIZE)
    ]

    if VERBOSE:
        cmd.append("--verbose")
    if FLASH_ATTN:
        cmd.extend(["--flash-attn", "on"])

    if chat_template:
        cmd.extend(["--chat-template", chat_template])


    shown = " ".join(f'"{a}"' if " " in str(a) else str(a) for a in cmd)
    print("Launching:", shown)


    proc = None

    if mode == "new_console" and sys.platform == "win32":
        print("Starting server in a new console window...")
        debug_cmd = ["cmd", "/k"] + cmd
        proc = subprocess.Popen(
            debug_cmd,
            cwd=str(BIN.parent),
            creationflags=subprocess.CREATE_NEW_CONSOLE  #start the process at the new console
        )
    else:
        if mode == "new_console":
            print(f"Warning: 'new_console' mode is only supported on Windows. Falling back to default mode.")
            
        proc = subprocess.Popen(
            cmd,
            cwd=str(BIN.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        log_thread = threading.Thread(target=log_server_output, args=(proc,))
        log_thread.daemon = True
        log_thread.start()

    print(f"llama.cpp server PID={proc.pid} → http://{HOST}:{PORT}/v1")

    return proc

def wait_until_ready(timeout: int = 300, require_model: bool = True, debug: bool = True) -> None:
    deadline = time.time() + timeout
    paths = ["/v1/models", "/health", "/healthz"]
    backoff = 0.5
    last_status = None
    last_err = None

    while time.time() < deadline:
        for path in paths:
            try:
                conn = http.client.HTTPConnection(HOST, PORT, timeout=2)
                conn.request("GET", path)
                resp = conn.getresponse()
                body = resp.read()
                status = resp.status
                conn.close()

                if debug and status != last_status:
                    print(f"[wait] {path} -> {status}")
                    last_status = status

                if status == 200:
                    if path == "/v1/models" and require_model:
                        try:
                            data = json.loads(body.decode("utf-8", "ignore"))
                            if data.get("data"):
                                if debug: print(f"[wait] ready: {len(data['data'])} model(s) loaded")
                                return
                            else:
                                continue
                        except Exception:
                            if debug: print("[wait] ready (models 200, json parse skipped)")
                            return
                    else:
                        if debug: print("[wait] ready (health 200)")
                        return
            except (ConnectionRefusedError, socket.timeout, OSError) as e:
                last_err = e
            except Exception as e:
                last_err = e

        time.sleep(backoff)
        backoff = min(backoff * 1.3, 2.0)

    raise TimeoutError(
        f"Server not ready at http://{HOST}:{PORT} within {timeout}s; last_err={last_err}"
    )

def wait_inference_ready(model_id: str,timeout: int = 180, 
                         use_chat: bool = True, debug: bool = True) -> None:

    end = time.time() + timeout
    backoff = 0.5

    while time.time() < end:
        try:
            conn = http.client.HTTPConnection(HOST, PORT, timeout=5)
            if use_chat:
                path = "/v1/chat/completions"
                payload = {
                    "model": model_id,
                    "messages": [
                        {"role":"system","content":"you are a concise assistant"},
                        {"role":"user","content":"ping"}
                    ],
                    "max_tokens": 1,
                    "temperature": 0.0,
                    "stream": False
                }
            else:
                path = "/v1/completions"
                payload = {
                    "model": model_id,
                    "prompt": "User: ping\nAssistant:",
                    "max_tokens": 1,
                    "temperature": 0.0,
                    "stream": False
                }

            body = json.dumps(payload).encode("utf-8")
            conn.request("POST", path, body=body, headers={"Content-Type":"application/json"})
            resp = conn.getresponse()
            text = resp.read().decode("utf-8", "ignore")
            status = resp.status
            conn.close()

            if debug:
                print(f"[probe] {path} -> {status}")

            if status == 200:
                if debug: print("[probe] inference ready ✅")
                return True

            if debug and status == 400:
                print("[probe] 400 body:", text[:500])

        except (ConnectionRefusedError, socket.timeout, OSError) as e:
            if debug: print(f"[probe] conn err: {e}")

        time.sleep(backoff)
        backoff = min(backoff * 1.4, 2.0)

    raise TimeoutError("Inference endpoint not ready in time")

def get_model_ids() -> list[str]:
    conn = http.client.HTTPConnection(HOST, PORT, timeout=3)
    conn.request("GET", "/v1/models")
    resp = conn.getresponse()
    body = resp.read()
    conn.close()
    if resp.status != 200:
        return []
    try:
        data = json.loads(body.decode("utf-8", "ignore"))
        return [m.get("id") for m in data.get("data", []) if m.get("id")]
    except Exception:
        return []

def log_server_output(proc: subprocess.Popen):
    if proc.stdout:
        for line in iter(proc.stdout.readline, ''):
            print(f"[LLAMA SERVER]: {line.strip()}")

#
def startServer(mode = "new_console", chat_template="chatml") -> subprocess.Popen:
    controller: subprocess.Popen | None = None
    try:
        #start the server
        controller = startLlamaCppServer(mode=mode, chat_template=chat_template)

        #wait for server
        print("\n--- Waiting for server to become ready... ---")
        wait_until_ready(timeout=300, require_model=True, debug=True)

        ids = get_model_ids()
        print("Server models:", ids)

        #wait for ai is fully loaded
        model_id = ALIAS if ALIAS in ids else (ids[0] if ids else ALIAS)
        wait_inference_ready(model_id, timeout=180, use_chat=True, debug=True)

        return controller 

    except TimeoutError as e:
        print(f"\n❌ Server failed to start or become ready: {e}")
        return None

    except KeyboardInterrupt:
        print("\nInterrupted by user. Shutting down server...")
        return None

    finally:
        if controller and controller.poll() is None:
            if isinstance(sys.exc_info()[1], (TimeoutError, KeyboardInterrupt)):
                controller.terminate()
                controller.wait()
                print("Server process terminated.")

