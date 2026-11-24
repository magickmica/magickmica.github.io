#!/usr/bin/env python3
"""
MAGICKMICA - add_subscribe.py  (v2, 24 Nov 2026)
Puts the Substack subscribe calls-to-action (mm-subscribe.js) into the pages, in place.

    python3 tools/add_subscribe.py            # from anywhere; finds the repo itself
    python3 tools/add_subscribe.py <repo>

What goes where (edit PAGES / GLOBS below to change it):
  index.html                     big teaser box, between Y3K MAGAZINE and PLAY & LISTEN
  notes.html, blog.html          slim strip (top of the notes / top of the blog sidebar)
  arcade + circus pages          circus banner (circus theme)
  every circus game              the after-game pop-up (just loads the script)
  explore/ tapes + tape player   VHS banner (tapes theme)
  explore/ constellation + sky   starfield banner (sky theme)
  explore/ other rooms, archive  archive banner
  Y3K issues, magazine pages     end-of-issue banner (y3k look)
  broadcasts, almanac, signal    end-of-page banner (signal theme)
  academy/, desktop/             a "Subscribe" button on the MagickOS taskbar

Safe to run any number of times: a page that already has a box is left alone,
and a page whose layout has changed so the spot can't be found is skipped and
reported, never guessed at. update_all.py runs it at the end of every site
update, so the boxes come back even if a page is rebuilt without them.
"""
import glob
import os
import re
import sys

SUB_URL = ("https://magickmica.substack.com/subscribe?utm_source=magickmica.github.io"
           "&utm_medium=site&utm_campaign=subscribe-box&utm_content=")
FALLBACK = '<a href="https://magickmica.substack.com/subscribe">Subscribe to Magick Mica TV on Substack</a>'
VERSION = "2"

# Anchor shortcuts
FOOTER = "<footer"                          # the page's last <footer> outside any <script>
PRIZES = '<script src="mm-prizes.js'
EXPLORE_FOOT = '<footer class="ar-wrap mmx-foot"'

# page -> dict(variant, theme, anchors (tried in order), where, style, attrs)
PAGES = {
    "index.html": dict(variant="full", anchors=['<div class="sect"><h2 class="holo">PLAY &amp; LISTEN</h2>'],
                       where="before"),
    "notes.html": dict(variant="compact", anchors=['<div class="results-info" id="resultsInfo">', '<div id="grid">'],
                       where="before", style="position:relative;z-index:2;max-width:1200px;margin:0 auto;padding:0 20px"),
    "blog.html": dict(variant="compact", anchors=['<div class="sidebar">'], where="after"),

    # the circus
    "arcade.html": dict(theme="circus", anchors=['<section class="floor" id="cabinets">', FOOTER]),
    "arcade-new.html": dict(theme="circus", anchors=['<section class="floor" id="cabinets">', FOOTER]),
    "six-in-one.html": dict(theme="circus", anchors=[FOOTER]),
    "my-prizes.html": dict(theme="circus", anchors=[PRIZES],
                           title="Your shelf is filling up nicely",
                           sub="Subscribe free and my new articles land in your inbox. New circus games and prizes get announced in my Notes."),
    "winter-carnival.html": dict(theme="circus", anchors=[PRIZES], art="❄️",
                                 eyebrow="❄ WINTER CARNIVAL · FREE"),
    "ticket-booth.html": dict(theme="circus", anchors=[PRIZES], art="🎟️"),

    # explore the notes
    "explore/index.html": dict(theme="archive", anchors=[EXPLORE_FOOT]),
    "explore/hall.html": dict(theme="archive", anchors=[EXPLORE_FOOT]),
    "explore/gallery.html": dict(theme="archive", anchors=[EXPLORE_FOOT], art="🖼️"),
    "explore/book.html": dict(theme="archive", anchors=[EXPLORE_FOOT], art="📖"),
    "explore/themes.html": dict(theme="archive", anchors=[EXPLORE_FOOT]),
    "explore/tapes.html": dict(theme="tapes", anchors=[EXPLORE_FOOT]),
    "explore/player.html": dict(theme="tapes", anchors=[EXPLORE_FOOT], art="📺",
                                eyebrow="● LIVE · CHANNEL MAGICK MICA",
                                title="Never miss a new episode"),
    "explore/stars.html": dict(theme="sky", anchors=[EXPLORE_FOOT], art="✨"),
    "explore/sky.html": dict(theme="sky", anchors=[EXPLORE_FOOT]),

    # reading
    "archive.html": dict(theme="archive", anchors=[FOOTER]),
    "articles.html": dict(theme="archive", anchors=[FOOTER], art="📜",
                          eyebrow="✦ EVERY ARTICLE, FIRST", title="Read the next one the day it's published"),
    "minimags.html": dict(theme="y3k", anchors=[FOOTER]),
    "newsstand.html": dict(theme="y3k", anchors=[FOOTER], art="🗞️"),
    "random-note.html": dict(theme="signal", anchors=[FOOTER], art="📺"),
    "tv-notes.html": dict(theme="signal", anchors=[FOOTER], art="📺"),
    "sasquatch-gazette.html": dict(theme="y3k", anchors=['<footer class="colophon"'], art="🦶",
                                   eyebrow="✦ ENJOYED THE GAZETTE? · FREE"),
    "almanac/index.html": dict(theme="sky", anchors=['<footer class="foot"'], art="🌙",
                               eyebrow="✧ Y3K ALMANAC", title="Get today's transmission in your inbox"),
    "signal/index.html": dict(theme="signal", anchors=['<footer class="foot"']),
}

