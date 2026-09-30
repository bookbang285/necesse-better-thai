package thailanguage;

import java.util.ArrayList;
import java.util.List;

/** รายการฟอนต์ไทยในมอด (thaifont/fonts.txt: "ชื่อ|ไฟล์" บรรทัดละตัว · ตัวแรก = ค่าเริ่มต้น) + ช่วงขนาดที่ปลอดภัย
 *  ขนาดเกิน 115% ปุ่มของเกมจะตัดวรรณยุกต์ด้านบน (กรอบบรรทัดสูงเท่าตัวละติน) */
public final class FontChoices {
    public static final int MIN_SIZE = 90;
    public static final int MAX_SIZE = 115;

    private final List<String[]> fonts = new ArrayList<>();

    private FontChoices() {}

    public static FontChoices parse(String text) {
        FontChoices c = new FontChoices();
        for (String line : text.split("\\r?\\n")) {
            int bar = line.indexOf('|');
            if (bar > 0 && bar < line.length() - 1) {
                c.fonts.add(new String[]{line.substring(0, bar).trim(), line.substring(bar + 1).trim()});
            }
        }
        return c;
    }

    public int size() {
        return fonts.size();
    }

    /** {ชื่อ, ไฟล์} ของฟอนต์ชื่อนี้ · ไม่เจอ/null = ตัวแรก */
    public String[] find(String name) {
        for (String[] f : fonts) if (f[0].equals(name)) return f;
        return fonts.isEmpty() ? null : fonts.get(0);
    }

    public String next(String name) {
        for (int i = 0; i < fonts.size(); i++) {
            if (fonts.get(i)[0].equals(name)) return fonts.get((i + 1) % fonts.size())[0];
        }
        return fonts.size() > 1 ? fonts.get(1)[0] : find(null)[0];
    }

    public static int clampSize(int size) {
        return Math.max(MIN_SIZE, Math.min(MAX_SIZE, size));
    }
}
