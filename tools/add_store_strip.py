#!/usr/bin/env python3
"""Put the shop strip on every page.

mm-store.js is self-contained, so a page only needs the one script tag. This
adds it just before </body>, after mm-nav.js where that is already there so
the two load in a predictable order.

    python3 tools/add_store_strip.py            # add it
    python3 tools/add_store_strip.py --check    # list pages still missing it

Idempotent: a page that already has the tag is left alone, so re-running
after adding new pages only touches the new ones.
"""

import glob
import os
import re
import sys

TAG = '<script src="mm-store.js?v=1" defer></script>'
NAV = re.compile(r'(<script src="mm-nav\.js[^"]*"[^>]*></script>)')

# Pages where a shop strip does not belong. The collector and meme tools are
# utilities people use rather than read, and the verification file is not a
# page at all.
SKIP = {
    "google7a658e18c43e8a60.html",
    "404.html",
}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "."
    check = "--check" in sys.argv

    added, already, skipped, nobody = [], [], [], []

    for path in sorted(glob.glob(os.path.join(root, "*.html"))):
        name = os.path.basename(path)
        if name in SKIP:
            skipped.append(name)
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        if "mm-store.js" in html:
            already.append(name)
            continue
        if "</body>" not in html:
            nobody.append(name)
            continue
        if check:
            added.append(name)
            continue

        if NAV.search(html):
            out = NAV.sub(lambda m: m.group(1) + "\n" + TAG, html, count=1)
        else:
            idx = html.rfind("</body>")
            out = html[:idx] + TAG + "\n" + html[idx:]

        # The only thing that may change is the one tag we inserted.
        assert out.replace(TAG + "\n", "", 1) == html, f"{name}: unexpected edit"
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        added.append(name)

    verb = "would add to" if check else "added to"
    print(f"{verb} {len(added)} pages; {len(already)} already had it; "
          f"{len(skipped)} skipped; {len(nobody)} had no </body>")
    for n in nobody:
        print("  no </body>:", n)
    if check and added:
        for n in added[:20]:
            print("  missing:", n)
        if len(added) > 20:
            print(f"  … and {len(added) - 20} more")
    return 1 if (check and added) else 0


if __name__ == "__main__":
    sys.exit(main())
