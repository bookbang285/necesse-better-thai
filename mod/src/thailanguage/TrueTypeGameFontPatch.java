package thailanguage;

import necesse.engine.modLoader.annotations.ModConstructorPatch;
import necesse.gfx.gameFont.CustomGameFont;
import necesse.gfx.gameFont.TrueTypeGameFont;
import necesse.gfx.gameFont.TrueTypeGameFontInfo;
import net.bytebuddy.asm.Advice;

@ModConstructorPatch(target = TrueTypeGameFont.class,
        arguments = {int.class, int.class, int.class, int.class, CustomGameFont.CharArray.class, TrueTypeGameFontInfo[].class})
public class TrueTypeGameFontPatch {
    @Advice.OnMethodEnter
    static void onEnter(@Advice.Argument(value = 5, readOnly = false) TrueTypeGameFontInfo[] fonts) {
        fonts = ThaiFont.insert(fonts);
    }
}
