import tempfile, unittest
from pathlib import Path
from tools import glossary, review, split, store


def row(key, en, official="", th="", status="todo"):
    return {"key": key, "en": en, "official": official, "th": th, "status": status, "note": ""}


class TestSplit(unittest.TestCase):
    def test_balanced_and_covers_everything(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store.save(root / "game" / "romance.json", {"category": "romance", "entries": [row(f"r{i}", "x") for i in range(100)], "removed": []})
            store.save(root / "game" / "ui.json", {"category": "ui", "entries": [row(f"u{i}", "x") for i in range(40)], "removed": []})
            store.save(root / "game" / "item.json", {"category": "item", "entries": [row(f"i{i}", "x") for i in range(20)], "removed": []})
            groups = split.plan(store.data_files(root), 4)
        self.assertEqual(len(groups), 4)
        sizes = [sum(e - s for _, s, e in g) for g in groups]
        self.assertEqual(sum(sizes), 160)
        self.assertLessEqual(max(sizes) - min(sizes), 40)
        covered = sorted((p, i) for g in groups for p, s, e in g for i in range(s, e))
        self.assertEqual(len(covered), len(set(covered)))


class TestGlossary(unittest.TestCase):
    def test_collects_official_variants(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store.save(root / "game" / "mob.json", {"category": "mob", "entries": [row("a", "Crone", "ยายเฒ่า")], "removed": []})
            store.save(root / "game" / "ui.json", {"category": "ui", "entries": [row(f"u{i}", "Your Settler is hungry", "ผู้อพยพหิว") for i in range(6)], "removed": []})
            cands = glossary.candidates(store.data_files(root))
        by = {c["en"]: c for c in cands}
        self.assertEqual(by["Crone"]["official_variants"], {"ยายเฒ่า": 1})
        self.assertIn("Settler", by)


class TestReview(unittest.TestCase):
    def test_html_escapes_and_filters(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            store.save(root / "game" / "ui.json", {"category": "ui", "entries": [row("a", "<name> & co", "x", "<name> และพวก", "fixed")], "removed": []})
            store.save(root / "game" / "item.json", {"category": "item", "entries": [row("b", "B")], "removed": []})
            html = review.render(store.data_files(root), {"ui"})
        self.assertIn("&lt;name&gt; &amp; co", html)
        self.assertNotIn(">b<", html)
        self.assertIn('class="fixed"', html)
