"""แบ่งไฟล์ data เป็นกลุ่มงานขนาดใกล้กันให้ agent แปลขนาน (ไม่ทับกัน)

py -m tools.split 7   → build/split.json
"""
import json
import sys
from pathlib import Path

from tools import store
from tools.paths import BUILD


def plan(files: list[Path], n: int) -> list[list[tuple[str, int, int]]]:
    sizes = [(str(p), len(store.load(p)["entries"])) for p in files]
    total = sum(s for _, s in sizes)
    target = max(1, -(-total // n))
    chunks: list[tuple[str, int, int]] = []
    for path, size in sizes:
        for start in range(0, size, target):
            chunks.append((path, start, min(size, start + target)))
    chunks.sort(key=lambda c: c[2] - c[1], reverse=True)
    groups: list[list[tuple[str, int, int]]] = [[] for _ in range(n)]
    loads = [0] * n
    for c in chunks:
        i = loads.index(min(loads))
        groups[i].append(c)
        loads[i] += c[2] - c[1]
    return groups


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    groups = plan(store.data_files(), n)
    BUILD.mkdir(exist_ok=True)
    (BUILD / "split.json").write_text(json.dumps(groups, ensure_ascii=False, indent=1), encoding="utf-8")
    for i, g in enumerate(groups, 1):
        print(f"กลุ่ม {i}: {sum(e - s for _, s, e in g)} แถว — "
              + ", ".join(f"{Path(p).parent.name}/{Path(p).stem}[{s}:{e}]" for p, s, e in g))


if __name__ == "__main__":
    main()
