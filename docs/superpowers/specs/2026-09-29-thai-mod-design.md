# มอดภาษาไทย Necesse — Design

วันที่: 2026-09-29 · สถานะ: รอผู้ใช้รีวิว
โปรเจกต์ย่อยที่ 1 จาก 3 (มอดภาษา → เซิร์ฟ → Discord bot) — เซิร์ฟ/บอทมี spec แยก

## เป้าหมาย

มอด Steam Workshop สาธารณะ ตัวเดียว ให้คนไทยกด Subscribe แล้วได้:

1. คำแปลไทยครบทุก key ของตัวเกม — เติม key ที่ขาด (~1,585) **และรีวิวคำแปลทางการเดิมทุกบรรทัด**
2. คำแปลไทยของมอดที่ผู้ใช้เล่นอยู่ (Aphorea, ABetterTorch, BossFightSummary, ExtendedRange, QuickRecipesMenu, OreExcavator, IncreasedStackSize, MoreTrinketSlots — ตัวที่มีข้อความให้แปล)
3. ฟอนต์ไทยที่อ่านง่าย แทน Code2000

**ความสำเร็จ** = เปิดเกมภาษาไทย + มอดนี้ → ไม่เห็นภาษาอังกฤษค้าง (ยกเว้นชื่อเฉพาะที่ตั้งใจทับศัพท์) · ไม่มีข้อความพัง (ตัวแปร/สี/ขึ้นบรรทัด) · ศัพท์เดียวกันแปลเหมือนกันทั้งเกม · ตัวไทยอ่านง่ายกว่าเดิมชัดเจนในสายตาผู้ใช้

## สิ่งที่ผู้ใช้ตัดสินใจแล้ว

| เรื่อง | ตัดสินใจ |
|---|---|
| การแจก | Workshop สาธารณะ · `clientside = true` (คนไม่ลงเข้าเซิร์ฟเดียวกันได้ เซิร์ฟไม่ต้องลง) |
| โครงสร้าง | มอดเดียวครบ (คำแปล + ฟอนต์ + โค้ด Java แทรกฟอนต์) |
| ขอบเขตแปล | ตัวเกม + มอดที่ผู้ใช้เล่นอยู่ |
| คำแปลเดิม | รีวิวทุกบรรทัด |
| ผู้ใช้ตรวจ | คลังศัพท์ (อนุมัติก่อนแปล) + ไล่อ่านหมวดบทพูด NPC และ objectives · ที่เหลือพึ่งชุดตรวจอัตโนมัติ + ลองเล่น |
| ภาษาพูด NPC | ภาษากลาง ไม่มีคำลงท้ายตามเพศ · ใช้ครับ/ค่ะ เฉพาะ key ที่ตรวจโค้ดแล้วว่าเกมแยกตามเพศจริง |
| การแปล | ใช้ agent หลายตัวพร้อมกัน (6–8 ตัว) ให้เสร็จเร็ว |
| Version control | ไม่ใช้ git · ใช้ checkpoint สำเนาโฟลเดอร์แบบ runes |

## ข้อเท็จจริงทางเทคนิคที่ยืนยันจากโค้ดเกม (CFR decompile)

- **ภาษาของมอด**: `Translation.loadModLanguageFile` วนดู entry ใน jar ที่ path ขึ้นต้น `resources/` และลงท้าย `th.lang` → โหลด **ไฟล์แรกที่เจอไฟล์เดียวแล้ว `break`** → มอดเราต้องมี `th.lang` **ไฟล์เดียว** รวมทุก key (ของเกม + ของทุกมอด) — วางที่ `resources/locale/th.lang`
- key ที่มอดโหลดทับ key เดิม (ของเกมหรือมอดอื่น) · มอดที่โหลดทีหลังชนะ · ลำดับโหลดมาจาก dependency → ประกาศมอดที่แปลเป็น `optionalDependencies` เพื่อให้ของเราโหลดทีหลัง (สำคัญกับ Aphorea ที่มี `th.lang` ของตัวเอง)
- **`mod.info`** อยู่ที่ root ของ jar เป็น text รูปแบบ save ของเกม: `id, name, version, gameVersion, author, description, clientside, dependencies, optionalDependencies`
- **รูปแบบ `.lang`**: UTF-8 · `// comment` · `[category]` · `key=value` · ค่าในไฟล์ทางการอาจขึ้นต้น `MISSING_TRANSLATION:` / `SAME_TRANSLATION:` · ใน value มี `<ตัวแปร>`, `§` + ตัวอักษร/เลข/#hex (จัดรูปแบบ), `\n`, `[item=...]` / `[input=...]`
- **ฟอนต์**: `FontManager.loadFonts()` สร้าง `private static TrueTypeGameFontInfo[] fontInfo = {base, japanese, korean, chinese, backup}` แล้วสร้างฟอนต์ทุกขนาดจาก array นั้น · `TrueTypeGameFontInfo(name)` อ่าน `<rootPath>/res/fonts/<name>.ttf` ก่อน ไม่มีค่อยอ่านจาก `res.data` · เรนเดอร์ด้วย STB truetype (ไม่มี shaping/GPOS) · ตัวไทยตอนนี้มาจาก `backup` (Code2000)
- ฟอนต์ถูกโหลดครั้งเดียวตอนเปิดเกม (ก่อน/หลังมอด init ต้องยืนยันใน spike) · `loadFonts()` เป็น `public static` เรียกซ้ำได้ (มัน `deleteFonts()` ก่อน)

