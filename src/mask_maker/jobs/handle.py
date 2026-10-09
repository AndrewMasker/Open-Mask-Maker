import json
from importlib.resources import files
from pathlib import Path
from platformdirs import user_config_dir
from pathvalidate import is_valid_filename
import tempfile
import os

JOB_EXTENSIONS = {"json" , "jsn" , "JSON" , "JSN"}

def get_user_jobs_dir() -> Path:
    path = Path(user_config_dir("mask_maker" , appauthor=False)) / "jobs"
    path.mkdir(parents=True , exist_ok=True)
    return path

def _load_dir(folder) -> dict[str , dict]:
    out = {}
    for f in folder.iterdir():
        name , dot , ext = f.name.rartition(".")
        if dot and ext in JOB_EXTENSIONS:
            out[name] = json.loads(f.read_text(encoding="utf-8"))
    return out

def get_default_jobs() -> dict[str , dict]:
    return _load_dir(files("mask_maker.jobs"))

def get_user_jobs() -> dict[str , dict]:
    return _load_dir(get_user_jobs_dir())

def get_all_jobs() -> dict[str , dict]:
    return get_default_jobs() | get_user_jobs() # User jobs override default jobs of the same name

def save_job(name: str , job: dict , overwrite: bool = False) -> Path:
    name = name.strip().lower()
    if not is_valid_filename(name) or name.endswith("."):
        raise ValueError(f"Invalid name: {name!r}.")

    folder = get_user_jobs_dir()
    path = folder / name / ".json"

    existing = {f.name.rpartition(".")[0] for f in folder.iterdir() if f.name.rpartition(".")[2] in JOB_EXTENSIONS}
    if name in {e.lower() for e in existing}:
        if not overwrite:
            raise FileExistsError(f"The name {name} already exists in {folder}. Names and extenstions are saved as lowercase.")
        if overwrite:
            name_idx = [e.lower() for e in existing].index(name)
            file_name_to_del = existing[name_idx]

    text = json.dumps(job , indent=2)
    fd , tmp = tempfile.mkstemp(dir = folder , suffix = ".tmp")
    try:
        with os.fdopen(fd , "w" , encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp , path)
    except BaseException:
        os.unlink(tmp)
        raise
    return path