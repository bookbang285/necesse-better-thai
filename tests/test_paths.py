import unittest
from tools import paths


class TestPaths(unittest.TestCase):
    def test_game_files_exist(self):
        self.assertTrue((paths.GAME_LOCALE / "en.lang").is_file())
        self.assertTrue(paths.GAME_JAR.is_file())
        self.assertTrue(paths.GAME_LIB.is_dir())
        self.assertTrue((paths.JDK_BIN / "javac.exe").is_file())

    def test_data_under_root(self):
        self.assertEqual(paths.DATA, paths.ROOT / "data")
        self.assertEqual(paths.LOCAL_MODS, paths.APPDATA_NECESSE / "mods")
