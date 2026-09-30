"""ดึงศัพท์ผู้สมัครสำหรับร่างคลังศัพท์

py -m tools.glossary  → build/glossary_candidates.json
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from tools import store
from tools.paths import BUILD

NAME_CATEGORIES = {"item", "mob", "biome", "buff", "object", "tile", "incursion", "settlement", "jobs", "tech", "expedition"}
TEXT_CATEGORIES = {"ui", "objectives", "itemtooltip", "quests", "settlement"}
WORD_RE = re.compile(r"\b[A-Z][a-z]{3,}\b")


def candidates(files: list[Path]) -> list[dict]:
    variants: dict[str, Counter] = defaultdict(Counter)
    cats: dict[str, str] = {}
    words: Counter = Counter()
    for path in files:
        doc = store.load(path)
        cat = doc["category"]
        for r in doc["entries"]:
            if cat in NAME_CATEGORIES and len(r["en"]) <= 40 and "<" not in r["en"]:
                cats.setdefault(r["en"], cat)
                if r["official"]:
                    variants[r["en"]][r["official"]] += 1
            if cat in TEXT_CATEGORIES:
                words.update(WORD_RE.findall(r["en"]))
    for w, n in words.items():
        if n >= 5:
            cats.setdefault(w, "text")
    return [{"en": en, "category": cats[en], "count": words.get(en, 0) + sum(variants[en].values()),
             "official_variants": dict(variants[en])} for en in sorted(cats)]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    out = candidates(store.data_files())
    BUILD.mkdir(exist_ok=True)
    (BUILD / "glossary_candidates.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out)} คำ → build/glossary_candidates.json")


if __name__ == "__main__":
    main()
