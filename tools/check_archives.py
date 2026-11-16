#!/usr/bin/env python3
"""
MAGICKMICA - check_archives.py  ·  safety check for notes.html and minimags.html

    python3 tools/check_archives.py            # from anywhere; finds the repo itself

Read-only: it never writes into the repo. Run it after any change to
notes.html, minimags.html or tools/update_pages.py, and before uploading.

It answers one question: will the "Update site from exports" workflow
still be able to update both archive pages, and is every note and
issue still there?

  notes.html
    - exactly one `const NOTES = [...]` block, which update_pages.py can find
    - it holds every note in _data/notes_with_media_compact.json (same ids)
    - a dry run of update_pages.inject() on a copy succeeds
  minimags.html
    - the #wGrid / #mGrid grids and both end markers update_pages.py needs
    - one weekly card per real week and one monthly card per real month,
      newest first, matching what update_pages.py would build from _data/
    - every card links to an issue page that exists
    - a dry run of update_pages.rebuild_minimags() on a copy succeeds
  shared
    - archive.css / archive.js exist if a page links to them
  optional (warnings only)
    - the spots the Substack subscribe box (tools/add_subscribe.py) and the
      store strip (mm-store.js placers) look for are still there

Exit code 0 = all good, 1 = something would break.
"""
import json
import os
import re
import shutil
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
DATA = os.path.join(REPO, "_data")
sys.path.insert(0, TOOLS)
import update_pages as up  # noqa: E402  (the real script, so the check can't drift from it)

FAILS, WARNS = [], []


def ok(msg):
    print("  ok    " + msg)


def fail(msg):
    FAILS.append(msg)
    print("  FAIL  " + msg)


def warn(msg):
    WARNS.append(msg)
    print("  warn  " + msg)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# the exact markers update_pages.rebuild_minimags() uses
W_END = '</div>\n<div class="issues-grid hidden" id="mGrid"'
M_END = "</div>\n<footer>"


def check_notes(notes):
    print("\nnotes.html")
    path = os.path.join(REPO, "notes.html")
    if not os.path.exists(path):
        fail("notes.html is missing")
        return
    html = read(path)
    decls = re.findall(r"const\s+NOTES\s*=", html)
    if len(decls) != 1:
        fail(f"expected exactly one `const NOTES =`, found {len(decls)}")
        return
    blob = up.read_blob(html, "NOTES")
    if blob is None:
        fail("update_pages.py cannot read the NOTES block (pattern or JSON broken)")
        return
    ok("one NOTES block, readable by update_pages.py")
    want = {int(n["id"]) for n in notes}
    have = {int(n["id"]) for n in blob}
    if have == want:
        ok(f"all {len(want):,} notes present, same ids as _data/")
    else:
        missing, extra = want - have, have - want
        if missing:
            fail(f"{len(missing)} notes in _data/ are missing from the page (e.g. {sorted(missing)[:3]})")
        if extra:
            warn(f"{len(extra)} notes on the page are not in _data/ yet; the next update adds them to _data/")
    # dry run on a copy: empty the block, inject, and read it back
    emptied, found = up.inject(html, "NOTES", [])
    if not found:
        fail("update_pages.inject() did not find NOTES")
        return
    refilled, found = up.inject(emptied, "NOTES", notes)
    back = up.read_blob(refilled, "NOTES") or []
    if found and len(back) == len(notes):
        ok("dry run: update_pages.py re-injects every note")
    else:
        fail("dry run: re-injection lost notes")
    if 'id="resultsInfo"' not in html or 'id="grid"' not in html:
        warn('#resultsInfo / #grid are gone: tools/add_subscribe.py (subscribe box) will not find its spot')
    if "placeStoreStrip" in html and 'class="card' not in html and "'card'" not in html and "ar-card" not in html:
        warn("placeStoreStrip() counts .card elements; check the store strip still lands in the grid")


def expected_issues(notes):
    weeks = sorted(up.group_by_week(notes), reverse=True)
    months = sorted({n["d"][:7] for n in notes} - up.SKIP_MONTHS, reverse=True)
    return [f"week-{w}.html" for w in weeks], [f"month-{m}.html" for m in months]


