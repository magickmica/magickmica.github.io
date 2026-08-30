#!/usr/bin/env python3
"""
MAGICKMICA - sync_frequencies.py
Brings the 15 seasonal index-*.html variants in line with index.html:

  1. REMOVE the Ko-fi membership block ("Incoming Mothership Transmissions"
     + the two tier TVs + "Join the Transmission" panel). index.html does
     not carry it, so the variants should not either.
  2. ADD the Channel Dial (<details class="chdial">) so every frequency can
     reach every other one, plus arcade and the broadcast pages.

Each page keeps its own theme, layout and copy. Only these two things move.

The Ko-fi block is delimited by HTML section comments in every file, so it
is cut marker-to-marker rather than by guessing at tag nesting.
"""
import os, re, glob, shutil

START_RE = re.compile(r"<!--[^>]*?MBERSHIP TRANSMISSIONS \(Ko-fi tiers\)[^>]*?-->")
NEXT_SECTION_RE = re.compile(r"<!--\s*\u2500+[^>]{0,160}?\u2500+\s*-->")


def strip_kofi(html_text):
    m = START_RE.search(html_text)
    if not m:
        return html_text, False
    nxt = NEXT_SECTION_RE.search(html_text, m.end())
    if not nxt:
        return html_text, False
    return html_text[:m.start()] + html_text[nxt.start():], True


CSS_BLOCK_RE = re.compile(
    r"/\*\s*\u2550+\s*KO-FI MEMBERSHIP TRANSMISSIONS.*?(?=/\*\s*\u2550)",
    re.DOTALL)


def strip_kofi_css(html_text):
    """The markup cut leaves the block's CSS rules behind. Harmless, but
    dead weight on 15 pages, so remove those too."""
    new, n = CSS_BLOCK_RE.subn("", html_text)
    return new, bool(n)


def extract_dial(index_html):
    """Pull the dial's <style> block and <details> element out of index.html."""
    i = index_html.find(".chdial")
    if i == -1:
        return None
    style_start = index_html.rfind("<style>", 0, i)
    det_start = index_html.find('<details class="chdial"', i)
    det_end = index_html.find("</details>", det_start)
    if -1 in (style_start, det_start, det_end):
        return None
    return index_html[style_start:det_end + len("</details>")]


def add_dial(html_text, dial):
    if "chdial" in html_text:
        return html_text, False
    # sits right after <body ...>, same as on index.html
    m = re.search(r"<body[^>]*>", html_text)
    if not m:
        return html_text, False
    return html_text[:m.end()] + "\n" + dial + "\n" + html_text[m.end():], True


def run(repo, out_dir):
    index_path = os.path.join(out_dir, "index.html")
    if not os.path.exists(index_path):
        index_path = os.path.join(repo, "index.html")
    index_html = open(index_path, encoding="utf-8").read()
    dial = extract_dial(index_html)
    if not dial:
        raise SystemExit("could not find the channel dial in index.html")

    os.makedirs(out_dir, exist_ok=True)
    report = []
    for f in sorted(glob.glob(os.path.join(repo, "index-*.html"))):
        name = os.path.basename(f)
        src = os.path.join(out_dir, name)
        if not os.path.exists(src):
            src = f
        text = open(src, encoding="utf-8").read()
        before = len(text)

        text, removed = strip_kofi(text)
        text, _ = strip_kofi_css(text)
        text, added = add_dial(text, dial)

        if removed or added:
            open(os.path.join(out_dir, name), "w", encoding="utf-8").write(text)
        report.append((name, removed, added, before, len(text)))

    # index.html itself: make sure the Ko-fi block is gone there too
    text, removed = strip_kofi(index_html)
    if removed:
        open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(text)
        report.append(("index.html", True, False, len(index_html), len(text)))
    return report


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "magickmica.github.io-main"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "build"
    rows = run(repo, out_dir)
    print(f"{'page':26} {'ko-fi removed':14} {'dial added':11} size change")
    for name, rem, add, b, a in rows:
        print(f"{name:26} {str(rem):14} {str(add):11} {b:,} -> {a:,}")
