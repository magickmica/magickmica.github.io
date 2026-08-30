#!/usr/bin/env python3
"""
MAGICKMICA - update_pages.py
Refreshes the embedded JSON data blobs in the core pages and the
index/frequency variants, preserving each page's unique design.

CRITICAL RULE: every re.sub that injects JSON uses a lambda replacement.
A plain replacement string makes Python interpret backslash escapes in
the JSON and corrupts the JS ("Invalid or unexpected token").

Curated pools are deliberately NOT touched: QUEST, POS, AFFIRMATIONS,
DREAM_POOL, PROMPTS, SYMBOLS, MOODS. Those are hand-themed, not
top-N-by-likes, so regenerating them would degrade them.
"""
import json, os, re, shutil, datetime, glob

CURATED = {"QUEST", "POS", "AFFIRMATIONS", "DREAM_POOL",
           "PROMPTS", "SYMBOLS", "MOODS", "TYPE_LABELS", "NL_LABELS", "NL_URLS"}


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def inject(html_text, name, obj):
    """Replace `const NAME = ...;` with fresh JSON. Lambda replacement only."""
    pat = re.compile(r"const\s+" + re.escape(name) + r"\s*=\s*(?:\[.*?\]|\{.*?\});",
                     re.DOTALL)
    if not pat.search(html_text):
        return html_text, False
    payload = dumps(obj)
    return pat.sub(lambda m: f"const {name} = {payload};", html_text, count=1), True


def top_notes(notes, n, need_image=False, fields=None):
    pool = [x for x in notes if x.get("t")] if need_image else list(notes)
    pool.sort(key=lambda x: (-(x.get("l") or 0), -int(x["id"])))
    out = []
    for x in pool[:n]:
        if fields is None:
            out.append(x)
        else:
            out.append({k: x[k] for k in fields if k in x})
    return out


def preserve_extra(new_list, old_list, key="c"):
    """Carry forward a curated field (e.g. MTV_NOTES 'c' tags) by note id."""
    old = {int(o["id"]): o for o in old_list if key in o}
    for n in new_list:
        o = old.get(int(n["id"]))
        if o is not None:
            n[key] = o[key]
    return new_list


