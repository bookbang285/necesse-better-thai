"""ตรวจคุณภาพคำแปลใน data/

py -m tools.check                      ตรวจทุกไฟล์
py -m tools.check --files a.json b.json
py -m tools.check --release            todo/stale = error
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tools import store
from tools.checkdata import GENDERED, MISSPELL, NPC_CATEGORIES, STATUSES
from tools.paths import DATA

TOKEN_RE = re.compile(r"<[A-Za-z0-9_.]+>|\[(?:input|item|mob)=[^\]]*\]|§#[0-9A-Fa-f]{6}|§.|\\n|\[newline\]|:[a-z_]+:")
NEWLINES = ("\\n", "[newline]")


@dataclass
class Issue:
    level: str
    file: str
    key: str
    rule: str
    msg: str


def tokens(s: str) -> Counter:
    return Counter(TOKEN_RE.findall(s))


def _bad_chars(s: str) -> list[str]:
    return [f"U+{ord(c):04X}" for c in s if unicodedata.category(c) in ("Cc", "Cf")]


def check_row(row: dict, category: str, glossary: list[dict], allow: set[str], release: bool) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    en, th, status = row["en"], row["th"], row["status"]
    if status not in STATUSES:
        out.append(("error", "status", f"status ไม่รู้จัก: {status}"))
    if status in ("todo", "stale") and release:
        out.append(("error", "unfinished", f"ยังเป็น {status}"))
    if status == "todo":
        return out
    if not th:
        out.append(("error", "empty", "th ว่าง"))
        return out
    bad = _bad_chars(th)
    if bad:
        out.append(("error", "chars", "อักขระควบคุม/มองไม่เห็น: " + " ".join(bad)))
    if th != th.strip():
        out.append(("error", "whitespace", "มีช่องว่างหัว/ท้าย"))
    te, tt = tokens(en), tokens(th)
    te_main = Counter({k: v for k, v in te.items() if k not in NEWLINES})
    tt_main = Counter({k: v for k, v in tt.items() if k not in NEWLINES})
    if te_main != tt_main:
        out.append(("error", "tokens", f"ตัวแปร/โค้ดไม่ตรง: en={dict(te_main)} th={dict(tt_main)}"))
    if sum(te[k] for k in NEWLINES) != sum(tt[k] for k in NEWLINES):
        out.append(("warn", "newline", "จำนวนขึ้นบรรทัดต่างจากต้นฉบับ"))
    en_text = TOKEN_RE.sub(" ", en)  # <mob> [item=x] ไม่ใช่คำศัพท์
    for term in glossary:
        if term.get("approved") and re.search(rf"\b{re.escape(term['en'])}(?:e?s)?\b", en_text, re.I) and term["th"] not in th:
            out.append(("warn", "glossary", f"'{term['en']}' ควรใช้ '{term['th']}'"))
    for wrong, right in MISSPELL.items():
        if wrong in th:
            out.append(("warn", "spelling", f"'{wrong}' → '{right}'"))
    if category in NPC_CATEGORIES and f"{category}.{row['key']}" not in allow:
        found = [w for w in GENDERED if w in th]
        if found:
            out.append(("warn", "gender", "คำตามเพศในบทพูด NPC: " + ", ".join(found)))
    if th == en and status != "same" and re.search(r"[A-Za-z]", en):
        out.append(("warn", "same", "เหมือนภาษาอังกฤษ — ถ้าตั้งใจให้ใช้ status same"))
    if category == "ui" and len(en) >= 4 and len(th) > 2 * len(en) + 4:
        out.append(("warn", "length", f"ยาว {len(th)} ตัว vs en {len(en)} — อาจล้นกรอบ"))
    return out


def check_collisions(docs: list[tuple[Path, dict]]) -> list[Issue]:
    seen: dict[tuple[str, str], tuple[str, str]] = {}
    out: list[Issue] = []
    for path, doc in docs:
        for r in doc["entries"]:
            if not r["th"]:
                continue
            k = (doc["category"], r["key"])
            if k in seen and seen[k][1] != r["th"]:
                out.append(Issue("error", str(path), r["key"], "collision",
                                 f"key ซ้ำกับ {seen[k][0]} แต่คำแปลต่างกัน"))
            seen.setdefault(k, (str(path), r["th"]))
    return out


def run(files: list[Path], release: bool) -> list[Issue]:
    glossary = json.loads((DATA / "glossary.json").read_text(encoding="utf-8"))
    allow = set(json.loads((DATA / "gender_allow.json").read_text(encoding="utf-8")))
    issues: list[Issue] = []
    for path in files:
        doc = store.load(path)
        for r in doc["entries"]:
            for level, rule, msg in check_row(r, doc["category"], glossary, allow, release):
                issues.append(Issue(level, str(path), r["key"], rule, msg))
    issues += check_collisions([(p, store.load(p)) for p in store.data_files()])
    return issues


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    release = "--release" in args
    if "--files" in args:
        files = [Path(a) for a in args[args.index("--files") + 1:] if not a.startswith("--")]
    else:
        files = store.data_files()
    issues = run(files, release)
    for i in issues:
        print(f"{i.level.upper():5} {i.rule:10} {i.file} :: {i.key} — {i.msg}")
    errors = sum(i.level == "error" for i in issues)
    print(f"\n{errors} error, {len(issues) - errors} warning ใน {len(files)} ไฟล์")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
