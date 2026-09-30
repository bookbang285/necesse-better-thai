package thailanguage;

import java.io.IOException;
import necesse.gfx.gameFont.TrueTypeGameFontInfo;

/** ฟอนต์ไทยที่ขยายขนาด — ตัวไทยที่ขนาด em เท่าตัวละตินดูเล็กและบางกว่า FreeSans Bold มาก */
public class ScaledFontInfo extends TrueTypeGameFontInfo {
    private final float scale;

    public ScaledFontInfo(String file, float scale) throws IOException {
        super(file);
        this.scale = scale;
    }

    @Override
    public synchronized float getFontSize(int size) {
        return super.getFontSize(size) * this.scale;
    }

    @Override
    public synchronized float getLineGap(int size) {
        return super.getLineGap(size) * this.scale;
    }
}