def read_blob(html_text, name):
    m = re.search(r"const\s+" + re.escape(name) + r"\s*=\s*(\[.*?\]|\{.*?\});",
                  html_text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def build_sidebar(notes, articles, digest_weeks):
    """blog.html sidebar structures."""
    imgs = [n for n in notes if n.get("t")]
    by_likes = sorted(notes, key=lambda x: (-(x.get("l") or 0), -int(x["id"])))
    img_by_likes = sorted(imgs, key=lambda x: (-(x.get("l") or 0), -int(x["id"])))
    recent = sorted(notes, key=lambda x: (x["d"], x["id"]), reverse=True)

    f4 = lambda x: {k: x[k] for k in ("b", "id", "l", "t") if k in x}
    f5 = lambda x: {k: x[k] for k in ("b", "d", "id", "l", "t") if k in x}
    g3 = lambda x: {k: x[k] for k in ("id", "l", "t") if k in x}

    # on_this_day is a map of MM-DD -> notes, so the sidebar works on any
    # date the visitor loads the page, not just the day it was built.
    otd = {}
    for n in notes:
        otd.setdefault(n["d"][5:], []).append(n)
    on_this_day = {}
    for md, group in otd.items():
        group.sort(key=lambda x: -(x.get("l") or 0))
        on_this_day[md] = [
            {"id": x["id"], "b": x.get("b", ""), "l": x.get("l", 0),
             "t": x.get("t", ""), "d": x["d"]}
            for x in group[:6]
        ]

    spot = by_likes[0] if by_likes else None
    spotlight = ({"id": spot["id"], "b": spot.get("b", ""), "l": spot.get("l", 0),
                  "r": spot.get("r", 0), "t": spot.get("t", ""), "d": spot["d"]}
                 if spot else {})

    data = {
        "random_pool": [f4(x) for x in img_by_likes[:40]],
        "recent_top": [f5(x) for x in sorted(recent[:200],
                       key=lambda x: -(x.get("l") or 0))[:6]],
        "gallery": [g3(x) for x in img_by_likes[:9]],
    }
    extra = {
        "on_this_day": on_this_day,
        "affirmations": [{k: x[k] for k in ("b", "id", "l") if k in x}
                         for x in by_likes[:40]],
        "spotlight": spotlight,
    }
    issues = []
    for wk in digest_weeks[-5:][::-1]:
        start = datetime.date.fromisoformat(wk)
        end = start + datetime.timedelta(days=6)
        cnt = sum(1 for n in notes if wk <= n["d"] <= end.isoformat())
        issues.append({
            "key": f"week-{wk}",
            "label": f"{start.strftime('%b %-d')}\u2013{end.strftime('%b %-d')}",
            "count": cnt,
        })
    return data, extra, issues


def update_all(repo, out_dir, notes, articles, digest_weeks):
    os.makedirs(out_dir, exist_ok=True)
    changed = []

    f4 = ("b", "id", "l", "t")
    f6 = ("b", "d", "id", "l", "r", "t")

    sidebar, extra, issues = build_sidebar(notes, articles, digest_weeks)

    plan = {
        "notes.html":       [("NOTES", notes)],
        "index2.html":      [("NOTES", notes)],
        "random-note.html": [("NOTES", notes)],
        "articles.html":    [("POSTS", articles),
                             ("NOTES_POOL", top_notes(notes, 200, True, f4))],
        "archive.html":     [("ARTICLES", articles),
                             ("NOTES_MOSAIC", top_notes(notes, 24, True, ("id", "t")))],
        "blog.html":        [("POSTS", articles),
                             ("FEED_NOTES", top_notes(notes, 1000, False, f4)),
                             ("SIDEBAR_DATA", sidebar),
                             ("SIDEBAR_EXTRA", extra),
                             ("SIDEBAR_ISSUES", issues)],
        "arcade.html":      [("POOL", top_notes(notes, 400, True, f6))],
    }

    # index.html + every frequency variant share the MTV_NOTES pool
    mtv_fields = ("b", "d", "id", "l", "r")
    for f in ["index.html"] + sorted(glob.glob(os.path.join(repo, "index-*.html"))):
        plan.setdefault(os.path.basename(f), []).append(("MTV_NOTES", None))

    for fname, jobs in plan.items():
        src = os.path.join(repo, fname)
        if not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as fh:
            html_text = fh.read()
        orig = html_text
        for name, payload in jobs:
            if name in CURATED:
                continue
            if name == "MTV_NOTES":
                old = read_blob(html_text, "MTV_NOTES") or []
                fresh = top_notes(notes, 150, False, mtv_fields)
                payload = preserve_extra(fresh, old, "c")
            html_text, ok = inject(html_text, name, payload)
        if html_text != orig:
            with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as fh:
                fh.write(html_text)
            changed.append(fname)
    return changed


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "magickmica.github.io-main"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "_data"
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "build"

    with open(os.path.join(data_dir, "notes_with_media_compact.json"), encoding="utf-8") as f:
        notes = json.load(f)
    with open(os.path.join(data_dir, "magazine_articles.json"), encoding="utf-8") as f:
        articles = json.load(f)

    weeks = sorted({(datetime.date.fromisoformat(n["d"])
                     - datetime.timedelta(days=datetime.date.fromisoformat(n["d"]).weekday())
                     ).isoformat() for n in notes})

    changed = update_all(repo, out_dir, notes, articles, weeks)
    print(f"updated {len(changed)} pages")
    for c in changed:
        print("  ", c)


# ---------------------------------------------------------------- minimags hub
def issue_card(href, cover, count, title):
    img = ""
    if cover:
        img = (f'<img src="{cover}" loading="lazy" '
               f"onerror=\"this.parentElement.classList.add('no-img')\" />")
    return (f'<a class="issue-card" href="{href}"><div class="issue-cover">{img}'
            f'<div class="issue-cover-overlay"></div>'
            f'<div class="issue-count">{count} NOTES</div></div>'
            f'<div class="issue-info"><div class="issue-title">{title}</div></div></a>')


def rebuild_minimags(repo, out_dir, notes):
    src = os.path.join(repo, "minimags.html")
    if not os.path.exists(src):
        return False
    with open(src, encoding="utf-8") as f:
        html_text = f.read()

    def cover_of(group):
        imgs = [n for n in group if n.get("t")]
        if not imgs:
            return ""
        return sorted(imgs, key=lambda x: -(x.get("l") or 0))[0]["t"]

    # weekly cards, newest first
    weeks = {}
    for n in notes:
        d = datetime.date.fromisoformat(n["d"])
        wk = (d - datetime.timedelta(days=d.weekday())).isoformat()
        weeks.setdefault(wk, []).append(n)
    wcards = []
    for wk in sorted(weeks, reverse=True):
        s = datetime.date.fromisoformat(wk)
        e = s + datetime.timedelta(days=6)
        label = f"{s.strftime('%b %-d')}\u2013{e.strftime('%b %-d, %Y')}"
        wcards.append(issue_card(f"week-{wk}.html", cover_of(weeks[wk]),
                                 len(weeks[wk]), label))

    months = {}
    for n in notes:
        months.setdefault(n["d"][:7], []).append(n)
    mcards = []
    for m in sorted(months, reverse=True):
        label = datetime.date(int(m[:4]), int(m[5:7]), 1).strftime("%B %Y")
        mcards.append(issue_card(f"month-{m}.html", cover_of(months[m]),
                                 len(months[m]), label))

    def swap(text, div_id, cards, end_marker):
        """Replace the full contents of a grid div. Boundaries are explicit
        because the cards contain nested </div>s, so a lazy match on the
        first closing tag would only replace part of the grid."""
        open_pat = re.compile(r'(<div[^>]*id="' + div_id + r'"[^>]*>)')
        m = open_pat.search(text)
        if not m:
            return text, False
        start = m.end()
        end = text.find(end_marker, start)
        if end == -1:
            return text, False
        return text[:start] + "".join(cards) + text[end:], True

    new, ok1 = swap(html_text, "wGrid", wcards,
                    '</div>\n<div class="issues-grid hidden" id="mGrid"')
    new, ok2 = swap(new, "mGrid", mcards, "</div>\n<footer>")
    if not (ok1 and ok2) or new == html_text:
        return False
    with open(os.path.join(out_dir, "minimags.html"), "w", encoding="utf-8") as f:
        f.write(new)
    return True


# ---------------------------------------------------------------- SEO head
SITE = "https://magickmica.github.io/"

PAGE_META = {
 "index.html": ("Magick Mica \u2014 Where Magic Meets the Pixel",
   "Daily cosmic art notes, AI artwork, games and interactive oddities from Magick Mica. Curiosities, dreams and delightful nonsense."),
 "notes.html": ("All Notes \u2014 Magick Mica",
   "The complete searchable archive of Magick Mica's daily art notes and cosmic transmissions."),
 "articles.html": ("Magazine \u2014 Magick Mica",
   "Every article from MagickMica TV and MagickMica Art \u2014 AI art, dream visions, and cosmic curiosities."),
 "blog.html": ("Blog \u2014 Magick Mica",
   "Long-form posts woven with daily notes from Magick Mica's cosmic archive."),
 "archive.html": ("Archive \u2014 Magick Mica",
   "Browse the full Magick Mica archive of articles and art notes."),
 "minimags.html": ("Y3K Magazine \u2014 Magick Mica",
   "Weekly and monthly Y3K Magazine issues collecting every Magick Mica transmission."),
 "arcade.html": ("Arcade \u2014 Magick Mica",
   "Play jigsaw, memory match, dream slots and more, built from Magick Mica's own artwork."),
}


def add_seo_head(html_text, fname, title, desc, canonical):
    """Insert description/canonical/OG/Twitter after <title>, without
    disturbing the page's existing head or design."""
    out = html_text
    if not re.search(r'name="description"', out, re.I):
        tag = f'\n<meta name="description" content="{html_escape(desc)}">'
        out = re.sub(r"(</title>)", lambda m: m.group(1) + tag, out, count=1)
    if not re.search(r'rel="canonical"', out, re.I):
        tag = f'\n<link rel="canonical" href="{canonical}">'
        out = re.sub(r"(</title>)", lambda m: m.group(1) + tag, out, count=1)
    if not re.search(r'property="og:', out, re.I):
        og = (f'\n<meta property="og:type" content="website">'
              f'\n<meta property="og:site_name" content="Magick Mica">'
              f'\n<meta property="og:title" content="{html_escape(title)}">'
              f'\n<meta property="og:description" content="{html_escape(desc)}">'
              f'\n<meta property="og:url" content="{canonical}">'
              f'\n<meta name="twitter:card" content="summary_large_image">'
              f'\n<meta name="twitter:title" content="{html_escape(title)}">'
              f'\n<meta name="twitter:description" content="{html_escape(desc)}">')
        out = re.sub(r"(</title>)", lambda m: m.group(1) + og, out, count=1)
    return out


def html_escape(s):
    import html as _h
    return _h.escape(s or "", quote=True)


def seo_pass(repo, out_dir):
    """Add meta to the core pages, and point every seasonal index variant's
    canonical at the real homepage so they stop competing with it."""
    touched = []
    for f in sorted(glob.glob(os.path.join(repo, "*.html"))):
        fname = os.path.basename(f)
        src = os.path.join(out_dir, fname)
        if not os.path.exists(src):
            src = f
        with open(src, encoding="utf-8") as fh:
            text = fh.read()
        orig = text

        if fname in PAGE_META:
            title, desc = PAGE_META[fname]
            canon = SITE + ("" if fname == "index.html" else fname)
            text = add_seo_head(text, fname, title, desc, canon)
        elif fname.startswith("index-"):
            # near-duplicate of the homepage: canonical points home
            title, desc = PAGE_META["index.html"]
            text = add_seo_head(text, fname, title, desc, SITE)
        else:
            continue

        if text != orig:
            with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as fh:
                fh.write(text)
            touched.append(fname)
    return touched
