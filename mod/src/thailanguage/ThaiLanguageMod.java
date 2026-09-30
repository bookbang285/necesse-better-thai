package thailanguage;

import necesse.engine.modLoader.annotations.ModEntry;
import necesse.gfx.gameFont.FontManager;

@ModEntry
public class ThaiLanguageMod {
    public void init() {
        // ให้เกมเตรียม glyph ของรูปสระ/วรรณยุกต์ที่ ThaiShaper สลับให้ (ไม่งั้นขึ้น ?)
        if (ThaiFont.available() && !FontManager.additionalFontCharacters.contains(ThaiShaper.PUA_CHARS)) {
            FontManager.additionalFontCharacters += ThaiShaper.PUA_CHARS;
        }
        System.out.println("[thai] Thai Language mod loaded");
    }

    /** เกมสร้างฟอนต์ก่อน patch ของมอดติดตั้ง → สร้างใหม่ตอนนี้ให้ patch แทรกฟอนต์ไทย
     *  (ฝั่งเซิร์ฟไม่มีฟอนต์ → isLoaded() เป็น false ข้ามไป) */
    public void postInit() {
        try {
            if (FontManager.isLoaded()) {
                FontManager.loadFonts();
            }
        } catch (Throwable t) {
            System.err.println("[thai] font reload failed: " + t);
            t.printStackTrace();
        }
    }
}
