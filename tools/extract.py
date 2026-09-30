"""ดึง en.lang/th.lang ของเกมและมอด → data/**.json โดยไม่ทับงานแปลเดิม

py -m tools.extract
"""
import json
import re
import sys
import zipfile
from pathlib import Path

from tools import langfile, store
from tools.langfile import Entry
from tools.paths import DATA, GAME_LOCALE, WORKSHOP

SKIP_CATEGORIES = {"lang"}


def official_value(entry: Entry | None) -> str:
    if entry is None or entry.flag == "missing":
        return ""
    return entry.value


def merge(doc: dict | None, category: str, en: list[tuple[str, str]], official: dict[str, str]) -> dict:
    old = {r["key"]: r for r in (doc or {}).get("entries", [])}
    old.update({r["key"]: r for r in (doc or {}).get("removed", [])})
    entries = []
    for key, en_value in en:
        row = old.pop(key, None)
        if row is None:
            row = {"key": key, "en": en_value, "official": "", "th": "", "status": "todo", "note": ""}
        elif row["en"] != en_value:
            if row["status"] != "todo":
                row["en_prev"] = row["en"]
                row["status"] = "stale"
            row["en"] = en_value
        new_official = official.get(key, "")
        if row["status"] == "kept" and new_official and new_official != row["official"]:
            row["th"] = new_official  # เกมแก้คำแปลทางการ → ตามของใหม่ ไม่งั้น build จะเอาของเก่าไปทับ
        row["official"] = new_official
        entries.append(row)
    return {"category": category, "entries": entries, "removed": list(old.values())}


def parse_modinfo(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^\s*(\w+)\s*=\s*(.*?),?\s*$", text, re.M)}


def read_mod_jar(jar: Path) -> tuple[str, str | None, str | None]:
    with zipfile.ZipFile(jar) as z:
        names = set(z.namelist())
        info = parse_modinfo(z.read("mod.info").decode("utf-8"))

        def text(name):
            return z.read(name).decode("utf-8") if name in names else None
        return info["id"], text("resources/locale/en.lang"), text("resources/locale/th.lang")


def extract_target(out_dir: Path, en_text: str, th_text: str | None) -> tuple[int, int]:
    en_entries = langfile.parse(en_text)
    th_map = langfile.to_map(langfile.parse(th_text or ""))
    rows = todo = 0
    for category in langfile.categories(en_entries):
        if category in SKIP_CATEGORIES:
            continue
        en_map = {e.key: e.value for e in en_entries if e.category == category}
        official = {k: official_value(th_map.get((category, k))) for k in en_map}
        path = out_dir / f"{category}.json"
        doc = merge(store.load(path) if path.exists() else None, category, list(en_map.items()), official)
        store.save(path, doc)
        rows += len(doc["entries"])
        todo += sum(r["status"] in ("todo", "stale") for r in doc["entries"])
    return rows, todo


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    source = DATA / "source"
    source.mkdir(parents=True, exist_ok=True)
    en = (GAME_LOCALE / "en.lang").read_text(encoding="utf-8")
    th = (GAME_LOCALE / "th.lang").read_text(encoding="utf-8")
    (source / "game-en.lang").write_text(en, encoding="utf-8")
    (source / "game-th.lang").write_text(th, encoding="utf-8")
    print("game: %d แถว, ต้องทำ %d" % extract_target(DATA / "game", en, th))

    for wid in json.loads((DATA / "mods.json").read_text(encoding="utf-8"))["workshop_ids"]:
        jars = sorted((WORKSHOP / wid).glob("*.jar"))
        if not jars:
            print(f"{wid}: ไม่พบ jar (ยังไม่ได้ subscribe?) — ข้าม")
            continue
        modid, en_m, th_m = read_mod_jar(jars[-1])
        if en_m is None:
            print(f"{modid}: ไม่มี en.lang — ไม่มีข้อความให้แปล")
            continue
        (source / f"{modid}-en.lang").write_text(en_m, encoding="utf-8")
        if th_m is not None:
            (source / f"{modid}-th.lang").write_text(th_m, encoding="utf-8")
        print(f"{modid}: %d แถว, ต้องทำ %d" % extract_target(DATA / "mods" / modid, en_m, th_m))


if __name__ == "__main__":
    main()
