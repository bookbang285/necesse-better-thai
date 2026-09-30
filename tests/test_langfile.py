import unittest
from tools import langfile
from tools.langfile import Entry

SAMPLE = """// comment
[lang]
localname=ไทย

[item]
coinpouch=ถุงใส่เหรียญ
MISSING_TRANSLATION:scrap=Scrap
SAME_TRANSLATION:nachos=Nachos
runicset1=Press [input=setability] to gain
unknown line without equals
[ui]
a=1
[item]
coinpouch=ถุงเหรียญ
"""


class TestParse(unittest.TestCase):
    def setUp(self):
        self.entries = langfile.parse(SAMPLE)

    def test_flags_stripped_from_key(self):
        m = langfile.to_map(self.entries)
        self.assertEqual(m[("item", "scrap")].flag, "missing")
        self.assertEqual(m[("item", "nachos")].flag, "same")
        self.assertIsNone(m[("item", "runicset1")].flag)

    def test_split_on_first_equals(self):
        m = langfile.to_map(self.entries)
        self.assertEqual(m[("item", "runicset1")].value, "Press [input=setability] to gain")

    def test_repeated_category_and_duplicate_key_last_wins(self):
        m = langfile.to_map(self.entries)
        self.assertEqual(m[("item", "coinpouch")].value, "ถุงเหรียญ")
        self.assertEqual(langfile.categories(self.entries), ["lang", "item", "ui"])

    def test_comments_blank_unknown_ignored(self):
        keys = [(e.category, e.key) for e in self.entries]
        self.assertNotIn(("item", "unknown line without equals"), keys)
        self.assertEqual(len(self.entries), 7)

    def test_value_keeps_literal_backslash_n(self):
        e = langfile.parse("[a]\nk=one\\ntwo\n")[0]
        self.assertEqual(e.value, "one\\ntwo")

    def test_bom_and_crlf(self):
        e = langfile.parse("﻿[a]\r\nk=v\r\n")[0]
        self.assertEqual((e.category, e.key, e.value), ("a", "k", "v"))


class TestDump(unittest.TestCase):
    def test_groups_categories_and_roundtrips(self):
        rows = [("item", "a", "ก"), ("item", "b", "ข\\nค"), ("ui", "c", "[input=x] ง")]
        text = langfile.dump(rows, header="// hi")
        self.assertTrue(text.startswith("// hi\n"))
        self.assertEqual(text.count("[item]"), 1)
        back = [(e.category, e.key, e.value) for e in langfile.parse(text)]
        self.assertEqual(back, rows)

    def test_rejects_real_newline(self):
        with self.assertRaises(ValueError):
            langfile.dump([("item", "a", "x\ny")])

    def test_rejects_equals_in_key(self):
        with self.assertRaises(ValueError):
            langfile.dump([("item", "a=b", "x")])
