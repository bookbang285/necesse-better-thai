# หน้า Steam Workshop — ภาษาไทย (Thai Language)

## ชื่อ
ภาษาไทย ฉบับสมบูรณ์ + ฟอนต์อ่านง่าย (Thai Language)

## คำอธิบาย (วางในช่อง Description)

[h1]ภาษาไทยครบทั้งเกม + ฟอนต์ไทยที่อ่านง่าย[/h1]

มอดนี้ทำให้ Necesse เป็นภาษาไทยที่ครบและอ่านง่ายขึ้น:

[list]
[*] [b]แปลครบทุกข้อความ[/b] — เติมข้อความที่ภาษาไทยทางการยังขาด (~1,500 บรรทัด) และตรวจคำแปลเดิมทุกบรรทัด แก้คำสะกดผิด ความหมายผิด และศัพท์ที่ไม่ตรงกัน
[*] [b]คลังศัพท์เดียวกันทั้งเกม[/b] — ชื่อไอเทม มอนสเตอร์ บอส ชีวนิเวศ เรียกเหมือนกันทุกที่
[*] [b]ชื่อไอเทม/มอนสเตอร์มีภาษาอังกฤษในวงเล็บ[/b] — เช่น "แท่งเหล็ก (Iron Bar)" ค้นข้อมูลใน Google/Wiki ได้ทันที
[*] [b]ฟอนต์ไทยใหม่ (Prompt)[/b] — แทนฟอนต์เดิมที่อ่านยาก สระ/วรรณยุกต์ซ้อนถูกตำแหน่ง ไม่หาย ไม่ทับกัน
[*] [b]แปลมอดยอดนิยมด้วย[/b] — Aphorea, Quick Recipes Menu, More Trinket Slots, A Better Torch, Boss Fight Summary, Increased Stack Size
[*] [b]บทพูด NPC เป็นภาษากลาง[/b] — อ่านเป็นธรรมชาติ ไม่ติดคำลงท้ายตามเพศ
[/list]

[h2]วิธีใช้[/h2]
[olist]
[*] กด Subscribe
[*] เปิดเกม → ตั้งค่า → ภาษา → ไทย
[/olist]

มอดนี้เป็น [b]clientside[/b] — ลงเฉพาะคนที่อยากเล่นภาษาไทย ไม่ต้องลงที่เซิร์ฟ และเล่นร่วมกับเพื่อนที่ไม่ได้ลงได้ตามปกติ
มอดที่แปลไว้จะแสดงภาษาไทยเฉพาะเมื่อเปิดมอดนั้นอยู่

[h2]ข้อจำกัดที่รู้แล้ว[/h2]
[list]
[*] ข้อความที่พิมพ์เอง (แชต/ช่องค้นหา) สระบางคำอาจซ้อนไม่สวย
[*] ค้นหาไอเทมด้วยคำไทยที่มีวรรณยุกต์บนสระ (เช่น "ที่") อาจหาไม่เจอ — ค้นด้วยภาษาอังกฤษได้
[/list]

[h2]เครดิต[/h2]
[list]
[*] คำแปลภาษาไทยทางการของเกม: Himeda Fukusa, Miraisa Gaizaku, Mitsuaki Tora (ใช้เป็นฐานและคงไว้ส่วนที่ดีอยู่แล้ว)
[*] ฟอนต์ Prompt โดย Cadson Demak — SIL Open Font License 1.1
[/list]

เจอคำแปลผิด/แปลก แจ้งในคอมเมนต์ได้เลย (บอกข้อความภาษาอังกฤษหรือแนบภาพ F5)

---

[h1]Thai Language — complete translation + readable Thai font[/h1]
Complete Thai localisation for Necesse: fills ~1,500 missing lines, reviews every existing line, consistent terminology, English names in brackets for items/mobs, a new Thai font (Prompt, OFL) with correct vowel/tone-mark stacking, and Thai for popular mods (Aphorea, Quick Recipes Menu, More Trinket Slots, A Better Torch, Boss Fight Summary, Increased Stack Size). Client-side only — not needed on servers.

## ขั้นตอนอัปโหลด (ผู้ใช้ทำ)
1. `py -m tools.build` (ตั้ง `version` = 1.0.0 ใน `mod/build.json` แล้ว) → jar อยู่ใน `%APPDATA%\Necesse\mods\`
2. เปิดเกม → เมนู Mods → เลือก Thai Language → Upload to Workshop
3. ใส่ชื่อ/คำอธิบายจากไฟล์นี้ · ภาพ preview: ภาพหน้าจอเมนูภาษาไทย (F5) · ตั้ง Visibility = Public เมื่อพร้อม
