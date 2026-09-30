package thailanguage;

/** จัดตำแหน่งสระ/วรรณยุกต์ไทยแบบง่ายสำหรับ renderer ของเกม (STB ไม่มี GSUB/GPOS)
 *  เปลี่ยนตัวอักษรเป็นรูปที่ย้ายตำแหน่งแล้วในช่อง PUA ของฟอนต์ที่ tools/thaifont.py สร้าง
 *  codepoint ต้องตรงกับ tools/thaifont.py (tests/test_shaper.py ตรวจให้) */
public final class ThaiShaper {
    public static final char TONE_HIGH = 0xF700;
    public static final char TONE_LOW_LEFT = 0xF705;
    public static final char TONE_HIGH_LEFT = 0xF70A;
    public static final char UPPER_LEFT = 0xF710;
    public static final char LOWER_LOW = 0xF718;

    private static final String TONES = "่้๊๋์";
    private static final String UPPERS = "ัิีึื็ํ";
    private static final String LOWERS = "ฺุู";
    private static final String TALL = "ปฝฟฬ";       // ป ฝ ฟ ฬ
    private static final String LOW_TAIL = "ฎฏ";             // ฎ ฏ
    private static final char SARA_AM = 'ำ';

    /** ตัวอักษร PUA ทั้งหมดที่อาจถูกวาด — ต้องใส่ใน FontManager.additionalFontCharacters ให้เกมเตรียม glyph */
    public static final String PUA_CHARS = range(TONE_HIGH, 5) + range(TONE_LOW_LEFT, 5)
            + range(TONE_HIGH_LEFT, 5) + range(UPPER_LEFT, 7) + range(LOWER_LOW, 3);

    private ThaiShaper() {}

    public static String shape(String s) {
        if (s == null || !hasThai(s)) return s;
        char[] in = s.toCharArray();
        char[] out = in.clone();
        for (int i = 0; i < in.length; i++) {
            char c = in[i];
            int tone = TONES.indexOf(c);
            int upper = UPPERS.indexOf(c);
            int lower = LOWERS.indexOf(c);
            if (tone < 0 && upper < 0 && lower < 0) continue;
            char base = baseOf(in, i);
            boolean tall = TALL.indexOf(base) >= 0;
            if (tone >= 0) {
                boolean hasUpper = (i > 0 && UPPERS.indexOf(in[i - 1]) >= 0)
                        || (i + 1 < in.length && in[i + 1] == SARA_AM);
                if (hasUpper && tall) out[i] = (char) (TONE_HIGH_LEFT + tone);
                else if (hasUpper) out[i] = (char) (TONE_HIGH + tone);
                else if (tall) out[i] = (char) (TONE_LOW_LEFT + tone);
            } else if (upper >= 0) {
                if (tall) out[i] = (char) (UPPER_LEFT + upper);
            } else if (LOW_TAIL.indexOf(base) >= 0) {
                out[i] = (char) (LOWER_LOW + lower);
            }
        }
        return new String(out);
    }

    private static char baseOf(char[] in, int i) {
        for (int j = i - 1; j >= 0; j--) {
            char p = in[j];
            if (TONES.indexOf(p) < 0 && UPPERS.indexOf(p) < 0 && LOWERS.indexOf(p) < 0) return p;
        }
        return 0;
    }

    private static boolean hasThai(String s) {
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '฀' && c <= '๿') return true;
        }
        return false;
    }

    private static String range(char start, int n) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < n; i++) b.append((char) (start + i));
        return b.toString();
    }
}
