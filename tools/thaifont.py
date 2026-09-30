"""ทำฟอนต์ไทยสำหรับเกม: เพิ่มรูปสระ/วรรณยุกต์ที่ย้ายตำแหน่งแล้วไว้ใน PUA

เกมวาดด้วย STB (ไม่มี GSUB/GPOS) → วรรณยุกต์ทับสระบน (ที่ → ที) และทับหาง ป ฝ ฟ
มอดฝั่ง Java (ThaiShaper) เปลี่ยนตัวอักษรเป็น codepoint ด้านล่างก่อนวาด — ต้องตรงกันทั้งสองฝั่ง

py -m tools.thaifont <src.ttf> <out.ttf>
"""
import sys
from pathlib import Path

from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

TONES = [0x0E48, 0x0E49, 0x0E4A, 0x0E4B, 0x0E4C]            # ่ ้ ๊ ๋ ์
UPPERS = [0x0E31, 0x0E34, 0x0E35, 0x0E36, 0x0E37, 0x0E47, 0x0E4D]  # ั ิ ี ึ ื ็ ํ
LOWERS = [0x0E38, 0x0E39, 0x0E3A]                            # ุ ู ฺ

TONE_HIGH = 0xF700        # วรรณยุกต์ยกสูง (มีสระบน / ตามด้วย ำ)
TONE_LOW_LEFT = 0xF705    # วรรณยุกต์เยื้องซ้าย (ป ฝ ฟ ฬ ไม่มีสระบน)
TONE_HIGH_LEFT = 0xF70A   # ยกสูง + เยื้องซ้าย
UPPER_LEFT = 0xF710       # สระบนเยื้องซ้าย (ป ฝ ฟ ฬ)
LOWER_LOW = 0xF718        # สระล่างต่ำลง (ฎ ฏ)

PUA = ([TONE_HIGH + i for i in range(len(TONES))] + [TONE_LOW_LEFT + i for i in range(len(TONES))]
       + [TONE_HIGH_LEFT + i for i in range(len(TONES))] + [UPPER_LEFT + i for i in range(len(UPPERS))]
       + [LOWER_LOW + i for i in range(len(LOWERS))])


TALL = "ปฝฟฬ"
LOW_TAIL = "ฎฏ"


def shape(s: str) -> str:
    """ตัวเดียวกับ ThaiShaper.java — ใช้ทำภาพตัวอย่างฟอนต์"""
    tones, uppers, lowers = map(lambda l: "".join(map(chr, l)), (TONES, UPPERS, LOWERS))
    out = list(s)
    for i, c in enumerate(s):
        j = i - 1
        while j >= 0 and s[j] in tones + uppers + lowers:
            j -= 1
        base = s[j] if j >= 0 else ""
        tall = base != "" and base in TALL
        if c in tones:
            t = tones.index(c)
            high = (i > 0 and s[i - 1] in uppers) or (i + 1 < len(s) and s[i + 1] == "ำ")
            if high and tall:
                out[i] = chr(TONE_HIGH_LEFT + t)
            elif high:
                out[i] = chr(TONE_HIGH + t)
            elif tall:
                out[i] = chr(TONE_LOW_LEFT + t)
        elif c in uppers and tall:
            out[i] = chr(UPPER_LEFT + uppers.index(c))
        elif c in lowers and base != "" and base in LOW_TAIL:
            out[i] = chr(LOWER_LOW + lowers.index(c))
    return "".join(out)


def _shifted(font: TTFont, src: str, name: str, dx: int, dy: int) -> str:
    gs = font.getGlyphSet()
    pen = TTGlyphPen(gs)
    gs[src].draw(TransformPen(pen, (1, 0, 0, 1, dx, dy)))
    glyph = pen.glyph()
    font["glyf"][name] = glyph
    glyph.recalcBounds(font["glyf"])
    font["hmtx"][name] = (0, getattr(glyph, "xMin", 0))
    font.setGlyphOrder(font.getGlyphOrder() + [name]) if name not in font.getGlyphOrder() else None
    return name


def _variant(font: TTFont, base: str, suffix: str, fallback: tuple[str, str, int, int] | None) -> str:
    """ใช้ glyph สำรองที่ฟอนต์มีอยู่ (เช่น uni0E48.small) ถ้าไม่มีก็สร้างโดยเลื่อน glyph เดิม"""
    order = set(font.getGlyphOrder())
    if f"{base}{suffix}" in order:
        return f"{base}{suffix}"
    src, name, dx, dy = fallback
    return _shifted(font, src, name, dx, dy)


def _bounds(font: TTFont, name: str) -> tuple[int, int, int, int]:
    g = font["glyf"][name]
    g.recalcBounds(font["glyf"])
    return g.xMin, g.yMin, g.xMax, g.yMax


def make(src: Path, dst: Path, high_cap: float | None = None) -> None:
    """high_cap = ความสูงสูงสุดของวรรณยุกต์ยกสูง (หน่วย em) — ปุ่มของเกมตัดทุกอย่างที่เกินกรอบบรรทัด"""
    font = TTFont(src)
    upem = font["head"].unitsPerEm
    cmap = font.getBestCmap()
    names = {cp: cmap[cp] for cp in TONES + UPPERS + LOWERS if cp in cmap}
    # ระยะอ้างอิงจากไม้เอก: .small = ยกสูง, .narrow = เยื้องซ้าย
    ref = names[0x0E48]
    up = _bounds(font, ref + ".small")[1] - _bounds(font, ref)[1]
    left = _bounds(font, ref + ".narrow")[0] - _bounds(font, ref)[0]
    ref_u = names[0x0E34]
    left_u = _bounds(font, ref_u + ".narrow")[0] - _bounds(font, ref_u)[0]
    if names[0x0E38] + ".small" in set(font.getGlyphOrder()):
        low = _bounds(font, names[0x0E38] + ".small")[1] - _bounds(font, names[0x0E38])[1]
    else:
        low = -font["head"].unitsPerEm // 5

    mapping: dict[int, str] = {}
    for i, cp in enumerate(TONES):
        n = names[cp]
        high = _variant(font, n, ".small", (n, f"{n}.th_high", 0, up))
        if high_cap is not None:
            over = _bounds(font, high)[3] - int(high_cap * upem)
            if over > 0:
                high = _shifted(font, high, f"{n}.th_highcap", 0, -over)
        mapping[TONE_HIGH + i] = high
        mapping[TONE_LOW_LEFT + i] = _variant(font, n, ".narrow", (n, f"{n}.th_left", left, 0))
        mapping[TONE_HIGH_LEFT + i] = _shifted(font, high, f"{n}.th_highleft", left, 0)
    for i, cp in enumerate(UPPERS):
        n = names[cp]
        mapping[UPPER_LEFT + i] = _variant(font, n, ".narrow", (n, f"{n}.th_left", left_u, 0))
    for i, cp in enumerate(LOWERS):
        n = names[cp]
        mapping[LOWER_LOW + i] = _variant(font, n, ".small", (n, f"{n}.th_low", 0, low))

    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap.update(mapping)
    for name in set(mapping.values()):
        font["hmtx"][name] = (0, font["hmtx"][name][1])
    dst.parent.mkdir(parents=True, exist_ok=True)
    font.save(dst)


if __name__ == "__main__":
    make(Path(sys.argv[1]), Path(sys.argv[2]))
    print(sys.argv[2])
