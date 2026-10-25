#!/usr/bin/env python3
"""
MAGICKMICA - update_all.py  ·  one update for the whole site

    python3 tools/update_all.py                       # uses every .json in incoming/
    python3 tools/update_all.py get-notes-….json get-articles-….json …
    python3 tools/update_all.py --rebuild             # no new exports: rebuild from _data/

Runs, in order:
  1. merge_notes.py      GET NOTES! file(s)     -> _data/notes_with_media_compact.json
  2. merge_articles.py   GET ARTICLES! file(s)  -> _data/magazine_articles.json
  3. build_digests.py    week-*.html, month-*.html
  4. update_pages.py     notes.html, articles.html, archive.html, minimags.html,
                         blog.html, random-note.html, arcade.html, index*.html, pools.js
  5. signal/build_signal.py, almanac/build_almanac.py, reader/build_reader.py

Run it from anywhere; it finds the repo from its own location. Files are
written straight into the repo, so the changes are ready to commit.
On GitHub, .github/workflows/update-site.yml runs this automatically whenever
export files are uploaded into incoming/.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
DATA = os.path.join(REPO, "_data")
BUILD = os.path.join(REPO, ".build-tmp")
PY = sys.executable


def step(title):
    print(f"\n=== {title}")


def run(*args):
    subprocess.run([PY, *args], cwd=REPO, check=True)


def kind_of(path):
    """GET NOTES! / GET ARTICLES! file, or the older collect_notes.js list."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError):
        return None
    if isinstance(raw, dict):
        app = (raw.get("app") or "").upper()
        if "NOTES" in app or "notes" in raw:
            return "notes"
        if "ARTICLES" in app or "posts" in raw:
            return "articles"
    if isinstance(raw, list):
        return "notes"
    return None


def copy_build_into_repo():
    if not os.path.isdir(BUILD):
        return []
    copied = []
    for root, dirs, files in os.walk(BUILD):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            src = os.path.join(root, name)
            rel = os.path.relpath(src, BUILD)
            dst = os.path.join(REPO, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            copied.append(rel)
    shutil.rmtree(BUILD, ignore_errors=True)
    return copied


def main(argv):
    rebuild_only = "--rebuild" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files and not rebuild_only:
        files = sorted(glob.glob(os.path.join(REPO, "incoming", "*.json")))
    notes_files = [f for f in files if kind_of(f) == "notes"]
    article_files = [f for f in files if kind_of(f) == "articles"]
    unknown = [f for f in files if f not in notes_files and f not in article_files]
    if unknown:
        print("Skipped (not a GET NOTES! or GET ARTICLES! file):")
        for f in unknown:
            print("  ", f)
    if not notes_files and not article_files and not rebuild_only:
        print("No export files found. Put them in incoming/ or name them on the command line,")
        print("or run with --rebuild to rebuild every page from the current _data/.")
        return 1

    shutil.rmtree(BUILD, ignore_errors=True)

    for f in notes_files:
        step(f"Notes: {os.path.basename(f)}")
        run(os.path.join(TOOLS, "merge_notes.py"), REPO, DATA, f)
    if article_files:
        step("Articles")
        run(os.path.join(TOOLS, "merge_articles.py"), DATA, *article_files)

    step("Y3K weekly and monthly issues")
    run(os.path.join(TOOLS, "build_digests.py"), REPO, DATA, BUILD)
    digests = copy_build_into_repo()          # minimags.html links to these, so they go in first

    step("Site pages: notes, articles, archive, minimags, blog, homepages")
    run(os.path.join(TOOLS, "update_pages.py"), REPO, DATA, BUILD)
    pages = copy_build_into_repo()

    step("Signal Band, Almanac, Transmission Reader 98")
    for b in ("signal/build_signal.py", "almanac/build_almanac.py", "reader/build_reader.py"):
        if os.path.exists(os.path.join(REPO, b)):
            run(os.path.join(REPO, b))

    with open(os.path.join(DATA, "notes_with_media_compact.json"), encoding="utf-8") as f:
        notes = json.load(f)
    with open(os.path.join(DATA, "magazine_articles.json"), encoding="utf-8") as f:
        arts = json.load(f)
    print("\n=== Done")
    print(f"{len(notes):,} notes through {max(n['d'] for n in notes)}, {len(arts)} articles")
    print(f"{len(digests)} issue pages and {len(pages)} site files updated, "
          "plus the Signal Band, Almanac and Reader data.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
