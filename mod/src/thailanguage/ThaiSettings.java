package thailanguage;

import necesse.engine.modLoader.ModSettings;
import necesse.engine.save.LoadData;
import necesse.engine.save.SaveData;

/** ค่าตั้งค่าฟอนต์ไทย — เกมเก็บให้ใน %APPDATA%\Necesse\cfg\mods\thaicommunity.thailanguage.cfg
 *  (เกมเซฟตอน Settings.saveClientSettings()) */
public class ThaiSettings extends ModSettings {
    /** ชื่อฟอนต์ที่เลือก (null = ตัวแรกในรายการ) */
    public static String font = null;
    /** ขนาดตัวไทยเป็น % (-1 = ค่าเริ่มต้นจาก thaifont/size.txt) */
    public static int size = -1;

    @Override
    public void addSaveData(SaveData save) {
        if (font != null) save.addUnsafeString("font", font);
        if (size > 0) save.addInt("size", size);
    }

    @Override
    public void applyLoadData(LoadData load) {
        font = load.getUnsafeString("font", font);
        int s = load.getInt("size", size);
        size = s > 0 ? FontChoices.clampSize(s) : -1;
    }
}
