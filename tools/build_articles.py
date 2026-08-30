#!/usr/bin/env python3
"""
MAGICKMICA - build_articles.py
Extracts published articles from the two Substack export zips and
rebuilds _data/magazine_articles.json.

Cover-image picker (per the project rules):
  a) blacklist any image url appearing in >=3 posts across all exports
     (those are logos / banners / footers, not covers)
  b) take the FIRST substantial image (the hero), skipping thin banners
     (height < 100 or aspect > 4) and icons (min dimension < 400)
"""
import csv, json, os, re, glob
from collections import Counter

MANUAL_COVERS = {"the-starseed-chronicles": "starseed-chronicles-cover.jpg"}
NO_COVER_OK = {"we-fly-free", "the-daily-enchantment"}

IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"[^>]*>', re.I)
DIM_RE = re.compile(r"_(\d+)x(\d+)\.(?:png|jpe?g|webp|gif)", re.I)

# Article covers are served through the Substack CDN at w_600
# (notes use w_400). Format verified against the live articles.html.
COVER_CDN = ("https://substackcdn.com/image/fetch/"
             "$s_!G4Yk!,w_600,c_limit,f_webp,q_auto:good,fl_progressive:steep/")


def cdn_cover(image_url):
    from urllib.parse import quote
    return COVER_CDN + quote(image_url, safe="")


def slug_of(post_id):
    return post_id.split(".", 1)[1] if "." in post_id else post_id


def images_in(html_text):
    return IMG_RE.findall(html_text or "")


def dims(url):
    m = DIM_RE.search(url)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def usable(url):
    """Preferred-cover test. Deliberately strict: several posts open with a
    small decorative image before the real hero, and this skips those."""
    w, h = dims(url)
    if w is None:
        return True                      # unknown size: allow, order decides
    if h < 100:
        return False                     # thin banner
    if max(w, h) / max(min(w, h), 1) > 4:
        return False                     # extreme aspect = banner strip
    if min(w, h) < 400:
        return False                     # icon / avatar
    return True


def acceptable(url):
    """Fallback test, used only when no image passes `usable`. Still rejects
    banners and icons, but allows a modest hero (e.g. a 600x334 gif) rather
    than leaving the article with no cover at all."""
    w, h = dims(url)
    if w is None:
        return True
    if h < 100:
        return False
    if max(w, h) / max(min(w, h), 1) > 4:
        return False
    return max(w, h) >= 500


def area(url):
    w, h = dims(url)
    return (w or 0) * (h or 0)


def collect(export_dir, newsletter):
    posts_csv = os.path.join(export_dir, "posts.csv")
    rows = list(csv.DictReader(open(posts_csv, encoding="utf-8")))
    out = []
    for r in rows:
        if str(r.get("is_published", "")).lower() not in ("true", "1"):
            continue
        pid = r.get("post_id") or ""
        slug = slug_of(pid)
        path = os.path.join(export_dir, "posts", pid + ".html")
        body = ""
        if os.path.exists(path):
            body = open(path, encoding="utf-8", errors="replace").read()
        out.append({
            "post_id": pid,
            "slug": slug,
            "date": (r.get("post_date") or "")[:10],
            "published": r.get("post_date") or "",
            "type": r.get("type") or "",
            "audience": r.get("audience") or "",
            "title": (r.get("title") or "").strip(),
            "subtitle": (r.get("subtitle") or "").strip(),
            "newsletter": newsletter,
            "_images": images_in(body),
            "_body": body,
        })
    return out


def pick_covers(articles):
    freq = Counter()
    for a in articles:
        for u in set(a["_images"]):
            freq[u] += 1
    blacklist = {u for u, c in freq.items() if c >= 3}

    for a in articles:
        if a["slug"] in MANUAL_COVERS:
            # manual overrides point at local repo files, stored raw
            a["cover_url"] = MANUAL_COVERS[a["slug"]]
            continue
        cover = ""
        for u in a["_images"]:
            if u in blacklist or not usable(u):
                continue
            cover = u
            break
        if not cover:
            # nothing met the strict bar - take the largest acceptable image
            cands = [u for u in a["_images"]
                     if u not in blacklist and acceptable(u)]
            if cands:
                cover = max(cands, key=area)
        a["cover_url"] = cdn_cover(cover) if cover else ""
    return blacklist


def preview_of(body, n=200):
    text = re.sub(r"<[^>]+>", " ", body or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:n]


def dedupe(arts):
    """Some posts are cross-posted to both newsletters. One copy is an empty
    stub with no body file; keep whichever copy actually has content."""
    best = {}
    for a in arts:
        prev = best.get(a["slug"])
        if prev is None or len(a["_body"]) > len(prev["_body"]):
            best[a["slug"]] = a
    return list(best.values())


def build(uploads, data_dir, tv_dir, art_dir):
    arts = collect(tv_dir, "MagickMica TV") + collect(art_dir, "MagickMica Art")
    arts = dedupe(arts)
    blacklist = pick_covers(arts)

    for a in arts:
        base = ("https://magickmica.substack.com/p/"
                if a["newsletter"] == "MagickMica TV"
                else "https://magickmicaart.substack.com/p/")
        a["url"] = base + a["slug"]
        a["preview"] = preview_of(a.pop("_body"))
        a.pop("_images", None)

    arts.sort(key=lambda a: a["date"], reverse=True)
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "magazine_articles.json"), "w", encoding="utf-8") as f:
        json.dump(arts, f, ensure_ascii=False, separators=(",", ":"))
    return arts, blacklist


if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "_data"
    tv = sys.argv[2] if len(sys.argv) > 2 else "exp_tv"
    art = sys.argv[3] if len(sys.argv) > 3 else "exp_art"
    arts, bl = build(None, data_dir, tv, art)
    nocov = [a["slug"] for a in arts if not a["cover_url"]]
    print(f"articles: {len(arts)}  (TV {sum(1 for a in arts if a['newsletter']=='MagickMica TV')}, "
          f"Art {sum(1 for a in arts if a['newsletter']=='MagickMica Art')})")
    print(f"blacklisted repeat images: {len(bl)}")
    print(f"with covers: {sum(1 for a in arts if a['cover_url'])}  without: {len(nocov)}")
    for s in nocov:
        print("   no cover:", s)
