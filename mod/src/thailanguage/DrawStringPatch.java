package thailanguage;

import necesse.engine.modLoader.annotations.ModMethodPatch;
import necesse.gfx.gameFont.FontBasicOptions;
import necesse.gfx.gameFont.TrueTypeGameFont;
import net.bytebuddy.asm.Advice;

/** จัดสระ/วรรณยุกต์ไทยก่อนเกมวาดข้อความ (ความกว้างไม่เปลี่ยน — glyph ที่สลับเป็นเครื่องหมายกว้าง 0 เหมือนเดิม) */
public class DrawStringPatch {
    @ModMethodPatch(target = TrueTypeGameFont.class, name = "drawString",
            arguments = {float.class, float.class, String.class, FontBasicOptions.class})
    public static class Draw {
        @Advice.OnMethodEnter
        static void onEnter(@Advice.Argument(value = 2, readOnly = false) String text) {
            if (ThaiFont.available()) text = ThaiShaper.shape(text);
        }
    }

    @ModMethodPatch(target = TrueTypeGameFont.class, name = "drawStringShadow",
            arguments = {float.class, float.class, String.class, FontBasicOptions.class})
    public static class Shadow {
        @Advice.OnMethodEnter
        static void onEnter(@Advice.Argument(value = 2, readOnly = false) String text) {
            if (ThaiFont.available()) text = ThaiShaper.shape(text);
        }
    }
}
