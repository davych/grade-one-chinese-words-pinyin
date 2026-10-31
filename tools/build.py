"""Rebuild the standalone HTML using only the Python standard library."""
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
template = (root / "tools/index.template.html").read_text(encoding="utf-8")
for marker, filename in [("__WORDS__", "words.json"), ("__STROKES__", "strokes.json")]:
    data = json.loads((root / "data" / filename).read_text(encoding="utf-8"))
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = template.replace(marker, payload)
template = template.replace("__LICENSE__", html.escape((root / "data/ARPHICPL.TXT").read_text(encoding="utf-8")))
(root / "index.html").write_text(template, encoding="utf-8")
print(f"Created {root / 'index.html'} ({len(template.encode('utf-8')):,} bytes)")
