package thailanguage;

import necesse.gfx.forms.Form;
import necesse.gfx.forms.components.FormComponent;
import necesse.gfx.forms.components.FormInputSize;
import necesse.gfx.forms.components.FormSlider;
import necesse.gfx.forms.components.FormTextButton;
import necesse.gfx.forms.components.lists.FormLanguageList;
import necesse.gfx.forms.components.localComponents.FormLocalTextButton;
import necesse.gfx.gameFont.FontOptions;
import necesse.gfx.ui.ButtonColor;

/** ส่วน "ฟอนต์ภาษาไทย" ในหน้า ตั้งค่า → ภาษา ของเกม (ใต้รายการภาษา เหนือปุ่มช่วยแปล)
 *  ปุ่มกดวนเปลี่ยนฟอนต์ + แถบเลื่อนขนาด — เปลี่ยนแล้วสร้างฟอนต์ใหม่ทันทีและเซฟค่า */
public final class ThaiFontMenu {
    static final int AREA = 64;  // ความสูงที่กันไว้ใต้รายการภาษา
    private static FormTextButton fontButton;
    private static SizeSlider sizeSlider;

    private ThaiFontMenu() {}

    static String label(String text) {
        return ThaiFont.available() ? ThaiShaper.shape(text) : text;
    }

    public static void addTo(Form language) {
        fontButton = null;
        sizeSlider = null;
        if (language == null || ThaiFont.choices() == null) return;
        int w = language.getWidth() - 20;
        fontButton = (FormTextButton) language.addComponent((FormComponent) new FormTextButton(
                fontText(), 10, 0, w, FormInputSize.SIZE_24, ButtonColor.BASE));
        fontButton.onClicked(e -> {
            ThaiFont.apply(ThaiFont.choices().next(ThaiFont.currentFont()), ThaiFont.currentSize());
            fontButton.setText(fontText());
        });
        sizeSlider = (SizeSlider) language.addComponent((FormComponent) new SizeSlider(
                label("ขนาดตัวอักษรไทย"), 10, 0, ThaiFont.currentSize(), w));
        sizeSlider.onGrab(e -> {
            if (!sizeSlider.isGrabbed()) applySize();          // ปล่อยเมาส์ → ค่อยสร้างฟอนต์ใหม่ (ไม่ทำทุกครั้งที่ลาก)
        });
        sizeSlider.onChanged(e -> {
            if (!sizeSlider.isGrabbed()) applySize();          // คีย์บอร์ด/จอย/คลิกตรงแถบ
        });
    }

    private static void applySize() {
        if (sizeSlider.getValue() != ThaiFont.currentSize()) {
            ThaiFont.apply(ThaiFont.currentFont(), sizeSlider.getValue());
        }
    }

    private static String fontText() {
        return label("ฟอนต์ภาษาไทย: " + ThaiFont.currentFont() + "  (กดเพื่อเปลี่ยน)");
    }

    /** เรียกหลัง updateLanguageHeight ของเกม: ย่อรายการภาษาแล้ววางส่วนของเราเหนือปุ่มช่วยแปล */
    public static void layout(FormLanguageList list, FormLocalTextButton help) {
        if (fontButton == null || list == null || help == null) return;
        int top = help.getY() - AREA;
        list.setHeight(Math.max(40, top - 4 - list.getY()));
        fontButton.setY(top);
        sizeSlider.setY(top + 30);
    }

    static class SizeSlider extends FormSlider {
        SizeSlider(String text, int x, int y, int value, int width) {
            super(text, x, y, value, FontChoices.MIN_SIZE, FontChoices.MAX_SIZE, width, new FontOptions(12));
        }

        @Override
        public String getValueText() {
            return getValue() + "%";
        }
    }
}
