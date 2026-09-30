"""เขียนคำแปลลง data/*.json อย่างปลอดภัยเมื่อหลาย agent แก้ไฟล์เดียวกันพร้อมกัน

py -m tools.apply patch.json [patch2.json ...]
patch = {"file": "data/game/ui.json", "rows": {"<key>": {"th": "...", "status": "new", "note": ""}}}
- ล็อกไฟล์ระหว่าง load → แก้ → save (กันงานทับกัน)
- แก้ได้แค่ th / status / note · key ต้องมีอยู่จริง · status ต้องถูกต้อง
"""
import json
import msvcrt
import sys
import time
from contextlib import contextmanager
from pathlib import Path

from tools import store
from tools.checkdata import STATUSES

FIELDS = ("th", "status", "note")


@contextmanager
def _locked(path: Path):
    lock = path.with_suffix(path.suffix + ".lock")
    with open(lock, "a+b") as f:
        for _ in range(600):
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                time.sleep(0.05)
        else:
            raise TimeoutError(f"ล็อก {path} ไม่ได้")
        try:
            yield
        finally:
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)


def apply(path: Path, rows: dict[str, dict]) -> int:
    with _locked(path):
        doc = store.load(path)
        index = {r["key"]: r for r in doc["entries"]}
        for key, change in rows.items():
            if key not in index:
                raise ValueError(f"{path}: ไม่มี key {key}")
            if change.get("status", index[key]["status"]) not in STATUSES:
                raise ValueError(f"{path}: {key} status ไม่ถูกต้อง: {change.get('status')}")
        for key, change in rows.items():
            for field in FIELDS:
                if field in change:
                    index[key][field] = change[field]
        store.save(path, doc)
    return len(rows)


def main(argv: list[str] | None = None) -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    for p in argv if argv is not None else sys.argv[1:]:
        patch = json.loads(Path(p).read_text(encoding="utf-8"))
        n = apply(Path(patch["file"]), patch["rows"])
        print(f"{patch['file']}: เขียน {n} แถว")


if __name__ == "__main__":
    main()
