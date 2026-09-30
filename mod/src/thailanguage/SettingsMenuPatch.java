package thailanguage;

import necesse.engine.modLoader.annotations.ModMethodPatch;
import necesse.gfx.forms.Form;
import necesse.gfx.forms.components.lists.FormLanguageList;
import necesse.gfx.forms.components.localComponents.FormLocalTextButton;
import necesse.gfx.forms.presets.SettingsForm;
import net.bytebuddy.asm.Advice;

/** แทรกส่วนตั้งค่าฟอนต์ไทยเข้าหน้า ตั้งค่า → ภาษา (ไม่มีหน้าตั้งค่ามอดในเกม) */
public class SettingsMenuPatch {
    @ModMethodPatch(target = SettingsForm.class, name = "updateLanguageForm", arguments = {})
    public static class Build {
        @Advice.OnMethodExit
        static void onExit(@Advice.FieldValue("language") Form language,
                           @Advice.FieldValue("languageList") FormLanguageList list,
                           @Advice.FieldValue("languageHelp") FormLocalTextButton help) {
            try {
                ThaiFontMenu.addTo(language);
                ThaiFontMenu.layout(list, help);
            } catch (Throwable t) {
                System.err.println("[thai] font menu failed: " + t);
            }
        }
    }

    @ModMethodPatch(target = SettingsForm.class, name = "updateLanguageHeight", arguments = {})
    public static class Height {
        @Advice.OnMethodExit
        static void onExit(@Advice.FieldValue("languageList") FormLanguageList list,
                           @Advice.FieldValue("languageHelp") FormLocalTextButton help) {
            try {
                ThaiFontMenu.layout(list, help);
            } catch (Throwable t) {
                System.err.println("[thai] font menu layout failed: " + t);
            }
        }
    }
}