def card_hrefs(html, grid_id, end_marker):
    m = re.search(r'<div[^>]*id="' + grid_id + r'"[^>]*>', html)
    if not m:
        return None
    end = html.find(end_marker, m.end())
    if end == -1:
        return None
    return re.findall(r'<a[^>]*class="[^"]*issue-card[^"]*"[^>]*href="([^"]+)"', html[m.end():end]) or \
        re.findall(r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*issue-card', html[m.end():end])


def check_minimags(notes):
    print("\nminimags.html")
    path = os.path.join(REPO, "minimags.html")
    if not os.path.exists(path):
        fail("minimags.html is missing")
        return
    html = read(path)
    good = True
    if not re.search(r'<div[^>]*id="wGrid"[^>]*>', html):
        fail('weekly grid <div id="wGrid"> not found'); good = False
    if not re.search(r'<div[^>]*id="mGrid"[^>]*>', html):
        fail('monthly grid <div id="mGrid"> not found'); good = False
    if W_END not in html:
        fail('end marker after the weekly grid is gone: "</div>" + newline + '
             '<div class="issues-grid hidden" id="mGrid"'); good = False
    if M_END not in html:
        fail('end marker after the monthly grid is gone: "</div>" + newline + "<footer>"'); good = False
    if not good:
        print("        (update_pages.py would silently stop adding new editions)")
        return
    ok("both grids and both end markers present")

    want_w, want_m = expected_issues(notes)
    have_w = card_hrefs(html, "wGrid", W_END) or []
    have_m = card_hrefs(html, "mGrid", M_END) or []
    for name, have, want in (("weekly", have_w, want_w), ("monthly", have_m, want_m)):
        if have == want:
            ok(f"{len(have)} {name} cards, newest first, match _data/")
        else:
            gone = [h for h in want if h not in have]
            new = [h for h in have if h not in want]
            if gone and set(gone) <= {want[0]}:
                warn(f"{name}: newest issue {gone[0]} not on the page yet; the next update adds it")
            elif gone:
                fail(f"{name}: {len(gone)} issues missing from the page (e.g. {gone[:3]})")
            if new:
                fail(f"{name}: {len(new)} cards with no matching data (e.g. {new[:3]})")
            if not gone and not new:
                fail(f"{name}: cards are out of order")
    missing_files = [h for h in have_w + have_m if not os.path.exists(os.path.join(REPO, h))]
    if missing_files:
        fail(f"{len(missing_files)} cards link to pages that do not exist (e.g. {missing_files[:3]})")
    else:
        ok(f"all {len(have_w) + len(have_m)} card links point to existing issue pages")

    # dry run on a copy: drop the newest weekly card, rebuild, expect it back
    tmp = tempfile.mkdtemp(prefix="mm-check-")
    try:
        repo, out = os.path.join(tmp, "repo"), os.path.join(tmp, "out")
        os.makedirs(repo)
        trimmed = re.sub(r'<a class="issue-card".*?</a>', "", html, count=1, flags=re.S)
        with open(os.path.join(repo, "minimags.html"), "w", encoding="utf-8") as f:
            f.write(trimmed)
        os.makedirs(out)
        if up.rebuild_minimags(repo, out, notes):
            rebuilt = read(os.path.join(out, "minimags.html"))
            rw = card_hrefs(rebuilt, "wGrid", W_END) or []
            rm = card_hrefs(rebuilt, "mGrid", M_END) or []
            if rw == want_w and rm == want_m:
                ok("dry run: update_pages.py rebuilds every weekly and monthly card")
            else:
                fail(f"dry run: rebuild produced {len(rw)} weekly / {len(rm)} monthly cards, "
                     f"expected {len(want_w)} / {len(want_m)}")
        else:
            fail("dry run: update_pages.rebuild_minimags() returned False (markers not matched)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if "mms-wrap" not in html and "mm-store.js" in html and "issue-card" not in html:
        warn("store strip placer counts .issue-card; check it still lands in the grid")


def check_shared():
    print("\nshared files")
    for page in ("notes.html", "minimags.html"):
        p = os.path.join(REPO, page)
        if not os.path.exists(p):
            continue
        html = read(p)
        for asset in ("archive.css", "archive.js"):
            if re.search(r'(?:href|src)="' + re.escape(asset), html):
                if os.path.exists(os.path.join(REPO, asset)):
                    ok(f"{page} links {asset}, and it exists")
                else:
                    fail(f"{page} links {asset}, but the file is missing")


def check_explore(notes):
    path = os.path.join(REPO, "explore", "notes-data.js")
    if not os.path.isdir(os.path.join(REPO, "explore")):
        return
    print("\nexplore/")
    if not os.path.exists(path):
        fail("explore/notes-data.js is missing: run python3 explore/build_explore.py")
        return
    text = read(path)
    try:
        data = json.loads(text.split("window.MM_NOTES = ", 1)[1].rstrip().rstrip(";"))
    except Exception:
        fail("explore/notes-data.js is not readable")
        return
    have = {row[0] for row in data.get("notes", [])}
    hidden = set()
    hp = os.path.join(DATA, "explore_hidden.json")
    if os.path.exists(hp):
        hidden = {int(h["id"]) for h in json.load(open(hp, encoding="utf-8")).get("hidden", [])}
    want = {int(n["id"]) for n in notes} - hidden
    if have == want:
        ok(f"notes-data.js holds all {len(want):,} notes" + (f" ({len(hidden)} hidden on purpose)" if hidden else ""))
    else:
        fail(f"notes-data.js is out of step with _data/ ({len(have):,} vs {len(want):,}): "
             "run python3 explore/build_explore.py")
    for page in ("index.html", "book.html", "gallery.html", "tapes.html", "sky.html", "themes.html", "hall.html"):
        if not os.path.exists(os.path.join(REPO, "explore", page)):
            fail(f"explore/{page} is missing")


def main():
    print("MAGICKMICA archive check:", REPO)
    with open(os.path.join(DATA, "notes_with_media_compact.json"), encoding="utf-8") as f:
        notes = json.load(f)
    print(f"_data/: {len(notes):,} notes, {min(n['d'] for n in notes)} to {max(n['d'] for n in notes)}")
    check_notes(notes)
    check_minimags(notes)
    check_shared()
    check_explore(notes)
    print()
    if FAILS:
        print(f"{len(FAILS)} problem(s) would break the archives or the update workflow.")
        return 1
    print("All good" + (f" ({len(WARNS)} warning(s))." if WARNS else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
