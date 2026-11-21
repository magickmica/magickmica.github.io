#!/usr/bin/env python3
"""
MAGICKMICA - desktop/build_desktop.py  ·  data for MagickOS 98 (desktop/index.html)

    python3 desktop/build_desktop.py          # run from anywhere

Writes desktop/desktop.js with what's new right now:
  - this week's most-loved notes (My Notes window, Welcome window)
  - notes per day this week, and the all-time count
  - the newest articles (Inbox window)
  - the newest Y3K issues (Y3K Magazine window)
  - the 16 seasonal themes (Control Panel)
  - every page of the site, grouped (Start menu)

Only rewrites desktop.js when something changed. Run by tools/update_all.py on
every site update, so the desktop always shows the newest notes and articles.
"""
import datetime as dt
import glob
import json
import os
import re
import sys
from urllib.parse import quote, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DATA = os.environ.get("MM_DATA") or os.path.join(REPO, "_data")
OUT = os.path.join(HERE, "desktop.js")

NOTES = 12
ARTICLES = 12
ISSUES = 8

COVER_CDN = ("https://substackcdn.com/image/fetch/"
             "$s_!G4Yk!,w_600,c_limit,f_webp,q_auto:good,fl_progressive:steep/")
S3 = "https://substack-post-media.s3.amazonaws.com/public/images/"


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def cover_600(url):
    if not url:
        return ""
    raw = unquote(url.rsplit("/https%3A", 1)[-1]) if "/https%3A" in url else url
    if not raw.startswith("http"):
        raw = "https:" + raw
    return COVER_CDN + quote(raw, safe="") if raw.startswith(S3) else url


def day(s):
    return dt.date.fromisoformat(s[:10])


def clean(t, n):
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


def main():
    notes = load("notes_with_media_compact.json")
    articles = load("magazine_articles.json")
    themes = load("themes.json")
    nav = load("sitemap_nav.json")

    last = max(day(n["d"]) for n in notes)
    first = last - dt.timedelta(days=6)
    week = [n for n in notes if first <= day(n["d"]) <= last]

    pics = sorted((n for n in week if n.get("t")), key=lambda n: (-n.get("l", 0), -n.get("r", 0), n["d"]))
    if len(pics) < NOTES:
        seen = {n["id"] for n in pics}
        pics += sorted((n for n in notes if n.get("t") and n["id"] not in seen and day(n["d"]) < first),
                       key=lambda n: n["d"], reverse=True)[: NOTES - len(pics)]
    words = sorted((n for n in week if not n.get("t") and len((n.get("b") or "").strip()) > 20),
                   key=lambda n: (-n.get("l", 0), n["d"]))[:6]

    def note(n, size):
        return {"id": n["id"], "d": n["d"][:10], "l": n.get("l", 0), "r": n.get("r", 0),
                "b": clean(n.get("b"), size), "t": n.get("t") or ""}

    days = [first + dt.timedelta(days=k) for k in range(7)]
    per_day = [{"d": d.isoformat(), "n": sum(1 for n in week if day(n["d"]) == d)} for d in days]

    arts = sorted(articles, key=lambda a: (a.get("date", ""), a.get("published", "")), reverse=True)[:ARTICLES]
    arts = [{"title": (a.get("title") or "").strip(), "sub": clean(a.get("subtitle") or a.get("preview"), 220),
             "date": a.get("date", "")[:10], "nl": a.get("newsletter") or "Substack", "url": a.get("url", ""),
             "cover": cover_600(a.get("cover_url")), "likes": a.get("likes"), "comments": a.get("comments")}
            for a in arts]

    weeks = sorted((os.path.basename(p)[5:15] for p in glob.glob(os.path.join(REPO, "reader", "issues", "week-*.html"))),
                   reverse=True)[:ISSUES]
    issues = []
    for w in weeks:
        a = day(w)
        issues.append({"w": w, "n": sum(1 for n in notes if a <= day(n["d"]) < a + dt.timedelta(days=7)),
                       "classic": os.path.exists(os.path.join(REPO, f"week-{w}.html"))})

    th = []
    for f, t in themes.items():
        c = t.get("colors", {})
        th.append({"slug": t["slug"], "ch": t.get("ch", ""), "label": t.get("label") or t.get("name") or t["slug"],
                   "emoji": t.get("emoji") or "📺", "file": f,
                   "c": {k: c[k] for k in ("deep", "pink", "cyan", "lime", "purple", "gold", "teal") if k in c}})
    th.sort(key=lambda t: (t["slug"] != "home", t["ch"]))

    menu = [{"name": k, "items": [[h, t] for h, t in v]} for k, v in nav.items() if not k.startswith("_")]

    data = {
        "updated": last.isoformat(), "weekStart": first.isoformat(),
        "total": len(notes), "articlesTotal": len(articles),
        "week": {"count": len(week), "loves": sum(n.get("l", 0) for n in week), "days": per_day},
        "notes": [note(n, 240) for n in pics[:NOTES]],
        "words": [note(n, 280) for n in words],
        "articles": arts, "issues": issues, "themes": th, "menu": menu,
    }
    body = ("/* MagickOS 98 data. Written by desktop/build_desktop.py on every site update; "
            "don't edit by hand. */\nwindow.MMOS = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")

    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if body != old:
        with open(OUT, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"desktop.js: {len(notes):,} notes through {last}, {len(week)} this week, {len(articles)} articles")
    else:
        print("desktop.js: already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