# Every page matching these gets the same treatment (only if it exists).
GLOBS = [
    ("week-*.html", dict(theme="y3k", anchors=[FOOTER])),
    ("month-*.html", dict(theme="y3k", anchors=[FOOTER])),
    ("*-broadcast.html", dict(theme="signal", anchors=[FOOTER])),
]
for _p in ("glitter-transmission", "galactic-dessert-issue", "stargazer-june-2026", "starseed-chronicles",
           "glow-the-transmission-issue", "copper-the-ancient-issue", "the-sampler-three-transmissions",
           "prism-parlour-crystal-living", "the-art-wing-gallery", "turn-down-the-static"):
    PAGES.setdefault(_p + ".html", dict(theme="signal", anchors=[FOOTER]))

# Circus games: no box on the page, just the script, which adds the after-game pop-up.
GAMES = ["cosmic-clown-splash.html", "ring-toss.html", "moon-striker.html", "star-darts.html", "prize-wheel.html",
         "fortune-teller.html", "photo-booth.html", "duck-pond.html", "claw-machine.html", "whack-an-alien.html",
         "skee-ball.html", "coin-pusher.html", "shooting-gallery.html", "hoop-shot.html", "snowball-splat.html",
         "cocoa-catch.html", "ferris-wheel.html", "witching-hour.html", "moon-shot.html", "cosmic-echo.html",
         "pong.html", "gingerbread-run.html", "santa-vs-snowmen.html", "fireside-cocoa.html", "graveyard-shift.html"]

# MagickOS taskbars: a Subscribe button just before the clock tray.
TASKBARS = ["academy/index.html", "desktop/index.html"]
TASKBAR_ANCHOR = '<div class="tray">'


def script_tag(rel):
    depth = rel.count("/")
    return f'<script src="{"../" * depth}mm-subscribe.js?v={VERSION}" defer></script>'


def box(cfg):
    variant = cfg.get("variant", "banner")
    attrs = [f'data-mm-subscribe="{variant}"']
    if variant == "banner":
        attrs.append(f'data-theme="{cfg.get("theme", "signal")}"')
    for k in ("art", "eyebrow", "title", "sub", "button"):
        if cfg.get(k):
            v = cfg[k].replace("&", "&amp;").replace('"', "&quot;")
            attrs.append(f'data-{k}="{v}"')
    if cfg.get("style"):
        attrs.append(f'style="{cfg["style"]}"')
    return f'<div {" ".join(attrs)}>{FALLBACK}</div>'


