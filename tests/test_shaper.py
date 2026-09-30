import subprocess, tempfile, unittest
from pathlib import Path
from tools import thaifont
from tools.paths import JDK_BIN, MOD_DIR


class TestThaiShaperJava(unittest.TestCase):
    def test_java_shaper(self):
        with tempfile.TemporaryDirectory() as d:
            src = [str(MOD_DIR / "src" / "thailanguage" / "ThaiShaper.java"), str(MOD_DIR / "test" / "ThaiShaperTest.java")]
            r = subprocess.run([str(JDK_BIN / "javac.exe"), "--release", "17", "-encoding", "UTF-8", "-d", d, *src],
                               capture_output=True, text=True, errors="replace")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            r = subprocess.run([str(JDK_BIN / "java.exe"), "-cp", d, "ThaiShaperTest"], capture_output=True, text=True, errors="replace")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_java_font_choices(self):
        with tempfile.TemporaryDirectory() as d:
            src = [str(MOD_DIR / "src" / "thailanguage" / "FontChoices.java"), str(MOD_DIR / "test" / "FontChoicesTest.java")]
            r = subprocess.run([str(JDK_BIN / "javac.exe"), "--release", "17", "-encoding", "UTF-8", "-d", d, *src],
                               capture_output=True, text=True, errors="replace")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            r = subprocess.run([str(JDK_BIN / "java.exe"), "-cp", d, "FontChoicesTest"], capture_output=True, text=True, errors="replace")
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_codepoints_match_python(self):
        java = (MOD_DIR / "src" / "thailanguage" / "ThaiShaper.java").read_text(encoding="utf-8")
        for name in ("TONE_HIGH", "TONE_LOW_LEFT", "TONE_HIGH_LEFT", "UPPER_LEFT", "LOWER_LOW"):
            self.assertIn(f"{name} = 0x{getattr(thaifont, name):04X}", java, name)
