import json, tempfile, unittest
from pathlib import Path
from tools import apply, store


def row(key, en):
    return {"key": key, "en": en, "official": "", "th": "", "status": "todo", "note": ""}


class TestApply(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.file = Path(self.tmp.name) / "game" / "ui.json"
        store.save(self.file, {"category": "ui", "entries": [row("a", "A"), row("b", "B")], "removed": []})

    def tearDown(self):
        self.tmp.cleanup()

    def test_updates_only_allowed_fields_by_key(self):
        n = apply.apply(self.file, {"a": {"th": "เอ", "status": "new", "note": "", "en": "HACK"}})
        doc = store.load(self.file)
        self.assertEqual(n, 1)
        self.assertEqual(doc["entries"][0], {"key": "a", "en": "A", "official": "", "th": "เอ", "status": "new", "note": ""})
        self.assertEqual(doc["entries"][1]["status"], "todo")

    def test_rejects_unknown_key_and_status(self):
        with self.assertRaises(ValueError):
            apply.apply(self.file, {"zzz": {"th": "x", "status": "new"}})
        with self.assertRaises(ValueError):
            apply.apply(self.file, {"a": {"th": "x", "status": "done"}})
        self.assertEqual(store.load(self.file)["entries"][0]["th"], "")

    def test_cli_reads_patch_file(self):
        patch = Path(self.tmp.name) / "p.json"
        patch.write_text(json.dumps({"file": str(self.file), "rows": {"b": {"th": "บี", "status": "new"}}}, ensure_ascii=False), encoding="utf-8")
        apply.main([str(patch)])
        self.assertEqual(store.load(self.file)["entries"][1]["th"], "บี")
