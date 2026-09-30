"""อ่าน/เขียนไฟล์คำแปลใน data/"""
import json
from pathlib import Path

from tools.paths import DATA


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def data_files(root: Path = DATA) -> list[Path]:
    return sorted((root / "game").glob("*.json")) + sorted((root / "mods").glob("*/*.json"))


def target_of(path: Path) -> str:
    parts = Path(path).parts
    return "game" if parts[-2] == "game" else parts[-2]
