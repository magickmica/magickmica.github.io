#!/usr/bin/env python3
"""
MAGICKVISION SIGNAL BAND — data builder
---------------------------------------
Reads the site's existing data (read-only) and writes signal/signal.js.
Touches nothing outside the signal/ folder.

    python3 signal/build_signal.py            # from the repo root
    python3 build_signal.py                   # from inside signal/

Inputs  (never modified):
    _data/notes_with_media_compact.json
    _data/magazine_articles.json
    minimags.html                 -> which week/month issues are published
    week-*.html / month-*.html    -> each issue's --accent colour
Output:
    signal/signal.js              -> const SIGNAL = {...};
"""
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # repo root = parent of signal/
# Data folder: the repo's _data/ by default; set MM_DATA to build from another copy.
DATA = os.environ.get("MM_DATA") or os.path.join(ROOT, "_data")
OUT = os.path.join(HERE, "signal.js")

# Same palettes as tools/build_digests.py, used only as a fallback when an
# issue page does not exist to read its colour from.
WEEK_PALETTE = ["#ff6ef7", "#6ef7ff", "#f7ff6e", "#6effa0",
                "#b06eff", "#ff9d6e", "#ff6e9d", "#ffd76e"]
MONTH_PALETTE = ["#b06eff", "#ff9d6e", "#ff6e9d", "#ffd76e",
                 "#ff6ef7", "#6ef7ff", "#f7ff6e", "#6effa0"]

# Image URLs share a long prefix; store only the tail to keep the file small.
IMG_PREFIX = ("https://substackcdn.com/image/fetch/$s_!G4Yk!,w_400,c_limit,f_webp,"
              "q_auto:good,fl_progressive:steep/"
              "https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F")

ACCENT_RE = re.compile(r"--accent:\s*(#[0-9a-fA-F]{6})")
URL_RE = re.compile(r"https?://\S+")


def load(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return json.load(f)


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def clean(text, limit=150):
    t = URL_RE.sub("", text or "")
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return t


def accent_from(page):
    p = os.path.join(ROOT, page)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", errors="ignore") as f:
        m = ACCENT_RE.search(f.read(4000))
    return m.group(1).lower() if m else None


def main():
    notes = load(os.path.join(DATA, "notes_with_media_compact.json"))
    articles = load(os.path.join(DATA, "magazine_articles.json"))

    with open(os.path.join(ROOT, "minimags.html"), encoding="utf-8") as f:
        mm = f.read()
    published = set(re.findall(r'href="((?:week|month)-\d{4}-\d{2}(?:-\d{2})?\.html)"', mm))

    by_week = {}
    for n in notes:
        w = monday(dt.date.fromisoformat(n["d"]))
        by_week.setdefault(w, []).append(n)

    first, last = min(by_week), max(by_week)
    note_weeks = sorted(by_week)
    palette_ix = {w: i for i, w in enumerate(note_weeks)}

    arts_by_week, pre_signal = {}, []
    for a in sorted(articles, key=lambda a: a["date"]):
        w = monday(dt.date.fromisoformat(a["date"]))
        item = {"t": a["title"].strip(), "u": a["url"],
                "nl": "Art" if "Art" in a.get("newsletter", "") else "TV",
                "d": a["date"]}
        if w < first:
            pre_signal.append(item)
        else:
            arts_by_week.setdefault(w, []).append(item)

    weeks = []
    w = first
    while w <= last:
        group = by_week.get(w, [])
        top = sorted(group, key=lambda n: (n.get("l", 0), n.get("r", 0)), reverse=True)
        picks = []
        for n in top:
            text = clean(n.get("b", ""))
            if not text and "t" not in n:
                continue
            p = {"id": n["id"], "x": text, "l": n.get("l", 0), "d": n["d"]}
            t = n.get("t")
            if t:
                p["i"] = t[len(IMG_PREFIX):] if t.startswith(IMG_PREFIX) else t
            picks.append(p)
            if len(picks) == 3:
                break
        page = f"week-{w.isoformat()}.html"
        has_issue = page in published
        accent = (accent_from(page) if has_issue else None) or \
            WEEK_PALETTE[palette_ix.get(w, 0) % 8]
        weeks.append({
            "w": w.isoformat(),
            "n": len(group),
            "l": sum(n.get("l", 0) for n in group),
            "img": sum(1 for n in group if "t" in n),
            "top": picks,
            "a": arts_by_week.get(w, []),
            "iss": has_issue,
            "c": accent,
        })
        w += dt.timedelta(days=7)

    months = {}
    for n in notes:
        months[n["d"][:7]] = months.get(n["d"][:7], 0) + 1
    month_list = []
    for m in sorted(months):
        y, mo = map(int, m.split("-"))
        page = f"month-{m}.html"
        has_issue = page in published
        month_list.append({
            "m": m, "n": months[m], "iss": has_issue,
            "c": (accent_from(page) if has_issue else None) or MONTH_PALETTE[(y * 12 + mo) % 8],
        })

    data = {
        "built": dt.date.today().isoformat(),
        "total": len(notes),
        "articles": len(articles),
        "first": first.isoformat(),
        "last": last.isoformat(),
        "imgPrefix": IMG_PREFIX,
        "weeks": weeks,
        "months": month_list,
        "preSignal": pre_signal,
    }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* generated by signal/build_signal.py — do not edit by hand */\n")
        f.write(f"const SIGNAL = {payload};\n")

    size = os.path.getsize(OUT)
    print(f"signal.js: {len(weeks)} weeks ({first} to {last}), "
          f"{len(notes):,} notes, {len(articles)} articles "
          f"({len(pre_signal)} before the first note), {size/1024:.1f} KB")


if __name__ == "__main__":
    sys.exit(main())
