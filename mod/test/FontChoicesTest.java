import thailanguage.FontChoices;

/** รันผ่าน tests/test_shaper.py */
public class FontChoicesTest {
    static int failed = 0;

    static void eq(String name, Object got, Object expected) {
        if (got == null ? expected != null : !got.equals(expected)) {
            failed++;
            System.out.println("FAIL " + name + ": " + got + " != " + expected);
        } else {
            System.out.println("ok   " + name);
        }
    }

    public static void main(String[] args) {
        FontChoices c = FontChoices.parse("Prompt|Prompt-Medium.ttf\nKanit|Kanit-Medium.ttf\r\nMitr|Mitr-Regular.ttf\n\n");
        eq("count", c.size(), 3);
        eq("default is first", c.find(null)[0], "Prompt");
        eq("find by name", c.find("Kanit")[1], "Kanit-Medium.ttf");
        eq("unknown falls back to first", c.find("Comic Sans")[0], "Prompt");
        eq("next", c.next("Prompt"), "Kanit");
        eq("next wraps", c.next("Mitr"), "Prompt");
        eq("next of unknown", c.next("x"), "Kanit");
        eq("clamp low", FontChoices.clampSize(50), 90);
        eq("clamp high", FontChoices.clampSize(200), 115);
        eq("clamp inside", FontChoices.clampSize(104), 104);
        eq("empty list", FontChoices.parse("").size(), 0);
        if (failed > 0) {
            System.out.println(failed + " failed");
            System.exit(1);
        }
        System.out.println("all passed");
    }
}
