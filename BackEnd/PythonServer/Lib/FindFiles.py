from pathlib import Path

def FindFiles(file_type:str, root:Path):
    file_names_and_paths = {p.name: p for p in root.glob(f"*.{file_type}")}
    return file_names_and_paths