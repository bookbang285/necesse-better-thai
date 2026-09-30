import json, shutil, unittest
from tools import checkpoint, paths


class TestCheckpoint(unittest.TestCase):
    def setUp(self):
        paths.DATA.mkdir(exist_ok=True)
        self.probe = paths.DATA / "_probe.json"
        self.probe.write_text(json.dumps({"n": 1}), encoding="utf-8")
        self.made = None

    def tearDown(self):
        self.probe.unlink(missing_ok=True)
        if self.made and self.made.exists():
            shutil.rmtree(self.made)

    def test_copies_data_and_tools(self):
        self.made = checkpoint.make("unittest-probe")
        self.assertTrue((self.made / "data" / "_probe.json").exists())
        self.assertTrue((self.made / "tools" / "checkpoint.py").exists())

    def test_sanitizes_label(self):
        self.made = checkpoint.make("../../x")
        self.assertTrue(str(self.made).startswith(str(paths.ROOT / "checkpoints")))
        self.assertNotIn("/", self.made.name)
        self.assertNotIn("\\", self.made.name)

    def test_sanitizes_backslash_label(self):
        self.made = checkpoint.make("a\\b")
        self.assertEqual(self.made.parent, paths.ROOT / "checkpoints")
        self.assertTrue(self.made.name.endswith("a_b"))
