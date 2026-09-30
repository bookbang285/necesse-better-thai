package thailanguage;

import necesse.engine.localization.fileLanguage.TranslationCategory;
import necesse.engine.modLoader.LoadedMod;
import net.bytebuddy.asm.Advice;
import necesse.engine.modLoader.annotations.ModMethodPatch;

/** เกมวาดข้อความ UI ทีละตัวอักษร (drawChar) → จัดสระ/วรรณยุกต์ตอนวาดไม่ได้เพราะไม่เห็นตัวข้างเคียง
 *  จึงจัดตั้งแต่ตอนโหลดคำแปลแทน (ครอบคลุมทุกข้อความที่มาจากไฟล์ภาษา ทั้งของเกม มอดนี้ และมอดอื่น) */
@ModMethodPatch(target = TranslationCategory.class, name = "addTranslation",
        arguments = {String.class, String.class, String.class, boolean.class, boolean.class, LoadedMod.class})
public class TranslationPatch {
    @Advice.OnMethodEnter
    static void onEnter(@Advice.Argument(value = 2, readOnly = false) String translation) {
        if (ThaiFont.available()) translation = ThaiShaper.shape(translation);
    }
}
