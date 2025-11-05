import sys, time, webbrowser
import subprocess
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent

# is it windows? --> if it is windows = True
is_windows = sys.platform == "win32"
# path
base_path = get_base_path()
backend_dir = base_path / "BackEnd"
frontend_dir = base_path / "FrontEnd"
server_path = backend_dir / "delta_me13_server.py"

if not server_path.exists():
    sys.exit(f"Failed to find backend server: {server_path}")

# os check
venv_path = base_path / ".venv"

if is_windows:
    #windows
    python_exe = venv_path / "Scripts" / "python.exe"
    npm_cmd = "npm.cmd"

else:
    # Linux, MacOS
    python_exe = venv_path / "bin" / "python"
    npm_cmd = "npm"

if not python_exe.exists():
    sys.exit(f"Failed to find Python executable in virtual environment: {python_exe}")

# build a command line for each os
cmd_back_end = [
    str(python_exe),  # Path -> str
    "-m", "uvicorn",
    "delta_me13_server:app",
    "--reload"
]

cmd_front_end = [
    npm_cmd,
    "run",
    "dev"
]


print("Starting BackEnd and FrontEnd servers...")

back_process = subprocess.Popen(
    cmd_back_end,
    cwd=backend_dir
)
front_process = subprocess.Popen(
    cmd_front_end,
    cwd=frontend_dir,
    shell=is_windows  
)

print("Waiting for servers to start...")
time.sleep(5)

webbrowser.open("http://localhost:5173")
webbrowser.open("http://127.0.0.1:8000/docs")
print("Servers launched and browser opened.")
