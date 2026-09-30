package thailanguage;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import necesse.engine.GlobalData;
import necesse.engine.Settings;
import necesse.gfx.gameFont.FontManager;
import necesse.gfx.gameFont.TrueTypeGameFontInfo;

/** ฟอนต์ไทยที่ผู้เล่นเลือก (ThaiSettings) — แตกไฟล์จาก jar ไปโฟลเดอร์ที่อยู่ไดรฟ์เดียวกับเกม
 *  (เกมเปิดฟอนต์ด้วย path สัมพัทธ์จาก res/fonts/ เท่านั้น) แล้วแทรกเข้า fallback chain ถัดจาก base
 *  available() = มีโฟลเดอร์ให้วางไฟล์ → ค่อยสลับรูปสระเป็น PUA (ไม่งั้นสระจะกลายเป็นกล่อง) */
public final class ThaiFont {
    private static Path fontsDir;        // <root>/res/fonts
    private static Path dir;             // โฟลเดอร์ที่วางไฟล์ฟอนต์
    private static boolean prepared;
    private static FontChoices choices;
    private static TrueTypeGameFontInfo info;
    private static String infoKey;       // ฟอนต์+ขนาดของ info ปัจจุบัน
    private static boolean failed;

    private ThaiFont() {}

    public static synchronized boolean available() {
        if (!prepared) {
            prepared = true;
            try {
                choices = FontChoices.parse(readText("/thaifont/fonts.txt"));
                if (choices.size() == 0) throw new IOException("no fonts in thaifont/fonts.txt");
                prepareDir();
                System.out.println("[thai] Thai font folder ready: " + dir);
            } catch (Throwable t) {
                fail(t);
            }
        }
        return dir != null && !failed;
    }

    public static synchronized FontChoices choices() {
        return available() ? choices : null;
    }

    public static synchronized String currentFont() {
        String[] f = available() ? choices.find(ThaiSettings.font) : null;
        return f == null ? "-" : f[0];
    }

    public static synchronized int currentSize() {
        if (ThaiSettings.size > 0) return ThaiSettings.size;
        try {
            return FontChoices.clampSize(Integer.parseInt(readText("/thaifont/size.txt").trim()));
        } catch (Throwable t) {
            return 100;
        }
    }

    /** เปลี่ยนฟอนต์/ขนาดจากเมนู → สร้างฟอนต์ของเกมใหม่ทันที + เซฟค่า */
    public static void apply(String font, int size) {
        synchronized (ThaiFont.class) {
            ThaiSettings.font = font;
            ThaiSettings.size = FontChoices.clampSize(size);
        }
        try {
            if (FontManager.isLoaded()) FontManager.loadFonts();
            Settings.saveClientSettings();
        } catch (Throwable t) {
            System.err.println("[thai] apply font failed: " + t);
            t.printStackTrace();
        }
    }

    /** เรียงที่ลองวางไฟล์: %TEMP% (ถ้าไดรฟ์เดียวกับเกม) → โฟลเดอร์ข้าง ๆ เกมใน Steam library → ในโฟลเดอร์เกม */
    private static void prepareDir() throws IOException {
        Path root = Paths.get(GlobalData.rootPath()).toAbsolutePath().normalize();
        fontsDir = root.resolve("res").resolve("fonts");
        List<Path> candidates = new ArrayList<>();
        candidates.add(Paths.get(System.getProperty("java.io.tmpdir"), "necesse-thailanguage"));
        if (root.getParent() != null) candidates.add(root.getParent().resolve("necesse-thailanguage"));
        candidates.add(root.resolve("necesse-thailanguage"));
        IOException last = null;
        for (Path c : candidates) {
            Path d = c.toAbsolutePath().normalize();
            if (d.getRoot() == null || !d.getRoot().equals(fontsDir.getRoot())) continue;  // คนละไดรฟ์ relativize ไม่ได้
            try {
                Files.createDirectories(d);
                Path probe = d.resolve("write-test.tmp");
                Files.write(probe, new byte[]{1});
                Files.delete(probe);
                dir = d;
                return;
            } catch (IOException e) {
                last = e;
            }
        }
        throw last != null ? last : new IOException("no writable folder on the game's drive");
    }

    /** แตกไฟล์ฟอนต์ออกมา (ถ้ายังไม่มี/ขนาดไม่ตรง) → path สัมพัทธ์จาก res/fonts ไม่มี .ttf */
    private static String extract(String file) throws IOException {
        byte[] ttf;
        try (InputStream in = ThaiFont.class.getResourceAsStream("/thaifont/" + file)) {
            if (in == null) throw new IOException("thaifont/" + file + " not found in mod jar");
            ttf = in.readAllBytes();
        }
        Path out = dir.resolve(file);
        if (!Files.exists(out) || Files.size(out) != ttf.length) {
            Path tmp = dir.resolve(file + ".tmp");
            Files.write(tmp, ttf);
            Files.move(tmp, out, StandardCopyOption.REPLACE_EXISTING);
        }
        String name = file.endsWith(".ttf") ? file.substring(0, file.length() - 4) : file;
        return fontsDir.relativize(dir).toString().replace('\\', '/') + "/" + name;
    }

    public static TrueTypeGameFontInfo[] insert(TrueTypeGameFontInfo[] fonts) {
        try {
            TrueTypeGameFontInfo thai = get();
            if (thai == null || fonts == null || fonts.length == 0) return fonts;
            for (TrueTypeGameFontInfo f : fonts) if (f == thai) return fonts;
            TrueTypeGameFontInfo[] out = new TrueTypeGameFontInfo[fonts.length + 1];
            out[0] = fonts[0];
            out[1] = thai;
            System.arraycopy(fonts, 1, out, 2, fonts.length - 1);
            return out;
        } catch (Throwable t) {
            fail(t);
            return fonts;
        }
    }

    private static synchronized TrueTypeGameFontInfo get() {
        if (!available()) return null;
        String[] f = choices.find(ThaiSettings.font);
        int size = currentSize();
        String key = f[1] + "@" + size;
        if (info != null && key.equals(infoKey)) return info;
        try {
            info = new ScaledFontInfo(extract(f[1]), size / 100f);
            infoKey = key;
            System.out.println("[thai] Thai font loaded: " + f[0] + " (" + f[1] + ") size " + size + "%");
            return info;
        } catch (Throwable t) {
            String[] first = choices.find(null);
            if (!f[0].equals(first[0])) {  // ฟอนต์ที่เลือกโหลดไม่ได้ → กลับไปใช้ตัวแรก
                System.err.println("[thai] font " + f[0] + " failed, falling back to " + first[0] + ": " + t);
                ThaiSettings.font = first[0];
                return get();
            }
            fail(t);
            return null;
        }
    }

    private static String readText(String resource) throws IOException {
        try (InputStream in = ThaiFont.class.getResourceAsStream(resource)) {
            if (in == null) throw new IOException(resource + " not found in mod jar");
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }
    }

    private static void fail(Throwable t) {
        failed = true;
        System.err.println("[thai] font inject failed: " + t);
        t.printStackTrace();
    }
}
