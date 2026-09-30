import unittest
from tools import check

G = [{"en": "Settler", "th": "ชาวนิคม", "kind": "system", "note": "", "approved": True},
     {"en": "Incursion", "th": "การบุกรุก", "kind": "system", "note": "", "approved": False}]


def row(en, th, status="new", official="", key="k"):
    return {"key": key, "en": en, "official": official, "th": th, "status": status, "note": ""}


def rules(r, category="ui", allow=frozenset(), release=False):
    return {(lvl, rule) for lvl, rule, _ in check.check_row(r, category, G, set(allow), release)}


class TestTokens(unittest.TestCase):
    def test_counts(self):
        t = check.tokens("§a<name>§r got [item=coin] x<count>\\n§#ff00aa!")
        self.assertEqual(t["<name>"], 1)
        self.assertEqual(t["[item=coin]"], 1)
        self.assertEqual(t["§a"], 1)
        self.assertEqual(t["§#ff00aa"], 1)
        self.assertEqual(t["\\n"], 1)

    def test_emoji_token(self):
        self.assertEqual(check.tokens("Kiss :heart:")[":heart:"], 1)
        self.assertIn(("error", "tokens"), rules(row("Kiss :heart:", "จูบ")))


class TestErrors(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(rules(row("Hello <name>", "สวัสดี <name>")), set())

    def test_placeholder_mismatch(self):
        self.assertIn(("error", "tokens"), rules(row("Hi <name>", "สวัสดี <mob>")))
        self.assertIn(("error", "tokens"), rules(row("Press [input=setability]", "กด")))
        self.assertIn(("error", "tokens"), rules(row("§aGreen", "เขียว")))

    def test_placeholder_reorder_ok(self):
        self.assertEqual(rules(row("<a> hits <b>", "<b> โดน <a> ตี")), set())

    def test_newline_count_is_warning(self):
        self.assertIn(("warn", "newline"), rules(row("a\\nb", "ก ข")))

    def test_empty_th_not_todo(self):
        self.assertIn(("error", "empty"), rules(row("A", "", status="new")))
        self.assertEqual(rules(row("A", "", status="todo")), set())

    def test_release_blocks_todo_and_stale(self):
        self.assertIn(("error", "unfinished"), rules(row("A", "", status="todo"), release=True))
        self.assertIn(("error", "unfinished"), rules(row("A", "เอ", status="stale"), release=True))

    def test_control_and_zero_width_chars(self):
        self.assertIn(("error", "chars"), rules(row("A", "เอ​")))
        self.assertIn(("error", "chars"), rules(row("A", "เอ\nบี")))

    def test_whitespace_edges(self):
        self.assertIn(("error", "whitespace"), rules(row("A", " เอ")))

    def test_bad_status(self):
        self.assertIn(("error", "status"), rules(row("A", "เอ", status="done")))


class TestWarnings(unittest.TestCase):
    def test_glossary_only_approved(self):
        self.assertIn(("warn", "glossary"), rules(row("A settler arrived", "มีผู้อพยพมา")))
        self.assertEqual(rules(row("A settler arrived", "มีชาวนิคมมา")), set())
        self.assertEqual(rules(row("Incursion", "อะไรก็ได้")), set())

    def test_glossary_whole_word_allows_plural(self):
        g = [{"en": "Hat", "th": "หมวก", "kind": "item", "note": "", "approved": True}]
        def r(en, th):
            return {x[1] for x in check.check_row(row(en, th), "item", g, set(), False)}
        self.assertNotIn("glossary", r("Hatchling", "ลูกนก"))
        self.assertIn("glossary", r("Two hats", "สองใบ"))

    def test_glossary_ignores_placeholders(self):
        g = [{"en": "Mob", "th": "มอนสเตอร์", "kind": "system", "note": "", "approved": True}]
        found = {x[1] for x in check.check_row(row("Kill <mob>", "ฆ่า <mob>"), "ui", g, set(), False)}
        self.assertNotIn("glossary", found)

    def test_misspelling(self):
        self.assertIn(("warn", "spelling"), rules(row("Set", "ครบเช็ท")))

    def test_gendered_npc(self):
        self.assertIn(("warn", "gender"), rules(row("Thanks", "ขอบคุณครับ"), category="romance"))
        self.assertEqual(rules(row("Thanks", "ขอบคุณครับ"), category="ui"), set())
        self.assertEqual(rules(row("Thanks", "ขอบคุณครับ", key="k"), category="romance", allow={"romance.k"}), set())

    def test_same_as_english(self):
        self.assertIn(("warn", "same"), rules(row("Nachos", "Nachos", status="new")))
        self.assertEqual(rules(row("Nachos", "Nachos", status="same")), set())

    def test_too_long_ui(self):
        self.assertIn(("warn", "length"), rules(row("Save", "บันทึกเกมทั้งหมดตอนนี้เลยนะ"), category="ui"))


class TestCollisions(unittest.TestCase):
    def test_same_key_different_th(self):
        a = ("data/game/item.json", {"category": "item", "entries": [row("A", "เอ", key="x")]})
        b = ("data/mods/m/item.json", {"category": "item", "entries": [row("A", "บี", key="x")]})
        c = ("data/mods/n/item.json", {"category": "item", "entries": [row("A", "เอ", key="x")]})
        self.assertEqual(len(check.check_collisions([a, b])), 1)
        self.assertEqual(check.check_collisions([a, c]), [])
