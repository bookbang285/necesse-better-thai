import tempfile, unittest, zipfile
from pathlib import Path
from tools import servermods

CLIENT = """{
\t{
\t\tid = bolo.bettertorch,
\t\tname = A Better Torch,
\t\ttype = STEAM_MOD,
\t\tenabled = true
\t},
\t{
\t\tid = aphoreateam.aphoreamod,
\t\tname = Aphorea Mod,
\t\ttype = STEAM_MOD,
\t\tenabled = true
\t},
\t{
\t\tid = off.mod,
\t\tname = Off,
\t\ttype = STEAM_MOD,
\t\tenabled = false
\t},
\t{
\t\tid = thaicommunity.thailanguage,
\t\tname = Thai Language,
\t\ttype = FILE_MOD,
\t\tenabled = true
\t}
}"""


def jar(path: Path, modid: str, version: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("mod.info", f"{{\n\tid = {modid},\n\tversion = {version},\n}}")
    return path


class TestParse(unittest.TestCase):
    def test_enabled_in_order(self):
        mods = servermods.parse_modlist(CLIENT)
        self.assertEqual([(m.id, m.name, m.enabled) for m in mods][:3],
                         [("bolo.bettertorch", "A Better Torch", True), ("aphoreateam.aphoreamod", "Aphorea Mod", True), ("off.mod", "Off", False)])

    def test_render_file_mods_roundtrip(self):
        text = servermods.render_modlist([servermods.Mod("a.b", "A B", True)])
        self.assertIn("type = FILE_MOD", text)
        self.assertEqual([(m.id, m.enabled) for m in servermods.parse_modlist(text)], [("a.b", True)])


class TestSync(unittest.TestCase):
    def test_copies_enabled_jars_in_order_and_skips_thai_and_missing(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "client").mkdir()
            (d / "client" / "modlist.data").write_text(CLIENT, encoding="utf-8")
            ws = d / "workshop"
            jar(ws / "1" / "ABetterTorch-1.jar", "bolo.bettertorch", "1.2.1")
            jar(ws / "2" / "Aphorea-1.jar", "aphoreateam.aphoreamod", "1.0.38")
            out = d / "server" / "mods"
            jar(out / "old-aphorea.jar", "aphoreateam.aphoreamod", "1.0.37")
            report = servermods.sync(d / "client" / "modlist.data", ws, out)
            names = sorted(p.name for p in out.glob("*.jar"))
            modlist = servermods.parse_modlist((out / "modlist.data").read_text(encoding="utf-8"))
        self.assertEqual(names, ["ABetterTorch-1.jar", "Aphorea-1.jar"])
        self.assertEqual([m.id for m in modlist], ["bolo.bettertorch", "aphoreateam.aphoreamod"])
        self.assertEqual(report.missing, [])
        self.assertIn("aphoreateam.aphoreamod", report.changed)

    def test_reports_missing_jar(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "modlist.data").write_text(CLIENT, encoding="utf-8")
            report = servermods.sync(d / "modlist.data", d / "ws", d / "mods")
        self.assertEqual(report.missing, ["bolo.bettertorch", "aphoreateam.aphoreamod"])
