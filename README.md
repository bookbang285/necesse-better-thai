# necesse-better-thai

มอดภาษาไทยฉบับสมบูรณ์สำหรับ **Necesse** — แปลครบทั้งเกม + มอดยอดนิยม และฟอนต์ไทยที่อ่านง่าย (สระ/วรรณยุกต์ไม่หาย)

- ติดตั้ง: Subscribe บน Steam Workshop แล้วเลือกภาษาไทยในเกม (มอด clientside — ไม่ต้องลงที่เซิร์ฟ)
- เกมเวอร์ชัน: 1.3.3 · มอดเวอร์ชัน: 1.0.0

## มีอะไรบ้าง

| | |
|---|---|
| คำแปล | 8,167 บรรทัด (เกม 7,524 + มอด 643) — เติมที่ขาด ~1,500 บรรทัด และรีวิวคำแปลทางการเดิมทุกบรรทัด |
| คลังศัพท์ | `data/glossary.json` ~300 คำ ให้ชื่อไอเทม/มอนสเตอร์/บอส/ชีวนิเวศเรียกเหมือนกันทั้งเกม |
| ชื่อไอเทม/มอนสเตอร์ | มีภาษาอังกฤษในวงเล็บ เช่น "แท่งเหล็ก (Iron Bar)" ไว้ค้นใน Google/Wiki |
| ฟอนต์ | Prompt (Cadson Demak, SIL OFL 1.1) แทรกเข้า fallback chain ของเกม |
| จัดสระ | เกมวาดตัวอักษรด้วย STB (ไม่มี GPOS) → สร้างรูปวรรณยุกต์ยกสูง/เยื้องซ้ายไว้ใน PUA ของฟอนต์ แล้วสลับตอนโหลดคำแปล |
| มอดที่แปล | Aphorea, Quick Recipes Menu, More Trinket Slots, A Better Torch, Boss Fight Summary, Increased Stack Size |

## โครงสร้าง

```
data/game/<category>.json          คำแปลตัวเกม (key, en, official, th, status, note)
data/mods/<modid>/<category>.json  คำแปลของแต่ละมอด
data/glossary.json                 คลังศัพท์
docs/style-guide.md                คู่มือสไตล์การแปล — อ่านก่อนแก้คำแปล
mod/src/thailanguage/*.java        โค้ดมอด (แทรกฟอนต์, จัดสระ)
mod/fonts/                         ฟอนต์ + สัญญาอนุญาต
tools/                             เครื่องมือ Python (py -m tools.<ชื่อ>)
tests/                             unittest
```

`status` ของแต่ละแถว: `kept` ใช้คำแปลทางการ · `fixed` แก้คำแปลทางการ (ดูเหตุผลใน `note`) · `new` แปลใหม่ · `same` ตั้งใจเป็นอังกฤษ · `todo`/`stale` ยังไม่ได้แปล/ต้นฉบับเปลี่ยน

## ใช้เครื่องมือ (Windows, Python 3.12+, JDK 17)

```
py -m tools.extract        ดึงข้อความจากเกม + มอด (หลังเกมอัปเดตก็รันใหม่ — ไม่ทับงานแปล)
py -m tools.check          ตรวจตัวแปร/โค้ดสี/คลังศัพท์/คำสะกดผิด (--release = ห้ามเหลือ todo)
py -m tools.review         หน้า HTML ตาราง อังกฤษ/ทางการ/ของเรา (build/review.html)
py -m tools.build          รวมเป็น jar + ติดตั้งลง %APPDATA%\Necesse\mods
py -m unittest discover -s tests -t .
```

path ของเกม/JDK อยู่ใน `tools/paths.py` · `pip install fonttools pillow` สำหรับทำฟอนต์และภาพตัวอย่าง

## เมื่อเกมอัปเดต

1. `py -m tools.extract` → แถวใหม่เป็น `todo`, แถวที่ต้นฉบับเปลี่ยนเป็น `stale`
2. แปลแถวเหล่านั้น → `py -m tools.check --release`
3. แก้ `gameVersion`/`version` ใน `mod/build.json` → `py -m tools.build` → อัปโหลดเวอร์ชันใหม่

## เครดิต / สัญญาอนุญาต

- คำแปลภาษาไทยทางการของเกม (ฐาน): Himeda Fukusa, Miraisa Gaizaku, Mitsuaki Tora
- ฟอนต์ Prompt © Cadson Demak — SIL Open Font License 1.1 (`mod/fonts/OFL-Prompt.txt`)
- Necesse © Fair Games · ข้อความต้นฉบับภาษาอังกฤษในไฟล์ `data/` เป็นของเกม ใช้เพื่อการแปลเท่านั้น
