import thailanguage.ThaiShaper;

/** รันผ่าน tests/test_shaper.py — ไม่มี JUnit ในโปรเจกต์นี้ */
public class ThaiShaperTest {
    static int failed = 0;

    static void eq(String name, String input, String expected) {
        String got = ThaiShaper.shape(input);
        if (got == null ? expected != null : !got.equals(expected)) {
            failed++;
            System.out.println("FAIL " + name + ": " + hex(got) + " != " + hex(expected));
        } else {
            System.out.println("ok   " + name);
        }
    }

    static String hex(String s) {
        if (s == null) return "null";
        StringBuilder b = new StringBuilder();
        for (char c : s.toCharArray()) b.append(String.format("%04X ", (int) c));
        return b.toString().trim();
    }

    public static void main(String[] args) {
        eq("no thai unchanged", "Iron Sword 12%", "Iron Sword 12%");
        eq("tone on plain consonant unchanged", "ย่า", "ย่า");                // ย่า
        eq("tone above upper vowel goes high", "ที่", "ที");                 // ที่
        eq("tone before sara am goes high", "น้ำ", "นำ");                    // น้ำ
        eq("tone on tall consonant shifts left", "ป่า", "ปา");               // ป่า
        eq("upper vowel on tall consonant shifts left", "ปี", "ป");                   // ปี
        eq("tall + upper + tone = both left, tone high", "ปั้น", "ปน"); // ปั้น
        eq("tall + lower vowel + tone: tone left", "ปู่", "ปู");             // ปู่
        eq("lower vowel under do chada goes low", "ฎุ", "ฎ");                          // ฎุ
        eq("thanthakhat above upper vowel", "สิ์", "สิ");                    // สิ์
        eq("null safe", null, null);
        if (failed > 0) {
            System.out.println(failed + " failed");
            System.exit(1);
        }
        System.out.println("all passed");
    }
}
