#!/usr/bin/env python3
"""
MAGICKMICA - refresh_hero.py
Refreshes the hero tile on all 16 homepages in place:
  - the background picture  -> cover of the newest article
  - "N transmissions and counting" -> the current note count

Why not just rerun build_index.py: the live homepages carry changes made
after it was last run (the og-card meta tags, the CH 05 Crystal Stress Index
tile, the CH 06 store tile). A full rebuild would drop them. This touches
only the hero tile, so it is safe to run after every notes/articles refresh.

usage: python3 tools/refresh_hero.py <repo> <data_dir> <out_dir>
Writes only the pages that change into out_dir.
"""
import html, json, os, re, sys

repo = sys.argv[1] if len(sys.argv) > 1 else "."
data_dir = sys.argv[2] if len(sys.argv) > 2 else "_data"
out_dir = sys.argv[3] if len(sys.argv) > 3 else "build"

articles = json.load(open(os.path.join(data_dir, "magazine_articles.json"), encoding="utf-8"))
notes = json.load(open(os.path.join(data_dir, "notes_with_media_compact.json"), encoding="utf-8"))
themes = json.load(open(os.path.join(data_dir, "themes.json"), encoding="utf-8"))

latest = max((a for a in articles if a.get("cover_url")), key=lambda a: a["date"])
cover = html.escape(latest["cover_url"], quote=True)
count = f"{len(notes):,}"

HERO_IMG = re.compile(r'(<a class="tile hero" href="articles\.html"><img src=")[^"]*(")')
COUNT = re.compile(r'(<div class="sm">)[\d,]+( transmissions and counting\.)')

os.makedirs(out_dir, exist_ok=True)
changed = []
for fname in themes:
    path = os.path.join(repo, fname)
    if not os.path.exists(path):
        print(f"  missing: {fname}")
        continue
    src = open(path, encoding="utf-8").read()
    new, n1 = HERO_IMG.subn(lambda m: m.group(1) + cover + m.group(2), src, count=1)
    new, n2 = COUNT.subn(lambda m: m.group(1) + count + m.group(2), new, count=1)
    if n1 != 1 or n2 != 1:
        print(f"  hero not found in {fname} (img {n1}, count {n2}) - left alone")
        continue
    if new != src:
        open(os.path.join(out_dir, fname), "w", encoding="utf-8").write(new)
        changed.append(fname)

print(f"hero: {latest['title']} ({latest['date']}), {count} transmissions")
print(f"wrote {len(changed)} of {len(themes)} homepages")
