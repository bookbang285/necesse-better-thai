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
import necesse.gfx.gameFont.TrueTypeGameFontInfo;

/** ฟอนต์ไทย: แตกไฟล์จาก jar ไปโฟลเดอร์ที่อยู่ไดรฟ์เดียวกับเกม (เกมเปิดฟอนต์ด้วย path สัมพัทธ์จาก res/fonts/ เท่านั้น)
 *  แล้วแทรกเข้า fallback chain ถัดจาก base
 *  available() = เตรียมไฟล์ได้ → ค่อยสลับรูปสระเป็น PUA (ไม่งั้นสระจะกลายเป็นกล่อง เพราะฟอนต์อื่นไม่มี PUA) */
public final class ThaiFont {
    private static String relPath;       // path สัมพัทธ์จาก <root>/res/fonts/ (ไม่มี .ttf)
    private static boolean prepared;
    private static TrueTypeGameFontInfo info;
    private static boolean failed;

    private ThaiFont() {}

    public static synchronized boolean available() {
        if (!prepared) {
            prepared = true;
            try {
                relPath = extract();
                System.out.println("[thai] Thai font file ready: " + relPath);
            } catch (Throwable t) {
                fail(t);
            }
        }
        return relPath != null && !failed;
    }

    /** เรียงที่ลองวางไฟล์: %TEMP% (ถ้าไดรฟ์เดียวกับเกม) → โฟลเดอร์ข้าง ๆ เกมใน Steam library → ในโฟลเดอร์เกม */
    private static String extract() throws IOException {
        Path root = Paths.get(GlobalData.rootPath()).toAbsolutePath().normalize();
        Path fontsDir = root.resolve("res").resolve("fonts");
        List<Path> candidates = new ArrayList<>();
        candidates.add(Paths.get(System.getProperty("java.io.tmpdir"), "necesse-thailanguage"));
        if (root.getParent() != null) candidates.add(root.getParent().resolve("necesse-thailanguage"));
        candidates.add(root.resolve("necesse-thailanguage"));
        byte[] ttf;
        try (InputStream in = ThaiFont.class.getResourceAsStream("/thaifont/thai.ttf")) {
            if (in == null) throw new IOException("thaifont/thai.ttf not found in mod jar");
            ttf = in.readAllBytes();
        }
        IOException last = null;
        for (Path c : candidates) {
            Path dir = c.toAbsolutePath().normalize();
            if (dir.getRoot() == null || !dir.getRoot().equals(fontsDir.getRoot())) continue;  // คนละไดรฟ์ relativize ไม่ได้
            try {
                Files.createDirectories(dir);
                Path file = dir.resolve("thai.ttf");
                Path tmp = dir.resolve("thai.ttf.tmp");
                Files.write(tmp, ttf);
                Files.move(tmp, file, StandardCopyOption.REPLACE_EXISTING);
                return fontsDir.relativize(dir).toString().replace('\\', '/') + "/thai";
            } catch (IOException e) {
                last = e;
            }
        }
        throw last != null ? last : new IOException("no writable folder on the game's drive");
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
        if (info != null) return info;
        if (!available()) return null;
        try {
            float scale = readScale();
            info = new ScaledFontInfo(relPath, scale);
            System.out.println("[thai] Thai font loaded: " + relPath + " scale " + scale);
            return info;
        } catch (Throwable t) {
            fail(t);
            return null;
        }
    }

    private static float readScale() {
        try (InputStream in = ThaiFont.class.getResourceAsStream("/thaifont/scale.txt")) {
            if (in == null) return 1f;
            float s = Float.parseFloat(new String(in.readAllBytes(), StandardCharsets.US_ASCII).trim());
            return s > 0.5f && s < 2f ? s : 1f;
        } catch (Throwable t) {
            return 1f;
        }
    }

    private static void fail(Throwable t) {
        failed = true;
        System.err.println("[thai] font inject failed: " + t);
        t.printStackTrace();
    }
}
