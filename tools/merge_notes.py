#!/usr/bin/env python3
"""
MAGICKMICA - merge_notes.py
Rebuilds _data/notes_with_media_compact.json from:
  - the existing master (or the NOTES blob inside notes.html as a fallback)
  - a fresh notes_refresh.json collected by collect_notes.js

Compact record shape:  {d, l, r, id, b, t}
  d = date YYYY-MM-DD   l = likes   r = restacks
  id = note id          b = body    t = cdn image url (or absent)
"""
import json, os, re
from urllib.parse import quote

CDN_SIG = "$s_!G4Yk!,w_400,c_limit,f_webp,q_auto:good,fl_progressive:steep"
CDN_BASE = "https://substackcdn.com/image/fetch/" + CDN_SIG + "/"
HANDLE = "magickmica"


def cdn(image_url: str) -> str:
    """Wrap a raw S3 image url in the Substack CDN fetch url, width 400."""
    return CDN_BASE + quote(image_url, safe="")


def load_master(data_dir: str, notes_html: str | None = None) -> list:
    """Load the master archive, falling back to the NOTES blob in notes.html."""
    path = os.path.join(data_dir, "notes_with_media_compact.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    if notes_html and os.path.exists(notes_html):
        with open(notes_html, encoding="utf-8") as f:
            html = f.read()
        m = re.search(r"const\s+NOTES\s*=\s*(\[.*?\]);", html, re.DOTALL)
        if m:
            return json.loads(m.group(1))
    return []


def parse_refresh(refresh_path: str) -> list:
    """Turn raw collector output into compact records (own notes only)."""
    with open(refresh_path, encoding="utf-8") as f:
        raw = json.load(f)

    out = []
    for item in raw:
        c = item.get("comment") or {}
        if c.get("handle") != HANDLE:
            continue
        nid = c.get("id")
        if nid is None:
            continue
        date = (c.get("date") or "")[:10]
        if not date:
            continue

        rec = {
            "d": date,
            "l": int(c.get("reaction_count") or 0),
            "r": int(c.get("restacks") or 0),
            "id": int(nid),
            "b": c.get("body") or "",
        }
        for a in c.get("attachments") or []:
            if a.get("type") == "image" and a.get("imageUrl"):
                rec["t"] = cdn(a["imageUrl"])
                break
        out.append(rec)
    return out


def merge(master: list, fresh: list) -> tuple[list, dict]:
    """Merge fresh over master, keyed by id. Fresh wins (newer like counts)."""
    by_id = {int(n["id"]): n for n in master if n.get("id") is not None}
    before = len(by_id)

    added = updated = 0
    for rec in fresh:
        nid = rec["id"]
        if nid in by_id:
            old = by_id[nid]
            if old.get("l") != rec["l"] or old.get("r") != rec["r"]:
                updated += 1
            # keep an existing image if the fresh copy somehow lacks one
            if "t" in old and "t" not in rec:
                rec["t"] = old["t"]
            by_id[nid] = rec
        else:
            by_id[nid] = rec
            added += 1

    merged = sorted(by_id.values(), key=lambda n: (n.get("d", ""), n["id"]))
    stats = {
        "before": before,
        "after": len(merged),
        "added": added,
        "engagement_updated": updated,
        "with_images": sum(1 for n in merged if n.get("t")),
    }
    return merged, stats


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "magickmica.github.io-main"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "_data"
    refresh = sys.argv[3] if len(sys.argv) > 3 else "/mnt/user-data/uploads/notes_refresh.json"

    os.makedirs(data_dir, exist_ok=True)
    master = load_master(data_dir, os.path.join(repo, "notes.html"))
    fresh = parse_refresh(refresh)
    merged, stats = merge(master, fresh)

    with open(os.path.join(data_dir, "notes_with_media_compact.json"), "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, separators=(",", ":"))

    print(json.dumps(stats, indent=2))
    dates = [n["d"] for n in merged if n.get("d")]
    print(f"range: {min(dates)} -> {max(dates)}")