## โครงโฟลเดอร์ (`Desktop\necesse\`)

```
data/
  glossary.json            คลังศัพท์
  game/<category>.json     คำแปลตัวเกม 1 ไฟล์ต่อ [category]
  mods/<modid>/<category>.json   คำแปลของแต่ละมอด
  source/                  สำเนา en.lang/th.lang ที่ extract มาล่าสุด (ไว้เทียบตอนเกมอัปเดต)
mod/
  mod.info.template
  src/...                  โค้ด Java (แทรกฟอนต์)
  fonts/<ชื่อ>.ttf + OFL.txt
docs/
  style-guide.md           คู่มือสไตล์การแปล (ให้ agent ทุกตัวอ่าน)
  superpowers/specs, plans
tools/                     Python · เรียก `py -m tools.<ชื่อ>`
tests/                     unittest (`py -m unittest discover -s tests -t .`)
build/                     ผลลัพธ์ build (jar, th.lang ที่รวมแล้ว)
checkpoints/               สำเนาโฟลเดอร์
```

### รูปแบบไฟล์คำแปล (`data/game/<category>.json` ฯลฯ)

JSON UTF-8 เรียงตามลำดับ key ใน `en.lang` · 1 ไฟล์ = 1 category:

```json
{
  "category": "item",
  "entries": [
    {"key": "coinpouch", "en": "Coin Pouch", "official": "ถุงใส่เหรียญ",
     "th": "ถุงใส่เหรียญ", "status": "kept", "note": ""}
  ]
}
```

- `en` = ต้นฉบับอังกฤษ ณ ตอนแปล (ใช้จับว่าต้นฉบับเปลี่ยน)
- `official` = คำแปลทางการ (ตัด prefix `MISSING_TRANSLATION:`/`SAME_TRANSLATION:` ออก · ว่างถ้าขาด)
- `th` = คำแปลของเรา (ว่าง = ยังไม่แปล)
- `status`: `todo` (ยังไม่ทำ) · `kept` (ใช้ของทางการ) · `fixed` (แก้ของทางการ) · `new` (แปลใหม่ — เดิมขาด) · `same` (ตั้งใจให้เหมือนอังกฤษ) · `stale` (ต้นฉบับอังกฤษเปลี่ยนหลังแปล)
- `note` = เหตุผลสั้น ๆ เมื่อ `fixed` หรือข้อควรรู้

### `glossary.json`

```json
[{"en": "Settler", "th": "ชาวนิคม", "kind": "system", "note": "", "approved": false}]
```

`kind`: `system` (ระบบเกม) · `item` · `mob` · `boss` · `biome` · `place` · `name` · `other`

## เครื่องมือ (`tools/`)

