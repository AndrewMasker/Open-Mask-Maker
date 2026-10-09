from importlib.resources import files
import json
import os
from pathlib import Path
from pathvalidate import is_valid_filename
from platformdirs import user_config_dir
import tempfile
import warnings

JOB_EXTENSIONS = {"json" , "jsn"}

def get_user_jobs_dir() -> Path:
    path = Path(user_config_dir("mask_maker" , appauthor=False)) / "jobs"
    path.mkdir(parents=True , exist_ok=True)
    return path

def _load_dir(folder) -> dict[str , dict]:
    out = {}
    for f in folder.iterdir():
        name , dot , ext = f.name.rpartition(".")
        if not (dot and ext.lower() in JOB_EXTENSIONS):
            continue
        key = name.lower()
        if key in out:
            warnings.warn(f"Skipping {f.name} as another file is already named {key!r}.")
            continue
        try:
            out[name] = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError , UnicodeDecodeError) as e:
            warnings.warn(f"Skipping {f.name}: not valid JSON with error {e}.")
    return out

def get_default_jobs() -> dict[str , dict]:
    return _load_dir(files("mask_maker.jobs"))

def get_user_jobs() -> dict[str , dict]:
    return _load_dir(get_user_jobs_dir())

def get_all_jobs() -> dict[str , dict]:
    return get_default_jobs() | get_user_jobs() # User jobs override default jobs of the same name

def save_job(name: str , job: dict , overwrite: bool = False) -> Path:
    name = name.strip().lower()
    if not name.isascii() or not is_valid_filename(name) or name.endswith("."):
        raise ValueError(f"Invalid name: {name!r}.")

    folder = get_user_jobs_dir()
    path = folder / f"{name}.json"

    conflict_files = [
        f for f in folder.iterdir()
        if f.name.rpartition(".")[0].lower() == name
        and f.name.rpartition(".")[2].lower() in JOB_EXTENSIONS
    ]
    if conflict_files and not overwrite:
        raise FileExistsError(f"A job named {name} already exists in {folder}.")
       
    text = json.dumps(job , indent=2)
    fd , tmp = tempfile.mkstemp(dir = folder , suffix = ".tmp")
    try:
        with os.fdopen(fd , "w" , encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp , path)
    except BaseException:
        os.unlink(tmp)
        raise

    # Catch the conflict files that made it through the replace.
    for old in conflict_files:
        if old.exists() and not os.path.samefile(old , path):
            os.unlink(old)
    
    return path