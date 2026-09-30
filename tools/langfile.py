"""อ่าน/เขียนไฟล์ภาษาของ Necesse (.lang) ตามกติกาเดียวกับ Translation.loadLanguageFile ของเกม

- บรรทัดว่าง / ขึ้นต้น // = ข้าม
- [ชื่อ] = เปลี่ยน category (ชื่อซ้ำได้ — รวมเข้าของเดิม)
- key=value ตัดที่ = ตัวแรก · key อาจขึ้นต้น MISSING_TRANSLATION: / SAME_TRANSLATION:
- บรรทัดอื่นที่ไม่มี = ถูกข้าม
"""
from dataclasses import dataclass

MISSING = "MISSING_TRANSLATION:"
SAME = "SAME_TRANSLATION:"


@dataclass
class Entry:
    category: str
    key: str
    value: str
    flag: str | None


def parse(text: str) -> list[Entry]:
    text = text.lstrip("﻿")
    out: list[Entry] = []
    category = "null"
    for line in text.splitlines():
        if not line or line.startswith("//"):
            continue
        if line.startswith("[") and "]" in line:
            category = line[1:line.index("]")]
            continue
        eq = line.find("=")
        if eq == -1:
            continue
        key, value = line[:eq], line[eq + 1:]
        flag = None
        if key.startswith(MISSING):
            key, flag = key[len(MISSING):], "missing"
        elif key.startswith(SAME):
            key, flag = key[len(SAME):], "same"
        out.append(Entry(category, key, value, flag))
    return out


def to_map(entries: list[Entry]) -> dict[tuple[str, str], Entry]:
    return {(e.category, e.key): e for e in entries}


def categories(entries: list[Entry]) -> list[str]:
    seen: dict[str, None] = {}
    for e in entries:
        seen.setdefault(e.category, None)
    return list(seen)


def dump(rows: list[tuple[str, str, str]], header: str = "") -> str:
    lines: list[str] = [header] if header else []
    current = None
    for category, key, value in rows:
        for part in (category, key, value):
            if "\n" in part or "\r" in part:
                raise ValueError(f"มีขึ้นบรรทัดจริงใน {category}.{key}")
        if "=" in key:
            raise ValueError(f"key มี = : {category}.{key}")
        if category != current:
            if lines:
                lines.append("")
            lines.append(f"[{category}]")
            current = category
        lines.append(f"{key}={value}")
    return "\n".join(lines) + "\n"