| สคริปต์ | หน้าที่ |
|---|---|
| `paths` | path เกม/เซิร์ฟ/workshop/appdata ที่เดียว |
| `langfile` | parse/เขียนไฟล์ `.lang` (รักษาลำดับ category/key) |
| `extract` | อ่าน `en.lang`+`th.lang` ของเกม และ `en.lang`+`th.lang` ใน jar ของมอดในรายการ → สร้าง/อัปเดต `data/**.json` แบบไม่ทับงานแปล: key ใหม่ → `todo` · key ที่ `en` เปลี่ยน → `stale` · key ที่หายจาก en → ย้ายไป `removed` ในไฟล์ (ไม่ลบทิ้ง) |
| `check` | ตรวจคุณภาพ (ด้านล่าง) · รันเฉพาะบางไฟล์ได้ (`--files`) ให้ agent ตรวจงานตัวเอง · exit ≠ 0 ถ้ามี error |
| `glossary` | ดึงศัพท์ผู้สมัคร (ชื่อ item/mob/biome/buff + คำที่ซ้ำบ่อยใน ui) + คำแปลทางการที่ใช้จริงและจำนวนแบบที่ไม่ตรงกัน → ให้ agent ร่างคลังศัพท์ |
| `review` | สร้างหน้า HTML ตาราง en / ทางการ / ของเรา / status ทีละ category (ไฮไลต์ `fixed`) ให้ผู้ใช้อ่าน |
| `build` | รวม `data/**` → `build/th.lang` (ไฟล์เดียว, category ซ้ำจากหลายแหล่งรวมกัน) → `javac` (classpath = `Necesse.jar` + lib ของเกม) → jar (`mod.info`, classes, `resources/locale/th.lang`, ฟอนต์) → ก๊อปไป `%APPDATA%\Necesse\mods\` ให้ลองเล่น |
| `checkpoint` | สำเนาโฟลเดอร์ `data/ docs/ mod/ tools/ tests/` ไป `checkpoints/<วันเวลา>/` |

### กฎของ `check`

Error (ต้องแก้ก่อน build):
- `th` ว่างในแถวที่ status ไม่ใช่ `todo` · หรือยังมี `todo`/`stale` ตอนรันโหมด `--release`
- ชุดของ `<...>`, `[item=...]`/`[input=...]`, `§<code>` ใน `th` ไม่ตรงกับ `en` (ลำดับเปลี่ยนได้ จำนวน/ชื่อต้องตรง)
- จำนวน `\n` ต่างจาก `en` (warning ถ้าตั้งใจ — ใส่เหตุผลใน `note`)
- key ชนกันระหว่างเกมกับมอด หรือระหว่างมอด ที่ `th` ไม่เท่ากัน
- ตัวอักษรไทยที่ฟอนต์วาดไม่ได้ / อักขระควบคุมแปลก ๆ / ช่องว่างหัวท้าย

Warning (รายงาน ไม่บล็อก):
- ใช้คำที่ขัดกับคลังศัพท์ (เจอคำอังกฤษของศัพท์ใน `en` แต่ไม่เจอคำไทยที่อนุมัติใน `th`)
- คำสะกดผิดที่พบบ่อย (รายการใน `tools/checkdata.py` เช่น เช็ท→เซ็ต, ล๊อค→ล็อก, ไอเท็ม→ไอเทม ตามที่คลังศัพท์กำหนด)
- คำลงท้ายตามเพศ (ครับ ค่ะ คะ ผม ดิฉัน) ในหมวดบทพูด NPC ยกเว้น key ใน allowlist
- `th` เหมือน `en` ทุกตัวอักษรแต่ status ไม่ใช่ `same`
- `th` ยาวกว่า `en` มาก (> 2 เท่าของจำนวนตัวอักษร) ในหมวด ui — อาจล้นกรอบ

## ฟอนต์ (spike ก่อน — เป็นงานแรก)

แผน:
1. โค้ด Java คลาส `@ModEntry` ทำงานเฉพาะ client
2. สร้าง `TrueTypeGameFontInfo` ของฟอนต์ไทย — ตัว constructor อ่านจากไฟล์ตาม path เท่านั้น → วิธีที่ต้องลองใน spike (เรียงตามความชอบ):
   - a. ใช้ reflection สร้าง object แล้วใส่ bytes ของฟอนต์จาก jar เอง (ไม่เขียนไฟล์ลงเครื่อง)
   - b. แตก ttf จาก jar ไปไฟล์ชั่วคราว แล้วสร้างด้วย path นั้น (ถ้า constructor รับ path ได้ทางอ้อม)
3. แทรกเข้า `fontInfo` **ถัดจาก `base`** (ตัวละตินยังมาจาก FreeSans Bold เหมือนเดิม) แล้วเรียก `FontManager.loadFonts()` ใหม่ หรือแทรกก่อนเกมเรียกครั้งแรกถ้ามอด init ก่อน
4. ทุกขั้นห่อ try/catch → ล้มเหลว = log `[thai] font inject failed: ...` แล้วปล่อยเกมใช้ฟอนต์เดิม (คำแปลยังทำงาน)
5. เทียบฟอนต์ OFL: **Sarabun, Noto Sans Thai, Kanit, Prompt** (น้ำหนัก Regular/Medium ให้เข้ากับ FreeSans Bold) → ถ่ายภาพในเกมหน้าเดียวกัน (เมนู, tooltip ไอเทม, บทพูด) ขนาด 12/16/20 → ผู้ใช้เลือก
6. ดูเรื่องสระบน+วรรณยุกต์ซ้อน (STB ไม่ย้ายตำแหน่งให้) — ถ้าชนกันหนักในทุกฟอนต์ ให้ลองฟอนต์ที่ออกแบบ mark ให้ยกสูงพอ หรือประเมินการแปลงเป็น glyph แบบ "ยกต่ำ/ยกสูง" ใน PUA (ยังไม่ทำจนกว่าจะเห็นว่าจำเป็น)

**ถ้า spike ไม่สำเร็จ** (แทรกไม่ได้เลย) → ถอยเป็นแบบ C: มอดมีแค่คำแปล + แจก ttf ให้วางเองที่ `<game>\res\fonts\backup.ttf` พร้อมคำอธิบายในหน้า Workshop — แจ้งผู้ใช้ก่อนเปลี่ยนแผน

## ขั้นตอนแปล (multi-agent)

1. `extract` → `data/**`
2. **คู่มือสไตล์** `docs/style-guide.md` (ผมเขียนเอง): ภาษากลางใน NPC, แนวทับศัพท์ vs แปลความ (ตามแนวทางการเดิม: แปลความเมื่อเป็นคำทั่วไป ทับศัพท์ชื่อเฉพาะ), ตัวเลข/หน่วย, วิธีเขียนคำอังกฤษที่ทับศัพท์ (ตามราชบัณฑิตฯ แต่ยอมตามที่คนเล่นเกมคุ้นเมื่อชัด เช่น ไอเทม), ห้ามแตะตัวแปร/โค้ดสี
3. **คลังศัพท์**: agent 1 ตัวใช้ `tools.glossary` ร่าง ~200–300 คำ → ผู้ใช้อนุมัติ (เปิดในหน้า HTML ได้) → `approved: true` · **ห้ามเริ่มขั้น 4 ก่อนอนุมัติ**
4. **แปลขนาน 6–8 agent**: แบ่ง `data/**.json` เป็นกลุ่มไม่ทับกัน จำนวนแถวใกล้เคียงกัน (romance แตก 2–3 ก้อนตามช่วง key) · แต่ละ agent: อ่าน style guide + glossary → รีวิว/แปลทุกแถวในไฟล์ของตัวเอง → รัน `py -m tools.check --files ...` จนไม่มี error → รายงานคำที่อยากเพิ่มในคลังศัพท์ (ไม่แก้ glossary เอง)
5. **ตรวจรวม**: agent 1–2 ตัวอ่านข้ามไฟล์หาความไม่สม่ำเสมอ (เช่น ชื่อเดียวกันสะกดต่าง) + `check` ทั้งหมด
6. **ผู้ใช้ตรวจ**: `review` หมวด romance / personalities / mobmsg / objectives (+ อื่นตามต้องการ)
7. `build` → ลองเล่นตามเช็กลิสต์ → แก้ → checkpoint

แปลมอดอื่นอยู่ในขั้น 4 (agent ตัวหนึ่งถือ `data/mods/**`)

## การปล่อย

- `mod.info`: `id = thaicommunity.thailanguage` (ชื่อจริงตกลงตอนปล่อย) · `clientside = true` · `gameVersion` = เวอร์ชันเกมปัจจุบัน · `optionalDependencies` = id ของมอดที่แปล
- อัปโหลด Workshop ผ่านเมนูมอดในเกม (ผู้ใช้ทำเอง) · หน้า Workshop มีคำอธิบายไทย + เครดิตผู้แปลทางการเดิม + สัญญาอนุญาตฟอนต์ OFL
- เกมอัปเดต → `extract` → แปลแถว `todo`/`stale` → `build` → อัปโหลดเวอร์ชันใหม่ (`gameVersion` ใหม่)

## การทดสอบ

- **unittest** ของ `langfile`, `extract` (merge ไม่ทับงานแปล, จับ stale/removed), `check` (ทุกกฎ), `build` (th.lang ที่รวมแล้ว parse กลับได้ครบ key, jar มีไฟล์ครบ, `mod.info` ถูก)
- **ลองเล่น** (เช็กลิสต์ใน plan): เมนูหลัก/ตั้งค่า · คลังของ + tooltip · คุยกับ NPC/settler · ภารกิจ · ไอเทม Aphorea · ตรวจ log ว่าโหลดมอดและฟอนต์สำเร็จ · สระบน+วรรณยุกต์ (เช่น "ที่นี่", "เรื่อง", "น้ำ", "ปั้น")
- เปิดเกมภาษาอังกฤษพร้อมมอด → ต้องไม่มีผลอะไร

## นอกขอบเขต

- ภาษาอื่นนอกจากไทย · แปลมอดที่ผู้ใช้ไม่ได้เล่น (เพิ่มทีหลังได้)
- แก้ไฟล์ในโฟลเดอร์เกม/`res.data` ตรง ๆ
- shaping ภาษาไทยเต็มรูปแบบ (เว้นแต่ spike ฟอนต์พบว่าจำเป็น → ออกแบบแยก)
