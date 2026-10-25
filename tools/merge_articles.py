#!/usr/bin/env python3
"""
MAGICKMICA - merge_articles.py
Merges GET ARTICLES! files (get-articles.html) into _data/magazine_articles.json.

    python3 tools/merge_articles.py _data get-articles-magickmica.substack.com-2026-10-25.json [...]

- Posts already in the archive keep their cover and preview, and gain fresh
  likes / comments / restacks / words.
- New posts are added with a cover in the same CDN format build_articles.py uses.
- Restacks of the other newsletter's posts are never added as new posts.
- Which newsletter a file belongs to comes from its "site" field.

build_articles.py (Substack's own export zips) still works; it rebuilds the
archive from scratch, after which this tool can add the engagement numbers again.
"""
import json
import os
import sys
from urllib.parse import quote

COVER_CDN = ("https://substackcdn.com/image/fetch/"
             "$s_!G4Yk!,w_600,c_limit,f_webp,q_auto:good,fl_progressive:steep/")
RAW_S3 = "https://substack-post-media.s3.amazonaws.com/"


def cover_of(url):
    if not url:
        return ""
    if url.startswith(RAW_S3):
        return COVER_CDN + quote(url, safe="")
    return url


def newsletter_of(site):
    return "MagickMica Art" if "art" in (site or "").lower() else "MagickMica TV"


def merge(archive, raw):
    posts = raw.get("posts") or []
    nl = newsletter_of(raw.get("site"))
    by_slug = {a["slug"]: a for a in archive}
    added, updated = [], 0
    for p in posts:
        slug = p.get("slug")
        if not slug:
            continue
        stats = {k: int(p.get(k) or 0) for k in ("likes", "comments", "restacks", "words")}
        a = by_slug.get(slug)
        if a:
            a.update(stats)
            updated += 1
            continue
        if p.get("type") == "restack":
            continue
        rec = {
            "post_id": f'{p.get("id")}.{slug}',
            "slug": slug,
            "date": (p.get("date") or "")[:10],
            "published": p.get("date") or "",
            "type": p.get("type") or "newsletter",
            "audience": p.get("audience") or "everyone",
            "title": (p.get("title") or "").strip(),
            "subtitle": (p.get("subtitle") or "").strip(),
            "newsletter": nl,
            "cover_url": cover_of(p.get("cover")),
            "url": p.get("url") or "",
            "preview": (p.get("description") or "").strip(),
        }
        rec.update(stats)
        archive.append(rec)
        by_slug[slug] = rec
        added.append(rec)
    archive.sort(key=lambda a: a.get("date", ""), reverse=True)
    return archive, added, updated


def main(data_dir, files):
    path = os.path.join(data_dir, "magazine_articles.json")
    with open(path, encoding="utf-8") as f:
        archive = json.load(f)
    for src in files:
        with open(src, encoding="utf-8") as f:
            raw = json.load(f)
        archive, added, updated = merge(archive, raw)
        print(f"{os.path.basename(src)}: {updated} updated, {len(added)} added")
        for a in added:
            print(f"   + {a['date']}  {a['title']}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, separators=(",", ":"))
    print(f"magazine_articles.json: {len(archive)} articles")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: merge_articles.py <data_dir> <get-articles-….json> [...]")
    main(sys.argv[1], sys.argv[2:])
