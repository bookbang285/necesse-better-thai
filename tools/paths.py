"""จุดเดียวที่รู้ว่าไฟล์ต่าง ๆ อยู่ที่ไหน"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BUILD = ROOT / "build"
MOD_DIR = ROOT / "mod"

STEAM = Path(r"C:\Program Files (x86)\Steam\steamapps")
GAME = STEAM / "common" / "Necesse"
GAME_LOCALE = GAME / "locale"
GAME_JAR = GAME / "Necesse.jar"
GAME_LIB = GAME / "lib"
WORKSHOP = STEAM / "workshop" / "content" / "1169040"

APPDATA_NECESSE = Path(os.environ["APPDATA"]) / "Necesse"
LOCAL_MODS = APPDATA_NECESSE / "mods"

JDK_BIN = Path(r"C:\Program Files\Java\jdk-17\bin")
