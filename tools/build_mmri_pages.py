#!/usr/bin/env python3
"""Generate mmri-modified.html from risk-indicator.html.

The two pages are the same instrument with a different formula bolted in, so
keeping them as two hand-maintained files would guarantee they drift. Instead
risk-indicator.html is the only source anyone edits, and this rewrites the
handful of strings that differ: which mode the page starts in, the titles and
share-card text, the canonical URL, and the link across to the sibling.

    python3 tools/build_mmri_pages.py            # write the file
    python3 tools/build_mmri_pages.py --check    # fail if it is out of date

Run it after any edit to risk-indicator.html, and upload both.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "risk-indicator.html"
OUT = ROOT / "mmri-modified.html"
SITE = "https://magickmica.github.io/"

DESC = (
    "The MMMRI — Gregory Mannarino's modified market risk reading, which "
    "multiplies the MMRI by federal debt over GDP. Rendered as a Magick Mica "
    "instrument."
)

# (find, replace) applied in order. Every one must match exactly once, so a
# change to the source that breaks an assumption fails loudly here rather
# than silently producing a half-converted page.
REPLACEMENTS = [
    ('var PAGE_MODE = "mmri";',
     'var PAGE_MODE = "mmmri";'),

    ('<title>Magick Mica Risk Indicator — Magick Mica</title>',
     '<title>Magick Mica Modified Risk Indicator — Magick Mica</title>'),

    ('<meta property="og:title" content="Magick Mica Risk Indicator">',
     '<meta property="og:title" content="Magick Mica Modified Risk Indicator">'),

    ('<meta name="twitter:title" content="Magick Mica Risk Indicator">',
     '<meta name="twitter:title" content="Magick Mica Modified Risk Indicator">'),

    ('<meta property="og:url" content="' + SITE + 'risk-indicator.html">',
     '<meta property="og:url" content="' + SITE + 'mmri-modified.html">'),

    ('<link rel="canonical" href="' + SITE + 'risk-indicator.html">',
     '<link rel="canonical" href="' + SITE + 'mmri-modified.html">'),

    ('<a class="mode-link" id="siblingLink" href="mmri-modified.html">'
     'Also see the modified MMMRI →</a>',
     '<a class="mode-link" id="siblingLink" href="risk-indicator.html">'
     '← Back to the standard MMRI</a>'),

    ('<h1><span class="sheen">Magick Mica</span><br>Risk Indicator</h1>',
     '<h1><span class="sheen">Magick Mica</span><br>Modified Risk Indicator</h1>'),
]

# The share-card description appears twice, in the og: and twitter: tags.
OLD_DESC = (
    "The MMRI market risk reading, rendered as a Magick Mica instrument. "
    "Originally created by Gregory Mannarino."
)


def build():
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    s = SRC.read_text(encoding="utf-8")

    for find, repl in REPLACEMENTS:
        n = s.count(find)
        if n != 1:
            sys.exit(
                f"build_mmri_pages: expected exactly one match for\n  {find[:90]}\n"
                f"but found {n}. risk-indicator.html changed shape — update this script."
            )
        s = s.replace(find, repl)

    if s.count(OLD_DESC) != 2:
        sys.exit(
            f"build_mmri_pages: expected the share description twice, "
            f"found {s.count(OLD_DESC)}."
        )
    s = s.replace(OLD_DESC, DESC)

    return s


def main():
    built = build()
    check = "--check" in sys.argv
    current = OUT.read_text(encoding="utf-8") if OUT.exists() else None

    if check:
        if current != built:
            sys.exit(f"{OUT.name} is out of date — run: python3 tools/build_mmri_pages.py")
        print(f"{OUT.name} is up to date")
        return

    if current == built:
        print(f"{OUT.name} already current ({len(built)} bytes)")
        return
    OUT.write_text(built, encoding="utf-8")
    print(f"wrote {OUT.name} ({len(built)} bytes) from {SRC.name}")


if __name__ == "__main__":
    main()
