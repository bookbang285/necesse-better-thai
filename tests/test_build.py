import tempfile, unittest, zipfile
from pathlib import Path
from tools import build, langfile, store


def row(key, en, official, th, status):
    return {"key": key, "en": en, "official": official, "th": th, "status": status, "note": ""}


class TestInclude(unittest.TestCase):
    def test_rules(self):
        self.assertFalse(build.include(row("a", "A", "เอ", "เอ", "kept")))
        self.assertTrue(build.include(row("a", "A", "เอ", "เอ๋", "fixed")))
        self.assertTrue(build.include(row("a", "A", "", "เอ", "new")))
        self.assertFalse(build.include(row("a", "A", "", "", "todo")))
        self.assertFalse(build.include(row("a", "Nachos", "Nachos", "Nachos", "same")))
        self.assertTrue(build.include(row("a", "Nachos", "", "Nachos", "same")))
        self.assertTrue(build.include(row("a", "B", "เอ", "บี", "stale")))


class TestCollect(unittest.TestCase):
    def test_order_and_mod_ids(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store.save(root / "game" / "ui.json", {"category": "ui", "entries": [row("u", "U", "", "ยู", "new")], "removed": []})
            store.save(root / "game" / "item.json", {"category": "item", "entries": [row("i", "I", "ไอ", "ไอ", "kept"), row("j", "J", "", "เจ", "new")], "removed": []})
            store.save(root / "mods" / "z.mod" / "item.json", {"category": "item", "entries": [row("m", "M", "", "เอ็ม", "new")], "removed": []})
            store.save(root / "mods" / "y.mod" / "item.json", {"category": "item", "entries": [row("n", "N", "", "", "todo")], "removed": []})
            rows, mods = build.collect(store.data_files(root))
        self.assertEqual(rows, [("item", "j", "เจ"), ("ui", "u", "ยู"), ("item", "m", "เอ็ม")])
        self.assertEqual(mods, ["z.mod"])
        langfile.dump(rows)  # ต้องไม่ error


class TestAppendEnglish(unittest.TestCase):
    def test_names_get_english_in_parens(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store.save(root / "game" / "item.json", {"category": "item", "entries": [
                row("ironbar", "Iron Bar", "แท่งเหล็ก", "แท่งเหล็ก", "kept"),
                row("x", "<mob> Banner", "", "ธง<mob>", "new"),
                row("nachos", "Nachos", "Nachos", "Nachos", "same"),
                row("t", "Todo", "", "", "todo")], "removed": []})
            store.save(root / "game" / "ui.json", {"category": "ui", "entries": [row("u", "Save", "บันทึก", "บันทึก", "kept")], "removed": []})
            rows, _ = build.collect(store.data_files(root), append_english={"item"})
        self.assertEqual(rows, [("item", "ironbar", "แท่งเหล็ก (Iron Bar)"), ("item", "x", "ธง<mob>")])

    def test_render(self):
        cfg = {"modid": "thaicommunity.thailanguage", "name": "Thai Language", "version": "0.1.0",
               "gameVersion": "1.3.3", "author": "a", "description": "d"}
        tpl = (Path(build.MOD_DIR) / "mod.info.template").read_text(encoding="utf-8")
        text = build.render_modinfo(tpl, cfg, ["a.b", "c.d"])
        self.assertIn("id = thaicommunity.thailanguage,", text)
        self.assertIn("clientside = true", text)
        self.assertIn("optionalDependencies = [a.b, c.d]", text)


class TestJar(unittest.TestCase):
    def test_single_th_lang_under_resources(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            classes = d / "classes" / "thailanguage"
            classes.mkdir(parents=True)
            (classes / "X.class").write_bytes(b"\xca\xfe")
            font = d / "f.ttf"
            font.write_bytes(b"ttf")
            jar = d / "out.jar"
            lic = d / "OFL.txt"
            lic.write_text("SIL OFL", encoding="utf-8")
            prev = d / "p.png"
            prev.write_bytes(b"png")
            build.make_jar(jar, "{\n}", "[item]\na=ก\n", d / "classes", font, 1.2, lic, prev)
            with zipfile.ZipFile(jar) as z:
                names = z.namelist()
                self.assertEqual(z.read("resources/locale/th.lang").decode("utf-8"), "[item]\na=ก\n")
                self.assertEqual(z.read("thaifont/scale.txt").decode("ascii"), "1.2")
                self.assertEqual(z.read("thaifont/OFL.txt").decode("utf-8"), "SIL OFL")
                self.assertEqual(z.read("resources/preview.png"), b"png")
        self.assertIn("mod.info", names)
        self.assertIn("thailanguage/X.class", names)
        self.assertIn("thaifont/thai.ttf", names)
        self.assertEqual([n for n in names if n.startswith("resources/") and n.endswith("th.lang")],
                         ["resources/locale/th.lang"])
