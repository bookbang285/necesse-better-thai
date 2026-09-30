# necesse-better-thai

**English** · [ภาษาไทย](#ภาษาไทย)

A complete Thai language mod for **Necesse** — full translation of the game and popular mods, plus readable Thai fonts with correctly positioned vowels and tone marks.

- Install: subscribe on the Steam Workshop, then pick Thai in the game (client-side mod — servers don't need it)
- Game version: 1.3.3 · Mod version: 1.1.0

## Features

| | |
|---|---|
| Translation | 8,167 lines (game 7,524 + mods 643) — ~1,500 missing lines added and every official line reviewed |
| Glossary | `data/glossary.json`, 372 terms, so item/mob/boss/biome names are identical across the game |
| Item & mob names | English name in brackets, e.g. "แท่งเหล็ก (Iron Bar)", for wiki/Google lookups |
| Fonts | 6 to choose from (Prompt default, Kanit, Mitr, Sarabun, Niramit, Chakra Petch — SIL OFL 1.1), inserted into the game's font fallback chain |
| In-game settings | Settings → Language: switch Thai font + Thai text size 90–115% (applied instantly · stored in `cfg/mods/thaicommunity.thailanguage.cfg`) |
| Mark positioning | The game renders text with STB (no GPOS), so the mod adds raised/left-shifted tone-mark glyphs to the fonts' Private Use Area and swaps them in when translations load |
| Translated mods | Aphorea, Quick Recipes Menu, More Trinket Slots, A Better Torch, Boss Fight Summary, Increased Stack Size |

## Layout

```
data/game/<category>.json          game translations (key, en, official, th, status, note)
data/mods/<modid>/<category>.json  per-mod translations
data/glossary.json                 glossary
docs/style-guide.md                translation style guide (Thai) — read before editing
mod/src/thailanguage/*.java        mod code (font injection, mark positioning, settings menu)
mod/fonts/                         fonts + licences
tools/                             Python tools (py -m tools.<name>)
tests/                             unittest
```

Row `status`: `kept` official translation kept · `fixed` official translation corrected (reason in `note`) · `new` newly translated · `same` intentionally English · `todo`/`stale` not translated yet / English source changed

## Tools (Windows, Python 3.12+, JDK 17)

```
py -m tools.extract        pull strings from the game + mods (re-run after game updates — keeps translations)
py -m tools.check          check placeholders/colour codes/glossary/spelling (--release = no todo allowed)
py -m tools.review         HTML table English / official / ours (build/review.html)
py -m tools.build          build the jar + install into %APPDATA%\Necesse\mods
py -m unittest discover -s tests -t .
```

Game/JDK paths live in `tools/paths.py` · `pip install fonttools pillow` for font processing and previews

## When the game updates

1. `py -m tools.extract` → new rows become `todo`, rows whose English changed become `stale`
2. Translate those rows → `py -m tools.check --release`
3. Bump `gameVersion`/`version` in `mod/build.json` → `py -m tools.build` → upload the new version

## Credits / licences

- Official Thai translation of the game (base): Himeda Fukusa, Miraisa Gaizaku, Mitsuaki Tora
- Fonts Prompt, Kanit, Mitr, Sarabun, Niramit (Cadson Demak and contributors) and Chakra Petch — SIL Open Font License 1.1 (`mod/fonts/OFL-*.txt`) · modified by this mod to add positioned vowel/tone-mark glyphs in the PUA
- Necesse © Fair Games · the English source text in `data/` belongs to the game and is used for translation only

---

## ภาษาไทย

มอดภาษาไทยฉบับสมบูรณ์สำหรับ **Necesse** — แปลครบทั้งเกม + มอดยอดนิยม และฟอนต์ไทยที่อ่านง่าย (สระ/วรรณยุกต์ไม่หาย)

- ติดตั้ง: Subscribe บน Steam Workshop แล้วเลือกภาษาไทยในเกม (มอด clientside — ไม่ต้องลงที่เซิร์ฟ)
- เกมเวอร์ชัน: 1.3.3 · มอดเวอร์ชัน: 1.1.0

### มีอะไรบ้าง

| | |
|---|---|
| คำแปล | 8,167 บรรทัด (เกม 7,524 + มอด 643) — เติมที่ขาด ~1,500 บรรทัด และรีวิวคำแปลทางการเดิมทุกบรรทัด |
| คลังศัพท์ | `data/glossary.json` 372 คำ ให้ชื่อไอเทม/มอนสเตอร์/บอส/ชีวนิเวศเรียกเหมือนกันทั้งเกม |
| ชื่อไอเทม/มอนสเตอร์ | มีภาษาอังกฤษในวงเล็บ เช่น "แท่งเหล็ก (Iron Bar)" ไว้ค้นใน Google/Wiki |
| ฟอนต์ | 6 ตัวให้เลือก (Prompt ค่าเริ่มต้น, Kanit, Mitr, Sarabun, Niramit, Chakra Petch — SIL OFL 1.1) แทรกเข้า fallback chain ของเกม |
| ตั้งค่าในเกม | ตั้งค่า → ภาษา: ปุ่มเปลี่ยนฟอนต์ไทย + แถบขนาดตัวไทย 90–115% (เห็นผลทันที · เก็บใน `cfg/mods/thaicommunity.thailanguage.cfg`) |
| จัดสระ | เกมวาดตัวอักษรด้วย STB (ไม่มี GPOS) → สร้างรูปวรรณยุกต์ยกสูง/เยื้องซ้ายไว้ใน PUA ของฟอนต์ แล้วสลับตอนโหลดคำแปล |
| มอดที่แปล | Aphorea, Quick Recipes Menu, More Trinket Slots, A Better Torch, Boss Fight Summary, Increased Stack Size |

### โครงสร้าง

```
data/game/<category>.json          คำแปลตัวเกม (key, en, official, th, status, note)
data/mods/<modid>/<category>.json  คำแปลของแต่ละมอด
data/glossary.json                 คลังศัพท์
docs/style-guide.md                คู่มือสไตล์การแปล — อ่านก่อนแก้คำแปล
mod/src/thailanguage/*.java        โค้ดมอด (แทรกฟอนต์, จัดสระ, เมนูตั้งค่า)
mod/fonts/                         ฟอนต์ + สัญญาอนุญาต
tools/                             เครื่องมือ Python (py -m tools.<ชื่อ>)
tests/                             unittest
```

`status` ของแต่ละแถว: `kept` ใช้คำแปลทางการ · `fixed` แก้คำแปลทางการ (ดูเหตุผลใน `note`) · `new` แปลใหม่ · `same` ตั้งใจเป็นอังกฤษ · `todo`/`stale` ยังไม่ได้แปล/ต้นฉบับเปลี่ยน

### ใช้เครื่องมือ (Windows, Python 3.12+, JDK 17)

```
py -m tools.extract        ดึงข้อความจากเกม + มอด (หลังเกมอัปเดตก็รันใหม่ — ไม่ทับงานแปล)
py -m tools.check          ตรวจตัวแปร/โค้ดสี/คลังศัพท์/คำสะกดผิด (--release = ห้ามเหลือ todo)
py -m tools.review         หน้า HTML ตาราง อังกฤษ/ทางการ/ของเรา (build/review.html)
py -m tools.build          รวมเป็น jar + ติดตั้งลง %APPDATA%\Necesse\mods
py -m unittest discover -s tests -t .
```

path ของเกม/JDK อยู่ใน `tools/paths.py` · `pip install fonttools pillow` สำหรับทำฟอนต์และภาพตัวอย่าง

### เมื่อเกมอัปเดต

1. `py -m tools.extract` → แถวใหม่เป็น `todo`, แถวที่ต้นฉบับเปลี่ยนเป็น `stale`
2. แปลแถวเหล่านั้น → `py -m tools.check --release`
3. แก้ `gameVersion`/`version` ใน `mod/build.json` → `py -m tools.build` → อัปโหลดเวอร์ชันใหม่

### เครดิต / สัญญาอนุญาต

- คำแปลภาษาไทยทางการของเกม (ฐาน): Himeda Fukusa, Miraisa Gaizaku, Mitsuaki Tora
- ฟอนต์ Prompt, Kanit, Mitr, Sarabun, Niramit (Cadson Demak และผู้ร่วมพัฒนา), Chakra Petch — SIL Open Font License 1.1 (`mod/fonts/OFL-*.txt`) · มอดแก้ไขฟอนต์โดยเพิ่มรูปสระ/วรรณยุกต์ใน PUA
- Necesse © Fair Games · ข้อความต้นฉบับภาษาอังกฤษในไฟล์ `data/` เป็นของเกม ใช้เพื่อการแปลเท่านั้น
