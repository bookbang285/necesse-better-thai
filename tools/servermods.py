"""ก๊อปมอดจาก Steam Workshop ไปให้ dedicated server ใช้ — ลำดับเดียวกับ client

เซิร์ฟ Necesse ไม่มี Workshop provider: อ่านเฉพาะ <datadir>/mods/*.jar + modlist.data (type FILE_MOD)
และตรวจ hash id+version ของมอดที่ไม่ใช่ clientside ตามลำดับโหลด → ลำดับต้องตรง client

py -m tools.servermods   (เรียกก่อนเปิดเซิร์ฟทุกครั้ง — บอทเรียกให้ตอน /start)
"""
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from tools.extract import parse_modinfo
from tools.paths import APPDATA_NECESSE, ROOT, WORKSHOP

SERVER_DATA = ROOT / "server-data"
SKIP = {"thaicommunity.thailanguage"}  # clientside + ไม่ได้อยู่ใน workshop ของเครื่องนี้
_BLOCK = re.compile(r"\{([^{}]*)\}")


@dataclass(frozen=True)
class Mod:
    id: str
    name: str
    enabled: bool


@dataclass
class SyncReport:
    copied: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


def parse_modlist(text: str) -> list[Mod]:
    out = []
    for block in _BLOCK.findall(text):
        info = parse_modinfo(block)
        if "id" in info:
            out.append(Mod(info["id"], info.get("name", info["id"]), info.get("enabled", "true") == "true"))
    return out


def render_modlist(mods: list[Mod]) -> str:
    blocks = [f"\t{{\n\t\tid = {m.id},\n\t\tname = {m.name},\n\t\ttype = FILE_MOD,\n\t\tenabled = {str(m.enabled).lower()}\n\t}}"
              for m in mods]
    return "{\n" + ",\n".join(blocks) + "\n}"


def _jar_id(jar: Path) -> tuple[str, str]:
    with zipfile.ZipFile(jar) as z:
        info = parse_modinfo(z.read("mod.info").decode("utf-8"))
    return info["id"], info.get("version", "")


def workshop_jars(workshop: Path) -> dict[str, Path]:
    found = {}
    for jar in sorted(workshop.glob("*/*.jar")):
        try:
            found[_jar_id(jar)[0]] = jar
        except (KeyError, zipfile.BadZipFile):
            continue
    return found


def sync(client_modlist: Path, workshop: Path, mods_dir: Path) -> SyncReport:
    report = SyncReport()
    wanted = [m for m in parse_modlist(client_modlist.read_text(encoding="utf-8")) if m.enabled and m.id not in SKIP]
    available = workshop_jars(workshop) if workshop.exists() else {}
    mods_dir.mkdir(parents=True, exist_ok=True)
    existing = {}
    for jar in mods_dir.glob("*.jar"):
        try:
            existing.setdefault(_jar_id(jar)[0], []).append(jar)
        except (KeyError, zipfile.BadZipFile):
            continue
    kept = []
    for m in wanted:
        src = available.get(m.id)
        if src is None:
            report.missing.append(m.id)
            continue
        olds = existing.get(m.id, [])
        same = [o for o in olds if o.name == src.name and o.stat().st_size == src.stat().st_size]
        if not same:
            for o in olds:
                o.unlink()
            shutil.copy2(src, mods_dir / src.name)
            report.copied.append(m.id)
            if olds:
                report.changed.append(m.id)
        kept.append(m)
    (mods_dir / "modlist.data").write_text(render_modlist(kept), encoding="utf-8")
    return report


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    r = sync(APPDATA_NECESSE / "mods" / "modlist.data", WORKSHOP, SERVER_DATA / "mods")
    print(f"ก๊อปใหม่: {', '.join(r.copied) or '-'} · อัปเดต: {', '.join(r.changed) or '-'} · หาไม่เจอ: {', '.join(r.missing) or '-'}")
    sys.exit(1 if r.missing else 0)


if __name__ == "__main__":
    main()
