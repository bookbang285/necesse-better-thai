"""สร้าง checkpoint เป็นสำเนาโฟลเดอร์ตามวันที่-เวลา (โปรเจกต์นี้ไม่ใช้ git)"""
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from tools.paths import ROOT

CHECKPOINTS = ROOT / "checkpoints"
FOLDERS = ("data", "docs", "mod", "tools", "tests")


def _sanitize_label(label: str) -> str:
    label = re.sub(r"\.\.", "", label)
    return re.sub(r"[\\/]+", "_", label)


def make(label: str) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    dest = CHECKPOINTS / f"{stamp}_{_sanitize_label(label)}"
    dest.mkdir(parents=True, exist_ok=True)
    for name in FOLDERS:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, dest / name, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__"))
    return dest


if __name__ == "__main__":
    print(make(sys.argv[1] if len(sys.argv) > 1 else "manual"))