def script_spans(page):
    return [(m.start(), m.end()) for m in re.finditer(r"<script\b.*?</script>", page, re.S | re.I)]


def find_anchor(page, anchor):
    """Position of the anchor, skipping matches inside <script> blocks.
    The generic <footer anchor takes the last such match (the page footer)."""
    spans = script_spans(page)
    hits = [m.start() for m in re.finditer(re.escape(anchor), page)
            if not any(a < m.start() < b for a, b in spans)]
    if not hits:
        return -1
    return hits[-1] if anchor == FOOTER else hits[0]


def add_script(page, rel):
    if "mm-subscribe.js" in page:
        return page, False
    i = page.rfind("</body>")
    if i < 0:
        return page, False
    return page[:i] + script_tag(rel) + "\n" + page[i:], True


def bump_version(page):
    """Pages carrying the v1 script tag get the new version so browsers refetch it."""
    new = re.sub(r'mm-subscribe\.js\?v=\d+', f"mm-subscribe.js?v={VERSION}", page)
    return new, new != page


def patch_box(repo, rel, cfg, report):
    path = os.path.join(repo, rel)
    with open(path, encoding="utf-8") as f:
        page = f.read()
    changed = False
    if "data-mm-subscribe" not in page:
        where = cfg.get("where", "before")
        for a in cfg["anchors"]:
            i = find_anchor(page, a)
            if i < 0:
                continue
            if where == "after":
                i += len(a)
            page = page[:i] + "\n" + box(cfg) + "\n" + page[i:]
            changed = True
            break
        else:
            report["skipped"].append(rel)
            return
    page, c = add_script(page, rel); changed |= c
    page, c = bump_version(page); changed |= c
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
    report["added" if changed else "had"].append(rel)


def patch_script_only(repo, rel, report):
    path = os.path.join(repo, rel)
    with open(path, encoding="utf-8") as f:
        page = f.read()
    page, c1 = add_script(page, rel)
    page, c2 = bump_version(page)
    if c1 or c2:
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
    report["added" if (c1 or c2) else "had"].append(rel)


def patch_taskbar(repo, rel, report):
    path = os.path.join(repo, rel)
    with open(path, encoding="utf-8") as f:
        page = f.read()
    if "mmsub-task" in page:
        report["had"].append(rel); return
    i = page.find(TASKBAR_ANCHOR)
    if i < 0:
        report["skipped"].append(rel); return
    slug = rel.split("/")[0]
    btn = (f'<a class="btn mmsub-task" href="{SUB_URL}taskbar-{slug}" target="_blank" rel="noopener" '
           f'title="Get new transmissions in your inbox (free)" '
           f'style="flex:none;display:inline-flex;align-items:center;gap:6px;white-space:nowrap">'
           f'<span aria-hidden="true">📬</span>Subscribe</a>\n  ')
    page = page[:i] + btn + page[i:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    report["added"].append(rel)


def main(argv):
    repo = argv[0] if argv else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(os.path.join(repo, "mm-subscribe.js")):
        print("mm-subscribe.js is not in the repo yet; upload it first. Nothing changed.")
        return 0
    report = {"added": [], "had": [], "skipped": []}

    todo = dict(PAGES)
    for pattern, cfg in GLOBS:
        for p in sorted(glob.glob(os.path.join(repo, pattern))):
            todo.setdefault(os.path.relpath(p, repo).replace(os.sep, "/"), cfg)
    for rel, cfg in todo.items():
        if os.path.exists(os.path.join(repo, rel)):
            patch_box(repo, rel, cfg, report)
    for rel in GAMES:
        if os.path.exists(os.path.join(repo, rel)):
            patch_script_only(repo, rel, report)
    for rel in TASKBARS:
        if os.path.exists(os.path.join(repo, rel)):
            patch_taskbar(repo, rel, report)

    print(f"  subscribe boxes: {len(report['added'])} pages updated, {len(report['had'])} already had them")
    for rel in report["skipped"]:
        print(f"  {rel}: no place found for the box, skipped")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
