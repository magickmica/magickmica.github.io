#!/usr/bin/env python3
"""
MAGICKMICA - build_seo.py
Generates sitemap.xml and robots.txt for the whole site.

Priority reflects what is actually worth crawling: the homepage first,
then the hub pages, then the digests (which are static HTML with real
text, so they are the most indexable content on the site), then the
seasonal index variants last - those are near-duplicates of the
homepage and should not compete with it.
"""
import os, re, glob, datetime

SITE = "https://magickmica.github.io/"

# Seasonal homepage variants are near-duplicates of index.html.
# They stay in the sitemap at low priority but get a canonical pointing
# home so they never outrank or cannibalise the real homepage.
VARIANT_RE = re.compile(r"^index-.*\.html$")

PRIORITY = [
    ("index.html", "1.0", "daily"),
    ("notes.html", "0.9", "daily"),
    ("blog.html", "0.9", "daily"),
    ("articles.html", "0.8", "weekly"),
    ("archive.html", "0.8", "weekly"),
    ("minimags.html", "0.8", "weekly"),
    ("arcade.html", "0.7", "monthly"),
]


def entries(repo):
    seen, out = set(), []
    today = datetime.date.today().isoformat()

    for name, pri, freq in PRIORITY:
        if os.path.exists(os.path.join(repo, name)):
            out.append((name, pri, freq, today))
            seen.add(name)

    # digests: months slightly above weeks
    for f in sorted(glob.glob(os.path.join(repo, "month-*.html")), reverse=True):
        n = os.path.basename(f)
        out.append((n, "0.7", "monthly", today)); seen.add(n)
    for f in sorted(glob.glob(os.path.join(repo, "week-*.html")), reverse=True):
        n = os.path.basename(f)
        out.append((n, "0.6", "monthly", today)); seen.add(n)

    # everything else at the repo root
    for f in sorted(glob.glob(os.path.join(repo, "*.html"))):
        n = os.path.basename(f)
        if n in seen or n == "404.html":
            continue
        pri = "0.3" if VARIANT_RE.match(n) else "0.5"
        out.append((n, pri, "monthly", today))
    return out


def build(repo, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows = entries(repo)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name, pri, freq, lastmod in rows:
        loc = SITE + ("" if name == "index.html" else name)
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{pri}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(out_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# Backup bundles, not content\n"
        "Disallow: /files.zip\n"
        "\n"
        f"Sitemap: {SITE}sitemap.xml\n"
    )
    with open(os.path.join(out_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    return len(rows)


if __name__ == "__main__":
    import sys
    repo = sys.argv[1] if len(sys.argv) > 1 else "magickmica.github.io-main"
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "build"
    n = build(repo, out_dir)
    print(f"sitemap.xml: {n} urls")
    print("robots.txt written")
