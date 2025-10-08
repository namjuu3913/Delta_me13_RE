import sys, time, webbrowser, os
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent

base_path = get_base_path()
server_path = base_path / "BackEnd" / "delta_me13_server.py"

if not server_path.exists():
    sys.exit(f"Failed to find backend server: {server_path}")

backend_dir = base_path / "BackEnd"
frontend_dir = base_path / "FrontEnd"

python_exe_path = base_path / ".venv" / "Scripts" / "python.exe"

if not python_exe_path.exists():
    sys.exit(f"Failed to find Python executable in virtual environment: {python_exe_path}")

cmd_back_end = (
    f'start "BackEnd Server" /D "{backend_dir}" '
    f'"{python_exe_path}" -m uvicorn delta_me13_server:app --reload'
)


cmd_front_end = f'start "FrontEnd" /D "{frontend_dir}" cmd /k "npm run dev"'

print("Starting BackEnd and FrontEnd servers...")
os.system(cmd_back_end)
os.system(cmd_front_end)

print("Waiting for servers to start...")
time.sleep(5)

webbrowser.open("http://localhost:5173")
webbrowser.open("http://127.0.0.1:8000/docs")
print("Servers launched and browser opened.")
