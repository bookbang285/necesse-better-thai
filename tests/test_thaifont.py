import tempfile, unittest
from pathlib import Path
from fontTools.ttLib import TTFont
from tools import thaifont
from tools.paths import MOD_DIR

SRC = MOD_DIR / "fonts" / "Prompt-Medium.ttf"


class TestThaiFont(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "thai.ttf"
        thaifont.make(SRC, cls.out)
        cls.font = TTFont(cls.out)
        cls.cmap = cls.font.getBestCmap()

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def bounds(self, cp):
        g = self.font["glyf"][self.cmap[cp]]
        return g.xMin, g.yMin, g.xMax, g.yMax

    def test_all_pua_codepoints_mapped(self):
        for cp in thaifont.PUA:
            self.assertIn(cp, self.cmap, hex(cp))

    def test_high_tone_sits_above_upper_vowel(self):
        sara_ii_top = self.bounds(0x0E35)[3]
        self.assertGreater(self.bounds(thaifont.TONE_HIGH + 0)[1], sara_ii_top - 10)

    def test_left_variants_shift_left(self):
        self.assertLess(self.bounds(thaifont.TONE_LOW_LEFT + 0)[0], self.bounds(0x0E48)[0] - 100)
        self.assertLess(self.bounds(thaifont.UPPER_LEFT + 2)[0], self.bounds(0x0E35)[0] - 100)
        hl = self.bounds(thaifont.TONE_HIGH_LEFT + 1)
        self.assertLess(hl[0], self.bounds(thaifont.TONE_HIGH + 1)[0] - 100)
        self.assertEqual(hl[1], self.bounds(thaifont.TONE_HIGH + 1)[1])

    def test_marks_have_zero_advance(self):
        hmtx = self.font["hmtx"]
        for cp in thaifont.PUA:
            self.assertEqual(hmtx[self.cmap[cp]][0], 0, hex(cp))

    def test_high_tone_capped_to_fit_button_box(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "capped.ttf"
            thaifont.make(MOD_DIR / "fonts" / "Prompt-Medium.ttf", out, high_cap=0.93)
            f = TTFont(out)
            cm, glyf = f.getBestCmap(), f["glyf"]
            upem = f["head"].unitsPerEm
            for cp in [thaifont.TONE_HIGH + i for i in range(5)] + [thaifont.TONE_HIGH_LEFT + i for i in range(5)]:
                g = glyf[cm[cp]]
                g.recalcBounds(glyf)
                self.assertLessEqual(g.yMax, 0.93 * upem + 1, hex(cp))
            self.assertEqual(cm[0x0E48], "uni0E48")

    def test_original_thai_untouched(self):
        self.assertEqual(self.cmap[0x0E48], "uni0E48")
