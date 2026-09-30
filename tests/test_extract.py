import io, unittest, zipfile
from pathlib import Path
from tools import extract, store
from tools.langfile import Entry


class TestMerge(unittest.TestCase):
    def test_new_doc_all_todo_in_en_order(self):
        doc = extract.merge(None, "item", [("b", "B"), ("a", "A")], {"a": "เอ"})
        self.assertEqual([r["key"] for r in doc["entries"]], ["b", "a"])
        a = doc["entries"][1]
        self.assertEqual((a["en"], a["official"], a["th"], a["status"]), ("A", "เอ", "", "todo"))
        self.assertEqual(doc["removed"], [])

    def test_keeps_translation_when_en_unchanged(self):
        doc = extract.merge(None, "item", [("a", "A")], {"a": "เอ"})
        doc["entries"][0].update(th="เอเอ", status="fixed", note="x")
        doc2 = extract.merge(doc, "item", [("a", "A")], {"a": "เอ2"})
        r = doc2["entries"][0]
        self.assertEqual((r["th"], r["status"], r["note"], r["official"]), ("เอเอ", "fixed", "x", "เอ2"))

    def test_kept_row_follows_new_official(self):
        doc = extract.merge(None, "item", [("a", "A")], {"a": "เอ"})
        doc["entries"][0].update(th="เอ", status="kept")
        r = extract.merge(doc, "item", [("a", "A")], {"a": "เอใหม่"})["entries"][0]
        self.assertEqual((r["th"], r["status"], r["official"]), ("เอใหม่", "kept", "เอใหม่"))

    def test_en_changed_marks_stale_and_keeps_prev(self):
        doc = extract.merge(None, "item", [("a", "Old")], {})
        doc["entries"][0].update(th="เก่า", status="new")
        r = extract.merge(doc, "item", [("a", "New")], {})["entries"][0]
        self.assertEqual((r["status"], r["th"], r["en"], r["en_prev"]), ("stale", "เก่า", "New", "Old"))

    def test_en_changed_on_todo_stays_todo(self):
        doc = extract.merge(None, "item", [("a", "Old")], {})
        r = extract.merge(doc, "item", [("a", "New")], {})["entries"][0]
        self.assertEqual(r["status"], "todo")
        self.assertNotIn("en_prev", r)

    def test_removed_key_moves_to_removed(self):
        doc = extract.merge(None, "item", [("a", "A"), ("b", "B")], {})
        doc2 = extract.merge(doc, "item", [("a", "A")], {})
        self.assertEqual([r["key"] for r in doc2["removed"]], ["b"])
        doc3 = extract.merge(doc2, "item", [("a", "A"), ("b", "B")], {})
        self.assertEqual(doc3["removed"], [])
        self.assertEqual([r["key"] for r in doc3["entries"]], ["a", "b"])


class TestOfficial(unittest.TestCase):
    def test_missing_is_empty(self):
        self.assertEqual(extract.official_value(Entry("i", "k", "Scrap", "missing")), "")
        self.assertEqual(extract.official_value(Entry("i", "k", "Nachos", "same")), "Nachos")
        self.assertEqual(extract.official_value(None), "")


class TestModJar(unittest.TestCase):
    def test_reads_modinfo_and_langs(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("mod.info", "{\n\tid = a.b,\n\tname = X,\n\tclientside = false\n}")
            z.writestr("resources/locale/en.lang", "[item]\nk=V\n")
        p = Path(self.id() + ".jar")
        p.write_bytes(buf.getvalue())
        try:
            modid, en, th = extract.read_mod_jar(p)
        finally:
            p.unlink()
        self.assertEqual((modid, en, th), ("a.b", "[item]\nk=V\n", None))

    def test_parse_modinfo(self):
        info = extract.parse_modinfo("{\n\tid = aphoreateam.aphoreamod,\n\tversion = 1.0.38,\n}")
        self.assertEqual(info["id"], "aphoreateam.aphoreamod")
        self.assertEqual(info["version"], "1.0.38")


class TestStore(unittest.TestCase):
    def test_target_of(self):
        self.assertEqual(store.target_of(Path("data/game/item.json")), "game")
        self.assertEqual(store.target_of(Path("data/mods/a.b/item.json")), "a.b")
