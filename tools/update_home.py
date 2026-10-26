#!/usr/bin/env python3
"""
MAGICKMICA - update_home.py
Keeps the big "Now broadcasting" tile on index.html and every index-*.html current:

  - its picture becomes the cover of the newest article
  - "N transmissions and counting" becomes the current note count

Nothing else on those pages is touched, so hand edits survive. (build_index.py
regenerates the whole page from its template; this only swaps those two things.)

    python3 tools/update_home.py <repo> <data_dir>
Run by update_all.py on every update.
"""
import glob
import html
import json
import os
import re
import sys
from urllib.parse import quote, unquote

COVER_CDN = ("https://substackcdn.com/image/fetch/"
             "$s_!G4Yk!,w_600,c_limit,f_webp,q_auto:good,fl_progressive:steep/")
S3 = "https://substack-post-media.s3.amazonaws.com/public/images/"

HERO_IMG = re.compile(
    r'(<a class="tile hero" href="articles\.html">)'
    r'(?:<img src="[^"]*" alt="" loading="eager" onerror="this\.remove\(\)"><div class="scrim"></div>)?')
COUNT = re.compile(r'[\d,]+( transmissions and counting)')


def cover_600(url):
    """Any Substack cover URL -> the 600px webp version the homepage uses."""
    if not url:
        return ""
    raw = unquote(url.rsplit("/https%3A", 1)[-1]) if "/https%3A" in url else url
    if not raw.startswith("http"):
        raw = "https:" + raw
    if raw.startswith(S3):
        return COVER_CDN + quote(raw, safe="")
    return url


def newest_cover(articles):
    for a in sorted(articles, key=lambda a: a.get("date", ""), reverse=True):
        c = cover_600(a.get("cover_url"))
        if c:
            return c, a
    return "", None


def main(repo, data_dir):
    with open(os.path.join(data_dir, "notes_with_media_compact.json"), encoding="utf-8") as f:
        count = len(json.load(f))
    with open(os.path.join(data_dir, "magazine_articles.json"), encoding="utf-8") as f:
        articles = json.load(f)
    cover, art = newest_cover(articles)
    img = (f'<img src="{html.escape(cover, quote=True)}" alt="" loading="eager" '
           f'onerror="this.remove()"><div class="scrim"></div>') if cover else ""

    changed = []
    pages = [os.path.join(repo, "index.html")] + sorted(glob.glob(os.path.join(repo, "index-*.html")))
    for path in pages:
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if not HERO_IMG.search(text):
            continue
        new = HERO_IMG.sub(lambda m: m.group(1) + img, text, count=1)
        new = COUNT.sub(lambda m: f"{count:,}" + m.group(1), new)
        if new != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            changed.append(os.path.basename(path))
    print(f"homepage tile: {count:,} transmissions"
          + (f", picture from “{art['title'].strip()}” ({art['date']})" if art else "")
          + f"; {len(changed)} page(s) updated")
    return changed


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    data = sys.argv[2] if len(sys.argv) > 2 else os.path.join(repo, "_data")
    main(repo, data)
