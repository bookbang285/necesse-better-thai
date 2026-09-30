"""หน้า HTML ตาราง en / ทางการ / ของเรา ให้ผู้ใช้ตรวจ

py -m tools.review romance objectives   → build/review.html
"""
import html
import sys
from pathlib import Path

from tools import store
from tools.paths import BUILD

CSS = """body{font-family:Sarabun,Tahoma,sans-serif;margin:16px}table{border-collapse:collapse;width:100%}
td,th{border:1px solid #ccc;padding:4px 6px;vertical-align:top}tr.fixed td.th{background:#fff3c4}
tr.new td.th{background:#dff5e1}tr.todo td.th,tr.stale td.th{background:#fbdcdc}td.k{font-family:monospace;font-size:12px}"""


TOOLBAR = """<div id=bar style="position:sticky;top:0;background:#fff;padding:8px 0;border-bottom:1px solid #ccc">
<input id=q placeholder="ค้นหา (อังกฤษ/ไทย/key)" style="width:320px;padding:4px">
<select id=st><option value="">ทุกสถานะ</option><option>fixed</option><option>new</option><option>kept</option><option>same</option></select>
<select id=cat><option value="">ทุกหมวด</option></select> <span id=n></span></div>"""
SCRIPT = """<script>
const rows=[...document.querySelectorAll('tr[class]')],cat=document.getElementById('cat');
[...document.querySelectorAll('h2')].forEach(h=>{const o=document.createElement('option');o.textContent=h.textContent;cat.appendChild(o)});
function f(){const q=document.getElementById('q').value.toLowerCase(),s=document.getElementById('st').value,c=cat.value;let n=0;
document.querySelectorAll('table').forEach(t=>{const h=t.previousElementSibling.textContent;let vis=0;
t.querySelectorAll('tr[class]').forEach(r=>{const ok=(!q||r.textContent.toLowerCase().includes(q))&&(!s||r.className==s)&&(!c||h==c);r.style.display=ok?'':'none';if(ok){vis++;n++}});
t.style.display=t.previousElementSibling.style.display=vis?'':'none'});document.getElementById('n').textContent=n+' แถว'}
['q','st','cat'].forEach(i=>document.getElementById(i).addEventListener('input',f));f();
</script>"""


def render(files: list[Path], only: set[str] | None) -> str:
    parts = [f"<!doctype html><meta charset=utf-8><title>Thai review</title><style>{CSS}</style>", TOOLBAR]
    for path in files:
        doc = store.load(path)
        if only and doc["category"] not in only:
            continue
        parts.append(f"<h2>{html.escape(store.target_of(path))} / {html.escape(doc['category'])}</h2>")
        parts.append("<table><tr><th>key</th><th>English</th><th>ทางการเดิม</th><th>ของเรา</th><th>สถานะ</th><th>หมายเหตุ</th></tr>")
        for r in doc["entries"]:
            e = {k: html.escape(str(r.get(k, ""))) for k in ("key", "en", "official", "th", "status", "note")}
            parts.append(f'<tr class="{e["status"]}"><td class=k>{e["key"]}</td><td>{e["en"]}</td><td>{e["official"]}</td>'
                         f'<td class=th>{e["th"]}</td><td>{e["status"]}</td><td>{e["note"]}</td></tr>')
        parts.append("</table>")
    parts.append(SCRIPT)
    return "\n".join(parts)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    only = set(sys.argv[1:]) or None
    BUILD.mkdir(exist_ok=True)
    out = BUILD / "review.html"
    out.write_text(render(store.data_files(), only), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
